"""
Assessment admin configuration for Django Admin Interface
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    """
    Admin interface for AssessmentQuestion model
    """
    list_display = [
        'title', 'module', 'question_type', 'difficulty_level', 'points', 
        'is_active', 'version', 'created_at'
    ]
    list_filter = [
        'question_type', 'difficulty_level', 'is_active', 'module', 'created_at'
    ]
    search_fields = ['title', 'question_text']
    readonly_fields = ['question_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('question_id', 'module', 'title', 'question_text')
        }),
        ('Question Details', {
            'fields': ('question_type', 'difficulty_level', 'options')
        }),
        ('Answer', {
            'fields': ('correct_answer', 'explanation', 'points')
        }),
        ('Metadata', {
            'fields': ('tags', 'learning_objectives', 'is_active', 'version')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('module')


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    """
    Admin interface for AssessmentAttempt model
    """
    list_display = [
        'attempt_id', 'user', 'module', 'status', 'score', 
        'is_passed_display', 'started_at', 'completed_at'
    ]
    list_filter = [
        'status', 'module', 'started_at', 'completed_at', 'user'
    ]
    search_fields = ['user__username', 'module__title']
    readonly_fields = [
        'attempt_id', 'started_at', 'completed_at', 'duration_minutes', 
        'is_passed'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('attempt_id', 'user', 'module')
        }),
        ('Status', {
            'fields': ('status', 'started_at', 'completed_at', 'duration_minutes')
        }),
        ('Scoring', {
            'fields': ('score', 'max_score', 'passing_score', 'is_passed')
        }),
        ('Time Limit', {
            'fields': ('time_limit_minutes',)
        }),
        ('Content', {
            'fields': ('answers', 'feedback'),
            'classes': ('collapse',)
        })
    )
    
    def is_passed_display(self, obj):
        """Display pass/fail status with color coding"""
        if obj.is_passed:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ PASSED</span>'
            )
        elif obj.score is not None:
            return format_html(
                '<span style="color: red; font-weight: bold;">✗ FAILED</span>'
            )
        else:
            return format_html(
                '<span style="color: orange;">IN PROGRESS</span>'
            )
    is_passed_display.short_description = 'Pass Status'
    is_passed_display.admin_order_field = 'score'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'module')


@admin.register(UserAssessmentResult)
class UserAssessmentResultAdmin(admin.ModelAdmin):
    """
    Admin interface for UserAssessmentResult model
    """
    list_display = [
        'user', 'module', 'result_type', 'total_attempts', 
        'best_score', 'average_score', 'updated_at'
    ]
    list_filter = [
        'result_type', 'module', 'updated_at', 'user'
    ]
    search_fields = ['user__username', 'module__title']
    readonly_fields = [
        'result_id', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('result_id', 'user', 'module', 'result_type')
        }),
        ('Attempt Statistics', {
            'fields': ('total_attempts', 'best_score', 'average_score', 'average_time_minutes')
        }),
        ('Progress Data', {
            'fields': ('questions_attempted', 'topics_covered', 'learning_objectives_met'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user', 'module')


# Custom admin site header and title
admin.site.site_header = "JAC Learning Platform - Assessments Admin"
admin.site.site_title = "Assessments Admin"
admin.site.index_title = "Assessment Management Dashboard"