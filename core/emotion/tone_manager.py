"""
🎵 Tone Manager
Manages voice tone and speech patterns based on emotion
"""

import pyttsx3
from colorama import Fore, Style


class ToneManager:
    def __init__(self, config):
        self.config = config
        self.current_tone = "neutral"
        self.tone_settings = self.load_tone_settings()
        self.engine = None

        # Initialize TTS engine
        self.initialize_engine()

    @staticmethod
    def load_tone_settings():
        """🎵 Load tone settings for different emotions"""
        settings = {
            "happy": {
                "rate": 200,  # Faster
                "volume": 1.0,  # Louder
                "pitch": 120,  # Higher pitch
                "emphasis": "high",
                "style": "cheerful",
            },
            "sad": {
                "rate": 140,  # Slower
                "volume": 0.7,  # Softer
                "pitch": 90,  # Lower pitch
                "emphasis": "low",
                "style": "gentle",
            },
            "angry": {
                "rate": 180,  # Normal speed
                "volume": 0.9,  # Slightly louder
                "pitch": 100,  # Medium pitch
                "emphasis": "sharp",
                "style": "firm",
            },
            "excited": {
                "rate": 220,  # Very fast
                "volume": 1.0,  # Loud
                "pitch": 130,  # High pitch
                "emphasis": "very_high",
                "style": "energetic",
            },
            "calm": {
                "rate": 160,  # Slow
                "volume": 0.8,  # Medium volume
                "pitch": 100,  # Normal pitch
                "emphasis": "smooth",
                "style": "soothing",
            },
            "neutral": {
                "rate": 180,  # Default speed
                "volume": 1.0,  # Default volume
                "pitch": 100,  # Default pitch
                "emphasis": "normal",
                "style": "professional",
            },
            "professional": {
                "rate": 190,  # Slightly fast
                "volume": 0.9,  # Clear volume
                "pitch": 110,  # Clear pitch
                "emphasis": "clear",
                "style": "formal",
            },
            "friendly": {
                "rate": 170,  # Comfortable speed
                "volume": 0.85,  # Friendly volume
                "pitch": 105,  # Warm pitch
                "emphasis": "warm",
                "style": "casual",
            },
        }
        return settings

    def initialize_engine(self):
        """🎵 Initialize TTS engine"""
        try:
            self.engine = pyttsx3.init()

            # Get voices
            voices = self.engine.getProperty("voices")

            # Try to find Indian male voice
            for voice in voices:
                if "indian" in voice.name.lower() or "hindi" in voice.name.lower():
                    if "male" in voice.name.lower():
                        self.engine.setProperty("voice", voice.id)
                        print(
                            Fore.GREEN
                            + f"✅ Indian male voice found: {voice.name}"
                            + Style.RESET_ALL
                        )
                        break

            # Set default properties
            self.set_tone("neutral")

        except Exception as e:
            print(
                Fore.RED
                + f"❌ Tone manager initialization failed: {str(e)}"
                + Style.RESET_ALL
            )

    def set_tone(self, tone_name):
        """🎵 Set voice tone"""
        if tone_name not in self.tone_settings:
            tone_name = "neutral"

        self.current_tone = tone_name
        settings = self.tone_settings[tone_name]

        if self.engine:
            # Apply settings
            self.engine.setProperty("rate", settings["rate"])
            self.engine.setProperty("volume", settings["volume"])

            # Note: pyttsx3 doesn't directly support pitch control
            # We adjust through voice selection

            print(
                Fore.CYAN
                + f"🎵 Tone set to: {tone_name} (rate: {settings['rate']}, volume: {settings['volume']})"
                + Style.RESET_ALL
            )

        return settings

    def get_current_tone(self):
        """🎵 Get current tone settings"""
        return self.tone_settings.get(self.current_tone, self.tone_settings["neutral"])

    def adjust_tone_dynamically(self, emotion, intensity=0.5):
        """🎵 Adjust tone dynamically based on emotion intensity"""
        base_settings = self.tone_settings.get(emotion, self.tone_settings["neutral"])

        # Adjust based on intensity
        adjusted_settings = base_settings.copy()

        # Rate adjustment
        if intensity > 0.7:
            adjusted_settings["rate"] = int(base_settings["rate"] * 1.2)
        elif intensity < 0.3:
            adjusted_settings["rate"] = int(base_settings["rate"] * 0.8)

        # Volume adjustment
        if emotion in ["happy", "excited"]:
            adjusted_settings["volume"] = min(
                1.0, base_settings["volume"] * (0.8 + intensity)
            )
        elif emotion in ["sad", "calm"]:
            adjusted_settings["volume"] = max(
                0.3, base_settings["volume"] * (0.5 + intensity)
            )

        # Apply adjusted settings
        if self.engine:
            self.engine.setProperty("rate", adjusted_settings["rate"])
            self.engine.setProperty("volume", adjusted_settings["volume"])

        return adjusted_settings

    def speak_with_tone(self, text, tone=None):
        """🎵 Speak text with specified tone"""
        if not self.engine:
            print(Fore.RED + "❌ TTS engine not initialized" + Style.RESET_ALL)
            return False

        try:
            # Set tone if specified
            if tone:
                self.set_tone(tone)

            # Add emotional indicators to text
            emotional_text = self.add_emotional_indicators(text)

            # Speak
            print(
                Fore.CYAN
                + f"🗣️ Speaking with {self.current_tone} tone: {text[:50]}..."
                + Style.RESET_ALL
            )

            self.engine.say(emotional_text)
            self.engine.runAndWait()

            return True

        except Exception as e:
            print(Fore.RED + f"❌ Speech error: {str(e)}" + Style.RESET_ALL)
            return False

    def add_emotional_indicators(self, text):
        """🎵 Add emotional indicators to text"""
        tone = self.current_tone

        # Add appropriate punctuation/emphasis based on tone
        if tone == "excited":
            if not text.endswith(("!", "?", "...")):
                text += "!"
        elif tone == "calm":
            if text.endswith("!"):
                text = text[:-1] + "."
        elif tone == "sad":
            if not text.endswith((".", "...")):
                text += "..."

        # Add emotional words based on tone
        tone_prefixes = {
            "happy": ["Great! ", "Awesome! ", "Excellent! "],
            "sad": ["I understand... ", "Hmm... ", "Oh... "],
            "excited": ["Wow! ", "Fantastic! ", "Amazing! "],
            "calm": ["Sure. ", "Certainly. ", "Of course. "],
        }

        if tone in tone_prefixes and not text.startswith(tuple(tone_prefixes[tone])):
            # Occasionally add prefix
            import random

            if random.random() > 0.7:
                prefix = random.choice(tone_prefixes[tone])
                text = prefix + text

        return text

    def get_voice_properties(self):
        """🎵 Get current voice properties"""
        if not self.engine:
            return {}

        properties = {
            "rate": self.engine.getProperty("rate"),
            "volume": self.engine.getProperty("volume"),
            "voice": self.engine.getProperty("voice"),
            "tone": self.current_tone,
        }

        return properties

    def save_tone_preferences(self):
        """🎵 Save tone preferences to file"""
        try:
            preferences = {
                "current_tone": self.current_tone,
                "voice_properties": self.get_voice_properties(),
                "timestamp": datetime.now().isoformat(),
            }

            with open("memory/tone_preferences.json", "w", encoding="utf-8") as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(
                Fore.YELLOW
                + f"⚠️ Tone preferences save error: {str(e)}"
                + Style.RESET_ALL
            )
            return False

    def load_tone_preferences(self):
        """🎵 Load tone preferences from file"""
        try:
            with open("memory/tone_preferences.json", "r", encoding="utf-8") as f:
                preferences = json.load(f)

                # Set tone
                tone = preferences.get("current_tone", "neutral")
                self.set_tone(tone)

                # Apply saved properties if available
                properties = preferences.get("voice_properties", {})
                if properties and self.engine:
                    if "rate" in properties:
                        self.engine.setProperty("rate", properties["rate"])
                    if "volume" in properties:
                        self.engine.setProperty("volume", properties["volume"])

                print(
                    Fore.GREEN + f"✅ Tone preferences loaded: {tone}" + Style.RESET_ALL
                )

                return True

        except FileNotFoundError:
            print(Fore.YELLOW + "⚠️ No tone preferences found" + Style.RESET_ALL)
            return False
        except Exception as e:
            print(
                Fore.YELLOW
                + f"⚠️ Tone preferences load error: {str(e)}"
                + Style.RESET_ALL
            )
            return False

    def test_all_tones(self):
        """🎵 Test all available tones"""
        test_text = "Namaste sir, main JARVIS bol raha hoon."

        print(Fore.CYAN + "\n🎵 Testing all tones..." + Style.RESET_ALL)

        for tone_name in self.tone_settings.keys():
            print(Fore.YELLOW + f"\nTesting {tone_name} tone..." + Style.RESET_ALL)
            self.set_tone(tone_name)
            self.speak_with_tone(test_text)

            # Small pause between tones
            import time

            time.sleep(1)

        # Return to neutral
        self.set_tone("neutral")
        print(Fore.GREEN + "\n✅ Tone testing complete" + Style.RESET_ALL)
