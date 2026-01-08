"""
🎯 Entity Extractor
Extracts entities (names, numbers, dates) from commands
"""

import re
import json
from datetime import datetime

class EntityExtractor:
    def __init__(self, config):
        self.config = config
        self.entity_patterns = self.load_patterns()
        
    @staticmethod
    def load_patterns():
        """🎯 Load entity extraction patterns"""
        patterns = {
            'person_name': [
                r'(\b[A-Z][a-z]+\b)',  # Capitalized names
                r'(\b(?:mr\.?|mrs\.?|ms\.?|dr\.?)\s+[A-Z][a-z]+\b)',  # Titles
            ],
            'number': [
                r'(\d+)',  # Digits
                r'(\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b)',  # Words
            ],
            'time': [
                r'(\d{1,2}:\d{2})',  # HH:MM
                r'(\d{1,2}\s*(?:am|pm|AM|PM))',  # 10 am
            ],
            'date': [
                r'(\d{1,2}/\d{1,2}/\d{4})',  # DD/MM/YYYY
                r'(\d{1,2}-\d{1,2}-\d{4})',  # DD-MM-YYYY
            ],
            'website': [
                r'(\b(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b)',  # URLs
            ],
            'email': [
                r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',  # Emails
            ],
        }
        return patterns
    
    def extract(self, text, entity_type=None):
        """🎯 Extract entities from text"""
        text = str(text).lower()
        entities = {}
        
        if entity_type:
            # Extract specific entity type
            if entity_type in self.entity_patterns:
                entities[entity_type] = []
                for pattern in self.entity_patterns[entity_type]:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    entities[entity_type].extend(matches)
        else:
            # Extract all entity types
            for etype, patterns in self.entity_patterns.items():
                entities[etype] = []
                for pattern in patterns:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    entities[etype].extend(matches)
        
        # Remove duplicates
        for etype in entities:
            entities[etype] = list(set(entities[etype]))
            
        return entities
    
    @staticmethod
    def extract_app_name(command_text):
        """🎯 Extract app name from command"""
        patterns = [
            r'open\s+(.+?)\s+(?:app|application)',
            r'open\s+(.+)',
            r'start\s+(.+)',
            r'launch\s+(.+)',
            r'run\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_text.lower())
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def extract_website_name(command_text):
        """🎯 Extract website name from command"""
        patterns = [
            r'open\s+(.+?)\s+website',
            r'go to\s+(.+)',
            r'navigate to\s+(.+)',
            r'visit\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_text.lower())
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def extract_search_query(command_text):
        """🎯 Extract search query from command"""
        patterns = [
            r'search\s+(.+)',
            r'google\s+(.+)',
            r'find\s+(.+)',
            r'look up\s+(.+)',
            r'dhundho\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_text.lower())
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def extract_person_name(command_text):
        """🎯 Extract person name from command"""
        patterns = [
            r'to\s+(.+)',
            r'for\s+(.+)',
            r'(.+?)\s+ko',
            r'(.+?)\s+ke liye',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_text.lower())
            if match:
                name = match.group(1).strip()
                # Remove common words
                name = re.sub(r'\b(message|send|whatsapp|text|email)\b', '', name).strip()
                if name:
                    return name
        
        return None
    
    @staticmethod
    def extract_message_content(command_text):
        """🎯 Extract message content from command"""
        patterns = [
            r'message\s+(.+)',
            r'send\s+(.+)',
            r'bol do\s+(.+)',
            r'likh do\s+(.+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command_text.lower())
            if match:
                return match.group(1).strip()
        
        return None