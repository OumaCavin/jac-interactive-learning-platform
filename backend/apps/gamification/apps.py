"""
Gamification App Configuration - JAC Learning Platform

Django app configuration for the gamification system.

Author: MiniMax Agent
Created: 2025-11-26
"""

from django.apps import AppConfig


class GamificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gamification'
    verbose_name = 'Gamification System'
    
    def ready(self):
        """Import signals when the app is ready"""
        import apps.gamification.signals