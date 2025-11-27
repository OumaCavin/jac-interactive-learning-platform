# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
URL routing for the Users app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView, UserLoginView, UserProfileView,
    UserDetailView, LearningSummaryView, UserSettingsView,
    UserStatsView, current_user, logout_view, verify_email, resend_verification_email
)

# Create router for ViewSets
router = DefaultRouter()

urlpatterns = [
    # Authentication URLs
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/logout/', logout_view, name='user-logout'),
    path('auth/me/', current_user, name='current-user'),
    
    # Email verification URLs
    path('verify-email/', verify_email, name='verify-email'),
    path('resend-verification/', resend_verification_email, name='resend-verification'),
    
    # User management URLs
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
    path('learning-summary/', LearningSummaryView.as_view(), name='learning-summary'),
    
    # User detail URLs
    path('<str:user_id>/', UserDetailView.as_view(), name='user-detail'),
    path('<str:user_id>/learning-summary/', LearningSummaryView.as_view(), name='user-learning-summary'),
    
    # Include router URLs
    path('', include(router.urls)),
]