"""
Content admin interface for JAC Learning Platform
"""

from django.contrib import admin
from .models import Content, ContentRecommendation, ContentAnalytics


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """
    Admin interface for Content model
    """
    list_display = [
        'title', 'content_type', 'difficulty_level', 'topic', 
        'quality_rating', 'is_published', 'created_by', 'created_at'
    ]
    list_filter = [
        'content_type', 'difficulty_level', 'is_published', 
        'is_featured', 'created_at'
    ]
    search_fields = ['title', 'description', 'topic', 'tags']
    readonly_fields = ['content_id', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'content_type', 'difficulty_level')
        }),
        ('Content Data', {
            'fields': ('content_data', 'estimated_duration', 'tags', 'topic')
        }),
        ('Quality & Metadata', {
            'fields': ('quality_rating', 'learning_path')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'created_by')
        }),
        ('System', {
            'fields': ('content_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by if not already set"""
        if not change:  # Only for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContentRecommendation)
class ContentRecommendationAdmin(admin.ModelAdmin):
    """
    Admin interface for ContentRecommendation model
    """
    list_display = [
        'user', 'content', 'recommendation_type', 'match_score', 
        'is_viewed', 'is_dismissed', 'created_at'
    ]
    list_filter = [
        'recommendation_type', 'is_viewed', 'is_dismissed', 'created_at'
    ]
    search_fields = ['user__username', 'content__title']
    readonly_fields = ['recommendation_id', 'created_at', 'expires_at']
    ordering = ['-match_score', '-created_at']


@admin.register(ContentAnalytics)
class ContentAnalyticsAdmin(admin.ModelAdmin):
    """
    Admin interface for ContentAnalytics model
    """
    list_display = [
        'content', 'total_views', 'unique_viewers', 'average_completion_rate',
        'average_rating', 'bounce_rate', 'updated_at'
    ]
    list_filter = ['updated_at']
    readonly_fields = [
        'content', 'total_views', 'unique_viewers', 'total_time_spent',
        'average_completion_rate', 'total_clicks', 'total_shares',
        'total_ratings', 'average_rating', 'bounce_rate', 'return_visit_rate',
        'created_at', 'updated_at'
    ]
    ordering = ['-total_views']
