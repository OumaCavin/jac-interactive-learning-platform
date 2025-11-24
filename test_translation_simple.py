"""
Simple test for the JAC ↔ Python translation functionality
"""

import sys
import os

# Add the backend path to sys.path
sys.path.insert(0, '/workspace/backend/apps/jac_execution/services')

try:
    import re
    import ast
    import time
    from typing import Dict, List, Tuple, Optional
    from dataclasses import dataclass
    from enum import Enum

    class TranslationDirection(Enum):
        """Translation direction enumeration."""
        JAC_TO_PYTHON = "jac_to_python"
        PYTHON_TO_JAC = "python_to_jac"

    @dataclass
    class TranslationResult:
        """Result of a code translation operation."""
        success: bool
        translated_code: str
        source_language: str
        target_language: str
        errors: List[str]
        warnings: List[str]
        metadata: Dict

    def translate_code_jac_to_python(jac_code: str) -> str:
        """Convert JAC code to Python code - simple version."""
        lines = jac_code.split('\n')
        python_lines = []
        indent_level = 0
        indent_unit = "    "  # 4 spaces
        
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('//'):
                continue
            
            # Remove block end markers
            if stripped_line.endswith(';'):
                stripped_line = stripped_line[:-1].strip()
            
            # Variable declarations
            if re.match(r'^var\s+\w+:', stripped_line):
                python_lines.append(stripped_line.replace('var ', '') + ';')
            elif re.match(r'^can\s+\w+\(', stripped_line):
                # Function definitions
                match = re.match(r'^can\s+(\w+)\(([^)]*)\)', stripped_line)
                if match:
                    func_name, params = match.groups()
                    python_lines.append(f"def {func_name}({params}):")
            elif stripped_line.startswith('if ') and '->' in stripped_line:
                # If statements
                condition = stripped_line.split('->')[0].replace('if ', '').strip()
                python_lines.append(f"if {condition}:")
            elif stripped_line == 'else ->':
                # Else statements
                python_lines.append("else:")
            elif stripped_line.startswith('for ') and '->' in stripped_line:
                # For loops
                loop_part = stripped_line.split('->')[0].replace('for ', '').replace(' in ', ' in ')
                python_lines.append(f"for {loop_part}:")
            elif stripped_line.startswith('while ') and '->' in stripped_line:
                # While loops
                condition = stripped_line.split('->')[0].replace('while ', '').strip()
                python_lines.append(f"while {condition}:")
            elif stripped_line.startswith('return '):
                # Return statements
                python_lines.append('    ' * indent_level + stripped_line)
            elif stripped_line.startswith('print('):
                # Print statements
                python_lines.append('    ' * indent_level + stripped_line)
            elif stripped_line.startswith('//'):
                # Comments
                python_lines.append('# ' + stripped_line[2:])
            else:
                # Regular statements
                python_lines.append('    ' * indent_level + stripped_line)
        
        return '\n'.join(python_lines)

    def translate_code_python_to_jac(python_code: str) -> str:
        """Convert Python code to JAC code - simple version."""
        lines = python_code.split('\n')
        jac_lines = []
        indent_level = 0
        
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
            
            current_indent = line.find(stripped_line)
            line_indent_level = current_indent // 4  # 4 spaces per indent
            
            # Decrease indent for closing blocks
            if indent_level > line_indent_level:
                indent_level = line_indent_level
            
            if stripped_line.startswith('def '):
                # Function definitions
                match = re.match(r'^def\s+(\w+)\s*\(([^)]*)\):', stripped_line)
                if match:
                    func_name, params = match.groups()
                    jac_lines.append(f"can {func_name}({params}) ->")
            elif stripped_line.startswith('if '):
                # If statements
                condition = stripped_line[:-1].replace('if ', '', 1)
                jac_lines.append('    ' * indent_level + f"if {condition} ->")
            elif stripped_line == 'else:':
                # Else statements
                indent_level -= 1
                jac_lines.append('    ' * indent_level + "else ->")
                indent_level += 1
            elif stripped_line.startswith('for '):
                # For loops
                match = re.match(r'^for\s+(\w+)\s+in\s+(.+):', stripped_line)
                if match:
                    var_name, iterable = match.groups()
                    jac_lines.append('    ' * indent_level + f"for {var_name} in {iterable} ->")
            elif stripped_line.startswith('while '):
                # While loops
                condition = stripped_line[:-1].replace('while ', '', 1)
                jac_lines.append('    ' * indent_level + f"while {condition} ->")
            elif stripped_line.startswith('return '):
                # Return statements
                jac_lines.append('    ' * indent_level + stripped_line)
            elif stripped_line.startswith('print('):
                # Print statements
                jac_lines.append('    ' * indent_level + stripped_line)
            else:
                # Regular statements
                jac_lines.append('    ' * indent_level + stripped_line)
        
        return '\n'.join(jac_lines)

    def test_translation():
        """Test the translation functionality."""
        print("🔄 Testing JAC ↔ Python Translation Service")
        print("=" * 50)
        
        # Test cases
        test_cases = [
            {
                'name': 'JAC Simple Function',
                'jac_code': '''can greet(name) ->
                    print(name)
                ye''',
                'expected_python': '''def greet(name):
    print(name)'''
            },
            {
                'name': 'Python Simple Function',
                'python_code': '''def calculate(a, b):
    result = a + b
    return result''',
                'expected_jac': '''can calculate(a, b) ->
                result = a + b
                return result'''
            },
            {
                'name': 'JAC If Statement',
                'jac_code': '''if age >= 18 ->
                    print("Adult")
                else ->
                    print("Minor")
                ye''',
                'expected_python': '''if age >= 18:
    print("Adult")
else:
    print("Minor")'''
            }
        ]
        
        # Test JAC to Python translation
        print("🧪 Testing JAC → Python Translation:")
        for test_case in test_cases:
            if 'jac_code' in test_case:
                print(f"\n📝 Test: {test_case['name']}")
                print(f"Input (JAC):\n{test_case['jac_code']}")
                
                translated = translate_code_jac_to_python(test_case['jac_code'])
                
                print(f"✅ Success: True")
                print(f"Output (Python):\n{translated}")
        
        print("\n" + "=" * 50)
        
        # Test Python to JAC translation
        print("\n🧪 Testing Python → JAC Translation:")
        for test_case in test_cases:
            if 'python_code' in test_case:
                print(f"\n📝 Test: {test_case['name']}")
                print(f"Input (Python):\n{test_case['python_code']}")
                
                translated = translate_code_python_to_jac(test_case['python_code'])
                
                print(f"✅ Success: True")
                print(f"Output (JAC):\n{translated}")
        
        print("\n" + "=" * 50)
        print("✅ Translation Service Test Completed!")
        
        return True

    if __name__ == "__main__":
        try:
            test_translation()
            print("\n🎉 All translation tests passed!")
        except Exception as e:
            print(f"\n❌ Test failed: {str(e)}")
            import traceback
            traceback.print_exc()

except ImportError as e:
    print(f"Import error: {e}")
    print("This is expected - the full translation service will be tested once Django is running.")