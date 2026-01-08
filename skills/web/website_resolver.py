"""
🌐 Website Resolver
Resolves website names to URLs and provides quick access
"""

import json
import os
import re
from datetime import datetime

from colorama import Fore, Style


class WebsiteResolver:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.websites_file = os.path.join("data", "websites.json")
        self.websites = self.load_websites()

    def execute(self, params):
        """🌐 Execute website resolution"""
        action = params.get("action", "open")
        site_name = params.get("site", "")
        custom_url = params.get("url", "")

        if not action:
            self.tts.speak("Sir, what website action should I perform?")
            return {"success": False, "error": "No action specified"}

        print(Fore.YELLOW + f"🌐 Website action: {action}" + Style.RESET_ALL)

        action_map = {
            "open": self.open_website,
            "resolve": self.resolve_website,
            "add": self.add_website,
            "remove": self.remove_website,
            "list": self.list_websites,
            "search": self.search_websites,
            "shortcut": self.create_shortcut,
            "category": self.list_by_category,
        }

        if action in action_map:
            return action_map[action](
                site_name=site_name, custom_url=custom_url, params=params
            )
        else:
            self.tts.speak(f"Sir, {action} website action is not available")
            return {
                "success": False,
                "error": f"Action {action} not found",
                "available_actions": list(action_map.keys()),
            }

    def load_websites(self):
        """🌐 Load websites from JSON file"""
        try:
            if os.path.exists(self.websites_file):
                with open(self.websites_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                default_websites = {
                    "websites": {
                        "google": {
                            "name": "Google",
                            "url": "https://www.google.com",
                            "category": "search",
                            "shortcuts": ["search", "web"],
                            "favicon": "https://www.google.com/favicon.ico",
                        },
                        "youtube": {
                            "name": "YouTube",
                            "url": "https://www.youtube.com",
                            "category": "entertainment",
                            "shortcuts": ["video", "music", "videos"],
                            "favicon": "https://www.youtube.com/favicon.ico",
                        },
                        "github": {
                            "name": "GitHub",
                            "url": "https://github.com",
                            "category": "development",
                            "shortcuts": ["code", "git", "repository"],
                            "favicon": "https://github.com/favicon.ico",
                        },
                        "facebook": {
                            "name": "Facebook",
                            "url": "https://www.facebook.com",
                            "category": "social",
                            "shortcuts": ["fb", "social"],
                            "favicon": "https://www.facebook.com/favicon.ico",
                        },
                        "wikipedia": {
                            "name": "Wikipedia",
                            "url": "https://en.wikipedia.org",
                            "category": "reference",
                            "shortcuts": ["wiki", "encyclopedia"],
                            "favicon": "https://en.wikipedia.org/favicon.ico",
                        },
                        "amazon": {
                            "name": "Amazon",
                            "url": "https://www.amazon.com",
                            "category": "shopping",
                            "shortcuts": ["shop", "buy"],
                            "favicon": "https://www.amazon.com/favicon.ico",
                        },
                        "netflix": {
                            "name": "Netflix",
                            "url": "https://www.netflix.com",
                            "category": "entertainment",
                            "shortcuts": ["movies", "shows"],
                            "favicon": "https://www.netflix.com/favicon.ico",
                        },
                        "stackoverflow": {
                            "name": "Stack Overflow",
                            "url": "https://stackoverflow.com",
                            "category": "development",
                            "shortcuts": ["so", "questions", "programming"],
                            "favicon": "https://stackoverflow.com/favicon.ico",
                        },
                        "reddit": {
                            "name": "Reddit",
                            "url": "https://www.reddit.com",
                            "category": "social",
                            "shortcuts": ["subreddit", "discussion"],
                            "favicon": "https://www.reddit.com/favicon.ico",
                        },
                        "twitter": {
                            "name": "Twitter",
                            "url": "https://twitter.com",
                            "category": "social",
                            "shortcuts": ["tweet", "x"],
                            "favicon": "https://twitter.com/favicon.ico",
                        },
                    },
                    "categories": [
                        "search",
                        "entertainment",
                        "development",
                        "social",
                        "shopping",
                        "reference",
                        "news",
                        "education",
                        "productivity",
                    ],
                    "settings": {
                        "auto_complete": True,
                        "suggest_similar": True,
                        "default_browser": "default",
                    },
                }

                os.makedirs("data", exist_ok=True)
                with open(self.websites_file, "w", encoding="utf-8") as f:
                    json.dump(default_websites, f, indent=2)

                return default_websites

        except Exception as e:
            print(Fore.RED + f"Error loading websites: {e}" + Style.RESET_ALL)
            return {"websites": {}, "categories": [], "settings": {}}

    def save_websites(self):
        """🌐 Save websites to JSON file"""
        try:
            with open(self.websites_file, "w", encoding="utf-8") as f:
                json.dump(self.websites, f, indent=2)
            return True
        except Exception as e:
            print(Fore.RED + f"Error saving websites: {e}" + Style.RESET_ALL)
            return False

    def open_website(self, site_name="", custom_url="", params=None):
        """🌐 Open a website by name"""
        try:
            if not site_name and not custom_url:
                self.tts.speak("Sir, which website should I open?")
                return {"success": False, "error": "No website specified"}

            # If custom URL provided, open it directly
            if custom_url:
                import webbrowser

                # Ensure URL has scheme
                if not re.match(r"^https?://", custom_url):
                    custom_url = "https://" + custom_url

                webbrowser.open(custom_url)

                self.tts.speak(f"Opening {custom_url}")

                return {
                    "success": True,
                    "action": "open",
                    "url": custom_url,
                    "type": "custom_url",
                }

            # Resolve website name
            site_name_lower = site_name.lower()
            websites = self.websites.get("websites", {})

            # Check exact match
            if site_name_lower in websites:
                site_data = websites[site_name_lower]
                url = site_data["url"]

                import webbrowser

                webbrowser.open(url)

                self.tts.speak(f"Opening {site_data['name']}")

                return {
                    "success": True,
                    "action": "open",
                    "site": site_name,
                    "name": site_data["name"],
                    "url": url,
                    "category": site_data.get("category", ""),
                }

            # Check shortcuts
            for site_key, site_data in websites.items():
                shortcuts = site_data.get("shortcuts", [])
                if site_name_lower in shortcuts:
                    url = site_data["url"]

                    import webbrowser

                    webbrowser.open(url)

                    self.tts.speak(f"Opening {site_data['name']}")

                    return {
                        "success": True,
                        "action": "open",
                        "site": site_name,
                        "name": site_data["name"],
                        "url": url,
                        "matched_by": "shortcut",
                    }

            # Check partial match in site names
            for site_key, site_data in websites.items():
                if site_name_lower in site_data["name"].lower():
                    url = site_data["url"]

                    import webbrowser

                    webbrowser.open(url)

                    self.tts.speak(f"Opening {site_data['name']}")

                    return {
                        "success": True,
                        "action": "open",
                        "site": site_name,
                        "name": site_data["name"],
                        "url": url,
                        "matched_by": "partial_name",
                    }

            # If auto-complete is enabled, try to guess
            if self.websites.get("settings", {}).get("auto_complete", True):
                suggestions = self.suggest_websites(site_name_lower)

                if suggestions:
                    # Open first suggestion
                    first_suggestion = suggestions[0]
                    site_data = websites[first_suggestion["key"]]

                    import webbrowser

                    webbrowser.open(site_data["url"])

                    self.tts.speak(
                        f"Opening {site_data['name']} based on your request for {site_name}"
                    )

                    return {
                        "success": True,
                        "action": "open",
                        "site": site_name,
                        "name": site_data["name"],
                        "url": site_data["url"],
                        "matched_by": "suggestion",
                        "suggestions": suggestions,
                    }

            self.tts.speak(f"Sir, I couldn't find website {site_name}")
            return {"success": False, "error": "Website not found", "site": site_name}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def resolve_website(self, site_name="", custom_url="", params=None):
        """🌐 Resolve website name to URL without opening"""
        try:
            if not site_name:
                self.tts.speak("Sir, which website should I resolve?")
                return {"success": False, "error": "No website specified"}

            site_name_lower = site_name.lower()
            websites = self.websites.get("websites", {})

            # Check exact match
            if site_name_lower in websites:
                site_data = websites[site_name_lower]

                self.tts.speak(
                    f"{site_name} is {site_data['name']} at {site_data['url']}"
                )

                return {
                    "success": True,
                    "action": "resolve",
                    "site": site_name,
                    "name": site_data["name"],
                    "url": site_data["url"],
                    "category": site_data.get("category", ""),
                    "shortcuts": site_data.get("shortcuts", []),
                }

            # Check shortcuts
            for site_key, site_data in websites.items():
                shortcuts = site_data.get("shortcuts", [])
                if site_name_lower in shortcuts:
                    self.tts.speak(
                        f"{site_name} refers to {site_data['name']} at {site_data['url']}"
                    )

                    return {
                        "success": True,
                        "action": "resolve",
                        "site": site_name,
                        "name": site_data["name"],
                        "url": site_data["url"],
                        "matched_by": "shortcut",
                    }

            # Search for similar
            suggestions = self.suggest_websites(site_name_lower)

            if suggestions:
                self.tts.speak(f"Did you mean {suggestions[0]['name']}?")

                return {
                    "success": False,
                    "error": "Website not found directly",
                    "site": site_name,
                    "suggestions": suggestions,
                    "message": f'Did you mean {suggestions[0]["name"]}?',
                }

            self.tts.speak(f"Sir, I couldn't resolve website {site_name}")
            return {"success": False, "error": "Website not found", "site": site_name}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def add_website(self, site_name="", custom_url="", params=None):
        """🌐 Add a new website to the resolver"""
        try:
            if not site_name:
                self.tts.speak("Sir, what's the name of the website?")
                return {"success": False, "error": "No website name"}

            if not custom_url:
                self.tts.speak("Sir, what's the URL of the website?")
                return {"success": False, "error": "No URL provided"}

            # Validate URL
            if not re.match(r"^https?://", custom_url):
                custom_url = "https://" + custom_url

            site_key = site_name.lower().replace(" ", "_")
            websites = self.websites.get("websites", {})

            # Check if already exists
            if site_key in websites:
                self.tts.speak(f"Sir, website {site_name} already exists.")
                return {
                    "success": False,
                    "error": "Website already exists",
                    "site": site_name,
                }

            # Add new website
            category = params.get("category", "general") if params else "general"
            shortcuts = params.get("shortcuts", []) if params else []

            websites[site_key] = {
                "name": site_name,
                "url": custom_url,
                "category": category,
                "shortcuts": shortcuts,
                "added": datetime.now().isoformat(),
            }

            self.websites["websites"] = websites

            # Add category if new
            categories = self.websites.get("categories", [])
            if category not in categories:
                categories.append(category)
                self.websites["categories"] = categories

            if self.save_websites():
                self.tts.speak(f"Added website {site_name}")

                return {
                    "success": True,
                    "action": "add",
                    "site": site_name,
                    "url": custom_url,
                    "key": site_key,
                    "category": category,
                }
            else:
                self.tts.speak("Failed to save website.")
                return {"success": False, "error": "Failed to save website"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_website(self, site_name="", custom_url="", params=None):
        """🌐 Remove a website from the resolver"""
        try:
            if not site_name:
                self.tts.speak("Sir, which website should I remove?")
                return {"success": False, "error": "No website specified"}

            site_key = site_name.lower().replace(" ", "_")
            websites = self.websites.get("websites", {})

            if site_key not in websites:
                # Try to find by name match
                found_key = None
                for key, site_data in websites.items():
                    if site_name.lower() in site_data["name"].lower():
                        found_key = key
                        break

                if not found_key:
                    self.tts.speak(f"Sir, website {site_name} not found.")
                    return {
                        "success": False,
                        "error": "Website not found",
                        "site": site_name,
                    }

                site_key = found_key

            # Remove website
            removed_site = websites.pop(site_key)
            self.websites["websites"] = websites

            if self.save_websites():
                self.tts.speak(f"Removed website {removed_site['name']}")

                return {
                    "success": True,
                    "action": "remove",
                    "site": removed_site["name"],
                    "url": removed_site["url"],
                }
            else:
                self.tts.speak("Failed to remove website.")
                return {"success": False, "error": "Failed to save after removal"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_websites(self, site_name="", custom_url="", params=None):
        """🌐 List all websites"""
        try:
            websites = self.websites.get("websites", {})

            if not websites:
                self.tts.speak("No websites are configured.")
                return {"success": True, "action": "list", "count": 0, "websites": []}

            website_list = []
            for key, site_data in websites.items():
                website_list.append(
                    {
                        "key": key,
                        "name": site_data["name"],
                        "url": site_data["url"],
                        "category": site_data.get("category", ""),
                        "shortcuts": site_data.get("shortcuts", []),
                    }
                )

            count = len(website_list)

            if count == 1:
                self.tts.speak(
                    f"You have 1 website configured: {website_list[0]['name']}"
                )
            else:
                website_names = [w["name"] for w in website_list[:3]]
                self.tts.speak(
                    f"You have {count} websites configured. First few: {', '.join(website_names)}"
                )

            return {
                "success": True,
                "action": "list",
                "count": count,
                "websites": website_list[:20],  # Return first 20
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def search_websites(self, site_name="", custom_url="", params=None):
        """🌐 Search websites by name, URL, or category"""
        try:
            search_query = params.get("query", "") if params else ""

            if not search_query:
                self.tts.speak("Sir, what should I search for in websites?")
                return {"success": False, "error": "No search query"}

            websites = self.websites.get("websites", {})
            results = []

            search_lower = search_query.lower()

            for key, site_data in websites.items():
                # Search in name
                if search_lower in site_data["name"].lower():
                    results.append(
                        {
                            "key": key,
                            "name": site_data["name"],
                            "url": site_data["url"],
                            "category": site_data.get("category", ""),
                            "match_type": "name",
                        }
                    )
                    continue

                # Search in URL
                if search_lower in site_data["url"].lower():
                    results.append(
                        {
                            "key": key,
                            "name": site_data["name"],
                            "url": site_data["url"],
                            "category": site_data.get("category", ""),
                            "match_type": "url",
                        }
                    )
                    continue

                # Search in shortcuts
                shortcuts = site_data.get("shortcuts", [])
                if any(search_lower in shortcut.lower() for shortcut in shortcuts):
                    results.append(
                        {
                            "key": key,
                            "name": site_data["name"],
                            "url": site_data["url"],
                            "category": site_data.get("category", ""),
                            "match_type": "shortcut",
                        }
                    )
                    continue

                # Search in category
                if search_lower in site_data.get("category", "").lower():
                    results.append(
                        {
                            "key": key,
                            "name": site_data["name"],
                            "url": site_data["url"],
                            "category": site_data.get("category", ""),
                            "match_type": "category",
                        }
                    )

            if not results:
                self.tts.speak(f"No websites found for {search_query}")
            else:
                self.tts.speak(f"Found {len(results)} websites matching {search_query}")

            return {
                "success": True,
                "action": "search",
                "query": search_query,
                "count": len(results),
                "results": results,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_shortcut(self, site_name="", custom_url="", params=None):
        """🌐 Create a shortcut for a website"""
        try:
            if not site_name:
                self.tts.speak("Sir, for which website should I create a shortcut?")
                return {"success": False, "error": "No website specified"}

            shortcut = params.get("shortcut", "") if params else ""
            if not shortcut:
                self.tts.speak("Sir, what should the shortcut be?")
                return {"success": False, "error": "No shortcut specified"}

            site_key = site_name.lower().replace(" ", "_")
            websites = self.websites.get("websites", {})

            # Find website
            if site_key not in websites:
                # Try to find by name
                found_key = None
                for key, site_data in websites.items():
                    if site_name.lower() in site_data["name"].lower():
                        found_key = key
                        break

                if not found_key:
                    self.tts.speak(f"Sir, website {site_name} not found.")
                    return {
                        "success": False,
                        "error": "Website not found",
                        "site": site_name,
                    }

                site_key = found_key

            # Add shortcut
            site_data = websites[site_key]
            shortcuts = site_data.get("shortcuts", [])

            if shortcut in shortcuts:
                self.tts.speak(
                    f"Shortcut {shortcut} already exists for {site_data['name']}"
                )
                return {
                    "success": False,
                    "error": "Shortcut already exists",
                    "site": site_data["name"],
                    "shortcut": shortcut,
                }

            shortcuts.append(shortcut)
            site_data["shortcuts"] = shortcuts
            websites[site_key] = site_data
            self.websites["websites"] = websites

            if self.save_websites():
                self.tts.speak(f"Created shortcut {shortcut} for {site_data['name']}")

                return {
                    "success": True,
                    "action": "shortcut",
                    "site": site_data["name"],
                    "shortcut": shortcut,
                    "shortcuts": shortcuts,
                }
            else:
                self.tts.speak("Failed to create shortcut.")
                return {"success": False, "error": "Failed to save shortcut"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_by_category(self, site_name="", custom_url="", params=None):
        """🌐 List websites by category"""
        try:
            category = params.get("category", "") if params else ""

            if not category:
                # List all categories
                categories = self.websites.get("categories", [])

                if not categories:
                    self.tts.speak("No categories defined.")
                    return {"success": True, "action": "category", "categories": []}

                self.tts.speak(f"Available categories: {', '.join(categories)}")

                return {
                    "success": True,
                    "action": "category",
                    "categories": categories,
                    "count": len(categories),
                }
            else:
                # List websites in category
                websites = self.websites.get("websites", {})
                category_websites = []

                for key, site_data in websites.items():
                    if site_data.get("category", "").lower() == category.lower():
                        category_websites.append(
                            {
                                "key": key,
                                "name": site_data["name"],
                                "url": site_data["url"],
                                "shortcuts": site_data.get("shortcuts", []),
                            }
                        )

                if not category_websites:
                    self.tts.speak(f"No websites found in category {category}")
                else:
                    website_names = [w["name"] for w in category_websites[:3]]
                    self.tts.speak(
                        f"Found {len(category_websites)} websites in {category}: {', '.join(website_names)}"
                    )

                return {
                    "success": True,
                    "action": "category",
                    "category": category,
                    "count": len(category_websites),
                    "websites": category_websites,
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def suggest_websites(self, query):
        """🌐 Suggest websites based on query"""
        websites = self.websites.get("websites", {})
        suggestions = []

        for key, site_data in websites.items():
            score = 0

            # Check name
            if query in site_data["name"].lower():
                score += 10

            # Check shortcuts
            shortcuts = site_data.get("shortcuts", [])
            for shortcut in shortcuts:
                if query in shortcut.lower():
                    score += 5
                    break

            # Check partial matches
            if query in key:
                score += 3

            # Check category
            if query in site_data.get("category", "").lower():
                score += 2

            if score > 0:
                suggestions.append(
                    {
                        "key": key,
                        "name": site_data["name"],
                        "url": site_data["url"],
                        "score": score,
                        "category": site_data.get("category", ""),
                    }
                )

        # Sort by score descending
        suggestions.sort(key=lambda x: x["score"], reverse=True)

        return suggestions[:5]  # Return top 5 suggestions
