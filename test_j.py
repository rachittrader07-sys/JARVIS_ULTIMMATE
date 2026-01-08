"""
🧪 Test Script for JARVIS
Tests all major components
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init

from core.bootstrap import SystemBootstrap
from core.brain.intent_detector import IntentDetector
from core.config_loader import ConfigLoader
from core.emotion.emotion_detector import EmotionDetector
from core.voice.tts_engine import TTSEngine

init(autoreset=True)


def print_test_result(test_name, success):
    """🧪 Print test result"""
    if success:
        print(Fore.GREEN + f"✅ {test_name}: PASSED" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ {test_name}: FAILED" + Style.RESET_ALL)
    return success


def test_system_bootstrap():
    """🧪 Test system bootstrap"""
    try:
        bootstrap = SystemBootstrap()
        bootstrap.run_checks()
        return True
    except:
        return False


def test_config_loader():
    """🧪 Test config loader"""
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        return config is not None
    except:
        return False


def test_tts():
    """🧪 Test TTS engine"""
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        tts = TTSEngine(config)
        return tts.engine is not None
    except:
        return False


def test_intent_detector():
    """🧪 Test intent detector"""
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        detector = IntentDetector(config)

        # Test some commands
        test_commands = [
            "open chrome",
            "search python tutorial",
            "whatsapp rahul ko message bhejo",
            "system battery kitna hai",
        ]

        for cmd in test_commands:
            intent, entities = detector.detect(cmd)
            if intent == "unknown":
                return False

        return True
    except:
        return False


def test_emotion_detector():
    """🧪 Test emotion detector"""
    try:
        loader = ConfigLoader()
        config = loader.load_config()
        detector = EmotionDetector(config)

        test_texts = [
            "I am very happy today!",
            "This is so frustrating",
            "Please help me",
            "Thank you so much",
        ]

        for text in test_texts:
            emotion = detector.detect_emotion(text)
            if not emotion:
                return False

        return True
    except:
        return False


def run_all_tests():
    """🧪 Run all tests"""
    print(Fore.CYAN + "\n" + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "🧪 RUNNING JARVIS TESTS" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

    tests = [
        ("System Bootstrap", test_system_bootstrap),
        ("Config Loader", test_config_loader),
        ("TTS Engine", test_tts),
        ("Intent Detector", test_intent_detector),
        ("Emotion Detector", test_emotion_detector),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        success = test_func()
        print_test_result(test_name, success)
        if success:
            passed += 1

    print(Fore.CYAN + "\n" + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + f"🧪 TEST RESULTS: {passed}/{total} passed" + Style.RESET_ALL)

    if passed == total:
        print(Fore.GREEN + "🎉 All tests passed! JARVIS is ready." + Style.RESET_ALL)
    else:
        print(
            Fore.YELLOW
            + f"⚠️ {total - passed} tests failed. Check the logs."
            + Style.RESET_ALL
        )

    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
