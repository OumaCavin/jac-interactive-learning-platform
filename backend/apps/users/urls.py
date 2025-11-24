"""
URL patterns for the users app.
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # User profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/detailed/', views.UserProfileDetailView.as_view(), name='profile-detail'),
    
    # User dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),
    
    # Activity
    path('activity/', views.update_activity, name='update-activity'),
    
    # Admin endpoints
    path('stats/', views.user_stats, name='user-stats'),
    path('list/', views.UserListView.as_view(), name='user-list'),
    path('search/', views.UserSearchView.as_view(), name='user-search'),
]