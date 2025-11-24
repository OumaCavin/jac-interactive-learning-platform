"""
Configuration for the JAC Execution app.
Secure code execution engine for the JAC Learning Platform.
"""

from django.apps import AppConfig


class JacExecutionConfig(AppConfig):
    """Configuration for the JAC Execution app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.jac_execution'
    verbose_name = 'JAC Code Execution'
    
    def ready(self):
        """Import signal handlers and initialize execution environment when Django starts."""
        import apps.jac_execution.signals  # Import any signal handlers if defined
        
        # Initialize execution environment
        self._setup_execution_environment()
    
    def _setup_execution_environment(self):
        """Setup execution environment with security configurations."""
        # This will be called when Django starts to initialize execution environment
        pass
    
    def get_execution_config(self):
        """Get execution environment configuration."""
        return {
            'timeout': 30,  # seconds
            'memory_limit_mb': 128,
            'max_output_size': 1024,
            'supported_languages': ['jac', 'python'],
            'sandbox_enabled': True,
            'security_isolation': True
        }