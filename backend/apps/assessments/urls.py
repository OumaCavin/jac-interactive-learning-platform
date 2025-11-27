# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Assessment URLs for Django REST Framework

URL patterns for assessment management, question handling, and statistics
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AssessmentQuestionViewSet, AssessmentAttemptViewSet, AssessmentStatsAPIView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'questions', AssessmentQuestionViewSet, basename='assessmentquestion')
router.register(r'attempts', AssessmentAttemptViewSet, basename='assessmentattempt')
router.register(r'stats', AssessmentStatsAPIView, basename='assessmentstats',)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # Additional assessment-specific endpoints can be added here
    # Example: path('stats/overview/', views.OverviewStatsAPIView.as_view(), name='assessment-overview-stats'),
]