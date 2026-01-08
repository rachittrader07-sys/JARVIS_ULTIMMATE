"""
📝 Logging Utility
Handles all logging for JARVIS
"""

import logging
import os
from datetime import datetime

from colorama import Fore, Style


def setup_logger():
    """📝 Setup comprehensive logger"""
    # Create logs directory if not exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/jarvis_{timestamp}.log"

    # Configure logger
    logger = logging.getLogger("JARVIS")
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_command(user_text, jarvis_response, success=True):
    """📝 Log a command interaction"""
    logger = logging.getLogger("JARVIS")

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_text,
        "jarvis": jarvis_response,
        "success": success,
    }

    logger.info(f"COMMAND: {user_text} -> {jarris_response}")


def log_error(error, context=""):
    """📝 Log an error"""
    logger = logging.getLogger("JARVIS")
    logger.error(f"ERROR in {context}: {str(error)}")


def log_system_event(event, details=""):
    """📝 Log a system event"""
    logger = logging.getLogger("JARVIS")
    logger.info(f"SYSTEM: {event} - {details}")
