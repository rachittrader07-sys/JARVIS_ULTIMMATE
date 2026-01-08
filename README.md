# 🎯 JARVIS - Advanced Desktop Voice Assistant

## Overview
JARVIS is an intelligent voice assistant designed for desktop automation with natural language understanding, emotion detection, and self-learning capabilities.

## Features
- 🎙️ **Voice Control**: Wake word detection, speech recognition, text-to-speech
- 🧠 **AI Brain**: DeepSeek AI integration via OpenRouter
- 📱 **WhatsApp Automation**: Send messages via WhatsApp Desktop
- 🌐 **Web Integration**: Open websites, search web, YouTube control
- 💻 **Coding Assistant**: Write code in multiple languages
- 🖥️ **System Control**: Open apps, system info, window management
- ❤️ **Emotion Detection**: Understand user mood from voice and text
- 🛠️ **Self-Healing**: Automatic error detection and recovery
- 🔒 **Security**: Voice authentication, permission control
- 📝 **Memory**: Learn from interactions, custom commands

## Installation

### Windows
1. Clone the repository
2. Run `setup.bat`
3. Configure `config.yaml` with your OpenRouter API key
4. Run `python jarvis.py`

### Manual Installation
```bash
# Install Python 3.8+
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir voice_profile memory logs

# Run JARVIS
python jarvis.py