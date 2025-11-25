"""
Progress Services Package

This package contains service classes for progress tracking and analytics
in the JAC Interactive Learning Platform.

Services:
- ProgressService: Core progress tracking and snapshot management
- AnalyticsService: Advanced analytics and reporting
- NotificationService: Progress notifications and alerts

Author: Cavin Otieno
Created: 2025-11-25
"""

from .progress_service import ProgressService
from .analytics_service import AnalyticsService
from .notification_service import NotificationService

__all__ = ['ProgressService', 'AnalyticsService', 'NotificationService']