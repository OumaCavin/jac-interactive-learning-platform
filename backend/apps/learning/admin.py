# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Django admin configuration for the Learning app.
Admin interface for managing learning content, paths, modules, and assessments.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    LearningPath, Module, Lesson,
    UserLearningPath, UserModuleProgress, PathRating, LearningRecommendation,
    Assessment, AssessmentQuestion, AssessmentAttempt,
    UserDifficultyProfile, AdaptiveChallenge, UserChallengeAttempt, SpacedRepetitionSession
)

from config.custom_admin import custom_admin_site


@admin.register(LearningPath, site=custom_admin_site)
class LearningPathAdmin(admin.ModelAdmin):
    """Admin interface for LearningPath model."""
    
    list_display = (
        'name', 'difficulty_level', 'estimated_duration', 
        'is_published', 'is_featured', 'created_by', 'created_at'
    )
    
    list_filter = (
        'difficulty_level', 'is_published', 'is_featured', 
        'created_at', 'tags'
    )
    
    search_fields = ('name', 'description', 'created_by__username')
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'description', 'cover_image')
        }),
        ('Learning Settings', {
            'fields': (
                'difficulty_level', 'estimated_duration', 
                'prerequisites', 'tags'
            )
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('created_by')
    
    def get_readonly_fields(self, request, obj=None):
        """Make some fields readonly for non-superusers."""
        readonly = list(self.readonly_fields)
        if not request.user.is_superuser:
            readonly.extend(['created_by', 'is_published', 'is_featured'])
        return readonly
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter created_by to current user if not superuser."""
        if db_field.name == "created_by" and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(id=request.user.id)
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Module, site=custom_admin_site)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""
    
    list_display = (
        'title', 'learning_path', 'order', 'difficulty_rating',
        'duration_minutes', 'is_published'
    )
    
    list_filter = (
        'learning_path', 'difficulty_rating', 'is_published',
        'created_at', 'content_type'
    )
    
    search_fields = ('title', 'description', 'learning_path__name')
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description', 'learning_path', 'order')
        }),
        ('Content', {
            'fields': ('content', 'content_type')
        }),
        ('Structure', {
            'fields': (
                'difficulty_rating', 'duration_minutes', 'jac_concepts',
                'code_examples'
            )
        }),
        ('Interactive Elements', {
            'fields': ('has_quiz', 'has_coding_exercise', 'has_visual_demo')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('learning_path')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key relationships."""
        if db_field.name == "learning_path" and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lesson, site=custom_admin_site)
class LessonAdmin(admin.ModelAdmin):
    """Admin interface for Lesson model."""
    
    list_display = (
        'title', 'module', 'lesson_type', 'order',
        'estimated_duration', 'is_published'
    )
    
    list_filter = (
        'module', 'lesson_type', 'is_published', 'created_at'
    )
    
    search_fields = ('title', 'content', 'module__title')
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'module', 'order')
        }),
        ('Content', {
            'fields': ('lesson_type', 'content', 'code_example')
        }),
        ('Interactive Elements', {
            'fields': ('quiz_questions', 'interactive_demo')
        }),
        ('Media', {
            'fields': ('video_url', 'audio_url', 'resources')
        }),
        ('Publishing', {
            'fields': ('is_published', 'estimated_duration')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('module', 'module__learning_path')


@admin.register(Assessment, site=custom_admin_site)
class AssessmentAdmin(admin.ModelAdmin):
    """Admin interface for Assessment model."""
    
    list_display = (
        'title', 'assessment_type', 'difficulty_level',
        'time_limit', 'max_attempts', 'is_published', 'average_score'
    )
    
    list_filter = (
        'assessment_type', 'difficulty_level', 'is_published', 'created_at'
    )
    
    search_fields = ('title', 'description', 'module__title')
    
    readonly_fields = ('created_at', 'updated_at', 'id', 'average_score', 'question_count')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description', 'module')
        }),
        ('Assessment Settings', {
            'fields': (
                'assessment_type', 'difficulty_level',
                'time_limit', 'max_attempts', 'passing_score'
            )
        }),
        ('Questions', {
            'fields': ('questions',)
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Statistics', {
            'fields': ('average_score', 'question_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Note: Questions are managed through AssessmentQuestion model, not directly
    # filter_horizontal = ('assessment_questions',)  # Commented out as related field not suitable for filter_horizontal
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('module')
    
    def question_count(self, obj):
        """Display question count."""
        return obj.question_count
    question_count.short_description = 'Questions'



@admin.register(UserModuleProgress, site=custom_admin_site)
class UserModuleProgressAdmin(admin.ModelAdmin):
    """Admin interface for UserModuleProgress model."""
    
    list_display = (
        'user', 'module', 'status', 'progress_percentage',
        'time_spent', 'overall_score', 'last_activity_at'
    )
    
    list_filter = (
        'status', 'progress_percentage', 'last_activity_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'module__title'
    )
    
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'last_activity_at'
    )
    
    fieldsets = (
        ('User & Module', {
            'fields': ('user', 'module')
        }),
        ('Progress', {
            'fields': (
                'status', 'progress_percentage', 'time_spent',
                'quiz_score', 'coding_score', 'overall_score'
            )
        }),
        ('Feedback', {
            'fields': ('user_notes', 'feedback')
        }),
        ('Timestamps', {
            'fields': (
                'started_at', 'completed_at', 'last_activity_at',
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'module')


@admin.register(UserLearningPath, site=custom_admin_site)
class UserLearningPathAdmin(admin.ModelAdmin):
    """Admin interface for UserLearningPath model."""
    
    list_display = (
        'user', 'learning_path', 'status', 'progress_percentage',
        'current_module_order', 'last_activity_at'
    )
    
    list_filter = (
        'status', 'progress_percentage', 'last_activity_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'learning_path__name'
    )
    
    readonly_fields = (
        'id', 'last_activity_at', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('User & Learning Path', {
            'fields': ('user', 'learning_path')
        }),
        ('Progress', {
            'fields': (
                'status', 'progress_percentage', 'current_module_order'
            )
        }),
        ('Timestamps', {
            'fields': (
                'started_at', 'completed_at', 'last_activity_at',
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'learning_path')


# Custom admin site configuration
admin.site.site_header = "JAC Learning Platform Admin"
admin.site.site_title = "JAC Admin"
admin.site.index_title = "Content Management Dashboard"