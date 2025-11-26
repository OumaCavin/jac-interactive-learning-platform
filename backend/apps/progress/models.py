# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Progress App Models - JAC Learning Platform

This module defines the core models for tracking user learning progress,
analytics, and performance metrics in the JAC Interactive Learning Platform.

Models:
- ProgressSnapshot: Point-in-time progress snapshots for analytics
- LearningAnalytics: Aggregated learning analytics data
- Achievement: System-wide achievement definitions
- UserProgressMetric: Individual user progress metrics
- ProgressGoal: User-defined learning goals
- ProgressNotification: Progress-related notifications

Author: Cavin Otieno
Created: 2025-11-25
"""

import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class ProgressSnapshot(models.Model):
    """
    Point-in-time snapshot of user progress for analytics and reporting
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_snapshots')
    
    # Learning Path Context
    learning_path = models.ForeignKey('learning.LearningPath', on_delete=models.CASCADE, related_name='progress_snapshots', null=True, blank=True)
    module = models.ForeignKey('learning.Module', on_delete=models.CASCADE, related_name='progress_snapshots', null=True, blank=True)
    
    # Progress Metrics
    completion_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    total_modules = models.PositiveIntegerField(default=0)
    completed_modules = models.PositiveIntegerField(default=0)
    total_assessments = models.PositiveIntegerField(default=0)
    completed_assessments = models.PositiveIntegerField(default=0)
    
    # Performance Metrics
    average_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    best_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    total_time_spent = models.DurationField(default=timezone.timedelta)
    
    # Engagement Metrics
    days_active = models.PositiveIntegerField(default=0)
    session_count = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    
    # Snapshot Metadata
    snapshot_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    is_milestone = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'progress_snapshot'
        ordering = ['-snapshot_date']
        indexes = [
            models.Index(fields=['user', 'snapshot_date']),
            models.Index(fields=['learning_path', 'snapshot_date']),
            models.Index(fields=['is_milestone']),
        ]
    
    def __str__(self):
        return f"Progress Snapshot - {self.user.username} - {self.snapshot_date.date()}"


class LearningAnalytics(models.Model):
    """
    Aggregated learning analytics data for users and learning paths
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_analytics', null=True, blank=True)
    learning_path = models.ForeignKey('learning.LearningPath', on_delete=models.CASCADE, related_name='learning_analytics', null=True, blank=True)
    
    # Analytics Period
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Performance Analytics
    total_activities = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    accuracy_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    efficiency_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    # Engagement Analytics
    engagement_level = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    consistency_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    motivation_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    # Learning Velocity
    learning_velocity = models.FloatField(default=0.0)  # modules per week
    skill_progression_rate = models.FloatField(default=0.0)
    
    # Trend Data
    performance_trend = models.CharField(max_length=20, choices=[
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
        ('inconsistent', 'Inconsistent'),
    ], default='stable')
    
    # Predictions
    completion_prediction_days = models.PositiveIntegerField(null=True, blank=True)
    confidence_level = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Insights and Recommendations
    key_insights = models.JSONField(default=dict, blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_analytics'
        ordering = ['-period_end']
        indexes = [
            models.Index(fields=['user', 'period_end']),
            models.Index(fields=['learning_path', 'period_end']),
            models.Index(fields=['performance_trend']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else 'All Users'
        path_str = self.learning_path.title if self.learning_path else 'All Paths'
        return f"Analytics - {user_str} - {path_str} - {self.period_end.date()}"


class Achievement(models.Model):
    """
    System-wide achievement definitions for the gamification system
    """
    CATEGORY_CHOICES = [
        ('completion', 'Completion'),
        ('effort', 'Effort'),
        ('skill', 'Skill'),
        ('collaboration', 'Collaboration'),
        ('milestone', 'Milestone'),
        ('special', 'Special'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Achievement Criteria
    criteria_type = models.CharField(max_length=50)  # modules_completed, perfect_scores, consecutive_days, etc.
    criteria_value = models.PositiveIntegerField()
    criteria_operator = models.CharField(max_length=10, choices=[
        ('gte', 'Greater than or equal'),
        ('gt', 'Greater than'),
        ('eq', 'Equal'),
    ], default='gte')
    
    # Gamification
    points = models.PositiveIntegerField(default=10)
    badge_icon = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'achievement'
        ordering = ['category', 'difficulty', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class UserProgressMetric(models.Model):
    """
    Individual user progress metrics and tracking
    """
    METRIC_TYPES = [
        ('completion_rate', 'Completion Rate'),
        ('accuracy_rate', 'Accuracy Rate'),
        ('time_efficiency', 'Time Efficiency'),
        ('engagement_level', 'Engagement Level'),
        ('skill_development', 'Skill Development'),
        ('consistency_score', 'Consistency Score'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_metrics')
    learning_path = models.ForeignKey('learning.LearningPath', on_delete=models.CASCADE, related_name='user_progress_metrics', null=True, blank=True)
    
    metric_type = models.CharField(max_length=30, choices=METRIC_TYPES)
    current_value = models.FloatField(default=0.0)
    target_value = models.FloatField(default=100.0)
    previous_value = models.FloatField(default=0.0)
    
    # Trend Information
    trend_direction = models.CharField(max_length=20, choices=[
        ('increasing', 'Increasing'),
        ('stable', 'Stable'),
        ('decreasing', 'Decreasing'),
        ('volatile', 'Volatile'),
    ], default='stable')
    
    trend_strength = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Historical Data
    value_history = models.JSONField(default=list, blank=True)  # Array of {date, value} tuples
    
    # Timestamps
    last_updated = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_progress_metric'
        unique_together = ['user', 'metric_type', 'learning_path']
        ordering = ['-last_updated']
        indexes = [
            models.Index(fields=['user', 'metric_type']),
            models.Index(fields=['learning_path']),
            models.Index(fields=['trend_direction']),
        ]
    
    def __str__(self):
        learning_path_str = f" - {self.learning_path.title}" if self.learning_path else ""
        return f"{self.user.username} - {self.get_metric_type_display()}{learning_path_str}"


class ProgressGoal(models.Model):
    """
    User-defined learning goals and targets
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('abandoned', 'Abandoned'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Goal Definition
    goal_type = models.CharField(max_length=50)  # complete_modules, achieve_score, spend_time, etc.
    target_value = models.PositiveIntegerField()
    current_value = models.PositiveIntegerField(default=0)
    
    # Time Management
    start_date = models.DateField()
    target_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    # Status and Priority
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Learning Path Context
    learning_path = models.ForeignKey('learning.LearningPath', on_delete=models.CASCADE, related_name='user_goals', null=True, blank=True)
    
    # Notes and Motivation
    motivation_text = models.TextField(blank=True)
    completion_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'progress_goal'
        ordering = ['priority', 'target_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['learning_path']),
            models.Index(fields=['target_date']),
            models.Index(fields=['priority']),
        ]
    
    def clean(self):
        if self.target_date <= self.start_date:
            raise ValidationError("Target date must be after start date")
        
        if self.status == 'completed' and not self.completed_date:
            raise ValidationError("Completed goals must have a completion date")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Goal: {self.title} - {self.user.username}"
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)
    
    @property
    def is_overdue(self):
        if self.status == 'completed':
            return False
        return timezone.now().date() > self.target_date


class ProgressNotification(models.Model):
    """
    Progress-related notifications and alerts
    """
    NOTIFICATION_TYPES = [
        ('milestone_achieved', 'Milestone Achieved'),
        ('goal_completed', 'Goal Completed'),
        ('progress_alert', 'Progress Alert'),
        ('recommendation', 'Recommendation'),
        ('achievement_unlocked', 'Achievement Unlocked'),
        ('streak_warning', 'Streak Warning'),
        ('completion_prediction', 'Completion Prediction'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress_notifications')
    
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)  # Additional notification data
    
    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'progress_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} - {self.user.username} - {self.created_at.date()}"