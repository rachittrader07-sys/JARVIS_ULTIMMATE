"""
🖥️ OS Controller
Controls operating system functions
"""

import os
import platform
import subprocess
import sys
import time
from datetime import datetime

import psutil
from colorama import Fore, Style


class OSController:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts

    def execute(self, params):
        """🖥️ Execute OS control command"""
        action = params.get("action", "").lower()

        if not action:
            self.tts.speak("Sir, kya system command execute karna hai?")
            return {"success": False, "error": "No action specified"}

        print(Fore.YELLOW + f"🖥️ OS action: {action}" + Style.RESET_ALL)

        # Map actions to methods
        action_map = {
            "shutdown": self.shutdown_system,
            "restart": self.restart_system,
            "sleep": self.sleep_system,
            "lock": self.lock_system,
            "logout": self.logout_user,
            "hibernate": self.hibernate_system,
            "brightness_up": self.increase_brightness,
            "brightness_down": self.decrease_brightness,
            "volume_up": self.increase_volume,
            "volume_down": self.decrease_volume,
            "mute": self.toggle_mute,
            "screenshot": self.take_screenshot,
            "clipboard": self.manage_clipboard,
        }

        if action in action_map:
            result = action_map[action]()

            if result["success"]:
                self.tts.speak(f"Sir, system {action} ho gaya")
                return {"success": True, "speak": f"System {action} ho gaya"}
            else:
                self.tts.speak(f"Sir, system {action} nahi kar paya")
                return result
        else:
            self.tts.speak(f"Sir, ye system action main nahi kar sakta")
            return {"success": False, "error": f"Unknown action: {action}"}

    @staticmethod
    def shutdown_system(delay=0):
        """🖥️ Shutdown the system"""
        try:
            if platform.system() == "Windows":
                if delay > 0:
                    subprocess.run(["shutdown", "/s", "/t", str(delay)])
                else:
                    subprocess.run(["shutdown", "/s", "/t", "1"])
                return {"success": True, "action": "shutdown", "delay": delay}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def restart_system(delay=0):
        """🖥️ Restart the system"""
        try:
            if platform.system() == "Windows":
                if delay > 0:
                    subprocess.run(["shutdown", "/r", "/t", str(delay)])
                else:
                    subprocess.run(["shutdown", "/r", "/t", "1"])
                return {"success": True, "action": "restart", "delay": delay}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def sleep_system():
        """🖥️ Put system to sleep"""
        try:
            if platform.system() == "Windows":
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"]
                )
                return {"success": True, "action": "sleep"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def lock_system():
        """🖥️ Lock the system"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
                return {"success": True, "action": "lock"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def logout_user():
        """🖥️ Logout current user"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/l"])
                return {"success": True, "action": "logout"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def hibernate_system():
        """🖥️ Hibernate the system"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["shutdown", "/h"])
                return {"success": True, "action": "hibernate"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def increase_brightness():
        """🖥️ Increase screen brightness"""
        try:
            # This requires special permissions/libraries
            # For Windows, we can use PowerShell
            if platform.system() == "Windows":
                ps_command = """
                $brightness = (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 80)
                """
                subprocess.run(["powershell", "-Command", ps_command], shell=True)
                return {"success": True, "action": "brightness_up"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def decrease_brightness():
        """🖥️ Decrease screen brightness"""
        try:
            if platform.system() == "Windows":
                ps_command = """
                $brightness = (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 40)
                """
                subprocess.run(["powershell", "-Command", ps_command], shell=True)
                return {"success": True, "action": "brightness_down"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def increase_volume():
        """🖥️ Increase system volume"""
        try:
            import pyautogui

            pyautogui.press("volumeup")
            return {"success": True, "action": "volume_up"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def decrease_volume():
        """🖥️ Decrease system volume"""
        try:
            import pyautogui

            pyautogui.press("volumedown")
            return {"success": True, "action": "volume_down"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def toggle_mute():
        """🖥️ Toggle mute"""
        try:
            import pyautogui

            pyautogui.press("volumemute")
            return {"success": True, "action": "toggle_mute"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def take_screenshot():
        """🖥️ Take screenshot"""
        try:
            from datetime import datetime

            import pyautogui

            # Create screenshots directory if not exists
            screenshots_dir = "Screenshots"
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)

            # Take screenshot
            screenshot = pyautogui.screenshot()

            # Save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{screenshots_dir}/screenshot_{timestamp}.png"
            screenshot.save(filename)

            print(Fore.GREEN + f"✅ Screenshot saved: {filename}" + Style.RESET_ALL)
            return {"success": True, "action": "screenshot", "filename": filename}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def manage_clipboard(action="copy", text=None):
        """🖥️ Manage clipboard"""
        try:
            import pyperclip

            if action == "copy" and text:
                pyperclip.copy(text)
                return {"success": True, "action": "copy", "text": text[:50]}
            elif action == "paste":
                text = pyperclip.paste()
                return {"success": True, "action": "paste", "text": text[:100]}
            elif action == "clear":
                pyperclip.copy("")
                return {"success": True, "action": "clear"}
            else:
                return {"success": False, "error": "Unknown clipboard action"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_system_info():
        """🖥️ Get detailed system information"""
        try:
            info = {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "architecture": platform.architecture()[0],
                    "processor": platform.processor(),
                },
                "python": {
                    "version": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "compiler": platform.python_compiler(),
                },
                "hardware": {
                    "cpu_count": psutil.cpu_count(logical=True),
                    "cpu_percent": psutil.cpu_percent(interval=1),
                    "memory_total": psutil.virtual_memory().total,
                    "memory_available": psutil.virtual_memory().available,
                    "memory_percent": psutil.virtual_memory().percent,
                    "disk_usage": psutil.disk_usage("/").percent,
                },
                "network": {
                    "hostname": platform.node(),
                    "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                },
                "time": {
                    "current": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "uptime": str(
                        datetime.now() - datetime.fromtimestamp(psutil.boot_time())
                    ),
                },
            }

            return {"success": True, "info": info}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_file_explorer(path=""):
        """🖥️ Open file explorer"""
        try:
            if platform.system() == "Windows":
                if path:
                    subprocess.run(["explorer", path])
                else:
                    subprocess.run(["explorer"])
                return {"success": True, "action": "open_file_explorer", "path": path}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_command_prompt():
        """🖥️ Open command prompt"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["cmd"])
                return {"success": True, "action": "open_cmd"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_powershell():
        """🖥️ Open PowerShell"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["powershell"])
                return {"success": True, "action": "open_powershell"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_task_manager():
        """🖥️ Open Task Manager"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["taskmgr"])
                return {"success": True, "action": "open_task_manager"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def open_control_panel():
        """🖥️ Open Control Panel"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["control"])
                return {"success": True, "action": "open_control_panel"}
            else:
                return {"success": False, "error": "OS not supported"}
        except Exception as e:
            return {"success": False, "error": str(e)}
