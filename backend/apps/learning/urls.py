# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Learning URLs for Django REST Framework

URL patterns for code execution, learning paths, and progress tracking
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LearningPathViewSet, ModuleViewSet, LessonViewSet, AssessmentViewSet,
    UserLearningPathViewSet, UserModuleProgressViewSet,
    PathRatingViewSet, LearningRecommendationViewSet,
    LearningProgressAPIView,
    # Adaptive Learning Views
    AdaptiveChallengeViewSet, UserDifficultyProfileViewSet, SpacedRepetitionViewSet,
    PerformanceAnalyticsView, ChallengeRecommendationsView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'learning-paths', LearningPathViewSet, basename='learningpath')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'user-learning-paths', UserLearningPathViewSet, basename='userlearningpath')
router.register(r'user-module-progress', UserModuleProgressViewSet, basename='usermoduleprogress')
router.register(r'path-ratings', PathRatingViewSet, basename='pathrating')
router.register(r'recommendations', LearningRecommendationViewSet, basename='learningrecommendation')

# Adaptive Learning ViewSets
router.register(r'adaptive-challenges', AdaptiveChallengeViewSet, basename='adaptivechallenge')
router.register(r'difficulty-profile', UserDifficultyProfileViewSet, basename='difficultyprofile')
router.register(r'spaced-repetition', SpacedRepetitionViewSet, basename='spacedrepetition')

urlpatterns = [
    # API endpoints - Note: No 'api/' prefix here since main config provides it
    path('', include(router.urls)),
    
    # Progress tracking endpoint
    path('progress/', LearningProgressAPIView.as_view(), name='learning-progress'),
    
    # Adaptive Learning API endpoints
    path('performance/analytics/', PerformanceAnalyticsView.as_view(), name='performance-analytics'),
    path('recommendations/challenges/', ChallengeRecommendationsView.as_view(), name='challenge-recommendations'),
    
    # Additional learning endpoints can be added here
]