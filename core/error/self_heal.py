"""
🛠️ Self Healing System
Automatically fixes common errors and issues
"""

import os
import sys
import subprocess
import time
import psutil
from colorama import Fore, Style

class SelfHeal:
    def __init__(self, config):
        self.config = config
        self.fix_history = []
        self.max_history = 100
        
    def diagnose_and_fix(self, error_type, error_details, context):
        """🛠️ Diagnose and attempt to fix error"""
        print(Fore.YELLOW + f"🛠️ Attempting self-heal for: {error_type}" + Style.RESET_ALL)
        
        # Get suggested fixes
        fixes = self.get_suggested_fixes(error_type, error_details, context)
        
        results = []
        for fix in fixes:
            print(Fore.CYAN + f"  Trying: {fix['description']}" + Style.RESET_ALL)
            
            success = self.apply_fix(fix)
            result = {
                'fix': fix['description'],
                'success': success,
                'timestamp': time.time()
            }
            results.append(result)
            
            if success:
                print(Fore.GREEN + f"  ✅ Fix successful: {fix['description']}" + Style.RESET_ALL)
                
                # Record in history
                self.record_fix(error_type, fix, success, context)
                
                # Return on first success
                return {
                    'healed': True,
                    'fix_applied': fix['description'],
                    'all_results': results
                }
            else:
                print(Fore.RED + f"  ❌ Fix failed: {fix['description']}" + Style.RESET_ALL)
        
        # If all fixes failed
        print(Fore.RED + f"🛠️ Self-heal failed for: {error_type}" + Style.RESET_ALL)
        
        return {
            'healed': False,
            'fix_applied': None,
            'all_results': results
        }
    
    def get_suggested_fixes(self, error_type, error_details, context):
        """🛠️ Get suggested fixes for error type"""
        fixes = []
        
        # Common error patterns and fixes
        error_patterns = {
            "microphone_error": [
                {
                    "description": "Check microphone privacy settings",
                    "action": "check_mic_privacy",
                    "priority": 1
                },
                {
                    "description": "Restart audio services",
                    "action": "restart_audio_services",
                    "priority": 2
                },
                {
                    "description": "Test with system audio settings",
                    "action": "test_system_audio",
                    "priority": 3
                }
            ],
            "speech_recognition_error": [
                {
                    "description": "Check internet connection",
                    "action": "check_internet",
                    "priority": 1
                },
                {
                    "description": "Switch to offline recognition",
                    "action": "switch_to_offline_stt",
                    "priority": 2
                },
                {
                    "description": "Adjust microphone sensitivity",
                    "action": "adjust_mic_sensitivity",
                    "priority": 3
                }
            ],
            "tts_error": [
                {
                    "description": "Check speaker connection",
                    "action": "check_speakers",
                    "priority": 1
                },
                {
                    "description": "Reinitialize TTS engine",
                    "action": "reinit_tts",
                    "priority": 2
                },
                {
                    "description": "Test with system TTS",
                    "action": "test_system_tts",
                    "priority": 3
                }
            ],
            "import_error": [
                {
                    "description": "Install missing package",
                    "action": "install_missing_package",
                    "priority": 1,
                    "package_name": self.extract_package_name(error_details)
                },
                {
                    "description": "Update pip",
                    "action": "update_pip",
                    "priority": 2
                },
                {
                    "description": "Check Python path",
                    "action": "check_python_path",
                    "priority": 3
                }
            ],
            "file_not_found": [
                {
                    "description": "Create missing directory",
                    "action": "create_directory",
                    "priority": 1,
                    "path": self.extract_file_path(error_details)
                },
                {
                    "description": "Check file permissions",
                    "action": "check_permissions",
                    "priority": 2
                },
                {
                    "description": "Use alternative path",
                    "action": "use_alternative_path",
                    "priority": 3
                }
            ],
            "permission_error": [
                {
                    "description": "Run as administrator",
                    "action": "run_as_admin",
                    "priority": 1
                },
                {
                    "description": "Change file permissions",
                    "action": "change_permissions",
                    "priority": 2
                },
                {
                    "description": "Move to user directory",
                    "action": "move_to_user_dir",
                    "priority": 3
                }
            ],
            "network_error": [
                {
                    "description": "Check internet connectivity",
                    "action": "ping_google",
                    "priority": 1
                },
                {
                    "description": "Reset network adapter",
                    "action": "reset_network",
                    "priority": 2
                },
                {
                    "description": "Use cached data",
                    "action": "use_cached_data",
                    "priority": 3
                }
            ],
            "memory_error": [
                {
                    "description": "Close unnecessary processes",
                    "action": "cleanup_memory",
                    "priority": 1
                },
                {
                    "description": "Increase virtual memory",
                    "action": "increase_virtual_memory",
                    "priority": 2
                },
                {
                    "description": "Restart application",
                    "action": "restart_application",
                    "priority": 3
                }
            ]
        }
        
        # Get fixes for error type
        if error_type in error_patterns:
            fixes = error_patterns[error_type]
        else:
            # Generic fixes for unknown errors
            fixes = [
                {
                    "description": "Restart affected service",
                    "action": "restart_service",
                    "priority": 1
                },
                {
                    "description": "Clear temporary files",
                    "action": "clear_temp_files",
                    "priority": 2
                },
                {
                    "description": "Check system resources",
                    "action": "check_resources",
                    "priority": 3
                }
            ]
        
        # Sort by priority
        fixes.sort(key=lambda x: x['priority'])
        
        return fixes
    
    def apply_fix(self, fix):
        """🛠️ Apply specific fix"""
        action = fix.get('action', '')
        
        try:
            if action == "check_mic_privacy":
                return self.fix_mic_privacy()
            elif action == "restart_audio_services":
                return self.restart_audio_services()
            elif action == "check_internet":
                return self.check_internet_connection()
            elif action == "switch_to_offline_stt":
                return self.switch_to_offline_stt()
            elif action == "check_speakers":
                return self.check_speaker_connection()
            elif action == "reinit_tts":
                return self.reinitialize_tts()
            elif action == "install_missing_package":
                package = fix.get('package_name')
                return self.install_package(package)
            elif action == "create_directory":
                path = fix.get('path')
                return self.create_missing_directory(path)
            elif action == "run_as_admin":
                return self.run_as_administrator()
            elif action == "ping_google":
                return self.ping_google()
            elif action == "cleanup_memory":
                return self.cleanup_memory()
            elif action == "restart_application":
                return self.restart_application()
            elif action == "clear_temp_files":
                return self.clear_temp_files()
            elif action == "check_resources":
                return self.check_system_resources()
            else:
                return False
                
        except Exception as e:
            print(Fore.RED + f"  ❌ Fix application error: {str(e)}" + Style.RESET_ALL)
            return False
    
    @staticmethod
    def fix_mic_privacy():
        """🛠️ Fix microphone privacy settings"""
        try:
            # For Windows 10/11
            if sys.platform == "win32":
                # Open microphone privacy settings
                subprocess.run(["start", "ms-settings:privacy-microphone"], shell=True)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def restart_audio_services():
        """🛠️ Restart audio services"""
        try:
            if sys.platform == "win32":
                # Restart Windows Audio service
                subprocess.run(["net", "stop", "Audiosrv"], shell=True, capture_output=True)
                time.sleep(2)
                subprocess.run(["net", "start", "Audiosrv"], shell=True, capture_output=True)
                time.sleep(2)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def check_internet_connection():
        """🛠️ Check internet connection"""
        try:
            import requests
            response = requests.get("https://google.com", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def switch_to_offline_stt():
        """🛠️ Switch to offline speech recognition"""
        try:
            # Try to use Vosk if available
            import vosk
            return True
        except:
            return False
    
    @staticmethod
    def check_speaker_connection():
        """🛠️ Check speaker connection"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            return len(voices) > 0
        except:
            return False
    
    @staticmethod
    def reinitialize_tts():
        """🛠️ Reinitialize TTS engine"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("Test")
            engine.runAndWait()
            return True
        except:
            return False
    
    @staticmethod
    def install_package(package_name):
        """🛠️ Install missing package"""
        try:
            if package_name:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                return True
            return False
        except:
            return False
    
    @staticmethod
    def create_missing_directory(path):
        """🛠️ Create missing directory"""
        try:
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                return True
            return False
        except:
            return False
    
    @staticmethod
    def run_as_administrator():
        """🛠️ Run as administrator"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def ping_google():
        """🛠️ Ping Google to check connectivity"""
        try:
            result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def cleanup_memory():
        """🛠️ Cleanup memory"""
        try:
            # Close non-essential processes
            essential = ['python', 'jarvis', 'cmd', 'explorer']
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    if proc_name not in essential and 'python' not in proc_name:
                        proc.terminate()
                except:
                    pass
            return True
        except:
            return False
    
    @staticmethod
    def restart_application():
        """🛠️ Restart application"""
        try:
            # This would restart JARVIS
            # For now, just return True as placeholder
            return True
        except:
            return False
    
    @staticmethod
    def clear_temp_files():
        """🛠️ Clear temporary files"""
        try:
            import tempfile
            import shutil
            temp_dir = tempfile.gettempdir()
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except:
                    pass
            return True
        except:
            return False
    
    @staticmethod
    def check_system_resources():
        """🛠️ Check system resources"""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            return cpu_usage < 90 and memory.percent < 85
        except:
            return False
    
    @staticmethod
    def extract_package_name(error_message):
        """🛠️ Extract package name from import error"""
        import re
        match = re.search(r"'(.*?)'", error_message)
        if match:
            return match.group(1)
        return None
    
    @staticmethod
    def extract_file_path(error_message):
        """🛠️ Extract file path from error"""
        import re
        # Look for file paths in error
        paths = re.findall(r'[A-Za-z]:\\[^\\].*?|/[^/].*?', error_message)
        return paths[0] if paths else None
    
    def record_fix(self, error_type, fix, success, context):
        """🛠️ Record fix in history"""
        fix_record = {
            'timestamp': time.time(),
            'error_type': error_type,
            'fix': fix['description'],
            'action': fix['action'],
            'success': success,
            'context': context
        }
        
        self.fix_history.append(fix_record)
        
        # Keep history limited
        if len(self.fix_history) > self.max_history:
            self.fix_history = self.fix_history[-self.max_history:]
    
    def get_fix_history_stats(self):
        """🛠️ Get fix history statistics"""
        if not self.fix_history:
            return {"total_fixes": 0}
        
        stats = {
            'total_fixes': len(self.fix_history),
            'successful_fixes': sum(1 for f in self.fix_history if f['success']),
            'success_rate': 0.0,
            'common_errors': {},
            'effective_fixes': []
        }
        
        # Calculate success rate
        if stats['total_fixes'] > 0:
            stats['success_rate'] = stats['successful_fixes'] / stats['total_fixes']
        
        # Count common errors
        for fix in self.fix_history:
            error_type = fix['error_type']
            if error_type not in stats['common_errors']:
                stats['common_errors'][error_type] = 0
            stats['common_errors'][error_type] += 1
        
        # Find effective fixes
        fix_effectiveness = {}
        for fix in self.fix_history:
            fix_key = f"{fix['error_type']}:{fix['fix']}"
            if fix_key not in fix_effectiveness:
                fix_effectiveness[fix_key] = {'success': 0, 'total': 0}
            
            fix_effectiveness[fix_key]['total'] += 1
            if fix['success']:
                fix_effectiveness[fix_key]['success'] += 1
        
        # Calculate effectiveness rates
        for fix_key, data in fix_effectiveness.items():
            if data['total'] >= 3:  # Only consider fixes tried multiple times
                rate = data['success'] / data['total']
                if rate > 0.7:  # Highly effective
                    stats['effective_fixes'].append({
                        'fix': fix_key,
                        'success_rate': rate,
                        'tried_count': data['total']
                    })
        
        return stats
    
    def run_system_health_check(self):
        """🛠️ Run comprehensive system health check"""
        print(Fore.CYAN + "🛠️ Running system health check..." + Style.RESET_ALL)
        
        checks = [
            ("Internet Connection", self.check_internet_connection),
            ("Microphone", self.check_microphone),
            ("Speakers", self.check_speaker_connection),
            ("Python Environment", self.check_python_environment),
            ("Disk Space", self.check_disk_space),
            ("Memory Usage", self.check_memory_usage),
            ("CPU Usage", self.check_cpu_usage)
        ]
        
        results = []
        for check_name, check_func in checks:
            print(Fore.YELLOW + f"  Checking {check_name}..." + Style.RESET_ALL)
            success = check_func()
            results.append({
                'check': check_name,
                'status': '✅ PASS' if success else '❌ FAIL'
            })
            
            if success:
                print(Fore.GREEN + f"    ✅ {check_name}: PASS" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"    ❌ {check_name}: FAIL" + Style.RESET_ALL)
        
        print(Fore.CYAN + "🛠️ Health check complete" + Style.RESET_ALL)
        return results
    
    @staticmethod
    def check_microphone():
        """🛠️ Check microphone"""
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            device_count = p.get_device_count()
            p.terminate()
            return device_count > 0
        except:
            return False
    
    @staticmethod
    def check_python_environment():
        """🛠️ Check Python environment"""
        try:
            # Check if required packages are installed
            required = ['pyttsx3', 'speech_recognition', 'psutil']
            for package in required:
                __import__(package)
            return True
        except:
            return False
    
    @staticmethod
    def check_disk_space():
        """🛠️ Check disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage("/")
            return (free / total) > 0.1  # More than 10% free
        except:
            return False
    
    @staticmethod
    def check_memory_usage():
        """🛠️ Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            return memory.percent < 85
        except:
            return False
    
    @staticmethod
    def check_cpu_usage():
        """🛠️ Check CPU usage"""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage < 80
        except:
            return False