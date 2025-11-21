"""
Users app for the JAC Learning Platform.
Handles user authentication, profiles, and learning preferences.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    
    def ready(self):
        """Import signal handlers when Django starts."""
        import apps.users.signals