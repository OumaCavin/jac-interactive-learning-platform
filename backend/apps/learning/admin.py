"""
Django admin configuration for the Learning app.
Admin interface for managing learning content, paths, modules, and assessments.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    LearningPath, Module, UserLearningPath, UserModuleProgress,
    PathRating, LearningRecommendation, CodeSubmission, TestCase,
    CodeExecutionLog, AICodeReview
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





@admin.register(UserModuleProgress)
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


@admin.register(UserLearningPath)
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