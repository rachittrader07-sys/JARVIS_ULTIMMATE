"""
🔧 JARVIS Installation Script
Installs dependencies and sets up the JARVIS Assistant
"""

import os
import sys
import subprocess
import platform
import json
import shutil
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class JarvisInstaller:
    def __init__(self):
        self.system = platform.system()
        self.requirements_file = "requirements.txt"
        self.config_file = "config.default.yaml"
        self.config_target = "config.yaml"
        self.data_dir = "data"
        self.logs_dir = "logs"
        self.memory_dir = "memory"
        self.tools_dir = "tools"
        
    @staticmethod
    def print_banner():
        """🔧 Print installation banner"""
        banner = f"""
{Fore.CYAN}
    ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
    ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
    ██║███████║██████╔╝██║   ██║██║███████╗
██╗  ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
    {Fore.YELLOW}AI Assistant Installation
    {Fore.GREEN}Version 2.0.0
{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def check_python_version():
        """🔧 Check Python version"""
        print(f"{Fore.YELLOW}[1/8] Checking Python version...{Style.RESET_ALL}")
        
        if sys.version_info < (3, 7):
            print(f"{Fore.RED}❌ Python 3.7 or higher is required{Style.RESET_ALL}")
            print(f"Current version: {sys.version}")
            return False
        
        print(f"{Fore.GREEN}✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected{Style.RESET_ALL}")
        return True
    
    def create_directories(self):
        """🔧 Create necessary directories"""
        print(f"{Fore.YELLOW}[2/8] Creating directories...{Style.RESET_ALL}")
        
        directories = [
            self.data_dir,
            self.logs_dir,
            self.memory_dir,
            self.tools_dir,
            os.path.join(self.data_dir, "skills"),
            os.path.join(self.data_dir, "profiles"),
            os.path.join(self.data_dir, "cache"),
            os.path.join(self.data_dir, "backups"),
            os.path.join("skills", "coding"),
            os.path.join("skills", "communication"),
            os.path.join("skills", "media"),
            os.path.join("skills", "web"),
            os.path.join("skills", "apps")
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created: {directory}")
            except Exception as e:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} Failed to create {directory}: {e}")
        
        return True
    
    def copy_config_files(self):
        """🔧 Copy configuration files"""
        print(f"{Fore.YELLOW}[3/8] Setting up configuration...{Style.RESET_ALL}")
        
        # Copy default config if config.yaml doesn't exist
        if os.path.exists(self.config_file) and not os.path.exists(self.config_target):
            try:
                shutil.copy(self.config_file, self.config_target)
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created config.yaml from default")
            except Exception as e:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} Failed to copy config: {e}")
        elif os.path.exists(self.config_target):
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} config.yaml already exists, keeping existing")
        else:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} Default config not found: {self.config_file}")
        
        # Create commands.json if doesn't exist
        commands_file = "commands.json"
        if not os.path.exists(commands_file):
            default_commands = {
                "commands": {
                    "greetings": ["hello", "hi", "hey jarvis"],
                    "time": ["what time", "current time", "time now"],
                    "date": ["what date", "today's date", "date today"],
                    "weather": ["weather", "temperature", "humidity"],
                    "search": ["search for", "google", "find"],
                    "open": ["open website", "launch", "go to"],
                    "play": ["play music", "play song", "play video"],
                    "stop": ["stop music", "stop playing", "pause"],
                    "code": ["write code", "create program", "code for"],
                    "system": ["system info", "computer info", "specs"],
                    "shutdown": ["shutdown", "turn off", "power off"],
                    "restart": ["restart", "reboot"]
                },
                "settings": {
                    "hotword": "jarvis",
                    "language": "en",
                    "voice": "male",
                    "response_speed": "normal"
                }
            }
            try:
                with open(commands_file, 'w', encoding='utf-8') as f:
                    json.dump(default_commands, f, indent=2)
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created commands.json")
            except Exception as e:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} Failed to create commands.json: {e}")
        
        return True
    
    def install_python_dependencies(self):
        """🔧 Install Python dependencies"""
        print(f"{Fore.YELLOW}[4/8] Installing Python dependencies...{Style.RESET_ALL}")
        
        if not os.path.exists(self.requirements_file):
            print(f"{Fore.RED}❌ requirements.txt not found{Style.RESET_ALL}")
            
            # Create basic requirements
            basic_requirements = [
                "colorama==0.4.6",
                "pyttsx3==2.90",
                "speechrecognition==3.10.0",
                "pyaudio==0.2.11",
                "pyautogui==0.9.54",
                "requests==2.31.0",
                "beautifulsoup4==4.12.2",
                "pynput==1.7.6",
                "psutil==5.9.6",
                "pyyaml==6.0.1",
                "pillow==10.1.0",
                "numpy==1.24.3",
                "openai==0.28.1",
                "python-dotenv==1.0.0",
                "flask==3.0.0",
                "selenium==4.15.2"
            ]
            
            try:
                with open(self.requirements_file, 'w') as f:
                    for req in basic_requirements:
                        f.write(req + '\n')
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created requirements.txt")
            except Exception as e:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} Failed to create requirements.txt: {e}")
                return False
        
        # Install dependencies
        try:
            print(f"  Installing from {self.requirements_file}...")
            
            # Upgrade pip first
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            
            # Install requirements
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", self.requirements_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Dependencies installed successfully")
                return True
            else:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} Failed to install dependencies:")
                print(f"  {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} Installation failed: {e}")
            return False
        except Exception as e:
            print(f"  {Fore.RED}✗{Style.RESET_ALL} Unexpected error: {e}")
            return False
    
    def install_system_dependencies(self):
        """🔧 Install system-specific dependencies"""
        print(f"{Fore.YELLOW}[5/8] Installing system dependencies...{Style.RESET_ALL}")
        
        if self.system == "Windows":
            return self.install_windows_dependencies()
        elif self.system == "Linux":
            return self.install_linux_dependencies()
        elif self.system == "Darwin":  # macOS
            return self.install_macos_dependencies()
        else:
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Unsupported system: {self.system}")
            return True
    
    def install_windows_dependencies(self):
        """🔧 Install Windows-specific dependencies"""
        try:
            print("  Installing Windows components...")
            
            # Check if Chocolatey is installed
            try:
                subprocess.run(["choco", "--version"], capture_output=True, check=True)
                has_choco = True
            except:
                has_choco = False
                print("  Chocolatey not found, skipping package manager installs")
            
            # Install using Chocolatey if available
            if has_choco:
                packages = [
                    "ffmpeg",
                    "vlc",
                    "python3",
                    "git"
                ]
                
                for package in packages:
                    try:
                        print(f"    Installing {package}...")
                        subprocess.run(["choco", "install", package, "-y"], capture_output=True, check=True)
                        print(f"    {Fore.GREEN}✓{Style.RESET_ALL} {package}")
                    except:
                        print(f"    {Fore.YELLOW}⚠{Style.RESET_ALL} Failed to install {package}")
            
            # Download additional tools
            self.download_windows_tools()
            
            return True
            
        except Exception as e:
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Windows dependency installation had issues: {e}")
            return True  # Continue anyway
    
    @staticmethod
    def install_linux_dependencies():
        """🔧 Install Linux-specific dependencies"""
        try:
            print("  Installing Linux packages...")
            
            # Detect package manager
            if os.path.exists("/usr/bin/apt-get"):
                # Debian/Ubuntu
                packages = [
                    "python3-pip",
                    "python3-dev",
                    "portaudio19-dev",
                    "ffmpeg",
                    "vlc",
                    "espeak",
                    "git",
                    "build-essential"
                ]
                
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y"] + packages, check=True)
                
            elif os.path.exists("/usr/bin/yum"):
                # RedHat/CentOS/Fedora
                packages = [
                    "python3-pip",
                    "python3-devel",
                    "portaudio-devel",
                    "ffmpeg",
                    "vlc",
                    "espeak",
                    "git",
                    "gcc",
                    "gcc-c++"
                ]
                
                subprocess.run(["sudo", "yum", "install", "-y"] + packages, check=True)
            
            elif os.path.exists("/usr/bin/pacman"):
                # Arch Linux
                packages = [
                    "python-pip",
                    "python-dev",
                    "portaudio",
                    "ffmpeg",
                    "vlc",
                    "espeak",
                    "git",
                    "base-devel"
                ]
                
                subprocess.run(["sudo", "pacman", "-S", "--noconfirm"] + packages, check=True)
            
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Linux packages installed")
            return True
            
        except Exception as e:
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Linux dependency installation had issues: {e}")
            return True  # Continue anyway
    
    @staticmethod
    def install_macos_dependencies():
        """🔧 Install macOS-specific dependencies"""
        try:
            print("  Installing macOS packages...")
            
            # Check if Homebrew is installed
            try:
                subprocess.run(["brew", "--version"], capture_output=True, check=True)
                has_brew = True
            except:
                has_brew = False
                print("  Homebrew not found, skipping package manager installs")
            
            if has_brew:
                packages = [
                    "portaudio",
                    "ffmpeg",
                    "vlc",
                    "espeak",
                    "git"
                ]
                
                for package in packages:
                    try:
                        subprocess.run(["brew", "install", package], capture_output=True, check=True)
                        print(f"    {Fore.GREEN}✓{Style.RESET_ALL} {package}")
                    except:
                        print(f"    {Fore.YELLOW}⚠{Style.RESET_ALL} Failed to install {package}")
            
            return True
            
        except Exception as e:
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} macOS dependency installation had issues: {e}")
            return True  # Continue anyway
    
    def download_windows_tools(self):
        """🔧 Download additional Windows tools"""
        try:
            tools_dir = self.tools_dir
            os.makedirs(tools_dir, exist_ok=True)
            
            # List of tools to download
            tools = [
                {
                    "name": "nircmd.exe",
                    "url": "https://www.nirsoft.net/utils/nircmd.zip",
                    "extract": True
                }
            ]
            
            print("  Downloading additional tools...")
            
            for tool in tools:
                tool_path = os.path.join(tools_dir, tool["name"])
                if not os.path.exists(tool_path):
                    print(f"    Downloading {tool['name']}...")
                    # Note: In production, you would use requests to download
                    # For now, we'll just create placeholder
                    with open(tool_path, 'w') as f:
                        f.write(f"Placeholder for {tool['name']}\n")
                    print(f"    {Fore.GREEN}✓{Style.RESET_ALL} {tool['name']} (placeholder)")
            
            return True
            
        except Exception as e:
            print(f"    {Fore.YELLOW}⚠{Style.RESET_ALL} Tool download failed: {e}")
            return False
    
    @staticmethod
    def setup_voice_profile():
        """🔧 Setup voice profile and models"""
        print(f"{Fore.YELLOW}[6/8] Setting up voice profile...{Style.RESET_ALL}")
        
        voice_profile_dir = "voice_profile"
        model_file = "vosk-model-small-en-in-0.4"
        
        # Create voice profile directory
        os.makedirs(voice_profile_dir, exist_ok=True)
        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created voice profile directory")
        
        # Check for Vosk model
        if not os.path.exists(model_file):
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Vosk model not found")
            print(f"  You can download it from: https://alphacephei.com/vosk/models")
            print(f"  Place it in the project root directory")
        else:
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Vosk model found")
        
        # Create basic voice settings
        voice_settings = {
            "rate": 180,
            "volume": 0.9,
            "voice": "default",
            "language": "en",
            "pitch": 50
        }
        
        try:
            with open(os.path.join(voice_profile_dir, "settings.json"), 'w') as f:
                json.dump(voice_settings, f, indent=2)
            print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created voice settings")
        except Exception as e:
            print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Failed to create voice settings: {e}")
        
        return True
    
    def setup_skills(self):
        """🔧 Setup skills directory structure"""
        print(f"{Fore.YELLOW}[7/8] Setting up skills...{Style.RESET_ALL}")
        
        # Create __init__.py files in skill directories
        skill_dirs = [
            "skills",
            "skills/coding",
            "skills/communication", 
            "skills/media",
            "skills/web",
            "skills/apps"
        ]
        
        for skill_dir in skill_dirs:
            init_file = os.path.join(skill_dir, "__init__.py")
            if os.path.exists(skill_dir) and not os.path.exists(init_file):
                try:
                    with open(init_file, 'w') as f:
                        f.write(f'"""\n{os.path.basename(skill_dir).capitalize()} skills\n"""\n\n__version__ = "1.0.0"\n')
                    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created {init_file}")
                except Exception as e:
                    print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Failed to create {init_file}: {e}")
        
        # Create sample skills if they don't exist
        sample_skills = {
            "skills/coding/code_writer.py": self.get_code_writer_skill(),
            "skills/communication/confirmation_engine.py": self.get_confirmation_engine_skill(),
            "skills/media/control_media.py": self.get_control_media_skill(),
            "skills/web/website_resolver.py": self.get_website_resolver_skill()
        }
        
        for skill_path, skill_content in sample_skills.items():
            if not os.path.exists(skill_path):
                try:
                    os.makedirs(os.path.dirname(skill_path), exist_ok=True)
                    with open(skill_path, 'w', encoding='utf-8') as f:
                        f.write(skill_content)
                    print(f"  {Fore.GREEN}✓{Style.RESET_ALL} Created sample skill: {skill_path}")
                except Exception as e:
                    print(f"  {Fore.YELLOW}⚠{Style.RESET_ALL} Failed to create {skill_path}: {e}")
        
        return True
    
    @staticmethod
    def get_code_writer_skill():
        """🔧 Return sample code writer skill"""
        return '''"""
💻 Code Writer Skill
Helps with coding tasks
"""

import pyautogui

class CodeWriter:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """💻 Execute coding assistance"""
        # Skill implementation here
        self.tts.speak("Code Writer skill loaded")
        return {'success': True, 'message': 'Code Writer ready'}
'''
    
    @staticmethod
    def get_confirmation_engine_skill():
        """🔧 Return sample confirmation engine skill"""
        return '''"""
✅ Confirmation Engine
Handles user confirmation for critical actions
"""

class ConfirmationEngine:
    def __init__(self, config, tts, stt):
        self.config = config
        self.tts = tts
        self.stt = stt
        
    def execute(self, params):
        """✅ Execute confirmation request"""
        # Skill implementation here
        self.tts.speak("Confirmation Engine loaded")
        return {'success': True, 'message': 'Confirmation Engine ready'}
'''
    
    @staticmethod
    def get_control_media_skill():
        """🔧 Return sample media control skill"""
        return '''"""
🎵 Media Controller
Controls media playback and system volume
"""

class MediaController:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """🎵 Execute media control command"""
        # Skill implementation here
        self.tts.speak("Media Controller loaded")
        return {'success': True, 'message': 'Media Controller ready'}
'''
    
    @staticmethod
    def get_website_resolver_skill():
        """🔧 Return sample website resolver skill"""
        return '''"""
🌐 Website Resolver
Resolves website names to URLs
"""

class WebsiteResolver:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """🌐 Execute website resolution"""
        # Skill implementation here
        self.tts.speak("Website Resolver loaded")
        return {'success': True, 'message': 'Website Resolver ready'}
'''
    
    def verify_installation(self):
        """🔧 Verify the installation"""
        print(f"{Fore.YELLOW}[8/8] Verifying installation...{Style.RESET_ALL}")
        
        checks = [
            ("Python version", self.check_python_version()),
            ("Requirements file", os.path.exists(self.requirements_file)),
            ("Config file", os.path.exists(self.config_target)),
            ("Data directory", os.path.exists(self.data_dir)),
            ("Skills directory", os.path.exists("skills")),
            ("Commands file", os.path.exists("commands.json"))
        ]
        
        all_passed = True
        for check_name, check_result in checks:
            if check_result:
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {check_name}")
            else:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} {check_name}")
                all_passed = False
        
        return all_passed
    
    def run(self):
        """🔧 Run the complete installation"""
        self.print_banner()
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Creating directories", self.create_directories),
            ("Setting up configuration", self.copy_config_files),
            ("Installing Python dependencies", self.install_python_dependencies),
            ("Installing system dependencies", self.install_system_dependencies),
            ("Setting up voice profile", self.setup_voice_profile),
            ("Setting up skills", self.setup_skills),
            ("Verifying installation", self.verify_installation)
        ]
        
        success = True
        for i, (step_name, step_func) in enumerate(steps, 1):
            try:
                if not step_func():
                    print(f"{Fore.RED}❌ {step_name} failed{Style.RESET_ALL}")
                    success = False
                    break
            except Exception as e:
                print(f"{Fore.RED}❌ Error in {step_name}: {e}{Style.RESET_ALL}")
                success = False
                break
        
        if success:
            print(f"\n{Fore.GREEN}✅ Installation completed successfully!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
            print("1. Edit config.yaml to customize settings")
            print("2. Run: python start_j.py")
            print("3. Say 'Hello Jarvis' to start")
            
            # Create start script
            self.create_start_script()
        else:
            print(f"\n{Fore.RED}❌ Installation failed{Style.RESET_ALL}")
            print("Please check the errors above and try again")
        
        return success
    
    def create_start_script(self):
        """🔧 Create start script for the system"""
        print(f"\n{Fore.YELLOW}Creating start script...{Style.RESET_ALL}")
        
        if self.system == "Windows":
            # Create start_j.bat
            bat_content = '''@echo off
echo Starting JARVIS Assistant...
title JARVIS Assistant
python jarvis.py
pause
'''
            try:
                with open("start_j.bat", "w") as f:
                    f.write(bat_content)
                print(f"{Fore.GREEN}✅ Created start_j.bat{Style.RESET_ALL}")
                print(f"   Run: start_j.bat")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ Failed to create start_j.bat: {e}{Style.RESET_ALL}")
        
        # Create start_j.py (cross-platform)
        py_content = '''#!/usr/bin/env python3
"""
🚀 JARVIS Start Script
Starts the JARVIS Assistant
"""

import os
import sys
import subprocess

def main():
    """🚀 Main entry point"""
    print("🚀 Starting JARVIS Assistant...")
    
    # Check if jarvis.py exists
    if not os.path.exists("jarvis.py"):
        print("❌ Error: jarvis.py not found!")
        print("Please run install.py first")
        return 1
    
    # Run jarvis.py
    try:
        result = subprocess.run([sys.executable, "jarvis.py"])
        return result.returncode
    except KeyboardInterrupt:
        print("\n🛑 JARVIS stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error starting JARVIS: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''
        
        try:
            with open("start_j.py", "w", encoding="utf-8") as f:
                f.write(py_content)
            
            # Make executable on Unix-like systems
            if self.system != "Windows":
                os.chmod("start_j.py", 0o755)
            
            print(f"{Fore.GREEN}✅ Created start_j.py{Style.RESET_ALL}")
            print(f"   Run: python start_j.py")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Failed to create start_j.py: {e}{Style.RESET_ALL}")

def main():
    """🔧 Main installation function"""
    installer = JarvisInstaller()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Install JARVIS Assistant")
    parser.add_argument("--skip-deps", action="store_true", help="Skip dependency installation")
    parser.add_argument("--force", action="store_true", help="Force reinstallation")
    args = parser.parse_args()
    
    if args.skip_deps:
        print(f"{Fore.YELLOW}Skipping dependency installation{Style.RESET_ALL}")
        # Modify installer to skip dependency steps
        installer.install_python_dependencies = lambda: True
        installer.install_system_dependencies = lambda: True
    
    if args.force:
        print(f"{Fore.YELLOW}Forcing reinstallation{Style.RESET_ALL}")
        # Add force logic here if needed
    
    success = installer.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()