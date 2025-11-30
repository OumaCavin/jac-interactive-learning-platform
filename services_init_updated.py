# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Progress Services Package

This package contains service classes for progress tracking and analytics
in the JAC Interactive Learning Platform.

Services:
- ProgressService: Core progress tracking and snapshot management
- AnalyticsService: Advanced analytics and reporting
- NotificationService: Progress notifications and alerts
- PredictiveAnalyticsService: ML-based predictive analytics
- RealtimeMonitoringService: Real-time progress monitoring
- AdvancedAnalyticsService: Advanced analytics and statistics

Author: Cavin Otieno
Created: 2025-11-30
"""

from .progress_service import ProgressService
from .analytics_service import AnalyticsService
from .notification_service import NotificationService
from .predictive_analytics_service import PredictiveAnalyticsService
from .realtime_monitoring_service import RealtimeMonitoringService
from .advanced_analytics_service import AdvancedAnalyticsService

__all__ = [
    'ProgressService', 
    'AnalyticsService', 
    'NotificationService',
    'PredictiveAnalyticsService',
    'RealtimeMonitoringService',
    'AdvancedAnalyticsService'
]