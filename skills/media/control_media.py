"""
🎵 Media Controller
Controls media playback and system volume
"""

import os
import sys
import time
import json
import subprocess
import platform
from pathlib import Path
from colorama import Fore, Style
from datetime import datetime

class MediaController:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        self.media_history_file = os.path.join('data', 'media_history.json')
        self.current_media = None
        self.volume_level = self.config.get('default_volume', 50)
        self.is_playing = False
        self.media_players = self.detect_media_players()
        
    def execute(self, params):
        """🎵 Execute media control command"""
        action = params.get('action', '').lower()
        media_path = params.get('path', '')
        media_url = params.get('url', '')
        volume = params.get('volume', self.volume_level)
        
        if not action:
            self.tts.speak("Sir, what media action should I perform?")
            return {'success': False, 'error': 'No action specified'}
        
        print(Fore.YELLOW + f"🎵 Media action: {action}" + Style.RESET_ALL)
        
        action_map = {
            'play': self.play_media,
            'pause': self.pause_media,
            'stop': self.stop_media,
            'resume': self.resume_media,
            'next': self.next_track,
            'previous': self.previous_track,
            'volume': self.set_volume,
            'mute': self.mute_volume,
            'unmute': self.unmute_volume,
            'status': self.get_status,
            'list': self.list_media,
            'search': self.search_media,
            'playlist': self.manage_playlist,
            'radio': self.play_radio,
            'podcast': self.play_podcast
        }
        
        if action in action_map:
            return action_map[action](
                path=media_path,
                url=media_url,
                volume=volume,
                params=params
            )
        else:
            self.tts.speak(f"Sir, {action} media action is not available")
            return {
                'success': False,
                'error': f'Action {action} not found',
                'available_actions': list(action_map.keys())
            }
    
    def detect_media_players(self):
        """🎵 Detect available media players on system"""
        players = {
            'vlc': {'available': False, 'path': ''},
            'mpv': {'available': False, 'path': ''},
            'mplayer': {'available': False, 'path': ''},
            'windows_media': {'available': False, 'path': ''},
            'ffplay': {'available': False, 'path': ''}
        }
        
        # Check for VLC
        vlc_paths = [
            'vlc',
            'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe',
            'C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe',
            '/usr/bin/vlc',
            '/usr/local/bin/vlc'
        ]
        
        for path in vlc_paths:
            try:
                subprocess.run([path, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                players['vlc'] = {'available': True, 'path': path}
                break
            except:
                continue
        
        # Check for MPV
        try:
            subprocess.run(['mpv', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            players['mpv'] = {'available': True, 'path': 'mpv'}
        except:
            pass
        
        # Check for MPlayer
        try:
            subprocess.run(['mplayer', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            players['mplayer'] = {'available': True, 'path': 'mplayer'}
        except:
            pass
        
        # Check for FFplay (part of FFmpeg)
        try:
            subprocess.run(['ffplay', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            players['ffplay'] = {'available': True, 'path': 'ffplay'}
        except:
            pass
        
        # Windows Media Player (Windows only)
        if platform.system() == 'Windows':
            wmp_path = 'C:\\Program Files\\Windows Media Player\\wmplayer.exe'
            if os.path.exists(wmp_path):
                players['windows_media'] = {'available': True, 'path': wmp_path}
        
        # Set default player
        for player_name, player_info in players.items():
            if player_info['available']:
                self.default_player = player_name
                break
        else:
            self.default_player = None
        
        return players
    
    def play_media(self, path='', url='', volume=50, params=None):
        """🎵 Play media file or URL"""
        try:
            media_source = path or url
            if not media_source:
                self.tts.speak("Sir, what should I play? Please provide a file path or URL.")
                return {
                    'success': False,
                    'error': 'No media source provided'
                }
            
            # Determine if it's a local file or URL
            is_url = media_source.startswith(('http://', 'https://', 'ftp://'))
            
            if not is_url and not os.path.exists(media_source):
                # Try to find the file in common media directories
                found_path = self.find_media_file(media_source)
                if found_path:
                    media_source = found_path
                else:
                    self.tts.speak(f"Sir, I couldn't find {media_source}")
                    return {
                        'success': False,
                        'error': 'Media file not found',
                        'source': media_source
                    }
            
            # Get player to use
            player_name = params.get('player', self.default_player) if params else self.default_player
            
            if not player_name or not self.media_players.get(player_name, {}).get('available'):
                self.tts.speak("Sir, no media player is available. Please install VLC or MPV.")
                return {
                    'success': False,
                    'error': 'No media player available'
                }
            
            player_path = self.media_players[player_name]['path']
            
            # Prepare command based on player
            if player_name == 'vlc':
                cmd = [player_path, '--play-and-exit', '--qt-start-minimized']
                if volume:
                    cmd.extend(['--volume', str(volume)])
                cmd.append(media_source)
            
            elif player_name == 'mpv':
                cmd = [player_path, '--no-video' if params and params.get('audio_only') else '', '--volume=' + str(volume)]
                cmd = [c for c in cmd if c]  # Remove empty strings
                cmd.append(media_source)
            
            elif player_name == 'ffplay':
                cmd = [player_path, '-nodisp', '-autoexit', '-volume', str(volume), media_source]
            
            elif player_name == 'windows_media':
                cmd = [player_path, '/Play', media_source]
            
            else:
                cmd = [player_path, media_source]
            
            # Start playback
            print(Fore.CYAN + f"▶️ Playing: {media_source}" + Style.RESET_ALL)
            print(Fore.CYAN + f"🔊 Volume: {volume}%" + Style.RESET_ALL)
            
            self.current_media = {
                'source': media_source,
                'player': player_name,
                'start_time': datetime.now(),
                'volume': volume,
                'is_url': is_url
            }
            
            self.is_playing = True
            
            # Start playback in background
            if params and params.get('background', True):
                subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(cmd)
            
            # Add to history
            self.add_to_history({
                'action': 'play',
                'source': media_source,
                'player': player_name,
                'volume': volume,
                'timestamp': datetime.now().isoformat()
            })
            
            media_name = os.path.basename(media_source) if not is_url else media_source
            self.tts.speak(f"Playing {media_name}")
            
            return {
                'success': True,
                'action': 'play',
                'source': media_source,
                'player': player_name,
                'volume': volume,
                'is_url': is_url,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def pause_media(self, path='', url='', volume=50, params=None):
        """🎵 Pause current media playback"""
        try:
            if not self.is_playing or not self.current_media:
                self.tts.speak("Sir, no media is currently playing.")
                return {
                    'success': False,
                    'error': 'No media playing'
                }
            
            # For VLC, we can send pause command
            if self.current_media['player'] == 'vlc':
                # Try to send pause command via RC interface
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect(('localhost', 4212))
                    sock.send(b'pause\n')
                    sock.close()
                except:
                    # Fallback: kill and remember position
                    pass
            
            self.is_playing = False
            self.current_media['paused_at'] = datetime.now()
            
            self.tts.speak("Media paused sir.")
            
            return {
                'success': True,
                'action': 'pause',
                'source': self.current_media['source'],
                'player': self.current_media['player']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def stop_media(self, path='', url='', volume=50, params=None):
        """🎵 Stop media playback"""
        try:
            if not self.is_playing and not self.current_media:
                self.tts.speak("Sir, no media is currently playing.")
                return {
                    'success': False,
                    'error': 'No media playing'
                }
            
            # Kill media player processes
            system_platform = platform.system()
            
            if system_platform == 'Windows':
                subprocess.run(['taskkill', '/F', '/IM', 'vlc.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['taskkill', '/F', '/IM', 'mpv.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['taskkill', '/F', '/IM', 'ffplay.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['taskkill', '/F', '/IM', 'wmplayer.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'vlc'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-f', 'mpv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-f', 'ffplay'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-f', 'mplayer'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Add to history
            if self.current_media:
                self.add_to_history({
                    'action': 'stop',
                    'source': self.current_media['source'],
                    'timestamp': datetime.now().isoformat()
                })
            
            self.current_media = None
            self.is_playing = False
            
            self.tts.speak("Media stopped sir.")
            
            return {
                'success': True,
                'action': 'stop'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def resume_media(self, path='', url='', volume=50, params=None):
        """🎵 Resume paused media"""
        try:
            if not self.current_media or self.is_playing:
                self.tts.speak("Sir, no media is paused or media is already playing.")
                return {
                    'success': False,
                    'error': 'No media to resume'
                }
            
            # Resume from the same source
            result = self.play_media(
                path=self.current_media['source'] if not self.current_media['is_url'] else '',
                url=self.current_media['source'] if self.current_media['is_url'] else '',
                volume=self.current_media.get('volume', 50),
                params={'player': self.current_media['player']}
            )
            
            if result['success']:
                self.tts.speak("Resuming media sir.")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def set_volume(self, path='', url='', volume=50, params=None):
        """🎵 Set system or player volume"""
        try:
            # Validate volume level
            volume = max(0, min(100, volume))
            
            system_platform = platform.system()
            
            if system_platform == 'Windows':
                # Windows volume control
                try:
                    import comtypes
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_control = interface.QueryInterface(IAudioEndpointVolume)
                    
                    # Convert percentage to scalar (0.0 to 1.0)
                    volume_scalar = volume / 100.0
                    volume_control.SetMasterVolumeLevelScalar(volume_scalar, None)
                    
                    self.volume_level = volume
                    
                    self.tts.speak(f"Volume set to {volume} percent sir.")
                    
                    return {
                        'success': True,
                        'action': 'volume',
                        'volume': volume,
                        'platform': 'windows'
                    }
                except ImportError:
                    # Fallback using nircmd if available
                    nircmd_path = os.path.join('tools', 'nircmd.exe')
                    if os.path.exists(nircmd_path):
                        subprocess.run([nircmd_path, 'setsysvolume', str(volume * 655)])
                        self.volume_level = volume
                        self.tts.speak(f"Volume set to {volume} percent sir.")
                        return {
                            'success': True,
                            'action': 'volume',
                            'volume': volume
                        }
                    else:
                        self.tts.speak("Sir, I cannot control volume on Windows. Please install pycaw library.")
                        return {
                            'success': False,
                            'error': 'Volume control not available on Windows'
                        }
            
            elif system_platform == 'Linux':
                # Linux volume control (using amixer or pactl)
                try:
                    # Try pactl first (PulseAudio)
                    subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume}%'], 
                                  check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    try:
                        # Try amixer (ALSA)
                        subprocess.run(['amixer', 'set', 'Master', f'{volume}%'], 
                                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except:
                        self.tts.speak("Sir, I cannot control volume on Linux.")
                        return {
                            'success': False,
                            'error': 'Volume control not available on Linux'
                        }
                
                self.volume_level = volume
                self.tts.speak(f"Volume set to {volume} percent sir.")
                
                return {
                    'success': True,
                    'action': 'volume',
                    'volume': volume,
                    'platform': 'linux'
                }
            
            elif system_platform == 'Darwin':  # macOS
                # macOS volume control
                try:
                    volume_applescript = f'set volume output volume {volume}'
                    subprocess.run(['osascript', '-e', volume_applescript], 
                                  check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    self.volume_level = volume
                    self.tts.speak(f"Volume set to {volume} percent sir.")
                    
                    return {
                        'success': True,
                        'action': 'volume',
                        'volume': volume,
                        'platform': 'macos'
                    }
                except:
                    self.tts.speak("Sir, I cannot control volume on macOS.")
                    return {
                        'success': False,
                        'error': 'Volume control not available on macOS'
                    }
            
            else:
                self.tts.speak(f"Sir, volume control not supported on {system_platform}")
                return {
                    'success': False,
                    'error': f'Unsupported platform: {system_platform}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def mute_volume(self, path='', url='', volume=50, params=None):
        """🎵 Mute system volume"""
        try:
            system_platform = platform.system()
            
            if system_platform == 'Windows':
                try:
                    import comtypes
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_control = interface.QueryInterface(IAudioEndpointVolume)
                    volume_control.SetMute(1, None)
                    
                    self.tts.speak("Volume muted sir.")
                    
                    return {
                        'success': True,
                        'action': 'mute',
                        'platform': 'windows'
                    }
                except ImportError:
                    nircmd_path = os.path.join('tools', 'nircmd.exe')
                    if os.path.exists(nircmd_path):
                        subprocess.run([nircmd_path, 'mutesysvolume', '1'])
                        self.tts.speak("Volume muted sir.")
                        return {'success': True, 'action': 'mute'}
            
            elif system_platform == 'Linux':
                try:
                    subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '1'], 
                                  check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    try:
                        subprocess.run(['amixer', 'set', 'Master', 'mute'], 
                                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except:
                        pass
                
                self.tts.speak("Volume muted sir.")
                return {'success': True, 'action': 'mute'}
            
            elif system_platform == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume output muted true'], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.tts.speak("Volume muted sir.")
                return {'success': True, 'action': 'mute'}
            
            self.tts.speak("Sir, I cannot mute volume on this system.")
            return {'success': False, 'error': 'Mute not available'}
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def unmute_volume(self, path='', url='', volume=50, params=None):
        """🎵 Unmute system volume"""
        try:
            system_platform = platform.system()
            
            if system_platform == 'Windows':
                try:
                    import comtypes
                    from comtypes import CLSCTX_ALL
                    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                    
                    devices = AudioUtilities.GetSpeakers()
                    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                    volume_control = interface.QueryInterface(IAudioEndpointVolume)
                    volume_control.SetMute(0, None)
                    
                    self.tts.speak("Volume unmuted sir.")
                    
                    return {
                        'success': True,
                        'action': 'unmute',
                        'platform': 'windows'
                    }
                except ImportError:
                    nircmd_path = os.path.join('tools', 'nircmd.exe')
                    if os.path.exists(nircmd_path):
                        subprocess.run([nircmd_path, 'mutesysvolume', '0'])
                        self.tts.speak("Volume unmuted sir.")
                        return {'success': True, 'action': 'unmute'}
            
            elif system_platform == 'Linux':
                try:
                    subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '0'], 
                                  check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except:
                    try:
                        subprocess.run(['amixer', 'set', 'Master', 'unmute'], 
                                      check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except:
                        pass
                
                self.tts.speak("Volume unmuted sir.")
                return {'success': True, 'action': 'unmute'}
            
            elif system_platform == 'Darwin':
                subprocess.run(['osascript', '-e', 'set volume output muted false'], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.tts.speak("Volume unmuted sir.")
                return {'success': True, 'action': 'unmute'}
            
            self.tts.speak("Sir, I cannot unmute volume on this system.")
            return {'success': False, 'error': 'Unmute not available'}
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_media_file(self, filename):
        """🎵 Search for media file in common directories"""
        media_extensions = ['.mp3', '.mp4', '.avi', '.mkv', '.wav', '.flac', '.m4a', '.wma']
        
        # Common media directories
        search_dirs = [
            os.path.expanduser('~'),
            os.path.expanduser('~/Music'),
            os.path.expanduser('~/Videos'),
            os.path.expanduser('~/Downloads'),
            os.path.expanduser('~/Desktop'),
            'C:\\Users\\Public\\Music',
            'C:\\Users\\Public\\Videos',
            '/Music',
            '/Videos'
        ]
        
        # Also search in current directory
        if os.path.exists(filename):
            return filename
        
        # Search in directories
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                for root, dirs, files in os.walk(search_dir):
                    for file in files:
                        if filename.lower() in file.lower() and any(file.endswith(ext) for ext in media_extensions):
                            return os.path.join(root, file)
        
        return None
    
    def add_to_history(self, entry):
        """🎵 Add media action to history"""
        try:
            history = []
            if os.path.exists(self.media_history_file):
                with open(self.media_history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            # Keep only last 100 entries
            history.append(entry)
            if len(history) > 100:
                history = history[-100:]
            
            with open(self.media_history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(Fore.RED + f"Error saving media history: {e}" + Style.RESET_ALL)