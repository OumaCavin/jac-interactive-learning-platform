"""
Code Execution Service

This module provides secure code execution services for JAC and Python code
with proper sandboxing, resource limits, and security controls.
"""

import os
import sys
import time
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.utils import timezone
from ..models import SecuritySettings

# Try to import psutil, but make it optional
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class CodeExecutionError(Exception):
    """Custom exception for code execution errors."""
    pass


class ResourceLimitError(Exception):
    """Exception raised when resource limits are exceeded."""
    pass


class SecurityViolationError(Exception):
    """Exception raised when security rules are violated."""
    pass


class CodeExecutor:
    """
    Secure code executor with sandboxing and resource controls.
    """
    
    def __init__(self):
        """Initialize the code executor with security settings."""
        self.security_settings = self._load_security_settings()
        self.temp_dir = Path(tempfile.mkdtemp(prefix='jac_execution_'))
        self.jac_path = getattr(settings, 'JAC_EXECUTOR_PATH', None)
        self.python_path = sys.executable
        
    def _load_security_settings(self) -> SecuritySettings:
        """Load security settings from database or use defaults."""
        try:
            return SecuritySettings.objects.get(pk=1)
        except SecuritySettings.DoesNotExist:
            # Create default settings if none exist
            return SecuritySettings.objects.create(
                max_execution_time=5.0,
                max_memory=64,
                max_output_size=10240,
                max_code_size=102400,
                allowed_languages=['jac', 'python'],
                enable_sandboxing=True,
                max_executions_per_minute=60,
                blocked_imports=['os', 'sys', 'subprocess', 'importlib'],
                blocked_functions=['eval', 'exec', 'open', '__import__']
            )
    
    def execute_code(self, language: str, code: str, stdin: str = '') -> Dict:
        """
        Execute code with security controls and resource limits.
        
        Args:
            language: Programming language ('jac' or 'python')
            code: Code to execute
            stdin: Standard input data
            
        Returns:
            Dictionary containing execution results
        """
        if language not in self.security_settings.allowed_languages:
            raise SecurityViolationError(f"Language '{language}' is not allowed")
        
        # Validate and clean code
        self._validate_code(language, code)
        
        # Create temporary workspace
        workspace_path = self.temp_dir / f"workspace_{int(time.time())}"
        workspace_path.mkdir(exist_ok=True)
        
        try:
            if language == 'python':
                return self._execute_python(code, stdin, workspace_path)
            elif language == 'jac':
                return self._execute_jac(code, stdin, workspace_path)
            else:
                raise CodeExecutionError(f"Unsupported language: {language}")
                
        finally:
            # Clean up temporary files
            self._cleanup_workspace(workspace_path)
    
    def _validate_code(self, language: str, code: str) -> None:
        """Validate code against security rules."""
        if not code or not code.strip():
            raise CodeExecutionError("Code cannot be empty")
        
        # Check code size
        if len(code.encode('utf-8')) > self.security_settings.max_code_size:
            raise CodeExecutionError("Code exceeds maximum allowed size")
        
        if language == 'python':
            self._validate_python_code(code)
        elif language == 'jac':
            self._validate_jac_code(code)
    
    def _validate_python_code(self, code: str) -> None:
        """Validate Python code for security violations."""
        blocked_imports = self.security_settings.blocked_imports
        blocked_functions = self.security_settings.blocked_functions
        
        # Check for blocked imports
        for import_name in blocked_imports:
            if f'import {import_name}' in code or f'from {import_name}' in code:
                raise SecurityViolationError(f"Import '{import_name}' is blocked")
        
        # Check for blocked function calls
        for func_name in blocked_functions:
            if func_name in code and f'{func_name}(' in code:
                raise SecurityViolationError(f"Function '{func_name}' is blocked")
        
        # Check for dangerous patterns
        dangerous_patterns = [
            'eval(', 'exec(', '__import__', 'globals()', 'locals()',
            'open(', 'file(', 'input(', 'raw_input(', 'compile(',
            'chr(', 'ord(', 'hex(', 'oct(', 'bin('
        ]
        
        for pattern in dangerous_patterns:
            if pattern in code:
                raise SecurityViolationError(f"Dangerous pattern '{pattern}' detected")
    
    def _validate_jac_code(self, code: str) -> None:
        """Validate JAC code for basic safety."""
        # Basic validation for JAC code structure
        if 'import' in code and ('os' in code or 'sys' in code or 'subprocess' in code):
            raise SecurityViolationError("System imports are not allowed in JAC")
    
    def _execute_python(self, code: str, stdin: str, workspace_path: Path) -> Dict:
        """Execute Python code in a sandbox."""
        # Create Python script file
        script_path = workspace_path / 'script.py'
        
        # Add security wrapper if sandboxing is enabled
        if self.security_settings.enable_sandboxing:
            wrapped_code = self._wrap_python_code(code)
        else:
            wrapped_code = code
        
        # Write script to file
        script_path.write_text(wrapped_code, encoding='utf-8')
        
        # Execute with resource limits
        start_time = time.time()
        
        try:
            # Prepare execution command
            cmd = [
                self.python_path,
                '-u',  # Unbuffered output
                str(script_path)
            ]
            
            # Execute code
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(workspace_path),
                text=True,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            
            # Monitor execution time
            try:
                stdout, stderr = process.communicate(
                    input=stdin,
                    timeout=self.security_settings.max_execution_time
                )
            except subprocess.TimeoutExpired:
                # Kill process and children if timeout
                if os.name != 'nt':
                    os.killpg(os.getpgid(process.pid), 9)
                else:
                    process.kill()
                process.wait()
                return {
                    'stdout': '',
                    'stderr': 'Execution timeout exceeded',
                    'return_code': 124,
                    'execution_time': self.security_settings.max_execution_time,
                    'status': 'timeout'
                }
            
            execution_time = time.time() - start_time
            
            # Prepare result
            return {
                'stdout': stdout,
                'stderr': stderr,
                'return_code': process.returncode,
                'execution_time': execution_time,
                'status': 'completed' if process.returncode == 0 else 'failed'
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'stdout': '',
                'stderr': str(e),
                'return_code': 1,
                'execution_time': execution_time,
                'status': 'error'
            }
    
    def _execute_jac(self, code: str, stdin: str, workspace_path: Path) -> Dict:
        """Execute JAC code if JAC interpreter is available."""
        if not self.jac_path or not Path(self.jac_path).exists():
            return {
                'stdout': '',
                'stderr': 'JAC interpreter not found. Please install JAC or configure JAC_EXECUTOR_PATH.',
                'return_code': 127,
                'execution_time': 0,
                'status': 'error'
            }
        
        # Create JAC script file
        script_path = workspace_path / 'script.jac'
        script_path.write_text(code, encoding='utf-8')
        
        start_time = time.time()
        
        try:
            # Execute JAC code
            cmd = [self.jac_path, str(script_path)]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=str(workspace_path),
                text=True
            )
            
            stdout, stderr = process.communicate(
                input=stdin,
                timeout=self.security_settings.max_execution_time
            )
            
            execution_time = time.time() - start_time
            
            return {
                'stdout': stdout,
                'stderr': stderr,
                'return_code': process.returncode,
                'execution_time': execution_time,
                'status': 'completed' if process.returncode == 0 else 'failed'
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            execution_time = time.time() - start_time
            
            return {
                'stdout': '',
                'stderr': 'Execution timeout exceeded',
                'return_code': 124,
                'execution_time': execution_time,
                'status': 'timeout'
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                'stdout': '',
                'stderr': str(e),
                'return_code': 1,
                'execution_time': execution_time,
                'status': 'error'
            }
    
    def _wrap_python_code(self, code: str) -> str:
        """Wrap Python code with security restrictions."""
        wrapper = f'''
import sys
import io
import signal
import os

# Redirect stdin, stdout, stderr
sys.stdin = io.StringIO("")
sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

# Set execution time limit
def timeout_handler(signum, frame):
    print("Execution timeout exceeded", file=sys.stderr)
    sys.exit(124)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm({int(self.security_settings.max_execution_time)})

# User code starts here
{code}
# User code ends here

# Output results
print(sys.stdout.getvalue(), end="")
print(sys.stderr.getvalue(), file=sys.stderr, end="")
'''
        return wrapper
    
    def _cleanup_workspace(self, workspace_path: Path) -> None:
        """Clean up temporary workspace directory."""
        try:
            if workspace_path.exists():
                shutil.rmtree(workspace_path)
        except Exception as e:
            # Log cleanup error but don't raise exception
            print(f"Warning: Failed to clean up workspace {workspace_path}: {e}")
    
    def __del__(self):
        """Cleanup when executor is destroyed."""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
        except Exception:
            pass  # Ignore cleanup errors in destructor


class ExecutionService:
    """
    Service for managing code execution requests and results.
    """
    
    def __init__(self):
        """Initialize the execution service."""
        self.executor = CodeExecutor()
    
    def execute_with_tracking(self, user, language: str, code: str, 
                             stdin: str = '', save_result: bool = True) -> Dict:
        """
        Execute code with user tracking and optional database storage.
        
        Args:
            user: Django user object
            language: Programming language
            code: Code to execute
            stdin: Standard input data
            save_result: Whether to save result to database
            
        Returns:
            Dictionary with execution results
        """
        execution_record = None
        
        if save_result:
            # Create execution record
            from ..models import CodeExecution
            execution_record = CodeExecution.objects.create(
                user=user,
                language=language,
                code=code,
                stdin=stdin,
                status='running',
                max_execution_time=self.executor.security_settings.max_execution_time,
                max_memory=self.executor.security_settings.max_memory,
                max_output_size=self.executor.security_settings.max_output_size
            )
        
        try:
            # Execute code
            result = self.executor.execute_code(language, code, stdin)
            
            if execution_record:
                # Update execution record with results
                execution_record.status = result.get('status', 'error')
                execution_record.stdout = result.get('stdout', '')
                execution_record.stderr = result.get('stderr', '')
                execution_record.return_code = result.get('return_code', 1)
                execution_record.execution_time = result.get('execution_time', 0)
                execution_record.completed_at = timezone.now()
                execution_record.save()
                
                # Update user session statistics
                self._update_user_session(user, execution_record)
            
            return result
            
        except Exception as e:
            error_result = {
                'stdout': '',
                'stderr': str(e),
                'return_code': 1,
                'execution_time': 0,
                'status': 'error'
            }
            
            if execution_record:
                execution_record.status = 'error'
                execution_record.stderr = str(e)
                execution_record.completed_at = timezone.now()
                execution_record.save()
            
            return error_result
    
    def _update_user_session(self, user, execution_record):
        """Update user's execution session statistics."""
        from ..models import CodeExecutionSession
        from django.utils import timezone
        
        # Get or create active session
        session_id = f"session_{user.id}_{timezone.now().strftime('%Y%m%d')}"
        session, created = CodeExecutionSession.objects.get_or_create(
            session_id=session_id,
            user=user,
            defaults={'started_at': timezone.now()}
        )
        
        session.update_statistics(execution_record)
    
    def get_execution_history(self, user, limit: int = 50, 
                             language: Optional[str] = None) -> List[Dict]:
        """Get user's execution history."""
        from ..models import CodeExecution
        
        queryset = CodeExecution.objects.filter(user=user)
        
        if language:
            queryset = queryset.filter(language=language)
        
        executions = queryset.order_by('-created_at')[:limit]
        
        return [
            {
                'id': str(exec.id),
                'language': exec.language,
                'status': exec.status,
                'execution_time': exec.execution_time,
                'created_at': exec.created_at,
                'summary': exec.get_execution_summary()
            }
            for exec in executions
        ]
    
    def get_user_statistics(self, user) -> Dict:
        """Get user execution statistics."""
        from ..models import CodeExecution, CodeExecutionSession
        
        # Execution stats
        total_executions = CodeExecution.objects.filter(user=user).count()
        successful_executions = CodeExecution.objects.filter(
            user=user, status='completed', return_code=0
        ).count()
        failed_executions = total_executions - successful_executions
        
        # Language distribution
        language_stats = {}
        for lang in ['jac', 'python']:
            count = CodeExecution.objects.filter(user=user, language=lang).count()
            language_stats[lang] = count
        
        # Recent sessions
        recent_sessions = CodeExecutionSession.objects.filter(
            user=user
        ).order_by('-started_at')[:10]
        
        session_stats = [
            {
                'session_id': session.session_id,
                'total_executions': session.total_executions,
                'success_rate': session.success_rate,
                'started_at': session.started_at
            }
            for session in recent_sessions
        ]
        
        return {
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': failed_executions,
            'success_rate': (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            'language_distribution': language_stats,
            'recent_sessions': session_stats
        }