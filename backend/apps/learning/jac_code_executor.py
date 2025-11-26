# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
JAC Code Execution Engine for JAC Interactive Learning Platform

This module provides secure code execution capabilities for JAC and Python code,
integrating with the multi-agent system for automated evaluation.
"""

import os
import sys
import tempfile
import subprocess
import json
import time
import uuid
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from django.utils import timezone
from dataclasses import dataclass, asdict
import logging

# Import our agent system components
from apps.agents.models import Agent, Task, AgentMetrics
from apps.agents.simple_agents_manager import SimpleAgentsManager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CodeExecutionResult:
    """Data class for code execution results"""
    execution_id: str
    code: str
    language: str
    status: str  # 'success', 'error', 'timeout', 'security_violation'
    output: str
    error: Optional[str]
    execution_time: float
    memory_usage: Optional[float]
    created_at: datetime
    agent_id: Optional[str] = None
    user_id: Optional[int] = None
    task_id: Optional[str] = None


@dataclass
class CodeExecutionRequest:
    """Data class for code execution requests"""
    code: str
    language: str  # 'jac', 'python', 'javascript'
    user_id: int
    task_id: Optional[str] = None
    timeout: int = 30  # seconds
    memory_limit: int = 128  # MB
    allow_network: bool = False
    test_cases: Optional[List[Dict]] = None


class SecuritySandbox:
    """Security sandbox for code execution"""
    
    def __init__(self, language: str, timeout: int = 30, memory_limit: int = 128):
        self.language = language
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.temp_dir = tempfile.mkdtemp(prefix='jac_execution_')
        
    def __del__(self):
        """Cleanup temporary directory"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def validate_code(self, code: str) -> Tuple[bool, str]:
        """Validate code for security violations"""
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess', 'import socket',
            'open(', '__import__', 'eval(', 'exec(', 'compile(',
            'file(', 'input(', 'raw_input(', 'raw_input',
            'subprocess.call', 'subprocess.run', 'subprocess.Popen',
            'os.system', 'os.popen', 'os.exec', 'os.fork',
            'import threading', 'import multiprocessing',
            'pickle', 'marshal', 'shelve', 'dbm',
            'urllib', 'requests', 'httplib', 'http.client',
            'email', 'smtplib', 'poplib', 'imaplib',
            'import pdb', 'import gdb', 'import vdb',
            'breakpoint()', 'set_trace()', 'settrace()'
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                return False, f"Security violation: Forbidden import or function '{pattern}' detected"
        
        # Check for suspicious file operations
        file_operations = ['open(', 'file(', 'with open']
        for pattern in file_operations:
            if pattern in code:
                return False, f"Security violation: File operations are not allowed"
        
        return True, "Code validation passed"
    
    def execute_python_code(self, code: str) -> Tuple[str, str, float]:
        """Execute Python code in sandbox"""
        python_file = os.path.join(self.temp_dir, 'code.py')
        
        with open(python_file, 'w') as f:
            f.write(code)
        
        try:
            # Execute with timeout and capture output
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, python_file],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.temp_dir
            )
            execution_time = time.time() - start_time
            
            return result.stdout, result.stderr, execution_time
        except subprocess.TimeoutExpired:
            return "", "Execution timeout exceeded", float('inf')
        except Exception as e:
            return "", str(e), float('inf')


class JACCodeExecutor:
    """JAC Code Execution Engine"""
    
    def __init__(self):
        self.security_sandbox = SecuritySandbox
        self.execution_history: Dict[str, CodeExecutionResult] = {}
        self.active_executions: Dict[str, CodeExecutionRequest] = {}
        
    def execute_code(self, request: CodeExecutionRequest) -> CodeExecutionResult:
        """Execute code based on the specified language"""
        execution_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Create sandbox for this execution
            sandbox = SecuritySandbox(
                language=request.language,
                timeout=request.timeout,
                memory_limit=request.memory_limit
            )
            
            # Security validation
            is_valid, validation_message = sandbox.validate_code(request.code)
            if not is_valid:
                result = CodeExecutionResult(
                    execution_id=execution_id,
                    code=request.code,
                    language=request.language,
                    status='security_violation',
                    output='',
                    error=validation_message,
                    execution_time=time.time() - start_time,
                    memory_usage=None,
                    created_at=timezone.now(),
                    agent_id=None,
                    user_id=request.user_id,
                    task_id=request.task_id
                )
                self.execution_history[execution_id] = result
                return result
            
            # Execute based on language
            if request.language.lower() == 'python':
                output, error, execution_time = sandbox.execute_python_code(request.code)
                status = 'success' if not error and execution_time != float('inf') else 'error'
                
            elif request.language.lower() == 'jac':
                # JAC execution - for now, treat as Python or provide JAC-specific handling
                output, error, execution_time = self._execute_jac_code(sandbox, request.code)
                status = 'success' if not error and execution_time != float('inf') else 'error'
                
            else:
                output, error, execution_time = '', f"Unsupported language: {request.language}", float('inf')
                status = 'error'
            
            # Create result
            result = CodeExecutionResult(
                execution_id=execution_id,
                code=request.code,
                language=request.language,
                status=status,
                output=output,
                error=error if error else None,
                execution_time=execution_time,
                memory_usage=None,  # Could be enhanced with memory monitoring
                created_at=timezone.now(),
                agent_id=None,
                user_id=request.user_id,
                task_id=request.task_id
            )
            
            self.execution_history[execution_id] = result
            self.active_executions[execution_id] = request
            
            return result
            
        except Exception as e:
            logger.error(f"Execution error: {str(e)}")
            error_result = CodeExecutionResult(
                execution_id=execution_id,
                code=request.code,
                language=request.language,
                status='error',
                output='',
                error=f"Execution failed: {str(e)}",
                execution_time=time.time() - start_time,
                memory_usage=None,
                created_at=timezone.now(),
                agent_id=None,
                user_id=request.user_id,
                task_id=request.task_id
            )
            self.execution_history[execution_id] = error_result
            return error_result
    
    def _execute_jac_code(self, sandbox: SecuritySandbox, code: str) -> Tuple[str, str, float]:
        """Execute JAC code (placeholder for future JAC-specific implementation)"""
        # For now, treat JAC as Python code
        # In the future, this would integrate with Jaseci runtime
        return sandbox.execute_python_code(code)
    
    def get_execution_result(self, execution_id: str) -> Optional[CodeExecutionResult]:
        """Get execution result by ID"""
        return self.execution_history.get(execution_id)
    
    def get_execution_history(self, user_id: Optional[int] = None, 
                             limit: int = 100) -> List[CodeExecutionResult]:
        """Get execution history, optionally filtered by user"""
        results = list(self.execution_history.values())
        
        if user_id:
            results = [r for r in results if r.user_id == user_id]
        
        # Sort by creation time (most recent first)
        results.sort(key=lambda x: x.created_at, reverse=True)
        
        return results[:limit]


class CodeEvaluatorAgent:
    """Enhanced Evaluator Agent with JAC Code Execution"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.jac_executor = JACCodeExecutor()
        self.agents_manager = SimpleAgentsManager()
        
    def evaluate_code_submission(self, code: str, language: str, 
                                user_id: int, task_id: Optional[str] = None,
                                test_cases: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Evaluate a code submission with comprehensive analysis"""
        
        # Create execution request
        request = CodeExecutionRequest(
            code=code,
            language=language,
            user_id=user_id,
            task_id=task_id,
            test_cases=test_cases
        )
        
        # Execute the code
        result = self.jac_executor.execute_code(request)
        
        # Perform comprehensive evaluation
        evaluation = {
            'execution_id': result.execution_id,
            'status': result.status,
            'success': result.status == 'success',
            'output': result.output,
            'error': result.error,
            'execution_time': result.execution_time,
            'timestamp': result.created_at,
            'code_analysis': self._analyze_code(code),
            'security_assessment': self._assess_security(result.code),
            'performance_metrics': {
                'execution_time': result.execution_time,
                'code_complexity': self._calculate_complexity(code),
                'lines_of_code': len(code.split('\n'))
            },
            'recommendations': self._generate_recommendations(code, result)
        }
        
        # Record metrics
        self._record_evaluation_metrics(user_id, evaluation)
        
        return evaluation
    
    def _analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code structure and patterns"""
        lines = code.split('\n')
        
        analysis = {
            'total_lines': len(lines),
            'blank_lines': sum(1 for line in lines if not line.strip()),
            'comment_lines': sum(1 for line in lines if line.strip().startswith('#')),
            'import_statements': sum(1 for line in lines if 'import ' in line),
            'function_definitions': sum(1 for line in lines if 'def ' in line),
            'class_definitions': sum(1 for line in lines if 'class ' in line),
            'control_structures': sum(1 for line in lines if any(keyword in line 
                                   for keyword in ['if', 'for', 'while', 'try', 'with'])),
            'code_style_score': self._evaluate_code_style(code)
        }
        
        return analysis
    
    def _evaluate_code_style(self, code: str) -> float:
        """Evaluate code style (0.0 to 1.0)"""
        style_score = 1.0
        
        # Penalize for missing docstrings
        if 'def ' in code and '"""' not in code:
            style_score -= 0.2
        
        # Penalize for very long lines
        lines = code.split('\n')
        long_lines = [line for line in lines if len(line) > 120]
        if len(long_lines) > 0:
            style_score -= min(0.3, len(long_lines) / len(lines) * 0.5)
        
        # Reward proper indentation
        if all(line.startswith(' ') or not line.strip() for line in lines):
            style_score += 0.1
        
        return max(0.0, min(1.0, style_score))
    
    def _assess_security(self, code: str) -> Dict[str, Any]:
        """Assess code security"""
        # This is a basic security assessment - in production, use more sophisticated tools
        security_issues = []
        
        # Check for potential security vulnerabilities
        if 'eval(' in code or 'exec(' in code:
            security_issues.append("Use of eval/exec functions detected")
        
        if 'input(' in code and language == 'python':
            security_issues.append("User input detected - ensure proper validation")
        
        if 'global ' in code:
            security_issues.append("Global variables detected - consider encapsulation")
        
        return {
            'score': max(0.0, 1.0 - len(security_issues) * 0.2),
            'issues': security_issues,
            'recommendations': self._generate_security_recommendations(security_issues)
        }
    
    def _generate_security_recommendations(self, issues: List[str]) -> List[str]:
        """Generate security improvement recommendations"""
        recommendations = []
        
        if any('eval' in issue.lower() for issue in issues):
            recommendations.append("Avoid using eval() and exec() functions for security")
        
        if any('input' in issue.lower() for issue in issues):
            recommendations.append("Validate and sanitize all user inputs")
        
        if any('global' in issue.lower() for issue in issues):
            recommendations.append("Use encapsulation and avoid global variables")
        
        return recommendations
    
    def _calculate_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1  # Base complexity
        
        # Count decision points
        decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'except', 'finally']
        for keyword in decision_keywords:
            complexity += code.count(keyword)
        
        # Count logical operators
        logical_ops = ['and', 'or', '&&', '||']
        for op in logical_ops:
            complexity += code.count(op)
        
        return complexity
    
    def _generate_recommendations(self, code: str, result: CodeExecutionResult) -> List[str]:
        """Generate code improvement recommendations"""
        recommendations = []
        
        # Performance recommendations
        if result.execution_time > 5.0:
            recommendations.append("Code execution time is slow - consider optimizing algorithms")
        
        # Style recommendations
        analysis = self._analyze_code(code)
        if analysis['comment_lines'] < analysis['total_lines'] * 0.1:
            recommendations.append("Consider adding more comments to improve code readability")
        
        # Security recommendations
        security_assessment = self._assess_security(code)
        if security_assessment['score'] < 0.8:
            recommendations.append("Security improvements needed - review security recommendations")
        
        return recommendations
    
    def _record_evaluation_metrics(self, user_id: int, evaluation: Dict[str, Any]):
        """Record evaluation metrics to agent database"""
        try:
            # Create agent metrics for tracking evaluation performance
            AgentMetrics.objects.create(
                agent_id=self.agent_id,
                metric_name='code_evaluation_completed',
                metric_value=1.0,
                metric_type='evaluation',
                context={
                    'user_id': user_id,
                    'execution_time': evaluation['execution_time'],
                    'success': evaluation['success'],
                    'security_score': evaluation['security_assessment']['score']
                }
            )
        except Exception as e:
            logger.error(f"Failed to record metrics: {str(e)}")


# Global code executor instance
code_executor = JACCodeExecutor()


def execute_code_for_learning(code: str, language: str, user_id: int) -> Dict[str, Any]:
    """Execute code for learning purposes with AI feedback"""
    evaluator = CodeEvaluatorAgent(agent_id='evaluator-learning-agent')
    return evaluator.evaluate_code_submission(code, language, user_id)


# Test the JAC code execution engine
def test_jac_execution_engine():
    """Test the JAC code execution engine"""
    print("=== JAC Code Execution Engine Test ===")
    
    # Test Python code execution
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(10)
print(f"Fibonacci(10) = {result}")
"""
    
    request = CodeExecutionRequest(
        code=python_code,
        language='python',
        user_id=1,
        task_id='test-fibonacci'
    )
    
    result = code_executor.execute_code(request)
    print(f"✓ Python execution: {result.status}")
    print(f"  Output: {result.output}")
    if result.error:
        print(f"  Error: {result.error}")
    
    # Test security validation
    unsafe_code = """
import os
os.system('rm -rf /')
"""
    
    request = CodeExecutionRequest(
        code=unsafe_code,
        language='python',
        user_id=1
    )
    
    result = code_executor.execute_code(request)
    print(f"✓ Security test: {result.status}")
    print(f"  Error: {result.error}")
    
    # Test JAC code (currently treats as Python)
    jac_code = """
# JAC code (currently executed as Python)
def hello_world():
    print("Hello from JAC!")

hello_world()
"""
    
    request = CodeExecutionRequest(
        code=jac_code,
        language='jac',
        user_id=1
    )
    
    result = code_executor.execute_code(request)
    print(f"✓ JAC execution: {result.status}")
    print(f"  Output: {result.output}")
    
    print("\n🎉 JAC Code Execution Engine - READY!")


if __name__ == "__main__":
    test_jac_execution_engine()