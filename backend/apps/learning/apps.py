"""
Learning app for the JAC Learning Platform.
Manages learning paths, modules, and personalized learning experiences.
"""

from django.apps import AppConfig


class LearningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.learning'
    
    def ready(self):
        """Learning app is ready."""
        pass