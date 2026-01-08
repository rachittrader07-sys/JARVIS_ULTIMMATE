"""
📞 Contact Resolver
Resolves and manages contact information
"""

import json
import os
import re
from colorama import Fore, Style
from datetime import datetime

class ContactResolver:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.contacts_file = os.path.join('data', 'contacts.json')
        self.contacts = self.load_contacts()
        
    def execute(self, params):
        """📞 Execute contact resolution"""
        action = params.get('action', 'find')
        name = params.get('name', '')
        phone = params.get('phone', '')
        email = params.get('email', '')
        
        print(Fore.YELLOW + f"📞 Contact action: {action}" + Style.RESET_ALL)
        
        action_map = {
            'find': self.find_contact,
            'search': self.search_contacts,
            'add': self.add_contact,
            'update': self.update_contact,
            'delete': self.delete_contact,
            'list': self.list_contacts,
            'call': self.prepare_call,
            'message': self.prepare_message,
            'email': self.prepare_email
        }
        
        if action in action_map:
            return action_map[action](name, phone, email, params)
        else:
            self.tts.speak("Sir, that contact action is not available.")
            return {
                'success': False,
                'error': f'Unknown action: {action}',
                'available_actions': list(action_map.keys())
            }
    
    def load_contacts(self):
        """📞 Load contacts from JSON file"""
        try:
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Create default contacts file with sample data
                default_contacts = {
                    "contacts": [
                        {
                            "id": 1,
                            "name": "John Doe",
                            "phone": "+1234567890",
                            "email": "john@example.com",
                            "category": "family",
                            "notes": "Close friend",
                            "created_at": "2024-01-01",
                            "updated_at": "2024-01-01"
                        },
                        {
                            "id": 2,
                            "name": "Jane Smith",
                            "phone": "+0987654321",
                            "email": "jane@example.com",
                            "category": "work",
                            "notes": "Colleague",
                            "created_at": "2024-01-01",
                            "updated_at": "2024-01-01"
                        }
                    ],
                    "settings": {
                        "auto_save": True,
                        "backup_enabled": True,
                        "sync_enabled": False
                    }
                }
                
                # Create data directory if it doesn't exist
                os.makedirs('data', exist_ok=True)
                
                with open(self.contacts_file, 'w', encoding='utf-8') as f:
                    json.dump(default_contacts, f, indent=2)
                
                return default_contacts
                
        except Exception as e:
            print(Fore.RED + f"Error loading contacts: {e}" + Style.RESET_ALL)
            return {"contacts": [], "settings": {}}
    
    def save_contacts(self):
        """📞 Save contacts to JSON file"""
        try:
            with open(self.contacts_file, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, indent=2)
            return True
        except Exception as e:
            print(Fore.RED + f"Error saving contacts: {e}" + Style.RESET_ALL)
            return False
    
    def find_contact(self, name, phone, email, params):
        """📞 Find a specific contact"""
        try:
            search_term = name or phone or email
            if not search_term:
                self.tts.speak("Sir, who should I search for?")
                return {
                    'success': False,
                    'error': 'No search term provided'
                }
            
            search_term_lower = search_term.lower()
            contacts_list = self.contacts.get('contacts', [])
            found_contacts = []
            
            for contact in contacts_list:
                # Search in name, phone, and email
                if (search_term_lower in contact.get('name', '').lower() or
                    search_term_lower in contact.get('phone', '') or
                    search_term_lower in contact.get('email', '').lower()):
                    found_contacts.append(contact)
            
            if found_contacts:
                if len(found_contacts) == 1:
                    contact = found_contacts[0]
                    self.tts.speak(f"I found {contact['name']}. Phone: {contact.get('phone', 'Not available')}. Email: {contact.get('email', 'Not available')}")
                    
                    return {
                        'success': True,
                        'action': 'find',
                        'count': 1,
                        'contact': contact
                    }
                else:
                    names = [c['name'] for c in found_contacts[:3]]
                    self.tts.speak(f"I found {len(found_contacts)} contacts: {', '.join(names)}")
                    
                    return {
                        'success': True,
                        'action': 'find',
                        'count': len(found_contacts),
                        'contacts': found_contacts
                    }
            else:
                self.tts.speak(f"Sorry sir, I couldn't find any contact matching {search_term}")
                return {
                    'success': False,
                    'action': 'find',
                    'error': 'Contact not found',
                    'search_term': search_term
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_contacts(self, name, phone, email, params):
        """📞 Search contacts with filters"""
        try:
            category = params.get('category', '')
            limit = params.get('limit', 10)
            
            contacts_list = self.contacts.get('contacts', [])
            results = []
            
            for contact in contacts_list:
                match = True
                
                # Apply filters
                if name and name.lower() not in contact.get('name', '').lower():
                    match = False
                
                if phone and phone not in contact.get('phone', ''):
                    match = False
                
                if email and email.lower() not in contact.get('email', '').lower():
                    match = False
                
                if category and category.lower() != contact.get('category', '').lower():
                    match = False
                
                if match:
                    results.append(contact)
            
            self.tts.speak(f"Found {len(results)} contacts matching your criteria.")
            
            return {
                'success': True,
                'action': 'search',
                'count': len(results),
                'contacts': results[:limit]
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_contact(self, name, phone, email, params):
        """📞 Add a new contact"""
        try:
            if not name:
                self.tts.speak("Sir, what's the name of the new contact?")
                return {
                    'success': False,
                    'error': 'Name is required'
                }
            
            # Generate new ID
            contacts_list = self.contacts.get('contacts', [])
            new_id = max([c.get('id', 0) for c in contacts_list], default=0) + 1
            
            # Create new contact
            new_contact = {
                'id': new_id,
                'name': name,
                'phone': phone or '',
                'email': email or '',
                'category': params.get('category', 'general'),
                'notes': params.get('notes', ''),
                'created_at': datetime.now().strftime('%Y-%m-%d'),
                'updated_at': datetime.now().strftime('%Y-%m-%d')
            }
            
            # Validate phone number
            if phone and not self.validate_phone(phone):
                self.tts.speak("Sir, that phone number format is invalid. Please provide a valid number.")
                return {
                    'success': False,
                    'error': 'Invalid phone number format'
                }
            
            # Validate email
            if email and not self.validate_email(email):
                self.tts.speak("Sir, that email format is invalid. Please provide a valid email.")
                return {
                    'success': False,
                    'error': 'Invalid email format'
                }
            
            # Add to contacts
            contacts_list.append(new_contact)
            self.contacts['contacts'] = contacts_list
            
            # Save to file
            if self.save_contacts():
                self.tts.speak(f"Contact {name} added successfully.")
                return {
                    'success': True,
                    'action': 'add',
                    'contact': new_contact
                }
            else:
                self.tts.speak("Failed to save contact. Please try again.")
                return {
                    'success': False,
                    'error': 'Failed to save contact'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_contact(self, name, phone, email, params):
        """📞 Update an existing contact"""
        try:
            contact_id = params.get('id')
            search_name = name
            
            if not contact_id and not search_name:
                self.tts.speak("Sir, which contact should I update?")
                return {
                    'success': False,
                    'error': 'No contact identifier provided'
                }
            
            contacts_list = self.contacts.get('contacts', [])
            contact_to_update = None
            contact_index = -1
            
            # Find contact by ID or name
            for i, contact in enumerate(contacts_list):
                if (contact_id and contact.get('id') == contact_id) or \
                   (search_name and search_name.lower() in contact.get('name', '').lower()):
                    contact_to_update = contact
                    contact_index = i
                    break
            
            if not contact_to_update:
                self.tts.speak("Sir, I couldn't find that contact.")
                return {
                    'success': False,
                    'error': 'Contact not found'
                }
            
            # Update fields
            if name:
                contact_to_update['name'] = name
            if phone:
                if not self.validate_phone(phone):
                    self.tts.speak("Sir, that phone number format is invalid.")
                    return {
                        'success': False,
                        'error': 'Invalid phone number format'
                    }
                contact_to_update['phone'] = phone
            if email:
                if not self.validate_email(email):
                    self.tts.speak("Sir, that email format is invalid.")
                    return {
                        'success': False,
                        'error': 'Invalid email format'
                    }
                contact_to_update['email'] = email
            
            if 'category' in params:
                contact_to_update['category'] = params['category']
            if 'notes' in params:
                contact_to_update['notes'] = params['notes']
            
            contact_to_update['updated_at'] = datetime.now().strftime('%Y-%m-%d')
            
            # Update in list
            contacts_list[contact_index] = contact_to_update
            self.contacts['contacts'] = contacts_list
            
            # Save to file
            if self.save_contacts():
                self.tts.speak(f"Contact {contact_to_update['name']} updated successfully.")
                return {
                    'success': True,
                    'action': 'update',
                    'contact': contact_to_update
                }
            else:
                self.tts.speak("Failed to update contact.")
                return {
                    'success': False,
                    'error': 'Failed to save updated contact'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_contact(self, name, phone, email, params):
        """📞 Delete a contact"""
        try:
            contact_id = params.get('id')
            search_name = name
            
            if not contact_id and not search_name:
                self.tts.speak("Sir, which contact should I delete?")
                return {
                    'success': False,
                    'error': 'No contact identifier provided'
                }
            
            contacts_list = self.contacts.get('contacts', [])
            contact_to_delete = None
            
            # Find contact by ID or name
            for i, contact in enumerate(contacts_list):
                if (contact_id and contact.get('id') == contact_id) or \
                   (search_name and search_name.lower() in contact.get('name', '').lower()):
                    contact_to_delete = contact
                    del contacts_list[i]
                    break
            
            if not contact_to_delete:
                self.tts.speak("Sir, I couldn't find that contact.")
                return {
                    'success': False,
                    'error': 'Contact not found'
                }
            
            self.contacts['contacts'] = contacts_list
            
            # Save to file
            if self.save_contacts():
                self.tts.speak(f"Contact {contact_to_delete['name']} deleted successfully.")
                return {
                    'success': True,
                    'action': 'delete',
                    'contact': contact_to_delete
                }
            else:
                self.tts.speak("Failed to delete contact.")
                return {
                    'success': False,
                    'error': 'Failed to save after deletion'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_contacts(self, name, phone, email, params):
        """📞 List all contacts"""
        try:
            category = params.get('category', '')
            sort_by = params.get('sort_by', 'name')
            limit = params.get('limit', 20)
            
            contacts_list = self.contacts.get('contacts', [])
            
            # Filter by category if specified
            if category:
                contacts_list = [c for c in contacts_list if c.get('category', '').lower() == category.lower()]
            
            # Sort contacts
            if sort_by == 'name':
                contacts_list.sort(key=lambda x: x.get('name', '').lower())
            elif sort_by == 'date':
                contacts_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            count = len(contacts_list)
            
            if count == 0:
                self.tts.speak("You have no contacts saved.")
            else:
                self.tts.speak(f"You have {count} contacts saved.")
            
            return {
                'success': True,
                'action': 'list',
                'count': count,
                'contacts': contacts_list[:limit]
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def prepare_call(self, name, phone, email, params):
        """📞 Prepare to make a call"""
        try:
            if not name and not phone:
                self.tts.speak("Sir, who should I call?")
                return {
                    'success': False,
                    'error': 'No contact or phone number provided'
                }
            
            # If name provided, find contact
            if name:
                result = self.find_contact(name, '', '', {})
                if result['success']:
                    contact = result.get('contact') or (result.get('contacts', [])[0] if result.get('contacts') else None)
                    if contact and contact.get('phone'):
                        phone = contact['phone']
                        name = contact['name']
                    else:
                        self.tts.speak(f"Sir, {name} doesn't have a phone number saved.")
                        return {
                            'success': False,
                            'error': 'No phone number for contact'
                        }
                else:
                    self.tts.speak(f"Sir, I couldn't find {name} in your contacts.")
                    return result
            
            # Validate phone number
            if not self.validate_phone(phone):
                self.tts.speak("Sir, that phone number format is invalid.")
                return {
                    'success': False,
                    'error': 'Invalid phone number format'
                }
            
            self.tts.speak(f"Preparing to call {name or phone} at {phone}")
            
            # Return call preparation data
            return {
                'success': True,
                'action': 'call',
                'name': name,
                'phone': phone,
                'message': f'Call {name or phone} at {phone}'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def prepare_message(self, name, phone, email, params):
        """📞 Prepare to send a message"""
        try:
            message = params.get('message', '')
            
            if not name and not phone:
                self.tts.speak("Sir, who should I message?")
                return {
                    'success': False,
                    'error': 'No contact or phone number provided'
                }
            
            # If name provided, find contact
            if name:
                result = self.find_contact(name, '', '', {})
                if result['success']:
                    contact = result.get('contact') or (result.get('contacts', [])[0] if result.get('contacts') else None)
                    if contact and contact.get('phone'):
                        phone = contact['phone']
                        name = contact['name']
                    else:
                        self.tts.speak(f"Sir, {name} doesn't have a phone number saved.")
                        return {
                            'success': False,
                            'error': 'No phone number for contact'
                        }
                else:
                    self.tts.speak(f"Sir, I couldn't find {name} in your contacts.")
                    return result
            
            # Validate phone number
            if not self.validate_phone(phone):
                self.tts.speak("Sir, that phone number format is invalid.")
                return {
                    'success': False,
                    'error': 'Invalid phone number format'
                }
            
            self.tts.speak(f"Preparing message for {name or phone}")
            
            return {
                'success': True,
                'action': 'message',
                'name': name,
                'phone': phone,
                'message': message,
                'preview': f'Message to {name or phone}: {message}'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def prepare_email(self, name, phone, email, params):
        """📞 Prepare to send an email"""
        try:
            subject = params.get('subject', '')
            body = params.get('body', '')
            
            if not name and not email:
                self.tts.speak("Sir, who should I email?")
                return {
                    'success': False,
                    'error': 'No contact or email address provided'
                }
            
            # If name provided, find contact
            if name:
                result = self.find_contact(name, '', '', {})
                if result['success']:
                    contact = result.get('contact') or (result.get('contacts', [])[0] if result.get('contacts') else None)
                    if contact and contact.get('email'):
                        email = contact['email']
                        name = contact['name']
                    else:
                        self.tts.speak(f"Sir, {name} doesn't have an email address saved.")
                        return {
                            'success': False,
                            'error': 'No email for contact'
                        }
                else:
                    self.tts.speak(f"Sir, I couldn't find {name} in your contacts.")
                    return result
            
            # Validate email
            if not self.validate_email(email):
                self.tts.speak("Sir, that email format is invalid.")
                return {
                    'success': False,
                    'error': 'Invalid email format'
                }
            
            self.tts.speak(f"Preparing email for {name or email}")
            
            return {
                'success': True,
                'action': 'email',
                'name': name,
                'email': email,
                'subject': subject,
                'body': body,
                'preview': f'Email to {name or email}: {subject}'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def validate_phone(phone):
        """📞 Validate phone number format"""
        # Remove spaces, dashes, parentheses
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check for valid phone number patterns
        patterns = [
            r'^\+\d{10,15}$',  # International format
            r'^\d{10}$',        # US format without country code
            r'^\d{3}[\s\-]?\d{3}[\s\-]?\d{4}$'  # US format with separators
        ]
        
        for pattern in patterns:
            if re.match(pattern, clean_phone):
                return True
        
        return False
    
    @staticmethod
    def validate_email(email):
        """📞 Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def backup_contacts(self, backup_path=None):
        """📞 Create backup of contacts"""
        try:
            if not backup_path:
                backup_path = os.path.join('backups', f'contacts_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(self.contacts, f, indent=2)
            
            return {
                'success': True,
                'backup_path': backup_path,
                'size': os.path.getsize(backup_path)
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }