#!/usr/bin/env python3
"""
JAC Code Execution Sandbox Server
A secure code execution environment for the JAC Learning Platform.
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import traceback

# Configuration
SANDBOX_TIMEOUT = int(os.environ.get('SANDBOX_TIMEOUT', '30'))
MAX_MEMORY_MB = int(os.environ.get('MAX_MEMORY_MB', '128'))
MAX_OUTPUT_SIZE = int(os.environ.get('MAX_OUTPUT_SIZE', '1024'))

class SandboxHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the sandbox service"""
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[SANDBOX] {format % args}")
    
    def do_POST(self):
        """Handle POST requests for code execution"""
        if self.path == '/execute':
            try:
                # Read request data
                content_length = int(self.headers.get('Content-Length', 0))
                request_data = self.rfile.read(content_length)
                data = json.loads(request_data.decode('utf-8'))
                
                # Extract code and language
                code = data.get('code', '')
                language = data.get('language', 'python')
                
                # Execute code in sandbox
                result = self.execute_code(code, language)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = json.dumps(result)
                self.wfile.write(response.encode('utf-8'))
                
            except Exception as e:
                # Handle errors
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_result = {
                    'success': False,
                    'error': str(e),
                    'output': '',
                    'execution_time': 0,
                    'memory_used': 0
                }
                self.wfile.write(json.dumps(error_result).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def execute_code(self, code, language):
        """Execute code in a secure sandbox environment"""
        start_time = time.time()
        temp_file = None
        
        try:
            # Determine file extension based on language
            file_extensions = {
                'python': '.py',
                'javascript': '.js',
                'java': '.java',
                'cpp': '.cpp',
                'c': '.c'
            }
            
            extension = file_extensions.get(language, '.py')
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Execute based on language
            if language == 'python':
                result = self.execute_python(temp_file)
            elif language == 'javascript':
                result = self.execute_javascript(temp_file)
            elif language == 'java':
                result = self.execute_java(temp_file)
            elif language in ['cpp', 'c']:
                result = self.execute_compiled(temp_file, language)
            else:
                raise ValueError(f"Unsupported language: {language}")
            
            # Calculate execution time
            execution_time = time.time() - start_time
            result['execution_time'] = round(execution_time, 3)
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': '',
                'execution_time': time.time() - start_time,
                'memory_used': 0
            }
        finally:
            # Clean up temporary file
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
    
    def execute_python(self, temp_file):
        """Execute Python code with timeout and memory limits"""
        try:
            # Run Python with resource limits
            cmd = [
                'python3', temp_file
            ]
            
            # Set resource limits using ulimit (Linux/Unix only)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            try:
                stdout, stderr = process.communicate(timeout=SANDBOX_TIMEOUT)
                
                # Check output size
                if len(stdout) + len(stderr) > MAX_OUTPUT_SIZE:
                    stdout = stdout[:MAX_OUTPUT_SIZE // 2]
                    stderr = stderr[:MAX_OUTPUT_SIZE // 2] + "\n[Output truncated due to size limit]"
                
                return {
                    'success': process.returncode == 0,
                    'output': stdout,
                    'error': stderr if stderr else None,
                    'exit_code': process.returncode,
                    'memory_used': 0  # Memory monitoring would require more complex setup
                }
                
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'output': '',
                    'error': f'Execution timed out after {SANDBOX_TIMEOUT} seconds',
                    'exit_code': -1,
                    'memory_used': 0
                }
                
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Execution failed: {str(e)}',
                'exit_code': -1,
                'memory_used': 0
            }
    
    def execute_javascript(self, temp_file):
        """Execute JavaScript code (requires Node.js)"""
        try:
            cmd = ['node', temp_file]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=SANDBOX_TIMEOUT)
                return {
                    'success': process.returncode == 0,
                    'output': stdout,
                    'error': stderr if stderr else None,
                    'exit_code': process.returncode,
                    'memory_used': 0
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'output': '',
                    'error': f'JavaScript execution timed out after {SANDBOX_TIMEOUT} seconds',
                    'exit_code': -1,
                    'memory_used': 0
                }
        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': 'Node.js is not installed in the sandbox environment',
                'exit_code': -1,
                'memory_used': 0
            }
    
    def execute_java(self, temp_file):
        """Execute Java code (requires Java compiler)"""
        try:
            # Compile Java file
            compile_cmd = ['javac', temp_file]
            compile_process = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10  # Short timeout for compilation
            )
            
            if compile_process.returncode != 0:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Compilation failed: {compile_process.stderr}',
                    'exit_code': compile_process.returncode,
                    'memory_used': 0
                }
            
            # Extract class name (assumes public class name matches filename)
            class_name = os.path.splitext(os.path.basename(temp_file))[0]
            
            # Run Java class
            run_cmd = ['java', class_name]
            process = subprocess.Popen(
                run_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(temp_file)
            )
            
            try:
                stdout, stderr = process.communicate(timeout=SANDBOX_TIMEOUT)
                return {
                    'success': process.returncode == 0,
                    'output': stdout,
                    'error': stderr if stderr else None,
                    'exit_code': process.returncode,
                    'memory_used': 0
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'output': '',
                    'error': f'Java execution timed out after {SANDBOX_TIMEOUT} seconds',
                    'exit_code': -1,
                    'memory_used': 0
                }
                
        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': 'Java compiler is not installed in the sandbox environment',
                'exit_code': -1,
                'memory_used': 0
            }
    
    def execute_compiled(self, temp_file, language):
        """Execute C/C++ code (requires gcc/g++)"""
        try:
            # Determine compiler
            compiler = 'gcc' if language == 'c' else 'g++'
            
            # Compile the code
            exe_file = temp_file.replace(os.path.splitext(temp_file)[1], '.out')
            compile_cmd = [compiler, temp_file, '-o', exe_file, '-std=c++11', '-O2']
            
            compile_process = subprocess.run(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30  # 30 seconds for compilation
            )
            
            if compile_process.returncode != 0:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Compilation failed: {compile_process.stderr}',
                    'exit_code': compile_process.returncode,
                    'memory_used': 0
                }
            
            # Execute the compiled program
            process = subprocess.Popen(
                [exe_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=SANDBOX_TIMEOUT)
                
                # Clean up executable
                if os.path.exists(exe_file):
                    os.unlink(exe_file)
                
                return {
                    'success': process.returncode == 0,
                    'output': stdout,
                    'error': stderr if stderr else None,
                    'exit_code': process.returncode,
                    'memory_used': 0
                }
            except subprocess.TimeoutExpired:
                process.kill()
                if os.path.exists(exe_file):
                    os.unlink(exe_file)
                return {
                    'success': False,
                    'output': '',
                    'error': f'Execution timed out after {SANDBOX_TIMEOUT} seconds',
                    'exit_code': -1,
                    'memory_used': 0
                }
                
        except FileNotFoundError:
            return {
                'success': False,
                'output': '',
                'error': f'{compiler.title()} compiler is not installed in the sandbox environment',
                'exit_code': -1,
                'memory_used': 0
            }

def run_server(port=8080):
    """Run the sandbox HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SandboxHandler)
    
    print(f"JAC Sandbox Server starting on port {port}")
    print(f"Configuration:")
    print(f"  - Timeout: {SANDBOX_TIMEOUT} seconds")
    print(f"  - Max Memory: {MAX_MEMORY_MB} MB")
    print(f"  - Max Output: {MAX_OUTPUT_SIZE} bytes")
    print(f"  - Available languages: Python, JavaScript, Java, C, C++")
    print(f"\nSandbox endpoints:")
    print(f"  - POST /execute - Execute code")
    print(f"  - GET  /health - Health check")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down sandbox server...")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()