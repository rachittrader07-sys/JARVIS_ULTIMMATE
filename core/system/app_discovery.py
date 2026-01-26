"""
🔍 App Discovery
Discovers installed applications on the system
"""

import os
import subprocess
import sys
import winreg

from colorama import Fore, Style


class AppDiscovery:
    def __init__(self, config):
        self.config = config
        self.installed_apps = []
        self.app_cache = {}

        # Discover apps on initialization
        self.discover_apps()

    def discover_apps(self):
        """🔍 Discover all installed applications"""
        print(
            Fore.YELLOW + "🔍 Discovering installed applications..." + Style.RESET_ALL
        )

        all_apps = []

        # Method 1: Registry (Windows)
        all_apps.extend(self.discover_from_registry())

        # Method 2: Start Menu
        all_apps.extend(self.discover_from_start_menu())

        # Method 3: Common Program Files directories
        all_apps.extend(self.discover_from_program_files())

        # Method 4: User AppData
        all_apps.extend(self.discover_from_appdata())

        # Remove duplicates
        unique_apps = []
        seen_names = set()

        for app in all_apps:
            name = app.get("name", "").lower()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_apps.append(app)

        self.installed_apps = unique_apps
        self.app_cache = {app["name"].lower(): app for app in unique_apps}

        print(
            Fore.GREEN
            + f"✅ Discovered {len(self.installed_apps)} applications"
            + Style.RESET_ALL
        )

        return self.installed_apps

    @staticmethod
    def discover_from_registry():
        """🔍 Discover apps from Windows Registry"""
        apps = []
        registry_paths = [
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
            (
                winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            ),
        ]

        for hive, path in registry_paths:
            try:
                key = winreg.OpenKey(hive, path)
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        # Get app information
                        app_info = {}

                        try:
                            display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if display_name:
                                app_info["name"] = display_name
                        except:
                            continue

                        try:
                            display_version = winreg.QueryValueEx(
                                subkey, "DisplayVersion"
                            )[0]
                            app_info["version"] = display_version
                        except:
                            pass

                        try:
                            install_location = winreg.QueryValueEx(
                                subkey, "InstallLocation"
                            )[0]
                            app_info["path"] = install_location
                        except:
                            pass

                        try:
                            publisher = winreg.QueryValueEx(subkey, "Publisher")[0]
                            app_info["publisher"] = publisher
                        except:
                            pass

                        try:
                            uninstall_string = winreg.QueryValueEx(
                                subkey, "UninstallString"
                            )[0]
                            app_info["uninstall"] = uninstall_string
                        except:
                            pass

                        if "name" in app_info:
                            apps.append(app_info)

                        winreg.CloseKey(subkey)
                    except:
                        continue

                winreg.CloseKey(key)
            except:
                continue

        return apps

    @staticmethod
    def discover_from_start_menu():
        """🔍 Discover apps from Start Menu shortcuts"""
        apps = []
        start_menu_paths = [
            os.path.join(
                os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs"
            ),
            os.path.join(
                os.environ["PROGRAMDATA"], r"Microsoft\Windows\Start Menu\Programs"
            ),
        ]

        for start_menu_path in start_menu_paths:
            if os.path.exists(start_menu_path):
                for root, dirs, files in os.walk(start_menu_path):
                    for file in files:
                        if file.endswith(".lnk"):
                            app_name = os.path.splitext(file)[0]
                            app_path = os.path.join(root, file)

                            apps.append(
                                {
                                    "name": app_name,
                                    "shortcut": app_path,
                                    "type": "shortcut",
                                }
                            )

        return apps

    def discover_from_program_files(self):
        """🔍 Discover apps from Program Files directories"""
        apps = []
        program_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"D:\Program Files",
        ]

        for program_path in program_paths:
            if os.path.exists(program_path):
                for item in os.listdir(program_path):
                    item_path = os.path.join(program_path, item)

                    if os.path.isdir(item_path):
                        # Look for executables
                        exes = self.find_exes_in_directory(item_path)
                        if exes:
                            apps.append(
                                {
                                    "name": item,
                                    "path": item_path,
                                    "executables": exes,
                                    "type": "program_files",
                                }
                            )

        return apps

    def discover_from_appdata(self):
        """🔍 Discover apps from AppData directories"""
        apps = []
        appdata_paths = [
            os.path.join(os.environ["LOCALAPPDATA"]),
            os.path.join(os.environ["APPDATA"]),
        ]

        for appdata_path in appdata_paths:
            if os.path.exists(appdata_path):
                for item in os.listdir(appdata_path):
                    item_path = os.path.join(appdata_path, item)

                    if os.path.isdir(item_path):
                        # Look for executables
                        exes = self.find_exes_in_directory(item_path)
                        if exes:
                            apps.append(
                                {
                                    "name": item,
                                    "path": item_path,
                                    "executables": exes,
                                    "type": "appdata",
                                }
                            )

        return apps

    @staticmethod
    def find_exes_in_directory(directory):
        """🔍 Find executable files in directory"""
        exes = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".exe"):
                    # Skip common system executables
                    if not any(
                        sys_exe in file.lower()
                        for sys_exe in ["uninstall", "setup", "install"]
                    ):
                        exe_path = os.path.join(root, file)
                        exes.append({"name": file, "path": exe_path})

        return exes

    def search_app(self, query):
        """🔍 Search for app by name"""
        query_lower = query.lower()
        results = []

        # Check cache first
        if query_lower in self.app_cache:
            return [self.app_cache[query_lower]]

        # Search in installed apps
        for app in self.installed_apps:
            app_name = app.get("name", "").lower()

            # Exact match
            if query_lower == app_name:
                results.append(app)

            # Partial match
            elif query_lower in app_name:
                results.append(app)

            # Check in path
            elif "path" in app and query_lower in app["path"].lower():
                results.append(app)

        # Sort by relevance
        results.sort(key=lambda x: self.calculate_relevance(x, query))

        return results[:10]  # Return top 10 results

    @staticmethod
    def calculate_relevance(app, query):
        """🔍 Calculate relevance score for search"""
        score = 0
        query_lower = query.lower()
        app_name = app.get("name", "").lower()

        # Exact name match
        if query_lower == app_name:
            score += 100

        # Name contains query
        elif query_lower in app_name:
            score += 50

        # Query in path
        if "path" in app and query_lower in app["path"].lower():
            score += 30

        # Common app bonus
        common_apps = ["chrome", "firefox", "vscode", "whatsapp", "spotify", "discord"]
        if any(common_app in app_name for common_app in common_apps):
            score += 20

        return -score  # Negative for descending sort

    def get_app_info(self, app_name):
        """🔍 Get detailed information about app"""
        results = self.search_app(app_name)

        if results:
            app = results[0]

            # Add additional info
            if "path" in app:
                # Check if app is running
                app["is_running"] = self.is_app_running(app["name"])

                # Get file size
                try:
                    if os.path.exists(app["path"]):
                        if os.path.isfile(app["path"]):
                            size = os.path.getsize(app["path"])
                            app["size"] = self.format_size(size)
                        elif os.path.isdir(app["path"]):
                            total_size = 0
                            for dirpath, dirnames, filenames in os.walk(app["path"]):
                                for f in filenames:
                                    fp = os.path.join(dirpath, f)
                                    if os.path.exists(fp):
                                        total_size += os.path.getsize(fp)
                            app["size"] = self.format_size(total_size)
                except:
                    pass

            return app

        return None

    @staticmethod
    def is_app_running(app_name):
        """🔍 Check if app is currently running"""
        import psutil

        app_name_lower = app_name.lower()

        for proc in psutil.process_iter(["name"]):
            try:
                if app_name_lower in proc.info["name"].lower():
                    return True
            except:
                continue

        return False

    @staticmethod
    def format_size(size_bytes):
        """🔍 Format size in human readable format"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def get_app_count(self):
        """🔍 Get count of discovered apps"""
        return len(self.installed_apps)

    def get_apps_by_category(self):
        """🔍 Get apps grouped by category"""
        categories = {
            "browsers": [],
            "development": [],
            "media": [],
            "communication": [],
            "productivity": [],
            "system": [],
            "other": [],
        }

        browser_keywords = ["chrome", "firefox", "edge", "opera", "browser"]
        dev_keywords = [
            "visual studio",
            "vscode",
            "pycharm",
            "intellij",
            "eclipse",
            "android studio",
            "code",
            "editor",
        ]
        media_keywords = [
            "spotify",
            "vlc",
            "media player",
            "music",
            "video",
            "photoshop",
            "premiere",
        ]
        comm_keywords = [
            "whatsapp",
            "discord",
            "telegram",
            "skype",
            "zoom",
            "teams",
            "slack",
        ]
        productivity_keywords = [
            "office",
            "word",
            "excel",
            "powerpoint",
            "outlook",
            "notepad",
            "calculator",
        ]
        system_keywords = [
            "control panel",
            "task manager",
            "cmd",
            "powershell",
            "regedit",
            "device manager",
        ]

        for app in self.installed_apps:
            app_name = app.get("name", "").lower()
            categorized = False

            # Check categories
            if any(keyword in app_name for keyword in browser_keywords):
                categories["browsers"].append(app)
                categorized = True

            if any(keyword in app_name for keyword in dev_keywords):
                categories["development"].append(app)
                categorized = True

            if any(keyword in app_name for keyword in media_keywords):
                categories["media"].append(app)
                categorized = True

            if any(keyword in app_name for keyword in comm_keywords):
                categories["communication"].append(app)
                categorized = True

            if any(keyword in app_name for keyword in productivity_keywords):
                categories["productivity"].append(app)
                categorized = True

            if any(keyword in app_name for keyword in system_keywords):
                categories["system"].append(app)
                categorized = True

            if not categorized:
                categories["other"].append(app)

        return categories

    def refresh_cache(self):
        """🔍 Refresh app discovery cache"""
        print(Fore.YELLOW + "🔄 Refreshing app cache..." + Style.RESET_ALL)
        self.discover_apps()
        print(Fore.GREEN + "✅ App cache refreshed" + Style.RESET_ALL)

    def export_app_list(self, filename="installed_apps.json"):
        """🔍 Export app list to file"""
        import json

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.installed_apps, f, indent=2, ensure_ascii=False)

            print(Fore.GREEN + f"✅ App list exported: {filename}" + Style.RESET_ALL)
            return True

        except Exception as e:
            print(Fore.RED + f"❌ App export failed: {str(e)}" + Style.RESET_ALL)
            return False
