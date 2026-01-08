"""
🎵 Music Player
Specialized music playback functionality
"""

import os
import json
import random
import subprocess
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

class MusicPlayer:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.playlists_file = os.path.join('data', 'playlists.json')
        self.playlists = self.load_playlists()
        self.current_playlist = None
        self.current_track_index = 0
        self.shuffle_mode = False
        self.repeat_mode = False
        
    def execute(self, params):
        """🎵 Execute music player command"""
        action = params.get('action', '').lower()
        playlist = params.get('playlist', '')
        song = params.get('song', '')
        genre = params.get('genre', '')
        
        print(Fore.YELLOW + f"🎵 Music action: {action}" + Style.RESET_ALL)
        
        action_map = {
            'play': self.play_music,
            'play_playlist': self.play_playlist,
            'play_genre': self.play_genre,
            'play_artist': self.play_artist,
            'play_album': self.play_album,
            'shuffle': self.toggle_shuffle,
            'repeat': self.toggle_repeat,
            'next': self.next_song,
            'previous': self.previous_song,
            'create_playlist': self.create_playlist,
            'add_to_playlist': self.add_to_playlist,
            'remove_from_playlist': self.remove_from_playlist,
            'list_playlists': self.list_playlists,
            'list_songs': self.list_songs,
            'current': self.current_song,
            'lyrics': self.get_lyrics
        }
        
        if action in action_map:
            return action_map[action](
                playlist=playlist,
                song=song,
                genre=genre,
                params=params
            )
        else:
            self.tts.speak(f"Sir, {action} music action is not available")
            return {
                'success': False,
                'error': f'Action {action} not found',
                'available_actions': list(action_map.keys())
            }
    
    def load_playlists(self):
        """🎵 Load playlists from JSON file"""
        try:
            if os.path.exists(self.playlists_file):
                with open(self.playlists_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                default_playlists = {
                    'playlists': {
                        'favorites': {
                            'name': 'Favorites',
                            'songs': [],
                            'created': datetime.now().isoformat()
                        }
                    },
                    'settings': {
                        'auto_save': True,
                        'default_volume': 70
                    }
                }
                
                # Create data directory if it doesn't exist
                os.makedirs('data', exist_ok=True)
                
                with open(self.playlists_file, 'w', encoding='utf-8') as f:
                    json.dump(default_playlists, f, indent=2)
                
                return default_playlists
                
        except Exception as e:
            print(Fore.RED + f"Error loading playlists: {e}" + Style.RESET_ALL)
            return {'playlists': {}, 'settings': {}}
    
    def save_playlists(self):
        """🎵 Save playlists to JSON file"""
        try:
            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.playlists, f, indent=2)
            return True
        except Exception as e:
            print(Fore.RED + f"Error saving playlists: {e}" + Style.RESET_ALL)
            return False
    
    def play_music(self, playlist='', song='', genre='', params=None):
        """🎵 Play music file or search for music"""
        try:
            if song:
                # Play specific song
                return self.play_specific_song(song, params)
            elif playlist:
                # Play playlist
                return self.play_playlist(playlist, '', '', params)
            elif genre:
                # Play by genre
                return self.play_genre(genre, '', '', params)
            else:
                # Play random music from library
                return self.play_random_music(params)
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def play_specific_song(self, song_query, params):
        """🎵 Play a specific song"""
        try:
            # Search for song in music library
            music_library = self.get_music_library()
            found_songs = []
            
            for song_path in music_library:
                song_name = os.path.basename(song_path)
                if song_query.lower() in song_name.lower():
                    found_songs.append(song_path)
            
            if not found_songs:
                self.tts.speak(f"Sir, I couldn't find {song_query} in your music library.")
                return {
                    'success': False,
                    'error': 'Song not found',
                    'query': song_query
                }
            
            # Play first found song or let user choose
            song_to_play = found_songs[0]
            
            if len(found_songs) > 1:
                self.tts.speak(f"Found {len(found_songs)} songs. Playing {os.path.basename(song_to_play)}")
            
            # Use MediaController to play the song
            from .control_media import MediaController
            media_controller = MediaController(self.config, self.tts)
            
            result = media_controller.play_media(
                path=song_to_play,
                volume=params.get('volume', 70) if params else 70
            )
            
            if result['success']:
                self.tts.speak(f"Playing {os.path.basename(song_to_play)}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def play_playlist(self, playlist='', song='', genre='', params=None):
        """🎵 Play a playlist"""
        try:
            playlist_name = playlist.lower()
            
            if playlist_name not in self.playlists.get('playlists', {}):
                self.tts.speak(f"Sir, playlist {playlist} not found.")
                return {
                    'success': False,
                    'error': 'Playlist not found',
                    'playlist': playlist
                }
            
            playlist_data = self.playlists['playlists'][playlist_name]
            songs = playlist_data.get('songs', [])
            
            if not songs:
                self.tts.speak(f"Playlist {playlist} is empty.")
                return {
                    'success': False,
                    'error': 'Playlist empty',
                    'playlist': playlist
                }
            
            self.current_playlist = playlist_name
            self.current_track_index = 0
            
            # Apply shuffle if enabled
            if self.shuffle_mode:
                random.shuffle(songs)
                playlist_data['songs'] = songs
            
            # Play first song in playlist
            first_song = songs[0]
            
            from .control_media import MediaController
            media_controller = MediaController(self.config, self.tts)
            
            result = media_controller.play_media(
                path=first_song,
                volume=params.get('volume', 70) if params else 70
            )
            
            if result['success']:
                self.tts.speak(f"Playing playlist {playlist_data['name']}. {len(songs)} songs.")
            
            return {
                'success': True,
                'action': 'play_playlist',
                'playlist': playlist_data['name'],
                'song_count': len(songs),
                'current_song': first_song
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def play_genre(self, genre='', song='', playlist='', params=None):
        """🎵 Play music by genre"""
        try:
            # This is a simplified implementation
            # In a real system, you would have genre metadata for songs
            
            self.tts.speak(f"Playing {genre} music")
            
            # For now, play random music
            return self.play_random_music(params)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def play_random_music(self, params):
        """🎵 Play random music from library"""
        try:
            music_library = self.get_music_library()
            
            if not music_library:
                self.tts.speak("Sir, your music library is empty.")
                return {
                    'success': False,
                    'error': 'Music library empty'
                }
            
            # Select random song
            random_song = random.choice(music_library)
            
            from .control_media import MediaController
            media_controller = MediaController(self.config, self.tts)
            
            result = media_controller.play_media(
                path=random_song,
                volume=params.get('volume', 70) if params else 70
            )
            
            if result['success']:
                song_name = os.path.basename(random_song)
                self.tts.speak(f"Playing random song: {song_name}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def toggle_shuffle(self, playlist='', song='', genre='', params=None):
        """🎵 Toggle shuffle mode"""
        self.shuffle_mode = not self.shuffle_mode
        
        status = "enabled" if self.shuffle_mode else "disabled"
        self.tts.speak(f"Shuffle mode {status} sir.")
        
        return {
            'success': True,
            'action': 'shuffle',
            'shuffle_mode': self.shuffle_mode,
            'status': status
        }
    
    def toggle_repeat(self, playlist='', song='', genre='', params=None):
        """🎵 Toggle repeat mode"""
        self.repeat_mode = not self.repeat_mode
        
        status = "enabled" if self.repeat_mode else "disabled"
        self.tts.speak(f"Repeat mode {status} sir.")
        
        return {
            'success': True,
            'action': 'repeat',
            'repeat_mode': self.repeat_mode,
            'status': status
        }
    
    def next_song(self, playlist='', song='', genre='', params=None):
        """🎵 Play next song in playlist"""
        try:
            if not self.current_playlist:
                self.tts.speak("Sir, no playlist is currently playing.")
                return {
                    'success': False,
                    'error': 'No active playlist'
                }
            
            playlist_data = self.playlists['playlists'][self.current_playlist]
            songs = playlist_data.get('songs', [])
            
            if not songs:
                self.tts.speak("Playlist is empty.")
                return {
                    'success': False,
                    'error': 'Playlist empty'
                }
            
            # Move to next song
            self.current_track_index += 1
            
            # Check bounds
            if self.current_track_index >= len(songs):
                if self.repeat_mode:
                    self.current_track_index = 0
                else:
                    self.tts.speak("End of playlist reached.")
                    return {
                        'success': False,
                        'error': 'End of playlist',
                        'playlist': self.current_playlist
                    }
            
            next_song = songs[self.current_track_index]
            
            from .control_media import MediaController
            media_controller = MediaController(self.config, self.tts)
            
            result = media_controller.play_media(path=next_song)
            
            if result['success']:
                self.tts.speak(f"Playing next song: {os.path.basename(next_song)}")
            
            return {
                'success': True,
                'action': 'next',
                'current_song': next_song,
                'track_number': self.current_track_index + 1,
                'total_tracks': len(songs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def previous_song(self, playlist='', song='', genre='', params=None):
        """🎵 Play previous song in playlist"""
        try:
            if not self.current_playlist:
                self.tts.speak("Sir, no playlist is currently playing.")
                return {
                    'success': False,
                    'error': 'No active playlist'
                }
            
            playlist_data = self.playlists['playlists'][self.current_playlist]
            songs = playlist_data.get('songs', [])
            
            if not songs:
                self.tts.speak("Playlist is empty.")
                return {
                    'success': False,
                    'error': 'Playlist empty'
                }
            
            # Move to previous song
            self.current_track_index -= 1
            
            # Check bounds
            if self.current_track_index < 0:
                if self.repeat_mode:
                    self.current_track_index = len(songs) - 1
                else:
                    self.tts.speak("Beginning of playlist reached.")
                    return {
                        'success': False,
                        'error': 'Beginning of playlist',
                        'playlist': self.current_playlist
                    }
            
            prev_song = songs[self.current_track_index]
            
            from .control_media import MediaController
            media_controller = MediaController(self.config, self.tts)
            
            result = media_controller.play_media(path=prev_song)
            
            if result['success']:
                self.tts.speak(f"Playing previous song: {os.path.basename(prev_song)}")
            
            return {
                'success': True,
                'action': 'previous',
                'current_song': prev_song,
                'track_number': self.current_track_index + 1,
                'total_tracks': len(songs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_playlist(self, playlist='', song='', genre='', params=None):
        """🎵 Create a new playlist"""
        try:
            if not playlist:
                self.tts.speak("Sir, what should I name the new playlist?")
                return {
                    'success': False,
                    'error': 'No playlist name provided'
                }
            
            playlist_key = playlist.lower().replace(' ', '_')
            
            if playlist_key in self.playlists.get('playlists', {}):
                self.tts.speak(f"Sir, playlist {playlist} already exists.")
                return {
                    'success': False,
                    'error': 'Playlist already exists',
                    'playlist': playlist
                }
            
            # Create new playlist
            self.playlists['playlists'][playlist_key] = {
                'name': playlist,
                'songs': [],
                'created': datetime.now().isoformat(),
                'description': params.get('description', '') if params else ''
            }
            
            if self.save_playlists():
                self.tts.speak(f"Playlist {playlist} created successfully.")
                return {
                    'success': True,
                    'action': 'create_playlist',
                    'playlist': playlist,
                    'playlist_key': playlist_key
                }
            else:
                self.tts.speak("Failed to create playlist.")
                return {
                    'success': False,
                    'error': 'Failed to save playlist'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def add_to_playlist(self, playlist='', song='', genre='', params=None):
        """🎵 Add song to playlist"""
        try:
            if not playlist:
                self.tts.speak("Sir, which playlist should I add to?")
                return {
                    'success': False,
                    'error': 'No playlist specified'
                }
            
            playlist_key = playlist.lower().replace(' ', '_')
            
            if playlist_key not in self.playlists.get('playlists', {}):
                self.tts.speak(f"Sir, playlist {playlist} doesn't exist.")
                return {
                    'success': False,
                    'error': 'Playlist not found',
                    'playlist': playlist
                }
            
            if not song:
                self.tts.speak("Sir, which song should I add?")
                return {
                    'success': False,
                    'error': 'No song specified'
                }
            
            # Find the song
            music_library = self.get_music_library()
            found_songs = []
            
            for song_path in music_library:
                song_name = os.path.basename(song_path)
                if song.lower() in song_name.lower():
                    found_songs.append(song_path)
            
            if not found_songs:
                self.tts.speak(f"Sir, I couldn't find {song} in your music library.")
                return {
                    'success': False,
                    'error': 'Song not found',
                    'song': song
                }
            
            # Add first matching song to playlist
            song_to_add = found_songs[0]
            playlist_data = self.playlists['playlists'][playlist_key]
            
            # Check if song already in playlist
            if song_to_add in playlist_data.get('songs', []):
                self.tts.speak(f"{song} is already in the playlist.")
                return {
                    'success': False,
                    'error': 'Song already in playlist',
                    'song': song_to_add
                }
            
            playlist_data.setdefault('songs', []).append(song_to_add)
            
            if self.save_playlists():
                self.tts.speak(f"Added {os.path.basename(song_to_add)} to playlist {playlist}.")
                return {
                    'success': True,
                    'action': 'add_to_playlist',
                    'playlist': playlist,
                    'song': song_to_add
                }
            else:
                self.tts.speak("Failed to add song to playlist.")
                return {
                    'success': False,
                    'error': 'Failed to save playlist'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def get_music_library():
        """🎵 Get list of all music files"""
        music_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.wma', '.ogg', '.aac']
        music_library = []
        
        # Common music directories
        music_dirs = [
            os.path.expanduser('~/Music'),
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop'),
            'C:\\Users\\Public\\Music',
            '/Music',
            '/home/*/Music'
        ]
        
        for music_dir in music_dirs:
            if os.path.exists(music_dir):
                for root, dirs, files in os.walk(music_dir):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in music_extensions):
                            music_library.append(os.path.join(root, file))
        
        return music_library
    
    def list_playlists(self, playlist='', song='', genre='', params=None):
        """🎵 List all playlists"""
        try:
            playlists_data = self.playlists.get('playlists', {})
            
            if not playlists_data:
                self.tts.speak("You have no playlists.")
                return {
                    'success': True,
                    'action': 'list_playlists',
                    'count': 0,
                    'playlists': []
                }
            
            playlist_list = []
            for key, data in playlists_data.items():
                playlist_list.append({
                    'name': data['name'],
                    'song_count': len(data.get('songs', [])),
                    'created': data.get('created', ''),
                    'key': key
                })
            
            count = len(playlist_list)
            
            if count == 1:
                self.tts.speak(f"You have 1 playlist: {playlist_list[0]['name']}")
            else:
                playlist_names = [p['name'] for p in playlist_list[:3]]
                self.tts.speak(f"You have {count} playlists: {', '.join(playlist_names)}")
            
            return {
                'success': True,
                'action': 'list_playlists',
                'count': count,
                'playlists': playlist_list
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_songs(self, playlist='', song='', genre='', params=None):
        """🎵 List songs in playlist or library"""
        try:
            if playlist:
                # List songs in specific playlist
                playlist_key = playlist.lower().replace(' ', '_')
                
                if playlist_key not in self.playlists.get('playlists', {}):
                    self.tts.speak(f"Sir, playlist {playlist} not found.")
                    return {
                        'success': False,
                        'error': 'Playlist not found'
                    }
                
                playlist_data = self.playlists['playlists'][playlist_key]
                songs = playlist_data.get('songs', [])
                
                if not songs:
                    self.tts.speak(f"Playlist {playlist} is empty.")
                    return {
                        'success': True,
                        'action': 'list_songs',
                        'playlist': playlist,
                        'count': 0,
                        'songs': []
                    }
                
                song_names = [os.path.basename(s) for s in songs[:5]]  # Show first 5
                self.tts.speak(f"Playlist {playlist} has {len(songs)} songs. First few: {', '.join(song_names)}")
                
                return {
                    'success': True,
                    'action': 'list_songs',
                    'playlist': playlist,
                    'count': len(songs),
                    'songs': songs[:10]  # Return first 10
                }
            else:
                # List all songs in library
                music_library = self.get_music_library()
                
                if not music_library:
                    self.tts.speak("Your music library is empty.")
                    return {
                        'success': True,
                        'action': 'list_songs',
                        'count': 0,
                        'songs': []
                    }
                
                self.tts.speak(f"You have {len(music_library)} songs in your library.")
                
                return {
                    'success': True,
                    'action': 'list_songs',
                    'count': len(music_library),
                    'songs': music_library[:10]  # Return first 10
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def current_song(self, playlist='', song='', genre='', params=None):
        """🎵 Get current playing song info"""
        try:
            if not self.current_playlist:
                self.tts.speak("No music is currently playing.")
                return {
                    'success': False,
                    'error': 'No music playing'
                }
            
            playlist_data = self.playlists['playlists'][self.current_playlist]
            songs = playlist_data.get('songs', [])
            
            if self.current_track_index < 0 or self.current_track_index >= len(songs):
                self.tts.speak("Current song index is invalid.")
                return {
                    'success': False,
                    'error': 'Invalid track index'
                }
            
            current_song = songs[self.current_track_index]
            song_name = os.path.basename(current_song)
            
            self.tts.speak(f"Currently playing: {song_name}. Track {self.current_track_index + 1} of {len(songs)}.")
            
            return {
                'success': True,
                'action': 'current',
                'song': current_song,
                'song_name': song_name,
                'track_number': self.current_track_index + 1,
                'total_tracks': len(songs),
                'playlist': playlist_data['name']
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_lyrics(self, playlist='', song='', genre='', params=None):
        """🎵 Get lyrics for current song"""
        try:
            self.tts.speak("Lyrics feature is not implemented yet sir.")
            return {
                'success': False,
                'error': 'Feature not implemented',
                'message': 'Lyrics functionality coming soon'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }