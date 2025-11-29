# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Django admin configuration for the Users app.
"""

from django.contrib import admin
from config.custom_admin import custom_admin_site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User, site=custom_admin_site)
class UserAdmin(BaseUserAdmin):
    """Admin interface for the custom User model."""
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'level', 'total_points', 'learning_style', 
        'is_staff', 'is_active', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 
        'learning_style', 'preferred_difficulty', 'learning_pace',
        'agent_interaction_level', 'preferred_feedback_style',
        'dark_mode', 'notifications_enabled', 'is_verified',
        'date_joined', 'last_login'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    readonly_fields = (
        'id', 'date_joined', 'last_login', 'last_login_at', 
        'created_at', 'updated_at', 'last_activity_at',
        'verification_token'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_image')
        }),
        ('Learning Preferences', {
            'fields': (
                'learning_style', 'preferred_difficulty', 'learning_pace',
                'agent_interaction_level', 'preferred_feedback_style'
            )
        }),
        ('Progress Tracking', {
            'fields': (
                'total_modules_completed', 'total_time_spent',
                'current_streak', 'longest_streak', 'total_points', 'level',
                'current_goal', 'goal_deadline'
            ),
            'classes': ('collapse',)
        }),
        ('Gamification', {
            'fields': ('achievements', 'badges'),
            'classes': ('collapse',)
        }),
        ('Platform Preferences', {
            'fields': (
                'dark_mode', 'notifications_enabled', 
                'email_notifications', 'push_notifications'
            )
        }),
        ('Email Verification', {
            'fields': ('is_verified', 'verification_token', 'verification_token_expires_at')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('date_joined', 'last_login', 'last_login_at', 'created_at', 'updated_at', 'last_activity_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make some fields readonly for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.extend(['is_superuser', 'groups', 'user_permissions'])
        return readonly