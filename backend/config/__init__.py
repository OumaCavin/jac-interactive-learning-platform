"""
Django configuration module initialization.
This module initializes the Celery application for background tasks.
"""

from .celery import celery_app

# Export the celery instance so other modules can import it
__all__ = ['celery_app']