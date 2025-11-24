"""
Progress App URL Configuration

This module defines the URL patterns for the progress app API endpoints,
providing RESTful access to progress tracking and analytics functionality.

URL Patterns:
- /api/progress/snapshots/ - Progress snapshot management
- /api/progress/analytics/ - Learning analytics endpoints
- /api/progress/achievements/ - Achievement management
- /api/progress/metrics/ - User progress metrics
- /api/progress/goals/ - Progress goal management
- /api/progress/notifications/ - Progress notifications
- /api/progress/summary/ - Comprehensive progress summary
- /api/progress/track/ - Real-time progress tracking

Author: MiniMax Agent
Created: 2025-11-25
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProgressSnapshotViewSet, LearningAnalyticsViewSet, AchievementViewSet,
    UserProgressMetricViewSet, ProgressGoalViewSet, ProgressNotificationViewSet,
    ProgressSummaryAPIView, ProgressAnalyticsAPIView, CreateProgressSnapshotAPIView,
    TrackUserProgressAPIView
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'snapshots', ProgressSnapshotViewSet, basename='progresssnapshot')
router.register(r'analytics', LearningAnalyticsViewSet, basename='learninganalytics')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'metrics', UserProgressMetricViewSet, basename='userprogressmetric')
router.register(r'goals', ProgressGoalViewSet, basename='progressgoal')
router.register(r'notifications', ProgressNotificationViewSet, basename='progressnotification')

app_name = 'progress'

urlpatterns = [
    # Include router URLs
    path('api/v1/', include(router.urls)),
    
    # Custom API endpoints
    path('api/v1/summary/', ProgressSummaryAPIView.as_view(), name='progress-summary'),
    path('api/v1/analytics/comprehensive/', ProgressAnalyticsAPIView.as_view(), name='progress-analytics-comprehensive'),
    path('api/v1/snapshots/create/', CreateProgressSnapshotAPIView.as_view(), name='create-progress-snapshot'),
    path('api/v1/track/', TrackUserProgressAPIView.as_view(), name='track-user-progress'),
    
    # Alternative endpoint without API version (for frontend compatibility)
    path('api/summary/', ProgressSummaryAPIView.as_view(), name='progress-summary-no-version'),
    path('api/analytics/comprehensive/', ProgressAnalyticsAPIView.as_view(), name='progress-analytics-comprehensive-no-version'),
    path('api/snapshots/create/', CreateProgressSnapshotAPIView.as_view(), name='create-progress-snapshot-no-version'),
    path('api/track/', TrackUserProgressAPIView.as_view(), name='track-user-progress-no-version'),
    
    # Shorter URLs for common operations
    path('api/v1/progress/summary/', ProgressSummaryAPIView.as_view(), name='progress-summary-short'),
    path('api/v1/progress/analytics/', ProgressAnalyticsAPIView.as_view(), name='progress-analytics-short'),
]