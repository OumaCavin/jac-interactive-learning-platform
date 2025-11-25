"""
URL Configuration for Gamification App

URL patterns for gamification API endpoints including achievements, badges, points, and streaks.

Author: MiniMax Agent
Created: 2025-11-26
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'badges', views.BadgeViewSet, basename='badge')
router.register(r'user-badges', views.UserBadgeViewSet, basename='user-badge')
router.register(r'achievements', views.AchievementViewSet, basename='achievement')
router.register(r'user-achievements', views.UserAchievementViewSet, basename='user-achievement')
router.register(r'user-points', views.UserPointsViewSet, basename='user-points')
router.register(r'user-level', views.UserLevelViewSet, basename='user-level')
router.register(r'learning-streak', views.LearningStreakViewSet, basename='learning-streak')
router.register(r'achievement-progress', views.AchievementProgressViewSet, basename='achievement-progress')

app_name = 'gamification'

urlpatterns = [
    # Core gamification endpoints
    path('overview/', views.GamificationOverviewView.as_view(), name='overview'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('stats/', views.GamificationStatsView.as_view(), name='stats'),
    
    # Integration endpoints
    path('integration/<str:action>/', views.GamificationIntegrationView.as_view(), name='integration'),
    
    # Include router URLs
    path('', include(router.urls)),
]