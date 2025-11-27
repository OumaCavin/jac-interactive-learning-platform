# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Content models for JAC Learning Platform
Handles learning content management and curation
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

# Import learning models
from apps.learning.models import LearningPath, Module


class Content(models.Model):
    """
    Base content model for all learning materials
    """
    CONTENT_TYPE_CHOICES = [
        ('markdown', 'Markdown'),
        ('html', 'HTML'),
        ('interactive', 'Interactive Content'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('code_tutorial', 'Code Tutorial'),
        ('exercise', 'Exercise'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    # Core identification
    content_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Content details
    content_type = models.CharField(
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES, 
        default='markdown'
    )
    difficulty_level = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        default='beginner'
    )
    
    # Content data
    content_data = models.JSONField(
        default=dict, 
        help_text='Structured content data (markdown, HTML, interactive config, etc.)'
    )
    
    # Metadata
    estimated_duration = models.PositiveIntegerField(
        default=30, 
        help_text='Estimated time in minutes'
    )
    tags = models.JSONField(default=list, help_text='Content tags for categorization')
    topic = models.CharField(max_length=100, blank=True, help_text='Primary topic/category')
    
    # Quality and metadata
    quality_rating = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        help_text='Quality rating from 1.0 to 5.0'
    )
    
    # Optional relationships (using null=True to avoid migration issues)
    learning_path = models.ForeignKey(
        LearningPath, 
        on_delete=models.CASCADE, 
        related_name='content_items',
        null=True, 
        blank=True
    )
    
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='content_items',
        null=True,
        blank=True,
        help_text='Primary module using this content'
    )
    
    # Publishing
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_content'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_content'
        verbose_name = 'Content'
        verbose_name_plural = 'Content'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_published']),
            models.Index(fields=['topic']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"
    
    @property
    def quality_score(self):
        """Calculate quality score (0-1)"""
        if self.quality_rating:
            return self.quality_rating / 5.0
        return 0.5  # Default neutral score


class ContentRecommendation(models.Model):
    """
    Stores content recommendations for users
    """
    RECOMMENDATION_TYPE_CHOICES = [
        ('personalized', 'Personalized'),
        ('based_on_progress', 'Progress-based'),
        ('similar_users', 'Similar users'),
        ('trending', 'Trending'),
    ]
    
    recommendation_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_recommendations')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='recommendations')
    
    # Recommendation details
    recommendation_type = models.CharField(
        max_length=20, 
        choices=RECOMMENDATION_TYPE_CHOICES, 
        default='personalized'
    )
    match_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Match score from 0.0 to 1.0'
    )
    reasoning = models.JSONField(default=dict, help_text='Reasoning behind the recommendation')
    
    # Status
    is_viewed = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'content_recommendations'
        verbose_name = 'Content Recommendation'
        verbose_name_plural = 'Content Recommendations'
        ordering = ['-match_score', '-created_at']
        unique_together = ('user', 'content', 'recommendation_type')
    
    def __str__(self):
        return f"Rec: {self.user.username} - {self.content.title}"


class ContentAnalytics(models.Model):
    """
    Analytics data for content performance
    """
    content = models.OneToOneField(
        Content, 
        on_delete=models.CASCADE, 
        related_name='analytics'
    )
    
    # Usage metrics
    total_views = models.PositiveIntegerField(default=0)
    unique_viewers = models.PositiveIntegerField(default=0)
    total_time_spent = models.DurationField(default=0)
    average_completion_rate = models.FloatField(default=0.0)
    
    # Engagement metrics
    total_clicks = models.PositiveIntegerField(default=0)
    total_shares = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    # Performance metrics
    bounce_rate = models.FloatField(default=0.0)
    return_visit_rate = models.FloatField(default=0.0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content_analytics'
        verbose_name = 'Content Analytics'
        verbose_name_plural = 'Content Analytics'
    
    def __str__(self):
        return f"Analytics: {self.content.title}"