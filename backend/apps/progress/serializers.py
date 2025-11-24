"""
Progress App Serializers - JAC Learning Platform

This module provides DRF serializers for the progress app models,
handling data validation and transformation for API endpoints.

Serializers:
- ProgressSnapshotSerializer: User progress snapshot data
- LearningAnalyticsSerializer: Learning analytics data
- AchievementSerializer: Achievement definitions and user achievements
- UserProgressMetricSerializer: Individual user metrics
- ProgressGoalSerializer: User learning goals
- ProgressNotificationSerializer: Progress notifications
- ProgressSummarySerializer: Comprehensive progress summary
- ProgressAnalyticsSerializer: Advanced analytics data

Author: MiniMax Agent
Created: 2025-11-25
"""

from rest_framework import serializers
from django.utils import timezone
from django.db.models import Avg, Count, Q
from .models import (
    ProgressSnapshot, LearningAnalytics, Achievement, UserProgressMetric,
    ProgressGoal, ProgressNotification
)
from apps.learning.models import LearningPath, Module
from apps.assessments.models import Assessment


class ProgressSnapshotSerializer(serializers.ModelSerializer):
    """
    Serializer for user progress snapshots
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_title = serializers.CharField(source='learning_path.title', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = ProgressSnapshot
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_title',
            'module', 'module_title', 'completion_percentage', 'total_modules',
            'completed_modules', 'total_assessments', 'completed_assessments',
            'average_score', 'best_score', 'total_time_spent', 'days_active',
            'session_count', 'streak_days', 'snapshot_date', 'created_at',
            'is_milestone'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_completion_percentage(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Completion percentage must be between 0 and 100")
        return value
    
    def validate_average_score(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Average score must be between 0 and 100")
        return value


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for learning analytics data
    """
    user_username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    learning_path_title = serializers.CharField(source='learning_path.title', read_only=True, allow_null=True)
    period_duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningAnalytics
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_title',
            'period_start', 'period_end', 'period_duration_days', 'total_activities',
            'completion_rate', 'accuracy_rate', 'efficiency_score', 'engagement_level',
            'consistency_score', 'motivation_score', 'learning_velocity',
            'skill_progression_rate', 'performance_trend', 'completion_prediction_days',
            'confidence_level', 'key_insights', 'recommendations', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_period_duration_days(self, obj):
        if obj.period_start and obj.period_end:
            return (obj.period_end - obj.period_start).days
        return 0
    
    def validate_completion_rate(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Completion rate must be between 0 and 100")
        return value
    
    def validate_accuracy_rate(self, value):
        if not 0 <= value <= 100:
            raise serializers.ValidationError("Accuracy rate must be between 0 and 100")
        return value
    
    def validate_confidence_level(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Confidence level must be between 0 and 1")
        return value


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for achievement definitions
    """
    user_achievements_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'category', 'difficulty', 'criteria_type',
            'criteria_value', 'criteria_operator', 'points', 'badge_icon',
            'is_active', 'created_at', 'updated_at', 'user_achievements_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_achievements_count(self, obj):
        # This would be implemented when we have UserAchievement model
        return 0


class UserProgressMetricSerializer(serializers.ModelSerializer):
    """
    Serializer for individual user progress metrics
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_title = serializers.CharField(source='learning_path.title', read_only=True, allow_null=True)
    progress_percentage = serializers.ReadOnlyField()
    is_improving = serializers.ReadOnlyField()
    
    class Meta:
        model = UserProgressMetric
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_title',
            'metric_type', 'current_value', 'target_value', 'previous_value',
            'progress_percentage', 'trend_direction', 'trend_strength',
            'value_history', 'last_updated', 'created_at', 'is_improving'
        ]
        read_only_fields = ['id', 'last_updated', 'created_at', 'progress_percentage', 'is_improving']
    
    def validate_current_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Current value cannot be negative")
        return value
    
    def validate_target_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Target value must be positive")
        return value
    
    def validate_trend_strength(self, value):
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Trend strength must be between 0 and 1")
        return value


class ProgressGoalSerializer(serializers.ModelSerializer):
    """
    Serializer for user progress goals
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_title = serializers.CharField(source='learning_path.title', read_only=True, allow_null=True)
    progress_percentage = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    
    class Meta:
        model = ProgressGoal
        fields = [
            'id', 'user', 'user_username', 'title', 'description', 'goal_type',
            'target_value', 'current_value', 'progress_percentage', 'start_date',
            'target_date', 'completed_date', 'status', 'status_display',
            'priority', 'priority_display', 'learning_path', 'learning_path_title',
            'motivation_text', 'completion_notes', 'is_overdue', 'days_remaining',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'progress_percentage', 'is_overdue']
    
    def get_days_remaining(self, obj):
        if obj.status == 'completed' or not obj.target_date:
            return 0
        delta = obj.target_date - timezone.now().date()
        return max(0, delta.days)
    
    def validate_target_value(self, value):
        if value <= 0:
            raise serializers.ValidationError("Target value must be positive")
        return value
    
    def validate_current_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Current value cannot be negative")
        return value
    
    def validate(self, data):
        if data['target_date'] <= data['start_date']:
            raise serializers.ValidationError("Target date must be after start date")
        return data


class ProgressNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for progress notifications
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    age_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = ProgressNotification
        fields = [
            'id', 'user', 'user_username', 'notification_type', 'notification_type_display',
            'priority', 'priority_display', 'title', 'message', 'data',
            'is_read', 'is_sent', 'read_at', 'sent_at', 'age_hours',
            'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'created_at', 'age_hours']
    
    def get_age_hours(self, obj):
        delta = timezone.now() - obj.created_at
        return int(delta.total_seconds() / 3600)


class ProgressSummarySerializer(serializers.Serializer):
    """
    Comprehensive progress summary serializer
    """
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    
    # Overall Progress
    overall_completion = serializers.FloatField()
    total_modules = serializers.IntegerField()
    completed_modules = serializers.IntegerField()
    current_level = serializers.CharField()
    next_milestone = serializers.CharField()
    
    # Performance Metrics
    average_score = serializers.FloatField()
    best_score = serializers.FloatField()
    total_time_spent = serializers.DurationField()
    
    # Engagement
    days_active = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    
    # Recent Activity
    recent_snapshots = ProgressSnapshotSerializer(many=True, read_only=True)
    
    # Goals
    active_goals = serializers.IntegerField()
    completed_goals = serializers.IntegerField()
    overdue_goals = serializers.IntegerField()
    
    # Achievements
    total_achievements = serializers.IntegerField()
    recent_achievements = serializers.ListField(child=serializers.CharField())
    
    # Analytics Summary
    performance_trend = serializers.CharField()
    engagement_level = serializers.FloatField()
    learning_velocity = serializers.FloatField()


class ProgressAnalyticsSerializer(serializers.Serializer):
    """
    Advanced progress analytics serializer
    """
    analytics_id = serializers.CharField()
    user_id = serializers.IntegerField()
    learning_path_id = serializers.IntegerField(allow_null=True)
    
    # Time Period
    time_period_days = serializers.IntegerField()
    analytics_type = serializers.CharField()
    generation_date = serializers.DateTimeField()
    
    # Summary Metrics
    summary_metrics = serializers.DictField()
    
    # Detailed Analytics
    performance_analytics = serializers.DictField()
    engagement_analytics = serializers.DictField()
    learning_analytics = serializers.DictField()
    
    # Analysis
    comparative_analysis = serializers.DictField()
    trends = serializers.DictField()
    
    # Insights and Recommendations
    insights = serializers.ListField(child=serializers.CharField())
    recommendations = serializers.ListField(child=serializers.CharField())
    alerts = serializers.ListField(child=serializers.CharField())


class ProgressSnapshotCreateSerializer(serializers.Serializer):
    """
    Serializer for creating progress snapshots
    """
    learning_path_id = serializers.IntegerField(required=False, allow_null=True)
    module_id = serializers.IntegerField(required=False, allow_null=True)
    force_snapshot = serializers.BooleanField(default=False)
    
    def validate_learning_path_id(self, value):
        if value:
            try:
                LearningPath.objects.get(id=value)
            except LearningPath.DoesNotExist:
                raise serializers.ValidationError("Learning path not found")
        return value
    
    def validate_module_id(self, value):
        if value:
            try:
                Module.objects.get(id=value)
            except Module.DoesNotExist:
                raise serializers.ValidationError("Module not found")
        return value


class LearningAnalyticsCreateSerializer(serializers.Serializer):
    """
    Serializer for creating learning analytics
    """
    learning_path_id = serializers.IntegerField(required=False, allow_null=True)
    time_period_days = serializers.IntegerField(default=30, min_value=1, max_value=365)
    analytics_type = serializers.ChoiceField(
        choices=['basic', 'performance', 'engagement', 'comprehensive'],
        default='comprehensive'
    )
    
    def validate_learning_path_id(self, value):
        if value:
            try:
                LearningPath.objects.get(id=value)
            except LearningPath.DoesNotExist:
                raise serializers.ValidationError("Learning path not found")
        return value


class ProgressGoalCreateSerializer(serializers.Serializer):
    """
    Serializer for creating progress goals
    """
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    goal_type = serializers.CharField(max_length=50)
    target_value = serializers.IntegerField(min_value=1)
    start_date = serializers.DateField()
    target_date = serializers.DateField()
    priority = serializers.ChoiceField(
        choices=['low', 'medium', 'high', 'urgent'],
        default='medium'
    )
    learning_path_id = serializers.IntegerField(required=False, allow_null=True)
    motivation_text = serializers.CharField(required=False, allow_blank=True)
    
    def validate_learning_path_id(self, value):
        if value:
            try:
                LearningPath.objects.get(id=value)
            except LearningPath.DoesNotExist:
                raise serializers.ValidationError("Learning path not found")
        return value
    
    def validate(self, data):
        if data['target_date'] <= data['start_date']:
            raise serializers.ValidationError("Target date must be after start date")
        return data