# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Django app configuration for agents
"""

from django.apps import AppConfig


class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.agents'
    verbose_name = 'AI Agents'
    
    def ready(self):
        """Import signal handlers when Django starts"""
        # Import signal handlers if any are created
        # from . import signals  # noqa
        pass