"""
🚀 Open Application Skill
Opens any application by name (even if not in code)
"""

import os
import sys
import subprocess
import winreg
import psutil
from colorama import Fore, Style

class OpenApp:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.installed_apps = self.get_installed_apps()
        
    def execute(self, params):
        """🚀 Execute app opening"""
        app_name = params.get('app_name', '').lower()
        
        if not app_name:
            self.tts.speak("Sir, which app should I open?")
            return {'success': False, 'error': 'No app name provided'}
        
        print(Fore.YELLOW + f"🔍 Looking for app: {app_name}" + Style.RESET_ALL)
        
        # Try multiple methods to open app
        result = self.open_app_multi_method(app_name)
        
        if result['success']:
            self.tts.speak(f"Sir, I have opened {app_name}")
            return {'success': True, 'speak': f"{app_name} opened successfully"}
        else:
            # Try appopener library
            result2 = self.try_appopener(app_name)
            if result2['success']:
                return result2
            
            # Try system search
            result3 = self.try_system_search(app_name)
            if result3['success']:
                return result3
            
            # Ask user for clarification
            self.tts.speak(f"Sir, I couldn't find {app_name}. Could you please specify the exact name?")
            return {'success': False, 'error': 'App not found'}
    
    def open_app_multi_method(self, app_name):
        """🚀 Try multiple methods to open app"""
        methods = [
            self.open_via_system_path,
            self.open_via_start_menu,
            self.open_via_registry,
            self.open_via_common_paths
        ]
        
        for method in methods:
            try:
                result = method(app_name)
                if result['success']:
                    return result
            except:
                continue
        
        return {'success': False, 'error': 'All methods failed'}
    
    @staticmethod
    def open_via_system_path(app_name):
        """🚀 Open app using system PATH"""
        common_executables = {
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'vscode': 'code.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'python': 'python.exe',
            'excel': 'excel.exe',
            'word': 'winword.exe',
            'powerpoint': 'powerpnt.exe',
            'outlook': 'outlook.exe',
            'photoshop': 'photoshop.exe',
            'premiere': 'premiere.exe',
            'spotify': 'spotify.exe',
            'whatsapp': 'whatsapp.exe',
            'discord': 'discord.exe',
            'telegram': 'telegram.exe'
        }
        
        # Check if app_name matches any common executable
        for key, exe in common_executables.items():
            if key in app_name:
                try:
                    subprocess.Popen(exe, shell=True)
                    print(Fore.GREEN + f"✅ Opened {key} via system path" + Style.RESET_ALL)
                    return {'success': True, 'method': 'system_path'}
                except:
                    continue
        
        return {'success': False}
    
    @staticmethod
    def open_via_start_menu(app_name):
        """🚀 Open app via Start Menu search"""
        try:
            # Use PowerShell to open app
            ps_command = f'''
            $app = Get-StartApps | Where-Object {{$_.Name -like "*{app_name}*"}} | Select-Object -First 1
            if ($app) {{ Start-Process $app.AppID }}
            '''
            
            subprocess.run(['powershell', '-Command', ps_command], shell=True, capture_output=True)
            print(Fore.GREEN + f"✅ Attempted to open {app_name} via Start Menu" + Style.RESET_ALL)
            return {'success': True, 'method': 'start_menu'}
        except:
            return {'success': False}
    
    @staticmethod
    def open_via_registry(app_name):
        """🚀 Open app via Windows Registry"""
        try:
            # Look in Uninstall registry keys
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for path in registry_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            
                            # Get display name
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if app_name in display_name.lower():
                                    # Get install location
                                    try:
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                        if install_location:
                                            # Look for executable
                                            for root, dirs, files in os.walk(install_location):
                                                for file in files:
                                                    if file.endswith('.exe'):
                                                        exe_path = os.path.join(root, file)
                                                        subprocess.Popen(exe_path, shell=True)
                                                        print(Fore.GREEN + f"✅ Opened via registry: {display_name}" + Style.RESET_ALL)
                                                        return {'success': True, 'method': 'registry'}
                                    except:
                                        pass
                            except:
                                pass
                                
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    
                    winreg.CloseKey(key)
                except:
                    continue
            
            return {'success': False}
        except:
            return {'success': False}
    
    @staticmethod
    def open_via_common_paths(app_name):
        """🚀 Open app via common installation paths"""
        common_paths = [
            r"C:\Program Files",
            r"C:\Program Files (x86)",
            r"D:\Program Files",
            os.path.expanduser("~\\AppData\\Local"),
            os.path.expanduser("~\\AppData\\Roaming")
        ]
        
        for base_path in common_paths:
            if os.path.exists(base_path):
                for root, dirs, files in os.walk(base_path):
                    for file in files:
                        if file.endswith('.exe') and app_name in file.lower():
                            try:
                                exe_path = os.path.join(root, file)
                                subprocess.Popen(exe_path, shell=True)
                                print(Fore.GREEN + f"✅ Opened via common path: {file}" + Style.RESET_ALL)
                                return {'success': True, 'method': 'common_path'}
                            except:
                                continue
        
        return {'success': False}
    
    @staticmethod
    def try_appopener(app_name):
        """🚀 Try using appopener library"""
        try:
            import appopener
            appopener.open(app_name, match_closest=True)
            print(Fore.GREEN + f"✅ Opened using appopener: {app_name}" + Style.RESET_ALL)
            return {'success': True, 'method': 'appopener'}
        except:
            return {'success': False}
    
    @staticmethod
    def try_system_search(app_name):
        """🚀 Try Windows search"""
        try:
            # Use Windows search via PowerShell
            ps_command = f'''
            Add-Type -AssemblyName Microsoft.VisualBasic
            [Microsoft.VisualBasic.Interaction]::Shell("explorer.exe shell:appsFolder\\{app_name}", 1)
            '''
            
            subprocess.run(['powershell', '-Command', ps_command], shell=True)
            print(Fore.GREEN + f"✅ Attempted Windows search for: {app_name}" + Style.RESET_ALL)
            return {'success': True, 'method': 'windows_search'}
        except:
            return {'success': False}
    
    @staticmethod
    def get_installed_apps():
        """🚀 Get list of installed applications"""
        apps = []
        try:
            # Get from registry
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for path in registry_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if display_name:
                                    apps.append(display_name.lower())
                            except:
                                pass
                                
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    
                    winreg.CloseKey(key)
                except:
                    continue
        except:
            pass
        
        return apps