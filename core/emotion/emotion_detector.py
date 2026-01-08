"""
❤️ Emotion Detector
Detects emotion from voice and text
"""

import re
import json
import numpy as np
from datetime import datetime
from colorama import Fore, Style

class EmotionDetector:
    def __init__(self, config):
        self.config = config
        self.current_emotion = "neutral"
        self.emotion_history = []
        self.emotion_keywords = self.load_emotion_keywords()
        self.voice_features = {}
        
    def detect_emotion(self, text, voice_features=None):
        """❤️ Detect emotion from text and voice"""
        # Store voice features if provided
        if voice_features:
            self.voice_features = voice_features
        
        # Detect from text
        text_emotion = self.detect_from_text(text)
        
        # Detect from voice if available
        voice_emotion = "neutral"
        if voice_features:
            voice_emotion = self.detect_from_voice(voice_features)
        
        # Combine emotions
        combined_emotion = self.combine_emotions(text_emotion, voice_emotion)
        
        # Update history
        self.update_emotion_history(combined_emotion, text)
        
        # Set current emotion
        self.current_emotion = combined_emotion
        
        print(Fore.MAGENTA + f"❤️ Emotion detected: {combined_emotion}" + Style.RESET_ALL)
        return combined_emotion
    
    def detect_from_text(self, text):
        """❤️ Detect emotion from text content"""
        text_lower = text.lower()
        emotion_scores = {
            "happy": 0,
            "sad": 0,
            "angry": 0,
            "excited": 0,
            "calm": 0,
            "neutral": 0.5  # Default neutral score
        }
        
        # Check for keywords
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    emotion_scores[emotion] += 1
        
        # Check for exclamation marks (excitement)
        if "!" in text:
            emotion_scores["excited"] += 2
        
        # Check for question marks (curiosity/concern)
        if "?" in text:
            emotion_scores["calm"] += 1
        
        # Check for negative words
        negative_words = ["nahi", "mat", "rok", "band", "galti", "problem", "error"]
        for word in negative_words:
            if word in text_lower:
                emotion_scores["sad"] += 1
                emotion_scores["angry"] += 0.5
        
        # Check for positive words
        positive_words = ["acha", "shabash", "badhiya", "thanks", "dhanyavad", "great", "good"]
        for word in positive_words:
            if word in text_lower:
                emotion_scores["happy"] += 1
                emotion_scores["excited"] += 0.5
        
        # Get emotion with highest score
        max_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[max_emotion]
        
        # If score is too low, return neutral
        if max_score < 0.7:
            return "neutral"
        
        return max_emotion
    
    def detect_from_voice(self, voice_features):
        """❤️ Detect emotion from voice features"""
        # Simplified voice emotion detection
        # In real implementation, you would use ML model
        
        # Mock implementation based on pitch and speed
        pitch = voice_features.get('pitch', 0)
        speed = voice_features.get('speed', 0)
        volume = voice_features.get('volume', 0)
        
        if pitch > 200 and speed > 180:
            return "excited"
        elif pitch < 150 and speed < 120:
            return "sad"
        elif volume > 0.8 and speed > 160:
            return "angry"
        elif volume < 0.6 and speed < 140:
            return "calm"
        elif pitch > 180 and volume > 0.7:
            return "happy"
        
        return "neutral"
    
    def combine_emotions(self, text_emotion, voice_emotion):
        """❤️ Combine text and voice emotions"""
        if text_emotion == voice_emotion:
            return text_emotion
        
        # Weight text emotion more (70%)
        emotion_weights = {
            text_emotion: 0.7,
            voice_emotion: 0.3
        }
        
        return max(emotion_weights, key=emotion_weights.get)
    
    def update_emotion_history(self, emotion, text):
        """❤️ Update emotion history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'text': text[:100],  # Store first 100 chars
            'duration': 0
        }
        
        self.emotion_history.append(entry)
        
        # Keep only last 100 entries
        if len(self.emotion_history) > 100:
            self.emotion_history = self.emotion_history[-100:]
        
        # Save to file periodically
        if len(self.emotion_history) % 10 == 0:
            self.save_emotion_history()
    
    def save_emotion_history(self):
        """❤️ Save emotion history to file"""
        try:
            with open('memory/emotion_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.emotion_history, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def load_emotion_keywords(self):
        """❤️ Load emotion keywords"""
        keywords = {
            "happy": [
                "happy", "khush", "acha", "badhiya", "maza",
                "fun", "enjoy", "thanks", "dhanyavad", "shukriya",
                "great", "good", "wow", "awesome", "excellent"
            ],
            "sad": [
                "sad", "udaas", "dukhi", "thak", "tired",
                "bore", "problem", "issue", "error", "galti",
                "sorry", "maaf", "afsoos", "disappoint"
            ],
            "angry": [
                "angry", "gussa", "naraz", "problem", "wrong",
                "error", "fail", "nahi hua", "not work", "band",
                "stop", "ruk", "mat karo"
            ],
            "excited": [
                "excited", "utsahit", "josh", "ready", "let's go",
                "chalo", "start", "begin", "fast", "quick",
                "now", "immediately", "turant"
            ],
            "calm": [
                "calm", "shant", "aram", "slow", "thoda",
                "please", "kripya", "zara", "wait", "ruk",
                "thoda der", "patience", "sabr"
            ]
        }
        
        return keywords
    
    def get_emotion_response(self, emotion):
        """❤️ Get appropriate response based on emotion"""
        responses = {
            "happy": {
                "prefix": "Great! ",
                "suffix": " Sir 😊",
                "tone": "excited"
            },
            "sad": {
                "prefix": "I understand. ",
                "suffix": " Sir 🫂",
                "tone": "soft"
            },
            "angry": {
                "prefix": "I apologize. ",
                "suffix": " Sir 🫡",
                "tone": "calm"
            },
            "excited": {
                "prefix": "Awesome! ",
                "suffix": " Sir 🎉",
                "tone": "excited"
            },
            "calm": {
                "prefix": "Sure. ",
                "suffix": " Sir 🧘",
                "tone": "calm"
            },
            "neutral": {
                "prefix": "",
                "suffix": " Sir ✅",
                "tone": "neutral"
            }
        }
        
        return responses.get(emotion, responses["neutral"])
    
    def get_emotion_stats(self):
        """❤️ Get emotion statistics"""
        stats = {}
        total = len(self.emotion_history)
        
        if total == 0:
            return stats
        
        for entry in self.emotion_history:
            emotion = entry['emotion']
            if emotion not in stats:
                stats[emotion] = 0
            stats[emotion] += 1
        
        # Convert to percentages
        for emotion in stats:
            stats[emotion] = (stats[emotion] / total * 100)
        
        return stats