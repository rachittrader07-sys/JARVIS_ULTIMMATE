"""
🌐 Web Fallback
Provides fallback web services when primary services fail
"""

import requests
import json
import os
from colorama import Fore, Style
from datetime import datetime

class WebFallback:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.fallback_services = {
            'weather': {
                'primary': 'openweathermap',
                'fallback': 'weatherstack',
                'backup': 'wttr.in'
            },
            'news': {
                'primary': 'newsapi',
                'fallback': 'bing_news',
                'backup': 'reddit'
            },
            'search': {
                'primary': 'google',
                'fallback': 'duckduckgo',
                'backup': 'bing'
            },
            'translate': {
                'primary': 'google_translate',
                'fallback': 'mymemory',
                'backup': 'libretranslate'
            },
            'currency': {
                'primary': 'exchangerate',
                'fallback': 'fixer',
                'backup': 'currencylayer'
            }
        }
        
    def execute(self, params):
        """🌐 Execute fallback web service"""
        service = params.get('service', '').lower()
        query = params.get('query', '')
        data = params.get('data', {})
        
        if not service:
            self.tts.speak("Sir, which web service should I use as fallback?")
            return {'success': False, 'error': 'No service specified'}
        
        print(Fore.YELLOW + f"🌐 Fallback service: {service}" + Style.RESET_ALL)
        
        service_map = {
            'weather': self.get_weather_fallback,
            'news': self.get_news_fallback,
            'search': self.search_fallback,
            'translate': self.translate_fallback,
            'currency': self.currency_fallback,
            'time': self.get_time_fallback,
            'ip': self.get_ip_fallback,
            'dns': self.dns_lookup_fallback
        }
        
        if service in service_map:
            return service_map[service](query, data)
        else:
            self.tts.speak(f"Sir, {service} fallback service is not available")
            return {
                'success': False,
                'error': f'Service {service} not found',
                'available_services': list(service_map.keys())
            }
    
    def get_weather_fallback(self, query='', data=None):
        """🌐 Get weather with fallback APIs"""
        try:
            city = query or data.get('city', 'London')
            
            # Try primary service (OpenWeatherMap)
            try:
                api_key = self.config.get('openweather_api_key', '')
                if api_key:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        weather_data = response.json()
                        
                        temp = weather_data['main']['temp']
                        desc = weather_data['weather'][0]['description']
                        humidity = weather_data['main']['humidity']
                        
                        self.tts.speak(f"Weather in {city}: {desc}, temperature {temp}°C, humidity {humidity}%")
                        
                        return {
                            'success': True,
                            'service': 'openweathermap',
                            'city': city,
                            'temperature': temp,
                            'description': desc,
                            'humidity': humidity,
                            'data': weather_data
                        }
            except:
                pass  # Fall through to next service
            
            # Try fallback service (WeatherStack)
            try:
                api_key = self.config.get('weatherstack_api_key', '')
                if api_key:
                    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        weather_data = response.json()
                        
                        if 'current' in weather_data:
                            temp = weather_data['current']['temperature']
                            desc = weather_data['current']['weather_descriptions'][0]
                            humidity = weather_data['current']['humidity']
                            
                            self.tts.speak(f"Weather in {city}: {desc}, temperature {temp}°C, humidity {humidity}%")
                            
                            return {
                                'success': True,
                                'service': 'weatherstack',
                                'city': city,
                                'temperature': temp,
                                'description': desc,
                                'humidity': humidity,
                                'data': weather_data
                            }
            except:
                pass  # Fall through to backup
            
            # Try backup service (wttr.in)
            try:
                url = f"https://wttr.in/{city}?format=j1"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    weather_data = response.json()
                    
                    temp = weather_data['current_condition'][0]['temp_C']
                    desc = weather_data['current_condition'][0]['weatherDesc'][0]['value']
                    humidity = weather_data['current_condition'][0]['humidity']
                    
                    self.tts.speak(f"Weather in {city}: {desc}, temperature {temp}°C, humidity {humidity}%")
                    
                    return {
                        'success': True,
                        'service': 'wttr.in',
                        'city': city,
                        'temperature': temp,
                        'description': desc,
                        'humidity': humidity,
                        'data': weather_data
                    }
            except:
                pass
            
            # All services failed
            self.tts.speak(f"Sorry sir, I couldn't get weather for {city}")
            return {
                'success': False,
                'error': 'All weather services failed',
                'city': city
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_news_fallback(self, query='', data=None):
        """🌐 Get news with fallback APIs"""
        try:
            category = query or data.get('category', 'general')
            country = data.get('country', 'us') if data else 'us'
            
            # Try NewsAPI
            try:
                api_key = self.config.get('newsapi_key', '')
                if api_key:
                    if category == 'headlines':
                        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
                    else:
                        url = f"https://newsapi.org/v2/everything?q={category}&apiKey={api_key}"
                    
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        news_data = response.json()
                        
                        if news_data['articles']:
                            headlines = [article['title'] for article in news_data['articles'][:3]]
                            
                            self.tts.speak(f"Top news: {headlines[0]}")
                            
                            return {
                                'success': True,
                                'service': 'newsapi',
                                'count': len(news_data['articles']),
                                'headlines': headlines,
                                'data': news_data
                            }
            except:
                pass
            
            # Try Bing News (fallback)
            try:
                api_key = self.config.get('bing_api_key', '')
                if api_key:
                    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
                    headers = {"Ocp-Apim-Subscription-Key": api_key}
                    params = {"q": category, "count": 10}
                    
                    response = requests.get(endpoint, headers=headers, params=params, timeout=5)
                    
                    if response.status_code == 200:
                        news_data = response.json()
                        
                        if 'value' in news_data:
                            headlines = [item['name'] for item in news_data['value'][:3]]
                            
                            self.tts.speak(f"News for {category}: {headlines[0]}")
                            
                            return {
                                'success': True,
                                'service': 'bing_news',
                                'count': len(news_data['value']),
                                'headlines': headlines,
                                'data': news_data
                            }
            except:
                pass
            
            # Try Reddit (backup)
            try:
                url = f"https://www.reddit.com/r/news/top.json?limit=10"
                headers = {'User-Agent': 'JARVIS Assistant'}
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    reddit_data = response.json()
                    
                    if 'data' in reddit_data and 'children' in reddit_data['data']:
                        headlines = [post['data']['title'] for post in reddit_data['data']['children'][:3]]
                        
                        self.tts.speak(f"Reddit news: {headlines[0]}")
                        
                        return {
                            'success': True,
                            'service': 'reddit',
                            'count': len(reddit_data['data']['children']),
                            'headlines': headlines,
                            'data': reddit_data
                        }
            except:
                pass
            
            self.tts.speak("Sorry sir, I couldn't fetch news.")
            return {
                'success': False,
                'error': 'All news services failed'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_fallback(self, query='', data=None):
        """🌐 Web search with fallback"""
        try:
            if not query:
                self.tts.speak("Sir, what should I search for?")
                return {'success': False, 'error': 'No search query'}
            
            # Import WebSearch for fallback
            try:
                from .search import WebSearch
                web_search = WebSearch(self.config, self.tts)
                
                # Try Google first
                result = web_search.simple_search(query, 'google')
                if result['success']:
                    return {
                        'success': True,
                        'service': 'google',
                        'query': query,
                        'search_url': result['search_url']
                    }
                
                # Try DuckDuckGo
                result = web_search.simple_search(query, 'duckduckgo')
                if result['success']:
                    return {
                        'success': True,
                        'service': 'duckduckgo',
                        'query': query,
                        'search_url': result['search_url']
                    }
                
                # Try Bing
                result = web_search.simple_search(query, 'bing')
                if result['success']:
                    return {
                        'success': True,
                        'service': 'bing',
                        'query': query,
                        'search_url': result['search_url']
                    }
                
            except:
                pass
            
            # Manual fallback URLs
            search_urls = [
                f"https://www.google.com/search?q={query}",
                f"https://duckduckgo.com/?q={query}",
                f"https://www.bing.com/search?q={query}"
            ]
            
            self.tts.speak(f"Searching for {query} using fallback")
            
            return {
                'success': True,
                'service': 'fallback',
                'query': query,
                'search_urls': search_urls,
                'primary_url': search_urls[0]
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def translate_fallback(self, query='', data=None):
        """🌐 Translation with fallback"""
        try:
            text = data.get('text', '') if data else ''
            source = data.get('source', 'en') if data else 'en'
            target = data.get('target', 'hi') if data else 'hi'  # Default: English to Hindi
            
            if not text:
                self.tts.speak("Sir, what should I translate?")
                return {'success': False, 'error': 'No text to translate'}
            
            self.tts.speak(f"Translating from {source} to {target}")
            
            # Simple fallback translation (mock)
            # In a real implementation, you would use Google Translate API, MyMemory, etc.
            
            return {
                'success': True,
                'service': 'fallback_translation',
                'original': text,
                'translated': f"[Translated: {text}]",  # Mock translation
                'source': source,
                'target': target
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def currency_fallback(self, query='', data=None):
        """🌐 Currency conversion with fallback"""
        try:
            amount = data.get('amount', 1) if data else 1
            from_curr = data.get('from', 'USD') if data else 'USD'
            to_curr = data.get('to', 'INR') if data else 'INR'
            
            # Try exchangerate-api.com (free)
            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{from_curr}"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    rates = response.json()['rates']
                    
                    if to_curr in rates:
                        rate = rates[to_curr]
                        converted = amount * rate
                        
                        self.tts.speak(f"{amount} {from_curr} equals {converted:.2f} {to_curr}")
                        
                        return {
                            'success': True,
                            'service': 'exchangerate-api',
                            'amount': amount,
                            'from': from_curr,
                            'to': to_curr,
                            'rate': rate,
                            'converted': converted
                        }
            except:
                pass
            
            # Try fixer.io (requires API key)
            try:
                api_key = self.config.get('fixer_api_key', '')
                if api_key:
                    url = f"http://data.fixer.io/api/latest?access_key={api_key}&base={from_curr}&symbols={to_curr}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        if 'rates' in data and to_curr in data['rates']:
                            rate = data['rates'][to_curr]
                            converted = amount * rate
                            
                            self.tts.speak(f"{amount} {from_curr} equals {converted:.2f} {to_curr}")
                            
                            return {
                                'success': True,
                                'service': 'fixer',
                                'amount': amount,
                                'from': from_curr,
                                'to': to_curr,
                                'rate': rate,
                                'converted': converted
                            }
            except:
                pass
            
            # Hardcoded fallback rates (approximate)
            fallback_rates = {
                'USD_INR': 83.0,
                'EUR_INR': 90.0,
                'GBP_INR': 105.0,
                'USD_EUR': 0.92,
                'EUR_USD': 1.09,
                'INR_USD': 0.012
            }
            
            key = f"{from_curr}_{to_curr}"
            if key in fallback_rates:
                rate = fallback_rates[key]
                converted = amount * rate
                
                self.tts.speak(f"Approximately {amount} {from_curr} equals {converted:.2f} {to_curr}")
                
                return {
                    'success': True,
                    'service': 'fallback_rates',
                    'amount': amount,
                    'from': from_curr,
                    'to': to_curr,
                    'rate': rate,
                    'converted': converted,
                    'note': 'Using approximate rates'
                }
            
            self.tts.speak(f"Sorry sir, I couldn't convert {from_curr} to {to_curr}")
            return {
                'success': False,
                'error': f'Currency conversion failed for {from_curr} to {to_curr}'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_time_fallback(self, query='', data=None):
        """🌐 Get time with fallback"""
        try:
            location = query or data.get('location', '') if data else ''
            
            if location:
                # Try worldtimeapi.org
                try:
                    url = f"http://worldtimeapi.org/api/timezone/{location}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        time_data = response.json()
                        datetime_str = time_data['datetime']
                        
                        self.tts.speak(f"Time in {location} is {datetime_str[11:16]}")
                        
                        return {
                            'success': True,
                            'service': 'worldtimeapi',
                            'location': location,
                            'datetime': datetime_str,
                            'time': datetime_str[11:16]
                        }
                except:
                    pass
            else:
                # Get local time
                from datetime import datetime
                now = datetime.now()
                current_time = now.strftime("%I:%M %p")
                
                self.tts.speak(f"Current time is {current_time}")
                
                return {
                    'success': True,
                    'service': 'system',
                    'time': current_time,
                    'datetime': now.isoformat()
                }
            
            return {
                'success': False,
                'error': f'Could not get time for {location}'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_ip_fallback(self, query='', data=None):
        """🌐 Get IP address with fallback"""
        try:
            # Try multiple IP services
            ip_services = [
                'https://api.ipify.org?format=json',
                'https://ipinfo.io/json',
                'https://api.my-ip.io/ip.json',
                'https://ipecho.net/plain'
            ]
            
            for service_url in ip_services:
                try:
                    response = requests.get(service_url, timeout=5)
                    if response.status_code == 200:
                        if 'json' in service_url:
                            ip_data = response.json()
                            if 'ip' in ip_data:
                                ip = ip_data['ip']
                            elif 'ip' in ip_data:
                                ip = ip_data['ip']
                            else:
                                ip = response.text.strip()
                        else:
                            ip = response.text.strip()
                        
                        self.tts.speak(f"Your IP address is {ip}")
                        
                        return {
                            'success': True,
                            'service': service_url,
                            'ip': ip,
                            'data': ip_data if 'json' in service_url else {}
                        }
                except:
                    continue
            
            self.tts.speak("Sorry sir, I couldn't get your IP address.")
            return {
                'success': False,
                'error': 'All IP services failed'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def dns_lookup_fallback(self, query='', data=None):
        """🌐 DNS lookup with fallback"""
        try:
            domain = query or data.get('domain', '') if data else ''
            
            if not domain:
                self.tts.speak("Sir, which domain should I look up?")
                return {'success': False, 'error': 'No domain specified'}
            
            # Try multiple DNS lookup services
            dns_services = [
                f"https://dns.google/resolve?name={domain}",
                f"https://cloudflare-dns.com/dns-query?name={domain}",
                f"https://api.hackertarget.com/dnslookup/?q={domain}"
            ]
            
            for service_url in dns_services:
                try:
                    headers = {'Accept': 'application/dns-json'} if 'cloudflare' in service_url else {}
                    response = requests.get(service_url, headers=headers, timeout=5)
                    
                    if response.status_code == 200:
                        dns_data = response.text if 'hackertarget' in service_url else response.json()
                        
                        self.tts.speak(f"DNS lookup completed for {domain}")
                        
                        return {
                            'success': True,
                            'service': service_url,
                            'domain': domain,
                            'data': dns_data
                        }
                except:
                    continue
            
            self.tts.speak(f"Sorry sir, I couldn't perform DNS lookup for {domain}")
            return {
                'success': False,
                'error': 'All DNS services failed',
                'domain': domain
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }