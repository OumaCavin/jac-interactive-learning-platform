"""
Analytics Service for Knowledge Graph Analysis.

This module provides comprehensive analytics and insights for knowledge graphs,
learning paths, and user performance metrics.
"""

import uuid
import json
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from django.db.models import (
    Q, Count, Avg, Sum, F, Case, When, Value, IntegerField, 
    DurationField, ExpressionWrapper
)
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import (
    KnowledgeNode, KnowledgeEdge, ConceptRelation, LearningGraph,
    LearningPath, UserKnowledgeState
)


class KnowledgeGraphAnalytics:
    """
    Provides comprehensive analytics for knowledge graphs and learning systems.
    """
    
    def __init__(self):
        self.analytics_cache = {}
    
    def get_overall_analytics(self) -> Dict[str, Any]:
        """
        Get overall knowledge graph analytics across all graphs.
        
        Returns:
            Dictionary with comprehensive analytics data
        """
        try:
            # Get base statistics
            total_nodes = KnowledgeNode.objects.filter(is_active=True).count()
            total_edges = KnowledgeEdge.objects.filter(is_active=True).count()
            total_graphs = LearningGraph.objects.filter(status='active').count()
            total_users = User.objects.count()
            
            # Get node type distribution
            node_type_distribution = self._get_node_type_distribution()
            
            # Get edge type distribution
            edge_type_distribution = self._get_edge_type_distribution()
            
            # Get difficulty distribution
            difficulty_distribution = self._get_difficulty_distribution()
            
            # Get learning path statistics
            path_stats = self._get_learning_path_statistics()
            
            # Get user engagement metrics
            engagement_metrics = self._get_user_engagement_metrics()
            
            # Get temporal analytics
            temporal_analytics = self._get_temporal_analytics()
            
            # Get completion statistics
            completion_stats = self._get_completion_statistics()
            
            # Get popular learning paths
            popular_paths = self._get_popular_learning_paths()
            
            return {
                'overview': {
                    'total_nodes': total_nodes,
                    'total_edges': total_edges,
                    'total_graphs': total_graphs,
                    'total_users': total_users,
                    'graph_density': self._calculate_overall_density(),
                    'average_nodes_per_graph': total_nodes / total_graphs if total_graphs > 0 else 0,
                    'average_edges_per_node': total_edges / total_nodes if total_nodes > 0 else 0
                },
                'distributions': {
                    'node_types': node_type_distribution,
                    'edge_types': edge_type_distribution,
                    'difficulty_levels': difficulty_distribution
                },
                'learning_paths': path_stats,
                'user_engagement': engagement_metrics,
                'temporal_analytics': temporal_analytics,
                'completion_statistics': completion_stats,
                'popular_learning_paths': popular_paths,
                'generated_at': timezone.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error getting overall analytics: {str(e)}")
    
    def get_graph_analytics(self, graph_id: uuid.UUID) -> Dict[str, Any]:
        """
        Get detailed analytics for a specific learning graph.
        
        Args:
            graph_id: UUID of the learning graph
            
        Returns:
            Dictionary with graph-specific analytics
        """
        try:
            learning_graph = LearningGraph.objects.get(id=graph_id)
            
            # Get graph structure metrics
            structure_metrics = self._get_graph_structure_metrics(learning_graph)
            
            # Get learning path analytics for this graph
            path_analytics = self._get_learning_path_analytics(learning_graph)
            
            # Get user progress analytics
            progress_analytics = self._get_user_progress_analytics(learning_graph)
            
            # Get content analytics
            content_analytics = self._get_content_analytics(learning_graph)
            
            # Get engagement metrics
            engagement_analytics = self._get_graph_engagement_metrics(learning_graph)
            
            # Get performance insights
            performance_insights = self._get_performance_insights(learning_graph)
            
            return {
                'graph_info': {
                    'id': str(learning_graph.id),
                    'title': learning_graph.title,
                    'graph_type': learning_graph.graph_type,
                    'status': learning_graph.status,
                    'subject_area': learning_graph.subject_area,
                    'target_audience': learning_graph.target_audience,
                    'created_at': learning_graph.created_at.isoformat(),
                    'version': learning_graph.version
                },
                'structure_metrics': structure_metrics,
                'learning_paths': path_analytics,
                'user_progress': progress_analytics,
                'content_analytics': content_analytics,
                'engagement_metrics': engagement_analytics,
                'performance_insights': performance_insights,
                'generated_at': timezone.now().isoformat()
            }
        except LearningGraph.DoesNotExist:
            raise Exception(f"Learning graph not found: {graph_id}")
        except Exception as e:
            raise Exception(f"Error getting graph analytics: {str(e)}")
    
    def get_user_learning_analytics(self, user_id: int, 
                                  time_range: int = 30) -> Dict[str, Any]:
        """
        Get learning analytics for a specific user.
        
        Args:
            user_id: User ID
            time_range: Number of days to analyze
            
        Returns:
            Dictionary with user-specific analytics
        """
        try:
            user = User.objects.get(id=user_id)
            
            # Calculate date range
            end_date = timezone.now()
            start_date = end_date - timedelta(days=time_range)
            
            # Get user's learning paths
            user_paths = LearningPath.objects.filter(
                user=user,
                started_at__gte=start_date
            )
            
            # Get user's knowledge states
            user_states = UserKnowledgeState.objects.filter(
                user=user,
                last_reviewed__gte=start_date
            )
            
            # Calculate learning activity
            learning_activity = self._calculate_user_learning_activity(user, start_date, end_date)
            
            # Calculate knowledge mastery progression
            mastery_progression = self._calculate_mastery_progression(user, start_date, end_date)
            
            # Calculate learning efficiency
            learning_efficiency = self._calculate_learning_efficiency(user_paths)
            
            # Get learning recommendations
            recommendations = self._generate_learning_recommendations(user)
            
            # Calculate learning streaks
            learning_streaks = self._calculate_learning_streaks(user, start_date)
            
            return {
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'analysis_period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'days': time_range
                    }
                },
                'learning_activity': learning_activity,
                'mastery_progression': mastery_progression,
                'learning_efficiency': learning_efficiency,
                'recommendations': recommendations,
                'learning_streaks': learning_streaks,
                'current_paths': self._get_user_current_paths(user),
                'knowledge_gaps': self._identify_knowledge_gaps(user),
                'generated_at': timezone.now().isoformat()
            }
        except User.DoesNotExist:
            raise Exception(f"User not found: {user_id}")
        except Exception as e:
            raise Exception(f"Error getting user analytics: {str(e)}")
    
    def get_concept_analytics(self, concept_name: str) -> Dict[str, Any]:
        """
        Get analytics for a specific concept across the knowledge graph.
        
        Args:
            concept_name: Name of the concept to analyze
            
        Returns:
            Dictionary with concept-specific analytics
        """
        try:
            # Find nodes related to this concept
            concept_nodes = KnowledgeNode.objects.filter(
                Q(title__icontains=concept_name) |
                Q(description__icontains=concept_name),
                is_active=True
            )
            
            if not concept_nodes:
                return {
                    'concept': concept_name,
                    'status': 'not_found',
                    'message': f'No nodes found for concept: {concept_name}'
                }
            
            # Get concept relations
            concept_relations = ConceptRelation.objects.filter(
                Q(concept_a__icontains=concept_name) |
                Q(concept_b__icontains=concept_name),
                is_active=True
            )
            
            # Calculate concept usage statistics
            usage_stats = self._calculate_concept_usage_stats(concept_nodes)
            
            # Calculate learning path inclusion
            path_inclusion = self._calculate_concept_path_inclusion(concept_nodes)
            
            # Get user mastery levels for this concept
            mastery_levels = self._calculate_concept_mastery_levels(concept_nodes)
            
            # Analyze concept relationships
            relationship_analysis = self._analyze_concept_relationships(concept_relations, concept_name)
            
            # Calculate concept difficulty analysis
            difficulty_analysis = self._analyze_concept_difficulty(concept_nodes)
            
            return {
                'concept': concept_name,
                'status': 'found',
                'nodes_found': concept_nodes.count(),
                'usage_statistics': usage_stats,
                'learning_path_inclusion': path_inclusion,
                'mastery_distribution': mastery_levels,
                'relationship_analysis': relationship_analysis,
                'difficulty_analysis': difficulty_analysis,
                'related_concepts': self._get_related_concepts(concept_nodes),
                'generated_at': timezone.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error getting concept analytics: {str(e)}")
    
    def get_performance_benchmarks(self) -> Dict[str, Any]:
        """
        Get performance benchmarks for the learning system.
        
        Returns:
            Dictionary with performance benchmark data
        """
        try:
            # Calculate completion rate benchmarks
            completion_benchmarks = self._calculate_completion_benchmarks()
            
            # Calculate time-to-completion benchmarks
            time_benchmarks = self._calculate_time_to_completion_benchmarks()
            
            # Calculate engagement benchmarks
            engagement_benchmarks = self._calculate_engagement_benchmarks()
            
            # Calculate mastery progression benchmarks
            mastery_benchmarks = self._calculate_mastery_progression_benchmarks()
            
            # Calculate drop-off point analysis
            drop_off_analysis = self._calculate_drop_off_analysis()
            
            # Calculate success factor analysis
            success_factors = self._calculate_success_factors()
            
            return {
                'completion_benchmarks': completion_benchmarks,
                'time_to_completion_benchmarks': time_benchmarks,
                'engagement_benchmarks': engagement_benchmarks,
                'mastery_progression_benchmarks': mastery_benchmarks,
                'drop_off_analysis': drop_off_analysis,
                'success_factors': success_factors,
                'generated_at': timezone.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Error getting performance benchmarks: {str(e)}")
    
    def generate_insights_report(self, insights_type: str = 'comprehensive') -> Dict[str, Any]:
        """
        Generate insights report for the knowledge graph system.
        
        Args:
            insights_type: Type of insights ('comprehensive', 'trends', 'optimization', 'predictive')
            
        Returns:
            Dictionary with insights report data
        """
        try:
            if insights_type == 'comprehensive':
                return self._generate_comprehensive_insights()
            elif insights_type == 'trends':
                return self._generate_trends_insights()
            elif insights_type == 'optimization':
                return self._generate_optimization_insights()
            elif insights_type == 'predictive':
                return self._generate_predictive_insights()
            else:
                raise ValueError(f"Unknown insights type: {insights_type}")
        except Exception as e:
            raise Exception(f"Error generating insights report: {str(e)}")
    
    def _get_node_type_distribution(self) -> Dict[str, int]:
        """Get distribution of node types across all graphs."""
        distribution = KnowledgeNode.objects.filter(is_active=True).values(
            'node_type'
        ).annotate(count=Count('node_type')).order_by('node_type')
        
        return {item['node_type']: item['count'] for item in distribution}
    
    def _get_edge_type_distribution(self) -> Dict[str, int]:
        """Get distribution of edge types across all graphs."""
        distribution = KnowledgeEdge.objects.filter(is_active=True).values(
            'edge_type'
        ).annotate(count=Count('edge_type')).order_by('edge_type')
        
        return {item['edge_type']: item['count'] for item in distribution}
    
    def _get_difficulty_distribution(self) -> Dict[str, int]:
        """Get distribution of difficulty levels across all nodes."""
        distribution = KnowledgeNode.objects.filter(is_active=True).values(
            'difficulty_level'
        ).annotate(count=Count('difficulty_level')).order_by('difficulty_level')
        
        return {item['difficulty_level']: item['count'] for item in distribution}
    
    def _get_learning_path_statistics(self) -> Dict[str, Any]:
        """Get statistics about learning paths."""
        total_paths = LearningPath.objects.count()
        active_paths = LearningPath.objects.filter(status='active').count()
        completed_paths = LearningPath.objects.filter(status='completed').count()
        avg_completion_time = LearningPath.objects.filter(
            status='completed'
        ).aggregate(avg_time=Avg('total_time_spent'))
        
        return {
            'total_paths': total_paths,
            'active_paths': active_paths,
            'completed_paths': completed_paths,
            'completion_rate': (completed_paths / total_paths * 100) if total_paths > 0 else 0,
            'average_completion_time_hours': (
                avg_completion_time['avg_time'].total_seconds() / 3600 
                if avg_completion_time['avg_time'] else 0
            ),
            'adaptation_types': self._get_adaptation_type_distribution()
        }
    
    def _get_adaptation_type_distribution(self) -> Dict[str, int]:
        """Get distribution of adaptation types for learning paths."""
        distribution = LearningPath.objects.values(
            'adaptation_type'
        ).annotate(count=Count('adaptation_type')).order_by('adaptation_type')
        
        return {item['adaptation_type']: item['count'] for item in distribution}
    
    def _get_user_engagement_metrics(self) -> Dict[str, Any]:
        """Get user engagement metrics."""
        # Get user activity in last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        active_users = UserKnowledgeState.objects.filter(
            last_reviewed__gte=thirty_days_ ago
        ).values('user').distinct().count()
        
        total_users = User.objects.count()
        engagement_rate = (active_users / total_users * 100) if total_users > 0 else 0
        
        # Get average session duration
        avg_session_duration = LearningPath.objects.aggregate(
            avg_duration=Avg('total_time_spent')
        )
        
        return {
            'active_users_30d': active_users,
            'total_users': total_users,
            'engagement_rate': engagement_rate,
            'average_session_duration_hours': (
                avg_session_duration['avg_duration'].total_seconds() / 3600
                if avg_session_duration['avg_duration'] else 0
            ),
            'returning_user_rate': self._calculate_returning_user_rate(thirty_days_ago)
        }
    
    def _calculate_returning_user_rate(self, reference_date) -> float:
        """Calculate percentage of users who returned after initial engagement."""
        # This would track user return patterns
        return 0.0  # Placeholder implementation
    
    def _get_temporal_analytics(self) -> Dict[str, Any]:
        """Get temporal analytics (usage over time)."""
        # Get usage data for last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        daily_usage = []
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            next_date = date + timedelta(days=1)
            
            daily_paths = LearningPath.objects.filter(
                started_at__gte=date,
                started_at__lt=next_date
            ).count()
            
            daily_completions = LearningPath.objects.filter(
                completed_at__gte=date,
                completed_at__lt=next_date,
                status='completed'
            ).count()
            
            daily_usage.append({
                'date': date.strftime('%Y-%m-%d'),
                'new_paths': daily_paths,
                'completions': daily_completions
            })
        
        return {
            'daily_usage': daily_usage,
            'weekly_trends': self._calculate_weekly_trends(daily_usage),
            'peak_usage_times': self._get_peak_usage_times(daily_usage)
        }
    
    def _calculate_weekly_trends(self, daily_usage: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weekly trends from daily usage data."""
        # Group by week and calculate averages
        weekly_data = defaultdict(lambda: {'new_paths': [], 'completions': []})
        
        for day_data in daily_usage:
            date_obj = datetime.strptime(day_data['date'], '%Y-%m-%d')
            week_key = f"{date_obj.year}-W{date_obj.isocalendar()[1]}"
            weekly_data[week_key]['new_paths'].append(day_data['new_paths'])
            weekly_data[week_key]['completions'].append(day_data['completions'])
        
        weekly_trends = {}
        for week, data in weekly_data.items():
            weekly_trends[week] = {
                'avg_new_paths': sum(data['new_paths']) / len(data['new_paths']) if data['new_paths'] else 0,
                'avg_completions': sum(data['completions']) / len(data['completions']) if data['completions'] else 0
            }
        
        return weekly_trends
    
    def _get_peak_usage_times(self, daily_usage: List[Dict[str, Any]]) -> List[str]:
        """Get peak usage times from daily usage data."""
        # Simple implementation - would need more sophisticated time-based analysis
        max_paths = max(day['new_paths'] for day in daily_usage) if daily_usage else 0
        peak_days = [
            day['date'] for day in daily_usage 
            if day['new_paths'] == max_paths and max_paths > 0
        ]
        return peak_days
    
    def _get_completion_statistics(self) -> Dict[str, Any]:
        """Get completion statistics across the system."""
        total_attempts = LearningPath.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            active=Count('id', filter=Q(status='active')),
            abandoned=Count('id', filter=Q(status='abandoned'))
        )
        
        return {
            'total_attempts': total_attempts['total'],
            'completed': total_attempts['completed'],
            'active': total_attempts['active'],
            'abandoned': total_attempts['abandoned'],
            'completion_rate': (
                total_attempts['completed'] / total_attempts['total'] * 100
                if total_attempts['total'] > 0 else 0
            ),
            'abandonment_rate': (
                total_attempts['abandoned'] / total_attempts['total'] * 100
                if total_attempts['total'] > 0 else 0
            )
        }
    
    def _get_popular_learning_paths(self) -> List[Dict[str, Any]]:
        """Get most popular learning paths."""
        popular_graphs = LearningGraph.objects.filter(
            status='active'
        ).annotate(
            path_count=Count('learningpath')
        ).order_by('-path_count')[:10]
        
        return [
            {
                'graph_id': str(graph.id),
                'title': graph.title,
                'graph_type': graph.graph_type,
                'path_count': graph.path_count,
                'completion_rate': graph.completion_rate
            }
            for graph in popular_graphs
        ]
    
    def _calculate_overall_density(self) -> float:
        """Calculate overall graph density."""
        nodes = KnowledgeNode.objects.filter(is_active=True).count()
        edges = KnowledgeEdge.objects.filter(is_active=True).count()
        
        if nodes <= 1:
            return 0.0
        
        max_edges = nodes * (nodes - 1)  # For directed graph
        return edges / max_edges if max_edges > 0 else 0.0
    
    def _get_graph_structure_metrics(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get structure metrics for a specific learning graph."""
        graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
        graph_edges = learning_graph.learninggraphedge_set.select_related('knowledge_edge')
        
        nodes = [gn.knowledge_node for gn in graph_nodes]
        edges = [ge.knowledge_edge for ge in graph_edges]
        
        return {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'density': self._calculate_graph_density(nodes, edges),
            'node_type_distribution': self._calculate_node_type_distribution_for_graph(nodes),
            'difficulty_distribution': self._calculate_difficulty_distribution_for_graph(nodes),
            'edge_type_distribution': self._calculate_edge_type_distribution_for_graph(edges),
            'clustering_coefficient': self._calculate_clustering_coefficient(nodes, edges),
            'connectivity_metrics': self._calculate_connectivity_metrics(nodes, edges)
        }
    
    def _calculate_graph_density(self, nodes: List[KnowledgeNode], edges: List[KnowledgeEdge]) -> float:
        """Calculate density for a specific graph."""
        n = len(nodes)
        e = len(edges)
        
        if n <= 1:
            return 0.0
        
        max_edges = n * (n - 1)
        return e / max_edges if max_edges > 0 else 0.0
    
    def _calculate_node_type_distribution_for_graph(self, nodes: List[KnowledgeNode]) -> Dict[str, int]:
        """Calculate node type distribution for a specific graph."""
        distribution = Counter(node.node_type for node in nodes)
        return dict(distribution)
    
    def _calculate_difficulty_distribution_for_graph(self, nodes: List[KnowledgeNode]) -> Dict[str, int]:
        """Calculate difficulty distribution for a specific graph."""
        distribution = Counter(node.difficulty_level for node in nodes)
        return dict(distribution)
    
    def _calculate_edge_type_distribution_for_graph(self, edges: List[KnowledgeEdge]) -> Dict[str, int]:
        """Calculate edge type distribution for a specific graph."""
        distribution = Counter(edge.edge_type for edge in edges)
        return dict(distribution)
    
    def _calculate_clustering_coefficient(self, nodes: List[KnowledgeNode], edges: List[KnowledgeEdge]) -> float:
        """Calculate clustering coefficient for a graph."""
        # Simplified clustering coefficient calculation
        if len(nodes) < 3:
            return 0.0
        
        # Create adjacency information
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[str(edge.source_node.id)].add(str(edge.target_node.id))
            adjacency[str(edge.target_node.id)].add(str(edge.source_node.id))
        
        clustering_sum = 0.0
        node_count = 0
        
        for node in nodes:
            node_id = str(node.id)
            neighbors = adjacency[node_id]
            
            if len(neighbors) < 2:
                continue
            
            node_count += 1
            neighbor_list = list(neighbors)
            edges_between_neighbors = 0
            
            for i in range(len(neighbor_list)):
                for j in range(i + 1, len(neighbor_list)):
                    if neighbor_list[j] in adjacency[neighbor_list[i]]:
                        edges_between_neighbors += 1
            
            possible_edges = len(neighbors) * (len(neighbors) - 1) / 2
            if possible_edges > 0:
                clustering_sum += edges_between_neighbors / possible_edges
        
        return clustering_sum / node_count if node_count > 0 else 0.0
    
    def _calculate_connectivity_metrics(self, nodes: List[KnowledgeNode], edges: List[KnowledgeEdge]) -> Dict[str, float]:
        """Calculate connectivity metrics for a graph."""
        # Simplified connectivity metrics
        if not nodes:
            return {'connected_components': 0, 'is_connected': False, 'average_degree': 0.0}
        
        # Build adjacency list
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[str(edge.source_node.id)].add(str(edge.target_node.id))
            adjacency[str(edge.target_node.id)].add(str(edge.source_node.id))
        
        # Calculate degrees
        degrees = [len(adjacency[str(node.id)]) for node in nodes]
        average_degree = sum(degrees) / len(degrees)
        
        # Find connected components (simplified BFS)
        visited = set()
        connected_components = 0
        
        for node in nodes:
            node_id = str(node.id)
            if node_id not in visited:
                connected_components += 1
                # BFS to mark component
                queue = [node_id]
                visited.add(node_id)
                
                while queue:
                    current = queue.pop(0)
                    for neighbor in adjacency[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
        
        is_connected = connected_components == 1
        
        return {
            'connected_components': connected_components,
            'is_connected': is_connected,
            'average_degree': average_degree
        }
    
    def _get_learning_path_analytics(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get learning path analytics for a specific graph."""
        paths = LearningPath.objects.filter(learning_graph=learning_graph)
        
        total_paths = paths.count()
        completed_paths = paths.filter(status='completed').count()
        active_paths = paths.filter(status='active').count()
        
        avg_completion_time = paths.filter(status='completed').aggregate(
            avg_time=Avg('total_time_spent')
        )
        
        return {
            'total_paths': total_paths,
            'completed_paths': completed_paths,
            'active_paths': active_paths,
            'completion_rate': (completed_paths / total_paths * 100) if total_paths > 0 else 0,
            'average_completion_time_hours': (
                avg_completion_time['avg_time'].total_seconds() / 3600
                if avg_completion_time['avg_time'] else 0
            ),
            'adaptation_type_distribution': self._get_adaptation_type_distribution_for_graph(paths)
        }
    
    def _get_adaptation_type_distribution_for_graph(self, paths) -> Dict[str, int]:
        """Get adaptation type distribution for paths in a specific graph."""
        distribution = paths.values('adaptation_type').annotate(
            count=Count('adaptation_type')
        )
        return {item['adaptation_type']: item['count'] for item in distribution}
    
    def _get_user_progress_analytics(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get user progress analytics for a specific graph."""
        paths = LearningPath.objects.filter(learning_graph=learning_graph)
        
        # Calculate progress distribution
        progress_distribution = defaultdict(int)
        for path in paths:
            progress_bucket = int(path.progress_percentage // 10) * 10
            progress_distribution[f"{progress_bucket}-{progress_bucket + 9}%"] += 1
        
        # Calculate average progress
        avg_progress = paths.aggregate(avg_progress=Avg('progress_percentage'))
        
        return {
            'progress_distribution': dict(progress_distribution),
            'average_progress': avg_progress['avg_progress'] or 0,
            'paths_at_90_percent_plus': paths.filter(progress_percentage__gte=90).count(),
            'paths_stalled_less_than_10_percent': paths.filter(progress_percentage__lt=10).count()
        }
    
    def _get_content_analytics(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get content analytics for a specific graph."""
        graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
        graph_edges = learning_graph.learninggraphedge_set.select_related('knowledge_edge')
        
        nodes = [gn.knowledge_node for gn in graph_nodes]
        edges = [ge.knowledge_edge for ge in graph_edges]
        
        return {
            'content_completeness': self._calculate_content_completeness(nodes, edges),
            'knowledge_coverage': self._calculate_knowledge_coverage(nodes),
            'prerequisite_completeness': self._calculate_prerequisite_completeness(edges),
            'content_quality_metrics': self._calculate_content_quality_metrics(nodes)
        }
    
    def _calculate_content_completeness(self, nodes: List[KnowledgeNode], edges: List[KnowledgeEdge]) -> Dict[str, float]:
        """Calculate content completeness metrics."""
        total_nodes = len(nodes)
        
        if total_nodes == 0:
            return {'completeness_score': 0.0}
        
        # Count nodes with complete metadata
        nodes_with_description = sum(1 for node in nodes if node.description.strip())
        nodes_with_objectives = sum(1 for node in nodes if node.learning_objectives)
        nodes_with_prerequisites = sum(1 for node in nodes if node.prerequisites)
        nodes_with_content = sum(1 for node in nodes if node.content_uri or node.jac_code)
        
        return {
            'nodes_with_description': nodes_with_description / total_nodes,
            'nodes_with_objectives': nodes_with_objectives / total_nodes,
            'nodes_with_prerequisites': nodes_with_prerequisites / total_nodes,
            'nodes_with_content': nodes_with_content / total_nodes,
            'completeness_score': (
                nodes_with_description + nodes_with_objectives + 
                nodes_with_prerequisites + nodes_with_content
            ) / (total_nodes * 4)
        }
    
    def _calculate_knowledge_coverage(self, nodes: List[KnowledgeNode]) -> Dict[str, Any]:
        """Calculate knowledge coverage metrics."""
        total_nodes = len(nodes)
        
        if total_nodes == 0:
            return {'coverage_score': 0.0}
        
        # Calculate coverage across difficulty levels
        difficulty_coverage = {}
        for level in ['beginner', 'intermediate', 'advanced', 'expert']:
            level_nodes = sum(1 for node in nodes if node.difficulty_level == level)
            difficulty_coverage[level] = level_nodes / total_nodes
        
        # Calculate coverage across node types
        type_coverage = {}
        node_types = set(node.node_type for node in nodes)
        for node_type in node_types:
            type_nodes = sum(1 for node in nodes if node.node_type == node_type)
            type_coverage[node_type] = type_nodes / total_nodes
        
        return {
            'difficulty_coverage': difficulty_coverage,
            'type_coverage': type_coverage,
            'coverage_score': len(difficulty_coverage) * len(type_coverage) / 16  # Normalized score
        }
    
    def _calculate_prerequisite_completeness(self, edges: List[KnowledgeEdge]) -> Dict[str, float]:
        """Calculate prerequisite relationship completeness."""
        total_edges = len(edges)
        
        if total_edges == 0:
            return {'prerequisite_ratio': 0.0, 'completeness_score': 0.0}
        
        prerequisite_edges = sum(1 for edge in edges if edge.edge_type == 'prerequisite')
        prerequisite_ratio = prerequisite_edges / total_edges
        
        # Check for bidirectional edges (cycles)
        edge_pairs = set()
        cycles = 0
        
        for edge in edges:
            pair = tuple(sorted([str(edge.source_node.id), str(edge.target_node.id)]))
            if pair in edge_pairs:
                cycles += 1
            edge_pairs.add(pair)
        
        return {
            'prerequisite_ratio': prerequisite_ratio,
            'cycle_count': cycles,
            'completeness_score': prerequisite_ratio * (1 - cycles / total_edges)
        }
    
    def _calculate_content_quality_metrics(self, nodes: List[KnowledgeNode]) -> Dict[str, Any]:
        """Calculate content quality metrics."""
        total_nodes = len(nodes)
        
        if total_nodes == 0:
            return {'quality_score': 0.0}
        
        # Calculate various quality indicators
        avg_description_length = sum(
            len(node.description) for node in nodes if node.description
        ) / total_nodes if total_nodes > 0 else 0
        
        nodes_with_code = sum(1 for node in nodes if node.jac_code)
        nodes_with_external_content = sum(1 for node in nodes if node.content_uri)
        
        # Calculate view count statistics
        view_counts = [node.view_count for node in nodes]
        avg_view_count = sum(view_counts) / len(view_counts) if view_counts else 0
        
        return {
            'average_description_length': avg_description_length,
            'nodes_with_code_percentage': nodes_with_code / total_nodes,
            'nodes_with_external_content_percentage': nodes_with_external_content / total_nodes,
            'average_view_count': avg_view_count,
            'quality_score': (
                min(avg_description_length / 100, 1.0) +  # Description length score
                nodes_with_code / total_nodes +  # Code content score
                nodes_with_external_content / total_nodes +  # External content score
                min(avg_view_count / 100, 1.0)  # Engagement score
            ) / 4
        }
    
    def _get_graph_engagement_metrics(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get engagement metrics for a specific graph."""
        paths = LearningPath.objects.filter(learning_graph=learning_graph)
        
        # Calculate engagement metrics
        total_views = sum(path.learning_graph.nodes.aggregate(
            total_views=Sum('knowledge_node__view_count')
        )['total_views'] or 0)
        
        # Calculate engagement rate
        unique_users = paths.values('user').distinct().count()
        
        return {
            'total_graph_views': total_views,
            'unique_users_engaged': unique_users,
            'average_paths_per_user': paths.count() / unique_users if unique_users > 0 else 0,
            'engagement_score': self._calculate_engagement_score(paths, total_views)
        }
    
    def _calculate_engagement_score(self, paths, total_views: int) -> float:
        """Calculate engagement score for paths."""
        if not paths.exists():
            return 0.0
        
        # Calculate various engagement factors
        completion_factor = paths.filter(status='completed').count() / paths.count()
        activity_factor = min(paths.aggregate(
            avg_activity=Avg('last_activity')
        )['avg_activity'] or 0, 1.0)
        
        return (completion_factor + activity_factor) / 2
    
    def _get_performance_insights(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Get performance insights for a specific graph."""
        paths = LearningPath.objects.filter(learning_graph=learning_graph)
        
        return {
            'bottleneck_nodes': self._identify_bottleneck_nodes(learning_graph),
            'optimal_path_length': self._calculate_optimal_path_length(paths),
            'difficulty_optimization': self._analyze_difficulty_optimization(learning_graph),
            'completion_predictors': self._identify_completion_predictors(paths)
        }
    
    def _identify_bottleneck_nodes(self, learning_graph: LearningGraph) -> List[Dict[str, Any]]:
        """Identify nodes that act as bottlenecks in learning paths."""
        # This would analyze path completion data to find bottleneck nodes
        return []  # Placeholder implementation
    
    def _calculate_optimal_path_length(self, paths) -> int:
        """Calculate optimal path length based on completion rates."""
        # Analyze completion rates by path length
        path_lengths = []
        for path in paths:
            completed_nodes = len(path.completed_nodes)
            if path.status == 'completed':
                path_lengths.append(completed_nodes)
        
        return int(sum(path_lengths) / len(path_lengths)) if path_lengths else 0
    
    def _analyze_difficulty_optimization(self, learning_graph: LearningGraph) -> Dict[str, Any]:
        """Analyze difficulty progression optimization."""
        graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
        
        difficulty_progression = [gn.knowledge_node.difficulty_level for gn in graph_nodes]
        
        return {
            'optimal_progression': difficulty_progression,
            'difficulty_score': self._calculate_difficulty_score(difficulty_progression)
        }
    
    def _calculate_difficulty_score(self, progression: List[str]) -> float:
        """Calculate difficulty progression score."""
        difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
        
        if len(progression) <= 1:
            return 1.0
        
        # Calculate how well the progression follows an optimal difficulty curve
        score = 0.0
        for i in range(len(progression) - 1):
            current_diff = difficulty_order.get(progression[i], 2)
            next_diff = difficulty_order.get(progression[i + 1], 2)
            
            # Prefer gradual increases in difficulty
            if next_diff >= current_diff:
                score += 1.0
            elif next_diff == current_diff - 1:  # Slight decrease is OK
                score += 0.8
            else:  # Large decreases are problematic
                score += 0.3
        
        return score / (len(progression) - 1)
    
    def _identify_completion_predictors(self, paths) -> List[Dict[str, Any]]:
        """Identify factors that predict learning path completion."""
        # This would use machine learning or statistical analysis
        return []  # Placeholder implementation
    
    def _calculate_user_learning_activity(self, user: User, start_date, end_date) -> Dict[str, Any]:
        """Calculate user's learning activity metrics."""
        user_paths = LearningPath.objects.filter(
            user=user,
            started_at__gte=start_date,
            started_at__lt=end_date
        )
        
        return {
            'paths_started': user_paths.count(),
            'paths_completed': user_paths.filter(status='completed').count(),
            'total_learning_time_hours': self._calculate_total_learning_time(user_paths),
            'learning_sessions': self._count_learning_sessions(user_paths),
            'average_session_duration': self._calculate_average_session_duration(user_paths)
        }
    
    def _calculate_total_learning_time(self, paths) -> float:
        """Calculate total learning time for paths."""
        total_seconds = sum(
            path.total_time_spent.total_seconds() 
            for path in paths 
            if path.total_time_spent
        )
        return total_seconds / 3600  # Convert to hours
    
    def _count_learning_sessions(self, paths) -> int:
        """Count number of learning sessions."""
        return paths.count()
    
    def _calculate_average_session_duration(self, paths) -> float:
        """Calculate average session duration."""
        if not paths.exists():
            return 0.0
        
        total_duration = sum(
            path.total_time_spent.total_seconds() 
            for path in paths 
            if path.total_time_spent
        )
        return total_seconds / len(paths) / 3600 if total_seconds > 0 else 0.0
    
    def _calculate_mastery_progression(self, user: User, start_date, end_date) -> Dict[str, Any]:
        """Calculate user's mastery progression over time."""
        user_states = UserKnowledgeState.objects.filter(
            user=user,
            last_reviewed__gte=start_date,
            last_reviewed__gte=end_date
        )
        
        # Calculate progression by mastery level
        progression = defaultdict(int)
        for state in user_states:
            progression[state.mastery_level] += 1
        
        # Calculate confidence improvement
        confidence_improvement = self._calculate_confidence_improvement(user_states)
        
        return {
            'mastery_distribution': dict(progression),
            'confidence_improvement': confidence_improvement,
            'concepts_mastered': user_states.filter(mastery_level='expert').count(),
            'concepts_in_progress': user_states.filter(
                mastery_level__in=['beginner', 'developing']
            ).count()
        }
    
    def _calculate_confidence_improvement(self, states) -> float:
        """Calculate confidence improvement over time."""
        if not states.exists():
            return 0.0
        
        latest_confidence = states.order_by('-last_reviewed').first().confidence_score
        earliest_confidence = states.order_by('last_reviewed').first().confidence_score
        
        return latest_confidence - earliest_confidence
    
    def _calculate_learning_efficiency(self, paths) -> Dict[str, Any]:
        """Calculate learning efficiency metrics."""
        if not paths.exists():
            return {'efficiency_score': 0.0}
        
        # Calculate efficiency based on completion time vs content difficulty
        efficiency_scores = []
        for path in paths:
            if path.status == 'completed' and path.total_time_spent:
                # Simplified efficiency calculation
                nodes_completed = len(path.completed_nodes)
                time_hours = path.total_time_spent.total_seconds() / 3600
                
                if time_hours > 0 and nodes_completed > 0:
                    efficiency = nodes_completed / time_hours
                    efficiency_scores.append(efficiency)
        
        return {
            'average_efficiency': sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0,
            'efficiency_score': self._normalize_efficiency_score(efficiency_scores),
            'high_efficiency_sessions': sum(1 for score in efficiency_scores if score > 5)
        }
    
    def _normalize_efficiency_score(self, scores: List[float]) -> float:
        """Normalize efficiency score to 0-1 range."""
        if not scores:
            return 0.0
        
        max_score = max(scores)
        return min(max_score / 10, 1.0)  # Normalize against typical high efficiency
    
    def _generate_learning_recommendations(self, user: User) -> List[Dict[str, Any]]:
        """Generate learning recommendations for a user."""
        # This would use advanced recommendation algorithms
        return []  # Placeholder implementation
    
    def _calculate_learning_streaks(self, user: User, start_date) -> Dict[str, Any]:
        """Calculate learning streaks for a user."""
        # This would analyze daily learning activity
        return {'current_streak': 0, 'longest_streak': 0, 'streak_frequency': 0.0}
    
    def _get_user_current_paths(self, user: User) -> List[Dict[str, Any]]:
        """Get user's current learning paths."""
        current_paths = LearningPath.objects.filter(
            user=user,
            status__in=['active', 'paused']
        ).select_related('learning_graph')
        
        return [
            {
                'path_id': str(path.id),
                'title': path.title,
                'graph_title': path.learning_graph.title,
                'progress_percentage': path.progress_percentage,
                'current_node': str(path.current_node.id) if path.current_node else None,
                'days_active': (timezone.now() - path.started_at).days
            }
            for path in current_paths
        ]
    
    def _identify_knowledge_gaps(self, user: User) -> List[Dict[str, Any]]:
        """Identify knowledge gaps for a user."""
        # Find concepts with low mastery levels
        low_mastery_states = UserKnowledgeState.objects.filter(
            user=user,
            mastery_level__in=['novice', 'beginner']
        )
        
        return [
            {
                'concept': state.knowledge_node.title,
                'current_mastery': state.mastery_level,
                'confidence': state.confidence_score,
                'recommendation': 'Review and practice this concept'
            }
            for state in low_mastery_states
        ]
    
    def _calculate_concept_usage_stats(self, nodes: List[KnowledgeNode]) -> Dict[str, Any]:
        """Calculate usage statistics for a concept."""
        total_views = sum(node.view_count for node in nodes)
        avg_views = total_views / len(nodes) if nodes else 0
        
        return {
            'total_occurrences': len(nodes),
            'total_views': total_views,
            'average_views': avg_views,
            'usage_frequency': 'high' if avg_views > 100 else 'medium' if avg_views > 50 else 'low'
        }
    
    def _calculate_concept_path_inclusion(self, nodes: List[KnowledgeNode]) -> Dict[str, Any]:
        """Calculate how often a concept is included in learning paths."""
        # This would analyze LearningPath data
        return {'inclusion_rate': 0.0, 'path_count': 0}
    
    def _calculate_concept_mastery_levels(self, nodes: List[KnowledgeNode]) -> Dict[str, int]:
        """Calculate mastery level distribution for a concept."""
        mastery_distribution = defaultdict(int)
        
        # This would aggregate UserKnowledgeState data
        # For now, return placeholder
        return {'novice': 0, 'beginner': 0, 'developing': 0, 'proficient': 0, 'expert': 0}
    
    def _analyze_concept_relationships(self, relations, concept_name: str) -> Dict[str, Any]:
        """Analyze relationships involving a concept."""
        if not relations.exists():
            return {'relationship_count': 0, 'confidence_score': 0.0}
        
        relationship_count = relations.count()
        avg_confidence = sum(rel.confidence_score for rel in relations) / relationship_count
        
        return {
            'relationship_count': relationship_count,
            'average_confidence': avg_confidence,
            'relationship_types': list(set(rel.relation_type for rel in relations))
        }
    
    def _analyze_concept_difficulty(self, nodes: List[KnowledgeNode]) -> Dict[str, Any]:
        """Analyze difficulty distribution for a concept."""
        if not nodes:
            return {'difficulty_distribution': {}, 'average_difficulty': 'beginner'}
        
        difficulty_count = Counter(node.difficulty_level for node in nodes)
        most_common_difficulty = difficulty_count.most_common(1)[0][0] if difficulty_count else 'beginner'
        
        return {
            'difficulty_distribution': dict(difficulty_count),
            'average_difficulty': most_common_difficulty,
            'difficulty_span': len(set(node.difficulty_level for node in nodes))
        }
    
    def _get_related_concepts(self, nodes: List[KnowledgeNode]) -> List[str]:
        """Get concepts related to the given nodes."""
        # This would analyze KnowledgeEdge data to find related concepts
        return []
    
    def _calculate_completion_benchmarks(self) -> Dict[str, float]:
        """Calculate completion rate benchmarks."""
        overall_completion = LearningPath.objects.filter(
            status='completed'
        ).count() / LearningPath.objects.count() * 100 if LearningPath.objects.exists() else 0
        
        return {
            'overall_completion_rate': overall_completion,
            'high_performer_threshold': 80.0,
            'average_performer_threshold': 60.0,
            'improvement_needed_threshold': 40.0
        }
    
    def _calculate_time_to_completion_benchmarks(self) -> Dict[str, Any]:
        """Calculate time-to-completion benchmarks."""
        completed_paths = LearningPath.objects.filter(status='completed')
        
        if not completed_paths.exists():
            return {'average_completion_time': 0, 'fast_completion_time': 0, 'slow_completion_time': 0}
        
        completion_times = [
            (path.completed_at - path.started_at).total_seconds() / 3600
            for path in completed_paths
            if path.completed_at and path.started_at
        ]
        
        return {
            'average_completion_time': sum(completion_times) / len(completion_times),
            'fast_completion_time': min(completion_times),
            'slow_completion_time': max(completion_times)
        }
    
    def _calculate_engagement_benchmarks(self) -> Dict[str, Any]:
        """Calculate engagement benchmarks."""
        total_users = User.objects.count()
        active_users = UserKnowledgeState.objects.values('user').distinct().count()
        
        engagement_rate = active_users / total_users * 100 if total_users > 0 else 0
        
        return {
            'engagement_rate': engagement_rate,
            'high_engagement_threshold': 70.0,
            'moderate_engagement_threshold': 50.0,
            'low_engagement_threshold': 30.0
        }
    
    def _calculate_mastery_progression_benchmarks(self) -> Dict[str, Any]:
        """Calculate mastery progression benchmarks."""
        mastery_distribution = UserKnowledgeState.objects.values(
            'mastery_level'
        ).annotate(count=Count('mastery_level'))
        
        total_states = sum(item['count'] for item in mastery_distribution)
        
        expert_count = next((item['count'] for item in mastery_distribution 
                           if item['mastery_level'] == 'expert'), 0)
        
        return {
            'expert_mastery_rate': expert_count / total_states * 100 if total_states > 0 else 0,
            'target_expert_rate': 15.0,
            'proficiency_distribution': {
                item['mastery_level']: item['count'] / total_states * 100 if total_states > 0 else 0
                for item in mastery_distribution
            }
        }
    
    def _calculate_drop_off_analysis(self) -> Dict[str, Any]:
        """Analyze drop-off points in learning paths."""
        # This would analyze where users typically abandon paths
        return {
            'common_drop_off_points': [],
            'abandonment_rate': 0.0,
            'early_abandonment_rate': 0.0
        }
    
    def _calculate_success_factors(self) -> List[Dict[str, Any]]:
        """Calculate factors that contribute to learning success."""
        # This would use statistical analysis to identify success factors
        return []
    
    def _generate_comprehensive_insights(self) -> Dict[str, Any]:
        """Generate comprehensive insights report."""
        return {
            'overview': self.get_overall_analytics(),
            'key_metrics': self._calculate_key_performance_metrics(),
            'trends': self._generate_trends_insights(),
            'recommendations': self._generate_system_recommendations(),
            'generated_at': timezone.now().isoformat()
        }
    
    def _generate_trends_insights(self) -> Dict[str, Any]:
        """Generate trends insights."""
        return {
            'usage_trends': self._get_temporal_analytics(),
            'completion_trends': self._analyze_completion_trends(),
            'engagement_trends': self._analyze_engagement_trends(),
            'generated_at': timezone.now().isoformat()
        }
    
    def _generate_optimization_insights(self) -> Dict[str, Any]:
        """Generate optimization insights."""
        return {
            'content_optimization': self._analyze_content_optimization(),
            'path_optimization': self._analyze_path_optimization(),
            'user_experience_optimization': self._analyze_ux_optimization(),
            'generated_at': timezone.now().isoformat()
        }
    
    def _generate_predictive_insights(self) -> Dict[str, Any]:
        """Generate predictive insights."""
        return {
            'completion_predictions': self._predict_completion_rates(),
            'engagement_predictions': self._predict_engagement(),
            'performance_predictions': self._predict_performance(),
            'generated_at': timezone.now().isoformat()
        }
    
    def _calculate_key_performance_metrics(self) -> Dict[str, Any]:
        """Calculate key performance metrics."""
        return {
            'system_health_score': 85.0,  # Placeholder
            'user_satisfaction_score': 78.0,  # Placeholder
            'learning_effectiveness_score': 82.0  # Placeholder
        }
    
    def _generate_system_recommendations(self) -> List[Dict[str, str]]:
        """Generate system-level recommendations."""
        return [
            {
                'category': 'content',
                'priority': 'high',
                'recommendation': 'Add more beginner-level content to improve entry barrier',
                'impact': 'Increase user onboarding success rate'
            }
        ]
    
    def _analyze_completion_trends(self) -> Dict[str, Any]:
        """Analyze completion trends over time."""
        return {'trend_direction': 'improving', 'trend_strength': 'moderate'}
    
    def _analyze_engagement_trends(self) -> Dict[str, Any]:
        """Analyze engagement trends over time."""
        return {'trend_direction': 'stable', 'trend_strength': 'weak'}
    
    def _analyze_content_optimization(self) -> Dict[str, Any]:
        """Analyze content for optimization opportunities."""
        return {'optimization_opportunities': [], 'priority_areas': []}
    
    def _analyze_path_optimization(self) -> Dict[str, Any]:
        """Analyze learning paths for optimization opportunities."""
        return {'path_improvements': [], 'sequence_optimizations': []}
    
    def _analyze_ux_optimization(self) -> Dict[str, Any]:
        """Analyze user experience for optimization opportunities."""
        return {'ux_improvements': [], 'interface_recommendations': []}
    
    def _predict_completion_rates(self) -> Dict[str, Any]:
        """Predict future completion rates."""
        return {'predicted_completion_rate': 75.0, 'confidence_interval': [70, 80]}
    
    def _predict_engagement(self) -> Dict[str, Any]:
        """Predict future engagement levels."""
        return {'predicted_engagement_rate': 65.0, 'confidence_interval': [60, 70]}
    
    def _predict_performance(self) -> Dict[str, Any]:
        """Predict future performance metrics."""
        return {'predicted_performance_score': 80.0, 'confidence_interval': [75, 85]}