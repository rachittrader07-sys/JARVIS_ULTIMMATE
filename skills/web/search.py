"""
🔍 Web Search Skill
Searches the web using multiple engines
"""

import webbrowser
import requests
from duckduckgo_search import DDGS
from colorama import Fore, Style

class WebSearch:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.search_engines = ['google', 'duckduckgo', 'bing']
        
    def execute(self, params):
        """🔍 Execute web search"""
        query = params.get('query', '').lower()
        engine = params.get('engine', 'google')
        
        if not query:
            self.tts.speak("Sir, what should I search for?")
            return {'success': False, 'error': 'No query'}
        
        print(Fore.YELLOW + f"🔍 Searching for: {query}" + Style.RESET_ALL)
        
        # Try the specified engine first
        result = self.search_with_engine(query, engine)
        
        if result['success']:
            self.tts.speak(f"Sir, I found results for {query}")
            return result
        else:
            # Try other engines
            for alt_engine in self.search_engines:
                if alt_engine != engine:
                    result = self.search_with_engine(query, alt_engine)
                    if result['success']:
                        self.tts.speak(f"Sir, I found results using {alt_engine}")
                        return result
            
            # If all fail, try direct Google search
            return self.search_google_direct(query)
    
    def search_with_engine(self, query, engine):
        """🔍 Search using specific engine"""
        try:
            if engine == 'google':
                return self.search_google(query)
            elif engine == 'duckduckgo':
                return self.search_duckduckgo(query)
            elif engine == 'bing':
                return self.search_bing(query)
            else:
                return self.search_google(query)
        except Exception as e:
            print(Fore.RED + f"❌ {engine} search error: {str(e)}" + Style.RESET_ALL)
            return {'success': False, 'error': str(e)}
    
    def search_google(self, query):
        """🔍 Search using Google"""
        try:
            # Open Google search in browser
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            
            print(Fore.GREEN + f"✅ Google search opened: {query}" + Style.RESET_ALL)
            
            return {
                'success': True,
                'engine': 'google',
                'url': url,
                'query': query
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_duckduckgo(self, query):
        """🔍 Search using DuckDuckGo"""
        try:
            # Get search results
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                
                if results:
                    # Open first result
                    first_result = results[0]
                    url = first_result.get('href', '')
                    
                    if url:
                        webbrowser.open(url)
                        print(Fore.GREEN + f"✅ DuckDuckGo result opened: {url}" + Style.RESET_ALL)
                        
                        return {
                            'success': True,
                            'engine': 'duckduckgo',
                            'url': url,
                            'query': query,
                            'results_count': len(results)
                        }
            
            # If no results, open DuckDuckGo website
            url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            
            return {
                'success': True,
                'engine': 'duckduckgo',
                'url': url,
                'query': query,
                'fallback': True
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_bing(self, query):
        """🔍 Search using Bing"""
        try:
            url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            
            print(Fore.GREEN + f"✅ Bing search opened: {query}" + Style.RESET_ALL)
            
            return {
                'success': True,
                'engine': 'bing',
                'url': url,
                'query': query
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def search_google_direct(self, query):
        """🔍 Direct Google search fallback"""
        try:
            # Simple Google search URL
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            
            return {
                'success': True,
                'engine': 'google_direct',
                'url': url,
                'query': query,
                'fallback': True
            }
        except:
            return {
                'success': False,
                'error': 'All search methods failed'
            }