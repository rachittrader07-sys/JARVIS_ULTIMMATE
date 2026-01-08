"""
❌ Close Application Skill
Closes running applications
"""

import os
import subprocess

import psutil
from colorama import Fore, Style


class CloseApp:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts

    def execute(self, params):
        """❌ Execute app closing"""
        app_name = params.get("app_name", "").lower()
        force = params.get("force", False)

        if not app_name:
            self.tts.speak("Sir, kaunsi app close karni hai?")
            return {"success": False, "error": "No app name"}

        print(Fore.YELLOW + f"❌ Closing app: {app_name}" + Style.RESET_ALL)

        # Try multiple methods to close app
        result = self.close_app_multi_method(app_name, force)

        if result["success"]:
            self.tts.speak(f"Sir, maine {app_name} close kar di")
            return {"success": True, "speak": f"{app_name} closed"}
        else:
            self.tts.speak(f"Sir, {app_name} close nahi kar paya")
            return result

    def close_app_multi_method(self, app_name, force=False):
        """❌ Try multiple methods to close app"""
        methods = [
            self.close_via_taskkill,
            self.close_via_process_termination,
            self.close_via_window_close,
        ]

        for method in methods:
            try:
                result = method(app_name, force)
                if result["success"]:
                    return result
            except:
                continue

        return {"success": False, "error": "All methods failed"}

    def close_via_taskkill(self, app_name, force=False):
        """❌ Close app using taskkill command"""
        try:
            # Build taskkill command
            cmd = (
                ["taskkill", "/IM", f"*{app_name}*", "/F"]
                if force
                else ["taskkill", "/IM", f"*{app_name}*"]
            )

            # Execute
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if result.returncode == 0 or "terminated" in result.stdout.lower():
                print(
                    Fore.GREEN + f"✅ Closed via taskkill: {app_name}" + Style.RESET_ALL
                )
                return {"success": True, "method": "taskkill"}
            else:
                return {"success": False}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_via_process_termination(self, app_name, force=False):
        """❌ Close app by terminating process"""
        try:
            processes_closed = 0

            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    proc_name = proc.info["name"].lower()

                    # Check if process matches app name
                    if app_name in proc_name:
                        if force:
                            proc.kill()
                        else:
                            proc.terminate()

                        processes_closed += 1
                        print(
                            Fore.GREEN
                            + f"✅ Terminated process: {proc_name}"
                            + Style.RESET_ALL
                        )

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    continue

            if processes_closed > 0:
                return {
                    "success": True,
                    "method": "process_termination",
                    "count": processes_closed,
                }
            else:
                return {"success": False}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_via_window_close(self, app_name, force=False):
        """❌ Close app by closing its window"""
        try:
            import pygetwindow as gw

            # Find windows containing app name
            windows = gw.getWindowsWithTitle(app_name)

            if not windows:
                # Try all windows
                all_windows = gw.getAllWindows()
                matching_windows = []

                for window in all_windows:
                    if app_name in window.title.lower():
                        matching_windows.append(window)

                windows = matching_windows

            windows_closed = 0

            for window in windows:
                try:
                    window.close()
                    windows_closed += 1
                    print(
                        Fore.GREEN
                        + f"✅ Closed window: {window.title}"
                        + Style.RESET_ALL
                    )
                except:
                    continue

            if windows_closed > 0:
                return {
                    "success": True,
                    "method": "window_close",
                    "count": windows_closed,
                }
            else:
                return {"success": False}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_current_app(self):
        """❌ Close current active application"""
        try:
            import pygetwindow as gw

            # Get active window
            active_window = gw.getActiveWindow()

            if active_window:
                app_name = active_window.title
                active_window.close()

                print(
                    Fore.GREEN + f"✅ Closed current app: {app_name}" + Style.RESET_ALL
                )
                return {"success": True, "app": app_name}
            else:
                return {"success": False, "error": "No active window"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def close_all_except(self, exceptions=[]):
        """❌ Close all apps except specified ones"""
        try:
            import pygetwindow as gw

            all_windows = gw.getAllWindows()
            closed_count = 0

            for window in all_windows:
                window_title = window.title.lower()

                # Check if window should be kept open
                keep_open = False
                for exception in exceptions:
                    if exception.lower() in window_title:
                        keep_open = True
                        break

                if not keep_open and window_title.strip():
                    try:
                        window.close()
                        closed_count += 1
                    except:
                        continue

            print(Fore.GREEN + f"✅ Closed {closed_count} apps" + Style.RESET_ALL)
            return {"success": True, "closed_count": closed_count}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def force_close_unresponsive(self):
        """❌ Force close unresponsive applications"""
        try:
            # Use taskkill to close not responding apps
            cmd = 'taskkill /FI "STATUS eq NOT RESPONDING" /F'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if "terminated" in result.stdout.lower() or result.returncode == 0:
                print(
                    Fore.GREEN + "✅ Force closed unresponsive apps" + Style.RESET_ALL
                )
                return {"success": True, "method": "force_close"}
            else:
                return {"success": False}

        except Exception as e:
            return {"success": False, "error": str(e)}
