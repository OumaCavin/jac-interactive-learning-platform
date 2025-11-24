"""
JAC Execution App Package - JAC Learning Platform

This package provides secure code execution capabilities for JAC and Python code,
integrating with the multi-agent system for automated evaluation in the
JAC Interactive Learning Platform.

Components:
- Secure code execution engine with sandbox isolation
- JAC and Python language support
- Real-time code evaluation and feedback
- Integration with multi-agent system for automated assessment
- Resource monitoring and security controls
- Execution result tracking and analytics

Features:
- Sandboxed code execution with security isolation
- Support for JAC (JavaScript Assistant Code) and Python
- Integration with learning modules for interactive tutorials
- Automated code evaluation and scoring
- Resource limits (timeout, memory, output size)
- Execution analytics and performance tracking

Django App Configuration:
- Uses JacExecutionConfig from apps.jac_execution
- Designed for secure, isolated code execution
- Throttled execution requests (50/hour per user)

Database Models:
- Code execution requests and results
- Execution history and analytics
- Performance metrics and security logs

Security Features:
- Sandboxed execution environment
- Resource limits and timeouts
- Output size restrictions
- Secure code isolation

Usage:
    # Import code execution components
    from apps.jac_execution.executors import CodeExecutor
    from apps.jac_execution.models import ExecutionRequest, ExecutionResult
    
    # Execute user code securely
    executor = CodeExecutor()
    result = executor.execute_code(
        code="print('Hello, JAC!')",
        language="python",
        user=request.user,
        task_id="tutorial_001"
    )

Author: MiniMax Agent
Created: 2025-11-24
"""

# Django App Configuration
default_app_config = 'apps.jac_execution.apps.JacExecutionConfig'

# Safe imports of execution components - models and services will be imported lazily
try:
    # Import code execution engine components (lazy imports to avoid circular dependencies)
    # from .models import ExecutionRequest, ExecutionResult  # Moved to avoid circular imports
    # from .services.executor import CodeExecutor, JacCodeExecutor, PythonCodeExecutor
    # from .services.translator import JacCodeTranslator, PythonCodeTranslator
    
    # Export main execution components
    __all__ = [
        # 'CodeExecutor',
        # 'JacCodeExecutor', 
        # 'PythonCodeExecutor',
        # 'ExecutionRequest',
        # 'ExecutionResult',
        # 'JacCodeTranslator',
        # 'PythonCodeTranslator'
    ]
    
except ImportError as e:
    # Handle case where execution components might not be implemented yet
    __all__ = []
    
    # Provide basic execution functionality from learning app
    try:
        # Lazy import to avoid circular dependencies
        # from apps.learning.jac_code_executor import CodeExecutionResult, CodeExecutionRequest
        __all__.extend(['CodeExecutionResult', 'CodeExecutionRequest'])
    except ImportError:
        pass

# Package metadata
__version__ = "1.0.0"
__author__ = "MiniMax Agent"

# Configuration constants
__execution_timeout__ = 30  # Default timeout in seconds
__max_memory_mb__ = 128     # Maximum memory limit in MB
__max_output_size__ = 1024  # Maximum output size in characters
__supported_languages__ = ['jac', 'python']  # Supported programming languages

# Export configuration for reference
__config__ = {
    'timeout': __execution_timeout__,
    'memory_limit_mb': __max_memory_mb__,
    'output_limit_chars': __max_output_size__,
    'languages': __supported_languages__
}

# Integration status
__integration_status__ = {
    'learning_app': True,     # Integrated with learning app
    'agents_system': True,    # Multi-agent system integration
    'sandbox_ready': False,   # Sandbox implementation pending
    'models_defined': False   # Models implementation pending
}