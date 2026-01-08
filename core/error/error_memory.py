"""
📊 Error Memory
Remembers and learns from past errors
"""

import json
import os
from datetime import datetime, timedelta

from colorama import Fore, Style


class ErrorMemory:
    def __init__(self, config):
        self.config = config
        self.error_history = []
        self.error_patterns = []
        self.solutions_database = self.load_solutions_database()
        self.max_history = 1000

        # Load existing error memory
        self.load_memory()

    def load_solutions_database(self):
        """📊 Load common error solutions database"""
        solutions = {
            "microphone_error": {
                "description": "Microphone not working",
                "solutions": [
                    "Check microphone connection",
                    "Adjust microphone privacy settings",
                    "Restart audio services",
                    "Test with another application",
                ],
                "priority": "high",
            },
            "speech_recognition_error": {
                "description": "Speech recognition failed",
                "solutions": [
                    "Check internet connection",
                    "Speak clearly and louder",
                    "Reduce background noise",
                    "Try different speech engine",
                ],
                "priority": "medium",
            },
            "tts_error": {
                "description": "Text-to-speech error",
                "solutions": [
                    "Check speaker connection",
                    "Adjust volume settings",
                    "Restart TTS engine",
                    "Install missing voices",
                ],
                "priority": "medium",
            },
            "import_error": {
                "description": "Module import error",
                "solutions": [
                    "Install missing package: pip install package_name",
                    "Check Python path",
                    "Update Python version",
                    "Reinstall dependencies",
                ],
                "priority": "high",
            },
            "file_not_found": {
                "description": "File not found",
                "solutions": [
                    "Check file path",
                    "Create directory if missing",
                    "Check file permissions",
                    "Verify file exists",
                ],
                "priority": "medium",
            },
            "permission_error": {
                "description": "Permission denied",
                "solutions": [
                    "Run as administrator",
                    "Change file permissions",
                    "Check user account control",
                    "Move to different directory",
                ],
                "priority": "high",
            },
            "network_error": {
                "description": "Network connection error",
                "solutions": [
                    "Check internet connection",
                    "Restart router",
                    "Disable VPN/firewall temporarily",
                    "Check proxy settings",
                ],
                "priority": "high",
            },
            "memory_error": {
                "description": "Memory/Resource error",
                "solutions": [
                    "Close unnecessary applications",
                    "Increase virtual memory",
                    "Restart system",
                    "Check for memory leaks",
                ],
                "priority": "medium",
            },
        }
        return solutions

    def record_error(
        self, error_type, error_message, context, solution=None, success=False
    ):
        """📊 Record an error"""
        error_entry = {
            "id": len(self.error_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message[:500],  # Limit length
            "context": context,
            "solution_applied": solution,
            "success": success,
            "occurrence_count": 1,
            "last_occurrence": datetime.now().isoformat(),
        }

        # Check if similar error already exists
        similar_error = self.find_similar_error(error_type, error_message, context)
        if similar_error:
            # Update existing error
            similar_error["occurrence_count"] += 1
            similar_error["last_occurrence"] = datetime.now().isoformat()
            if solution:
                similar_error["solution_applied"] = solution
            similar_error["success"] = success

            # Update pattern
            self.update_error_pattern(similar_error)
        else:
            # Add new error
            self.error_history.append(error_entry)

            # Keep history limited
            if len(self.error_history) > self.max_history:
                self.error_history = self.error_history[-self.max_history :]

            # Create new pattern
            self.create_error_pattern(error_entry)

        # Auto-save
        if len(self.error_history) % 50 == 0:
            self.save_memory()

        print(
            Fore.YELLOW
            + f"📊 Error recorded: {error_type} in {context}"
            + Style.RESET_ALL
        )

        return error_entry

    def find_similar_error(self, error_type, error_message, context):
        """📊 Find similar error in history"""
        for error in self.error_history:
            # Check type match
            if error["error_type"] == error_type:
                # Check message similarity
                msg_similarity = self.calculate_similarity(
                    error["error_message"], error_message
                )
                # Check context similarity
                ctx_similarity = self.calculate_similarity(error["context"], context)

                if msg_similarity > 0.6 or ctx_similarity > 0.7:
                    return error

        return None

    def calculate_similarity(self, text1, text2):
        """📊 Calculate text similarity (simple version)"""
        if not text1 or not text2:
            return 0.0

        # Convert to lowercase
        t1 = str(text1).lower()
        t2 = str(text2).lower()

        # Split into words
        words1 = set(t1.split())
        words2 = set(t2.split())

        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        if union == 0:
            return 0.0

        return intersection / union

    def create_error_pattern(self, error_entry):
        """📊 Create error pattern from error entry"""
        pattern = {
            "pattern_id": len(self.error_patterns) + 1,
            "error_type": error_entry["error_type"],
            "common_contexts": [error_entry["context"]],
            "common_messages": [error_entry["error_message"]],
            "solutions_tried": [],
            "success_rate": 0.0,
            "occurrence_count": 1,
            "first_seen": error_entry["timestamp"],
            "last_seen": error_entry["timestamp"],
        }

        if error_entry["solution_applied"]:
            pattern["solutions_tried"].append(
                {
                    "solution": error_entry["solution_applied"],
                    "success": error_entry["success"],
                }
            )

        self.error_patterns.append(pattern)

    def update_error_pattern(self, error_entry):
        """📊 Update existing error pattern"""
        for pattern in self.error_patterns:
            if pattern["error_type"] == error_entry["error_type"]:
                # Update pattern
                pattern["occurrence_count"] += 1
                pattern["last_seen"] = error_entry["timestamp"]

                # Add context if new
                if error_entry["context"] not in pattern["common_contexts"]:
                    pattern["common_contexts"].append(error_entry["context"])

                # Add message if new
                if error_entry["error_message"] not in pattern["common_messages"]:
                    pattern["common_messages"].append(error_entry["error_message"])

                # Add solution if exists
                if error_entry["solution_applied"]:
                    solution_exists = False
                    for sol in pattern["solutions_tried"]:
                        if sol["solution"] == error_entry["solution_applied"]:
                            solution_exists = True
                            sol["success"] = error_entry["success"]
                            break

                    if not solution_exists:
                        pattern["solutions_tried"].append(
                            {
                                "solution": error_entry["solution_applied"],
                                "success": error_entry["success"],
                            }
                        )

                # Update success rate
                successful_solutions = sum(
                    1 for sol in pattern["solutions_tried"] if sol["success"]
                )
                total_solutions = len(pattern["solutions_tried"])
                if total_solutions > 0:
                    pattern["success_rate"] = successful_solutions / total_solutions

                break

    def get_suggested_solution(self, error_type, context):
        """📊 Get suggested solution for error"""
        # First check patterns
        for pattern in self.error_patterns:
            if pattern["error_type"] == error_type:
                # Check for successful solutions
                successful_solutions = [
                    sol for sol in pattern["solutions_tried"] if sol["success"]
                ]
                if successful_solutions:
                    # Return most recent successful solution
                    return successful_solutions[-1]["solution"]

        # Check database
        if error_type in self.solutions_database:
            solutions = self.solutions_database[error_type]["solutions"]
            if solutions:
                return solutions[0]  # Return first solution

        # Generic solution
        return "Check logs and try common troubleshooting steps"

    def get_error_stats(self, days=30):
        """📊 Get error statistics"""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        # Filter recent errors
        recent_errors = [e for e in self.error_history if e["timestamp"] >= cutoff_str]

        stats = {
            "total_errors": len(self.error_history),
            "recent_errors": len(recent_errors),
            "error_types": {},
            "success_rate": 0.0,
            "most_common_error": None,
            "patterns_count": len(self.error_patterns),
        }

        # Count by error type
        for error in recent_errors:
            error_type = error["error_type"]
            if error_type not in stats["error_types"]:
                stats["error_types"][error_type] = 0
            stats["error_types"][error_type] += 1

        # Find most common error
        if stats["error_types"]:
            stats["most_common_error"] = max(
                stats["error_types"].items(), key=lambda x: x[1]
            )[0]

        # Calculate success rate
        successful_errors = sum(1 for e in recent_errors if e.get("success", False))
        if recent_errors:
            stats["success_rate"] = successful_errors / len(recent_errors)

        return stats

    def cleanup_old_errors(self, days=90):
        """📊 Cleanup errors older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()

        old_count = len(self.error_history)

        # Filter recent errors
        self.error_history = [
            e for e in self.error_history if e["timestamp"] >= cutoff_str
        ]

        removed = old_count - len(self.error_history)

        # Also cleanup patterns with no recent occurrences
        self.error_patterns = [
            p for p in self.error_patterns if p["last_seen"] >= cutoff_str
        ]

        print(Fore.YELLOW + f"📊 Cleaned up {removed} old errors" + Style.RESET_ALL)

        return removed

    def save_memory(self):
        """📊 Save error memory to file"""
        try:
            memory_data = {
                "error_history": self.error_history[-500:],  # Save recent
                "error_patterns": self.error_patterns,
                "solutions_database": self.solutions_database,
                "saved_at": datetime.now().isoformat(),
            }

            with open(self.config["paths"]["error_log"], "w", encoding="utf-8") as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)

            print(
                Fore.GREEN
                + f"📊 Error memory saved: {len(self.error_history)} errors"
                + Style.RESET_ALL
            )

        except Exception as e:
            print(
                Fore.YELLOW + f"⚠️ Error memory save error: {str(e)}" + Style.RESET_ALL
            )

    def load_memory(self):
        """📊 Load error memory from file"""
        try:
            if os.path.exists(self.config["paths"]["error_log"]):
                with open(
                    self.config["paths"]["error_log"], "r", encoding="utf-8"
                ) as f:
                    memory_data = json.load(f)

                    self.error_history = memory_data.get("error_history", [])
                    self.error_patterns = memory_data.get("error_patterns", [])
                    self.solutions_database = memory_data.get(
                        "solutions_database", self.solutions_database
                    )

                print(
                    Fore.GREEN
                    + f"📊 Error memory loaded: {len(self.error_history)} errors"
                    + Style.RESET_ALL
                )

        except Exception as e:
            print(
                Fore.YELLOW + f"⚠️ Error memory load error: {str(e)}" + Style.RESET_ALL
            )

    def get_learning_insights(self):
        """📊 Get learning insights from error patterns"""
        insights = []

        for pattern in self.error_patterns:
            if pattern["occurrence_count"] > 3:
                insight = {
                    "pattern": pattern["error_type"],
                    "frequency": pattern["occurrence_count"],
                    "common_context": (
                        pattern["common_contexts"][0]
                        if pattern["common_contexts"]
                        else "unknown"
                    ),
                    "best_solution": None,
                    "confidence": pattern["success_rate"],
                }

                # Find best solution
                successful_solutions = [
                    sol for sol in pattern["solutions_tried"] if sol["success"]
                ]
                if successful_solutions:
                    insight["best_solution"] = successful_solutions[-1]["solution"]

                insights.append(insight)

        return insights

    def export_errors_report(self, filepath="error_report.json"):
        """📊 Export errors report"""
        try:
            report = {
                "summary": self.get_error_stats(),
                "recent_errors": self.error_history[-100:],
                "patterns": self.error_patterns,
                "insights": self.get_learning_insights(),
                "generated_at": datetime.now().isoformat(),
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(
                Fore.GREEN + f"📊 Error report exported: {filepath}" + Style.RESET_ALL
            )
            return True

        except Exception as e:
            print(
                Fore.RED + f"❌ Error report export failed: {str(e)}" + Style.RESET_ALL
            )
            return False
