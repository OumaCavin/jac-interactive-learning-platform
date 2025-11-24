"""
Learning App Package
====================

This Django app contains the core learning functionality for the JAC Learning Platform.

Main Components:
- MockJWTAuthentication: Middleware for handling mock JWT tokens during development
- Learning models and views
- Code execution engine
- Assessment management

This package provides:
- Adaptive learning path management
- Real-time code execution capabilities
- Multi-agent learning assistance
- Personalized learning experiences

Author: MiniMax Agent
Created: 2025-11-24
"""

# Django App Configuration
default_app_config = 'apps.learning.apps.LearningConfig'

# Import middleware for easy access (optional)
try:
    from .middleware import MockJWTAuthentication
    __all__ = ['MockJWTAuthentication']
except ImportError:
    # Middleware might not be available during app loading
    pass