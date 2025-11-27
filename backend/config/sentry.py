# JAC Platform Configuration - Settings by Cavin Otieno

"""
Sentry Error Monitoring Configuration for JAC Learning Platform
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

def init_sentry_monitoring():
    """Initialize Sentry monitoring for the application"""
    
    # Get DSN from environment (never hardcode!)
    sentry_dsn = os.getenv('SENTRY_DSN_BACKEND', 'https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000')
    
    if not sentry_dsn or sentry_dsn == 'https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000':
        # Only enable Sentry if DSN is provided (use default for demo)
        return
        
    # Sentry configuration
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            DjangoIntegration(
                auto_enabling=True,
                transaction_style="endpoint",
            ),
            CeleryIntegration(
                monitor_beat_tasks=True,
                monitor_queues=True,
            ),
            RedisIntegration(),
            LoggingIntegration(
                level=os.getenv('SENTRY_LOG_LEVEL', 'INFO'),
                event_level=None,
            ),
        ],
        
        # Performance monitoring
        traces_sample_rate=float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        
        # Profiling (performance insights)
        profiles_sample_rate=float(os.getenv('SENTRY_PROFILES_SAMPLE_RATE', '0.0')),
        
        # Privacy and security
        send_default_pii=False,  # Don't send personally identifiable information
        send_attention_pii=True,  # Include error messages with PII if present
        
        # Environment and release information
        environment=os.getenv('ENVIRONMENT', 'development'),
        release=os.getenv('RELEASE_VERSION', 'dev'),
        
        # Session tracking
        auto_session_tracking=True,
        session_timeout=30,  # minutes
        
        # Error filtering
        before_send=filter_sentry_events,
        
        # Debug mode (only for development)
        debug=os.getenv('ENVIRONMENT') == 'development',
        
        # Additional configuration
        initial_scope={
            'tags': {
                'platform': 'jac-learning-platform',
                'service': 'backend',
            }
        }
    )

def filter_sentry_events(event, hint):
    """
    Filter out specific events that shouldn't be sent to Sentry
    """
    
    # Ignore health check requests
    if event.get('request', {}).get('url', '').endswith('/health/'):
        return None
        
    # Ignore common benign errors
    if event.get('exception', {}):
        for exception in event['exception']['values']:
            if 'CSRF' in exception.get('value', ''):
                return None
            if 'permission denied' in exception.get('value', '').lower():
                return None
                
    # Ignore rate limit responses
    if event.get('transaction') == '/api/auth/login' and 'rate limit' in event.get('message', '').lower():
        return None
        
    # Keep all other events
    return event

def set_user_context(user=None, request=None):
    """
    Set user context for error tracking (anonymized)
    """
    if user and hasattr(user, 'id'):
        sentry_sdk.set_user({
            "id": str(user.id),  # Convert to string for consistency
            "username": getattr(user, 'username', 'unknown'),
            "is_authenticated": user.is_authenticated,
        })
        
        # Add request context
        if request:
            sentry_sdk.set_extra("request_path", request.path)
            sentry_sdk.set_extra("request_method", request.method)

def set_agent_context(agent_type, agent_id=None, task_id=None):
    """
    Set context for multi-agent system errors
    """
    sentry_sdk.set_tag("agent_type", agent_type)
    if agent_id:
        sentry_sdk.set_tag("agent_id", agent_id)
    if task_id:
        sentry_sdk.set_tag("task_id", task_id)

def set_code_execution_context(execution_id, language, user_id=None):
    """
    Set context for JAC code execution errors
    """
    sentry_sdk.set_tag("execution_type", "code_execution")
    sentry_sdk.set_tag("execution_language", language)
    sentry_sdk.set_extra("execution_id", execution_id)
    if user_id:
        sentry_sdk.set_extra("execution_user_id", user_id)

def set_api_context(endpoint, method, status_code=None):
    """
    Set context for API errors
    """
    sentry_sdk.set_tag("api_endpoint", endpoint)
    sentry_sdk.set_tag("api_method", method)
    if status_code:
        sentry_sdk.set_tag("http_status_code", str(status_code))

# Initialize Sentry when module is imported
init_sentry_monitoring()