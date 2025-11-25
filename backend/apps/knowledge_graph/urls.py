"""
URL configuration for Knowledge Graph API endpoints.

This module defines all URL patterns for the knowledge graph application,
providing routing for OSP-based knowledge representation and adaptive learning.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'nodes', views.KnowledgeNodeViewSet, basename='knowledgenode')
router.register(r'edges', views.KnowledgeEdgeViewSet, basename='knowledgeedge')
router.register(r'concepts', views.ConceptRelationViewSet, basename='conceptrelation')
router.register(r'graphs', views.LearningGraphViewSet, basename='learninggraph')
router.register(r'paths', views.LearningPathViewSet, basename='learningpath')
router.register(r'states', views.UserKnowledgeStateViewSet, basename='userknowledgestate')

# New API endpoints for enhanced functionality
from apps.api_endpoints.knowledge_graph_api import KnowledgeGraphAPIViewSet
router.register(r'api-extended', KnowledgeGraphAPIViewSet, basename='knowledge-api-extended')

# Create URL patterns
urlpatterns = [
    # API v1 endpoints
    path('api/v1/', include(router.urls)),
    
    # Custom endpoints for concept relationships
    path(
        'api/v1/concepts/relationships/',
        views.ConceptRelationshipsViewSet.as_view({'get': 'list'}),
        name='concept-relationships'
    ),
    
    # Learning path recommendations
    path(
        'api/v1/recommendations/',
        views.LearningPathRecommendationsViewSet.as_view({'get': 'list'}),
        name='learning-path-recommendations'
    ),
    
    # Graph analytics
    path(
        'api/v1/analytics/',
        views.GraphAnalyticsViewSet.as_view({'get': 'list'}),
        name='graph-analytics'
    ),
    path(
        'api/v1/analytics/<uuid:pk>/',
        views.GraphAnalyticsViewSet.as_view({'get': 'retrieve'}),
        name='graph-analytics-detail'
    ),
    
    # Convenience endpoints for common operations
    path(
        'api/v1/knowledge-graph/',
        views.KnowledgeNodeViewSet.as_view({'get': 'graph'}),
        name='knowledge-graph-complete'
    ),
    path(
        'api/v1/knowledge-graph/topic/',
        views.KnowledgeNodeViewSet.as_view({'get': 'topic_graph'}),
        name='knowledge-graph-topic'
    ),
    path(
        'api/v1/knowledge-graph/search/',
        views.KnowledgeNodeViewSet.as_view({'post': 'search'}),
        name='knowledge-graph-search'
    ),
    
    # Path generation endpoint
    path(
        'api/v1/paths/generate/',
        views.LearningPathViewSet.as_view({'post': 'generate'}),
        name='learning-path-generate'
    ),
]

# Additional URLs for specific use cases
additional_patterns = [
    # Legacy endpoints for backward compatibility
    path(
        'api/v1/graph/nodes/<uuid:pk>/increment-view/',
        views.KnowledgeNodeViewSet.as_view({'post': 'increment_view'}),
        name='node-increment-view'
    ),
    path(
        'api/v1/graph/nodes/<uuid:pk>/edges/',
        views.KnowledgeNodeViewSet.as_view({'get': 'edges'}),
        name='node-edges'
    ),
    path(
        'api/v1/graph/edges/<uuid:pk>/increment-traversal/',
        views.KnowledgeEdgeViewSet.as_view({'post': 'increment_traversal'}),
        name='edge-increment-traversal'
    ),
    path(
        'api/v1/graph/edges/<uuid:pk>/path-analysis/',
        views.KnowledgeEdgeViewSet.as_view({'get': 'path_analysis'}),
        name='edge-path-analysis'
    ),
    path(
        'api/v1/graphs/<uuid:pk>/analytics/',
        views.LearningGraphViewSet.as_view({'get': 'analytics'}),
        name='graph-analytics'
    ),
    path(
        'api/v1/graphs/<uuid:pk>/generate-paths/',
        views.LearningGraphViewSet.as_view({'post': 'generate_learning_paths'}),
        name='graph-generate-paths'
    ),
    path(
        'api/v1/graphs/<uuid:pk>/nodes/',
        views.LearningGraphViewSet.as_view({'get': 'nodes'}),
        name='graph-nodes'
    ),
    path(
        'api/v1/graphs/<uuid:pk>/edges/',
        views.LearningGraphViewSet.as_view({'get': 'edges'}),
        name='graph-edges'
    ),
    path(
        'api/v1/paths/<uuid:pk>/complete-node/',
        views.LearningPathViewSet.as_view({'post': 'complete_node'}),
        name='path-complete-node'
    ),
    path(
        'api/v1/paths/<uuid:pk>/adapt/',
        views.LearningPathViewSet.as_view({'post': 'adapt_path'}),
        name='path-adapt'
    ),
    path(
        'api/v1/states/<uuid:pk>/update-mastery/',
        views.UserKnowledgeStateViewSet.as_view({'post': 'update_mastery'}),
        name='state-update-mastery'
    ),
    path(
        'api/v1/states/<uuid:pk>/add-assessment/',
        views.UserKnowledgeStateViewSet.as_view({'post': 'add_assessment_score'}),
        name='state-add-assessment'
    ),
    path(
        'api/v1/concepts/by-concept/',
        views.ConceptRelationViewSet.as_view({'get': 'by_concept'}),
        name='concepts-by-concept'
    ),
    path(
        'api/v1/concepts/domains/',
        views.ConceptRelationViewSet.as_view({'get': 'domains'}),
        name='concepts-domains'
    ),
]

# Combine all patterns
urlpatterns.extend(additional_patterns)

# URL names for reverse lookup
app_name = 'knowledge_graph'

# Named URL patterns for easy reference
named_urlpatterns = {
    'api-root': 'api/v1/',
    'nodes-list': 'knowledgenode-list',
    'nodes-detail': 'knowledgenode-detail',
    'nodes-graph': 'knowledge-graph-complete',
    'nodes-topic-graph': 'knowledge-graph-topic',
    'nodes-search': 'knowledge-graph-search',
    'edges-list': 'knowledgeedge-list',
    'edges-detail': 'knowledgeedge-detail',
    'concepts-list': 'conceptrelation-list',
    'concepts-detail': 'conceptrelation-detail',
    'concepts-relationships': 'concept-relationships',
    'concepts-by-concept': 'concepts-by-concept',
    'concepts-domains': 'concepts-domains',
    'graphs-list': 'learninggraph-list',
    'graphs-detail': 'learninggraph-detail',
    'graphs-analytics': 'graph-analytics',
    'graphs-generate-paths': 'graph-generate-paths',
    'paths-list': 'learningpath-list',
    'paths-detail': 'learningpath-detail',
    'paths-generate': 'learning-path-generate',
    'paths-complete-node': 'path-complete-node',
    'paths-adapt': 'path-adapt',
    'recommendations': 'learning-path-recommendations',
    'states-list': 'userknowledgestate-list',
    'states-detail': 'userknowledgestate-detail',
    'states-update-mastery': 'state-update-mastery',
    'states-add-assessment': 'state-add-assessment',
    'analytics': 'graph-analytics',
    'analytics-detail': 'graph-analytics-detail',
}

# Export for documentation and testing
__all__ = ['urlpatterns', 'named_urlpatterns']