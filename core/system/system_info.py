"""
🖥️ System Information Provider
Gets detailed system information
"""

import psutil
import platform
import socket
import datetime
from colorama import Fore, Style

class SystemInfo:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
    
    def execute(self, params):
        """🖥️ Provide system information"""
        query = params.get('query', '').lower()
        
        if not query:
            # Provide general system info
            info = self.get_all_info()
            self.speak_system_info(info)
            return {'success': True, 'info': info}
        
        # Specific query
        if 'battery' in query:
            info = self.get_battery_info()
        elif 'cpu' in query:
            info = self.get_cpu_info()
        elif 'ram' in query or 'memory' in query:
            info = self.get_memory_info()
        elif 'disk' in query or 'storage' in query:
            info = self.get_disk_info()
        elif 'network' in query or 'internet' in query:
            info = self.get_network_info()
        elif 'all' in query or 'full' in query:
            info = self.get_all_info()
        else:
            info = self.get_general_info()
        
        self.speak_system_info(info)
        return {'success': True, 'info': info}
    
    def get_all_info(self):
        """🖥️ Get all system information"""
        info = {
            'general': self.get_general_info(),
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'battery': self.get_battery_info(),
            'network': self.get_network_info()
        }
        return info
    
    @staticmethod
    def get_general_info():
        """🖥️ Get general system info"""
        info = {
            'system': platform.system(),
            'version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': socket.gethostname(),
            'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
            'uptime': str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))
        }
        return info
    
    @staticmethod
    def get_cpu_info():
        """🖥️ Get CPU information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        
        info = {
            'cpu_usage': f"{cpu_percent}%",
            'cpu_cores': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'cpu_frequency': f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A",
            'cpu_per_core': psutil.cpu_percent(percpu=True)
        }
        return info
    
    @staticmethod
    def get_memory_info():
        """🖥️ Get memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        info = {
            'total_ram': f"{mem.total / (1024**3):.2f} GB",
            'available_ram': f"{mem.available / (1024**3):.2f} GB",
            'used_ram': f"{mem.used / (1024**3):.2f} GB",
            'ram_percentage': f"{mem.percent}%",
            'total_swap': f"{swap.total / (1024**3):.2f} GB" if swap.total > 0 else "N/A",
            'swap_percentage': f"{swap.percent}%" if swap.total > 0 else "N/A"
        }
        return info
    
    @staticmethod
    def get_disk_info():
        """🖥️ Get disk information"""
        partitions = psutil.disk_partitions()
        disk_info = {}
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    'mountpoint': partition.mountpoint,
                    'total': f"{usage.total / (1024**3):.2f} GB",
                    'used': f"{usage.used / (1024**3):.2f} GB",
                    'free': f"{usage.free / (1024**3):.2f} GB",
                    'percentage': f"{usage.percent}%"
                }
            except:
                continue
        
        return disk_info
    
    @staticmethod
    def get_battery_info():
        """🖥️ Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                info = {
                    'percentage': f"{battery.percent}%",
                    'plugged': "Yes" if battery.power_plugged else "No",
                    'time_left': f"{battery.secsleft // 3600} hours {(battery.secsleft % 3600) // 60} minutes" if battery.secsleft > 0 else "Calculating"
                }
            else:
                info = {'error': 'No battery found'}
        except:
            info = {'error': 'Could not get battery info'}
        
        return info
    
    @staticmethod
    def get_network_info():
        """🖥️ Get network information"""
        try:
            # Get IP address
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            
            # Get network stats
            net_io = psutil.net_io_counters()
            
            info = {
                'ip_address': ip_address,
                'bytes_sent': f"{net_io.bytes_sent / (1024**2):.2f} MB",
                'bytes_recv': f"{net_io.bytes_recv / (1024**2):.2f} MB",
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            }
        except:
            info = {'error': 'Could not get network info'}
        
        return info
    
    def speak_system_info(self, info):
        """🖥️ Speak system information in understandable way"""
        if 'general' in info:
            # Full system info
            message = "Sir, here is your system information: "
            
            # CPU
            cpu = info['cpu']
            message += f"CPU usage is {cpu['cpu_usage']}. "
            
            # RAM
            mem = info['memory']
            message += f"RAM usage is {mem['ram_percentage']}. "
            
            # Battery
            if 'battery' in info and 'percentage' in info['battery']:
                battery = info['battery']
                message += f"Battery is at {battery['percentage']}. "
                if battery.get('plugged') == "Yes":
                    message += "System is plugged in. "
            
            # Disk
            disk = info['disk']
            for drive, stats in disk.items():
                if 'C:' in drive or 'C:\\' in stats.get('mountpoint', ''):
                    message += f"C drive has {stats['free']} free space. "
                    break
            
            self.tts.speak(message)
            
        elif 'cpu_usage' in info:
            # CPU specific
            message = f"Sir, CPU usage is {info['cpu_usage']}"
            self.tts.speak(message)
            
        elif 'ram_percentage' in info:
            # RAM specific
            message = f"Sir, RAM usage is {info['ram_percentage']}"
            self.tts.speak(message)
            
        elif 'percentage' in info:
            # Battery specific
            message = f"Sir, battery is at {info['percentage']}"
            if info.get('plugged') == "Yes":
                message += " and system is plugged in"
            self.tts.speak(message)