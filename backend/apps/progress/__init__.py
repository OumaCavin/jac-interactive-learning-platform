# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Progress App Package - JAC Learning Platform

This package handles user learning progress tracking, analytics,
and performance monitoring for the JAC Interactive Learning Platform.

Components:
- Models for tracking user progress, completion rates, and performance metrics
- Views for progress visualization and analytics
- Serializers for API data transformation

Django App Configuration:
- Uses ProgressConfig from apps.progress
- Designed for tracking learning progress and analytics

Database Models:
- Progress tracking for modules, assessments, and learning paths
- Performance analytics and reporting
- User engagement metrics

Usage:
    # Import progress models
    from apps.progress.models import UserProgress, LearningAnalytics
    
    # Track user progress
    progress = UserProgress.objects.create(
        user=request.user,
        module=module,
        progress_percentage=75
    )

Author: Cavin Otieno
Created: 2025-11-24
"""

# Django App Configuration
default_app_config = 'apps.progress.apps.ProgressConfig'

# Package metadata
__version__ = "1.0.0"
__author__ = "Cavin Otieno"

# Optional imports - handle gracefully if models don't exist yet
try:
    # These imports will work once models are defined
    # For now, just set up the package structure
    __all__ = []  # Will be populated when models are implemented
except ImportError:
    pass