"""
🛠️ Helper Functions
Common utility functions for JARVIS
"""

import os
import sys
import json
import time
import random
import string
from datetime import datetime
from colorama import Fore, Style

def print_colored(text, color="white", style="normal"):
    """🛠️ Print colored text"""
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    
    style_map = {
        "normal": Style.NORMAL,
        "bright": Style.BRIGHT,
        "dim": Style.DIM
    }
    
    color_code = color_map.get(color.lower(), Fore.WHITE)
    style_code = style_map.get(style.lower(), Style.NORMAL)
    
    print(f"{style_code}{color_code}{text}{Style.RESET_ALL}")

def create_directory(path):
    """🛠️ Create directory if it doesn't exist"""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return True
        return True
    except:
        return False

def read_json_file(filepath):
    """🛠️ Read JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

def write_json_file(filepath, data):
    """🛠️ Write JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_timestamp():
    """🛠️ Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_date():
    """🛠️ Get current date string"""
    return datetime.now().strftime("%Y-%m-%d")

def get_time():
    """🛠️ Get current time string"""
    return datetime.now().strftime("%H:%M:%S")

def format_duration(seconds):
    """🛠️ Format duration in seconds to readable string"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def generate_id(length=8):
    """🛠️ Generate random ID"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def safe_execute(func, *args, **kwargs):
    """🛠️ Execute function safely with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print_colored(f"Error in {func.__name__}: {str(e)}", "red")
        return None

def check_file_size(filepath, max_size_mb=10):
    """🛠️ Check if file size is within limit"""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb <= max_size_mb
    except:
        return False

def clear_screen():
    """🛠️ Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def progress_bar(iteration, total, length=50):
    """🛠️ Display progress bar"""
    percent = int(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    print(f'\r|{bar}| {percent}%', end='\r')
    if iteration == total:
        print()

def human_readable_size(size_bytes):
    """🛠️ Convert bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def is_admin():
    """🛠️ Check if running as administrator"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_system_language():
    """🛠️ Get system language"""
    import locale
    try:
        return locale.getdefaultlocale()[0]
    except:
        return "en_US"

def backup_file(filepath):
    """🛠️ Create backup of file"""
    try:
        if os.path.exists(filepath):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{filepath}.backup_{timestamp}"
            import shutil
            shutil.copy2(filepath, backup_path)
            return backup_path
    except:
        pass
    return None