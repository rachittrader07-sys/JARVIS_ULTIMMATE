"""
🔊 Text-to-Speech Engine
Converts text to speech with emotion and Indian accent
"""

import pyttsx3
import threading
import queue
import time
from colorama import Fore, Style

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.current_emotion = "neutral"
        
        self.initialize_engine()
        
        # Start speech thread
        self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.speech_thread.start()
        
        print(Fore.GREEN + "✅ TTS Engine Ready (Indian Male Voice)" + Style.RESET_ALL)
    
    def initialize_engine(self):
        """🔊 Initialize TTS engine with Indian voice"""
        try:
            self.engine = pyttsx3.init()
            
            # Get voices
            voices = self.engine.getProperty('voices')
            
            # Find Indian male voice
            indian_voice = None
            for voice in voices:
                if 'indian' in voice.name.lower() or 'hindi' in voice.name.lower():
                    if 'male' in voice.name.lower() or 'microsoft david' in voice.name.lower():
                        indian_voice = voice
                        break
            
            if indian_voice:
                self.engine.setProperty('voice', indian_voice.id)
                print(Fore.GREEN + f"✅ Voice set to: {indian_voice.name}" + Style.RESET_ALL)
            else:
                # Use default
                for voice in voices:
                    if 'male' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
            
            # Set properties from config
            self.engine.setProperty('rate', self.config['jarvis']['voice']['rate'])
            self.engine.setProperty('volume', self.config['jarvis']['voice']['volume'])
            
        except Exception as e:
            print(Fore.RED + f"❌ TTS initialization failed: {str(e)}" + Style.RESET_ALL)
    
    def speak(self, text, emotion=None):
        """🔊 Speak text with optional emotion"""
        if not text or not self.engine:
            return
        
        # Add to queue
        self.speech_queue.put((text, emotion))
    
    def _speech_worker(self):
        """🔊 Worker thread for speech synthesis"""
        while True:
            try:
                text, emotion = self.speech_queue.get()
                
                if emotion:
                    self.set_emotion(emotion)
                
                self.is_speaking = True
                
                # Add emotion indicators to speech
                emotion_text = self._add_emotion_indicators(text, emotion)
                
                print(Fore.CYAN + f"\n🗣️ JARVIS: {text}" + Style.RESET_ALL)
                
                # Speak
                self.engine.say(emotion_text)
                self.engine.runAndWait()
                
                self.is_speaking = False
                self.speech_queue.task_done()
                
            except Exception as e:
                print(Fore.RED + f"❌ Speech error: {str(e)}" + Style.RESET_ALL)
                self.is_speaking = False
    
    def set_emotion(self, emotion):
        """🔊 Adjust voice based on emotion"""
        self.current_emotion = emotion
        
        if emotion == "happy":
            self.engine.setProperty('rate', 200)  # Faster
            self.engine.setProperty('volume', 1.0)  # Louder
        elif emotion == "sad":
            self.engine.setProperty('rate', 140)  # Slower
            self.engine.setProperty('volume', 0.8)  # Softer
        elif emotion == "excited":
            self.engine.setProperty('rate', 220)  # Very fast
            self.engine.setProperty('volume', 1.0)
        elif emotion == "calm":
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 0.7)
        else:  # neutral
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 1.0)
    
    @staticmethod
    def _add_emotion_indicators(text, emotion):
        """🔊 Add emotional indicators to text"""
        if not emotion or emotion == "neutral":
            return text
        
        # Add appropriate punctuation/words based on emotion
        if emotion == "happy":
            return text + " 😊"
        elif emotion == "sad":
            return text + " 😔"
        elif emotion == "excited":
            return text + " 🎉"
        elif emotion == "calm":
            return text + " 🧘"
        
        return text
    
    def stop(self):
        """🔊 Stop current speech"""
        if self.engine:
            self.engine.stop()
    
    def is_busy(self):
        """🔊 Check if currently speaking"""
        return self.is_speaking or not self.speech_queue.empty()