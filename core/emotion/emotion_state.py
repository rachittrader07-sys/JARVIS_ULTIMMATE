"""
❤️ Emotion State Manager
Manages current emotional state
"""

import json
from datetime import datetime
from colorama import Fore, Style

class EmotionState:
    def __init__(self, config):
        self.config = config
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5  # 0.0 to 1.0
        self.emotion_history = []
        self.mood_score = 0.5  # Overall mood (-1.0 to 1.0)
        
        # Emotion parameters
        self.emotion_params = {
            "happy": {"energy": 0.8, "positivity": 0.9},
            "sad": {"energy": 0.3, "positivity": 0.2},
            "angry": {"energy": 0.9, "positivity": 0.1},
            "excited": {"energy": 0.95, "positivity": 0.8},
            "calm": {"energy": 0.4, "positivity": 0.7},
            "neutral": {"energy": 0.5, "positivity": 0.5}
        }
        
    def set_emotion(self, emotion, intensity=0.7):
        """❤️ Set current emotion"""
        if emotion not in self.emotion_params:
            emotion = "neutral"
        
        self.current_emotion = emotion
        self.emotion_intensity = max(0.1, min(1.0, intensity))
        
        # Update mood score
        self._update_mood_score()
        
        # Add to history
        self._add_to_history(emotion, intensity)
        
        print(Fore.MAGENTA + f"❤️ Emotion set: {emotion} (intensity: {intensity:.2f})" + Style.RESET_ALL)
        
        return True
    
    def get_emotion(self):
        """❤️ Get current emotion with parameters"""
        params = self.emotion_params.get(self.current_emotion, {})
        return {
            'emotion': self.current_emotion,
            'intensity': self.emotion_intensity,
            'mood_score': self.mood_score,
            'energy': params.get('energy', 0.5),
            'positivity': params.get('positivity', 0.5)
        }
    
    def adjust_emotion(self, delta_emotion=None, delta_intensity=0.0):
        """❤️ Adjust emotion based on interaction"""
        if delta_emotion:
            # Change emotion type
            self.set_emotion(delta_emotion, self.emotion_intensity)
        else:
            # Just adjust intensity
            self.emotion_intensity = max(0.1, min(1.0, self.emotion_intensity + delta_intensity))
            
            # If intensity very low, maybe switch to neutral
            if self.emotion_intensity < 0.2 and self.current_emotion != "neutral":
                self.current_emotion = "neutral"
        
        self._update_mood_score()
    
    def _update_mood_score(self):
        """❤️ Update overall mood score"""
        emotion_data = self.get_emotion()
        positivity = emotion_data['positivity']
        intensity = emotion_data['intensity']
        
        # Calculate mood score (-1.0 to 1.0)
        if self.current_emotion in ["happy", "excited", "calm"]:
            self.mood_score = positivity * intensity
        elif self.current_emotion in ["sad", "angry"]:
            self.mood_score = -positivity * intensity
        else:
            self.mood_score = 0.0
    
    def _add_to_history(self, emotion, intensity):
        """❤️ Add emotion to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'intensity': intensity,
            'mood_score': self.mood_score
        }
        
        self.emotion_history.append(entry)
        
        # Keep only last 1000 entries
        if len(self.emotion_history) > 1000:
            self.emotion_history = self.emotion_history[-1000:]
        
        # Auto-save every 10 entries
        if len(self.emotion_history) % 10 == 0:
            self.save_history()
    
    def get_emotion_trend(self, hours=24):
        """❤️ Get emotion trend over time"""
        # Filter entries from last N hours
        cutoff = datetime.now().timestamp() - (hours * 3600)
        
        recent = []
        for entry in self.emotion_history:
            try:
                entry_time = datetime.fromisoformat(entry['timestamp']).timestamp()
                if entry_time >= cutoff:
                    recent.append(entry)
            except:
                continue
        
        if not recent:
            return {"trend": "stable", "dominant_emotion": "neutral"}
        
        # Count emotions
        emotion_counts = {}
        for entry in recent:
            emotion = entry['emotion']
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
            emotion_counts[emotion] += 1
        
        # Find dominant emotion
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Calculate trend
        if len(recent) >= 2:
            first_mood = recent[0]['mood_score']
            last_mood = recent[-1]['mood_score']
            
            if last_mood > first_mood + 0.2:
                trend = "improving"
            elif last_mood < first_mood - 0.2:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "dominant_emotion": dominant_emotion,
            "recent_count": len(recent),
            "emotion_distribution": emotion_counts
        }
    
    def save_history(self):
        """❤️ Save emotion history to file"""
        try:
            with open('memory/emotion_state.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'current_emotion': self.current_emotion,
                    'emotion_intensity': self.emotion_intensity,
                    'mood_score': self.mood_score,
                    'history': self.emotion_history[-100:]  # Save only recent
                }, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def load_history(self):
        """❤️ Load emotion history from file"""
        try:
            with open('memory/emotion_state.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_emotion = data.get('current_emotion', 'neutral')
                self.emotion_intensity = data.get('emotion_intensity', 0.5)
                self.mood_score = data.get('mood_score', 0.5)
                self.emotion_history = data.get('history', [])
        except:
            pass
    
    def get_appropriate_response_style(self):
        """❤️ Get appropriate response style based on emotion"""
        styles = {
            "happy": {
                "tone": "cheerful",
                "speed": "fast",
                "volume": "high",
                "words": ["Great!", "Awesome!", "Excellent!", "Perfect!"]
            },
            "sad": {
                "tone": "gentle",
                "speed": "slow",
                "volume": "low",
                "words": ["I understand.", "It's okay.", "Take your time.", "I'm here."]
            },
            "angry": {
                "tone": "calm",
                "speed": "medium",
                "volume": "medium",
                "words": ["I apologize.", "Let me fix that.", "Right away.", "Understood."]
            },
            "excited": {
                "tone": "energetic",
                "speed": "very_fast",
                "volume": "high",
                "words": ["Wow!", "Fantastic!", "Let's go!", "Right on!"]
            },
            "calm": {
                "tone": "soothing",
                "speed": "slow",
                "volume": "low",
                "words": ["Certainly.", "Of course.", "As you wish.", "Perfect."]
            },
            "neutral": {
                "tone": "professional",
                "speed": "normal",
                "volume": "medium",
                "words": ["Okay.", "Sure.", "Right.", "Done."]
            }
        }
        
        return styles.get(self.current_emotion, styles["neutral"])