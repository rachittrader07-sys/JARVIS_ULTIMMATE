"""
❓ Unknown Command Handler
Handles unknown commands using AI reasoning
"""

import requests
import json
import re
from colorama import Fore, Style

class UnknownHandler:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.openrouter_config = config['jarvis']['openrouter']
        
    def handle_unknown_action(self, action, params):
        """❓ Handle unknown action using AI"""
        print(Fore.YELLOW + "🤔 Handling unknown action with AI..." + Style.RESET_ALL)
        
        # Try to understand the action using AI
        ai_response = self.query_openrouter(action, params)
        
        if ai_response:
            return self.execute_ai_suggestion(ai_response)
        else:
            return self.fallback_to_basic(action, params)
    
    def query_openrouter(self, action, params):
        """❓ Query OpenRouter AI for understanding"""
        api_key = self.openrouter_config['api_key']
        
        if not api_key:
            print(Fore.RED + "❌ No OpenRouter API key configured" + Style.RESET_ALL)
            return None
        
        try:
            # Prepare prompt
            prompt = self.create_prompt(action, params)
            
            # Make request to OpenRouter
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.openrouter_config['model'],
                "messages": [
                    {
                        "role": "system",
                        "content": "You are JARVIS, an AI assistant. Help understand what the user wants and suggest appropriate actions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                self.openrouter_config['endpoint'],
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_text = result['choices'][0]['message']['content']
                print(Fore.GREEN + f"✅ AI Response: {ai_text[:100]}..." + Style.RESET_ALL)
                return ai_text
            else:
                print(Fore.RED + f"❌ AI request failed: {response.status_code}" + Style.RESET_ALL)
                return None
                
        except Exception as e:
            print(Fore.RED + f"❌ AI query error: {str(e)}" + Style.RESET_ALL)
            return None
    
    @staticmethod
    def create_prompt(action, params):
        """❓ Create prompt for AI"""
        prompt = f"""
        User command/action: {action}
        Parameters: {json.dumps(params)}
        
        Please analyze what the user wants and suggest:
        1. What is the user trying to do?
        2. Which JARVIS skill should be used?
        3. What parameters should be passed?
        4. Any safety considerations?
        
        Respond in JSON format:
        {{
            "understanding": "brief understanding",
            "suggested_action": "action_name",
            "suggested_params": {{}},
            "confidence": 0.0-1.0,
            "safety_warning": "optional",
            "response_to_user": "what to say to user"
        }}
        """
        
        return prompt
    
    def execute_ai_suggestion(self, ai_text):
        """❓ Execute AI suggestion"""
        try:
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if json_match:
                suggestion = json.loads(json_match.group())
                
                # Extract components
                understanding = suggestion.get('understanding', '')
                action = suggestion.get('suggested_action', '')
                params = suggestion.get('suggested_params', {})
                confidence = suggestion.get('confidence', 0.5)
                response = suggestion.get('response_to_user', '')
                warning = suggestion.get('safety_warning', '')
                
                # Speak AI's response
                if response:
                    self.tts.speak(response)
                
                # If confidence is high, execute
                if confidence > 0.7 and action:
                    return {
                        'success': True,
                        'action': action,
                        'params': params,
                        'ai_understanding': understanding,
                        'confidence': confidence
                    }
                else:
                    # Ask for clarification
                    clarification = f"I think you want {understanding}. Can you please clarify?"
                    self.tts.speak(clarification)
                    return {
                        'success': False,
                        'needs_clarification': True,
                        'message': clarification
                    }
            
            return {
                'success': False,
                'error': 'Could not parse AI response'
            }
            
        except Exception as e:
            print(Fore.RED + f"❌ AI execution error: {str(e)}" + Style.RESET_ALL)
            return self.fallback_to_basic("", {})
    
    def fallback_to_basic(self, action, params):
        """❓ Fallback to basic handling"""
        # Try to extract intent from action string
        action_lower = str(action).lower()
        
        if any(word in action_lower for word in ['open', 'start', 'launch']):
            # Probably trying to open something
            # Extract what to open
            words = action_lower.split()
            for i, word in enumerate(words):
                if word in ['open', 'start', 'launch'] and i + 1 < len(words):
                    target = words[i + 1]
                    
                    # Check if it's a website
                    if any(web in target for web in ['.com', '.in', '.org', 'website']):
                        return {
                            'success': True,
                            'action': 'open_website',
                            'params': {'website_name': target},
                            'fallback': True
                        }
                    else:
                        # Probably an app
                        return {
                            'success': True,
                            'action': 'open_app',
                            'params': {'app_name': target},
                            'fallback': True
                        }
        
        elif any(word in action_lower for word in ['search', 'find', 'google']):
            # Probably trying to search
            return {
                'success': True,
                'action': 'search_web',
                'params': {'query': action_lower},
                'fallback': True
            }
        
        elif any(word in action_lower for word in ['message', 'whatsapp', 'send']):
            # Probably trying to send message
            return {
                'success': True,
                'action': 'send_whatsapp',
                'params': {'person': 'unknown', 'message': action_lower},
                'fallback': True
            }
        
        # Default fallback
        self.tts.speak("Sir, I didn't understand that command. Can you please rephrase?")
        return {
            'success': False,
            'error': 'Unknown command',
            'message': 'Please rephrase'
        }