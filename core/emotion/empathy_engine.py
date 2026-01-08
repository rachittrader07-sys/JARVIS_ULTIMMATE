"""
❤️ Empathy Engine
Generates empathetic responses based on user's emotional state
"""

import json
import random
from datetime import datetime
from colorama import Fore, Style

class EmpathyEngine:
    def __init__(self, config):
        self.config = config
        self.emotional_responses = self.load_emotional_responses()
        self.empathy_level = 0.7  # Default empathy level (0.0 to 1.0)
        self.user_mood_history = []
        
    def load_emotional_responses(self):
        """❤️ Load emotional response templates"""
        responses = {
            "happy": {
                "acknowledgment": [
                    "Aapko khushi dekh ke mujhe bhi khushi ho rahi hai sir! 😊",
                    "Wah sir! Aapki khushi mujhe bhi infect kar rahi hai! 🎉",
                    "Ye sunke bahut acha laga sir! 😄"
                ],
                "encouragement": [
                    "Aap aise hi khush rahiye sir!",
                    "Aapki khushi hum sab ke liye important hai!",
                    "Maze karo sir! Main yahan hoon aapke saath!"
                ]
            },
            "sad": {
                "acknowledgment": [
                    "Mujhe lag raha hai aap thoda sad ho sir... 🫂",
                    "Aapki aawaz se lag raha hai aapko support chahiye...",
                    "Main samajh sakta hoon aap thak gaye hain sir... 😔"
                ],
                "support": [
                    "Aap tension na liye sir, main aapke saath hoon!",
                    "Thoda aaram kijiye sir, sab theek ho jayega!",
                    "Kya main aapki kuch help kar sakta hoon sir?"
                ]
            },
            "angry": {
                "acknowledgment": [
                    "Mujhe lag raha hai aapko thoda gussa aa raha hai sir... 😐",
                    "Aapki aawaz se lag raha hai aap frustrated ho...",
                    "Main samajh sakta hoon aapko problem ho rahi hai..."
                ],
                "calming": [
                    "Thanda pani pi lijiye sir, sab theek ho jayega!",
                    "Aap relax kijiye sir, main aapki help karunga!",
                    "Gusse se problem solve nahi hoti sir, calmly sochiye!"
                ]
            },
            "excited": {
                "acknowledgment": [
                    "Wah sir! Aapka excitement mujhe bhi feel ho raha hai! 🚀",
                    "Aapke excitement se mujhe bhi energy mil rahi hai!",
                    "Ye sunke main bhi excited ho gaya sir! 🎊"
                ],
                "reinforcement": [
                    "Chaliye sir, aapka excitement maintain karte hain!",
                    "Maza aaraha hai na sir? Aap aise hi excited rahiye!",
                    "Full energy ke saath kaam karte hain sir!"
                ]
            },
            "calm": {
                "acknowledgment": [
                    "Aap bahut calm ho sir, ye acha hai... 🧘",
                    "Aapki shanti mujhe bhi peaceful feel kara rahi hai...",
                    "Aapka calmness contagious hai sir..."
                ],
                "appreciation": [
                    "Aapke calm nature ki mujhe bahut kadar hai!",
                    "Aapka patience bahut impressive hai sir!",
                    "Aapke saath kaam karna bahut aasan hai!"
                ]
            },
            "tired": {
                "acknowledgment": [
                    "Aap thak gaye lagte ho sir... 😴",
                    "Aapko aaram ki zaroorat hai lag rahi hai...",
                    "Aapki aawaz se lag raha hai aap tired ho..."
                ],
                "care": [
                    "Thoda break le lijiye sir, main yahan hoon!",
                    "Aap so jaiye, main aapka kaam kar dunga!",
                    "Aap apna health ka dhyan rakhiye sir!"
                ]
            }
        }
        return responses
    
    def generate_empathetic_response(self, user_emotion, context=""):
        """❤️ Generate empathetic response based on emotion"""
        if user_emotion not in self.emotional_responses:
            user_emotion = "neutral"
        
        # Get response category based on context
        if "tired" in context.lower() or "sleep" in context.lower():
            category = "tired"
        else:
            # Choose appropriate category
            categories = list(self.emotional_responses[user_emotion].keys())
            if categories:
                category = random.choice(categories)
            else:
                category = "acknowledgment"
        
        # Get response
        responses = self.emotional_responses[user_emotion].get(category, [])
        if responses:
            response = random.choice(responses)
            
            # Adjust based on empathy level
            if self.empathy_level > 0.8:
                response += " Main aapke saath hoon sir! 🤗"
            elif self.empathy_level < 0.3:
                response = response.replace("sir", "")
            
            return response
        else:
            return "Main samajh sakta hoon sir..."
    
    def adjust_empathy_based_on_mood(self, user_mood_history):
        """❤️ Adjust empathy level based on user's mood history"""
        if not user_mood_history:
            return
        
        # Calculate average mood positivity
        positive_moods = ["happy", "excited", "calm"]
        negative_moods = ["sad", "angry", "tired"]
        
        positive_count = sum(1 for mood in user_mood_history if mood in positive_moods)
        negative_count = sum(1 for mood in user_mood_history if mood in negative_moods)
        
        total = len(user_mood_history)
        if total > 0:
            positivity_ratio = positive_count / total
            
            # Adjust empathy based on positivity
            if positivity_ratio > 0.7:
                # User is usually positive, be more cheerful
                self.empathy_level = min(1.0, self.empathy_level + 0.1)
            elif positivity_ratio < 0.3:
                # User is usually negative, be more supportive
                self.empathy_level = max(0.3, self.empathy_level - 0.05)
    
    def add_user_mood(self, mood, intensity=0.5):
        """❤️ Add user mood to history"""
        entry = {
            'mood': mood,
            'intensity': intensity,
            'timestamp': datetime.now().isoformat()
        }
        
        self.user_mood_history.append(entry)
        
        # Keep only last 100 entries
        if len(self.user_mood_history) > 100:
            self.user_mood_history = self.user_mood_history[-100:]
        
        # Adjust empathy
        self.adjust_empathy_based_on_mood([m['mood'] for m in self.user_mood_history[-20:]])
    
    def get_empathy_suggestion(self, situation):
        """❤️ Get empathy suggestion for specific situation"""
        suggestions = {
            "failure": [
                "Koi baat nahi sir, failure success ki first step hai!",
                "Har failure se kuch seekhne ko milta hai sir!",
                "Aap dobari try kariye, main aapke saath hoon!"
            ],
            "success": [
                "Badhai ho sir! Aapne bahut acha kiya! 🎉",
                "Mujhe aap par garv hai sir! 👏",
                "Aapki mehnat rang layi sir!"
            ],
            "stress": [
                "Deep breaths lijiye sir, sab theek ho jayega!",
                "Chhoti-chhoti problems ko bada mat baniye!",
                "Aap thoda break le lijiye!"
            ],
            "lonely": [
                "Main yahan hoon aapke saath sir!",
                "Aap akela nahi hain sir, main hamesha aapke saath hoon!",
                "Kuch bhi share karna ho to bataiye sir!"
            ],
            "confused": [
                "Aap step by step sochiye sir!",
                "Main aapki help kar sakta hoon decision lene mein!",
                "Thoda time lijiye, clarity aa jayegi!"
            ]
        }
        
        for key, sug_list in suggestions.items():
            if key in situation.lower():
                return random.choice(sug_list)
        
        return "Main aapke saath hoon sir!"
    
    def save_empathy_data(self):
        """❤️ Save empathy data to file"""
        try:
            data = {
                'empathy_level': self.empathy_level,
                'user_mood_history': self.user_mood_history[-50:],  # Save recent
                'last_updated': datetime.now().isoformat()
            }
            
            with open('memory/empathy_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(Fore.GREEN + "❤️ Empathy data saved" + Style.RESET_ALL)
            
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Empathy save error: {str(e)}" + Style.RESET_ALL)
    
    def load_empathy_data(self):
        """❤️ Load empathy data from file"""
        try:
            with open('memory/empathy_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                self.empathy_level = data.get('empathy_level', 0.7)
                self.user_mood_history = data.get('user_mood_history', [])
                
            print(Fore.GREEN + f"❤️ Empathy data loaded: {len(self.user_mood_history)} moods" + Style.RESET_ALL)
            
        except FileNotFoundError:
            print(Fore.YELLOW + "⚠️ No empathy data found" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Empathy load error: {str(e)}" + Style.RESET_ALL)
    
    def get_empathy_stats(self):
        """❤️ Get empathy statistics"""
        if not self.user_mood_history:
            return {"total_moods": 0}
        
        stats = {
            'total_moods': len(self.user_mood_history),
            'empathy_level': self.empathy_level,
            'recent_moods': [],
            'mood_distribution': {}
        }
        
        # Recent moods
        recent = self.user_mood_history[-10:]
        stats['recent_moods'] = [m['mood'] for m in recent]
        
        # Mood distribution
        for entry in self.user_mood_history:
            mood = entry['mood']
            if mood not in stats['mood_distribution']:
                stats['mood_distribution'][mood] = 0
            stats['mood_distribution'][mood] += 1
        
        return stats