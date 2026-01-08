"""
🤖 LLM Reasoner
Uses AI for complex reasoning and problem solving
"""

import json
import re

import requests
from colorama import Fore, Style


class LLMReasoner:
    def __init__(self, config):
        self.config = config
        self.openrouter_config = config["jarvis"]["openrouter"]
        self.api_key = self.openrouter_config.get("api_key", "")
        self.model = self.openrouter_config.get("model", "deepseek/deepseek-r1:free")
        self.endpoint = self.openrouter_config.get(
            "endpoint", "https://openrouter.ai/api/v1/chat/completions"
        )

        # Cache for common queries
        self.response_cache = {}
        self.max_cache_size = 100

        print(Fore.GREEN + "🤖 LLM Reasoner Initialized" + Style.RESET_ALL)

    def reason(self, query, context=None, max_tokens=500):
        """🤖 Use AI for reasoning"""
        if not self.api_key:
            print(Fore.RED + "❌ No API key configured for LLM" + Style.RESET_ALL)
            return self.fallback_reasoning(query, context)

        # Check cache first
        cache_key = f"{query}:{str(context)}"
        if cache_key in self.response_cache:
            print(Fore.CYAN + "🤖 Using cached response" + Style.RESET_ALL)
            return self.response_cache[cache_key]

        try:
            print(Fore.YELLOW + "🤖 Thinking with AI..." + Style.RESET_ALL)

            # Prepare prompt
            prompt = self.prepare_prompt(query, context)

            # Make API request
            response = self.make_api_request(prompt, max_tokens)

            if response:
                # Cache the response
                self.cache_response(cache_key, response)
                return response
            else:
                return self.fallback_reasoning(query, context)

        except Exception as e:
            print(Fore.RED + f"❌ LLM reasoning error: {str(e)}" + Style.RESET_ALL)
            return self.fallback_reasoning(query, context)

    def prepare_prompt(self, query, context):
        """🤖 Prepare prompt for AI"""
        system_prompt = """You are JARVIS, an advanced AI assistant. Your task is to help the user by:
1. Understanding their intent from natural language
2. Providing accurate and helpful responses
3. Suggesting appropriate actions
4. Being respectful and professional

You speak in Hinglish (Hindi + English mix) and address the user as "Sir".

Important guidelines:
- Keep responses concise but informative
- If suggesting an action, explain why
- If unsure, ask for clarification
- Always maintain security and privacy
- Be empathetic and understanding"""

        user_prompt = f"User query: {query}\n"

        if context:
            user_prompt += f"Context: {context}\n"

        user_prompt += (
            "\nPlease provide a helpful response and suggest what JARVIS should do."
        )

        return {"system": system_prompt, "user": user_prompt}

    def make_api_request(self, prompt, max_tokens):
        """🤖 Make API request to OpenRouter"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://jarvis-assistant.com",
                "X-Title": "JARVIS Assistant",
            }

            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
            }

            response = requests.post(
                self.endpoint, headers=headers, json=data, timeout=15
            )

            if response.status_code == 200:
                result = response.json()
                ai_text = result["choices"][0]["message"]["content"]

                # Clean up response
                cleaned_response = self.clean_ai_response(ai_text)

                print(
                    Fore.GREEN
                    + f"🤖 AI Response: {cleaned_response[:100]}..."
                    + Style.RESET_ALL
                )
                return cleaned_response
            else:
                print(
                    Fore.RED
                    + f"❌ API request failed: {response.status_code}"
                    + Style.RESET_ALL
                )
                return None

        except requests.exceptions.Timeout:
            print(Fore.RED + "❌ API request timeout" + Style.RESET_ALL)
            return None
        except Exception as e:
            print(Fore.RED + f"❌ API request error: {str(e)}" + Style.RESET_ALL)
            return None

    def clean_ai_response(self, text):
        """🤖 Clean AI response"""
        # Remove markdown formatting
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove **bold**
        text = re.sub(r"\*(.*?)\*", r"\1", text)  # Remove *italic*
        text = re.sub(r"`(.*?)`", r"\1", text)  # Remove `code`

        # Remove excessive newlines
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # Trim whitespace
        text = text.strip()

        return text

    def cache_response(self, key, response):
        """🤖 Cache response"""
        self.response_cache[key] = response

        # Limit cache size
        if len(self.response_cache) > self.max_cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.response_cache))
            del self.response_cache[oldest_key]

    def fallback_reasoning(self, query, context):
        """🤖 Fallback reasoning when AI is unavailable"""
        query_lower = query.lower()

        # Simple pattern matching for common queries
        if any(word in query_lower for word in ["what", "kya", "kaise", "kaun"]):
            # Question type
            if "time" in query_lower or "samay" in query_lower:
                from datetime import datetime

                current_time = datetime.now().strftime("%I:%M %p")
                return f"Sir, abhi time hai {current_time}"

            elif "date" in query_lower or "tareekh" in query_lower:
                from datetime import datetime

                current_date = datetime.now().strftime("%d %B, %Y")
                return f"Sir, aaj ki date hai {current_date}"

            elif "weather" in query_lower or "mausam" in query_lower:
                return "Sir, weather ke liye internet connection chahiye. Kya main check karun?"

            else:
                return "Sir, main is sawal ka jawab dene ke liye AI ki help leta hoon, lekin abhi connection nahi hai. Aap kuch aur pooch sakte hain."

        elif any(
            word in query_lower for word in ["how to", "kaise kare", "kaise karna"]
        ):
            # How-to question
            topic = self.extract_topic(query)
            return f"Sir, {topic} ke baare mein main aapko step-by-step guide de sakta hoon. Kya aap specific details de sakte hain?"

        elif any(word in query_lower for word in ["why", "kyun", "kya wajah"]):
            # Why question
            return "Sir, iska exact reason samajhne ke liye thoda research chahiye. Kya main ispe kuch information dhundhu?"

        elif any(word in query_lower for word in ["tell me", "batao", "bataye"]):
            # Tell me something
            topic = self.extract_topic(query)
            return f"Sir, {topic} ke baare mein kuch interesting facts hain. Kya main aapko batayun?"

        # Default response
        return "Sir, main aapki baat samajh gaya hoon lekin iska best jawab dene ke liye AI ki zaroorat hai. Kya main kuch aur help kar sakta hoon?"

    def extract_topic(self, query):
        """🤖 Extract topic from query"""
        # Remove common question words
        words = [
            "what",
            "how",
            "why",
            "when",
            "where",
            "who",
            "tell",
            "me",
            "about",
            "kya",
            "kaise",
            "kyun",
            "kab",
            "kahan",
            "kaun",
        ]
        query_words = query.lower().split()

        # Filter out question words
        topic_words = [word for word in query_words if word not in words]

        if topic_words:
            return " ".join(topic_words[:3])
        else:
            return "ye topic"

    def analyze_sentiment(self, text):
        """🤖 Analyze sentiment using AI"""
        if not self.api_key:
            return "neutral"

        try:
            prompt = {
                "system": "You are a sentiment analyzer. Analyze the sentiment of the given text and return ONLY one word: positive, negative, neutral, happy, sad, angry, excited, or calm.",
                "user": f"Text to analyze: {text}",
            }

            response = self.make_api_request(prompt, max_tokens=10)
            if response:
                # Extract sentiment from response
                sentiment_words = [
                    "positive",
                    "negative",
                    "neutral",
                    "happy",
                    "sad",
                    "angry",
                    "excited",
                    "calm",
                ]
                for word in sentiment_words:
                    if word in response.lower():
                        return word

            return "neutral"

        except:
            return "neutral"

    def summarize_text(self, text, max_length=200):
        """🤖 Summarize text using AI"""
        if not self.api_key:
            return text[:max_length] + "..." if len(text) > max_length else text

        try:
            prompt = {
                "system": "You are a text summarizer. Summarize the given text concisely in Hinglish (Hindi+English). Keep it short and clear.",
                "user": f"Text to summarize: {text}",
            }

            response = self.make_api_request(prompt, max_tokens=150)
            return response if response else text[:max_length] + "..."

        except:
            return text[:max_length] + "..." if len(text) > max_length else text

    def translate_text(self, text, target_language="hindi"):
        """🤖 Translate text using AI"""
        if not self.api_key:
            return text

        try:
            prompt = {
                "system": f"You are a translator. Translate the given text to {target_language} while keeping the meaning accurate.",
                "user": f"Text to translate: {text}",
            }

            response = self.make_api_request(prompt, max_tokens=200)
            return response if response else text

        except:
            return text

    def generate_response_for_unknown(self, user_input, context):
        """🤖 Generate response for unknown commands"""
        prompt = {
            "system": "You are JARVIS. The user gave a command you don't understand. Generate a helpful response asking for clarification or suggesting alternatives.",
            "user": f"User command: {user_input}\nContext: {context}\nGenerate a helpful response in Hinglish.",
        }

        response = self.reason(json.dumps(prompt), max_tokens=100)
        return (
            response
            if response
            else "Sir, main ye command samajh nahi paya. Kya aap dobara bata sakte hain?"
        )

    def get_cache_stats(self):
        """🤖 Get cache statistics"""
        return {
            "cache_size": len(self.response_cache),
            "cache_hits": 0,  # Would track in production
            "cache_misses": 0,
        }

    def clear_cache(self):
        """🤖 Clear response cache"""
        self.response_cache = {}
        print(Fore.GREEN + "🤖 Response cache cleared" + Style.RESET_ALL)
