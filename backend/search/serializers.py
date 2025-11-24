"""
Search serializers for JAC Learning Platform
"""

from rest_framework import serializers
from .models import SearchQuery, SearchResult


class SearchResultSerializer(serializers.ModelSerializer):
    """
    Serializer for search result items
    """
    class Meta:
        model = SearchResult
        fields = [
            'id',
            'content_type',
            'content_id', 
            'title',
            'description',
            'url',
            'tags',
            'relevance_score',
            'popularity_score'
        ]
        read_only_fields = fields


class SearchQuerySerializer(serializers.ModelSerializer):
    """
    Serializer for search queries
    """
    class Meta:
        model = SearchQuery
        fields = [
            'id',
            'query',
            'results_count',
            'clicked_result',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SearchRequestSerializer(serializers.Serializer):
    """
    Serializer for search requests
    """
    query = serializers.CharField(
        max_length=255,
        help_text='Search query text'
    )
    content_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='List of content types to search in'
    )
    limit = serializers.IntegerField(
        default=20,
        min_value=1,
        max_value=100,
        help_text='Maximum number of results to return'
    )
    offset = serializers.IntegerField(
        default=0,
        min_value=0,
        help_text='Number of results to skip'
    )


class SearchResponseSerializer(serializers.Serializer):
    """
    Serializer for search responses
    """
    query = serializers.CharField()
    results = SearchResultSerializer(many=True)
    total_results = serializers.IntegerField()
    suggestions = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text='Search suggestions'
    )
    facets = serializers.DictField(
        required=False,
        help_text='Filter facets for results'
    )


class SearchSuggestionSerializer(serializers.Serializer):
    """
    Serializer for search suggestions
    """
    suggestions = serializers.ListField(
        child=serializers.CharField(),
        help_text='List of suggested search terms'
    )