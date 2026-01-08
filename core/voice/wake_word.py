"""
🎙️ Wake Word Detection
Listens for "Jarvis" keyword
"""

import threading
import time

import numpy as np
import speech_recognition as sr
from colorama import Fore, Style


class WakeWordDetector:
    def __init__(self, config):
        self.config = config
        self.wake_word = config["jarvis"]["wake_word"].lower()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_detected = False
        self.confidence_threshold = 0.6

        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        print(Fore.GREEN + f"🎙️ Wake word set to: '{self.wake_word}'" + Style.RESET_ALL)

    def detect(self):
        """🎙️ Detect wake word in audio stream"""
        try:
            with self.microphone as source:
                print(
                    Fore.YELLOW
                    + self.config["indicators"]["listening"]
                    + " Listening for wake word..."
                    + Style.RESET_ALL,
                    end="\r",
                )

                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=2)

                # Try to recognize using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(
                        audio, language="hi-IN"
                    ).lower()

                    # Check if wake word is in text
                    if self.wake_word in text:
                        print(
                            Fore.GREEN
                            + f"\n🎯 Wake word detected: '{text}'"
                            + Style.RESET_ALL
                        )
                        return True

                except sr.UnknownValueError:
                    pass  # No speech detected
                except sr.RequestError:
                    print(
                        Fore.YELLOW + "⚠️ Speech service unavailable" + Style.RESET_ALL
                    )

        except Exception as e:
            # Timeout or other error
            pass

        return False

    def detect_vosk(self):
        """🎙️ Alternative: Use Vosk for offline wake word detection"""
        try:
            import pyaudio
            import vosk

            # Load Vosk model
            model_path = "vosk-model-small-en-in-0.4"
            if not os.path.exists(model_path):
                print(
                    Fore.YELLOW
                    + "⚠️ Vosk model not found, using online recognition"
                    + Style.RESET_ALL
                )
                return self.detect()

            model = vosk.Model(model_path)
            recognizer = vosk.KaldiRecognizer(model, 16000)

            # Audio stream
            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000,
            )
            stream.start_stream()

            # Listen for 2 seconds
            start_time = time.time()
            while time.time() - start_time < 2:
                data = stream.read(4000, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    text = json.loads(result).get("text", "").lower()

                    if self.wake_word in text:
                        stream.stop_stream()
                        stream.close()
                        p.terminate()
                        return True

            stream.stop_stream()
            stream.close()
            p.terminate()

        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Vosk detection failed: {str(e)}" + Style.RESET_ALL)

        return False
