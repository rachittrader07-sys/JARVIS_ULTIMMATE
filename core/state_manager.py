"""
🔄 State Manager
Manages JARVIS states and transitions
"""

import time
from datetime import datetime

from colorama import Fore, Style


class StateManager:
    def __init__(self):
        self.current_state = "idle"
        self.previous_state = None
        self.state_history = []
        self.state_start_time = time.time()
        self.state_durations = {}

        # Define valid states
        self.valid_states = [
            "idle",
            "listening",
            "processing",
            "speaking",
            "executing",
            "error",
            "learning",
            "sleep",
            "shutdown",
        ]

        print(Fore.GREEN + "✅ State Manager Initialized" + Style.RESET_ALL)

    def set_state(self, new_state):
        """🔄 Change to a new state"""
        if new_state not in self.valid_states:
            print(Fore.RED + f"❌ Invalid state: {new_state}" + Style.RESET_ALL)
            return False

        # Calculate duration of previous state
        duration = time.time() - self.state_start_time
        if self.current_state in self.state_durations:
            self.state_durations[self.current_state] += duration
        else:
            self.state_durations[self.current_state] = duration

        # Record transition
        transition = {
            "from": self.current_state,
            "to": new_state,
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
        }
        self.state_history.append(transition)

        # Update states
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()

        print(
            Fore.CYAN
            + f"🔄 State: {self.previous_state} → {self.current_state}"
            + Style.RESET_ALL
        )

        # Log state change
        self.log_state_change(transition)

        return True

    def get_state(self):
        """🔄 Get current state"""
        return self.current_state

    def get_previous_state(self):
        """🔄 Get previous state"""
        return self.previous_state

    def get_state_duration(self):
        """🔄 Get current state duration"""
        return time.time() - self.state_start_time

    def get_state_stats(self):
        """🔄 Get state statistics"""
        total_time = sum(self.state_durations.values())
        stats = {}

        for state, duration in self.state_durations.items():
            percentage = (duration / total_time * 100) if total_time > 0 else 0
            stats[state] = {
                "duration": duration,
                "percentage": percentage,
                "transitions": len([h for h in self.state_history if h["to"] == state]),
            }

        return stats

    def is_state(self, state):
        """🔄 Check if in specific state"""
        return self.current_state == state

    def can_transition(self, target_state):
        """🔄 Check if transition to target state is valid"""
        valid_transitions = {
            "idle": ["listening", "sleep", "shutdown"],
            "listening": ["processing", "idle", "error"],
            "processing": ["executing", "speaking", "error"],
            "speaking": ["idle", "listening"],
            "executing": ["idle", "speaking", "error"],
            "error": ["idle", "learning"],
            "learning": ["idle"],
            "sleep": ["idle", "listening"],
            "shutdown": [],
        }

        return target_state in valid_transitions.get(self.current_state, [])

    def force_state(self, new_state):
        """🔄 Force state change (for emergencies)"""
        print(
            Fore.YELLOW
            + f"⚠️ Force state change: {self.current_state} → {new_state}"
            + Style.RESET_ALL
        )
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()
        return True

    def log_state_change(self, transition):
        """🔄 Log state change to file"""
        try:
            import json

            log_file = "memory/state_log.json"
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "transition": transition,
            }

            # Load existing log
            logs = []
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    logs = json.load(f)

            # Add new entry
            logs.append(log_entry)

            # Keep only last 1000 entries
            if len(logs) > 1000:
                logs = logs[-1000:]

            # Save
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(Fore.YELLOW + f"⚠️ State log error: {str(e)}" + Style.RESET_ALL)
