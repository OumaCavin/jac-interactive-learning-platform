# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

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

Author: Cavin Otieno
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
from .views_predictive import (
    MLPredictionsAPIView, HistoricalTrendsAPIView, AdaptivePredictionsAPIView,
    ConfidenceCalculationsAPIView, ComprehensivePredictiveAnalyticsAPIView,
    predictive_dashboard_data,
    # New Predictive Learning Models APIs
    LearningVelocityAPIView, EngagementPatternsAPIView, SuccessProbabilityAPIView,
    TimeToCompletionAPIView, RetentionRiskAPIView, KnowledgeGapsAPIView, LearningClustersAPIView
    # Note: PredictiveStreamingAPIView and AIInteractionAPIView not yet implemented
    # path('api/predictive/streaming/', PredictiveStreamingAPIView.as_view()),
    # path('api/predictive/streaming/<str:stream_type>/', PredictiveStreamingAPIView.as_view()),
    
    # Note: AIInteractionAPIView not yet implemented
    # path('api/ai/interaction/', AIInteractionAPIView.as_view()),
    # path('api/ai/agents/', AIInteractionAPIView.as_view()),
)
from .views_advanced_analytics import (
    SophisticatedStatisticalAnalysisAPIView, EnhancedMLInsightsAPIView,
    AdvancedPatternRecognitionAPIView, IntegratedPersonalizedRecommendationsAPIView,
    AdvancedAnalyticsDashboardAPIView, advanced_analytics_dashboard
)
from .views_realtime import (
    RealTimeDashboardAPIView, PredictiveAnalyticsAPIView,
    PerformanceAlertsAPIView, TrendAnalysisAPIView
)
from rest_framework.routers import DefaultRouter
from .views import (
    ProgressSnapshotViewSet, LearningAnalyticsViewSet, AchievementViewSet,
    UserProgressMetricViewSet, ProgressGoalViewSet, ProgressNotificationViewSet,
    ProgressSummaryAPIView, ProgressAnalyticsAPIView, CreateProgressSnapshotAPIView,
    TrackUserProgressAPIView
)
from .views_predictive import (
    MLPredictionsAPIView, HistoricalTrendsAPIView, AdaptivePredictionsAPIView,
    ConfidenceCalculationsAPIView, ComprehensivePredictiveAnalyticsAPIView,
    predictive_dashboard_data,
    # New Predictive Learning Models APIs
    LearningVelocityAPIView, EngagementPatternsAPIView, SuccessProbabilityAPIView,
    TimeToCompletionAPIView, RetentionRiskAPIView, KnowledgeGapsAPIView, LearningClustersAPIView
)
from .views_advanced_analytics import (
    SophisticatedStatisticalAnalysisAPIView, EnhancedMLInsightsAPIView,
    AdvancedPatternRecognitionAPIView, IntegratedPersonalizedRecommendationsAPIView,
    AdvancedAnalyticsDashboardAPIView, advanced_analytics_dashboard
)
from .views_realtime import (
    RealTimeDashboardAPIView, PredictiveAnalyticsAPIView,
    PerformanceAlertsAPIView, TrendAnalysisAPIView
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
    
    # Predictive Analytics Endpoints
    path('api/v1/predict/ml/', MLPredictionsAPIView.as_view(), name='ml-predictions'),
    path('api/v1/predict/trends/', HistoricalTrendsAPIView.as_view(), name='historical-trends'),
    path('api/v1/predict/adaptive/', AdaptivePredictionsAPIView.as_view(), name='adaptive-predictions'),
    path('api/v1/predict/confidence/', ConfidenceCalculationsAPIView.as_view(), name='confidence-calculations'),
    path('api/v1/predict/comprehensive/', ComprehensivePredictiveAnalyticsAPIView.as_view(), name='comprehensive-predictive'),
    path('api/v1/predict/dashboard/', predictive_dashboard_data, name='predictive-dashboard'),
    
    # New Predictive Learning Models Endpoints
    path('api/v1/predict/velocity/', LearningVelocityAPIView.as_view(), name='learning-velocity'),
    path('api/v1/predict/engagement/', EngagementPatternsAPIView.as_view(), name='engagement-patterns'),
    path('api/v1/predict/success-probability/', SuccessProbabilityAPIView.as_view(), name='success-probability'),
    path('api/v1/predict/time-to-completion/', TimeToCompletionAPIView.as_view(), name='time-to-completion'),
    path('api/v1/predict/retention-risk/', RetentionRiskAPIView.as_view(), name='retention-risk'),
    path('api/v1/predict/knowledge-gaps/', KnowledgeGapsAPIView.as_view(), name='knowledge-gaps'),
    path('api/v1/predict/learning-clusters/', LearningClustersAPIView.as_view(), name='learning-clusters'),
    
    # Advanced Analytics Endpoints
    path('api/v1/advanced/statistical/', SophisticatedStatisticalAnalysisAPIView.as_view(), name='sophisticated-statistical'),
    path('api/v1/advanced/ml-insights/', EnhancedMLInsightsAPIView.as_view(), name='enhanced-ml-insights'),
    path('api/v1/advanced/pattern-recognition/', AdvancedPatternRecognitionAPIView.as_view(), name='advanced-pattern-recognition'),
    path('api/v1/advanced/personalized-recommendations/', IntegratedPersonalizedRecommendationsAPIView.as_view(), name='integrated-personalized-recommendations'),
    path('api/v1/advanced/dashboard/', AdvancedAnalyticsDashboardAPIView.as_view(), name='advanced-analytics-dashboard'),
    path('api/v1/advanced/', advanced_analytics_dashboard, name='advanced-analytics'),
    
    # Alternative endpoints without API version
    path('api/predict/ml/', MLPredictionsAPIView.as_view(), name='ml-predictions-no-version'),
    path('api/predict/trends/', HistoricalTrendsAPIView.as_view(), name='historical-trends-no-version'),
    path('api/predict/adaptive/', AdaptivePredictionsAPIView.as_view(), name='adaptive-predictions-no-version'),
    path('api/predict/confidence/', ConfidenceCalculationsAPIView.as_view(), name='confidence-calculations-no-version'),
    path('api/predict/comprehensive/', ComprehensivePredictiveAnalyticsAPIView.as_view(), name='comprehensive-predictive-no-version'),
    path('api/predict/dashboard/', predictive_dashboard_data, name='predictive-dashboard-no-version'),
    
    # Alternative new predictive learning models endpoints
    path('api/predict/velocity/', LearningVelocityAPIView.as_view(), name='learning-velocity-no-version'),
    path('api/predict/engagement/', EngagementPatternsAPIView.as_view(), name='engagement-patterns-no-version'),
    path('api/predict/success-probability/', SuccessProbabilityAPIView.as_view(), name='success-probability-no-version'),
    path('api/predict/time-to-completion/', TimeToCompletionAPIView.as_view(), name='time-to-completion-no-version'),
    path('api/predict/retention-risk/', RetentionRiskAPIView.as_view(), name='retention-risk-no-version'),
    path('api/predict/knowledge-gaps/', KnowledgeGapsAPIView.as_view(), name='knowledge-gaps-no-version'),
    path('api/predict/learning-clusters/', LearningClustersAPIView.as_view(), name='learning-clusters-no-version'),
    
    # Alternative advanced analytics endpoints without API version
    path('api/advanced/statistical/', SophisticatedStatisticalAnalysisAPIView.as_view(), name='sophisticated-statistical-no-version'),
    path('api/advanced/ml-insights/', EnhancedMLInsightsAPIView.as_view(), name='enhanced-ml-insights-no-version'),
    path('api/advanced/pattern-recognition/', AdvancedPatternRecognitionAPIView.as_view(), name='advanced-pattern-recognition-no-version'),
    path('api/advanced/personalized-recommendations/', IntegratedPersonalizedRecommendationsAPIView.as_view(), name='integrated-personalized-recommendations-no-version'),
    path('api/advanced/dashboard/', AdvancedAnalyticsDashboardAPIView.as_view(), name='advanced-analytics-dashboard-no-version'),
    path('api/advanced/', advanced_analytics_dashboard, name='advanced-analytics-no-version'),
    
    # Real-time Progress API Endpoints (MISSING ENDPOINTS IMPLEMENTATION)
    path('api/progress/real-time-dashboard/', RealTimeDashboardAPIView.as_view(), name='real-time-dashboard'),
    path('api/progress/predictive-analytics/', PredictiveAnalyticsAPIView.as_view(), name='predictive-analytics'),
    path('api/progress/performance-alerts/', PerformanceAlertsAPIView.as_view(), name='performance-alerts'),
    path('api/progress/trend-analysis/', TrendAnalysisAPIView.as_view(), name='trend-analysis'),
    
    # Alternative real-time endpoints with API version
    path('api/v1/progress/real-time-dashboard/', RealTimeDashboardAPIView.as_view(), name='real-time-dashboard-v1'),
    path('api/v1/progress/predictive-analytics/', PredictiveAnalyticsAPIView.as_view(), name='predictive-analytics-v1'),
    path('api/v1/progress/performance-alerts/', PerformanceAlertsAPIView.as_view(), name='performance-alerts-v1'),
    path('api/v1/progress/trend-analysis/', TrendAnalysisAPIView.as_view(), name='trend-analysis-v1'),
]