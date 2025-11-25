"""
Gamification Serializers - JAC Learning Platform

DRF serializers for gamification API endpoints.

Author: MiniMax Agent
Created: 2025-11-26
"""

from rest_framework import serializers
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from .models import (
    Badge, UserBadge, Achievement, UserAchievement,
    UserPoints, PointTransaction, UserLevel, LearningStreak,
    LevelRequirement, AchievementProgress
)


class BadgeSerializer(serializers.ModelSerializer):
    """Badge definition serializer"""
    
    class Meta:
        model = Badge
        fields = [
            'id', 'name', 'description', 'icon', 'category', 'difficulty',
            'requirements', 'minimum_points', 'unlock_conditions',
            'rarity', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserBadgeSerializer(serializers.ModelSerializer):
    """User badge ownership serializer"""
    badge = BadgeSerializer(read_only=True)
    earned_days_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = UserBadge
        fields = [
            'id', 'badge', 'earned_at', 'progress_data', 'earned_through',
            'is_verified', 'verified_at', 'earned_days_ago'
        ]
        read_only_fields = ['id', 'earned_at', 'verified_at']
    
    def get_earned_days_ago(self, obj):
        """Calculate days since badge was earned"""
        if obj.earned_at:
            delta = timezone.now() - obj.earned_at
            return delta.days
        return None


class AchievementSerializer(serializers.ModelSerializer):
    """Achievement definition serializer"""
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'description', 'icon', 'category', 'difficulty',
            'criteria_type', 'criteria_value', 'criteria_operator',
            'points_reward', 'badge', 'is_active', 'unlock_order',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserAchievementSerializer(serializers.ModelSerializer):
    """User achievement progress serializer"""
    achievement = AchievementSerializer(read_only=True)
    badge_earned = UserBadgeSerializer(read_only=True)
    progress_percentage_formatted = serializers.SerializerMethodField()
    days_in_progress = serializers.SerializerMethodField()
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'achievement', 'current_progress', 'target_progress',
            'progress_percentage', 'progress_percentage_formatted',
            'is_completed', 'completed_at', 'started_at',
            'points_earned', 'badge_earned', 'progress_history',
            'last_progress_update', 'days_in_progress'
        ]
        read_only_fields = [
            'id', 'started_at', 'last_progress_update', 'progress_percentage'
        ]
    
    def get_progress_percentage_formatted(self, obj):
        """Return progress percentage as formatted string"""
        return f"{obj.progress_percentage:.1f}%"
    
    def get_days_in_progress(self, obj):
        """Calculate days since achievement started"""
        delta = timezone.now() - obj.started_at
        return delta.days


class UserPointsSerializer(serializers.ModelSerializer):
    """User points serializer"""
    points_by_category = serializers.SerializerMethodField()
    recent_transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPoints
        fields = [
            'id', 'total_points', 'available_points', 'lifetime_points',
            'learning_points', 'coding_points', 'assessment_points', 'engagement_points',
            'points_by_category', 'last_earned', 'last_spent',
            'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']
    
    def get_points_by_category(self, obj):
        """Return points breakdown by category"""
        return {
            'learning': obj.learning_points,
            'coding': obj.coding_points,
            'assessment': obj.assessment_points,
            'engagement': obj.engagement_points
        }
    
    def get_recent_transactions(self, obj):
        """Return recent point transactions"""
        recent_transactions = obj.point_transactions.order_by('-created_at')[:10]
        return PointTransactionSerializer(recent_transactions, many=True).data


class PointTransactionSerializer(serializers.ModelSerializer):
    """Point transaction serializer"""
    
    class Meta:
        model = PointTransaction
        fields = [
            'id', 'amount', 'transaction_type', 'source', 'description',
            'metadata', 'balance_after', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserLevelSerializer(serializers.ModelSerializer):
    """User level progression serializer"""
    progress_percentage = serializers.SerializerMethodField()
    xp_for_next_level = serializers.SerializerMethodField()
    
    class Meta:
        model = UserLevel
        fields = [
            'id', 'current_level', 'current_xp', 'total_xp',
            'xp_to_next_level', 'xp_for_next_level', 'progress_percentage',
            'level_up_notifications', 'last_level_up', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_at']
    
    def get_progress_percentage(self, obj):
        """Return progress percentage to next level"""
        return round(obj.progress_percentage, 1)
    
    def get_xp_for_next_level(self, obj):
        """Return total XP required for next level"""
        return obj.current_xp + obj.xp_to_next_level


class LearningStreakSerializer(serializers.ModelSerializer):
    """Learning streak serializer"""
    streak_multiplier_display = serializers.SerializerMethodField()
    days_since_last_activity = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningStreak
        fields = [
            'id', 'current_streak', 'longest_streak', 'last_activity_date',
            'streak_multiplier', 'streak_multiplier_display',
            'streak_history', 'streak_breaks',
            'days_since_last_activity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_streak_multiplier_display(self, obj):
        """Return formatted streak multiplier"""
        return f"{obj.streak_multiplier:.1f}x"
    
    def get_days_since_last_activity(self, obj):
        """Calculate days since last activity"""
        if obj.last_activity_date:
            delta = timezone.now().date() - obj.last_activity_date
            return delta.days
        return None


class LevelRequirementSerializer(serializers.ModelSerializer):
    """Level requirement serializer"""
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = LevelRequirement
        fields = [
            'id', 'level', 'requirement_type', 'requirement_value',
            'badge', 'title', 'description', 'unlock_features',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AchievementProgressSerializer(serializers.ModelSerializer):
    """Achievement progress tracking serializer"""
    achievement = AchievementSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = AchievementProgress
        fields = [
            'id', 'achievement', 'current_count', 'target_count',
            'progress_percentage', 'last_update', 'context_data'
        ]
        read_only_fields = ['id', 'last_update']
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage"""
        if obj.target_count == 0:
            return 0
        return round((obj.current_count / obj.target_count) * 100, 1)


class GamificationOverviewSerializer(serializers.Serializer):
    """Comprehensive gamification overview serializer"""
    
    total_points = serializers.IntegerField()
    current_level = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    total_achievements = serializers.IntegerField()
    completed_achievements = serializers.IntegerField()
    total_badges = serializers.IntegerField()
    earned_badges = serializers.IntegerField()
    
    # Detailed data
    recent_achievements = UserAchievementSerializer(many=True, read_only=True)
    recent_badges = UserBadgeSerializer(many=True, read_only=True)
    current_level_info = UserLevelSerializer(read_only=True)
    streak_info = LearningStreakSerializer(read_only=True)
    
    class Meta:
        fields = [
            'total_points', 'current_level', 'current_streak',
            'total_achievements', 'completed_achievements',
            'total_badges', 'earned_badges',
            'recent_achievements', 'recent_badges',
            'current_level_info', 'streak_info'
        ]


class LeaderboardSerializer(serializers.ModelSerializer):
    """Leaderboard entry serializer"""
    user = serializers.StringRelatedField(read_only=True)
    rank = serializers.IntegerField()
    
    class Meta:
        fields = ['user', 'rank', 'total_points', 'current_level', 'current_streak']


class GamificationStatsSerializer(serializers.Serializer):
    """Gamification statistics serializer"""
    
    total_users = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    total_achievements_completed = serializers.IntegerField()
    total_badges_earned = serializers.IntegerField()
    average_streak = serializers.FloatField()
    total_points_earned = serializers.IntegerField()
    
    # Top performers
    top_users_by_points = LeaderboardSerializer(many=True)
    top_users_by_streak = LeaderboardSerializer(many=True)
    
    # Recent activity
    recent_achievements = UserAchievementSerializer(many=True)
    recent_badges = UserBadgeSerializer(many=True)


# Create GamificationOverviewSerializer properly
class GamificationOverviewSerializer(serializers.Serializer):
    """Comprehensive gamification overview serializer"""
    
    total_points = serializers.IntegerField()
    current_level = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    total_achievements = serializers.IntegerField()
    completed_achievements = serializers.IntegerField()
    total_badges = serializers.IntegerField()
    earned_badges = serializers.IntegerField()
    
    # Detailed data
    recent_achievements = UserAchievementSerializer(many=True, read_only=True)
    recent_badges = UserBadgeSerializer(many=True, read_only=True)
    current_level_info = UserLevelSerializer(read_only=True)
    streak_info = LearningStreakSerializer(read_only=True)
    
    class Meta:
        fields = [
            'total_points', 'current_level', 'current_streak',
            'total_achievements', 'completed_achievements',
            'total_badges', 'earned_badges',
            'recent_achievements', 'recent_badges',
            'current_level_info', 'streak_info'
        ]


# Request serializers for API actions
class AddPointsSerializer(serializers.Serializer):
    """Request serializer for adding points"""
    amount = serializers.IntegerField(min_value=1)
    source = serializers.CharField(max_length=50)
    metadata = serializers.JSONField(required=False, default=dict)


class SpendPointsSerializer(serializers.Serializer):
    """Request serializer for spending points"""
    amount = serializers.IntegerField(min_value=1)
    purpose = serializers.CharField(max_length=100)
    metadata = serializers.JSONField(required=False, default=dict)


class UpdateAchievementProgressSerializer(serializers.Serializer):
    """Request serializer for updating achievement progress"""
    achievement_id = serializers.UUIDField()
    increment_by = serializers.IntegerField(min_value=1, default=1)
    context = serializers.JSONField(required=False, default=dict)


class RecordStreakActivitySerializer(serializers.Serializer):
    """Request serializer for recording streak activity"""
    activity_date = serializers.DateField(required=False)
    context = serializers.JSONField(required=False, default=dict)