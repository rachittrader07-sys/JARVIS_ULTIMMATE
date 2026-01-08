"""
🧠 Memory Controller
Manages short-term and long-term memory
"""

import json
import os
from datetime import datetime, timedelta

from colorama import Fore, Style


class MemoryController:
    def __init__(self, config):
        self.config = config
        self.short_term_memory = []
        self.long_term_memory = []
        self.max_short_term = config["jarvis"]["memory"]["short_term_size"]

        # Load existing memory
        self.load_memory()

    def add_short_term(self, entry):
        """🧠 Add entry to short-term memory"""
        entry["timestamp"] = datetime.now().isoformat()
        entry["id"] = len(self.short_term_memory) + 1

        self.short_term_memory.append(entry)

        # Keep within limit
        if len(self.short_term_memory) > self.max_short_term:
            self.short_term_memory = self.short_term_memory[-self.max_short_term :]

        # Auto-save
        self.save_short_term()

        print(
            Fore.GREEN
            + f"🧠 Memory updated: {entry.get('action', 'unknown')}"
            + Style.RESET_ALL
        )

    def add_long_term(self, entry):
        """🧠 Add entry to long-term memory"""
        entry["timestamp"] = datetime.now().isoformat()
        entry["id"] = len(self.long_term_memory) + 1
        entry["importance"] = entry.get("importance", 1)

        self.long_term_memory.append(entry)
        self.save_long_term()

    def get_recent(self, count=5):
        """🧠 Get recent memories"""
        return self.short_term_memory[-count:] if self.short_term_memory else []

    def search_memory(self, query, memory_type="both"):
        """🧠 Search in memory"""
        results = []
        query = query.lower()

        if memory_type in ["short", "both"]:
            for entry in self.short_term_memory:
                if self._matches_query(entry, query):
                    results.append(entry)

        if memory_type in ["long", "both"]:
            for entry in self.long_term_memory:
                if self._matches_query(entry, query):
                    results.append(entry)

        return results

    def _matches_query(self, entry, query):
        """🧠 Check if entry matches query"""
        # Check in action
        if "action" in entry and query in str(entry["action"]).lower():
            return True

        # Check in details
        if "details" in entry:
            details_str = json.dumps(entry["details"]).lower()
            if query in details_str:
                return True

        # Check in text
        if "text" in entry and query in str(entry["text"]).lower():
            return True

        return False

    def remember_pattern(self, pattern_data):
        """🧠 Remember a pattern for learning"""
        pattern_entry = {
            "type": "pattern",
            "pattern": pattern_data,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.5,
            "usage_count": 1,
        }

        # Check if similar pattern exists
        similar = self.find_similar_pattern(pattern_data)
        if similar:
            # Update existing pattern
            similar["usage_count"] += 1
            similar["confidence"] = min(1.0, similar["confidence"] + 0.1)
        else:
            # Add new pattern
            self.long_term_memory.append(pattern_entry)

        self.save_long_term()

    def find_similar_pattern(self, pattern_data):
        """🧠 Find similar pattern in memory"""
        for entry in self.long_term_memory:
            if entry.get("type") == "pattern":
                # Simple similarity check
                if self._patterns_similar(entry["pattern"], pattern_data):
                    return entry
        return None

    def _patterns_similar(self, pattern1, pattern2):
        """🧠 Check if two patterns are similar"""
        # This is a simplified version
        # In production, use more sophisticated similarity checking
        str1 = json.dumps(pattern1).lower()
        str2 = json.dumps(pattern2).lower()

        # Simple word overlap
        words1 = set(str1.split())
        words2 = set(str2.split())
        overlap = len(words1.intersection(words2))

        return overlap > 2

    def load_memory(self):
        """🧠 Load memory from files"""
        try:
            # Load short term
            short_term_file = self.config["paths"]["memory_short"]
            if os.path.exists(short_term_file):
                with open(short_term_file, "r", encoding="utf-8") as f:
                    self.short_term_memory = json.load(f)

            # Load long term
            long_term_file = self.config["paths"]["memory_long"]
            if os.path.exists(long_term_file):
                with open(long_term_file, "r", encoding="utf-8") as f:
                    self.long_term_memory = json.load(f)

            print(
                Fore.GREEN
                + f"🧠 Memory loaded: {len(self.short_term_memory)} short, {len(self.long_term_memory)} long"
                + Style.RESET_ALL
            )

        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Memory load error: {str(e)}" + Style.RESET_ALL)
            self.short_term_memory = []
            self.long_term_memory = []

    def save_short_term(self):
        """🧠 Save short-term memory"""
        try:
            with open(self.config["paths"]["memory_short"], "w", encoding="utf-8") as f:
                json.dump(self.short_term_memory, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False

    def save_long_term(self):
        """🧠 Save long-term memory"""
        try:
            with open(self.config["paths"]["memory_long"], "w", encoding="utf-8") as f:
                json.dump(self.long_term_memory, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False

    def cleanup_old_memory(self, days=30):
        """🧠 Cleanup old memories"""
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.isoformat()

        # Clean short term (keep all for now)
        # Clean long term
        new_long_term = []
        for entry in self.long_term_memory:
            if "timestamp" in entry:
                if entry["timestamp"] >= cutoff_str or entry.get("importance", 0) > 5:
                    new_long_term.append(entry)

        self.long_term_memory = new_long_term
        self.save_long_term()

        return len(self.long_term_memory) - len(new_long_term)

    def get_memory_stats(self):
        """🧠 Get memory statistics"""
        stats = {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "patterns_count": len(
                [m for m in self.long_term_memory if m.get("type") == "pattern"]
            ),
            "last_updated": datetime.now().isoformat(),
        }

        # Count by action type
        action_counts = {}
        for entry in self.short_term_memory:
            action = entry.get("action", "unknown")
            if action not in action_counts:
                action_counts[action] = 0
            action_counts[action] += 1

        stats["action_counts"] = action_counts

        return stats
