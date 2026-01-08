"""
💻 Code Writer Skill
Helps with coding tasks
"""

import pyautogui
import time
import os
from colorama import Fore, Style

class CodeWriter:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """💻 Execute coding assistance"""
        query = params.get('query', '').lower()
        language = params.get('language', 'python')
        
        if not query:
            self.tts.speak("Sir, what code should I write?")
            return {'success': False, 'error': 'No query'}
        
        print(Fore.YELLOW + f"💻 Coding: {query}" + Style.RESET_ALL)
        
        # Open code editor if not already open
        editor_open = self.open_code_editor()
        
        if not editor_open['success']:
            return editor_open
        
        # Type code based on query
        if 'hello' in query or 'print' in query:
            return self.write_hello_world(language)
        elif 'loop' in query or 'for' in query:
            return self.write_loop(language)
        elif 'function' in query or 'def' in query:
            return self.write_function(language)
        elif 'class' in query or 'object' in query:
            return self.write_class(language)
        elif 'file' in query or 'read' in query or 'write' in query:
            return self.write_file_operation(language)
        elif 'web' in query or 'scrape' in query:
            return self.write_web_scraper(language)
        elif 'database' in query or 'sql' in query or 'db' in query:
            return self.write_database_code(language)
        elif 'api' in query or 'rest' in query:
            return self.write_api_code(language)
        elif 'test' in query or 'unit test' in query:
            return self.write_test_code(language)
        else:
            return self.write_general_code(query, language)
    
    def open_code_editor(self):
        """💻 Open code editor"""
        try:
            # Try to open VS Code
            import subprocess
            
            vscode_paths = [
                "code",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                os.path.expanduser("~\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"),
                "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            ]
            
            for path in vscode_paths:
                try:
                    expanded_path = os.path.expandvars(path)
                    subprocess.Popen(expanded_path, shell=True)
                    time.sleep(2)  # Wait for editor to open
                    
                    print(Fore.GREEN + "✅ Code editor opened" + Style.RESET_ALL)
                    
                    return {
                        'success': True,
                        'editor': 'vscode'
                    }
                except:
                    continue
            
            # Try Notepad++ as fallback
            try:
                subprocess.Popen("notepad++", shell=True)
                time.sleep(2)
                
                return {
                    'success': True,
                    'editor': 'notepad++',
                    'fallback': True
                }
            except:
                pass
            
            # Try regular Notepad
            try:
                subprocess.Popen("notepad", shell=True)
                time.sleep(2)
                
                return {
                    'success': True,
                    'editor': 'notepad',
                    'fallback': True
                }
            except:
                pass
            
            return {
                'success': False,
                'error': 'No code editor found'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_hello_world(self, language):
        """💻 Write Hello World program"""
        try:
            code_map = {
                'python': 'print("Hello, World!")\n',
                'java': 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n',
                'javascript': 'console.log("Hello, World!");\n',
                'c': '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}\n',
                'cpp': '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}\n',
                'csharp': 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}\n',
                'php': '<?php\necho "Hello, World!";\n?>\n',
                'ruby': 'puts "Hello, World!"\n',
                'swift': 'print("Hello, World!")\n'
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a Hello World program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'hello_world',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_loop(self, language):
        """💻 Write loop program"""
        try:
            code_map = {
                'python': 'for i in range(10):\n    print(f"Number: {i}")\n',
                'java': 'for (int i = 0; i < 10; i++) {\n    System.out.println("Number: " + i);\n}\n',
                'javascript': 'for (let i = 0; i < 10; i++) {\n    console.log(`Number: ${i}`);\n}\n',
                'c': 'for (int i = 0; i < 10; i++) {\n    printf("Number: %d\\n", i);\n}\n',
                'cpp': 'for (int i = 0; i < 10; i++) {\n    std::cout << "Number: " << i << std::endl;\n}\n',
                'php': 'for ($i = 0; $i < 10; $i++) {\n    echo "Number: $i\\n";\n}\n'
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a loop program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'loop',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_function(self, language):
        """💻 Write function program"""
        try:
            code_map = {
                'python': 'def add_numbers(a, b):\n    """Add two numbers"""\n    return a + b\n\n# Example usage\nresult = add_numbers(5, 3)\nprint(f"Result: {result}")\n',
                'java': 'public class Calculator {\n    public static int addNumbers(int a, int b) {\n        return a + b;\n    }\n    \n    public static void main(String[] args) {\n        int result = addNumbers(5, 3);\n        System.out.println("Result: " + result);\n    }\n}\n',
                'javascript': 'function addNumbers(a, b) {\n    return a + b;\n}\n\n// Example usage\nconst result = addNumbers(5, 3);\nconsole.log(`Result: ${result}`);\n',
                'c': '#include <stdio.h>\n\nint addNumbers(int a, int b) {\n    return a + b;\n}\n\nint main() {\n    int result = addNumbers(5, 3);\n    printf("Result: %d\\n", result);\n    return 0;\n}\n'
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a function program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'function',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_class(self, language):
        """💻 Write class program"""
        try:
            code_map = {
                'python': 'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n    \n    def introduce(self):\n        return f"Hi, I\'m {self.name} and I\'m {self.age} years old."\n\n# Example usage\nperson = Person("John", 30)\nprint(person.introduce())\n',
                'java': 'public class Person {\n    private String name;\n    private int age;\n    \n    public Person(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n    \n    public String introduce() {\n        return "Hi, I\'m " + name + " and I\'m " + age + " years old.";\n    }\n    \n    public static void main(String[] args) {\n        Person person = new Person("John", 30);\n        System.out.println(person.introduce());\n    }\n}\n',
                'javascript': 'class Person {\n    constructor(name, age) {\n        this.name = name;\n        this.age = age;\n    }\n    \n    introduce() {\n        return `Hi, I\'m ${this.name} and I\'m ${this.age} years old.`;\n    }\n}\n\n// Example usage\nconst person = new Person("John", 30);\nconsole.log(person.introduce());\n',
                'csharp': 'using System;\n\npublic class Person {\n    public string Name { get; set; }\n    public int Age { get; set; }\n    \n    public Person(string name, int age) {\n        Name = name;\n        Age = age;\n    }\n    \n    public string Introduce() {\n        return $"Hi, I\'m {Name} and I\'m {Age} years old.";\n    }\n}\n\nclass Program {\n    static void Main() {\n        Person person = new Person("John", 30);\n        Console.WriteLine(person.Introduce());\n    }\n}\n'
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a class program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'class',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_file_operation(self, language):
        """💻 Write file operation program"""
        try:
            code_map = {
                'python': '# Write to file\nwith open("example.txt", "w") as file:\n    file.write("Hello, World!\\n")\n\n# Read from file\nwith open("example.txt", "r") as file:\n    content = file.read()\n    print(content)\n',
                'java': 'import java.io.*;\n\npublic class FileExample {\n    public static void main(String[] args) {\n        try {\n            // Write to file\n            FileWriter writer = new FileWriter("example.txt");\n            writer.write("Hello, World!\\n");\n            writer.close();\n            \n            // Read from file\n            BufferedReader reader = new BufferedReader(new FileReader("example.txt"));\n            String line = reader.readLine();\n            System.out.println(line);\n            reader.close();\n        } catch (IOException e) {\n            e.printStackTrace();\n        }\n    }\n}\n',
                'javascript': 'const fs = require(\'fs\');\n\n// Write to file\nfs.writeFileSync(\'example.txt\', \'Hello, World!\\n\');\n\n// Read from file\nconst content = fs.readFileSync(\'example.txt\', \'utf8\');\nconsole.log(content);\n'
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a file operation program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'file_operation',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_web_scraper(self, language):
        """💻 Write web scraper program"""
        try:
            code_map = {
                'python': '''# Web scraper example
import requests
from bs4 import BeautifulSoup

# Send request
url = "https://example.com"
response = requests.get(url)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extract data
title = soup.title.string
print(f"Title: {title}")

# Find all links
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
''',
                'javascript': '''// Web scraper example using Node.js with axios and cheerio
const axios = require('axios');
const cheerio = require('cheerio');

async function scrapeWebsite() {
    try {
        const response = await axios.get('https://example.com');
        const $ = cheerio.load(response.data);
        
        // Extract title
        const title = $('title').text();
        console.log(`Title: ${title}`);
        
        // Extract all links
        $('a').each((index, element) => {
            const link = $(element).attr('href');
            console.log(link);
        });
    } catch (error) {
        console.error('Error scraping website:', error);
    }
}

scrapeWebsite();
'''
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written a web scraper program in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'web_scraper',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_database_code(self, language):
        """💻 Write database operation code"""
        try:
            code_map = {
                'python': '''# Database connection example
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# Insert data
cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
               ('John Doe', 'john@example.com'))

# Query data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)

# Commit and close
conn.commit()
conn.close()
''',
                'javascript': '''// Database example using Node.js and SQLite
const sqlite3 = require('sqlite3').verbose();

// Open database
const db = new sqlite3.Database('./example.db');

// Create table
db.run(\`
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
\`, (err) => {
    if (err) {
        console.error('Error creating table:', err);
    }
});

// Insert data
db.run("INSERT INTO users (name, email) VALUES (?, ?)", 
       ['John Doe', 'john@example.com'], function(err) {
    if (err) {
        console.error('Error inserting data:', err);
    }
});

// Query data
db.all("SELECT * FROM users", [], (err, rows) => {
    if (err) {
        console.error('Error querying data:', err);
    }
    rows.forEach((row) => {
        console.log(row);
    });
});

// Close database
db.close();
'''
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written database code in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'database',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_api_code(self, language):
        """💻 Write API code"""
        try:
            code_map = {
                'python': '''# FastAPI example
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return item

# To run: uvicorn main:app --reload
''',
                'javascript': '''// Express.js API example
const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
    res.json({ message: 'Hello World!' });
});

app.get('/items/:id', (req, res) => {
    const { id } = req.params;
    const { q } = req.query;
    res.json({ item_id: id, query: q });
});

app.post('/items', (req, res) => {
    const item = req.body;
    res.json(item);
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
'''
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written API code in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'api',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_test_code(self, language):
        """💻 Write test code"""
        try:
            code_map = {
                'python': '''# Unit test example
import unittest

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class TestMathFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
    
    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 5), -5)
        self.assertEqual(multiply(0, 10), 0)

if __name__ == '__main__':
    unittest.main()
''',
                'javascript': '''// Jest test example
function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}

// Tests
describe('Math functions', () => {
    test('adds 2 + 3 to equal 5', () => {
        expect(add(2, 3)).toBe(5);
    });
    
    test('adds -1 + 1 to equal 0', () => {
        expect(add(-1, 1)).toBe(0);
    });
    
    test('multiplies 2 * 3 to equal 6', () => {
        expect(multiply(2, 3)).toBe(6);
    });
});
'''
            }
            
            code = code_map.get(language.lower(), code_map['python'])
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've written test code in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'test',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def write_general_code(self, query, language):
        """💻 Write general code based on query"""
        try:
            # Simple code template
            code = f'''# Code for: {query}
# This code was generated by JARVIS Assistant
# Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
# Language: {language}

def main():
    """Main function"""
    print("Implement your logic here")
    # TODO: Add your implementation based on: {query}
    
if __name__ == "__main__":
    main()
'''
            
            # Type the code
            pyautogui.write(code, interval=0.05)
            
            self.tts.speak(f"Sir, I've created a code template for {query} in {language}")
            
            return {
                'success': True,
                'language': language,
                'code_type': 'template',
                'code': code
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }