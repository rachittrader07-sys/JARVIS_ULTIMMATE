"""
🪟 Window Manager
Manages application windows (minimize, maximize, close, etc.)
"""

import time

import pyautogui
import pygetwindow as gw
from colorama import Fore, Style


class WindowManager:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts

    def execute(self, params):
        """🪟 Execute window management command"""
        action = params.get("action", "").lower()
        window_target = params.get("window", "current").lower()

        if not action:
            self.tts.speak("Sir, kya karna hai window ke saath?")
            return {"success": False, "error": "No action specified"}

        print(
            Fore.YELLOW
            + f"🪟 Window action: {action} on {window_target}"
            + Style.RESET_ALL
        )

        if window_target == "current":
            result = self.manage_current_window(action)
        elif window_target == "all":
            result = self.manage_all_windows(action)
        else:
            # Try to find window by title
            result = self.manage_specific_window(window_target, action)

        if result["success"]:
            self.tts.speak(f"Sir, window {action} ho gaya")
            return {"success": True, "speak": f"Window {action} ho gaya"}
        else:
            self.tts.speak(f"Sir, window {action} nahi kar paya")
            return result

    def manage_current_window(self, action):
        """🪟 Manage current active window"""
        try:
            # Get active window
            active_window = gw.getActiveWindow()

            if not active_window:
                return {"success": False, "error": "No active window"}

            # Perform action
            if action == "minimize":
                active_window.minimize()
            elif action == "maximize":
                active_window.maximize()
            elif action == "restore":
                active_window.restore()
            elif action == "close":
                active_window.close()
            elif action == "focus":
                active_window.activate()
            else:
                return {"success": False, "error": f"Unknown action: {action}"}

            print(
                Fore.GREEN
                + f"✅ Window {action}: {active_window.title}"
                + Style.RESET_ALL
            )
            return {"success": True, "window": active_window.title}

        except Exception as e:
            print(Fore.RED + f"❌ Window management error: {str(e)}" + Style.RESET_ALL)
            return {"success": False, "error": str(e)}

    def manage_all_windows(self, action):
        """🪟 Manage all windows"""
        try:
            windows = gw.getAllWindows()

            if not windows:
                return {"success": False, "error": "No windows found"}

            if action == "minimize":
                for window in windows:
                    if not window.isMinimized:
                        window.minimize()
            elif action == "restore":
                for window in windows:
                    if window.isMinimized:
                        window.restore()
            elif action == "close":
                # Don't close all windows by default (safety)
                return {"success": False, "error": "Safety: Cannot close all windows"}
            else:
                return {
                    "success": False,
                    "error": f"Unknown action for all windows: {action}",
                }

            print(
                Fore.GREEN
                + f"✅ All windows {action}: {len(windows)} windows"
                + Style.RESET_ALL
            )
            return {"success": True, "windows_affected": len(windows)}

        except Exception as e:
            print(Fore.RED + f"❌ All windows error: {str(e)}" + Style.RESET_ALL)
            return {"success": False, "error": str(e)}

    def manage_specific_window(self, window_title, action):
        """🪟 Manage specific window by title"""
        try:
            # Find windows containing the title
            windows = gw.getWindowsWithTitle(window_title)

            if not windows:
                # Try fuzzy matching
                all_windows = gw.getAllWindows()
                matching_windows = []

                for window in all_windows:
                    if window_title.lower() in window.title.lower():
                        matching_windows.append(window)

                windows = matching_windows

            if not windows:
                return {"success": False, "error": f"Window not found: {window_title}"}

            # Use first matching window
            window = windows[0]

            # Perform action
            if action == "minimize":
                window.minimize()
            elif action == "maximize":
                window.maximize()
            elif action == "restore":
                window.restore()
            elif action == "close":
                window.close()
            elif action == "focus":
                window.activate()
            elif action == "move":
                # Move window to specific position
                self.move_window(window, params.get("x", 0), params.get("y", 0))
            elif action == "resize":
                # Resize window
                self.resize_window(
                    window, params.get("width", 800), params.get("height", 600)
                )
            else:
                return {"success": False, "error": f"Unknown action: {action}"}

            print(Fore.GREEN + f"✅ Window {action}: {window.title}" + Style.RESET_ALL)
            return {"success": True, "window": window.title}

        except Exception as e:
            print(Fore.RED + f"❌ Specific window error: {str(e)}" + Style.RESET_ALL)
            return {"success": False, "error": str(e)}

    def move_window(self, window, x, y):
        """🪟 Move window to specific position"""
        try:
            window.moveTo(x, y)
            return True
        except:
            return False

    def resize_window(self, window, width, height):
        """🪟 Resize window"""
        try:
            window.resizeTo(width, height)
            return True
        except:
            return False

    def switch_to_window(self, window_title):
        """🪟 Switch to specific window"""
        try:
            windows = gw.getWindowsWithTitle(window_title)

            if not windows:
                # Try all windows
                all_windows = gw.getAllWindows()
                for window in all_windows:
                    if window_title.lower() in window.title.lower():
                        windows = [window]
                        break

            if windows:
                window = windows[0]
                if window.isMinimized:
                    window.restore()
                window.activate()
                return {"success": True, "window": window.title}
            else:
                return {"success": False, "error": "Window not found"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_window_list(self):
        """🪟 Get list of all open windows"""
        try:
            windows = gw.getAllWindows()
            window_list = []

            for window in windows:
                if window.title.strip():  # Skip windows with empty titles
                    window_list.append(
                        {
                            "title": window.title[:50],  # Limit length
                            "is_minimized": window.isMinimized,
                            "is_maximized": window.isMaximized,
                            "position": (window.left, window.top),
                            "size": (window.width, window.height),
                        }
                    )

            return window_list

        except Exception as e:
            print(Fore.RED + f"❌ Get window list error: {str(e)}" + Style.RESET_ALL)
            return []

    def arrange_windows(self, arrangement="cascade"):
        """🪟 Arrange windows in different patterns"""
        try:
            windows = gw.getAllWindows()

            if not windows:
                return {"success": False, "error": "No windows to arrange"}

            screen_width, screen_height = pyautogui.size()

            if arrangement == "cascade":
                # Cascade windows
                offset = 30
                for i, window in enumerate(windows):
                    if window.title.strip():
                        x = i * offset
                        y = i * offset
                        width = screen_width - (i * offset * 2)
                        height = screen_height - (i * offset * 2)

                        if window.isMinimized:
                            window.restore()

                        window.moveTo(x, y)
                        window.resizeTo(width, height)

            elif arrangement == "tile":
                # Tile windows vertically
                window_count = len([w for w in windows if w.title.strip()])
                if window_count > 0:
                    tile_width = screen_width // window_count
                    for i, window in enumerate(windows):
                        if window.title.strip():
                            if window.isMinimized:
                                window.restore()

                            x = i * tile_width
                            window.moveTo(x, 0)
                            window.resizeTo(tile_width, screen_height)

            elif arrangement == "grid":
                # Arrange in grid (2x2, 3x3, etc.)
                window_count = len([w for w in windows if w.title.strip()])
                if window_count > 0:
                    import math

                    cols = math.ceil(math.sqrt(window_count))
                    rows = math.ceil(window_count / cols)

                    cell_width = screen_width // cols
                    cell_height = screen_height // rows

                    idx = 0
                    for r in range(rows):
                        for c in range(cols):
                            if idx < len(windows):
                                window = windows[idx]
                                if window.title.strip():
                                    if window.isMinimized:
                                        window.restore()

                                    x = c * cell_width
                                    y = r * cell_height
                                    window.moveTo(x, y)
                                    window.resizeTo(cell_width, cell_height)

                                    idx += 1

            print(Fore.GREEN + f"✅ Windows arranged: {arrangement}" + Style.RESET_ALL)
            return {
                "success": True,
                "arrangement": arrangement,
                "windows": len(windows),
            }

        except Exception as e:
            print(Fore.RED + f"❌ Window arrangement error: {str(e)}" + Style.RESET_ALL)
            return {"success": False, "error": str(e)}

    def get_active_window_info(self):
        """🪟 Get information about active window"""
        try:
            window = gw.getActiveWindow()

            if not window:
                return {"success": False, "error": "No active window"}

            info = {
                "title": window.title,
                "is_minimized": window.isMinimized,
                "is_maximized": window.isMaximized,
                "position": {"x": window.left, "y": window.top},
                "size": {"width": window.width, "height": window.height},
                "process_id": getattr(window, "_hWnd", "N/A"),
            }

            return {"success": True, "info": info}

        except Exception as e:
            return {"success": False, "error": str(e)}
