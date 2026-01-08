"""
📱 WhatsApp Controller
Sends messages via WhatsApp Desktop
"""

import pyautogui
import time
import os
import json
from colorama import Fore, Style

class WhatsAppController:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.contacts = self.load_contacts()
        self.whatsapp_open = False
        
    def execute(self, params):
        """📱 Send WhatsApp message"""
        person = params.get('person', '').lower()
        message = params.get('message', '')
        
        if not person:
            self.tts.speak("Sir, whom should I message?")
            return {'success': False, 'error': 'No person specified'}
        
        # If message not provided, ask for it
        if not message:
            self.tts.speak(f"Sir, what message should I send to {person}?")
            # Wait for user response (this would be handled by conversation manager)
            return {
                'success': False, 
                'needs_followup': True,
                'followup_type': 'whatsapp_message',
                'person': person
            }
        
        print(Fore.YELLOW + f"📱 Sending WhatsApp to {person}: {message}" + Style.RESET_ALL)
        
        # Open WhatsApp if not already open
        if not self.whatsapp_open:
            open_result = self.open_whatsapp()
            if not open_result['success']:
                return open_result
        
        # Search for contact
        search_result = self.search_contact(person)
        if not search_result['success']:
            return search_result
        
        # Type and send message
        send_result = self.send_message(message)
        
        if send_result['success']:
            self.tts.speak(f"Sir, message sent to {person}")
            return {'success': True, 'speak': f"Message sent to {person}"}
        else:
            self.tts.speak(f"Sir, I couldn't send the message to {person}")
            return send_result
    
    def open_whatsapp(self):
        """📱 Open WhatsApp Desktop"""
        try:
            # Try multiple methods to open WhatsApp
            import subprocess
            
            # Method 1: Direct executable
            whatsapp_paths = [
                os.path.expanduser("~\\AppData\\Local\\WhatsApp\\WhatsApp.exe"),
                "C:\\Program Files\\WindowsApps\\WhatsAppDesktop\\WhatsApp.exe",
                "whatsapp"
            ]
            
            for path in whatsapp_paths:
                try:
                    subprocess.Popen(path, shell=True)
                    time.sleep(3)  # Wait for WhatsApp to open
                    self.whatsapp_open = True
                    print(Fore.GREEN + "✅ WhatsApp opened" + Style.RESET_ALL)
                    return {'success': True}
                except:
                    continue
            
            # Method 2: Try via appopener
            try:
                import appopener
                appopener.open("whatsapp")
                time.sleep(3)
                self.whatsapp_open = True
                print(Fore.GREEN + "✅ WhatsApp opened via appopener" + Style.RESET_ALL)
                return {'success': True}
            except:
                pass
            
            self.tts.speak("Sir, I couldn't open WhatsApp. Please make sure it's installed.")
            return {'success': False, 'error': 'WhatsApp not found'}
            
        except Exception as e:
            print(Fore.RED + f"❌ WhatsApp open error: {str(e)}" + Style.RESET_ALL)
            return {'success': False, 'error': str(e)}
    
    def search_contact(self, person):
        """📱 Search for contact in WhatsApp"""
        try:
            # Focus on WhatsApp window
            self.focus_whatsapp()
            time.sleep(1)
            
            # Press Ctrl+F to open search (Windows shortcut)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Type contact name
            pyautogui.write(person, interval=0.1)
            time.sleep(1)
            
            # Press Enter to select first result
            pyautogui.press('enter')
            time.sleep(1)
            
            print(Fore.GREEN + f"✅ Contact found: {person}" + Style.RESET_ALL)
            return {'success': True}
            
        except Exception as e:
            print(Fore.RED + f"❌ Contact search error: {str(e)}" + Style.RESET_ALL)
            return {'success': False, 'error': str(e)}
    
    def send_message(self, message):
        """📱 Type and send message"""
        try:
            # Type message
            pyautogui.write(message, interval=0.05)
            time.sleep(0.5)
            
            # Press Enter to send
            pyautogui.press('enter')
            time.sleep(0.5)
            
            print(Fore.GREEN + "✅ Message sent" + Style.RESET_ALL)
            return {'success': True}
            
        except Exception as e:
            print(Fore.RED + f"❌ Message send error: {str(e)}" + Style.RESET_ALL)
            return {'success': False, 'error': str(e)}
    
    def focus_whatsapp(self):
        """📱 Focus on WhatsApp window"""
        try:
            import pygetwindow as gw
            
            # Find WhatsApp window
            windows = gw.getWindowsWithTitle('WhatsApp')
            if windows:
                window = windows[0]
                if window.isMinimized:
                    window.restore()
                window.activate()
                return True
                
            return False
        except:
            return False
    
    def load_contacts(self):
        """📱 Load saved contacts"""
        contacts_path = "memory/contacts.json"
        contacts = {}
        
        try:
            if os.path.exists(contacts_path):
                with open(contacts_path, 'r', encoding='utf-8') as f:
                    contacts = json.load(f)
        except:
            pass
        
        return contacts