"""
Management App Package - JAC Learning Platform

This package provides Django management commands and platform utilities
for the JAC Interactive Learning Platform.

Components:
- commands: Custom Django management commands for platform administration
  - initialize_platform: Command for platform initialization

Django App Configuration:
- Uses ManagementConfig from apps.management
- Automatic command discovery through Django's management framework

Usage:
    # Import management commands
    from apps.management.commands.initialize_platform import InitializePlatformCommand
    
    # Run management command
    python manage.py initialize_platform --help

Author: MiniMax Agent
Created: 2025-11-24
"""

# Django App Configuration
default_app_config = 'apps.management.apps.ManagementConfig'

# Safe imports of management components
try:
    from .commands.initialize_platform import InitializePlatformCommand
    __all__ = ['InitializePlatformCommand']
except ImportError:
    # Handle case where commands module might not be available
    pass

# Package metadata
__version__ = "1.0.0"
__author__ = "MiniMax Agent"