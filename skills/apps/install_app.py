"""
📦 Install Application Skill
Installs applications from various sources
"""

import os
import subprocess

import requests
from colorama import Fore, Style


class InstallApp:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts

    def execute(self, params):
        """📦 Execute app installation"""
        app_name = params.get("app_name", "").lower()
        source = params.get("source", "winget").lower()

        if not app_name:
            self.tts.speak("Sir, kaunsi app install karni hai?")
            return {"success": False, "error": "No app name"}

        print(
            Fore.YELLOW
            + f"📦 Installing app: {app_name} from {source}"
            + Style.RESET_ALL
        )

        # Check if already installed
        if self.is_app_installed(app_name):
            self.tts.speak(f"Sir, {app_name} already installed hai")
            return {"success": False, "error": "App already installed"}

        # Install based on source
        if source == "winget":
            result = self.install_via_winget(app_name)
        elif source == "chocolatey":
            result = self.install_via_chocolatey(app_name)
        elif source == "scoop":
            result = self.install_via_scoop(app_name)
        elif source == "direct":
            result = self.install_direct_download(app_name)
        else:
            result = self.install_via_winget(app_name)  # Default

        if result["success"]:
            self.tts.speak(f"Sir, {app_name} install ho gaya")
            return {"success": True, "speak": f"{app_name} installed successfully"}
        else:
            self.tts.speak(f"Sir, {app_name} install nahi kar paya")
            return result

    def is_app_installed(self, app_name):
        """📦 Check if app is already installed"""
        try:
            # Try winget list
            result = subprocess.run(["winget", "list"], capture_output=True, text=True)

            if result.returncode == 0:
                # Check if app is in list
                for line in result.stdout.split("\n"):
                    if app_name.lower() in line.lower():
                        return True

            return False

        except:
            return False

    def install_via_winget(self, app_name):
        """📦 Install app using winget"""
        try:
            print(Fore.CYAN + f"  Installing via winget: {app_name}" + Style.RESET_ALL)

            # Search for app first
            search_cmd = ["winget", "search", app_name]
            search_result = subprocess.run(search_cmd, capture_output=True, text=True)

            if search_result.returncode != 0:
                return {"success": False, "error": "Winget search failed"}

            # Parse search results
            lines = search_result.stdout.split("\n")
            if len(lines) < 3:
                return {"success": False, "error": "No results found"}

            # Get first result (skip headers)
            for i in range(2, len(lines)):
                if lines[i].strip():
                    parts = lines[i].split()
                    if len(parts) >= 2:
                        exact_name = parts[0]

                        # Install the app
                        install_cmd = [
                            "winget",
                            "install",
                            "--id",
                            exact_name,
                            "--silent",
                            "--accept-package-agreements",
                            "--accept-source-agreements",
                        ]
                        install_result = subprocess.run(
                            install_cmd, capture_output=True, text=True
                        )

                        if install_result.returncode == 0:
                            print(
                                Fore.GREEN
                                + f"  ✅ Installed via winget: {exact_name}"
                                + Style.RESET_ALL
                            )
                            return {
                                "success": True,
                                "method": "winget",
                                "app": exact_name,
                            }
                        else:
                            # Try without silent mode
                            install_cmd = ["winget", "install", exact_name]
                            install_result = subprocess.run(
                                install_cmd, capture_output=True, text=True
                            )

                            if install_result.returncode == 0:
                                return {
                                    "success": True,
                                    "method": "winget_interactive",
                                    "app": exact_name,
                                }

            return {"success": False, "error": "Installation failed"}

        except FileNotFoundError:
            return {"success": False, "error": "Winget not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def install_via_chocolatey(self, app_name):
        """📦 Install app using Chocolatey"""
        try:
            print(
                Fore.CYAN + f"  Installing via Chocolatey: {app_name}" + Style.RESET_ALL
            )

            # Check if Chocolatey is installed
            choco_check = subprocess.run(
                ["choco", "--version"], capture_output=True, text=True
            )

            if choco_check.returncode != 0:
                return {"success": False, "error": "Chocolatey not installed"}

            # Install app
            install_cmd = ["choco", "install", app_name, "-y"]
            install_result = subprocess.run(install_cmd, capture_output=True, text=True)

            if install_result.returncode == 0:
                print(
                    Fore.GREEN
                    + f"  ✅ Installed via Chocolatey: {app_name}"
                    + Style.RESET_ALL
                )
                return {"success": True, "method": "chocolatey"}
            else:
                return {"success": False, "error": "Chocolatey installation failed"}

        except FileNotFoundError:
            return {"success": False, "error": "Chocolatey not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def install_via_scoop(self, app_name):
        """📦 Install app using Scoop"""
        try:
            print(Fore.CYAN + f"  Installing via Scoop: {app_name}" + Style.RESET_ALL)

            # Check if Scoop is installed
            scoop_check = subprocess.run(
                ["scoop", "--version"], capture_output=True, text=True
            )

            if scoop_check.returncode != 0:
                return {"success": False, "error": "Scoop not installed"}

            # Install app
            install_cmd = ["scoop", "install", app_name]
            install_result = subprocess.run(install_cmd, capture_output=True, text=True)

            if install_result.returncode == 0:
                print(
                    Fore.GREEN
                    + f"  ✅ Installed via Scoop: {app_name}"
                    + Style.RESET_ALL
                )
                return {"success": True, "method": "scoop"}
            else:
                return {"success": False, "error": "Scoop installation failed"}

        except FileNotFoundError:
            return {"success": False, "error": "Scoop not installed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def install_direct_download(self, app_name):
        """📦 Install app via direct download"""
        try:
            print(Fore.CYAN + f"  Downloading directly: {app_name}" + Style.RESET_ALL)

            # Map common apps to their download URLs
            app_urls = {
                "chrome": "https://dl.google.com/chrome/install/standalonesetup.exe",
                "firefox": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US",
                "vscode": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user",
                "whatsapp": "https://web.whatsapp.com/desktop/windows/release/x64/WhatsAppSetup.exe",
                "spotify": "https://download.scdn.co/SpotifySetup.exe",
                "discord": "https://dl.discordapp.net/apps/win/DiscordSetup.exe",
                "telegram": "https://telegram.org/dl/desktop/win64",
                "python": "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe",
                "notepad++": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.4.7/npp.8.4.7.Installer.x64.exe",
                "vlc": "https://get.videolan.org/vlc/3.0.16/win64/vlc-3.0.16-win64.exe",
            }

            # Check if app is in our list
            app_key = None
            for key in app_urls.keys():
                if key in app_name.lower():
                    app_key = key
                    break

            if not app_key:
                return {"success": False, "error": "Direct download URL not available"}

            download_url = app_urls[app_key]

            # Download the installer
            downloads_dir = os.path.expanduser("~/Downloads")
            installer_name = f"{app_key}_installer.exe"
            installer_path = os.path.join(downloads_dir, installer_name)

            print(Fore.YELLOW + f"  Downloading from: {download_url}" + Style.RESET_ALL)

            # Download file
            response = requests.get(download_url, stream=True)

            if response.status_code == 200:
                with open(installer_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(
                    Fore.GREEN + f"  ✅ Downloaded: {installer_path}" + Style.RESET_ALL
                )

                # Run installer
                print(Fore.YELLOW + f"  Running installer..." + Style.RESET_ALL)

                # Try silent install first
                install_cmd = [installer_path, "/S", "/quiet", "/norestart"]
                install_result = subprocess.run(
                    install_cmd, capture_output=True, text=True
                )

                if install_result.returncode == 0:
                    print(
                        Fore.GREEN
                        + f"  ✅ Installed via direct download: {app_key}"
                        + Style.RESET_ALL
                    )

                    # Cleanup installer
                    os.remove(installer_path)

                    return {
                        "success": True,
                        "method": "direct_download",
                        "app": app_key,
                    }
                else:
                    # Try normal install
                    install_cmd = [installer_path]
                    install_result = subprocess.run(install_cmd)

                    if install_result.returncode == 0:
                        return {
                            "success": True,
                            "method": "direct_download_interactive",
                            "app": app_key,
                        }
                    else:
                        return {"success": False, "error": "Installation failed"}
            else:
                return {
                    "success": False,
                    "error": f"Download failed: {response.status_code}",
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_package_manager_available(self):
        """📦 Check which package managers are available"""
        available = []

        # Check winget
        try:
            subprocess.run(["winget", "--version"], capture_output=True)
            available.append("winget")
        except:
            pass

        # Check chocolatey
        try:
            subprocess.run(["choco", "--version"], capture_output=True)
            available.append("chocolatey")
        except:
            pass

        # Check scoop
        try:
            subprocess.run(["scoop", "--version"], capture_output=True)
            available.append("scoop")
        except:
            pass

        return available

    def suggest_app_sources(self, app_name):
        """📦 Suggest where to get the app from"""
        suggestions = []

        # Common app mappings
        common_apps = {
            "chrome": ["winget", "direct"],
            "firefox": ["winget", "direct"],
            "vscode": ["winget", "direct"],
            "whatsapp": ["direct"],
            "spotify": ["winget", "direct"],
            "discord": ["winget", "direct"],
            "python": ["winget", "direct"],
            "nodejs": ["winget", "chocolatey"],
            "git": ["winget", "chocolatey"],
            "docker": ["winget", "chocolatey"],
        }

        for key, sources in common_apps.items():
            if key in app_name.lower():
                suggestions.extend(sources)
                break

        # Add generic suggestions
        if not suggestions:
            available_managers = self.check_package_manager_available()
            if available_managers:
                suggestions.extend(available_managers)
            else:
                suggestions.append("direct")

        return list(set(suggestions))  # Remove duplicates
