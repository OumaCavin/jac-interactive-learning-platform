"""
Content serializers for JAC Learning Platform
"""

from rest_framework import serializers
from .models import Content, ContentRecommendation, ContentAnalytics


class ContentSerializer(serializers.ModelSerializer):
    """
    Serializer for Content model
    """
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    quality_score = serializers.ReadOnlyField()
    
    class Meta:
        model = Content
        fields = [
            'content_id', 'title', 'description', 'content_type', 'difficulty_level',
            'content_data', 'estimated_duration', 'tags', 'topic', 'quality_rating',
            'quality_score', 'learning_path', 'is_published', 'is_featured',
            'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create content with current user as creator"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ContentRecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentRecommendation model
    """
    content_title = serializers.CharField(source='content.title', read_only=True)
    content_description = serializers.CharField(source='content.description', read_only=True)
    
    class Meta:
        model = ContentRecommendation
        fields = [
            'recommendation_id', 'user', 'content', 'content_title', 'content_description',
            'recommendation_type', 'match_score', 'reasoning', 'is_viewed',
            'is_dismissed', 'clicked_at', 'created_at', 'expires_at'
        ]
        read_only_fields = ['user', 'created_at']


class ContentAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentAnalytics model
    """
    content_title = serializers.CharField(source='content.title', read_only=True)
    
    class Meta:
        model = ContentAnalytics
        fields = [
            'content', 'content_title', 'total_views', 'unique_viewers',
            'total_time_spent', 'average_completion_rate', 'total_clicks',
            'total_shares', 'total_ratings', 'average_rating', 'bounce_rate',
            'return_visit_rate', 'created_at', 'updated_at'
        ]
