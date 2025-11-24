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
        'learning_level', 'preferred_learning_style', 
        'is_staff', 'is_active', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 
        'preferred_learning_style', 'learning_level', 
        'date_joined', 'last_login'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    readonly_fields = (
        'id', 'date_joined', 'last_login', 'last_activity'
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Learning Preferences', {
            'fields': (
                'preferred_learning_style', 'learning_level'
            )
        }),
        ('Platform Activity', {
            'fields': (
                'total_study_time', 'streak_days', 'last_activity'
            ),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('notifications_enabled',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('date_joined', 'last_login')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make some fields readonly for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.extend(['is_superuser', 'groups', 'user_permissions'])
        return readonly