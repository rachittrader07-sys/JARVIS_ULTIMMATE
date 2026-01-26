"""
🎙️ Speech-to-Text Engine
Converts speech to text using multiple fallback methods
"""

import json
import os
import tempfile

import speech_recognition as sr
from colorama import Fore, Style


class STTEngine:
    def __init__(self, config):
        self.config = config
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = "hi-IN"  # Hindi-English mixed

        # Adjust for ambient noise
        print(Fore.YELLOW + "🔧 Adjusting for ambient noise..." + Style.RESET_ALL)
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        print(Fore.GREEN + "✅ STT Engine Ready (Language: Hinglish)" + Style.RESET_ALL)

    def listen(self, timeout=5, phrase_time_limit=8):
        """🎙️ Listen for speech and convert to text"""
        try:
            with self.microphone as source:
                print(
                    Fore.GREEN
                    + self.config["indicators"]["listening"]
                    + " Listening... (Speak now)"
                    + Style.RESET_ALL
                )

                # Listen for audio
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )

                print(
                    Fore.YELLOW
                    + self.config["indicators"]["thinking"]
                    + " Processing speech..."
                    + Style.RESET_ALL
                )

                # Try multiple recognition methods
                text = self.recognize_with_fallback(audio)

                if text:
                    # Normalize text (Hinglish normalization)
                    text = self.normalize_text(text)
                    return text
                else:
                    print(Fore.RED + "❌ Could not understand speech" + Style.RESET_ALL)
                    return None

        except sr.WaitTimeoutError:
            print(Fore.YELLOW + "⏰ Listening timeout" + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"❌ Listening error: {str(e)}" + Style.RESET_ALL)
            return None

    def recognize_with_fallback(self, audio):
        """🎙️ Try multiple STT methods with fallback"""
        methods = [
            ("Google", self.recognize_google),
            ("Vosk", self.recognize_vosk),
            ("Whisper", self.recognize_whisper),
        ]

        for method_name, method_func in methods:
            try:
                text = method_func(audio)
                if text and len(text.strip()) > 1:
                    print(
                        Fore.GREEN
                        + f"✅ Recognized with {method_name}: {text}"
                        + Style.RESET_ALL
                    )
                    return text
            except Exception as e:
                print(
                    Fore.YELLOW + f"⚠️ {method_name} failed: {str(e)}" + Style.RESET_ALL
                )
                continue

        return None

    def recognize_google(self, audio):
        """🎙️ Google Speech Recognition"""
        return self.recognizer.recognize_google(audio, language=self.language)

    @staticmethod
    def recognize_vosk(audio):
        """🎙️ Offline recognition with Vosk"""
        try:
            import vosk

            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                audio_file = f.name
                with open(audio_file, "wb") as f_audio:
                    f_audio.write(audio.get_wav_data())

            # Use Vosk to transcribe
            model_path = "vosk-model-small-en-in-0.4"
            if os.path.exists(model_path):
                model = vosk.Model(model_path)
                rec = vosk.KaldiRecognizer(model, 16000)

                with open(audio_file, "rb") as f:
                    data = f.read()
                    if rec.AcceptWaveform(data):
                        result = rec.Result()
                        text = json.loads(result).get("text", "")

                os.remove(audio_file)
                return text

        except:
            pass

        return None

    @staticmethod
    def recognize_whisper(audio):
        """🎙️ Whisper speech recognition (if available)"""
        try:
            import whisper

            # Save audio to file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                audio_file = f.name
                with open(audio_file, "wb") as f_audio:
                    f_audio.write(audio.get_wav_data())

            # Load whisper model
            model = whisper.load_model("base")
            result = model.transcribe(audio_file)

            os.remove(audio_file)
            return result["text"]

        except:
            return None

    @staticmethod
    def normalize_text(text):
        """🎙️ Normalize Hinglish text"""
        normalization_map = {
            "kitni hai": "kitna hai",
            "kitni battery": "kitna battery",
            "minimise": "minimize",
            "band karo": "close",
            "kholo": "open",
            "chalao": "play",
            "rok do": "stop",
            "aage": "next",
            "piche": "previous",
            "upar": "up",
            "niche": "down",
            "bhejo": "send",
            "dhundho": "search",
            "batao": "tell",
            "kaise ho": "how are you",
        }

        text_lower = text.lower()
        for old, new in normalization_map.items():
            if old in text_lower:
                text_lower = text_lower.replace(old, new)

        return text_lower.strip()
