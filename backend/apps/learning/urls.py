"""
Learning URLs for Django REST Framework

URL patterns for code execution, learning paths, and progress tracking
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LearningPathViewSet, ModuleViewSet, CodeSubmissionViewSet,
    TestCaseViewSet, UserLearningPathViewSet, UserModuleProgressViewSet,
    PathRatingViewSet, LearningRecommendationViewSet,
    CodeExecutionAPIView, LearningProgressAPIView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'learning-paths', LearningPathViewSet, basename='learningpath')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'code-submissions', CodeSubmissionViewSet, basename='codesubmission')
router.register(r'test-cases', TestCaseViewSet, basename='testcase')
router.register(r'user-learning-paths', UserLearningPathViewSet, basename='userlearningpath')
router.register(r'user-module-progress', UserModuleProgressViewSet, basename='usermoduleprogress')
router.register(r'path-ratings', PathRatingViewSet, basename='pathrating')
router.register(r'recommendations', LearningRecommendationViewSet, basename='learningrecommendation')

urlpatterns = [
    # API endpoints - Note: No 'api/' prefix here since main config provides it
    path('', include(router.urls)),
    
    # Code execution endpoints
    path('code/execute/', CodeExecutionAPIView.as_view(), name='code-execute'),
    path('progress/', LearningProgressAPIView.as_view(), name='learning-progress'),
    
    # Additional learning endpoints can be added here
]