"""
🗣️ Context Tracker
Tracks and maintains conversation context
"""

import json
import re
from datetime import datetime, timedelta
from colorama import Fore, Style

class ContextTracker:
    def __init__(self, config):
        self.config = config
        self.current_context = {}
        self.context_history = []
        self.max_history = 20
        self.entity_context = {}
        self.topic_stack = []
        self.follow_up_expected = False
        self.follow_up_type = None
        self.follow_up_data = {}
        
        # Context patterns for different intents
        self.context_patterns = self.load_context_patterns()
        
        print(Fore.GREEN + "✅ Context Tracker Initialized" + Style.RESET_ALL)
    
    def load_context_patterns(self):
        """🗣️ Load context recognition patterns"""
        patterns = {
            "youtube": {
                "keywords": ["youtube", "video", "play", "search", "watch"],
                "follow_up": ["search", "play", "next", "previous", "pause", "stop"],
                "entities": ["video", "channel", "playlist"]
            },
            "whatsapp": {
                "keywords": ["whatsapp", "message", "send", "contact", "chat"],
                "follow_up": ["message", "send", "reply", "forward", "delete"],
                "entities": ["person", "group", "message"]
            },
            "web_search": {
                "keywords": ["search", "google", "find", "look up", "browse"],
                "follow_up": ["open", "read", "next", "previous", "save"],
                "entities": ["query", "website", "result"]
            },
            "system": {
                "keywords": ["system", "battery", "cpu", "ram", "disk", "memory"],
                "follow_up": ["check", "monitor", "status", "details"],
                "entities": ["component", "metric", "status"]
            },
            "apps": {
                "keywords": ["open", "close", "start", "launch", "run"],
                "follow_up": ["minimize", "maximize", "switch", "focus"],
                "entities": ["app", "window", "process"]
            },
            "coding": {
                "keywords": ["code", "program", "python", "write", "debug"],
                "follow_up": ["run", "test", "save", "explain", "fix"],
                "entities": ["language", "file", "error", "function"]
            }
        }
        return patterns
    
    def update_context(self, user_input, assistant_response, intent=None, entities=None):
        """🗣️ Update context with new interaction"""
        try:
            # Create context entry
            context_entry = {
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input[:200],  # Limit length
                'assistant_response': assistant_response[:200],
                'intent': intent,
                'entities': entities or {},
                'topic': self.detect_topic(user_input),
                'requires_followup': self.check_followup(user_input)
            }
            
            # Add to history
            self.context_history.append(context_entry)
            
            # Keep history limited
            if len(self.context_history) > self.max_history:
                self.context_history = self.context_history[-self.max_history:]
            
            # Update current context
            self.current_context = context_entry.copy()
            
            # Extract and store entities for reference
            self.update_entity_context(entities, user_input)
            
            # Update topic stack
            self.update_topic_stack(context_entry['topic'])
            
            # Check for follow-up expectations
            self.update_followup_expectation(user_input, intent)
            
            print(Fore.CYAN + f"🗣️ Context updated: {context_entry['topic']}" + Style.RESET_ALL)
            
            # Auto-save periodically
            if len(self.context_history) % 10 == 0:
                self.save_context()
                
            return context_entry
            
        except Exception as e:
            print(Fore.RED + f"❌ Context update error: {str(e)}" + Style.RESET_ALL)
            return None
    
    def detect_topic(self, user_input):
        """🗣️ Detect topic from user input"""
        input_lower = user_input.lower()
        
        for topic, pattern in self.context_patterns.items():
            for keyword in pattern['keywords']:
                if keyword in input_lower:
                    return topic
        
        # Check for common topics
        if any(word in input_lower for word in ['youtube', 'video', 'watch']):
            return 'youtube'
        elif any(word in input_lower for word in ['whatsapp', 'message', 'send']):
            return 'whatsapp'
        elif any(word in input_lower for word in ['search', 'google', 'find']):
            return 'web_search'
        elif any(word in input_lower for word in ['system', 'battery', 'cpu', 'ram']):
            return 'system'
        elif any(word in input_lower for word in ['open', 'close', 'app', 'application']):
            return 'apps'
        elif any(word in input_lower for word in ['code', 'program', 'python', 'write']):
            return 'coding'
        
        return 'general'
    
    def update_entity_context(self, entities, user_input):
        """🗣️ Update entity context for reference"""
        if not entities:
            return
        
        # Store entities with timestamp
        for entity_type, entity_values in entities.items():
            if entity_values:
                if entity_type not in self.entity_context:
                    self.entity_context[entity_type] = []
                
                # Add new entities
                for value in entity_values:
                    if isinstance(value, str) and value.strip():
                        entity_entry = {
                            'value': value,
                            'type': entity_type,
                            'timestamp': datetime.now().isoformat(),
                            'source': user_input[:50]
                        }
                        
                        # Check if already exists
                        exists = False
                        for existing in self.entity_context[entity_type]:
                            if existing['value'] == value:
                                exists = True
                                existing['timestamp'] = datetime.now().isoformat()
                                break
                        
                        if not exists:
                            self.entity_context[entity_type].append(entity_entry)
        
        # Clean old entities (older than 1 hour)
        self.clean_old_entities()
    
    def clean_old_entities(self, hours=1):
        """🗣️ Clean entities older than specified hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        cutoff_str = cutoff.isoformat()
        
        for entity_type in list(self.entity_context.keys()):
            new_entities = []
            for entity in self.entity_context[entity_type]:
                if entity['timestamp'] >= cutoff_str:
                    new_entities.append(entity)
            
            if new_entities:
                self.entity_context[entity_type] = new_entities
            else:
                del self.entity_context[entity_type]
    
    def update_topic_stack(self, new_topic):
        """🗣️ Update topic stack"""
        if not self.topic_stack or self.topic_stack[-1] != new_topic:
            self.topic_stack.append(new_topic)
            
            # Keep stack limited
            if len(self.topic_stack) > 10:
                self.topic_stack = self.topic_stack[-10:]
    
    def update_followup_expectation(self, user_input, intent):
        """🗣️ Update follow-up expectation"""
        input_lower = user_input.lower()
        
        # Check if current input expects follow-up
        if intent in ['send_whatsapp', 'search_web', 'open_app', 'open_website']:
            # Check if all required information is present
            if intent == 'send_whatsapp':
                if 'message' not in input_lower or 'to' not in input_lower:
                    self.follow_up_expected = True
                    self.follow_up_type = 'whatsapp_details'
                    self.follow_up_data = {'intent': intent}
            elif intent == 'search_web':
                if 'search' in input_lower and len(input_lower.split()) < 3:
                    self.follow_up_expected = True
                    self.follow_up_type = 'search_query'
            elif intent in ['open_app', 'open_website']:
                if 'open' in input_lower and len(input_lower.split()) < 3:
                    self.follow_up_expected = True
                    self.follow_up_type = 'open_target'
        else:
            # Check based on patterns
            patterns = [
                ('what should I', 'general_advice'),
                ('how do I', 'instructions'),
                ('can you', 'confirmation'),
                ('please', 'politeness')
            ]
            
            for pattern, f_type in patterns:
                if pattern in input_lower:
                    self.follow_up_expected = True
                    self.follow_up_type = f_type
                    break
    
    def check_followup(self, user_input):
        """🗣️ Check if user input is a follow-up"""
        if not self.context_history:
            return False
        
        # Check for follow-up indicators
        followup_indicators = [
            'it', 'that', 'this', 'there',
            'next', 'then', 'also', 'too',
            'again', 'more', 'another',
            'us', 'usko', 'isko', 'wahan'
        ]
        
        input_words = user_input.lower().split()
        
        # Check for pronouns/pointers
        for indicator in followup_indicators:
            if indicator in input_words:
                return True
        
        # Check if input is short and previous context exists
        if len(input_words) < 3 and self.context_history:
            last_context = self.context_history[-1]
            if last_context.get('requires_followup'):
                return True
        
        return False
    
    def get_context_for_intent(self, intent):
        """🗣️ Get relevant context for specific intent"""
        relevant_context = {
            'current_topic': self.get_current_topic(),
            'recent_entities': self.get_recent_entities(),
            'conversation_flow': self.get_conversation_flow(),
            'follow_up_expected': self.follow_up_expected,
            'follow_up_type': self.follow_up_type
        }
        
        # Add intent-specific context
        if intent in ['send_whatsapp', 'whatsapp_message']:
            relevant_context['last_contact'] = self.get_last_entity('person')
            relevant_context['last_message'] = self.get_last_interaction_with('whatsapp')
        
        elif intent in ['open_website', 'search_web']:
            relevant_context['last_search'] = self.get_last_entity('query')
            relevant_context['last_website'] = self.get_last_entity('website')
        
        elif intent in ['open_app', 'close_app']:
            relevant_context['last_app'] = self.get_last_entity('app')
            relevant_context['recent_apps'] = self.get_entities_by_type('app')
        
        elif intent == 'system_info':
            relevant_context['last_check'] = self.get_last_interaction_with('system')
            relevant_context['system_metrics'] = self.get_system_context()
        
        return relevant_context
    
    def get_current_topic(self):
        """🗣️ Get current topic"""
        if self.topic_stack:
            return self.topic_stack[-1]
        return 'general'
    
    def get_recent_entities(self, entity_type=None, limit=5):
        """🗣️ Get recent entities"""
        if entity_type:
            if entity_type in self.entity_context:
                return self.entity_context[entity_type][-limit:]
            return []
        
        # Get all recent entities
        all_entities = []
        for entities in self.entity_context.values():
            all_entities.extend(entities[-limit:])
        
        # Sort by timestamp
        all_entities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_entities[:limit]
    
    def get_last_entity(self, entity_type):
        """🗣️ Get last entity of specific type"""
        if entity_type in self.entity_context and self.entity_context[entity_type]:
            return self.entity_context[entity_type][-1]
        return None
    
    def get_entities_by_type(self, entity_type):
        """🗣️ Get all entities of specific type"""
        if entity_type in self.entity_context:
            return self.entity_context[entity_type]
        return []
    
    def get_last_interaction_with(self, topic):
        """🗣️ Get last interaction with specific topic"""
        for context in reversed(self.context_history):
            if context.get('topic') == topic:
                return context
        return None
    
    def get_system_context(self):
        """🗣️ Get system-related context"""
        system_context = []
        
        for context in self.context_history[-10:]:
            if context.get('topic') == 'system':
                system_context.append({
                    'time': context['timestamp'],
                    'query': context['user_input'],
                    'response': context['assistant_response']
                })
        
        return system_context
    
    def get_conversation_flow(self):
        """🗣️ Get conversation flow"""
        flow = []
        
        for context in self.context_history[-5:]:
            flow.append({
                'user': context['user_input'][:30] + '...',
                'assistant': context['assistant_response'][:30] + '...',
                'topic': context['topic']
            })
        
        return flow
    
    def clear_context(self):
        """🗣️ Clear all context"""
        self.current_context = {}
        self.context_history = []
        self.entity_context = {}
        self.topic_stack = []
        self.follow_up_expected = False
        self.follow_up_type = None
        self.follow_up_data = {}
        
        print(Fore.YELLOW + "🗣️ Context cleared" + Style.RESET_ALL)
    
    def save_context(self):
        """🗣️ Save context to file"""
        try:
            context_data = {
                'current_context': self.current_context,
                'topic_stack': self.topic_stack,
                'entity_context': self.entity_context,
                'saved_at': datetime.now().isoformat()
            }
            
            with open('memory/context_data.json', 'w', encoding='utf-8') as f:
                json.dump(context_data, f, indent=2, ensure_ascii=False)
                
            return True
            
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Context save error: {str(e)}" + Style.RESET_ALL)
            return False
    
    def load_context(self):
        """🗣️ Load context from file"""
        try:
            with open('memory/context_data.json', 'r', encoding='utf-8') as f:
                context_data = json.load(f)
                
                self.current_context = context_data.get('current_context', {})
                self.topic_stack = context_data.get('topic_stack', [])
                self.entity_context = context_data.get('entity_context', {})
                
                # Convert string timestamps back to datetime objects if needed
                for entity_type in self.entity_context:
                    for entity in self.entity_context[entity_type]:
                        if isinstance(entity['timestamp'], str):
                            # Keep as string for JSON compatibility
                            pass
                
                print(Fore.GREEN + f"🗣️ Context loaded: {len(self.topic_stack)} topics, {len(self.entity_context)} entity types" + Style.RESET_ALL)
                
                return True
                
        except FileNotFoundError:
            print(Fore.YELLOW + "⚠️ No saved context found" + Style.RESET_ALL)
            return False
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Context load error: {str(e)}" + Style.RESET_ALL)
            return False
    
    def get_context_summary(self):
        """🗣️ Get context summary"""
        summary = {
            'current_topic': self.get_current_topic(),
            'topic_history': self.topic_stack[-5:],
            'entity_types': list(self.entity_context.keys()),
            'total_interactions': len(self.context_history),
            'follow_up_expected': self.follow_up_expected,
            'follow_up_type': self.follow_up_type
        }
        
        # Add recent entities count
        entity_counts = {}
        for entity_type, entities in self.entity_context.items():
            entity_counts[entity_type] = len(entities)
        summary['entity_counts'] = entity_counts
        
        return summary
    
    def predict_next_action(self):
        """🗣️ Predict next likely action based on context"""
        if not self.context_history:
            return None
        
        last_context = self.context_history[-1]
        topic = last_context.get('topic', 'general')
        
        # Prediction based on topic
        predictions = {
            'youtube': ['search', 'play', 'pause', 'next'],
            'whatsapp': ['send', 'reply', 'forward', 'call'],
            'web_search': ['open', 'read', 'save', 'share'],
            'system': ['check', 'monitor', 'optimize', 'report'],
            'apps': ['switch', 'close', 'minimize', 'maximize'],
            'coding': ['run', 'debug', 'save', 'test']
        }
        
        if topic in predictions:
            return predictions[topic][0]  # Return most likely
        
        return None