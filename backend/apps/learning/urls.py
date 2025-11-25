"""
Learning URLs for Django REST Framework

URL patterns for code execution, learning paths, and progress tracking
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LearningPathViewSet, ModuleViewSet, LessonViewSet, AssessmentViewSet, QuestionViewSet,
    CodeSubmissionViewSet, TestCaseViewSet, UserLearningPathViewSet, UserModuleProgressViewSet,
    PathRatingViewSet, LearningRecommendationViewSet,
    CodeExecutionAPIView, LearningProgressAPIView,
    QuizAPIView, QuizDetailAPIView, AttemptAPIView, StartAttemptAPIView,
    SubmitAttemptAPIView, AttemptDetailAPIView, AssessmentStatsAPIView,
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
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'code-submissions', CodeSubmissionViewSet, basename='codesubmission')
router.register(r'test-cases', TestCaseViewSet, basename='testcase')
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
    
    # Code execution endpoints
    path('code/execute/', CodeExecutionAPIView.as_view(), name='code-execute'),
    path('progress/', LearningProgressAPIView.as_view(), name='learning-progress'),
    
    # Assessment API endpoints
    path('assessment/quizzes/', QuizAPIView.as_view(), name='assessment-quizzes'),
    path('assessment/quizzes/<uuid:quiz_id>/', QuizDetailAPIView.as_view(), name='assessment-quiz-detail'),
    path('assessment/quizzes/<uuid:quiz_id>/start/', StartAttemptAPIView.as_view(), name='assessment-start-attempt'),
    path('assessment/attempts/', AttemptAPIView.as_view(), name='assessment-attempts'),
    path('assessment/attempts/<uuid:attempt_id>/', AttemptDetailAPIView.as_view(), name='assessment-attempt-detail'),
    path('assessment/attempts/<uuid:attempt_id>/submit/', SubmitAttemptAPIView.as_view(), name='assessment-submit-attempt'),
    path('assessment/stats/', AssessmentStatsAPIView.as_view(), name='assessment-stats'),
    
    # Adaptive Learning API endpoints
    path('performance/analytics/', PerformanceAnalyticsView.as_view(), name='performance-analytics'),
    path('recommendations/challenges/', ChallengeRecommendationsView.as_view(), name='challenge-recommendations'),
    
    # Additional learning endpoints can be added here
]