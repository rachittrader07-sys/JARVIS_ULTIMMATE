"""
🎯 Decision Engine
Makes decisions about which skill to use
"""

import json
import os
from datetime import datetime

from colorama import Fore, Style


class DecisionEngine:
    def __init__(self, config):
        self.config = config
        self.skill_weights = self.load_skill_weights()
        self.context_history = []
        self.max_context_length = 10

    def decide(self, intent, entities, context):
        """🎯 Decide which action to take"""
        print(
            Fore.YELLOW
            + self.config["indicators"]["thinking"]
            + " Making decision..."
            + Style.RESET_ALL
        )

        # Add to context history
        self.context_history.append(
            {
                "intent": intent,
                "entities": entities,
                "timestamp": datetime.now().isoformat(),
                "context": context,
            }
        )

        # Keep history limited
        if len(self.context_history) > self.max_context_length:
            self.context_history = self.context_history[-self.max_context_length :]

        # Decision making based on intent
        if intent == "open_app":
            return self.decide_open_app(entities, context)
        elif intent == "open_website":
            return self.decide_open_website(entities, context)
        elif intent == "search_web":
            return self.decide_search_web(entities, context)
        elif intent == "send_whatsapp":
            return self.decide_send_whatsapp(entities, context)
        elif intent == "play_music":
            return self.decide_play_music(entities, context)
        elif intent == "system_info":
            return self.decide_system_info(entities, context)
        elif intent == "control_window":
            return self.decide_control_window(entities, context)
        elif intent == "code_assist":
            return self.decide_code_assist(entities, context)
        elif intent == "custom_command":
            return self.decide_custom_command(entities, context)
        else:
            return self.decide_unknown(intent, entities, context)

    def decide_open_app(self, entities, context):
        """🎯 Decide how to open app"""
        app_name = entities.get("app_name", "")

        # Check if app is in known list
        known_apps = self.get_known_apps()

        # Check for safety
        if self.is_dangerous_app(app_name):
            return {
                "action": "confirm_dangerous",
                "params": {"app_name": app_name, "reason": "dangerous_app"},
                "confidence": 0.9,
                "requires_confirmation": True,
            }

        return {
            "action": "open_app",
            "params": {"app_name": app_name, "method": "auto"},
            "confidence": 0.8,
            "requires_confirmation": False,
        }

    def decide_open_website(self, entities, context):
        """🎯 Decide how to open website"""
        website_name = entities.get("website_name", "")

        # Check if website is in known list
        known_websites = self.config["websites"]["common"]

        # Check for safety
        if self.is_dangerous_website(website_name):
            return {
                "action": "confirm_dangerous",
                "params": {"website_name": website_name, "reason": "dangerous_website"},
                "confidence": 0.9,
                "requires_confirmation": True,
            }

        return {
            "action": "open_website",
            "params": {"website_name": website_name, "method": "auto"},
            "confidence": 0.8,
            "requires_confirmation": False,
        }

    @staticmethod
    def decide_search_web(entities, context):
        """🎯 Decide how to search web"""
        query = entities.get("query", "")

        return {
            "action": "search_web",
            "params": {"query": query, "engine": "google"},
            "confidence": 0.9,
            "requires_confirmation": False,
        }

    def decide_send_whatsapp(self, entities, context):
        """🎯 Decide how to send WhatsApp"""
        person = entities.get("person", "")
        message = entities.get("message", "")

        # Check if person is in contacts
        contacts = self.get_contacts()
        person_found = False

        for contact in contacts:
            if person.lower() in contact["name"].lower():
                person_found = True
                person = contact["name"]
                break

        return {
            "action": "send_whatsapp",
            "params": {
                "person": person,
                "message": message,
                "person_found": person_found,
            },
            "confidence": 0.7,
            "requires_confirmation": not message,  # Confirm if message is empty
        }

    @staticmethod
    def decide_play_music(entities, context):
        """🎯 Decide how to play music"""
        song = entities.get("song", "")

        return {
            "action": "play_music",
            "params": {"song": song, "platform": "youtube"},
            "confidence": 0.8,
            "requires_confirmation": False,
        }

    @staticmethod
    def decide_system_info(entities, context):
        """🎯 Decide what system info to show"""
        query = entities.get("query", "all")

        return {
            "action": "system_info",
            "params": {"query": query},
            "confidence": 0.9,
            "requires_confirmation": False,
        }

    @staticmethod
    def decide_control_window(entities, context):
        """🎯 Decide window control action"""
        # Extract action from entities
        action = "minimize"
        if "maximize" in str(entities).lower():
            action = "maximize"
        elif "close" in str(entities).lower():
            action = "close"
        elif "restore" in str(entities).lower():
            action = "restore"

        return {
            "action": "control_window",
            "params": {"action": action, "window": "current"},
            "confidence": 0.9,
            "requires_confirmation": action == "close",  # Confirm for close
        }

    @staticmethod
    def decide_code_assist(entities, context):
        """🎯 Decide coding assistance"""
        query = str(entities).lower()

        return {
            "action": "code_assist",
            "params": {"query": query, "language": "python"},
            "confidence": 0.7,
            "requires_confirmation": False,
        }

    @staticmethod
    def decide_custom_command(entities, context):
        """🎯 Decide custom command execution"""
        command_name = entities.get("command_name", "")
        actions = entities.get("actions", [])

        return {
            "action": "execute_custom",
            "params": {"command_name": command_name, "actions": actions},
            "confidence": 0.95,
            "requires_confirmation": False,
        }

    @staticmethod
    def decide_unknown(intent, entities, context):
        """🎯 Decide for unknown intents"""
        # Use AI fallback for unknown commands
        return {
            "action": "ai_fallback",
            "params": {
                "original_intent": intent,
                "entities": entities,
                "context": context,
            },
            "confidence": 0.3,
            "requires_confirmation": True,
        }

    @staticmethod
    def load_skill_weights():
        """🎯 Load skill usage weights"""
        weights_file = "memory/skill_weights.json"
        default_weights = {
            "open_app": 1.0,
            "open_website": 1.0,
            "search_web": 1.0,
            "send_whatsapp": 1.0,
            "play_music": 1.0,
            "system_info": 1.0,
            "control_window": 1.0,
            "code_assist": 1.0,
        }

        try:
            if os.path.exists(weights_file):
                with open(weights_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass

        return default_weights

    @staticmethod
    def get_known_apps():
        """🎯 Get list of known apps"""
        apps_file = "memory/known_apps.json"
        default_apps = [
            "chrome",
            "firefox",
            "edge",
            "vscode",
            "notepad",
            "calculator",
            "cmd",
            "powershell",
            "python",
            "excel",
            "word",
            "powerpoint",
            "outlook",
            "photoshop",
            "premiere",
            "spotify",
            "whatsapp",
            "discord",
            "telegram",
        ]

        try:
            if os.path.exists(apps_file):
                with open(apps_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass

        return default_apps

    @staticmethod
    def get_contacts():
        """🎯 Get list of contacts"""
        contacts_file = "memory/contacts.json"

        try:
            if os.path.exists(contacts_file):
                with open(contacts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except:
            pass

        return []

    @staticmethod
    def is_dangerous_app(app_name):
        """🎯 Check if app is dangerous"""
        dangerous_apps = [
            "cmd",
            "powershell",
            "regedit",
            "taskmgr",
            "diskpart",
            "format",
            "shutdown",
            "del",
            "rm",
        ]

        for dangerous in dangerous_apps:
            if dangerous in app_name.lower():
                return True

        return False

    @staticmethod
    def is_dangerous_website(website_name):
        """🎯 Check if website is dangerous"""
        dangerous_websites = [
            "virus",
            "hack",
            "malware",
            "phishing",
            "scam",
            "fraud",
            "dangerous",
            "unsafe",
        ]

        for dangerous in dangerous_websites:
            if dangerous in website_name.lower():
                return True

        return False
