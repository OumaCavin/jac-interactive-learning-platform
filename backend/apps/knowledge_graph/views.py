"""
Views for Knowledge Graph API endpoints.

This module provides REST API endpoints for managing OSP-based knowledge graphs,
learning paths, and adaptive learning systems in the JAC Learning Platform.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg, F, Case, When
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import logging

from .models import (
    KnowledgeNode, KnowledgeEdge, ConceptRelation, LearningGraph,
    LearningGraphNode, LearningGraphEdge, LearningPath, UserKnowledgeState
)
from .serializers import (
    KnowledgeNodeSerializer, KnowledgeNodeCreateSerializer,
    KnowledgeEdgeSerializer, KnowledgeEdgeCreateSerializer,
    ConceptRelationSerializer, LearningGraphSerializer,
    LearningGraphNodeSerializer, LearningGraphEdgeSerializer,
    LearningPathSerializer, LearningPathUpdateSerializer,
    UserKnowledgeStateSerializer, UserKnowledgeStateUpdateSerializer,
    GraphDataSerializer, TopicGraphSerializer, ConceptRelationshipsSerializer,
    LearningPathRecommendationSerializer, GraphAnalyticsSerializer,
    GraphSearchSerializer, LearningPathGenerateSerializer
)
from .services.graph_algorithms import GraphAnalyzer, PathFinder, AdaptiveEngine
from .services.osp_implementation import OSPProcessor
from .services.analytics import KnowledgeGraphAnalytics


logger = logging.getLogger(__name__)


class KnowledgeNodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing KnowledgeNode instances.
    
    Provides CRUD operations and additional actions for knowledge graph nodes.
    """
    
    queryset = KnowledgeNode.objects.all().prefetch_related('outgoing_edges', 'incoming_edges')
    serializer_class = KnowledgeNodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['node_type', 'difficulty_level', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at', 'view_count', 'difficulty_level']
    ordering = ['title']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return KnowledgeNodeCreateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        """Get permissions for the action"""
        if self.action in ['list', 'retrieve', 'graph', 'topic_graph', 'search']:
            return [AllowAny()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """Increment view count for a knowledge node"""
        try:
            node = self.get_object()
            node.increment_view_count()
            return Response({
                'status': 'success',
                'view_count': node.view_count
            })
        except Exception as e:
            logger.error(f"Error incrementing view count: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def edges(self, request, pk=None):
        """Get all edges related to this node"""
        node = self.get_object()
        
        outgoing_edges = node.outgoing_edges.filter(is_active=True)
        incoming_edges = node.incoming_edges.filter(is_active=True)
        
        outgoing_serializer = KnowledgeEdgeSerializer(outgoing_edges, many=True)
        incoming_serializer = KnowledgeEdgeSerializer(incoming_edges, many=True)
        
        return Response({
            'outgoing_edges': outgoing_serializer.data,
            'incoming_edges': incoming_serializer.data,
            'total_edges': len(outgoing_edges) + len(incoming_edges)
        })
    
    @action(detail=False, methods=['get'])
    def graph(self, request):
        """Get complete knowledge graph with all nodes and edges"""
        try:
            analyzer = GraphAnalyzer()
            graph_data = analyzer.get_complete_graph()
            
            serializer = GraphDataSerializer(graph_data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting complete graph: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def topic_graph(self, request):
        """Get knowledge graph filtered by topic"""
        topic = request.query_params.get('topic')
        if not topic:
            return Response({
                'status': 'error',
                'message': 'Topic parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            analyzer = GraphAnalyzer()
            graph_data = analyzer.get_topic_graph(topic)
            
            serializer = TopicGraphSerializer(graph_data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting topic graph: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Search knowledge graph with advanced filters"""
        try:
            serializer = GraphSearchSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            analyzer = GraphAnalyzer()
            results = analyzer.search_nodes(**serializer.validated_data)
            
            node_serializer = KnowledgeNodeSerializer(results, many=True)
            return Response({
                'nodes': node_serializer.data,
                'total_results': len(results)
            })
        except Exception as e:
            logger.error(f"Error searching nodes: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KnowledgeEdgeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing KnowledgeEdge instances.
    
    Provides CRUD operations and pathfinding functionality.
    """
    
    queryset = KnowledgeEdge.objects.all()
    serializer_class = KnowledgeEdgeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['edge_type', 'strength', 'is_active']
    search_fields = ['description']
    ordering_fields = ['traversal_count', 'created_at', 'edge_type']
    ordering = ['-traversal_count']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'create':
            return KnowledgeEdgeCreateSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def increment_traversal(self, request, pk=None):
        """Increment traversal count for an edge"""
        try:
            edge = self.get_object()
            edge.increment_traversal()
            return Response({
                'status': 'success',
                'traversal_count': edge.traversal_count
            })
        except Exception as e:
            logger.error(f"Error incrementing traversal count: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def path_analysis(self, request, pk=None):
        """Analyze paths that include this edge"""
        try:
            edge = self.get_object()
            analyzer = GraphAnalyzer()
            paths = analyzer.analyze_edge_paths(edge.id)
            
            return Response({
                'edge_id': str(edge.id),
                'paths': paths,
                'total_paths': len(paths)
            })
        except Exception as e:
            logger.error(f"Error analyzing paths: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConceptRelationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ConceptRelation instances.
    
    Handles high-level concept relationships and semantic connections.
    """
    
    queryset = ConceptRelation.objects.all()
    serializer_class = ConceptRelationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['relation_type', 'domain', 'is_active']
    search_fields = ['concept_a', 'concept_b', 'description']
    ordering_fields = ['confidence_score', 'created_at', 'relation_type']
    ordering = ['-confidence_score', '-created_at']
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def by_concept(self, request):
        """Get all relations involving a specific concept"""
        concept = request.query_params.get('concept')
        if not concept:
            return Response({
                'status': 'error',
                'message': 'Concept parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        relations = self.queryset.filter(
            Q(concept_a__icontains=concept) | Q(concept_b__icontains=concept),
            is_active=True
        )
        
        serializer = self.get_serializer(relations, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def domains(self, request):
        """Get all available domains"""
        domains = self.queryset.filter(is_active=True).values_list(
            'domain', flat=True
        ).distinct().order_by('domain')
        
        return Response({
            'domains': list(domains)
        })


class LearningGraphViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LearningGraph instances.
    
    Provides CRUD operations for complete learning graphs and analytics.
    """
    
    queryset = LearningGraph.objects.all().prefetch_related(
        'learninggraphnode_set__knowledge_node',
        'learninggraphedge_set__knowledge_edge'
    )
    serializer_class = LearningGraphSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['graph_type', 'status', 'subject_area', 'target_audience']
    search_fields = ['title', 'description', 'subject_area']
    ordering_fields = ['title', 'completion_rate', 'created_at', 'total_attempts']
    ordering = ['-completion_rate']
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Get analytics data for a learning graph"""
        try:
            graph = self.get_object()
            analytics = KnowledgeGraphAnalytics()
            data = analytics.get_graph_analytics(graph.id)
            
            serializer = GraphAnalyticsSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting graph analytics: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def generate_learning_paths(self, request, pk=None):
        """Generate learning paths for users based on this graph"""
        try:
            graph = self.get_object()
            user_ids = request.data.get('user_ids', [])
            
            if not user_ids:
                return Response({
                    'status': 'error',
                    'message': 'user_ids parameter is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            adaptive_engine = AdaptiveEngine()
            paths = []
            
            for user_id in user_ids:
                try:
                    user = User.objects.get(id=user_id)
                    path = adaptive_engine.generate_learning_path(user, graph)
                    paths.append({
                        'user_id': user_id,
                        'path_id': str(path.id),
                        'status': 'success'
                    })
                except User.DoesNotExist:
                    paths.append({
                        'user_id': user_id,
                        'status': 'error',
                        'message': 'User not found'
                    })
            
            return Response({
                'graph_id': str(graph.id),
                'generated_paths': paths,
                'total_generated': len([p for p in paths if p['status'] == 'success'])
            })
        except Exception as e:
            logger.error(f"Error generating learning paths: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def nodes(self, request, pk=None):
        """Get all nodes in this learning graph"""
        graph = self.get_object()
        graph_nodes = graph.learninggraphnode_set.all()
        
        serializer = LearningGraphNodeSerializer(graph_nodes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def edges(self, request, pk=None):
        """Get all edges in this learning graph"""
        graph = self.get_object()
        graph_edges = graph.learninggraphedge_set.all()
        
        serializer = LearningGraphEdgeSerializer(graph_edges, many=True)
        return Response(serializer.data)


class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing LearningPath instances.
    
    Provides CRUD operations and path tracking functionality.
    """
    
    queryset = LearningPath.objects.all().select_related(
        'user', 'learning_graph', 'current_node'
    )
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'adaptation_type']
    search_fields = ['title']
    ordering_fields = ['progress_percentage', 'started_at', 'last_activity']
    ordering = ['-last_activity']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return LearningPathUpdateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        """Filter paths by user if user_id parameter is provided"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def complete_node(self, request, pk=None):
        """Mark a node as completed in the learning path"""
        try:
            path = self.get_object()
            node_id = request.data.get('node_id')
            time_spent = request.data.get('time_spent')
            
            if not node_id:
                return Response({
                    'status': 'error',
                    'message': 'node_id parameter is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            path.update_progress(node_id)
            
            if time_spent:
                from datetime import timedelta
                duration = timedelta(seconds=time_spent)
                path.add_time_spent(duration)
            
            return Response({
                'status': 'success',
                'path_id': str(path.id),
                'progress_percentage': path.progress_percentage,
                'completed_nodes_count': len(path.completed_nodes)
            })
        except Exception as e:
            logger.error(f"Error completing node: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def adapt_path(self, request, pk=None):
        """Adapt the learning path based on user performance"""
        try:
            path = self.get_object()
            adaptive_engine = AdaptiveEngine()
            
            adapted_path = adaptive_engine.adapt_learning_path(path)
            
            return Response({
                'status': 'success',
                'path_id': str(path.id),
                'adaptations_made': len(path.adaptation_history),
                'new_difficulty_adjustment': adapted_path.get('difficulty_adjustment', 0)
            })
        except Exception as e:
            logger.error(f"Error adapting path: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a new learning path"""
        try:
            serializer = LearningPathGenerateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            data = serializer.validated_data
            user = User.objects.get(id=data['user_id'])
            graph = LearningGraph.objects.get(id=data['learning_graph_id'])
            
            adaptive_engine = AdaptiveEngine()
            path = adaptive_engine.generate_learning_path(
                user, 
                graph, 
                adaptation_type=data['adaptation_type'],
                preferences=data.get('preferences', {}),
                constraints=data.get('constraints', {})
            )
            
            path_serializer = LearningPathSerializer(path)
            return Response(path_serializer.data)
        except (User.DoesNotExist, LearningGraph.DoesNotExist) as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserKnowledgeStateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing UserKnowledgeState instances.
    
    Tracks individual user's knowledge state and mastery levels.
    """
    
    queryset = UserKnowledgeState.objects.all().select_related('user', 'knowledge_node')
    serializer_class = UserKnowledgeStateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mastery_level', 'user', 'knowledge_node']
    search_fields = ['user__username', 'knowledge_node__title']
    ordering_fields = ['confidence_score', 'learning_velocity', 'last_reviewed']
    ordering = ['-confidence_score']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action in ['update', 'partial_update']:
            return UserKnowledgeStateUpdateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        """Filter by user if user_id parameter is provided"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def update_mastery(self, request, pk=None):
        """Update mastery level for a user knowledge state"""
        try:
            state = self.get_object()
            mastery_level = request.data.get('mastery_level')
            confidence = request.data.get('confidence')
            
            if not mastery_level:
                return Response({
                    'status': 'error',
                    'message': 'mastery_level parameter is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            state.update_mastery(mastery_level, confidence)
            
            return Response({
                'status': 'success',
                'mastery_level': state.mastery_level,
                'confidence_score': state.confidence_score,
                'learning_velocity': state.learning_velocity
            })
        except Exception as e:
            logger.error(f"Error updating mastery: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def add_assessment_score(self, request, pk=None):
        """Add an assessment score to the knowledge state"""
        try:
            state = self.get_object()
            score = request.data.get('score')
            max_score = request.data.get('max_score', 100)
            
            if score is None:
                return Response({
                    'status': 'error',
                    'message': 'score parameter is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            state.add_assessment_score(score, max_score)
            
            return Response({
                'status': 'success',
                'assessment_scores': state.assessment_scores,
                'confidence_score': state.confidence_score,
                'success_rate': state.get_success_rate()
            })
        except Exception as e:
            logger.error(f"Error adding assessment score: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConceptRelationshipsViewSet(viewsets.ViewSet):
    """
    ViewSet for concept relationship analysis.
    
    Provides endpoints for analyzing relationships between concepts.
    """
    
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Get concept relationships for a specific concept"""
        concept = request.query_params.get('concept')
        if not concept:
            return Response({
                'status': 'error',
                'message': 'concept parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get related concepts
            concept_relations = ConceptRelation.objects.filter(
                Q(concept_a__icontains=concept) | Q(concept_b__icontains=concept),
                is_active=True
            ).prefetch_related('related_nodes')
            
            # Get knowledge nodes for this concept
            knowledge_nodes = KnowledgeNode.objects.filter(
                Q(title__icontains=concept) | Q(description__icontains=concept),
                is_active=True
            )
            
            # Build related concepts list
            related_concepts = []
            for relation in concept_relations:
                if concept.lower() in relation.concept_a.lower():
                    related_concepts.append({
                        'concept': relation.concept_b,
                        'relation_type': relation.relation_type,
                        'confidence': relation.confidence_score,
                        'domain': relation.domain
                    })
                else:
                    related_concepts.append({
                        'concept': relation.concept_a,
                        'relation_type': relation.relation_type,
                        'confidence': relation.confidence_score,
                        'domain': relation.domain
                    })
            
            # Get learning paths that include this concept
            learning_paths = []
            for node in knowledge_nodes:
                paths = LearningPath.objects.filter(
                    learning_graph__nodes=node,
                    status__in=['active', 'completed']
                ).select_related('user', 'learning_graph')[:10]
                
                for path in paths:
                    if node.id in path.completed_nodes or path.current_node_id == node.id:
                        learning_paths.append({
                            'path_id': str(path.id),
                            'path_title': path.title,
                            'user': path.user.username,
                            'learning_graph': path.learning_graph.title,
                            'status': path.status
                        })
            
            concept_relations_serializer = ConceptRelationSerializer(concept_relations, many=True)
            
            serializer = ConceptRelationshipsSerializer({
                'concept': concept,
                'related_concepts': related_concepts,
                'concept_relations': concept_relations_serializer.data,
                'learning_paths': learning_paths
            })
            
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting concept relationships: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LearningPathRecommendationsViewSet(viewsets.ViewSet):
    """
    ViewSet for learning path recommendations.
    
    Provides AI-driven recommendations for personalized learning paths.
    """
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get learning path recommendations for a user"""
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                user_id = request.user.id
            else:
                # Check if user can view recommendations for other users
                if str(request.user.id) != str(user_id) and not request.user.is_staff:
                    return Response({
                        'status': 'error',
                        'message': 'Permission denied'
                    }, status=status.HTTP_403_FORBIDDEN)
            
            user = User.objects.get(id=user_id)
            adaptive_engine = AdaptiveEngine()
            
            recommendations = adaptive_engine.get_recommendations(user)
            
            # Get user's current learning paths
            current_paths = LearningPath.objects.filter(
                user=user,
                status__in=['active', 'paused']
            ).select_related('learning_graph')[:5]
            
            path_serializer = LearningPathSerializer(current_paths, many=True)
            
            serializer = LearningPathRecommendationSerializer({
                'user_id': user_id,
                'learning_paths': path_serializer.data,
                'recommendations': recommendations,
                'adaptation_suggestions': adaptive_engine.get_adaptation_suggestions(user)
            })
            
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GraphAnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for knowledge graph analytics.
    
    Provides comprehensive analytics and insights for knowledge graphs.
    """
    
    permission_classes = [AllowAny]
    
    def list(self, request):
        """Get overall knowledge graph analytics"""
        try:
            analytics = KnowledgeGraphAnalytics()
            data = analytics.get_overall_analytics()
            
            serializer = GraphAnalyticsSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting analytics: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk=None):
        """Get analytics for a specific learning graph"""
        try:
            analytics = KnowledgeGraphAnalytics()
            data = analytics.get_graph_analytics(pk)
            
            serializer = GraphAnalyticsSerializer(data)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting graph analytics: {str(e)}")
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)