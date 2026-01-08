"""
✅ Confirmation Engine
Handles user confirmation for critical actions
"""

import re
from colorama import Fore, Style
from datetime import datetime

class ConfirmationEngine:
    def __init__(self, config, tts, stt):
        self.config = config
        self.tts = tts
        self.stt = stt
        self.confirmation_history = []
        
    def execute(self, params):
        """✅ Execute confirmation request"""
        message = params.get('message', '')
        action = params.get('action', '')
        timeout = params.get('timeout', 10)
        require_explicit = params.get('require_explicit', True)
        
        if not message:
            self.tts.speak("Sir, what should I confirm?")
            return {
                'success': False,
                'error': 'No confirmation message provided'
            }
        
        print(Fore.YELLOW + f"✅ Confirmation: {message}" + Style.RESET_ALL)
        
        # Ask for confirmation
        result = self.ask_confirmation(message, timeout, require_explicit)
        
        # Log the confirmation attempt
        self.confirmation_history.append({
            'timestamp': datetime.now(),
            'message': message,
            'action': action,
            'result': result['success'],
            'user_response': result.get('user_response', '')
        })
        
        if result['success']:
            self.tts.speak("Confirmed sir, proceeding with the action.")
        else:
            self.tts.speak("Action cancelled sir.")
            
        return result
    
    def ask_confirmation(self, message, timeout=10, require_explicit=True):
        """✅ Ask user for confirmation"""
        try:
            # Speak the confirmation message
            self.tts.speak(message)
            
            # Listen for response
            print(Fore.CYAN + "🎤 Listening for confirmation (say YES or NO)..." + Style.RESET_ALL)
            
            # Get speech input
            response = self.stt.listen(timeout=timeout)
            
            if not response:
                return {
                    'success': False,
                    'error': 'No response received',
                    'timeout': True
                }
            
            print(Fore.GREEN + f"👤 User: {response}" + Style.RESET_ALL)
            
            # Analyze response for confirmation
            is_confirmed = self.analyze_response(response, require_explicit)
            
            return {
                'success': is_confirmed,
                'user_response': response,
                'confidence': self.get_confidence_score(response),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def analyze_response(self, response, require_explicit=True):
        """✅ Analyze user response for confirmation"""
        response_lower = response.lower().strip()
        
        # Explicit confirmation patterns
        yes_patterns = [
            r'\byes\b', r'\byeah\b', r'\byep\b', r'\byup\b', r'\bsure\b',
            r'\bok\b', r'\bokay\b', r'\bconfirm\b', r'\bproceed\b',
            r'\bgo ahead\b', r'\bdo it\b', r'\bplease do\b', r'\byes please\b',
            r'\baffirmative\b', r'\broger\b', r'\bcopy\b', r'\bapproved\b'
        ]
        
        # Implicit confirmation patterns (when require_explicit is False)
        implicit_yes = [
            r'\bfine\b', r'\balright\b', r'\bgood\b', r'\bperfect\b',
            r'\bcontinue\b', r'\bcarry on\b', r'\bcarry out\b'
        ]
        
        # Negative patterns
        no_patterns = [
            r'\bno\b', r'\bnope\b', r'\bnah\b', r'\bstop\b', r'\bcancel\b',
            r'\bdon\'t\b', r'\bdo not\b', r'\babort\b', r'\bnegative\b',
            r'\bwait\b', r'\bhold on\b', r'\bnot now\b', r'\blater\b'
        ]
        
        # Check for explicit yes
        yes_score = 0
        for pattern in yes_patterns:
            if re.search(pattern, response_lower):
                yes_score += 1
        
        # Check for implicit yes (only if explicit not required)
        if not require_explicit:
            for pattern in implicit_yes:
                if re.search(pattern, response_lower):
                    yes_score += 0.5
        
        # Check for no
        no_score = 0
        for pattern in no_patterns:
            if re.search(pattern, response_lower):
                no_score += 1
        
        # Determine result
        if yes_score > no_score:
            return True
        elif no_score > yes_score:
            return False
        else:
            # Tie or unclear response - ask again
            return False
    
    def get_confidence_score(self, response):
        """✅ Get confidence score for response analysis"""
        response_lower = response.lower()
        
        # Strong confirmation indicators
        strong_yes = ['yes', 'yeah', 'yep', 'yup', 'sure', 'confirm', 'proceed']
        strong_no = ['no', 'nope', 'nah', 'cancel', 'abort', 'stop']
        
        # Check for strong indicators
        for word in strong_yes:
            if word in response_lower:
                return 0.9
        
        for word in strong_no:
            if word in response_lower:
                return 0.9
        
        # Check for weak indicators
        weak_yes = ['maybe', 'perhaps', 'could be', 'might']
        weak_no = ['not sure', 'not certain', 'doubt']
        
        for phrase in weak_yes:
            if phrase in response_lower:
                return 0.5
        
        for phrase in weak_no:
            if phrase in response_lower:
                return 0.5
        
        # Default confidence
        return 0.7
    
    def require_confirmation(self, action_type, sensitivity_level='medium'):
        """✅ Determine if confirmation is required for an action"""
        # Critical actions always require confirmation
        critical_actions = [
            'delete', 'remove', 'uninstall', 'format', 'wipe',
            'shutdown', 'restart', 'reboot', 'power off',
            'send_email', 'send_message', 'post', 'publish',
            'purchase', 'buy', 'order', 'pay',
            'install', 'update', 'upgrade'
        ]
        
        # Check if action is critical
        for action in critical_actions:
            if action in action_type.lower():
                return True
        
        # Sensitivity-based confirmation
        sensitivity_map = {
            'high': True,  # Always confirm
            'medium': self.config.get('confirm_medium_risk', True),
            'low': self.config.get('confirm_low_risk', False),
            'none': False  # Never confirm
        }
        
        return sensitivity_map.get(sensitivity_level, True)
    
    def get_history(self, limit=10):
        """✅ Get confirmation history"""
        return self.confirmation_history[-limit:] if self.confirmation_history else []
    
    def clear_history(self):
        """✅ Clear confirmation history"""
        self.confirmation_history.clear()
        return {
            'success': True,
            'message': 'Confirmation history cleared'
        }