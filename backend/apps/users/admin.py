"""
Django admin configuration for the Users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for the custom User model."""
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'level', 'total_points', 'learning_style', 
        'is_staff', 'is_active', 'created_at'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'learning_style',
        'preferred_difficulty', 'learning_pace', 'agent_interaction_level',
        'preferred_feedback_style', 'created_at', 'last_activity_at'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'last_login_at', 
        'last_activity_at', 'level', 'experience_level', 'next_level_points'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Profile', {
            'fields': ('bio', 'profile_image')
        }),
        ('Learning Preferences', {
            'fields': (
                'learning_style', 'preferred_difficulty', 'learning_pace'
            )
        }),
        ('Progress Tracking', {
            'fields': (
                'total_modules_completed', 'total_time_spent', 
                'current_streak', 'longest_streak', 'total_points', 'level'
            )
        }),
        ('Gamification', {
            'fields': ('achievements', 'badges', 'current_goal', 'goal_deadline')
        }),
        ('Agent Preferences', {
            'fields': ('agent_interaction_level', 'preferred_feedback_style')
        }),
        ('Platform Preferences', {
            'fields': ('dark_mode', 'notifications_enabled', 'email_notifications', 'push_notifications')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('created_at', 'updated_at', 'last_login_at', 'last_activity_at')
        }),
        ('Computed Values', {
            'fields': ('experience_level', 'next_level_points'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make some fields readonly for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.extend(['is_superuser', 'groups', 'user_permissions'])
        return readonly
    
    def get_exclude(self, request, obj=None):
        """Exclude password field from admin form."""
        exclude = []
        if not request.user.is_superuser:
            exclude.extend(['is_superuser', 'groups', 'user_permissions'])
        return exclude