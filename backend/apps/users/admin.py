"""
Admin interface for the users app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Admin interface for the User model.
    """
    
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'preferred_learning_style', 'learning_level', 'is_active',
        'date_joined', 'last_login'
    )
    
    list_filter = (
        'is_active', 'is_staff', 'is_superuser', 'is_verified',
        'preferred_learning_style', 'learning_level',
        'date_joined', 'last_login'
    )
    
    search_fields = (
        'username', 'first_name', 'last_name', 'email'
    )
    
    readonly_fields = (
        'date_joined', 'last_login', 'last_activity',
        'total_study_time', 'streak_days', 'email_verified'
    )
    
    fieldsets = (
        ('Personal Info', {
            'fields': (
                'username', 'password', 'email',
                'first_name', 'last_name'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'is_verified', 'groups', 'user_permissions'
            )
        }),
        ('Learning Preferences', {
            'fields': (
                'preferred_learning_style', 'learning_level'
            )
        }),
        ('Platform Activity', {
            'fields': (
                'total_study_time', 'streak_days',
                'last_activity', 'notifications_enabled'
            ),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle custom fields.
        """
        super().save_model(request, obj, form, change)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for the UserProfile model.
    """
    
    list_display = (
        'user', 'location', 'modules_completed',
        'lessons_completed', 'total_points', 'created_at'
    )
    
    list_filter = (
        'created_at', 'updated_at', 'location'
    )
    
    search_fields = (
        'user__username', 'user__email', 'location', 'bio'
    )
    
    readonly_fields = (
        'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Info', {
            'fields': ('bio', 'location', 'website')
        }),
        ('Learning', {
            'fields': ('learning_goals', 'current_goals')
        }),
        ('Progress', {
            'fields': (
                'modules_completed', 'lessons_completed',
                'assessments_completed', 'average_lesson_score',
                'total_points'
            )
        }),
        ('Achievements', {
            'fields': ('badges', 'achievements'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )