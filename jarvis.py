#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 JARVIS - Advanced Desktop Voice Assistant
Author: Vaibhav
Version: 3.0
Language: Hinglish (Hindi + English)
"""

import os
import sys
import threading
import time
import traceback
from datetime import datetime

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.bootstrap import SystemBootstrap
from core.brain.decision_engine import DecisionEngine
from core.brain.intent_detector import IntentDetector
from core.conversation.dialogue_manager import DialogueManager
from core.emotion.emotion_detector import EmotionDetector
from core.error.error_catcher import ErrorCatcher
from core.state_manager import StateManager
from core.voice.stt_engine import STTEngine
from core.voice.tts_engine import TTSEngine
from core.voice.wake_word import WakeWordDetector
from utils.logger import setup_logger


class JARVIS:
    def __init__(self):
        """🎯 JARVIS Main Class Initialization"""
        print(
            Fore.CYAN
            + Style.BRIGHT
            + """
        ╔══════════════════════════════════════════╗
        ║           🎯 JARVIS v3.0                  ║
        ║   Advanced Desktop Voice Assistant       ║
        ║           Language: HINGLISH             ║
        ╚══════════════════════════════════════════╝
        """
        )

        # Setup logger
        self.logger = setup_logger()
        self.logger.info("🎯 JARVIS Initializing...")

        # Initialize components
        self.config = None
        self.bootstrap = None
        self.state = None
        self.wake_detector = None
        self.stt = None
        self.tts = None
        self.intent_detector = None
        self.decision_engine = None
        self.emotion_detector = None
        self.dialogue_manager = None
        self.error_catcher = None

        # Flags
        self.is_running = False
        self.is_listening = False
        self.current_context = {}

        # Performance metrics
        self.start_time = time.time()
        self.command_count = 0
        self.success_count = 0

    def initialize(self):
        """🎯 Initialize all JARVIS components"""
        try:
            print(
                Fore.YELLOW + "🎯 Initializing JARVIS Components..." + Style.RESET_ALL
            )

            # 1. Bootstrap system
            self.bootstrap = SystemBootstrap()
            self.bootstrap.run_checks()

            # 2. Load configuration
            from core.config_loader import ConfigLoader

            config_loader = ConfigLoader()
            self.config = config_loader.load_config()

            # 3. State Manager
            self.state = StateManager()
            self.state.set_state("idle")

            # 4. Voice System
            print(Fore.GREEN + "🎙️ Initializing Voice System..." + Style.RESET_ALL)
            self.wake_detector = WakeWordDetector(self.config)
            self.stt = STTEngine(self.config)
            self.tts = TTSEngine(self.config)

            # 5. Brain System
            print(Fore.GREEN + "🧠 Initializing Brain System..." + Style.RESET_ALL)
            self.intent_detector = IntentDetector(self.config)
            self.decision_engine = DecisionEngine(self.config)

            # 6. Emotion System
            print(Fore.GREEN + "❤️ Initializing Emotion System..." + Style.RESET_ALL)
            self.emotion_detector = EmotionDetector(self.config)

            # 7. Conversation System
            self.dialogue_manager = DialogueManager(self.config)

            # 8. Error Handler
            self.error_catcher = ErrorCatcher(self.config)

            # Test TTS
            self.tts.speak(
                "Jarvis initialization complete sir. I am ready to assist you."
            )

            self.logger.info("✅ JARVIS Initialization Complete")
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "✅ JARVIS READY TO ASSIST SIR!"
                + Style.RESET_ALL
            )

            return True

        except Exception as e:
            self.logger.error(f"❌ Initialization Failed: {str(e)}")
            print(Fore.RED + f"❌ Error during initialization: {str(e)}")
            traceback.print_exc()
            return False

    def main_loop(self):
        """🎯 Main JARVIS Loop: Wake → Listen → Think → Act"""
        self.is_running = True
        self.logger.info("🚀 Starting JARVIS Main Loop")

        print(
            Fore.CYAN
            + "\n🎯 JARVIS is now active. Say 'Jarvis' to wake me up!"
            + Style.RESET_ALL
        )

        try:
            while self.is_running:
                try:
                    # Step 1: Wake Word Detection
                    if self.wake_detector.detect():
                        self.on_wake_detected()

                    # Small delay to prevent CPU overuse
                    time.sleep(0.1)

                except KeyboardInterrupt:
                    self.logger.info("🛑 Keyboard Interrupt Received")
                    print(
                        Fore.YELLOW + "\n🛑 Shutting down JARVIS..." + Style.RESET_ALL
                    )
                    self.shutdown()
                    break

                except Exception as e:
                    self.error_catcher.handle_error(e, "main_loop")
                    time.sleep(1)  # Prevent tight error loop

        except Exception as e:
            self.logger.error(f"❌ Main Loop Crashed: {str(e)}")
            print(Fore.RED + f"❌ Critical Error: {str(e)}")
            traceback.print_exc()

    def on_wake_detected(self):
        """🎯 Handle wake word detection"""
        print(
            Fore.GREEN
            + "\n"
            + self.config["indicators"]["listening"]
            + " Wake word detected! Listening..."
            + Style.RESET_ALL
        )
        self.logger.info("👂 Wake word detected, starting listening")

        # Change state
        self.state.set_state("listening")

        # Give audio feedback
        self.tts.speak("Yes sir, I'm listening")

        # Listen for command
        command_text = self.stt.listen()

        if command_text:
            self.process_command(command_text)
        else:
            self.tts.speak("I couldn't hear you clearly sir, please try again")
            self.state.set_state("idle")

    def process_command(self, command_text):
        """🎯 Process user command"""
        try:
            print(Fore.CYAN + f"\n🗣️ You said: {command_text}" + Style.RESET_ALL)
            self.logger.info(f"📝 Command Received: {command_text}")

            # Update context
            self.current_context["last_command"] = command_text
            self.current_context["timestamp"] = datetime.now().isoformat()

            # Step 1: Emotion Detection
            emotion = self.emotion_detector.detect_emotion(command_text)
            self.current_context["emotion"] = emotion

            # Step 2: Intent Detection
            print(
                Fore.YELLOW
                + self.config["indicators"]["thinking"]
                + " Analyzing intent..."
                + Style.RESET_ALL
            )
            intent, entities = self.intent_detector.detect(command_text)

            # Step 3: Update Context
            self.current_context["intent"] = intent
            self.current_context["entities"] = entities

            # Step 4: Decision Making
            response = self.decision_engine.decide(
                intent, entities, self.current_context
            )

            # Step 5: Execute Action
            if response and response.get("action"):
                self.execute_action(response)

            # Step 6: Update Stats
            self.command_count += 1
            if response.get("success", False):
                self.success_count += 1

            # Step 7: Return to idle
            self.state.set_state("idle")

            # Step 8: Check for follow-up
            if self.dialogue_manager.expecting_followup():
                self.handle_followup()

        except Exception as e:
            self.error_catcher.handle_error(e, "process_command")
            self.tts.speak("Sorry sir, there was an error processing your command")
            self.state.set_state("idle")

    def execute_action(self, response):
        """🎯 Execute the decided action"""
        try:
            action = response["action"]
            params = response.get("params", {})

            print(Fore.GREEN + f"\n🚀 Executing: {action}" + Style.RESET_ALL)
            self.logger.info(f"⚡ Executing Action: {action}")

            # Import and execute skill module
            if action == "open_app":
                from skills.apps.open_app import OpenApp

                skill = OpenApp(self.config, self.tts)
                result = skill.execute(params)

            elif action == "open_website":
                from skills.web.url_opener import URLOpener

                skill = URLOpener(self.config, self.tts)
                result = skill.execute(params)

            elif action == "search_web":
                from skills.web.search import WebSearch

                skill = WebSearch(self.config, self.tts)
                result = skill.execute(params)

            elif action == "send_whatsapp":
                from skills.communication.whatsapp_controller import WhatsAppController

                skill = WhatsAppController(self.config, self.tts)
                result = skill.execute(params)

            elif action == "system_info":
                from core.system.system_info import SystemInfo

                skill = SystemInfo(self.config, self.tts)
                result = skill.execute(params)

            elif action == "control_window":
                from core.system.window_manager import WindowManager

                skill = WindowManager(self.config, self.tts)
                result = skill.execute(params)

            elif action == "play_music":
                from skills.media.play_music import PlayMusic

                skill = PlayMusic(self.config, self.tts)
                result = skill.execute(params)

            elif action == "code_assist":
                from skills.coding.code_writer import CodeWriter

                skill = CodeWriter(self.config, self.tts)
                result = skill.execute(params)

            else:
                # Use AI fallback for unknown actions
                from core.fallback.unknown_handler import UnknownHandler

                handler = UnknownHandler(self.config, self.tts)
                result = handler.handle_unknown_action(action, params)

            # Speak response if available
            if result.get("speak"):
                self.tts.speak(result["speak"])

            # Update memory
            self.update_memory(action, result)

        except Exception as e:
            self.error_catcher.handle_error(e, "execute_action")
            self.tts.speak("Sorry sir, I couldn't complete that action")

    def handle_followup(self):
        """🎯 Handle follow-up questions in conversation"""
        try:
            print(Fore.CYAN + "\n🗣️ Waiting for follow-up..." + Style.RESET_ALL)
            self.tts.speak("Yes sir, what next?")

            # Listen for follow-up
            followup_text = self.stt.listen()

            if followup_text:
                # Process in context
                contextual_command = self.dialogue_manager.add_context(followup_text)
                self.process_command(contextual_command)

        except Exception as e:
            self.error_catcher.handle_error(e, "handle_followup")

    def update_memory(self, action, result):
        """🎯 Update memory with action results"""
        try:
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "result": result.get("success", False),
                "details": result,
            }

            # Save to short-term memory
            from core.brain.memory_controller import MemoryController

            memory = MemoryController(self.config)
            memory.add_short_term(memory_entry)

        except Exception as e:
            self.logger.error(f"❌ Memory update failed: {str(e)}")

    def shutdown(self):
        """🎯 Gracefully shutdown JARVIS"""
        try:
            print(Fore.YELLOW + "\n🛑 Shutting down JARVIS..." + Style.RESET_ALL)
            self.logger.info("🔴 JARVIS Shutdown Initiated")

            # Calculate stats
            uptime = time.time() - self.start_time
            success_rate = (
                (self.success_count / self.command_count * 100)
                if self.command_count > 0
                else 0
            )

            # Speak goodbye
            goodbye_msg = f"Shutting down sir. I assisted with {self.command_count} commands today. Success rate: {success_rate:.1f} percent. Have a great day!"
            self.tts.speak(goodbye_msg)

            # Save state
            self.state.set_state("shutdown")

            # Cleanup
            self.is_running = False

            print(Fore.GREEN + f"\n📊 Session Stats:" + Style.RESET_ALL)
            print(Fore.GREEN + f"   Commands: {self.command_count}" + Style.RESET_ALL)
            print(
                Fore.GREEN + f"   Success Rate: {success_rate:.1f}%" + Style.RESET_ALL
            )
            print(Fore.GREEN + f"   Uptime: {uptime/60:.1f} minutes" + Style.RESET_ALL)
            print(Fore.CYAN + "\n👋 Goodbye Sir!" + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"❌ Error during shutdown: {str(e)}" + Style.RESET_ALL)
            self.logger.error(f"❌ Shutdown Error: {str(e)}")


def main():
    """🎯 Main Entry Point"""
    jarvis = JARVIS()

    if jarvis.initialize():
        jarvis.main_loop()
    else:
        print(
            Fore.RED
            + "❌ JARVIS failed to initialize. Please check the logs."
            + Style.RESET_ALL
        )
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
