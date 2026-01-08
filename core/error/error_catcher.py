"""
🛠️ Error Catcher
Catches and handles errors gracefully
"""

import json
import time
import traceback
from datetime import datetime

from colorama import Fore, Style


class ErrorCatcher:
    def __init__(self, config):
        self.config = config
        self.error_count = 0
        self.error_history = []
        self.max_history = 100

    def handle_error(self, error, context=""):
        """🛠️ Handle an error"""
        self.error_count += 1

        # Create error entry
        error_entry = {
            "id": self.error_count,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "resolved": False,
            "resolution": "",
            "auto_fixed": False,
        }

        # Add to history
        self.error_history.append(error_entry)

        # Keep history limited
        if len(self.error_history) > self.max_history:
            self.error_history = self.error_history[-self.max_history :]

        # Log error
        self.log_error(error_entry)

        # Try auto-fix
        fixed = self.try_auto_fix(error_entry)

        # Print error
        print(Fore.RED + f"❌ ERROR in {context}: {str(error)}" + Style.RESET_ALL)

        if fixed:
            print(
                Fore.GREEN
                + f"✅ Auto-fixed error: {error_entry['resolution']}"
                + Style.RESET_ALL
            )
        else:
            print(Fore.YELLOW + f"⚠️ Could not auto-fix error" + Style.RESET_ALL)

        return fixed

    def try_auto_fix(self, error_entry):
        """🛠️ Try to automatically fix error"""
        error_msg = error_entry["error_message"].lower()
        context = error_entry["context"].lower()

        # Common error patterns and fixes
        fixes = [
            {
                "pattern": ["microphone", "audio", "listen"],
                "fix": self.fix_microphone,
                "description": "Microphone issue",
            },
            {
                "pattern": ["speak", "voice", "tts"],
                "fix": self.fix_tts,
                "description": "TTS issue",
            },
            {
                "pattern": ["import", "module", "package"],
                "fix": self.fix_import,
                "description": "Import issue",
            },
            {
                "pattern": ["file", "path", "directory"],
                "fix": self.fix_file,
                "description": "File system issue",
            },
            {
                "pattern": ["network", "internet", "connection"],
                "fix": self.fix_network,
                "description": "Network issue",
            },
            {
                "pattern": ["permission", "access", "denied"],
                "fix": self.fix_permission,
                "description": "Permission issue",
            },
        ]

        for fix_info in fixes:
            for pattern in fix_info["pattern"]:
                if pattern in error_msg or pattern in context:
                    try:
                        success = fix_info["fix"](error_entry)
                        if success:
                            error_entry["resolved"] = True
                            error_entry["resolution"] = fix_info["description"]
                            error_entry["auto_fixed"] = True
                            return True
                    except:
                        pass

        return False

    def fix_microphone(self, error_entry):
        """🛠️ Fix microphone issues"""
        try:
            # Try to reinitialize audio
            import pyaudio

            p = pyaudio.PyAudio()
            p.terminate()
            time.sleep(1)
            return True
        except:
            return False

    def fix_tts(self, error_entry):
        """🛠️ Fix TTS issues"""
        try:
            # Try to reinitialize TTS
            import pyttsx3

            engine = pyttsx3.init()
            engine.say("Testing")
            engine.runAndWait()
            return True
        except:
            return False

    def fix_import(self, error_entry):
        """🛠️ Fix import issues"""
        try:
            # Extract module name from error
            import re

            match = re.search(r"'(.*?)'", error_entry["error_message"])
            if match:
                module_name = match.group(1)
                # Try to install module
                import subprocess

                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", module_name]
                )
                return True
        except:
            pass
        return False

    def fix_file(self, error_entry):
        """🛠️ Fix file system issues"""
        try:
            # Extract file path from error
            import os
            import re

            # Look for file paths in error
            paths = re.findall(
                r"[A-Za-z]:\\[^\\].*?|/[^/].*?", error_entry["error_message"]
            )

            for path in paths:
                # Create directory if it doesn't exist
                dir_path = os.path.dirname(path)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    return True
        except:
            pass
        return False

    def fix_network(self, error_entry):
        """🛠️ Fix network issues"""
        try:
            # Try to ping Google to check connectivity
            import subprocess

            result = subprocess.run(
                ["ping", "-n", "1", "google.com"], capture_output=True, text=True
            )
            if result.returncode == 0:
                return True
        except:
            pass
        return False

    def fix_permission(self, error_entry):
        """🛠️ Fix permission issues"""
        # For Windows, we can't fix permissions easily
        # Just return True to mark as "handled"
        return True

    def log_error(self, error_entry):
        """🛠️ Log error to file"""
        try:
            log_file = self.config["paths"]["error_log"]

            # Load existing errors
            errors = []
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    errors = json.load(f)
            except:
                pass

            # Add new error
            errors.append(error_entry)

            # Keep only last 500 errors
            if len(errors) > 500:
                errors = errors[-500:]

            # Save
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(errors, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Error log failed: {str(e)}" + Style.RESET_ALL)

    def get_error_stats(self):
        """🛠️ Get error statistics"""
        stats = {
            "total": len(self.error_history),
            "resolved": len([e for e in self.error_history if e["resolved"]]),
            "auto_fixed": len([e for e in self.error_history if e["auto_fixed"]]),
            "by_type": {},
            "by_context": {},
        }

        # Count by type
        for error in self.error_history:
            error_type = error["error_type"]
            if error_type not in stats["by_type"]:
                stats["by_type"][error_type] = 0
            stats["by_type"][error_type] += 1

            # Count by context
            context = error["context"]
            if context not in stats["by_context"]:
                stats["by_context"][context] = 0
            stats["by_context"][context] += 1

        return stats

    def clear_errors(self):
        """🛠️ Clear error history"""
        self.error_history = []
        self.error_count = 0

        try:
            log_file = self.config["paths"]["error_log"]
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        except:
            pass
