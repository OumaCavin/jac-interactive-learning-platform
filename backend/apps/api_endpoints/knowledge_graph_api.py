# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
API Endpoints for Knowledge Graph and AI Multi-Agent System

Provides REST API endpoints for knowledge graph operations and AI agent interactions
"""

import json
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.utils import timezone

from apps.knowledge_graph.models import (
    KnowledgeNode, KnowledgeEdge, LearningGraph, 
    UserKnowledgeState, LearningPath, ConceptRelation
)
from apps.knowledge_graph.services.jac_populator import JACKnowledgeGraphPopulator
from apps.agents.ai_multi_agent_system import get_multi_agent_system, MultiAgentSystem

User = get_user_model()


class KnowledgeGraphAPIViewSet(viewsets.ViewSet):
    """
    API ViewSet for Knowledge Graph operations
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def concepts(self, request):
        """Get all knowledge concepts with filtering and pagination"""
        try:
            # Get query parameters
            node_type = request.query_params.get('node_type', 'concept')
            difficulty = request.query_params.get('difficulty_level')
            category = request.query_params.get('category')
            search = request.query_params.get('search')
            limit = int(request.query_params.get('limit', 50))
            offset = int(request.query_params.get('offset', 0))
            
            # Build query
            queryset = KnowledgeNode.objects.filter(
                node_type=node_type,
                is_active=True
            )
            
            if difficulty:
                queryset = queryset.filter(difficulty_level=difficulty)
            
            if category:
                queryset = queryset.filter(category=category)
            
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) | 
                    Q(description__icontains=search) |
                    Q(tags__icontains=search)
                )
            
            # Get total count
            total_count = queryset.count()
            
            # Apply pagination
            concepts = queryset.order_by('title')[offset:offset + limit]
            
            # Serialize results
            concept_data = []
            for concept in concepts:
                concept_data.append({
                    'id': str(concept.id),
                    'title': concept.title,
                    'description': concept.description,
                    'node_type': concept.node_type,
                    'difficulty_level': concept.difficulty_level,
                    'category': concept.category,
                    'tags': concept.tags,
                    'learning_objectives': concept.learning_objectives,
                    'prerequisites': concept.prerequisites,
                    'view_count': concept.view_count,
                    'created_at': concept.created_at.isoformat(),
                    'updated_at': concept.updated_at.isoformat()
                })
            
            return Response({
                'success': True,
                'data': {
                    'concepts': concept_data,
                    'pagination': {
                        'total': total_count,
                        'limit': limit,
                        'offset': offset,
                        'has_more': offset + limit < total_count
                    }
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def concept_relations(self, request):
        """Get concept relationships and connections"""
        try:
            concept_id = request.query_params.get('concept_id')
            relation_type = request.query_params.get('relation_type')
            depth = int(request.query_params.get('depth', 1))
            
            if not concept_id:
                return Response({
                    'success': False,
                    'error': 'concept_id parameter required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get direct relationships
            edges = KnowledgeEdge.objects.filter(
                Q(source_node_id=concept_id) | Q(target_node_id=concept_id),
                is_active=True
            )
            
            if relation_type:
                edges = edges.filter(edge_type=relation_type)
            
            # Serialize relationships
            relationships = []
            for edge in edges:
                is_outgoing = edge.source_node_id == concept_id
                related_node = edge.target_node if is_outgoing else edge.source_node
                
                relationships.append({
                    'id': str(edge.id),
                    'related_concept': {
                        'id': str(related_node.id),
                        'title': related_node.title,
                        'description': related_node.description,
                        'node_type': related_node.node_type,
                        'difficulty_level': related_node.difficulty_level
                    },
                    'relationship': {
                        'type': edge.edge_type,
                        'strength': edge.strength,
                        'direction': 'outgoing' if is_outgoing else 'incoming',
                        'description': edge.description
                    },
                    'traversal_count': edge.traversal_count
                })
            
            return Response({
                'success': True,
                'data': {
                    'relationships': relationships,
                    'depth': depth,
                    'total_relations': len(relationships)
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def learning_paths(self, request):
        """Get available learning paths"""
        try:
            user_id = request.query_params.get('user_id')
            difficulty = request.query_params.get('difficulty_level')
            category = request.query_params.get('category')
            
            # Get learning graphs
            queryset = LearningGraph.objects.filter(status='active')
            
            if difficulty:
                queryset = queryset.filter(target_audience=difficulty)
            
            if category:
                queryset = queryset.filter(subject_area__icontains=category)
            
            graphs = queryset.order_by('-completion_rate', 'title')
            
            # Serialize learning paths
            paths = []
            for graph in graphs:
                # Get nodes in this graph
                nodes = graph.nodes.filter(is_active=True)
                
                paths.append({
                    'id': str(graph.id),
                    'title': graph.title,
                    'description': graph.description,
                    'graph_type': graph.graph_type,
                    'subject_area': graph.subject_area,
                    'target_audience': graph.target_audience,
                    'estimated_duration': str(graph.estimated_duration) if graph.estimated_duration else None,
                    'completion_rate': graph.completion_rate,
                    'total_nodes': nodes.count(),
                    'tags': graph.tags,
                    'created_at': graph.created_at.isoformat()
                })
            
            return Response({
                'success': True,
                'data': {
                    'learning_paths': paths
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def personalized_recommendations(self, request):
        """Get personalized concept recommendations based on user progress"""
        try:
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response({
                    'success': False,
                    'error': 'user_id parameter required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get user's current knowledge state
            user_states = UserKnowledgeState.objects.filter(user_id=user_id)
            
            # Get concepts the user has low mastery in
            low_mastery_concepts = user_states.filter(
                mastery_level__in=['novice', 'beginner']
            ).values_list('knowledge_node_id', flat=True)
            
            # Get concepts user hasn't studied yet
            studied_concept_ids = set(user_states.values_list('knowledge_node_id', flat=True))
            unstudied_concepts = KnowledgeNode.objects.filter(
                node_type='concept',
                is_active=True
            ).exclude(id__in=studied_concept_ids)
            
            # Get prerequisites for studied concepts that might be missing
            missing_prerequisites = []
            for state in user_states:
                concept = state.knowledge_node
                if concept.prerequisites:
                    for prereq in concept.prerequisites:
                        prereq_node = KnowledgeNode.objects.filter(
                            title__icontains=prereq
                        ).first()
                        if prereq_node and prereq_node.id not in studied_concept_ids:
                            missing_prerequisites.append(prereq_node)
            
            # Combine recommendations
            recommendations = {
                'concepts_to_learn': unstudied_concepts[:5].values(
                    'id', 'title', 'description', 'difficulty_level', 'category'
                ),
                'concepts_to_review': KnowledgeNode.objects.filter(
                    id__in=low_mastery_concepts
                ).values('id', 'title', 'description', 'difficulty_level')[:5],
                'missing_prerequisites': [
                    {
                        'id': str(node.id),
                        'title': node.title,
                        'description': node.description,
                        'difficulty_level': node.difficulty_level
                    } for node in missing_prerequisites[:3]
                ]
            }
            
            return Response({
                'success': True,
                'data': recommendations
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def populate_jac_knowledge_graph(self, request):
        """Populate the knowledge graph with JAC content"""
        try:
            # Only allow admin users to populate
            if not request.user.is_staff:
                return Response({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Populate the knowledge graph
            populator = JACKnowledgeGraphPopulator()
            result = populator.populate_graph()
            
            return Response({
                'success': True,
                'message': 'JAC Knowledge Graph populated successfully',
                'data': {
                    'concepts_created': len(result['concepts']),
                    'relationships_created': len(result['relationships']),
                    'graphs_created': len(result['graphs']),
                    'concept_relations_created': len(result['concept_relations'])
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def track_concept_interaction(self, request):
        """Track user interaction with a concept for learning analytics"""
        try:
            user_id = request.data.get('user_id')
            concept_id = request.data.get('concept_id')
            interaction_type = request.data.get('interaction_type', 'view')  # view, study, practice, mastered
            
            if not user_id or not concept_id:
                return Response({
                    'success': False,
                    'error': 'user_id and concept_id are required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get or create user knowledge state
            user_state, created = UserKnowledgeState.objects.get_or_create(
                user_id=user_id,
                knowledge_node_id=concept_id,
                defaults={
                    'mastery_level': 'novice',
                    'confidence_score': 0.0
                }
            )
            
            # Update interaction data based on type
            if interaction_type == 'view':
                user_state.knowledge_node.increment_view_count()
            elif interaction_type == 'study':
                user_state.practice_attempts += 1
                user_state.last_reviewed = timezone.now()
            elif interaction_type == 'mastered':
                user_state.mastery_level = 'proficient'
                user_state.confidence_score = 0.8
                user_state.successful_attempts += 1
            
            user_state.save()
            
            return Response({
                'success': True,
                'message': f'Interaction tracked: {interaction_type}',
                'data': {
                    'mastery_level': user_state.mastery_level,
                    'confidence_score': user_state.confidence_score,
                    'practice_attempts': user_state.practice_attempts,
                    'view_count': user_state.knowledge_node.view_count
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AIAgentAPIViewSet(viewsets.ViewSet):
    """
    API ViewSet for AI Multi-Agent System
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def available_agents(self, request):
        """Get information about available AI agents"""
        try:
            agent_system = get_multi_agent_system()
            agents_info = agent_system.get_available_agents()
            
            return Response({
                'success': True,
                'data': {
                    'agents': agents_info,
                    'total_agents': len(agents_info)
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Chat with AI agents"""
        try:
            agent_system = get_multi_agent_system()
            
            # Prepare request data
            chat_request = {
                'user_id': request.user.id,
                'message': request.data.get('message', ''),
                'agent_type': request.data.get('agent_type', 'learning_assistant'),
                'session_id': request.data.get('session_id'),
                'context': request.data.get('context', {})
            }
            
            # Process the request
            result = agent_system.process_request(chat_request)
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def multi_agent_collaboration(self, request):
        """Use multiple agents to provide comprehensive assistance"""
        try:
            agent_system = get_multi_agent_system()
            
            # Prepare request data
            collaboration_request = {
                'user_id': request.user.id,
                'message': request.data.get('message', ''),
                'context': request.data.get('context', {})
            }
            
            # Process multi-agent collaboration
            result = agent_system.multi_agent_collaboration(
                collaboration_request['message'],
                collaboration_request['context']
            )
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def generate_learning_content(self, request):
        """Generate educational content using AI agents"""
        try:
            agent_system = get_multi_agent_system()
            
            # Request content generation from content generator agent
            content_request = {
                'user_id': request.user.id,
                'message': f"""Please create educational content for: {request.data.get('topic', 'JAC programming')}
                
Requirements:
- Difficulty level: {request.data.get('difficulty', 'intermediate')}
- Content type: {request.data.get('content_type', 'tutorial')}
- Learning objectives: {request.data.get('learning_objectives', [])}
- Include practical examples: {request.data.get('include_examples', True)}
""",
                'agent_type': 'content_generator',
                'context': {
                    'topic': request.data.get('topic'),
                    'difficulty': request.data.get('difficulty'),
                    'content_type': request.data.get('content_type'),
                    'learning_objectives': request.data.get('learning_objectives', [])
                }
            }
            
            result = agent_system.process_request(content_request)
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def review_code(self, request):
        """Get AI code review and feedback"""
        try:
            agent_system = get_multi_agent_system()
            
            # Request code review from code reviewer agent
            review_request = {
                'user_id': request.user.id,
                'message': f"""Please review this JAC code and provide feedback:

Language: {request.data.get('language', 'jac')}
Code:
```{(request.data.get('language', 'jac'))}
{request.data.get('code', '')}
```

Areas to focus on:
- Code quality and readability
- JAC best practices
- Performance considerations
- Potential improvements
- Educational feedback
""",
                'agent_type': 'code_reviewer',
                'context': {
                    'code': request.data.get('code'),
                    'language': request.data.get('language', 'jac'),
                    'review_type': request.data.get('review_type', 'comprehensive')
                }
            }
            
            result = agent_system.process_request(review_request)
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def get_learning_path_recommendation(self, request):
        """Get personalized learning path recommendations"""
        try:
            agent_system = get_multi_agent_system()
            
            # Get user knowledge state for context
            user_id = request.user.id
            from apps.knowledge_graph.models import UserKnowledgeState
            
            user_states = UserKnowledgeState.objects.filter(user_id=user_id)
            knowledge_context = {
                'current_knowledge': [
                    {
                        'concept': state.knowledge_node.title,
                        'mastery_level': state.mastery_level,
                        'confidence': state.confidence_score
                    } for state in user_states[:10]
                ],
                'learning_goals': request.data.get('learning_goals', []),
                'time_available': request.data.get('time_available'),
                'preferred_difficulty': request.data.get('preferred_difficulty', 'intermediate')
            }
            
            # Request learning path from knowledge explorer agent
            path_request = {
                'user_id': user_id,
                'message': f"""Please create a personalized learning path recommendation based on my current knowledge and goals.

Current Knowledge: {json.dumps(knowledge_context['current_knowledge'], indent=2)}
Learning Goals: {', '.join(knowledge_context['learning_goals'])}
Available Time: {knowledge_context['time_available']} hours
Preferred Difficulty: {knowledge_context['preferred_difficulty']}

Please provide:
1. Recommended learning sequence
2. Key concepts to focus on
3. Estimated timeline
4. Prerequisites to address
5. Practice exercises suggestions
""",
                'agent_type': 'knowledge_explorer',
                'context': knowledge_context
            }
            
            result = agent_system.process_request(path_request)
            
            return Response({
                'success': True,
                'data': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)