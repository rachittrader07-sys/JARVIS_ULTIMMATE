"""
🔍 Code Analyzer
Analyzes code for errors, style, and improvements
"""

import ast
import re
import json
from datetime import datetime
from colorama import Fore, Style

class CodeAnalyzer:
    def __init__(self, config, tts):
        self.config = config
        self.tts = tts
        
    def execute(self, params):
        """🔍 Execute code analysis"""
        code = params.get('code', '')
        language = params.get('language', 'python').lower()
        analysis_type = params.get('type', 'all').lower()
        
        if not code:
            self.tts.speak("Sir, kaunsa code analyze karna hai?")
            return {'success': False, 'error': 'No code provided'}
        
        print(Fore.YELLOW + f"🔍 Analyzing {language} code..." + Style.RESET_ALL)
        
        if language == 'python':
            result = self.analyze_python_code(code, analysis_type)
        elif language == 'javascript':
            result = self.analyze_javascript_code(code, analysis_type)
        elif language == 'java':
            result = self.analyze_java_code(code, analysis_type)
        else:
            result = self.analyze_general_code(code, language, analysis_type)
        
        if result['success']:
            # Speak summary
            summary = self.get_analysis_summary(result)
            self.tts.speak(f"Sir, {summary}")
            
            return {
                'success': True,
                'analysis': result,
                'speak': f"Code analysis complete. {summary}"
            }
        else:
            self.tts.speak("Sir, code analyze nahi kar paya")
            return result
    
    def analyze_python_code(self, code, analysis_type):
        """🔍 Analyze Python code"""
        try:
            analysis = {
                'language': 'python',
                'timestamp': datetime.now().isoformat(),
                'syntax_valid': False,
                'errors': [],
                'warnings': [],
                'suggestions': [],
                'metrics': {},
                'complexity': 'low'
            }
            
            # Check syntax
            try:
                ast.parse(code)
                analysis['syntax_valid'] = True
            except SyntaxError as e:
                analysis['errors'].append({
                    'type': 'syntax_error',
                    'message': str(e),
                    'line': e.lineno if hasattr(e, 'lineno') else 'unknown'
                })
            
            # Only proceed if syntax is valid
            if analysis['syntax_valid']:
                # Parse AST for deeper analysis
                tree = ast.parse(code)
                
                # Check for common issues
                analysis.update(self.analyze_python_ast(tree))
                
                # Calculate metrics
                analysis['metrics'] = self.calculate_python_metrics(code, tree)
                
                # Determine complexity
                analysis['complexity'] = self.determine_complexity(analysis['metrics'])
            
            return {'success': True, 'analysis': analysis}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_python_ast(self, tree):
        """🔍 Analyze Python AST for issues"""
        issues = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Check for undefined variables
        undefined_vars = self.check_undefined_variables(tree)
        if undefined_vars:
            issues['errors'].extend(undefined_vars)
        
        # Check for unused imports
        unused_imports = self.check_unused_imports(tree)
        if unused_imports:
            issues['warnings'].extend(unused_imports)
        
        # Check for long functions
        long_functions = self.check_long_functions(tree)
        if long_functions:
            issues['warnings'].extend(long_functions)
        
        # Check for nested loops
        nested_loops = self.check_nested_loops(tree)
        if nested_loops:
            issues['warnings'].extend(nested_loops)
        
        # Check for magic numbers
        magic_numbers = self.check_magic_numbers(tree)
        if magic_numbers:
            issues['suggestions'].extend(magic_numbers)
        
        # Check for missing docstrings
        missing_docstrings = self.check_missing_docstrings(tree)
        if missing_docstrings:
            issues['suggestions'].extend(missing_docstrings)
        
        return issues
    
    def check_undefined_variables(self, tree):
        """🔍 Check for undefined variables"""
        issues = []
        
        class VariableChecker(ast.NodeVisitor):
            def __init__(self):
                self.defined_vars = set()
                self.issues = []
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    if node.id not in self.defined_vars and not node.id.startswith('_'):
                        self.issues.append({
                            'type': 'undefined_variable',
                            'message': f"Undefined variable: {node.id}",
                            'line': node.lineno
                        })
                elif isinstance(node.ctx, ast.Store):
                    self.defined_vars.add(node.id)
                
                self.generic_visit(node)
        
        checker = VariableChecker()
        checker.visit(tree)
        
        return checker.issues
    
    def check_unused_imports(self, tree):
        """🔍 Check for unused imports"""
        issues = []
        
        class ImportChecker(ast.NodeVisitor):
            def __init__(self):
                self.imports = set()
                self.used_names = set()
                self.issues = []
            
            def visit_Import(self, node):
                for alias in node.names:
                    self.imports.add(alias.name)
                self.generic_visit(node)
            
            def visit_ImportFrom(self, node):
                for alias in node.names:
                    self.imports.add(alias.name if alias.name != '*' else f"{node.module}.*")
                self.generic_visit(node)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    self.used_names.add(node.id)
                self.generic_visit(node)
            
            def report_unused(self):
                for imp in self.imports:
                    # Check if import is used
                    if '*' in imp:
                        module = imp.replace('.*', '')
                        # Can't check star imports easily
                        continue
                    
                    if imp.split('.')[0] not in self.used_names:
                        self.issues.append({
                            'type': 'unused_import',
                            'message': f"Unused import: {imp}",
                            'line': 1  # Approximate
                        })
        
        checker = ImportChecker()
        checker.visit(tree)
        checker.report_unused()
        
        return checker.issues
    
    def check_long_functions(self, tree, max_lines=50):
        """🔍 Check for functions that are too long"""
        issues = []
        
        class FunctionChecker(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # Count lines in function
                start_line = node.lineno
                end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start_line)
                line_count = end_line - start_line + 1
                
                if line_count > max_lines:
                    issues.append({
                        'type': 'long_function',
                        'message': f"Function '{node.name}' is too long ({line_count} lines). Consider breaking it down.",
                        'line': start_line,
                        'line_count': line_count
                    })
                
                self.generic_visit(node)
        
        checker = FunctionChecker()
        checker.visit(tree)
        
        return issues
    
    def check_nested_loops(self, tree, max_depth=3):
        """🔍 Check for deeply nested loops"""
        issues = []
        
        class LoopChecker(ast.NodeVisitor):
            def __init__(self):
                self.current_depth = 0
            
            def visit_For(self, node):
                self.current_depth += 1
                if self.current_depth > max_depth:
                    issues.append({
                        'type': 'deeply_nested_loop',
                        'message': f"Loop nested {self.current_depth} levels deep. Consider refactoring.",
                        'line': node.lineno,
                        'depth': self.current_depth
                    })
                self.generic_visit(node)
                self.current_depth -= 1
            
            def visit_While(self, node):
                self.current_depth += 1
                if self.current_depth > max_depth:
                    issues.append({
                        'type': 'deeply_nested_loop',
                        'message': f"Loop nested {self.current_depth} levels deep. Consider refactoring.",
                        'line': node.lineno,
                        'depth': self.current_depth
                    })
                self.generic_visit(node)
                self.current_depth -= 1
        
        checker = LoopChecker()
        checker.visit(tree)
        
        return issues
    
    def check_magic_numbers(self, tree):
        """🔍 Check for magic numbers (unnamed constants)"""
        issues = []
        
        class NumberChecker(ast.NodeVisitor):
            def visit_Constant(self, node):
                if isinstance(node.value, (int, float)):
                    # Check if it's a "magic number" (not 0, 1, etc.)
                    if node.value not in [0, 1, -1, 2, 10, 100, 1000]:
                        # Check if parent is a binary operation (more likely to be magic)
                        parent = getattr(node, 'parent', None)
                        if parent and isinstance(parent, ast.BinOp):
                            issues.append({
                                'type': 'magic_number',
                                'message': f"Consider replacing magic number {node.value} with a named constant.",
                                'line': node.lineno,
                                'value': node.value
                            })
                self.generic_visit(node)
        
        # Add parent references
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        
        checker = NumberChecker()
        checker.visit(tree)
        
        return issues
    
    def check_missing_docstrings(self, tree):
        """🔍 Check for missing docstrings"""
        issues = []
        
        class DocstringChecker(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if not ast.get_docstring(node):
                    issues.append({
                        'type': 'missing_docstring',
                        'message': f"Function '{node.name}' is missing a docstring.",
                        'line': node.lineno
                    })
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                if not ast.get_docstring(node):
                    issues.append({
                        'type': 'missing_docstring',
                        'message': f"Class '{node.name}' is missing a docstring.",
                        'line': node.lineno
                    })
                self.generic_visit(node)
            
            def visit_Module(self, node):
                if not ast.get_docstring(node):
                    issues.append({
                        'type': 'missing_docstring',
                        'message': "Module is missing a docstring.",
                        'line': 1
                    })
                self.generic_visit(node)
        
        checker = DocstringChecker()
        checker.visit(tree)
        
        return issues
    
    def calculate_python_metrics(self, code, tree):
        """🔍 Calculate Python code metrics"""
        metrics = {
            'lines_of_code': len(code.split('\n')),
            'functions': 0,
            'classes': 0,
            'imports': 0,
            'comments': 0,
            'complexity_score': 0
        }
        
        # Count functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                metrics['functions'] += 1
            elif isinstance(node, ast.ClassDef):
                metrics['classes'] += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics['imports'] += 1
        
        # Count comments (approximate)
        comment_pattern = r'^\s*#'
        lines = code.split('\n')
        metrics['comments'] = sum(1 for line in lines if re.match(comment_pattern, line))
        
        # Calculate comment percentage
        if metrics['lines_of_code'] > 0:
            metrics['comment_percentage'] = (metrics['comments'] / metrics['lines_of_code']) * 100
        else:
            metrics['comment_percentage'] = 0
        
        # Calculate complexity score (simplified)
        metrics['complexity_score'] = (
            metrics['functions'] * 5 +
            metrics['classes'] * 10 +
            metrics['lines_of_code'] * 0.1
        )
        
        return metrics
    
    def determine_complexity(self, metrics):
        """🔍 Determine code complexity level"""
        score = metrics.get('complexity_score', 0)
        
        if score < 20:
            return 'very_low'
        elif score < 50:
            return 'low'
        elif score < 100:
            return 'medium'
        elif score < 200:
            return 'high'
        else:
            return 'very_high'
    
    def analyze_javascript_code(self, code, analysis_type):
        """🔍 Analyze JavaScript code (simplified)"""
        try:
            analysis = {
                'language': 'javascript',
                'timestamp': datetime.now().isoformat(),
                'syntax_valid': True,  # Would need proper parser
                'errors': [],
                'warnings': [],
                'suggestions': [],
                'metrics': {},
                'complexity': 'unknown'
            }
            
            # Basic checks
            lines = code.split('\n')
            
            # Check for missing semicolons (basic)
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                    # Check if line might need semicolon
                    if stripped.endswith((')', '}', ']')) and not stripped.endswith(';'):
                        analysis['warnings'].append({
                            'type': 'missing_semicolon',
                            'message': "Consider adding semicolon",
                            'line': i
                        })
            
            # Check for console.log (might be debugging left)
            if 'console.log' in code:
                analysis['suggestions'].append({
                    'type': 'debug_code',
                    'message': "Remove console.log statements before production",
                    'line': 'multiple'
                })
            
            # Calculate basic metrics
            analysis['metrics'] = {
                'lines_of_code': len(lines),
                'functions': code.count('function '),
                'comments': sum(1 for line in lines if line.strip().startswith(('//', '/*')))
            }
            
            return {'success': True, 'analysis': analysis}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_java_code(self, code, analysis_type):
        """🔍 Analyze Java code (simplified)"""
        try:
            analysis = {
                'language': 'java',
                'timestamp': datetime.now().isoformat(),
                'syntax_valid': True,  # Would need proper parser
                'errors': [],
                'warnings': [],
                'suggestions': [],
                'metrics': {},
                'complexity': 'unknown'
            }
            
            # Basic checks
            lines = code.split('\n')
            
            # Check for public class
            if 'public class' not in code:
                analysis['warnings'].append({
                    'type': 'no_public_class',
                    'message': "Java files should have a public class",
                    'line': 1
                })
            
            # Check for main method
            if 'public static void main' not in code:
                analysis['warnings'].append({
                    'type': 'no_main_method',
                    'message': "Executable Java files need a main method",
                    'line': 'unknown'
                })
            
            # Calculate basic metrics
            analysis['metrics'] = {
                'lines_of_code': len(lines),
                'classes': code.count('class '),
                'methods': code.count('public ') + code.count('private ') + code.count('protected '),
                'comments': sum(1 for line in lines if line.strip().startswith(('//', '/*', '*')))
            }
            
            return {'success': True, 'analysis': analysis}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_general_code(self, code, language, analysis_type):
        """🔍 Analyze general code for any language"""
        try:
            analysis = {
                'language': language,
                'timestamp': datetime.now().isoformat(),
                'syntax_valid': True,  # Assume valid
                'errors': [],
                'warnings': [],
                'suggestions': [],
                'metrics': {},
                'complexity': 'unknown'
            }
            
            # Basic metrics
            lines = code.split('\n')
            analysis['metrics'] = {
                'lines_of_code': len(lines),
                'non_empty_lines': sum(1 for line in lines if line.strip()),
                'max_line_length': max(len(line) for line in lines) if lines else 0
            }
            
            # Check for long lines
            for i, line in enumerate(lines, 1):
                if len(line) > 80:  # Common limit
                    analysis['warnings'].append({
                        'type': 'long_line',
                        'message': f"Line {i} is too long ({len(line)} characters)",
                        'line': i,
                        'length': len(line)
                    })
            
            return {'success': True, 'analysis': analysis}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_analysis_summary(self, result):
        """🔍 Get human-readable analysis summary"""
        analysis = result.get('analysis', {})
        
        if not analysis:
            return "No analysis available"
        
        language = analysis.get('language', 'code')
        errors = len(analysis.get('errors', []))
        warnings = len(analysis.get('warnings', []))
        suggestions = len(analysis.get('suggestions', []))
        
        metrics = analysis.get('metrics', {})
        lines = metrics.get('lines_of_code', 0)
        functions = metrics.get('functions', 0)
        classes = metrics.get('classes', 0)
        
        summary_parts = []
        
        if errors == 0 and warnings == 0 and suggestions == 0:
            summary_parts.append("Code looks good")
        else:
            if errors > 0:
                summary_parts.append(f"{errors} errors")
            if warnings > 0:
                summary_parts.append(f"{warnings} warnings")
            if suggestions > 0:
                summary_parts.append(f"{suggestions} suggestions")
        
        summary_parts.append(f"{lines} lines")
        
        if functions > 0:
            summary_parts.append(f"{functions} functions")
        
        if classes > 0:
            summary_parts.append(f"{classes} classes")
        
        return f"{language} analysis: {', '.join(summary_parts)}"
    
    def explain_error(self, error_type, error_message):
        """🔍 Explain an error in simple terms"""
        explanations = {
            'syntax_error': "There's a syntax error in your code. Check for missing brackets, quotes, or colons.",
            'undefined_variable': "You're using a variable that hasn't been defined yet.",
            'unused_import': "You imported a module but didn't use it. Consider removing it.",
            'long_function': "This function is too long. Try breaking it into smaller functions.",
            'deeply_nested_loop': "The loops are too deeply nested. This can make code hard to read.",
            'magic_number': "Use named constants instead of hard-coded numbers for better readability.",
            'missing_docstring': "Add a docstring to explain what this function/class does.",
            'missing_semicolon': "JavaScript needs semicolons at the end of statements.",
            'no_public_class': "Java files should have at least one public class.",
            'no_main_method': "To run Java code, you need a main method.",
            'long_line': "This line is too long. Try to keep lines under 80 characters.",
            'debug_code': "Remove debugging code like console.log before finalizing."
        }
        
        return explanations.get(error_type, "There's an issue with the code that needs fixing.")