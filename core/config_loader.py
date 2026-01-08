"""
⚙️ Configuration Loader
Loads and manages all JARVIS configuration
"""

import json
import os
from pathlib import Path

import yaml
from colorama import Fore, Style


class ConfigLoader:
    def __init__(self):
        self.config = None
        self.config_path = "config.yaml"
        self.default_config = self.get_default_config()

    def load_config(self):
        """⚙️ Load configuration from file or create default"""
        try:
            # Check if config file exists
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f)
                print(
                    Fore.GREEN
                    + f"✅ Config loaded from {self.config_path}"
                    + Style.RESET_ALL
                )
            else:
                # Create default config
                self.config = self.default_config
                self.save_config()
                print(
                    Fore.YELLOW
                    + f"⚠️ Created default config at {self.config_path}"
                    + Style.RESET_ALL
                )

            # Ensure required directories exist
            self.create_directories()

            return self.config

        except Exception as e:
            print(Fore.RED + f"❌ Config load error: {str(e)}" + Style.RESET_ALL)
            return self.default_config

    def save_config(self):
        """⚙️ Save configuration to file"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            return True
        except:
            return False

    def create_directories(self):
        """⚙️ Create required directories"""
        dirs = ["voice_profile", "memory", "logs", "skills", "core", "utils", "vision"]

        for dir_name in dirs:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
                print(
                    Fore.GREEN + f"📁 Created directory: {dir_name}" + Style.RESET_ALL
                )

    def get_default_config(self):
        """⚙️ Get default configuration"""
        return {
            "jarvis": {
                "name": "JARVIS",
                "version": "3.0",
                "language": "hinglish",
                "voice": {
                    "gender": "male",
                    "rate": 180,
                    "volume": 1.0,
                    "accent": "indian",
                },
                "wake_word": "jarvis",
                "listening_timeout": 5,
                "openrouter": {
                    "api_key": "",
                    "model": "deepseek/deepseek-r1:free",
                    "endpoint": "https://openrouter.ai/api/v1/chat/completions",
                },
                "security": {
                    "voice_auth": True,
                    "face_auth": False,
                    "permission_level": "high",
                },
                "memory": {"short_term_size": 50, "long_term_days": 30},
                "emotions": {"enabled": True, "sensitivity": 0.7},
                "indicators": {
                    "listening": "🎙️",
                    "thinking": "🧠",
                    "success": "✅",
                    "error": "❌",
                    "warning": "⚠️",
                    "searching": "🔍",
                    "app_open": "🚀",
                    "message_sent": "📱✅",
                    "voice_train": "🎤",
                    "custom_cmd": "🛠️",
                    "system_info": "🖥️",
                    "heal": "🛠️🔄",
                },
            },
            "paths": {
                "voice_profile": "voice_profile/voice_fingerprint.npy",
                "commands": "commands.json",
                "memory_short": "memory/short_term.json",
                "memory_long": "memory/long_term.json",
                "custom_cmds": "memory/custom_commands.json",
                "error_log": "memory/error_log.json",
            },
            "websites": {
                "common": {
                    "youtube": "https://youtube.com",
                    "google": "https://google.com",
                    "github": "https://github.com",
                    "whatsapp": "https://web.whatsapp.com",
                    "facebook": "https://facebook.com",
                    "instagram": "https://instagram.com",
                    "twitter": "https://twitter.com",
                    "linkedin": "https://linkedin.com",
                }
            },
        }

    def update_config(self, key, value):
        """⚙️ Update configuration value"""
        keys = key.split(".")
        config_ref = self.config

        # Navigate to the nested key
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]

        # Set the value
        config_ref[keys[-1]] = value

        # Save to file
        self.save_config()
        return True

    def get(self, key, default=None):
        """⚙️ Get configuration value"""
        keys = key.split(".")
        config_ref = self.config

        for k in keys:
            if isinstance(config_ref, dict) and k in config_ref:
                config_ref = config_ref[k]
            else:
                return default

        return config_ref
