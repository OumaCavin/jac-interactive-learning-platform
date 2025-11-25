"""
JAC Code Execution Service for Interactive Learning Platform
Provides JAC code execution, validation, and feedback for learning purposes
"""

import re
import ast
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid


class JACSyntaxValidator:
    """Validates JAC syntax and provides feedback"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_code(self, code: str) -> Dict[str, Any]:
        """Validate JAC code and return results"""
        self.errors = []
        self.warnings = []
        
        # Basic syntax checks
        self._check_basic_syntax(code)
        self._check_node_syntax(code)
        self._check_edge_syntax(code)
        self._check_walker_syntax(code)
        self._check_spatial_operators(code)
        self._check_abilities_syntax(code)
        
        return {
            'is_valid': len(self.errors) == 0,
            'errors': self.errors,
            'warnings': self.warnings,
            'syntax_highlights': self._get_syntax_highlights(code),
            'line_count': len(code.split('\n'))
        }
    
    def _check_basic_syntax(self, code: str):
        """Check basic JAC syntax"""
        lines = code.split('\n')
        
        # Check for basic JAC constructs
        if 'with entry' in code and 'with entry {' not in code:
            self.errors.append("Line with 'with entry' should be: 'with entry {'")
        
        # Check for proper indentation (basic check)
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped:
                # Check for proper JAC keywords indentation
                if any(keyword in stripped for keyword in ['node', 'edge', 'walker', 'def']) and not line.startswith(' ' * 4):
                    if not any(prev.strip().endswith('{') for prev in lines[:i-1]):
                        self.warnings.append(f"Line {i}: Consider proper indentation for '{stripped.split()[0]}'")
    
    def _check_node_syntax(self, code: str):
        """Check node definitions"""
        node_pattern = r'node\s+(\w+)\s*{'
        nodes = re.findall(node_pattern, code)
        
        for node_name in nodes:
            # Check if node has proper closing
            if not re.search(rf'^{re.escape(node_name)}\s*}}', code, re.MULTILINE):
                self.errors.append(f"Node '{node_name}' may be missing closing brace '}}'")
            
            # Check for 'has' statements inside node
            node_block = self._extract_block(code, f'node {node_name}', '}')
            if node_block:
                has_statements = re.findall(r'has\s+(\w+):\s*(\w+)', node_block)
                for prop_name, prop_type in has_statements:
                    if prop_type not in ['str', 'int', 'float', 'bool', 'list', 'dict', 'any']:
                        self.errors.append(f"Node '{node_name}': Unknown property type '{prop_type}' for '{prop_name}'")
    
    def _check_edge_syntax(self, code: str):
        """Check edge definitions"""
        edge_pattern = r'edge\s+(\w+)\s*{'
        edges = re.findall(edge_pattern, code)
        
        for edge_name in edges:
            # Check if edge has proper closing
            if not re.search(rf'^{re.escape(edge_name)}\s*}}', code, re.MULTILINE):
                self.errors.append(f"Edge '{edge_name}' may be missing closing brace '}}'")
            
            # Check for 'has' statements inside edge
            edge_block = self._extract_block(code, f'edge {edge_name}', '}')
            if edge_block:
                has_statements = re.findall(r'has\s+(\w+):\s*(\w+)', edge_block)
                for prop_name, prop_type in has_statements:
                    if prop_type not in ['str', 'int', 'float', 'bool', 'list', 'dict', 'any']:
                        self.errors.append(f"Edge '{edge_name}': Unknown property type '{prop_type}' for '{prop_name}'")
    
    def _check_walker_syntax(self, code: str):
        """Check walker definitions"""
        walker_pattern = r'walker\s+(\w+)\s*{'
        walkers = re.findall(walker_pattern, code)
        
        for walker_name in walkers:
            # Check if walker has proper closing
            if not re.search(rf'^{re.escape(walker_name)}\s*}}', code, re.MULTILINE):
                self.errors.append(f"Walker '{walker_name}' may be missing closing brace '}}'")
            
            # Check for abilities in walker
            walker_block = self._extract_block(code, f'walker {walker_name}', '}')
            if walker_block:
                abilities = re.findall(r'can\s+(\w+)', walker_block)
                for ability_name in abilities:
                    # Check if ability has proper signature
                    if not re.search(rf'can\s+{re.escape(ability_name)}\s*(with\s+\w+)?\s*(entry|exit|\w+\s+entry|\w+\s+exit)?', walker_block):
                        self.warnings.append(f"Walker '{walker_name}': Ability '{ability_name}' may need proper signature")
    
    def _check_spatial_operators(self, code: str):
        """Check spatial operator usage"""
        spatial_operators = ['++>', '<++', '<++>', 'del-->', 'spawn', 'visit']
        
        for operator in spatial_operators:
            if operator in code:
                # Check for proper syntax around operators
                if operator in ['++>', '<++', '<++>']:
                    # Check for edge-like syntax
                    pattern = rf'(\w+)\s*([+<]*>?>\s*|[+<]*>\s*|\+>:.*?:\+>|\+<:.*?:\+<)(\w+)'
                    matches = re.findall(pattern, code)
                    for match in matches:
                        if len(match) >= 3:
                            self.warnings.append(f"Check spatial connection syntax between '{match[0]}' and '{match[2]}'")
    
    def _check_abilities_syntax(self, code: str):
        """Check abilities in nodes and walkers"""
        # Check for proper ability definitions
        ability_pattern = r'can\s+(\w+)\s+with\s+(\w+)\s+(entry|exit)'
        abilities = re.findall(ability_pattern, code)
        
        for ability_name, target, trigger in abilities:
            if target not in ['entry', 'exit']:
                # This is a visit-dependent ability
                pass  # This is valid
    
    def _extract_block(self, code: str, start_pattern: str, end_token: str) -> Optional[str]:
        """Extract a code block between start and end tokens"""
        lines = code.split('\n')
        start_found = False
        start_line = 0
        brace_count = 0
        block_lines = []
        
        for i, line in enumerate(lines):
            if not start_found and start_pattern in line:
                start_found = True
                start_line = i
                if '{' in line:
                    brace_count += line.count('{') - line.count('}')
                block_lines.append(line)
                continue
            
            if start_found:
                block_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                
                if brace_count == 0:
                    break
        
        return '\n'.join(block_lines) if block_lines else None
    
    def _get_syntax_highlights(self, code: str) -> Dict[int, List[str]]:
        """Get syntax highlights for different elements"""
        highlights = {}
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line_highlights = []
            
            # Highlight JAC keywords
            keywords = ['node', 'edge', 'walker', 'with', 'entry', 'can', 'def', 'has', 'spawn', 'visit', 'report', 'disengage']
            for keyword in keywords:
                if re.search(rf'\b{keyword}\b', line):
                    line_highlights.append(f'keyword-{keyword}')
            
            # Highlight data types
            types = ['str', 'int', 'float', 'bool', 'list', 'dict', 'any']
            for type_name in types:
                if re.search(rf'\b{type_name}\b', line):
                    line_highlights.append(f'type-{type_name}')
            
            # Highlight spatial operators
            spatial_ops = ['++>', '<++', '<++>', 'del-->']
            for op in spatial_ops:
                if op in line:
                    line_highlights.append('spatial-operator')
            
            # Highlight identifiers
            identifiers = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', line)
            for ident in identifiers:
                if ident not in keywords + types:
                    # Check if it's likely a class/type name
                    if any(pattern in line for pattern in [f'{ident} {{', f'{ident}(', f'{ident}:']):
                        line_highlights.append('identifier-class')
                    else:
                        line_highlights.append('identifier')
            
            if line_highlights:
                highlights[i] = line_highlights
        
        return highlights


class JACExecutionEngine:
    """Simulates JAC code execution for learning purposes"""
    
    def __init__(self):
        self.variables = {}
        self.graph = {'nodes': {}, 'edges': []}
        self.output = []
        self.walkers = {}
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """Execute JAC code and return results"""
        self.variables = {}
        self.graph = {'nodes': {}, 'edges': []}
        self.output = []
        self.walkers = {}
        
        try:
            # Parse and execute the code
            self._execute_with_entry(code)
            
            return {
                'success': True,
                'output': self.output,
                'variables': self.variables,
                'graph': self.graph,
                'walkers': self.walkers,
                'execution_time': 0.1,  # Simulated
                'memory_usage': 1024   # Simulated
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': self.output,
                'execution_time': 0.1
            }
    
    def _execute_with_entry(self, code: str):
        """Execute the with entry block"""
        # Find with entry block
        entry_match = re.search(r'with\s+entry\s*{([^}]*(?:{[^}]*}[^}]*)*)}', code, re.DOTALL)
        
        if entry_match:
            entry_code = entry_match.group(1)
            self._execute_statements(entry_code)
        else:
            self._execute_statements(code)  # Execute all if no entry block
    
    def _execute_statements(self, code: str):
        """Execute statements in a block"""
        lines = code.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            self._execute_statement(line)
    
    def _execute_statement(self, line: str):
        """Execute a single statement"""
        # Variable assignment
        if '=' in line and not any(op in line for op in ['==', '>=', '<=']):
            self._execute_assignment(line)
        
        # Node creation
        elif line.startswith('node '):
            self._execute_node_creation(line)
        
        # Edge creation (spatial operations)
        elif any(op in line for op in ['++>', '<++', '<++>', 'del-->']):
            self._execute_edge_creation(line)
        
        # Walker spawning
        elif 'spawn' in line:
            self._execute_spawn(line)
        
        # Function calls
        elif '(' in line and ')' in line:
            self._execute_function_call(line)
        
        # Print statements
        elif line.startswith('print('):
            self._execute_print(line)
        
        # Comments
        else:
            # Store as a comment or unknown statement
            if not line.startswith('#'):
                self.output.append(f"Note: '{line}' - This is a comment or unsupported statement")
    
    def _execute_assignment(self, line: str):
        """Execute variable assignment"""
        try:
            # Simple variable assignment
            if ':' in line:
                # Type annotation assignment
                var_expr, value_expr = line.split('=', 1)
                var_name = var_expr.split(':')[0].strip()
                value = self._evaluate_expression(value_expr.strip())
            else:
                # Simple assignment
                var_name, value_expr = line.split('=', 1)
                value = self._evaluate_expression(value_expr.strip())
            
            self.variables[var_name] = value
            self.output.append(f"Assigned {var_name} = {value}")
        
        except Exception as e:
            self.output.append(f"Error in assignment: {e}")
    
    def _execute_node_creation(self, line: str):
        """Execute node creation"""
        # Extract node type and parameters
        match = re.match(r'node\s+(\w+)\s*{([^}]*)}', line)
        if match:
            node_type = match.group(1)
            properties = match.group(2)
            self.output.append(f"Defined node type: {node_type}")
            
            # Parse properties
            props = {}
            for prop_match in re.finditer(r'has\s+(\w+):\s*(\w+)', properties):
                prop_name, prop_type = prop_match.groups()
                props[prop_name] = prop_type
            
            self.variables[f'_node_type_{node_type}'] = {'type': node_type, 'properties': props}
    
    def _execute_edge_creation(self, line: str):
        """Execute edge creation (spatial operations)"""
        if '++>' in line:
            # Simple forward connection
            parts = line.split('++>')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip().rstrip(';')
                self.output.append(f"Created connection: {left} → {right}")
                
                # Add to graph
                if left not in self.graph['nodes']:
                    self.graph['nodes'][left] = []
                if right not in self.graph['nodes']:
                    self.graph['nodes'][right] = []
                
                self.graph['edges'].append({'from': left, 'to': right, 'type': 'forward'})
        
        elif '<++>' in line:
            # Bidirectional connection
            parts = line.split('<++>')
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip().rstrip(';')
                self.output.append(f"Created bidirectional connection: {left} ↔ {right}")
                
                # Add to graph
                if left not in self.graph['nodes']:
                    self.graph['nodes'][left] = []
                if right not in self.graph['nodes']:
                    self.graph['nodes'][right] = []
                
                self.graph['edges'].extend([
                    {'from': left, 'to': right, 'type': 'bidirectional'},
                    {'from': right, 'to': left, 'type': 'bidirectional'}
                ])
    
    def _execute_spawn(self, line: str):
        """Execute walker spawning"""
        if 'spawn' in line:
            match = re.search(r'spawn\s+(\w+)\s*\(\s*\)', line)
            if match:
                walker_name = match.group(1)
                self.output.append(f"Spawned walker: {walker_name}")
                self.walkers[walker_name] = {'status': 'executed', 'traversed_nodes': []}
    
    def _execute_function_call(self, line: str):
        """Execute function call"""
        # Extract function name and arguments
        match = re.match(r'(\w+)\s*\((.*)\)', line)
        if match:
            func_name = match.group(1)
            args = match.group(2)
            
            if func_name == 'print':
                # Handle print function
                content = args.strip('"\'')
                self.output.append(content)
            else:
                self.output.append(f"Called function: {func_name}({args})")
    
    def _execute_print(self, line: str):
        """Execute print statement"""
        # Extract content from print()
        match = re.match(r'print\s*\((.*)\)', line)
        if match:
            content = match.group(1).strip()
            
            # Handle f-strings
            if content.startswith('f"') or content.startswith("f'"):
                content = content[2:-1]  # Remove f" and "
                # Simple f-string processing
                content = re.sub(r'\{([^}]+)\}', r'\1', content)
            
            self.output.append(content)
    
    def _evaluate_expression(self, expr: str) -> Any:
        """Evaluate a simple expression"""
        expr = expr.strip()
        
        # Handle string literals
        if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
            return expr[1:-1]
        
        # Handle numbers
        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except ValueError:
            pass
        
        # Handle booleans
        if expr.lower() in ['true', 'false']:
            return expr.lower() == 'true'
        
        # Handle variable references
        if expr in self.variables:
            return self.variables[expr]
        
        # Handle lists
        if expr.startswith('[') and expr.endswith(']'):
            return []  # Simplified list handling
        
        # Return as string if can't parse
        return expr


class JACCodeExecutor:
    """Main service for JAC code execution and validation"""
    
    def __init__(self):
        self.validator = JACSyntaxValidator()
        self.executor = JACExecutionEngine()
    
    def execute_code(self, code: str, language: str = 'jac') -> Dict[str, Any]:
        """Execute JAC code with full validation and execution"""
        if language.lower() != 'jac':
            return {
                'success': False,
                'error': f'Language "{language}" is not supported. Only JAC is supported.',
                'output': [],
                'execution_time': 0
            }
        
        # Validate syntax first
        validation_result = self.validator.validate_code(code)
        
        if not validation_result['is_valid']:
            return {
                'success': False,
                'validation_errors': validation_result['errors'],
                'warnings': validation_result['warnings'],
                'output': [],
                'execution_time': 0
            }
        
        # Execute the code
        execution_result = self.executor.execute_code(code)
        
        # Combine results
        return {
            'success': execution_result['success'],
            'validation': validation_result,
            'execution': {
                'output': execution_result.get('output', []),
                'error': execution_result.get('error'),
                'variables': execution_result.get('variables', {}),
                'graph': execution_result.get('graph', {}),
                'walkers': execution_result.get('walkers', {}),
                'execution_time': execution_result.get('execution_time', 0),
                'memory_usage': execution_result.get('memory_usage', 0)
            },
            'suggestions': self._generate_suggestions(code, validation_result, execution_result),
            'learning_tips': self._generate_learning_tips(code)
        }
    
    def _generate_suggestions(self, code: str, validation: Dict, execution: Dict) -> List[str]:
        """Generate helpful suggestions for the code"""
        suggestions = []
        
        if not validation['is_valid']:
            suggestions.append("Fix syntax errors before running the code")
        
        if 'node' in code and 'edge' not in code:
            suggestions.append("Try connecting your nodes with spatial operators like '++>'")
        
        if 'walker' not in code and 'node' in code:
            suggestions.append("Consider defining a walker to traverse your graph")
        
        if 'with entry' not in code:
            suggestions.append("Use 'with entry {' to define your main execution block")
        
        if not execution.get('output') and 'print' not in code:
            suggestions.append("Add print statements to see output from your code")
        
        if len(code.split('\n')) < 10:
            suggestions.append("Try creating a more complete example with nodes, edges, and walkers")
        
        return suggestions
    
    def _generate_learning_tips(self, code: str) -> List[str]:
        """Generate learning tips based on the code"""
        tips = []
        
        if 'node' in code:
            tips.append("Nodes are like objects in JAC - they hold data and can be connected")
        
        if any(op in code for op in ['++>', '<++', '<++>']):
            tips.append("Spatial operators make graph connections natural and type-safe")
        
        if 'walker' in code:
            tips.append("Walkers are autonomous agents that traverse graphs carrying state")
        
        if 'ability' in code or 'can ' in code:
            tips.append("Abilities are triggered automatically during walker-node interactions")
        
        if 'with entry' in code:
            tips.append("The 'with entry' block is where your JAC program starts executing")
        
        return tips
    
    def get_syntax_reference(self) -> Dict[str, Any]:
        """Get JAC syntax reference for the editor"""
        return {
            'keywords': {
                'node': 'Define a node type with properties',
                'edge': 'Define an edge type with properties', 
                'walker': 'Define a walker class for graph traversal',
                'with': 'Entry point and control structures',
                'can': 'Define abilities in nodes/walkers',
                'has': 'Declare properties in nodes/edges',
                'spawn': 'Launch walkers onto the graph',
                'visit': 'Navigate walker to connected nodes',
                'report': 'Send results while continuing traversal',
                'disengage': 'Stop walker execution immediately'
            },
            'operators': {
                '++>': 'Forward spatial connection',
                '<++': 'Backward spatial connection', 
                '<++>': 'Bidirectional spatial connection',
                'del-->': 'Remove spatial connection'
            },
            'types': {
                'str': 'String type',
                'int': 'Integer type',
                'float': 'Floating point type',
                'bool': 'Boolean type',
                'list': 'List type',
                'dict': 'Dictionary type',
                'any': 'Any type (dynamic typing)'
            },
            'examples': {
                'hello_world': '''with entry {
    print("Hello, JAC world!");
}''',
                'simple_node': '''node Person {
    has name: str;
    has age: int;
}''',
                'graph_creation': '''with entry {
    alice = Person(name="Alice", age=25);
    bob = Person(name="Bob", age=30);
    alice ++> bob;
}''',
                'walker': '''walker Greeter {
    can greet with Person entry {
        print(f"Hello, {here.name}!");
        visit [-->];
    }
}'''
            }
        }


# Global executor instance
jac_executor = JACCodeExecutor()
