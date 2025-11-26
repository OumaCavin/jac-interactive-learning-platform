# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Content views for JAC Learning Platform
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Content, ContentRecommendation, ContentAnalytics
from .serializers import ContentSerializer, ContentRecommendationSerializer
from ..agents.content_curator import ContentCuratorAgent


class ContentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for content management
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    
    def get_queryset(self):
        """Filter content based on user permissions and query params"""
        queryset = Content.objects.filter(is_published=True)
        
        # Filter by content type
        content_type = self.request.query_params.get('content_type', None)
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by topic
        topic = self.request.query_params.get('topic', None)
        if topic:
            queryset = queryset.filter(topic=topic)
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def by_learning_path(self, request):
        """Get content by learning path"""
        learning_path_id = request.query_params.get('learning_path_id')
        if not learning_path_id:
            return Response(
                {'error': 'learning_path_id parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        content_items = Content.objects.filter(
            learning_path_id=learning_path_id,
            is_published=True
        ).order_by('created_at')
        
        serializer = self.get_serializer(content_items, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def track_view(self, request, pk=None):
        """Track content view"""
        content = self.get_object()
        
        # Update analytics
        analytics, created = ContentAnalytics.objects.get_or_create(content=content)
        analytics.total_views += 1
        analytics.save()
        
        return Response({'message': 'View tracked successfully'})
    
    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get personalized content recommendations"""
        user = request.user
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Use ContentCuratorAgent to generate recommendations
        agent = ContentCuratorAgent()
        task = {
            'type': 'recommend_content',
            'params': {
                'user_id': str(user.id),
                'max_recommendations': 10
            }
        }
        
        result = agent.process_task(task)
        return Response(result)


class ContentRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for content recommendations
    """
    queryset = ContentRecommendation.objects.all()
    serializer_class = ContentRecommendationSerializer
    
    def get_queryset(self):
        """Filter recommendations for current user"""
        if not self.request.user.is_authenticated:
            return ContentRecommendation.objects.none()
        
        return ContentRecommendation.objects.filter(
            user=self.request.user,
            is_dismissed=False
        ).order_by('-match_score', '-created_at')
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss a recommendation"""
        recommendation = get_object_or_404(ContentRecommendation, pk=pk, user=request.user)
        recommendation.is_dismissed = True
        recommendation.save()
        
        return Response({'message': 'Recommendation dismissed'})
