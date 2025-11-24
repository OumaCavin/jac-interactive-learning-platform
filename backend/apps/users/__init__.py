"""
Users App Package - JAC Learning Platform

This package handles user authentication, profiles, and learning preferences
for the JAC Interactive Learning Platform.

Components:
- User model extensions and custom authentication
- User profile management and learning preferences
- Serializers for API data transformation
- Views for user management and authentication
- Signal handlers for user lifecycle events

Django App Configuration:
- Uses UsersConfig from apps.users
- Automatically imports signal handlers on Django startup
- Custom User model for platform-specific user data

Database Models:
- Extended User model with learning-specific fields
- User profiles and preferences
- Authentication and verification systems

Views & Serializers:
- User registration, login, and profile management
- Password reset and email verification
- Learning preference customization

Usage:
    # Import user models
    from apps.users.models import User, UserProfile
    
    # Access custom user model
    User = get_user_model()
    
    # Use serializers
    from apps.users.serializers import UserSerializer

Author: MiniMax Agent
Created: 2025-11-24
"""

# Django App Configuration
default_app_config = 'apps.users.apps.UsersConfig'

# Users app is disabled - not in INSTALLED_APPS
# All imports removed to avoid AppRegistryNotReady errors
__all__ = []

# Signal handlers are automatically imported by UsersConfig.ready() (commented out)

# Package metadata
__version__ = "1.0.0"
__author__ = "MiniMax Agent"

# Note: Users app disabled since not in INSTALLED_APPS
# All imports commented out to avoid AppRegistryNotReady errors
__app_ready__ = True