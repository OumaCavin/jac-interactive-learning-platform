# JAC Platform Configuration - Settings by Cavin Otieno

"""
Django configuration module initialization.
This module initializes the Celery application for background tasks.
"""

try:
    from .celery import celery_app
    # Export the celery instance so other modules can import it
    __all__ = ['celery_app']
except ImportError:
    # Celery is optional - continue without it if not available
    __all__ = []