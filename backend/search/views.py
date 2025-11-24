"""
Search views for JAC Learning Platform
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import SearchQuery, SearchResult
from .serializers import (
    SearchRequestSerializer, 
    SearchResponseSerializer, 
    SearchSuggestionSerializer,
    SearchQuerySerializer,
    SearchResultSerializer
)
from .services.search_service import SearchService

User = get_user_model()


class SearchViewSet(viewsets.ViewSet):
    """
    ViewSet for handling search requests
    """
    permission_classes = []
    service = SearchService()
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Perform a comprehensive search across all content types
        """
        serializer = SearchRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query = serializer.validated_data['query']
        content_types = serializer.validated_data.get('content_types')
        limit = serializer.validated_data.get('limit', 20)
        offset = serializer.validated_data.get('offset', 0)
        
        # Get current user (optional)
        user = None
        if request.user.is_authenticated:
            user = request.user
        
        # Perform search
        search_results = self.service.search(
            query=query,
            user=user,
            content_types=content_types,
            limit=limit,
            offset=offset
        )
        
        # Serialize response
        response_serializer = SearchResponseSerializer(search_results)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        """
        Get search suggestions for autocomplete
        """
        query = request.query_params.get('query', '')
        limit = int(request.query_params.get('limit', 10))
        
        if len(query) < 2:
            return Response({'suggestions': []})
        
        suggestions = self.service.get_suggestions(query, limit)
        
        serializer = SearchSuggestionSerializer({'suggestions': suggestions})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def track_click(self, request):
        """
        Track user click on search result
        """
        query = request.data.get('query')
        result_url = request.data.get('result_url')
        
        if query and result_url:
            try:
                # Update search query with clicked result
                SearchQuery.objects.filter(query=query).update(clicked_result=result_url)
                return Response({'status': 'tracked'})
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'error': 'Missing query or result_url'}, status=status.HTTP_400_BAD_REQUEST)


class SearchHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user's search history
    """
    serializer_class = SearchQuerySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return user's search history"""
        return SearchQuery.objects.filter(user=self.request.user).order_by('-created_at')[:50]
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Clear user's search history"""
        SearchQuery.objects.filter(user=request.user).delete()
        return Response({'status': 'cleared'}, status=status.HTTP_200_OK)


class PopularSearchesViewSet(viewsets.ViewSet):
    """
    ViewSet for popular searches
    """
    permission_classes = []
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular search terms
        """
        limit = int(request.query_params.get('limit', 10))
        
        # Get most frequent search queries
        popular_queries = (SearchQuery.objects
                          .values('query')
                          .annotate(count=models.Count('query'))
                          .order_by('-count')
                          .values_list('query', flat=True)[:limit])
        
        return Response({'popular_searches': list(popular_queries)})
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """
        Get trending search terms (from last 24 hours)
        """
        from django.utils import timezone
        from datetime import timedelta
        
        limit = int(request.query_params.get('limit', 10))
        
        # Get recent popular queries
        recent_queries = (SearchQuery.objects
                         .filter(created_at__gte=timezone.now() - timedelta(days=1))
                         .values('query')
                         .annotate(count=models.Count('query'))
                         .order_by('-count')
                         .values_list('query', flat=True)[:limit])
        
        return Response({'trending_searches': list(recent_queries)})