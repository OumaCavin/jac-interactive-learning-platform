# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Collaboration App Configuration - JAC Learning Platform

Django app configuration for collaboration features.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.apps import AppConfig

class CollaborationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.collaboration'
    verbose_name = 'Collaboration System'
    
    def ready(self):
        """Import signals when the app is ready"""
        import apps.collaboration.signals