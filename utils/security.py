"""
🔒 Security Utilities
Handles security and permissions
"""

import hashlib
import json
import os
from datetime import datetime
from colorama import Fore, Style

class SecurityManager:
    def __init__(self, config):
        self.config = config
        self.permissions = self.load_permissions()
        self.voice_profiles = self.load_voice_profiles()
        
    @staticmethod
    def load_permissions():
        """🔒 Load permissions from file"""
        permissions_file = "memory/permissions.json"
        default_permissions = {
            'dangerous_commands': {
                'shutdown': 'confirm',
                'format': 'block',
                'delete_all': 'confirm',
                'registry': 'block',
                'system32': 'block'
            },
            'allowed_apps': [
                'chrome', 'firefox', 'vscode', 'notepad',
                'calculator', 'spotify', 'whatsapp'
            ],
            'blocked_websites': [
                'malware.com', 'virus.com', 'hack.com'
            ],
            'voice_auth_enabled': True
        }
        
        try:
            if os.path.exists(permissions_file):
                with open(permissions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return default_permissions
    
    @staticmethod
    def load_voice_profiles():
        """🔒 Load voice profiles"""
        profiles_file = "memory/voice_profiles.json"
        
        try:
            if os.path.exists(profiles_file):
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {}
    
    def check_command_safety(self, command, context):
        """🔒 Check if command is safe to execute"""
        command_lower = command.lower()
        
        # Check for dangerous commands
        dangerous = self.permissions.get('dangerous_commands', {})
        
        for dangerous_cmd, action in dangerous.items():
            if dangerous_cmd in command_lower:
                return {
                    'safe': action != 'block',
                    'action': action,
                    'reason': f'Contains dangerous command: {dangerous_cmd}',
                    'requires_confirmation': action == 'confirm'
                }
        
        # Check for blocked websites
        if 'open' in command_lower or 'website' in command_lower:
            for blocked in self.permissions.get('blocked_websites', []):
                if blocked in command_lower:
                    return {
                        'safe': False,
                        'action': 'block',
                        'reason': f'Blocked website: {blocked}',
                        'requires_confirmation': False
                    }
        
        # Check context for suspicious patterns
        suspicious_patterns = [
            'format c:', 'del *', 'rm -rf', 'shutdown -f',
            'taskkill /f', 'reg delete', 'netsh firewall'
        ]
        
        for pattern in suspicious_patterns:
            if pattern in command_lower:
                return {
                    'safe': False,
                    'action': 'block',
                    'reason': f'Suspicious pattern: {pattern}',
                    'requires_confirmation': False
                }
        
        return {
            'safe': True,
            'action': 'allow',
            'reason': 'Command appears safe',
            'requires_confirmation': False
        }
    
    def authenticate_voice(self, voice_features):
        """🔒 Authenticate user by voice"""
        if not self.permissions.get('voice_auth_enabled', True):
            return {'authenticated': True, 'user': 'default'}
        
        # Simple voice authentication (in production, use ML)
        # This is a placeholder implementation
        
        # Extract features
        pitch = voice_features.get('pitch', 0)
        speed = voice_features.get('speed', 0)
        
        # Check against stored profiles
        for user_id, profile in self.voice_profiles.items():
            profile_pitch = profile.get('pitch', 0)
            profile_speed = profile.get('speed', 0)
            
            # Simple threshold check
            if (abs(pitch - profile_pitch) < 20 and 
                abs(speed - profile_speed) < 20):
                return {
                    'authenticated': True,
                    'user': user_id,
                    'confidence': 0.8
                }
        
        # Unknown voice
        return {
            'authenticated': False,
            'user': 'unknown',
            'confidence': 0.3,
            'message': 'Voice not recognized'
        }
    
    def register_voice(self, user_id, voice_features):
        """🔒 Register new voice profile"""
        self.voice_profiles[user_id] = {
            'pitch': voice_features.get('pitch', 0),
            'speed': voice_features.get('speed', 0),
            'timestamp': datetime.now().isoformat(),
            'samples': 1
        }
        
        self.save_voice_profiles()
        return True
    
    def update_voice_profile(self, user_id, voice_features):
        """🔒 Update existing voice profile"""
        if user_id in self.voice_profiles:
            profile = self.voice_profiles[user_id]
            samples = profile.get('samples', 1)
            
            # Update with moving average
            profile['pitch'] = (profile['pitch'] * samples + voice_features.get('pitch', 0)) / (samples + 1)
            profile['speed'] = (profile['speed'] * samples + voice_features.get('speed', 0)) / (samples + 1)
            profile['samples'] = samples + 1
            profile['last_updated'] = datetime.now().isoformat()
            
            self.save_voice_profiles()
            return True
        
        return False
    
    def save_voice_profiles(self):
        """🔒 Save voice profiles to file"""
        try:
            with open('memory/voice_profiles.json', 'w', encoding='utf-8') as f:
                json.dump(self.voice_profiles, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def log_security_event(self, event_type, details):
        """🔒 Log security event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'details': details,
            'ip': self.get_ip_address()
        }
        
        try:
            log_file = "memory/security_log.json"
            logs = []
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            logs.append(log_entry)
            
            # Keep only last 1000 entries
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Security log error: {str(e)}" + Style.RESET_ALL)
    
    @staticmethod
    def get_ip_address():
        """🔒 Get IP address"""
        try:
            import socket
            return socket.gethostbyname(socket.gethostname())
        except:
            return "unknown"
    
    @staticmethod
    def encrypt_data(data, key):
        """🔒 Simple encryption (for demonstration)"""
        # Note: In production, use proper encryption like AES
        import base64
        data_str = json.dumps(data)
        encoded = base64.b64encode(data_str.encode()).decode()
        return encoded
    
    @staticmethod
    def decrypt_data(encrypted_data, key):
        """🔒 Simple decryption"""
        import base64
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return json.loads(decoded)
        except:
            return {}