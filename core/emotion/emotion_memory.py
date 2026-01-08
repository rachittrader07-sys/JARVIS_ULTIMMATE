"""
❤️ Emotion Memory
Remembers emotional patterns and responses
"""

import json
import os
from datetime import datetime, timedelta
from colorama import Fore, Style

class EmotionMemory:
    def __init__(self, config):
        self.config = config
        self.emotional_patterns = []
        self.user_mood_patterns = []
        self.interaction_history = []
        self.emotion_responses = self.load_default_responses()
        
        self.load_memory()
    
    def load_default_responses(self):
        """❤️ Load default emotional responses"""
        return {
            "greeting": {
                "happy": "Hello sir! Great to see you today! 😊",
                "sad": "Hello sir... I hope you're doing okay. 🫂",
                "angry": "Sir. 🫡",
                "excited": "HELLO SIR! Ready for action! 🚀",
                "calm": "Good day, sir. 🧘",
                "neutral": "Hello sir. How can I help?"
            },
            "success": {
                "happy": "Done sir! That was fun! ✅",
                "sad": "Completed, sir... 😐",
                "angry": "Task executed. ✅",
                "excited": "SUCCESS! Perfect execution! 🎉",
                "calm": "Completed successfully, sir. ✅",
                "neutral": "Task completed, sir."
            },
            "error": {
                "happy": "Oops! A little hiccup, but no problem! 😅",
                "sad": "I'm sorry sir, I couldn't do that... 😔",
                "angry": "Error occurred. My apologies. ⚠️",
                "excited": "Whoops! Let me try that again! 🔄",
                "calm": "There seems to be an issue, sir. 😐",
                "neutral": "Sorry sir, there was an error."
            },
            "confirmation": {
                "happy": "Are you sure sir? Just checking! 😊",
                "sad": "Please confirm, sir... 😐",
                "angry": "Confirm action. ⚠️",
                "excited": "Double checking! Are you SURE sure? 🤔",
                "calm": "Please confirm, sir. 🧘",
                "neutral": "Please confirm, sir."
            }
        }
    
    def record_interaction(self, user_input, jarvis_response, user_emotion, jarvis_emotion):
        """❤️ Record an interaction with emotions"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input[:100],  # Limit length
            'jarvis_response': jarvis_response[:100],
            'user_emotion': user_emotion,
            'jarvis_emotion': jarvis_emotion,
            'success': True  # Default, can be updated
        }
        
        self.interaction_history.append(entry)
        
        # Keep history limited
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
        
        # Analyze for patterns
        self.analyze_pattern(entry)
        
        # Auto-save
        if len(self.interaction_history) % 50 == 0:
            self.save_memory()
    
    def analyze_pattern(self, interaction):
        """❤️ Analyze interaction for patterns"""
        # Check time-based patterns
        hour = datetime.now().hour
        
        # Check if this is a recurring interaction
        similar_interactions = self.find_similar_interactions(interaction)
        
        if len(similar_interactions) > 3:
            # Pattern detected
            pattern = {
                'type': 'interaction_pattern',
                'user_input': interaction['user_input'],
                'common_emotion': interaction['user_emotion'],
                'time_of_day': hour,
                'count': len(similar_interactions),
                'first_seen': similar_interactions[0]['timestamp'],
                'last_seen': interaction['timestamp']
            }
            
            # Check if pattern already exists
            existing = self.find_similar_pattern(pattern)
            if existing:
                existing['count'] += 1
                existing['last_seen'] = interaction['timestamp']
            else:
                self.emotional_patterns.append(pattern)
    
    def find_similar_interactions(self, interaction):
        """❤️ Find similar interactions in history"""
        similar = []
        user_input = interaction['user_input'].lower()
        
        for hist in self.interaction_history:
            if hist['user_input'].lower() == user_input:
                similar.append(hist)
        
        return similar
    
    def find_similar_pattern(self, pattern):
        """❤️ Find similar pattern in memory"""
        for p in self.emotional_patterns:
            if p['type'] == pattern['type'] and p['user_input'] == pattern['user_input']:
                return p
        return None
    
    def get_emotional_response(self, response_type, emotion):
        """❤️ Get emotional response for given type"""
        responses = self.emotion_responses.get(response_type, {})
        return responses.get(emotion, responses.get("neutral", ""))
    
    def learn_user_mood_pattern(self, time_of_day, day_of_week, mood):
        """❤️ Learn user's mood patterns"""
        pattern_key = f"{day_of_week}_{time_of_day}"
        
        # Find existing pattern
        for pattern in self.user_mood_patterns:
            if pattern['key'] == pattern_key:
                # Update existing
                pattern['moods'].append(mood)
                pattern['count'] += 1
                pattern['last_updated'] = datetime.now().isoformat()
                return
        
        # Create new pattern
        new_pattern = {
            'key': pattern_key,
            'time_of_day': time_of_day,
            'day_of_week': day_of_week,
            'moods': [mood],
            'count': 1,
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        
        self.user_mood_patterns.append(new_pattern)
    
    def predict_user_mood(self, time_of_day=None, day_of_week=None):
        """❤️ Predict user's mood based on patterns"""
        if not time_of_day:
            time_of_day = datetime.now().hour
        
        if not day_of_week:
            day_of_week = datetime.now().strftime("%A")
        
        pattern_key = f"{day_of_week}_{time_of_day}"
        
        # Find matching patterns
        matching_patterns = []
        for pattern in self.user_mood_patterns:
            if pattern['key'] == pattern_key:
                matching_patterns.append(pattern)
        
        if not matching_patterns:
            return "neutral"
        
        # Calculate average mood from patterns
        mood_counts = {}
        for pattern in matching_patterns:
            for mood in pattern['moods']:
                if mood not in mood_counts:
                    mood_counts[mood] = 0
                mood_counts[mood] += 1
        
        # Return most common mood
        if mood_counts:
            return max(mood_counts, key=mood_counts.get)
        
        return "neutral"
    
    def get_user_mood_insights(self):
        """❤️ Get insights about user's mood patterns"""
        insights = {
            'most_common_mood': 'neutral',
            'best_time_of_day': 'unknown',
            'worst_time_of_day': 'unknown',
            'mood_by_day': {},
            'total_interactions': len(self.interaction_history)
        }
        
        if not self.user_mood_patterns:
            return insights
        
        # Analyze mood patterns
        mood_counts = {}
        time_mood_map = {}
        day_mood_map = {}
        
        for pattern in self.user_mood_patterns:
            for mood in pattern['moods']:
                # Overall mood count
                if mood not in mood_counts:
                    mood_counts[mood] = 0
                mood_counts[mood] += 1
                
                # Mood by time
                time_key = pattern['time_of_day']
                if time_key not in time_mood_map:
                    time_mood_map[time_key] = {}
                if mood not in time_mood_map[time_key]:
                    time_mood_map[time_key][mood] = 0
                time_mood_map[time_key][mood] += 1
                
                # Mood by day
                day_key = pattern['day_of_week']
                if day_key not in day_mood_map:
                    day_mood_map[day_key] = {}
                if mood not in day_mood_map[day_key]:
                    day_mood_map[day_key][mood] = 0
                day_mood_map[day_key][mood] += 1
        
        # Find most common mood
        if mood_counts:
            insights['most_common_mood'] = max(mood_counts, key=mood_counts.get)
        
        # Find best/worst time of day
        positivity_scores = {}
        for time_key, moods in time_mood_map.items():
            # Calculate positivity score for this time
            positive_moods = moods.get('happy', 0) + moods.get('excited', 0)
            negative_moods = moods.get('sad', 0) + moods.get('angry', 0)
            total = sum(moods.values())
            
            if total > 0:
                score = (positive_moods - negative_moods) / total
                positivity_scores[time_key] = score
        
        if positivity_scores:
            insights['best_time_of_day'] = max(positivity_scores, key=positivity_scores.get)
            insights['worst_time_of_day'] = min(positivity_scores, key=positivity_scores.get)
        
        # Mood by day
        insights['mood_by_day'] = day_mood_map
        
        return insights
    
    def save_memory(self):
        """❤️ Save emotion memory to file"""
        try:
            data = {
                'emotional_patterns': self.emotional_patterns,
                'user_mood_patterns': self.user_mood_patterns,
                'interaction_history': self.interaction_history[-500],  # Save recent
                'saved_at': datetime.now().isoformat()
            }
            
            with open('memory/emotion_memory.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(Fore.GREEN + "❤️ Emotion memory saved" + Style.RESET_ALL)
            
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Emotion memory save error: {str(e)}" + Style.RESET_ALL)
    
    def load_memory(self):
        """❤️ Load emotion memory from file"""
        try:
            if os.path.exists('memory/emotion_memory.json'):
                with open('memory/emotion_memory.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    self.emotional_patterns = data.get('emotional_patterns', [])
                    self.user_mood_patterns = data.get('user_mood_patterns', [])
                    self.interaction_history = data.get('interaction_history', [])
                    
                print(Fore.GREEN + f"❤️ Emotion memory loaded: {len(self.interaction_history)} interactions" + Style.RESET_ALL)
                
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Emotion memory load error: {str(e)}" + Style.RESET_ALL)
    
    def cleanup_old_memory(self, days=90):
        """❤️ Cleanup old memory entries"""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()
        
        # Clean interaction history
        new_history = []
        for interaction in self.interaction_history:
            if interaction['timestamp'] >= cutoff_str:
                new_history.append(interaction)
        
        removed = len(self.interaction_history) - len(new_history)
        self.interaction_history = new_history
        
        return removed