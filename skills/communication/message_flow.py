"""
💬 Message Flow Manager
Manages conversation flow and message history
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from colorama import Fore, Style


class MessageFlow:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.history_file = os.path.join("data", "message_history.json")
        self.conversations = self.load_conversations()
        self.current_conversation_id = None

    def execute(self, params):
        """💬 Execute message flow command"""
        action = params.get("action", "add")
        conversation_id = params.get("conversation_id", self.current_conversation_id)
        message = params.get("message", "")
        sender = params.get("sender", "user")
        receiver = params.get("receiver", "jarvis")

        print(Fore.YELLOW + f"💬 Message flow: {action}" + Style.RESET_ALL)

        action_map = {
            "add": self.add_message,
            "get": self.get_conversation,
            "create": self.create_conversation,
            "switch": self.switch_conversation,
            "list": self.list_conversations,
            "search": self.search_messages,
            "clear": self.clear_conversation,
            "export": self.export_conversation,
            "summary": self.get_summary,
        }

        if action in action_map:
            return action_map[action](
                conversation_id=conversation_id,
                message=message,
                sender=sender,
                receiver=receiver,
                params=params,
            )
        else:
            self.tts.speak("Sir, that message flow action is not available.")
            return {
                "success": False,
                "error": f"Unknown action: {action}",
                "available_actions": list(action_map.keys()),
            }

    def load_conversations(self):
        """💬 Load conversations from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("conversations", {})
            else:
                # Create default structure
                default_data = {
                    "conversations": {},
                    "settings": {
                        "auto_save": True,
                        "max_history": 1000,
                        "backup_enabled": True,
                    },
                    "metadata": {
                        "created_at": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat(),
                    },
                }

                # Create data directory if it doesn't exist
                os.makedirs("data", exist_ok=True)

                with open(self.history_file, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=2)

                return {}

        except Exception as e:
            print(Fore.RED + f"Error loading conversations: {e}" + Style.RESET_ALL)
            return {}

    def save_conversations(self):
        """💬 Save conversations to JSON file"""
        try:
            data = {
                "conversations": self.conversations,
                "settings": {
                    "auto_save": True,
                    "max_history": 1000,
                    "backup_enabled": True,
                },
                "metadata": {"last_updated": datetime.now().isoformat()},
            }

            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(Fore.RED + f"Error saving conversations: {e}" + Style.RESET_ALL)
            return False

    def create_conversation(self, conversation_id=None, **kwargs):
        """💬 Create a new conversation"""
        try:
            params = kwargs.get("params", {})
            title = params.get("title", f"Conversation {len(self.conversations) + 1}")
            tags = params.get("tags", [])

            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())[:8]

            # Check if conversation already exists
            if conversation_id in self.conversations:
                self.tts.speak("Sir, a conversation with that ID already exists.")
                return {
                    "success": False,
                    "error": "Conversation already exists",
                    "conversation_id": conversation_id,
                }

            # Create new conversation
            new_conversation = {
                "id": conversation_id,
                "title": title,
                "tags": tags,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "messages": [],
                "participants": ["user", "jarvis"],
                "settings": {
                    "auto_scroll": True,
                    "notifications": True,
                    "archived": False,
                },
            }

            # Add to conversations
            self.conversations[conversation_id] = new_conversation

            # Set as current conversation
            self.current_conversation_id = conversation_id

            # Save to file
            if self.save_conversations():
                self.tts.speak(f"Created new conversation: {title}")
                return {
                    "success": True,
                    "action": "create",
                    "conversation_id": conversation_id,
                    "title": title,
                    "conversation": new_conversation,
                }
            else:
                self.tts.speak("Failed to create conversation.")
                return {"success": False, "error": "Failed to save conversation"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_message(
        self,
        conversation_id=None,
        message="",
        sender="user",
        receiver="jarvis",
        **kwargs,
    ):
        """💬 Add a message to conversation"""
        try:
            # Use current conversation if none specified
            if not conversation_id:
                if not self.current_conversation_id:
                    # Create a new conversation if none exists
                    result = self.create_conversation()
                    if not result["success"]:
                        return result
                    conversation_id = result["conversation_id"]
                else:
                    conversation_id = self.current_conversation_id

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {
                    "success": False,
                    "error": "Conversation not found",
                    "conversation_id": conversation_id,
                }

            # Create message object
            message_id = str(uuid.uuid4())[:8]
            message_obj = {
                "id": message_id,
                "text": message,
                "sender": sender,
                "receiver": receiver,
                "timestamp": datetime.now().isoformat(),
                "read": False,
                "type": "text",
                "metadata": {"length": len(message), "words": len(message.split())},
            }

            # Add message to conversation
            conversation = self.conversations[conversation_id]
            conversation["messages"].append(message_obj)
            conversation["updated_at"] = datetime.now().isoformat()

            # Limit message history
            max_history = self.config.get("max_message_history", 100)
            if len(conversation["messages"]) > max_history:
                conversation["messages"] = conversation["messages"][-max_history:]

            # Save to file
            if self.save_conversations():
                return {
                    "success": True,
                    "action": "add",
                    "conversation_id": conversation_id,
                    "message_id": message_id,
                    "message": message_obj,
                }
            else:
                return {"success": False, "error": "Failed to save message"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_conversation(self, conversation_id=None, **kwargs):
        """💬 Get conversation messages"""
        try:
            params = kwargs.get("params", {})
            limit = params.get("limit", 50)
            offset = params.get("offset", 0)

            # Use current conversation if none specified
            if not conversation_id:
                if not self.current_conversation_id:
                    self.tts.speak("Sir, no active conversation. Let me create one.")
                    result = self.create_conversation()
                    if not result["success"]:
                        return result
                    conversation_id = result["conversation_id"]
                else:
                    conversation_id = self.current_conversation_id

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {
                    "success": False,
                    "error": "Conversation not found",
                    "conversation_id": conversation_id,
                }

            conversation = self.conversations[conversation_id]
            messages = conversation.get("messages", [])

            # Apply limit and offset
            paginated_messages = messages[offset : offset + limit]

            # Mark messages as read
            for msg in paginated_messages:
                if msg["sender"] != "user":
                    msg["read"] = True

            self.tts.speak(
                f"Retrieved {len(paginated_messages)} messages from conversation."
            )

            return {
                "success": True,
                "action": "get",
                "conversation_id": conversation_id,
                "title": conversation["title"],
                "total_messages": len(messages),
                "messages": paginated_messages,
                "conversation": conversation,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def switch_conversation(self, conversation_id=None, **kwargs):
        """💬 Switch to a different conversation"""
        try:
            if not conversation_id:
                self.tts.speak("Sir, which conversation should I switch to?")
                return {"success": False, "error": "No conversation ID provided"}

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {
                    "success": False,
                    "error": "Conversation not found",
                    "conversation_id": conversation_id,
                }

            # Switch conversation
            old_conversation_id = self.current_conversation_id
            self.current_conversation_id = conversation_id

            conversation = self.conversations[conversation_id]

            self.tts.speak(f"Switched to conversation: {conversation['title']}")

            return {
                "success": True,
                "action": "switch",
                "old_conversation_id": old_conversation_id,
                "new_conversation_id": conversation_id,
                "title": conversation["title"],
                "message_count": len(conversation.get("messages", [])),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_conversations(self, **kwargs):
        """💬 List all conversations"""
        try:
            params = kwargs.get("params", {})
            filter_archived = params.get("filter_archived", False)
            sort_by = params.get("sort_by", "updated")
            limit = params.get("limit", 20)

            conversations_list = []

            for conv_id, conversation in self.conversations.items():
                # Filter archived conversations if requested
                if filter_archived and conversation.get("settings", {}).get(
                    "archived", False
                ):
                    continue

                conversations_list.append(
                    {
                        "id": conv_id,
                        "title": conversation["title"],
                        "message_count": len(conversation.get("messages", [])),
                        "created_at": conversation["created_at"],
                        "updated_at": conversation["updated_at"],
                        "tags": conversation.get("tags", []),
                        "archived": conversation.get("settings", {}).get(
                            "archived", False
                        ),
                        "is_current": conv_id == self.current_conversation_id,
                    }
                )

            # Sort conversations
            if sort_by == "updated":
                conversations_list.sort(key=lambda x: x["updated_at"], reverse=True)
            elif sort_by == "created":
                conversations_list.sort(key=lambda x: x["created_at"], reverse=True)
            elif sort_by == "title":
                conversations_list.sort(key=lambda x: x["title"].lower())
            elif sort_by == "messages":
                conversations_list.sort(key=lambda x: x["message_count"], reverse=True)

            total = len(conversations_list)
            active = len([c for c in conversations_list if not c["archived"]])

            if total == 0:
                self.tts.speak("You have no conversations saved.")
            else:
                self.tts.speak(f"You have {total} conversations, {active} active.")

            return {
                "success": True,
                "action": "list",
                "total": total,
                "active": active,
                "current_conversation_id": self.current_conversation_id,
                "conversations": conversations_list[:limit],
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_messages(self, **kwargs):
        """💬 Search messages across conversations"""
        try:
            params = kwargs.get("params", {})
            query = params.get("query", "")
            conversation_id = params.get("conversation_id")
            sender = params.get("sender")
            limit = params.get("limit", 20)

            if not query:
                self.tts.speak("Sir, what should I search for?")
                return {"success": False, "error": "No search query provided"}

            query_lower = query.lower()
            results = []

            # Search in specified conversation or all conversations
            if conversation_id:
                if conversation_id in self.conversations:
                    conversations_to_search = [
                        (conversation_id, self.conversations[conversation_id])
                    ]
                else:
                    self.tts.speak("Sir, that conversation doesn't exist.")
                    return {"success": False, "error": "Conversation not found"}
            else:
                conversations_to_search = self.conversations.items()

            # Search through messages
            for conv_id, conversation in conversations_to_search:
                for message in conversation.get("messages", []):
                    # Apply sender filter if specified
                    if sender and message["sender"].lower() != sender.lower():
                        continue

                    # Search in message text
                    if query_lower in message["text"].lower():
                        results.append(
                            {
                                "conversation_id": conv_id,
                                "conversation_title": conversation["title"],
                                "message": message,
                                "relevance": self.calculate_relevance(
                                    message["text"], query
                                ),
                            }
                        )

            # Sort by relevance
            results.sort(key=lambda x: x["relevance"], reverse=True)

            if results:
                self.tts.speak(f"Found {len(results)} messages matching '{query}'.")
            else:
                self.tts.speak(f"No messages found matching '{query}'.")

            return {
                "success": True,
                "action": "search",
                "query": query,
                "total_results": len(results),
                "results": results[:limit],
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def clear_conversation(self, conversation_id=None, **kwargs):
        """💬 Clear messages from a conversation"""
        try:
            # Use current conversation if none specified
            if not conversation_id:
                if not self.current_conversation_id:
                    self.tts.speak("Sir, no active conversation to clear.")
                    return {"success": False, "error": "No conversation selected"}
                conversation_id = self.current_conversation_id

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {"success": False, "error": "Conversation not found"}

            # Clear messages
            conversation = self.conversations[conversation_id]
            message_count = len(conversation.get("messages", []))
            conversation["messages"] = []
            conversation["updated_at"] = datetime.now().isoformat()

            # Save to file
            if self.save_conversations():
                self.tts.speak(f"Cleared {message_count} messages from conversation.")
                return {
                    "success": True,
                    "action": "clear",
                    "conversation_id": conversation_id,
                    "cleared_count": message_count,
                }
            else:
                self.tts.speak("Failed to clear conversation.")
                return {"success": False, "error": "Failed to save after clearing"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def export_conversation(self, conversation_id=None, **kwargs):
        """💬 Export conversation to file"""
        try:
            params = kwargs.get("params", {})
            format_type = params.get("format", "json")
            include_metadata = params.get("include_metadata", True)

            # Use current conversation if none specified
            if not conversation_id:
                if not self.current_conversation_id:
                    self.tts.speak("Sir, no active conversation to export.")
                    return {"success": False, "error": "No conversation selected"}
                conversation_id = self.current_conversation_id

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {"success": False, "error": "Conversation not found"}

            conversation = self.conversations[conversation_id]

            # Create export directory
            export_dir = os.path.join("exports", "conversations")
            os.makedirs(export_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{conversation_id}_{timestamp}"

            if format_type == "json":
                filepath = os.path.join(export_dir, f"{filename}.json")
                with open(filepath, "w", encoding="utf-8") as f:
                    export_data = {"conversation": conversation}
                    if include_metadata:
                        export_data["export_metadata"] = {
                            "exported_at": datetime.now().isoformat(),
                            "format": "json",
                            "version": "1.0",
                        }
                    json.dump(export_data, f, indent=2, ensure_ascii=False)

            elif format_type == "txt":
                filepath = os.path.join(export_dir, f"{filename}.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"Conversation: {conversation['title']}\n")
                    f.write(f"ID: {conversation_id}\n")
                    f.write(f"Created: {conversation['created_at']}\n")
                    f.write(f"Updated: {conversation['updated_at']}\n")
                    f.write("=" * 50 + "\n\n")

                    for message in conversation.get("messages", []):
                        timestamp = datetime.fromisoformat(
                            message["timestamp"]
                        ).strftime("%Y-%m-%d %H:%M:%S")
                        f.write(
                            f"[{timestamp}] {message['sender']}: {message['text']}\n"
                        )

            else:
                self.tts.speak(f"Sir, {format_type} format is not supported.")
                return {"success": False, "error": f"Unsupported format: {format_type}"}

            self.tts.speak(f"Exported conversation to {filepath}")

            return {
                "success": True,
                "action": "export",
                "conversation_id": conversation_id,
                "format": format_type,
                "filepath": filepath,
                "size": os.path.getsize(filepath),
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_summary(self, conversation_id=None, **kwargs):
        """💬 Get conversation summary"""
        try:
            # Use current conversation if none specified
            if not conversation_id:
                if not self.current_conversation_id:
                    self.tts.speak("Sir, no active conversation to summarize.")
                    return {"success": False, "error": "No conversation selected"}
                conversation_id = self.current_conversation_id

            # Check if conversation exists
            if conversation_id not in self.conversations:
                self.tts.speak("Sir, that conversation doesn't exist.")
                return {"success": False, "error": "Conversation not found"}

            conversation = self.conversations[conversation_id]
            messages = conversation.get("messages", [])

            if not messages:
                self.tts.speak("This conversation has no messages.")
                return {
                    "success": True,
                    "action": "summary",
                    "conversation_id": conversation_id,
                    "message_count": 0,
                    "summary": "No messages",
                }

            # Calculate statistics
            user_messages = [m for m in messages if m["sender"] == "user"]
            jarvis_messages = [m for m in messages if m["sender"] == "jarvis"]

            total_words = sum(len(m["text"].split()) for m in messages)
            avg_words = total_words / len(messages) if messages else 0

            # Get time range
            if messages:
                first_time = datetime.fromisoformat(messages[0]["timestamp"])
                last_time = datetime.fromisoformat(messages[-1]["timestamp"])
                duration = last_time - first_time
            else:
                duration = None

            summary = {
                "title": conversation["title"],
                "total_messages": len(messages),
                "user_messages": len(user_messages),
                "jarvis_messages": len(jarvis_messages),
                "total_words": total_words,
                "average_words_per_message": round(avg_words, 1),
                "duration": str(duration) if duration else "N/A",
                "created_at": conversation["created_at"],
                "updated_at": conversation["updated_at"],
            }

            # Generate summary text
            summary_text = (
                f"Conversation '{conversation['title']}' has {len(messages)} messages "
            )
            summary_text += (
                f"({len(user_messages)} from you, {len(jarvis_messages)} from me). "
            )
            summary_text += f"Average message length: {round(avg_words, 1)} words."

            self.tts.speak(summary_text)

            return {
                "success": True,
                "action": "summary",
                "conversation_id": conversation_id,
                "summary": summary,
                "summary_text": summary_text,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_relevance(text, query):
        """💬 Calculate search relevance score"""
        text_lower = text.lower()
        query_lower = query.lower()

        # Simple relevance calculation
        if text_lower == query_lower:
            return 1.0
        elif query_lower in text_lower:
            # Longer matches are better
            return len(query_lower) / len(text_lower)
        else:
            # Partial match score
            words = query_lower.split()
            matches = sum(1 for word in words if word in text_lower)
            return matches / len(words) if words else 0

    def archive_conversation(self, conversation_id, archive=True):
        """💬 Archive or unarchive a conversation"""
        try:
            if conversation_id not in self.conversations:
                return {"success": False, "error": "Conversation not found"}

            conversation = self.conversations[conversation_id]
            conversation["settings"]["archived"] = archive

            if self.save_conversations():
                action = "archived" if archive else "unarchived"
                self.tts.speak(f"Conversation {action}.")
                return {
                    "success": True,
                    "action": "archive" if archive else "unarchive",
                    "conversation_id": conversation_id,
                    "archived": archive,
                }
            else:
                return {"success": False, "error": "Failed to save conversation"}

        except Exception as e:
            return {"success": False, "error": str(e)}
