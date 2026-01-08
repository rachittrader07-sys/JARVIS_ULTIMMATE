"""
🌐 Website URL Opener
Opens websites by name (even unknown ones)
"""

import webbrowser
import requests
from duckduckgo_search import DDGS
from colorama import Fore, Style

class URLOpener:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.website_map = self.config['websites']['common']
        
    def execute(self, params):
        """🌐 Open website"""
        website_name = params.get('website_name', '').lower()
        
        if not website_name:
            self.tts.speak("Sir, which website should I open?")
            return {'success': False, 'error': 'No website name'}
        
        print(Fore.YELLOW + f"🔍 Opening website: {website_name}" + Style.RESET_ALL)
        
        # Try multiple methods
        result = self.open_website_multi_method(website_name)
        
        if result['success']:
            self.tts.speak(f"Sir, I have opened {website_name}")
            return {'success': True, 'speak': f"{website_name} opened"}
        else:
            # Try intelligent search
            result2 = self.intelligent_website_search(website_name)
            if result2['success']:
                return result2
            
            self.tts.speak(f"Sir, I couldn't find {website_name}. Would you like me to search for it?")
            return {'success': False, 'error': 'Website not found'}
    
    def open_website_multi_method(self, website_name):
        """🌐 Try multiple methods to open website"""
        # Method 1: Direct from map
        for key, url in self.website_map.items():
            if key in website_name or website_name in key:
                webbrowser.open(url)
                print(Fore.GREEN + f"✅ Opened: {key} -> {url}" + Style.RESET_ALL)
                return {'success': True, 'url': url, 'method': 'direct_map'}
        
        # Method 2: Try common patterns
        common_patterns = {
            'youtube': 'https://youtube.com',
            'facebook': 'https://facebook.com',
            'instagram': 'https://instagram.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            'wikipedia': 'https://wikipedia.org',
            'amazon': 'https://amazon.in',
            'flipkart': 'https://flipkart.com',
            'netflix': 'https://netflix.com',
            'prime': 'https://primevideo.com',
            'hotstar': 'https://hotstar.com',
            'gmail': 'https://gmail.com',
            'outlook': 'https://outlook.com',
            'drive': 'https://drive.google.com',
            'docs': 'https://docs.google.com'
        }
        
        for pattern, url in common_patterns.items():
            if pattern in website_name:
                webbrowser.open(url)
                print(Fore.GREEN + f"✅ Opened via pattern: {pattern}" + Style.RESET_ALL)
                return {'success': True, 'url': url, 'method': 'pattern'}
        
        # Method 3: Try with www and .com
        if '.' not in website_name:
            possible_urls = [
                f"https://www.{website_name}.com",
                f"https://{website_name}.com",
                f"https://www.{website_name}.in",
                f"https://{website_name}.in",
                f"https://www.{website_name}.org",
                f"https://{website_name}.org"
            ]
            
            for url in possible_urls:
                if self.check_url_exists(url):
                    webbrowser.open(url)
                    print(Fore.GREEN + f"✅ Opened via guessing: {url}" + Style.RESET_ALL)
                    return {'success': True, 'url': url, 'method': 'guessed'}
        
        return {'success': False}
    
    @staticmethod
    def intelligent_website_search(website_name):
        """🌐 Intelligent search for unknown websites"""
        try:
            # Use DuckDuckGo to search
            with DDGS() as ddgs:
                search_query = f"{website_name} website official"
                results = list(ddgs.text(search_query, max_results=3))
                
                if results:
                    # Find the most likely official website
                    for result in results:
                        url = result.get('href', '')
                        title = result.get('title', '').lower()
                        body = result.get('body', '').lower()
                        
                        # Check if this looks like an official website
                        if (website_name in title or website_name in body) and \
                           ('official' in title or 'official' in body or 'home' in title):
                            webbrowser.open(url)
                            print(Fore.GREEN + f"✅ Found via search: {title}" + Style.RESET_ALL)
                            return {
                                'success': True,
                                'url': url,
                                'method': 'intelligent_search',
                                'found_via': 'search'
                            }
                    
                    # If no official found, use first result
                    first_result = results[0]
                    url = first_result.get('href', '')
                    if url:
                        webbrowser.open(url)
                        print(Fore.GREEN + f"✅ Using search result: {url}" + Style.RESET_ALL)
                        return {
                            'success': True,
                            'url': url,
                            'method': 'search_fallback'
                        }
        
        except Exception as e:
            print(Fore.RED + f"❌ Search failed: {str(e)}" + Style.RESET_ALL)
        
        return {'success': False}
    
    @staticmethod
    def check_url_exists(url):
        """🌐 Check if URL exists"""
        try:
            response = requests.head(url, timeout=3, allow_redirects=True)
            return response.status_code < 400
        except:
            return False