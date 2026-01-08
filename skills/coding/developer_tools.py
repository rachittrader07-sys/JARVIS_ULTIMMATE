"""
🛠️ Developer Tools
Provides various development utilities
"""

import os
import subprocess
import json
import webbrowser
import requests
from datetime import datetime
from colorama import Fore, Style

class DeveloperTools:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """🛠️ Execute developer tool command"""
        tool = params.get('tool', '').lower()
        action = params.get('action', '').lower()
        args = params.get('args', {})
        
        if not tool:
            self.tts.speak("Sir, kaunsa developer tool use karna hai?")
            return {'success': False, 'error': 'No tool specified'}
        
        print(Fore.YELLOW + f"🛠️ Using developer tool: {tool}" + Style.RESET_ALL)
        
        # Map tools to methods
        tool_map = {
            'git': self.git_tools,
            'docker': self.docker_tools,
            'npm': self.npm_tools,
            'pip': self.pip_tools,
            'system': self.system_tools,
            'web': self.web_tools,
            'database': self.database_tools,
            'api': self.api_tools,
            'format': self.format_code,
            'test': self.run_tests,
            'build': self.build_project,
            'deploy': self.deploy_project,
            'monitor': self.monitor_system,
            'search': self.search_docs
        }
        
        if tool in tool_map:
            return tool_map[tool](action, args)
        else:
            self.tts.speak(f"Sir, {tool} tool not available")
            return {
                'success': False,
                'error': f'Tool {tool} not found',
                'available_tools': list(tool_map.keys())
            }
    
    def git_tools(self, action, args):
        """🛠️ Git version control tools"""
        try:
            commands = {
                'init': 'git init',
                'clone': f'git clone {args.get("url", "")}',
                'status': 'git status',
                'add': f'git add {args.get("files", ".")}',
                'commit': f'git commit -m "{args.get("message", "Update")}"',
                'push': 'git push',
                'pull': 'git pull',
                'branch': f'git branch {args.get("name", "")}',
                'checkout': f'git checkout {args.get("branch", "")}',
                'merge': f'git merge {args.get("branch", "")}',
                'log': 'git log --oneline'
            }
            
            if action not in commands:
                self.tts.speak(f"Sir, {action} git command not recognized")
                return {
                    'success': False,
                    'error': f'Git action {action} not found',
                    'available_actions': list(commands.keys())
                }
            
            command = commands[action]
            print(Fore.CYAN + f"$ {command}" + Style.RESET_ALL)
            
            # Execute command
            if action in ['init', 'clone', 'add', 'commit', 'push', 'pull', 'branch', 'checkout', 'merge']:
                self.tts.speak(f"Executing git {action}")
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.tts.speak(f"Git {action} completed successfully")
                return {
                    'success': True,
                    'tool': 'git',
                    'action': action,
                    'output': result.stdout,
                    'command': command
                }
            else:
                self.tts.speak(f"Git {action} failed")
                return {
                    'success': False,
                    'tool': 'git',
                    'action': action,
                    'error': result.stderr,
                    'command': command
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def docker_tools(self, action, args):
        """🛠️ Docker container tools"""
        try:
            commands = {
                'build': f'docker build -t {args.get("tag", "myapp")} .',
                'run': f'docker run {args.get("options", "")} {args.get("image", "")}',
                'ps': 'docker ps',
                'images': 'docker images',
                'stop': f'docker stop {args.get("container", "")}',
                'rm': f'docker rm {args.get("container", "")}',
                'rmi': f'docker rmi {args.get("image", "")}',
                'logs': f'docker logs {args.get("container", "")}',
                'exec': f'docker exec -it {args.get("container", "")} {args.get("command", "bash")}',
                'compose': f'docker-compose {args.get("command", "up")}'
            }
            
            if action not in commands:
                self.tts.speak(f"Sir, {action} docker command not recognized")
                return {
                    'success': False,
                    'error': f'Docker action {action} not found',
                    'available_actions': list(commands.keys())
                }
            
            command = commands[action]
            print(Fore.CYAN + f"$ {command}" + Style.RESET_ALL)
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.tts.speak(f"Docker {action} completed successfully")
                return {
                    'success': True,
                    'tool': 'docker',
                    'action': action,
                    'output': result.stdout,
                    'command': command
                }
            else:
                self.tts.speak(f"Docker {action} failed")
                return {
                    'success': False,
                    'tool': 'docker',
                    'action': action,
                    'error': result.stderr,
                    'command': command
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def npm_tools(self, action, args):
        """🛠️ NPM package manager tools"""
        try:
            commands = {
                'init': 'npm init -y',
                'install': f'npm install {args.get("package", "")}',
                'uninstall': f'npm uninstall {args.get("package", "")}',
                'update': 'npm update',
                'start': 'npm start',
                'test': 'npm test',
                'build': 'npm run build',
                'audit': 'npm audit',
                'list': 'npm list',
                'outdated': 'npm outdated'
            }
            
            if action not in commands:
                return {
                    'success': False,
                    'error': f'NPM action {action} not found'
                }
            
            command = commands[action]
            print(Fore.CYAN + f"$ {command}" + Style.RESET_ALL)
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return {
                'success': result.returncode == 0,
                'tool': 'npm',
                'action': action,
                'output': result.stdout if result.returncode == 0 else result.stderr,
                'command': command
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def pip_tools(self, action, args):
        """🛠️ PIP package manager tools"""
        try:
            commands = {
                'install': f'pip install {args.get("package", "")}',
                'uninstall': f'pip uninstall {args.get("package", "")} -y',
                'freeze': 'pip freeze',
                'list': 'pip list',
                'update': f'pip install --upgrade {args.get("package", "")}',
                'search': f'pip search {args.get("package", "")}',
                'show': f'pip show {args.get("package", "")}'
            }
            
            if action not in commands:
                return {
                    'success': False,
                    'error': f'PIP action {action} not found'
                }
            
            command = commands[action]
            print(Fore.CYAN + f"$ {command}" + Style.RESET_ALL)
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            return {
                'success': result.returncode == 0,
                'tool': 'pip',
                'action': action,
                'output': result.stdout if result.returncode == 0 else result.stderr,
                'command': command
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def system_tools(self, action, args):
        """🛠️ System monitoring and management tools"""
        try:
            if action == 'processes':
                # Get running processes
                if os.name == 'nt':  # Windows
                    result = subprocess.run('tasklist', shell=True, capture_output=True, text=True)
                else:  # Linux/Mac
                    result = subprocess.run('ps aux', shell=True, capture_output=True, text=True)
                
                return {
                    'success': True,
                    'tool': 'system',
                    'action': action,
                    'output': result.stdout
                }
            
            elif action == 'disk':
                # Get disk usage
                if os.name == 'nt':
                    result = subprocess.run('wmic logicaldisk get size,freespace,caption', 
                                          shell=True, capture_output=True, text=True)
                else:
                    result = subprocess.run('df -h', shell=True, capture_output=True, text=True)
                
                return {
                    'success': True,
                    'tool': 'system',
                    'action': action,
                    'output': result.stdout
                }
            
            elif action == 'memory':
                # Get memory usage
                if os.name == 'nt':
                    result = subprocess.run('wmic OS get FreePhysicalMemory,TotalVisibleMemorySize', 
                                          shell=True, capture_output=True, text=True)
                else:
                    result = subprocess.run('free -h', shell=True, capture_output=True, text=True)
                
                return {
                    'success': True,
                    'tool': 'system',
                    'action': action,
                    'output': result.stdout
                }
            
            elif action == 'network':
                # Get network info
                if os.name == 'nt':
                    result = subprocess.run('ipconfig', shell=True, capture_output=True, text=True)
                else:
                    result = subprocess.run('ifconfig', shell=True, capture_output=True, text=True)
                
                return {
                    'success': True,
                    'tool': 'system',
                    'action': action,
                    'output': result.stdout
                }
            
            else:
                return {
                    'success': False,
                    'error': f'System action {action} not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def web_tools(self, action, args):
        """🛠️ Web development tools"""
        try:
            if action == 'check_status':
                url = args.get('url', 'https://google.com')
                try:
                    response = requests.get(url, timeout=5)
                    status = "online" if response.status_code == 200 else "offline"
                    
                    self.tts.speak(f"Website {url} is {status}")
                    
                    return {
                        'success': True,
                        'tool': 'web',
                        'action': action,
                        'url': url,
                        'status': response.status_code,
                        'status_text': status
                    }
                except:
                    self.tts.speak(f"Website {url} is offline")
                    return {
                        'success': False,
                        'tool': 'web',
                        'action': action,
                        'url': url,
                        'status': 'offline'
                    }
            
            elif action == 'open_browser':
                url = args.get('url', 'https://google.com')
                webbrowser.open(url)
                
                self.tts.speak(f"Opening {url} in browser")
                
                return {
                    'success': True,
                    'tool': 'web',
                    'action': action,
                    'url': url
                }
            
            elif action == 'screenshot':
                # Take webpage screenshot (requires selenium)
                try:
                    from selenium import webdriver
                    from selenium.webdriver.chrome.service import Service
                    
                    url = args.get('url', 'https://google.com')
                    driver = webdriver.Chrome()
                    driver.get(url)
                    driver.save_screenshot('screenshot.png')
                    driver.quit()
                    
                    return {
                        'success': True,
                        'tool': 'web',
                        'action': action,
                        'url': url,
                        'screenshot': 'screenshot.png'
                    }
                except:
                    return {
                        'success': False,
                        'error': 'Selenium not installed or Chrome driver not found'
                    }
            
            else:
                return {
                    'success': False,
                    'error': f'Web action {action} not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def database_tools(self, action, args):
        """🛠️ Database management tools"""
        try:
            if action == 'backup':
                db_type = args.get('type', 'sqlite')
                db_name = args.get('name', 'database.db')
                backup_name = args.get('backup', f'{db_name}.backup')
                
                if db_type == 'sqlite':
                    import shutil
                    shutil.copy2(db_name, backup_name)
                    
                    self.tts.speak(f"Database {db_name} backed up to {backup_name}")
                    
                    return {
                        'success': True,
                        'tool': 'database',
                        'action': action,
                        'type': db_type,
                        'database': db_name,
                        'backup': backup_name
                    }
            
            elif action == 'query':
                db_type = args.get('type', 'sqlite')
                query = args.get('query', 'SELECT 1')
                
                if db_type == 'sqlite':
                    import sqlite3
                    conn = sqlite3.connect(args.get('name', 'database.db'))
                    cursor = conn.cursor()
                    cursor.execute(query)
                    results = cursor.fetchall()
                    conn.close()
                    
                    return {
                        'success': True,
                        'tool': 'database',
                        'action': action,
                        'type': db_type,
                        'query': query,
                        'results': results
                    }
            
            else:
                return {
                    'success': False,
                    'error': f'Database action {action} not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def api_tools(self, action, args):
        """🛠️ API testing tools"""
        try:
            if action == 'test_endpoint':
                url = args.get('url', '')
                method = args.get('method', 'GET').upper()
                data = args.get('data', {})
                
                if not url:
                    return {
                        'success': False,
                        'error': 'URL required for API test'
                    }
                
                headers = args.get('headers', {'Content-Type': 'application/json'})
                
                if method == 'GET':
                    response = requests.get(url, headers=headers)
                elif method == 'POST':
                    response = requests.post(url, json=data, headers=headers)
                elif method == 'PUT':
                    response = requests.put(url, json=data, headers=headers)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers)
                else:
                    return {
                        'success': False,
                        'error': f'Method {method} not supported'
                    }
                
                self.tts.speak(f"API returned status {response.status_code}")
                
                return {
                    'success': True,
                    'tool': 'api',
                    'action': action,
                    'url': url,
                    'method': method,
                    'status': response.status_code,
                    'response': response.text
                }
            
            else:
                return {
                    'success': False,
                    'error': f'API action {action} not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def format_code(self, action, args):
        """🛠️ Code formatting tools"""
        try:
            file_path = args.get('file', '')
            
            if not file_path:
                return {
                    'success': False,
                    'error': 'File path required'
                }
            
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': f'File not found: {file_path}'
                }
            
            # Determine language based on file extension
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.py':
                # Format Python code with autopep8
                try:
                    import autopep8
                    with open(file_path, 'r') as f:
                        code = f.read()
                    
                    formatted_code = autopep8.fix_code(code)
                    
                    with open(file_path, 'w') as f:
                        f.write(formatted_code)
                    
                    self.tts.speak(f"Formatted Python file {file_path}")
                    
                    return {
                        'success': True,
                        'tool': 'format',
                        'action': 'format_python',
                        'file': file_path
                    }
                except ImportError:
                    # Try using black if available
                    try:
                        result = subprocess.run(f'black {file_path}', shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            self.tts.speak(f"Formatted Python file with black")
                            return {
                                'success': True,
                                'tool': 'format',
                                'action': 'format_python',
                                'file': file_path
                            }
                    except:
                        pass
                    
                    return {
                        'success': False,
                        'error': 'Python formatter not installed. Install autopep8 or black'
                    }
            
            elif ext == '.js' or ext == '.ts' or ext == '.jsx' or ext == '.tsx':
                # Format JavaScript/TypeScript with prettier
                try:
                    result = subprocess.run(f'npx prettier --write {file_path}', shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.tts.speak(f"Formatted JavaScript file {file_path}")
                        return {
                            'success': True,
                            'tool': 'format',
                            'action': 'format_javascript',
                            'file': file_path
                        }
                except:
                    pass
                
                return {
                    'success': False,
                    'error': 'Prettier not available for JavaScript formatting'
                }
            
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {ext}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_tests(self, action, args):
        """🛠️ Run tests"""
        try:
            test_path = args.get('path', '.')
            
            # Check for test files
            test_files = []
            for root, dirs, files in os.walk(test_path):
                for file in files:
                    if file.startswith('test_') and file.endswith('.py'):
                        test_files.append(os.path.join(root, file))
                    elif file.endswith('_test.py'):
                        test_files.append(os.path.join(root, file))
                    elif file == 'test.py':
                        test_files.append(os.path.join(root, file))
            
            if not test_files:
                # Try running pytest on directory
                result = subprocess.run(f'pytest {test_path}', shell=True, capture_output=True, text=True)
                
                self.tts.speak(f"Ran tests in {test_path}")
                
                return {
                    'success': result.returncode == 0 or result.returncode == 5,  # 5 means no tests found
                    'tool': 'test',
                    'action': 'run_pytest',
                    'path': test_path,
                    'output': result.stdout,
                    'exit_code': result.returncode
                }
            
            # Run specific test files
            for test_file in test_files:
                print(Fore.CYAN + f"Running tests in {test_file}" + Style.RESET_ALL)
                result = subprocess.run(f'python -m pytest {test_file} -v', shell=True, capture_output=True, text=True)
            
            self.tts.speak("Tests completed")
            
            return {
                'success': True,
                'tool': 'test',
                'action': 'run_tests',
                'test_files': test_files,
                'output': result.stdout if test_files else 'No tests found'
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def build_project(self, action, args):
        """🛠️ Build project"""
        try:
            project_type = args.get('type', 'python')
            build_dir = args.get('dir', '.')
            
            if project_type == 'python':
                # Create setup.py or pyproject.toml if not exists
                if not os.path.exists('setup.py') and not os.path.exists('pyproject.toml'):
                    setup_content = '''from setuptools import setup, find_packages

setup(
    name="your_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here
    ],
)
'''
                    with open('setup.py', 'w') as f:
                        f.write(setup_content)
                
                # Build wheel
                result = subprocess.run('python setup.py sdist bdist_wheel', shell=True, capture_output=True, text=True)
                
                self.tts.speak("Python project built successfully")
                
                return {
                    'success': result.returncode == 0,
                    'tool': 'build',
                    'action': 'build_python',
                    'output': result.stdout
                }
            
            elif project_type == 'web':
                # Check for package.json
                if os.path.exists('package.json'):
                    result = subprocess.run('npm run build', shell=True, capture_output=True, text=True)
                    
                    self.tts.speak("Web project built successfully")
                    
                    return {
                        'success': result.returncode == 0,
                        'tool': 'build',
                        'action': 'build_web',
                        'output': result.stdout
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No package.json found for web project'
                    }
            
            else:
                return {
                    'success': False,
                    'error': f'Project type {project_type} not supported'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def deploy_project(self, action, args):
        """🛠️ Deploy project"""
        try:
            platform = args.get('platform', 'local')
            project_dir = args.get('dir', '.')
            
            self.tts.speak(f"Starting deployment to {platform}")
            
            if platform == 'local':
                # Just run the project locally
                if os.path.exists('main.py'):
                    result = subprocess.run('python main.py', shell=True, capture_output=True, text=True)
                elif os.path.exists('app.py'):
                    result = subprocess.run('python app.py', shell=True, capture_output=True, text=True)
                elif os.path.exists('index.js'):
                    result = subprocess.run('node index.js', shell=True, capture_output=True, text=True)
                else:
                    return {
                        'success': False,
                        'error': 'No main entry point found'
                    }
                
                return {
                    'success': True,
                    'tool': 'deploy',
                    'action': 'deploy_local',
                    'output': result.stdout
                }
            
            else:
                return {
                    'success': False,
                    'error': f'Platform {platform} not supported yet'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def monitor_system(self, action, args):
        """🛠️ Monitor system resources"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.tts.speak(f"System status: CPU {cpu_percent} percent, Memory {memory.percent} percent used")
            
            return {
                'success': True,
                'tool': 'monitor',
                'action': 'system_status',
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_gb': memory.used / (1024**3),
                'memory_total_gb': memory.total / (1024**3),
                'disk_percent': disk.percent,
                'disk_free_gb': disk.free / (1024**3),
                'disk_total_gb': disk.total / (1024**3)
            }
                
        except ImportError:
            return {
                'success': False,
                'error': 'psutil library not installed'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_docs(self, action, args):
        """🛠️ Search documentation"""
        try:
            query = args.get('query', '')
            source = args.get('source', 'google')
            
            if not query:
                return {
                    'success': False,
                    'error': 'Search query required'
                }
            
            search_urls = {
                'google': f'https://www.google.com/search?q={query}+programming',
                'stackoverflow': f'https://stackoverflow.com/search?q={query}',
                'github': f'https://github.com/search?q={query}',
                'python': f'https://docs.python.org/3/search.html?q={query}',
                'mdn': f'https://developer.mozilla.org/search?q={query}'
            }
            
            url = search_urls.get(source, search_urls['google'])
            webbrowser.open(url)
            
            self.tts.speak(f"Searching {source} for {query}")
            
            return {
                'success': True,
                'tool': 'search',
                'action': 'search_docs',
                'query': query,
                'source': source,
                'url': url
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }