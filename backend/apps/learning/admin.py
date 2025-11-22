"""
Django admin configuration for the Learning app.
Admin interface for managing learning content, paths, modules, and assessments.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    LearningPath, Module, Lesson, Assessment, Question,
    UserProgress, LearningPathEnrollment, AssessmentAttempt
)


@admin.register(LearningPath)
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


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Admin interface for Module model."""
    
    list_display = (
        'title', 'learning_path', 'order', 'difficulty_level',
        'estimated_duration', 'is_published', 'created_by'
    )
    
    list_filter = (
        'learning_path', 'difficulty_level', 'is_published',
        'created_at', 'jac_concepts'
    )
    
    search_fields = ('title', 'description', 'learning_path__name')
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description', 'learning_path', 'order')
        }),
        ('Learning Content', {
            'fields': (
                'difficulty_level', 'estimated_duration',
                'prerequisites', 'jac_concepts', 'tags'
            )
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url', 'resources')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('learning_path', 'created_by')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter foreign key relationships."""
        if db_field.name == "learning_path" and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(created_by=request.user)
        elif db_field.name == "created_by" and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(id=request.user.id)
            kwargs["initial"] = request.user.id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Lesson)
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


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    """Admin interface for Assessment model."""
    
    list_display = (
        'title', 'assessment_type', 'difficulty_level',
        'time_limit', 'max_attempts', 'is_published'
    )
    
    list_filter = (
        'assessment_type', 'difficulty_level', 'is_published', 'created_at'
    )
    
    search_fields = ('title', 'description')
    
    readonly_fields = ('created_at', 'updated_at', 'id', 'average_score')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'title', 'description')
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
            'fields': ('average_score', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ('questions',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Question model."""
    
    list_display = (
        'question_text', 'question_type', 'difficulty_level',
        'points', 'assessment'
    )
    
    list_filter = (
        'question_type', 'difficulty_level', 'created_at'
    )
    
    search_fields = ('question_text', 'assessment__title')
    
    readonly_fields = ('created_at', 'updated_at', 'id')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'assessment', 'question_text')
        }),
        ('Question Details', {
            'fields': (
                'question_type', 'difficulty_level', 'points',
                'explanation', 'hints'
            )
        }),
        ('Question Content', {
            'fields': (
                'question_options', 'correct_answer',
                'code_template', 'test_cases'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    filter_horizontal = ('question_options',)
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('assessment')


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin interface for UserProgress model."""
    
    list_display = (
        'user', 'module', 'status', 'completion_percentage',
        'time_spent', 'last_accessed', 'completed_at'
    )
    
    list_filter = (
        'status', 'completion_percentage', 'last_accessed', 'completed_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'module__title'
    )
    
    readonly_fields = (
        'id', 'created_at', 'updated_at', 'last_accessed', 'completed_at'
    )
    
    fieldsets = (
        ('User & Module', {
            'fields': ('user', 'module')
        }),
        ('Progress', {
            'fields': (
                'status', 'completion_percentage', 'score',
                'time_spent', 'attempts_count'
            )
        }),
        ('Timestamps', {
            'fields': (
                'started_at', 'last_accessed', 'completed_at',
                'created_at', 'updated_at'
            )
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'module')


@admin.register(LearningPathEnrollment)
class LearningPathEnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for LearningPathEnrollment model."""
    
    list_display = (
        'user', 'learning_path', 'status', 'progress_percentage',
        'enrolled_at', 'completed_at'
    )
    
    list_filter = (
        'status', 'progress_percentage', 'enrolled_at', 'completed_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'learning_path__name'
    )
    
    readonly_fields = (
        'id', 'enrolled_at', 'completed_at', 'created_at', 'updated_at'
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'learning_path')


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    """Admin interface for AssessmentAttempt model."""
    
    list_display = (
        'user', 'assessment', 'status', 'score', 'time_taken',
        'attempted_at'
    )
    
    list_filter = (
        'status', 'score', 'attempted_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'assessment__title'
    )
    
    readonly_fields = (
        'id', 'attempted_at', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('User & Assessment', {
            'fields': ('user', 'assessment', 'attempt_number')
        }),
        ('Attempt Details', {
            'fields': (
                'status', 'score', 'time_taken',
                'started_at', 'completed_at'
            )
        }),
        ('Response Data', {
            'fields': ('responses', 'feedback'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('attempted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with related fields."""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'assessment')


# Custom admin site configuration
admin.site.site_header = "JAC Learning Platform Admin"
admin.site.site_title = "JAC Admin"
admin.site.index_title = "Content Management Dashboard"