# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
JAC ↔ Python Code Translation Service

This module provides bidirectional translation between JAC and Python programming languages.
It includes code parsing, syntax conversion, and validation capabilities.
"""

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


class CodeTranslator:
    """
    Main code translation service supporting JAC ↔ Python conversion.
    """
    
    def __init__(self):
        self.jac_patterns = {
            'variable_declaration': r'\b(var|can|has)\s+(\w+)\s*:\s*(\w+)',
            'function_definition': r'\b(can\s+(\w+))\s*\(([^)]*)\)',
            'if_statement': r'\bif\s+(\w+)\s*->',
            'else_statement': r'\belse\s*->',
            'loop_statement': r'\bfor\s+(\w+)\s+in\s+(\w+)\s*->',
            'while_statement': r'\bwhile\s+(\w+)\s*->',
            'return_statement': r'\breturn\s+(\w+)',
            'print_statement': r'\bprint\s*\(([^)]*)\)',
            'class_definition': r'\bclass\s+(\w+)\s*:\s*(\w+)',
            'comment': r'//\s*(.+)$',
            'line_continuation': r'\.\.\.',
            'block_end': r'\bye\s*;',
        }
        
        self.python_patterns = {
            'variable_declaration': r'(\w+)\s*=\s*(.+)$',
            'function_definition': r'def\s+(\w+)\s*\(([^)]*)\):',
            'if_statement': r'if\s+(.+):',
            'else_statement': r'else:',
            'loop_statement': r'for\s+(\w+)\s+in\s+(.+):',
            'while_statement': r'while\s+(.+):',
            'return_statement': r'return\s+(.+)$',
            'print_statement': r'print\s*\(([^)]*)\)',
            'class_definition': r'class\s+(\w+)\s*\(([^)]*)\):',
            'comment': r'#\s*(.+)$',
        }
    
    def translate_code(self, code: str, direction: TranslationDirection) -> TranslationResult:
        """
        Translate code from source language to target language.
        
        Args:
            code: Source code to translate
            direction: Translation direction (JAC_TO_PYTHON or PYTHON_TO_JAC)
            
        Returns:
            TranslationResult object containing translated code and metadata
        """
        errors = []
        warnings = []
        
        try:
            if direction == TranslationDirection.JAC_TO_PYTHON:
                translated_code = self._translate_jac_to_python(code, warnings)
                source_lang, target_lang = "JAC", "Python"
            else:
                translated_code = self._translate_python_to_jac(code, warnings)
                source_lang, target_lang = "Python", "JAC"
            
            success = len(errors) == 0
            return TranslationResult(
                success=success,
                translated_code=translated_code,
                source_language=source_lang,
                target_language=target_lang,
                errors=errors,
                warnings=warnings,
                metadata={
                    'original_length': len(code),
                    'translated_length': len(translated_code),
                    'direction': direction.value,
                    'timestamp': str(int(time.time())),
                }
            )
        except Exception as e:
            errors.append(f"Translation failed: {str(e)}")
            return TranslationResult(
                success=False,
                translated_code="",
                source_language="Unknown",
                target_language="Unknown",
                errors=errors,
                warnings=warnings,
                metadata={'error': str(e)}
            )
    
    def _translate_jac_to_python(self, jac_code: str, warnings: List[str]) -> str:
        """Convert JAC code to Python code."""
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
                indent_level += 1
            elif stripped_line == 'else ->':
                # Else statements
                indent_level -= 1
                python_lines.append("else:")
                indent_level += 1
            elif stripped_line.startswith('for ') and '->' in stripped_line:
                # For loops
                loop_part = stripped_line.split('->')[0].replace('for ', '').replace(' in ', ' in ')
                python_lines.append(f"for {loop_part}:")
                indent_level += 1
            elif stripped_line.startswith('while ') and '->' in stripped_line:
                # While loops
                condition = stripped_line.split('->')[0].replace('while ', '').strip()
                python_lines.append(f"while {condition}:")
                indent_level += 1
            elif stripped_line.startswith('return '):
                # Return statements
                python_lines.append(stripped_line)
            elif stripped_line.startswith('print('):
                # Print statements
                python_lines.append(stripped_line)
            elif stripped_line.startswith('//'):
                # Comments
                python_lines.append('# ' + stripped_line[2:])
            else:
                # Regular statements
                python_lines.append('    ' * indent_level + stripped_line)
        
        return '\n'.join(python_lines)
    
    def _translate_python_to_jac(self, python_code: str, warnings: List[str]) -> str:
        """Convert Python code to JAC code."""
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
                    indent_level += 1
            elif stripped_line.startswith('if '):
                # If statements
                condition = stripped_line[:-1].replace('if ', '', 1)
                jac_lines.append('    ' * indent_level + f"if {condition} ->")
                indent_level += 1
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
                    indent_level += 1
            elif stripped_line.startswith('while '):
                # While loops
                condition = stripped_line[:-1].replace('while ', '', 1)
                jac_lines.append('    ' * indent_level + f"while {condition} ->")
                indent_level += 1
            elif stripped_line.startswith('return '):
                # Return statements
                jac_lines.append('    ' * indent_level + stripped_line)
            elif stripped_line.startswith('print('):
                # Print statements
                jac_lines.append('    ' * indent_level + stripped_line)
            elif stripped_line.startswith('var ') or stripped_line.startswith('const '):
                # Variable declarations
                jac_lines.append('    ' * indent_level + stripped_line + ';')
            else:
                # Regular statements
                jac_lines.append('    ' * indent_level + stripped_line)
        
        return '\n'.join(jac_lines)
    
    def validate_jac_syntax(self, jac_code: str) -> List[str]:
        """Validate JAC code syntax and return list of errors."""
        errors = []
        lines = jac_code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                continue
            
            # Basic syntax checks
            if stripped.endswith('->') and i == len(lines):
                errors.append(f"Line {i}: Block statement '{stripped}' missing body")
            
            if stripped == 'else ->' and i == len(lines):
                errors.append(f"Line {i}: 'else' block missing body")
            
            # Check for proper JAC keywords
            valid_statements = ['var', 'can', 'if', 'else', 'for', 'while', 'return', 'print']
            if stripped.split()[0] not in valid_statements and not stripped.startswith('//'):
                # Could be a variable assignment or function call
                pass
        
        return errors
    
    def validate_python_syntax(self, python_code: str) -> List[str]:
        """Validate Python code syntax using AST parser."""
        errors = []
        try:
            ast.parse(python_code)
        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        return errors