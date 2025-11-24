"""
Search models for JAC Learning Platform
Handles search functionality across all content types
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class SearchQuery(models.Model):
    """
    Tracks user search queries and provides search suggestions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=255, help_text='Search query text')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_queries', null=True, blank=True)
    
    # Search metadata
    results_count = models.PositiveIntegerField(default=0, help_text='Number of results found')
    clicked_result = models.CharField(max_length=255, null=True, blank=True, help_text='URL or identifier of clicked result')
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'search_queries'
        verbose_name = 'Search Query'
        verbose_name_plural = 'Search Queries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Search: {self.query}"


class SearchResult(models.Model):
    """
    Represents a search result item
    """
    CONTENT_TYPE_CHOICES = [
        ('learning_path', 'Learning Path'),
        ('module', 'Module'),
        ('lesson', 'Lesson'),
        ('assessment', 'Assessment'),
        ('knowledge_node', 'Knowledge Node'),
        ('content', 'Content'),
        ('user', 'User'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=255, help_text='Associated search query')
    
    # Content identification
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_id = models.CharField(max_length=255, help_text='ID of the content item')
    title = models.CharField(max_length=255, help_text='Title of the content')
    description = models.TextField(blank=True, help_text='Description or summary')
    
    # Content metadata
    url = models.CharField(max_length=500, help_text='URL to access the content')
    tags = models.JSONField(default=list, help_text='Tags associated with content')
    
    # Search relevance
    relevance_score = models.FloatField(default=0.0, help_text='Relevance score (0-1)')
    popularity_score = models.FloatField(default=0.0, help_text='Popularity score (0-1)')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'search_results'
        verbose_name = 'Search Result'
        verbose_name_plural = 'Search Results'
        ordering = ['-relevance_score', '-popularity_score']
        indexes = [
            models.Index(fields=['content_type']),
            models.Index(fields=['query']),
        ]
    
    def __str__(self):
        return f"{self.content_type}: {self.title}"