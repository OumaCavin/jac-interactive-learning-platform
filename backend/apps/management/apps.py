# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Configuration for the management app.
Custom Django app for management commands and platform utilities.
"""

from django.apps import AppConfig


class ManagementConfig(AppConfig):
    """Configuration for the management app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.management'
    verbose_name = 'Platform Management'
    
    def ready(self):
        """Import signal handlers when Django starts."""
        pass