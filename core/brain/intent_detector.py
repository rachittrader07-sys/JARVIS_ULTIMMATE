"""
🧠 Intent Detection System
Detects what user wants from their command
"""

import json
import os
import re
from datetime import datetime


class IntentDetector:
    def __init__(self, config):
        self.config = config
        self.intent_patterns = self.load_intent_patterns()
        self.entity_patterns = self.load_entity_patterns()

    def load_intent_patterns(self):
        """🧠 Load intent recognition patterns"""
        patterns = {
            "open_app": [
                r"open (.*)",
                r"(.*) open karo",
                r"start (.*)",
                r"(.*) chalao",
                r"launch (.*)",
                r"run (.*)",
            ],
            "open_website": [
                r"open (.*) website",
                r"(.*) website kholo",
                r"go to (.*)",
                r"navigate to (.*)",
                r"(.*) par jao",
            ],
            "search_web": [
                r"search (.*)",
                r"dhundho (.*)",
                r"google (.*)",
                r"find (.*)",
                r"look up (.*)",
            ],
            "send_whatsapp": [
                r"whatsapp (.*)",
                r"message (.*)",
                r"text (.*)",
                r"send message to (.*)",
                r"(.*) ko message bhejo",
                r"(.*) ko bol do",
            ],
            "play_music": [
                r"play (.*)",
                r"music (.*)",
                r"gaana (.*)",
                r"song (.*)",
                r"play music",
                r"gaana chalao",
            ],
            "system_info": [
                r"system (.*)",
                r"battery (.*)",
                r"cpu (.*)",
                r"ram (.*)",
                r"kitna (.*)",
                r"kya (.*)",
                r"kaise (.*)",
            ],
            "control_window": [
                r"minimize (.*)",
                r"maximize (.*)",
                r"close (.*)",
                r"window (.*)",
                r"restore (.*)",
            ],
            "code_assist": [
                r"code (.*)",
                r"program (.*)",
                r"python (.*)",
                r"write (.*) code",
                r"create (.*) program",
            ],
            "unknown": [],  # Will be handled by fallback
        }
        return patterns

    def load_entity_patterns(self):
        """🧠 Load entity extraction patterns"""
        patterns = {
            "app_name": r"open\s+(.+?)(?:\s+app|\s+|$)",
            "website_name": r"website\s+(.+?)(?:\s+|$)",
            "search_query": r"search\s+(.+?)(?:\s+|$)",
            "person_name": r"to\s+(.+?)(?:\s+|$)",
            "message_content": r"message\s+(.+?)(?:\s+|$)",
            "music_query": r"play\s+(.+?)(?:\s+|$)",
        }
        return patterns

    def detect(self, command_text):
        """🧠 Detect intent and extract entities from command"""
        command_lower = command_text.lower().strip()

        # Check for custom commands first
        custom_intent = self.check_custom_commands(command_lower)
        if custom_intent:
            return custom_intent

        # Detect intent
        intent = "unknown"
        confidence = 0
        entities = {}

        for intent_name, patterns in self.intent_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower, re.IGNORECASE)
                if match:
                    intent = intent_name
                    confidence = 0.8

                    # Extract entities based on intent
                    entities = self.extract_entities(command_lower, intent_name)
                    break

            if intent != "unknown":
                break

        # If still unknown, try fuzzy matching
        if intent == "unknown":
            intent, confidence = self.fuzzy_intent_match(command_lower)

        # Add emotion context if available
        entities["timestamp"] = datetime.now().isoformat()

        return intent, entities

    def extract_entities(self, command_text, intent):
        """🧠 Extract entities from command text"""
        entities = {}

        if intent == "open_app":
            match = re.search(self.entity_patterns["app_name"], command_text)
            if match:
                entities["app_name"] = match.group(1)

        elif intent == "open_website":
            match = re.search(self.entity_patterns["website_name"], command_text)
            if match:
                entities["website_name"] = match.group(1)
            else:
                # Try to extract website name without "website" keyword
                words = command_text.split()
                if "open" in words:
                    idx = words.index("open")
                    if idx + 1 < len(words):
                        entities["website_name"] = words[idx + 1]

        elif intent == "search_web":
            match = re.search(self.entity_patterns["search_query"], command_text)
            if match:
                entities["query"] = match.group(1)

        elif intent == "send_whatsapp":
            # Extract person name
            match = re.search(self.entity_patterns["person_name"], command_text)
            if match:
                entities["person"] = match.group(1)

            # Extract message content if available
            msg_match = re.search(self.entity_patterns["message_content"], command_text)
            if msg_match:
                entities["message"] = msg_match.group(1)

        elif intent == "play_music":
            match = re.search(self.entity_patterns["music_query"], command_text)
            if match:
                entities["song"] = match.group(1)

        return entities

    def fuzzy_intent_match(self, command_text):
        """🧠 Fuzzy matching for unknown intents"""
        keywords_intent_map = {
            "open": "open_app",
            "start": "open_app",
            "website": "open_website",
            "search": "search_web",
            "google": "search_web",
            "whatsapp": "send_whatsapp",
            "message": "send_whatsapp",
            "play": "play_music",
            "music": "play_music",
            "song": "play_music",
            "system": "system_info",
            "battery": "system_info",
            "cpu": "system_info",
            "ram": "system_info",
            "minimize": "control_window",
            "maximize": "control_window",
            "close": "control_window",
            "code": "code_assist",
            "program": "code_assist",
            "python": "code_assist",
        }

        words = command_text.split()
        for word in words:
            if word in keywords_intent_map:
                return keywords_intent_map[word], 0.6

        return "unknown", 0.3

    def check_custom_commands(self, command_text):
        """🧠 Check if command matches any custom saved command"""
        try:
            custom_cmds_path = self.config["paths"]["custom_cmds"]
            if os.path.exists(custom_cmds_path):
                with open(custom_cmds_path, "r", encoding="utf-8") as f:
                    custom_commands = json.load(f)

                for cmd_name, cmd_data in custom_commands.items():
                    trigger = cmd_data.get("trigger", "").lower()
                    if trigger in command_text:
                        return {
                            "intent": "custom_command",
                            "entities": {
                                "command_name": cmd_name,
                                "actions": cmd_data.get("actions", []),
                            },
                            "confidence": 0.9,
                        }
        except:
            pass

        return None
