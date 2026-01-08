"""
🎯 System Bootstrap & Self-Check
Checks all dependencies and system requirements
"""

import os
import sys
import subprocess
import platform
import psutil
from colorama import Fore, Style

class SystemBootstrap:
    def __init__(self):
        self.system_info = {}
        self.issues = []
        self.warnings = []
        
    def run_checks(self):
        """🎯 Run all system checks"""
        print(Fore.CYAN + "\n🔍 Running System Checks..." + Style.RESET_ALL)
        
        self.check_python_version()
        self.check_dependencies()
        self.check_microphone()
        self.check_speakers()
        self.check_internet()
        self.check_system_resources()
        self.check_permissions()
        
        self.print_summary()
        
    def check_python_version(self):
        """🎯 Check Python version"""
        version = platform.python_version()
        required = (3, 8)
        current = tuple(map(int, version.split('.')[:2]))
        
        if current >= required:
            print(Fore.GREEN + f"✅ Python {version} - OK" + Style.RESET_ALL)
        else:
            self.issues.append(f"Python {version} is too old. Need 3.8+")
            print(Fore.RED + f"❌ Python {version} - Too old" + Style.RESET_ALL)
    
    def check_dependencies(self):
        """🎯 Check required packages"""
        required = [
            'pyttsx3', 'SpeechRecognition', 'psutil',
            'pyautogui', 'requests', 'pyyaml'
        ]
        
        for package in required:
            try:
                __import__(package.replace('-', '_'))
                print(Fore.GREEN + f"✅ {package} - OK" + Style.RESET_ALL)
            except ImportError:
                self.issues.append(f"Missing package: {package}")
                print(Fore.RED + f"❌ {package} - Missing" + Style.RESET_ALL)
    
    def check_microphone(self):
        """🎯 Check microphone availability"""
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            if p.get_device_count() > 0:
                print(Fore.GREEN + "✅ Microphone - Available" + Style.RESET_ALL)
            else:
                self.warnings.append("No microphone found")
                print(Fore.YELLOW + "⚠️ Microphone - Not found" + Style.RESET_ALL)
            p.terminate()
        except:
            self.warnings.append("Microphone check failed")
            print(Fore.YELLOW + "⚠️ Microphone - Check failed" + Style.RESET_ALL)
    
    def check_speakers(self):
        """🎯 Check speaker availability"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if voices:
                print(Fore.GREEN + "✅ Speakers - Available" + Style.RESET_ALL)
            else:
                self.warnings.append("No speakers/voices found")
                print(Fore.YELLOW + "⚠️ Speakers - No voices" + Style.RESET_ALL)
        except:
            self.warnings.append("Speaker check failed")
            print(Fore.YELLOW + "⚠️ Speakers - Check failed" + Style.RESET_ALL)
    
    def check_internet(self):
        """🎯 Check internet connectivity"""
        try:
            import requests
            response = requests.get("https://google.com", timeout=5)
            if response.status_code == 200:
                print(Fore.GREEN + "✅ Internet - Connected" + Style.RESET_ALL)
            else:
                self.warnings.append("Internet connection unstable")
                print(Fore.YELLOW + "⚠️ Internet - Unstable" + Style.RESET_ALL)
        except:
            self.warnings.append("No internet connection")
            print(Fore.YELLOW + "⚠️ Internet - Disconnected" + Style.RESET_ALL)
    
    def check_system_resources(self):
        """🎯 Check system resources"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 80:
                print(Fore.GREEN + f"✅ CPU Usage: {cpu_percent}% - OK" + Style.RESET_ALL)
            else:
                self.warnings.append(f"High CPU usage: {cpu_percent}%")
                print(Fore.YELLOW + f"⚠️ CPU Usage: {cpu_percent}% - High" + Style.RESET_ALL)
            
            # RAM
            ram = psutil.virtual_memory()
            if ram.percent < 85:
                print(Fore.GREEN + f"✅ RAM Usage: {ram.percent}% - OK" + Style.RESET_ALL)
            else:
                self.warnings.append(f"High RAM usage: {ram.percent}%")
                print(Fore.YELLOW + f"⚠️ RAM Usage: {ram.percent}% - High" + Style.RESET_ALL)
            
            # Disk
            disk = psutil.disk_usage('/')
            if disk.percent < 90:
                print(Fore.GREEN + f"✅ Disk Space: {disk.percent}% used - OK" + Style.RESET_ALL)
            else:
                self.warnings.append(f"Low disk space: {disk.percent}% used")
                print(Fore.YELLOW + f"⚠️ Disk Space: {disk.percent}% used - Low" + Style.RESET_ALL)
                
        except Exception as e:
            self.warnings.append(f"Resource check failed: {str(e)}")
            print(Fore.YELLOW + f"⚠️ Resource Check - Failed" + Style.RESET_ALL)
    
    def check_permissions(self):
        """🎯 Check system permissions"""
        try:
            # Check if we can write to current directory
            test_file = "permission_test.txt"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print(Fore.GREEN + "✅ File Permissions - OK" + Style.RESET_ALL)
        except:
            self.issues.append("Cannot write to current directory")
            print(Fore.RED + "❌ File Permissions - Denied" + Style.RESET_ALL)
    
    def print_summary(self):
        """🎯 Print check summary"""
        print(Fore.CYAN + "\n" + "="*50 + Style.RESET_ALL)
        print(Fore.CYAN + "🔍 SYSTEM CHECK SUMMARY" + Style.RESET_ALL)
        print(Fore.CYAN + "="*50 + Style.RESET_ALL)
        
        if not self.issues and not self.warnings:
            print(Fore.GREEN + "✅ All checks passed! System is ready." + Style.RESET_ALL)
        else:
            if self.issues:
                print(Fore.RED + "\n❌ ISSUES (Need fixing):" + Style.RESET_ALL)
                for issue in self.issues:
                    print(Fore.RED + f"  • {issue}" + Style.RESET_ALL)
            
            if self.warnings:
                print(Fore.YELLOW + "\n⚠️ WARNINGS (Can proceed):" + Style.RESET_ALL)
                for warning in self.warnings:
                    print(Fore.YELLOW + f"  • {warning}" + Style.RESET_ALL)
        
        print(Fore.CYAN + "\n" + "="*50 + Style.RESET_ALL)