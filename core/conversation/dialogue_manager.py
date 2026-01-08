"""
🗣️ Dialogue Manager
Manages conversations and context
"""

import json
import time
from datetime import datetime

from colorama import Fore, Style


class DialogueManager:
    def __init__(self, config):
        self.config = config
        self.conversation_history = []
        self.current_context = {}
        self.expecting_followup = False
        self.followup_type = None
        self.followup_data = {}
        self.max_history = 20

    def add_to_history(self, user_input, jarvis_response):
        """🗣️ Add conversation to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "jarvis": jarvis_response,
            "context": self.current_context.copy(),
        }

        self.conversation_history.append(entry)

        # Keep history limited
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history :]

        # Save history periodically
        if len(self.conversation_history) % 5 == 0:
            self.save_history()

    def get_context(self):
        """🗣️ Get current context"""
        return self.current_context

    def update_context(self, key, value):
        """🗣️ Update context"""
        self.current_context[key] = value

    def clear_context(self):
        """🗣️ Clear context"""
        self.current_context = {}
        self.expecting_followup = False
        self.followup_type = None
        self.followup_data = {}

    def expecting_followup(self):
        """🗣️ Check if expecting followup"""
        return self.expecting_followup

    def set_followup(self, followup_type, data=None):
        """🗣️ Set followup expectation"""
        self.expecting_followup = True
        self.followup_type = followup_type
        self.followup_data = data or {}

        print(Fore.CYAN + f"🗣️ Expecting followup: {followup_type}" + Style.RESET_ALL)

    def handle_followup(self, user_input):
        """🗣️ Handle followup response"""
        if not self.expecting_followup:
            return user_input

        processed_input = user_input

        if self.followup_type == "whatsapp_message":
            # Add message to WhatsApp data
            if "person" in self.followup_data:
                processed_input = f"whatsapp {self.followup_data['person']} ko message bhejo: {user_input}"

        elif self.followup_type == "app_name":
            # Add app name to command
            processed_input = f"open {user_input}"

        elif self.followup_type == "website_name":
            # Add website name to command
            processed_input = f"open {user_input} website"

        elif self.followup_type == "search_query":
            # Add search query
            processed_input = f"search {user_input}"

        # Clear followup
        self.clear_followup()

        return processed_input

    def clear_followup(self):
        """🗣️ Clear followup expectation"""
        self.expecting_followup = False
        self.followup_type = None
        self.followup_data = {}

    def add_context(self, text):
        """🗣️ Add context to user input"""
        # Check if this is a followup to previous command
        if self.conversation_history:
            last_entry = self.conversation_history[-1]
            last_user = last_entry["user"].lower()

            # Check for common followup patterns
            if any(word in last_user for word in ["open", "search", "play"]):
                # This might be a search query or parameter
                if "youtube" in last_user or "website" in last_user:
                    return f"search {text}"

        return text

    def get_conversation_summary(self, num_entries=5):
        """🗣️ Get conversation summary"""
        if not self.conversation_history:
            return "No conversation history"

        recent = self.conversation_history[-num_entries:]
        summary = []

        for entry in recent:
            summary.append(f"User: {entry['user'][:50]}...")
            summary.append(f"JARVIS: {entry['jarvis'][:50]}...")

        return "\n".join(summary)

    def save_history(self):
        """🗣️ Save conversation history to file"""
        try:
            with open("memory/conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        except:
            pass

    def load_history(self):
        """🗣️ Load conversation history from file"""
        try:
            with open("memory/conversation_history.json", "r", encoding="utf-8") as f:
                self.conversation_history = json.load(f)
        except:
            self.conversation_history = []

    def get_most_common_commands(self, limit=10):
        """🗣️ Get most common commands"""
        command_count = {}

        for entry in self.conversation_history:
            command = entry["user"].lower()
            if command not in command_count:
                command_count[command] = 0
            command_count[command] += 1

        # Sort by frequency
        sorted_commands = sorted(
            command_count.items(), key=lambda x: x[1], reverse=True
        )

        return sorted_commands[:limit]
