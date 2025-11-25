"""
Graph Algorithms for Knowledge Graph Processing.

This module provides algorithms for analyzing knowledge graphs, finding paths,
and implementing Object-Spatial Programming (OSP) concepts.
"""

import uuid
import json
import networkx as nx
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, deque
from django.db.models import Q, Count, Avg
from ..models import KnowledgeNode, KnowledgeEdge, LearningGraph, LearningPath, UserKnowledgeState


class GraphAnalyzer:
    """
    Analyzes knowledge graphs and provides insights about structure and connectivity.
    """
    
    def __init__(self):
        self.graph_cache = {}
    
    def build_networkx_graph(self, nodes_queryset=None, edges_queryset=None) -> nx.DiGraph:
        """
        Build a NetworkX directed graph from Django models.
        
        Args:
            nodes_queryset: QuerySet of KnowledgeNode instances
            edges_queryset: QuerySet of KnowledgeEdge instances
            
        Returns:
            NetworkX DiGraph representing the knowledge graph
        """
        graph = nx.DiGraph()
        
        # Get nodes if not provided
        if nodes_queryset is None:
            nodes_queryset = KnowledgeNode.objects.filter(is_active=True)
        
        # Get edges if not provided
        if edges_queryset is None:
            edges_queryset = KnowledgeEdge.objects.filter(is_active=True)
        
        # Add nodes
        for node in nodes_queryset:
            graph.add_node(
                str(node.id),
                title=node.title,
                node_type=node.node_type,
                difficulty_level=node.difficulty_level,
                x_position=node.x_position,
                y_position=node.y_position,
                z_position=node.z_position,
                width=node.width,
                height=node.height,
                content_uri=node.content_uri,
                jac_code=node.jac_code,
                view_count=node.view_count
            )
        
        # Add edges
        for edge in edges_queryset:
            if (str(edge.source_node.id) in graph.nodes and 
                str(edge.target_node.id) in graph.nodes):
                graph.add_edge(
                    str(edge.source_node.id),
                    str(edge.target_node.id),
                    edge_type=edge.edge_type,
                    strength=edge.strength,
                    edge_weight=edge.edge_weight,
                    traversal_count=edge.traversal_count,
                    curve_points=edge.curve_points,
                    description=edge.description
                )
        
        return graph
    
    def get_complete_graph(self) -> Dict[str, Any]:
        """
        Get complete knowledge graph data for frontend visualization.
        
        Returns:
            Dictionary containing nodes, edges, and metadata
        """
        try:
            # Get all active nodes and edges
            nodes = KnowledgeNode.objects.filter(is_active=True).prefetch_related(
                'outgoing_edges', 'incoming_edges'
            )
            edges = KnowledgeEdge.objects.filter(is_active=True)
            
            # Build NetworkX graph
            nx_graph = self.build_networkx_graph(nodes, edges)
            
            # Calculate graph statistics
            stats = self._calculate_graph_statistics(nx_graph)
            
            # Serialize data for frontend
            node_serializer = self._get_node_serializer()
            edge_serializer = self._get_edge_serializer()
            
            return {
                'nodes': node_serializer(nodes, many=True).data,
                'edges': edge_serializer(edges, many=True).data,
                'meta': {
                    'total_nodes': len(nodes),
                    'total_edges': len(edges),
                    'statistics': stats,
                    'generated_at': timezone.now().isoformat()
                }
            }
        except Exception as e:
            raise Exception(f"Error getting complete graph: {str(e)}")
    
    def get_topic_graph(self, topic: str) -> Dict[str, Any]:
        """
        Get knowledge graph filtered by topic.
        
        Args:
            topic: Topic name to filter by
            
        Returns:
            Dictionary containing topic-specific graph data
        """
        try:
            # Filter nodes by topic (case-insensitive search in title, description, or content)
            nodes = KnowledgeNode.objects.filter(
                Q(title__icontains=topic) |
                Q(description__icontains=topic) |
                Q(content_uri__icontains=topic),
                is_active=True
            )
            
            node_ids = set(node.id for node in nodes)
            
            # Get edges that connect these nodes
            edges = KnowledgeEdge.objects.filter(
                (Q(source_node_id__in=node_ids) & Q(target_node_id__in=node_ids)) |
                Q(source_node_id__in=node_ids) |
                Q(target_node_id__in=node_ids),
                is_active=True
            )
            
            # Build filtered NetworkX graph
            nx_graph = self.build_networkx_graph(nodes, edges)
            
            # Calculate topic-specific statistics
            stats = self._calculate_topic_statistics(nx_graph, topic)
            
            return {
                'topic': topic,
                'nodes': nodes,
                'edges': edges,
                'statistics': stats
            }
        except Exception as e:
            raise Exception(f"Error getting topic graph: {str(e)}")
    
    def search_nodes(self, query: str, node_types: List[str] = None, 
                    difficulty_levels: List[str] = None, max_results: int = 50) -> List[KnowledgeNode]:
        """
        Search knowledge nodes with advanced filters.
        
        Args:
            query: Search query string
            node_types: Optional list of node types to filter by
            difficulty_levels: Optional list of difficulty levels to filter by
            max_results: Maximum number of results to return
            
        Returns:
            List of matching KnowledgeNode instances
        """
        try:
            queryset = KnowledgeNode.objects.filter(is_active=True)
            
            # Text search
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(learning_objectives__icontains=query) |
                Q(jac_code__icontains=query)
            )
            
            # Apply filters
            if node_types:
                queryset = queryset.filter(node_type__in=node_types)
            
            if difficulty_levels:
                queryset = queryset.filter(difficulty_level__in=difficulty_levels)
            
            # Order by relevance (simple scoring based on title matches)
            queryset = queryset.extra(
                select={'relevance_score': 
                    "CASE WHEN title ILIKE %s THEN 3 "
                    "WHEN description ILIKE %s THEN 2 "
                    "ELSE 1 END"},
                select_params=[f'%{query}%', f'%{query}%']
            ).order_by('-relevance_score', '-view_count')
            
            return queryset[:max_results]
        except Exception as e:
            raise Exception(f"Error searching nodes: {str(e)}")
    
    def analyze_edge_paths(self, edge_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Analyze all paths that include a specific edge.
        
        Args:
            edge_id: UUID of the edge to analyze
            
        Returns:
            List of path information dictionaries
        """
        try:
            edge = KnowledgeEdge.objects.get(id=edge_id, is_active=True)
            
            # Build NetworkX graph
            nx_graph = self.build_networkx_graph()
            
            paths = []
            
            # Find all simple paths that include this edge
            try:
                # Get all paths from source to target
                all_paths = list(nx.all_simple_paths(
                    nx_graph, 
                    str(edge.source_node.id), 
                    str(edge.target_node.id),
                    cutoff=10  # Limit path length
                ))
                
                for path in all_paths:
                    path_info = {
                        'path_length': len(path),
                        'nodes': path,
                        'includes_target_edge': True,
                        'path_nodes': []
                    }
                    
                    # Get node details for this path
                    for node_id in path:
                        try:
                            node = KnowledgeNode.objects.get(id=node_id)
                            path_info['path_nodes'].append({
                                'id': str(node.id),
                                'title': node.title,
                                'node_type': node.node_type,
                                'difficulty_level': node.difficulty_level
                            })
                        except KnowledgeNode.DoesNotExist:
                            continue
                    
                    paths.append(path_info)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                # No paths found
                pass
            
            return paths
        except KnowledgeEdge.DoesNotExist:
            raise Exception(f"Edge not found: {edge_id}")
        except Exception as e:
            raise Exception(f"Error analyzing edge paths: {str(e)}")
    
    def _calculate_graph_statistics(self, graph: nx.DiGraph) -> Dict[str, Any]:
        """Calculate comprehensive graph statistics."""
        if len(graph.nodes) == 0:
            return {
                'node_count': 0,
                'edge_count': 0,
                'density': 0.0,
                'connected_components': 0,
                'average_degree': 0.0
            }
        
        stats = {
            'node_count': len(graph.nodes),
            'edge_count': len(graph.edges),
            'density': nx.density(graph),
            'connected_components': nx.number_weakly_connected_components(graph),
            'average_degree': sum(dict(graph.degree()).values()) / len(graph.nodes),
            'is_connected': nx.is_weakly_connected(graph),
            'diameter': None,
            'average_shortest_path_length': None
        }
        
        # Calculate diameter and average shortest path length if graph is connected
        if stats['is_connected'] and len(graph.nodes) > 1:
            try:
                stats['diameter'] = nx.diameter(graph.to_undirected())
                stats['average_shortest_path_length'] = nx.average_shortest_path_length(graph.to_undirected())
            except (nx.NetworkXError, nx.NodeNotFound):
                pass
        
        # Calculate centrality measures
        try:
            in_centrality = nx.in_degree_centrality(graph)
            out_centrality = nx.out_degree_centrality(graph)
            betweenness_centrality = nx.betweenness_centrality(graph)
            
            # Get top nodes by centrality
            top_in_central = sorted(in_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            top_out_central = sorted(out_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            
            stats.update({
                'top_in_central_nodes': [{'node_id': nid, 'centrality': centrality} 
                                       for nid, centrality in top_in_central],
                'top_out_central_nodes': [{'node_id': nid, 'centrality': centrality} 
                                        for nid, centrality in top_out_central],
                'top_betweenness_central_nodes': [{'node_id': nid, 'centrality': centrality} 
                                                 for nid, centrality in top_betweenness]
            })
        except (nx.NetworkXError, ZeroDivisionError):
            pass
        
        return stats
    
    def _calculate_topic_statistics(self, graph: nx.DiGraph, topic: str) -> Dict[str, Any]:
        """Calculate statistics specific to a topic graph."""
        base_stats = self._calculate_graph_statistics(graph)
        
        # Add topic-specific metrics
        topic_stats = base_stats.copy()
        topic_stats.update({
            'topic': topic,
            'node_types_distribution': self._calculate_node_type_distribution(graph),
            'difficulty_distribution': self._calculate_difficulty_distribution(graph),
            'edge_type_distribution': self._calculate_edge_type_distribution(graph),
            'clustering_coefficient': nx.average_clustering(graph.to_undirected()) if len(graph.nodes) > 2 else 0.0
        })
        
        return topic_stats
    
    def _calculate_node_type_distribution(self, graph: nx.DiGraph) -> Dict[str, int]:
        """Calculate distribution of node types in the graph."""
        distribution = defaultdict(int)
        for node_id in graph.nodes:
            node_data = graph.nodes[node_id]
            node_type = node_data.get('node_type', 'unknown')
            distribution[node_type] += 1
        return dict(distribution)
    
    def _calculate_difficulty_distribution(self, graph: nx.DiGraph) -> Dict[str, int]:
        """Calculate distribution of difficulty levels in the graph."""
        distribution = defaultdict(int)
        for node_id in graph.nodes:
            node_data = graph.nodes[node_id]
            difficulty = node_data.get('difficulty_level', 'unknown')
            distribution[difficulty] += 1
        return dict(distribution)
    
    def _calculate_edge_type_distribution(self, graph: nx.DiGraph) -> Dict[str, int]:
        """Calculate distribution of edge types in the graph."""
        distribution = defaultdict(int)
        for _, _, edge_data in graph.edges(data=True):
            edge_type = edge_data.get('edge_type', 'unknown')
            distribution[edge_type] += 1
        return dict(distribution)
    
    def _get_node_serializer(self):
        """Get the node serializer (placeholder for actual import)"""
        from ..serializers import KnowledgeNodeSerializer
        return KnowledgeNodeSerializer
    
    def _get_edge_serializer(self):
        """Get the edge serializer (placeholder for actual import)"""
        from ..serializers import KnowledgeEdgeSerializer
        return KnowledgeEdgeSerializer


class PathFinder:
    """
    Finds optimal learning paths through knowledge graphs.
    """
    
    def __init__(self):
        self.graph_cache = {}
    
    def find_learning_path(self, start_node_id: uuid.UUID, end_node_id: uuid.UUID, 
                          user_knowledge: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Find an optimal learning path from start to end node.
        
        Args:
            start_node_id: Starting knowledge node UUID
            end_node_id: Target knowledge node UUID
            user_knowledge: User's current knowledge state
            
        Returns:
            List of dictionaries representing the learning path
        """
        try:
            # Get all active nodes and edges
            nodes = KnowledgeNode.objects.filter(is_active=True)
            edges = KnowledgeEdge.objects.filter(is_active=True)
            
            # Build NetworkX graph
            graph = self._build_path_graph(nodes, edges)
            
            # Find path using NetworkX algorithms
            start_id = str(start_node_id)
            end_id = str(end_node_id)
            
            if start_id not in graph.nodes or end_id not in graph.nodes:
                raise ValueError("Start or end node not found in graph")
            
            # Use Dijkstra's algorithm for weighted shortest path
            try:
                path = nx.shortest_path(graph, start_id, end_id, weight='weight')
            except nx.NetworkXNoPath:
                raise ValueError("No path found between start and end nodes")
            
            # Convert path to detailed learning path
            learning_path = []
            for node_id in path:
                try:
                    node = KnowledgeNode.objects.get(id=node_id)
                    learning_path.append({
                        'node_id': str(node.id),
                        'title': node.title,
                        'node_type': node.node_type,
                        'difficulty_level': node.difficulty_level,
                        'description': node.description,
                        'estimated_time': self._estimate_learning_time(node),
                        'prerequisites': node.prerequisites,
                        'learning_objectives': node.learning_objectives
                    })
                except KnowledgeNode.DoesNotExist:
                    continue
            
            return learning_path
        except Exception as e:
            raise Exception(f"Error finding learning path: {str(e)}")
    
    def find_prerequisite_path(self, target_node_id: uuid.UUID) -> List[Dict[str, Any]]:
        """
        Find all prerequisite nodes for a target node.
        
        Args:
            target_node_id: Target knowledge node UUID
            
        Returns:
            List of prerequisite nodes ordered by importance
        """
        try:
            target_id = str(target_node_id)
            
            # Get all nodes and edges
            nodes = KnowledgeNode.objects.filter(is_active=True)
            edges = KnowledgeEdge.objects.filter(is_active=True)
            
            # Build graph
            graph = self._build_path_graph(nodes, edges)
            
            if target_id not in graph.nodes:
                raise ValueError("Target node not found in graph")
            
            # Find all nodes that can reach the target
            prerequisites = []
            
            try:
                # Use reverse BFS to find all prerequisites
                predecessors = nx.predecessors(graph, target_id)
                
                for pred_id in predecessors:
                    try:
                        node = KnowledgeNode.objects.get(id=pred_id)
                        prerequisites.append({
                            'node_id': str(node.id),
                            'title': node.title,
                            'node_type': node.node_type,
                            'difficulty_level': node.difficulty_level,
                            'description': node.description,
                            'estimated_time': self._estimate_learning_time(node)
                        })
                    except KnowledgeNode.DoesNotExist:
                        continue
            except nx.NetworkXError:
                pass
            
            # Sort by difficulty (easier prerequisites first)
            difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3, 'expert': 4}
            prerequisites.sort(key=lambda x: difficulty_order.get(x['difficulty_level'], 99))
            
            return prerequisites
        except Exception as e:
            raise Exception(f"Error finding prerequisite path: {str(e)}")
    
    def _build_path_graph(self, nodes, edges) -> nx.DiGraph:
        """Build NetworkX graph for path finding."""
        graph = nx.DiGraph()
        
        # Add nodes
        for node in nodes:
            graph.add_node(str(node.id), weight=1.0)
        
        # Add edges with weights
        for edge in edges:
            source_id = str(edge.source_node.id)
            target_id = str(edge.target_node.id)
            
            # Calculate edge weight based on type and strength
            weight = self._calculate_edge_weight(edge)
            
            if source_id in graph.nodes and target_id in graph.nodes:
                graph.add_edge(source_id, target_id, weight=weight)
        
        return graph
    
    def _calculate_edge_weight(self, edge: KnowledgeEdge) -> float:
        """Calculate edge weight for path finding."""
        base_weight = {
            'prerequisite': 1.0,
            'related': 2.0,
            'example': 1.5,
            'depends_on': 1.0,
            'leads_to': 1.0,
            'contradicts': 3.0,
            'similar_to': 2.0,
            'part_of': 1.0,
            'contains': 1.0
        }
        
        strength_multiplier = {
            'weak': 1.5,
            'moderate': 1.0,
            'strong': 0.8,
            'essential': 0.5
        }
        
        base = base_weight.get(edge.edge_type, 2.0)
        multiplier = strength_multiplier.get(edge.strength, 1.0)
        
        return base * multiplier
    
    def _estimate_learning_time(self, node: KnowledgeNode) -> int:
        """
        Estimate learning time for a node in minutes.
        
        Args:
            node: KnowledgeNode instance
            
        Returns:
            Estimated time in minutes
        """
        base_times = {
            'concept': 15,
            'skill': 30,
            'topic': 45,
            'objective': 20,
            'assessment': 60,
            'resource': 10
        }
        
        difficulty_multipliers = {
            'beginner': 1.0,
            'intermediate': 1.5,
            'advanced': 2.0,
            'expert': 3.0
        }
        
        base_time = base_times.get(node.node_type, 20)
        difficulty_mult = difficulty_multipliers.get(node.difficulty_level, 1.0)
        
        # Adjust based on content complexity
        complexity_factor = 1.0
        if node.jac_code:
            complexity_factor += len(node.jac_code) / 1000  # Add time for code content
        
        return int(base_time * difficulty_mult * complexity_factor)


class AdaptiveEngine:
    """
    Provides adaptive learning path generation and personalization.
    """
    
    def __init__(self):
        self.learning_cache = {}
    
    def generate_learning_path(self, user, learning_graph: LearningGraph, 
                              adaptation_type: str = 'adaptive',
                              preferences: Dict[str, Any] = None,
                              constraints: Dict[str, Any] = None) -> LearningPath:
        """
        Generate a personalized learning path for a user.
        
        Args:
            user: User instance
            learning_graph: Target learning graph
            adaptation_type: Type of adaptation ('static', 'adaptive', 'personalized', 'ai_generated')
            preferences: User preferences
            constraints: Learning constraints
            
        Returns:
            Generated LearningPath instance
        """
        try:
            # Get user's current knowledge state
            user_knowledge = self._get_user_knowledge_state(user)
            
            # Generate path based on adaptation type
            if adaptation_type == 'static':
                path = self._generate_static_path(user, learning_graph)
            elif adaptation_type == 'adaptive':
                path = self._generate_adaptive_path(user, learning_graph, user_knowledge)
            elif adaptation_type == 'personalized':
                path = self._generate_personalized_path(user, learning_graph, user_knowledge, preferences)
            else:  # ai_generated
                path = self._generate_ai_path(user, learning_graph, user_knowledge, preferences, constraints)
            
            # Save learning path
            path.save()
            
            return path
        except Exception as e:
            raise Exception(f"Error generating learning path: {str(e)}")
    
    def get_recommendations(self, user) -> List[Dict[str, Any]]:
        """
        Get personalized learning recommendations for a user.
        
        Args:
            user: User instance
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            recommendations = []
            
            # Get user's knowledge gaps
            knowledge_gaps = self._identify_knowledge_gaps(user)
            
            # Get user's learning preferences
            preferences = self._get_user_preferences(user)
            
            # Find relevant learning graphs
            relevant_graphs = self._find_relevant_graphs(knowledge_gaps, preferences)
            
            for graph in relevant_graphs:
                recommendation = {
                    'learning_graph_id': str(graph.id),
                    'graph_title': graph.title,
                    'graph_type': graph.graph_type,
                    'estimated_duration': graph.estimated_duration,
                    'difficulty_level': self._assess_graph_difficulty(graph, user),
                    'relevance_score': self._calculate_relevance_score(graph, knowledge_gaps, preferences),
                    'reason': self._generate_recommendation_reason(graph, knowledge_gaps),
                    'prerequisites': self._get_graph_prerequisites(graph),
                    'learning_outcomes': self._get_graph_learning_outcomes(graph)
                }
                recommendations.append(recommendation)
            
            # Sort by relevance score
            recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            return recommendations[:10]  # Return top 10 recommendations
        except Exception as e:
            raise Exception(f"Error getting recommendations: {str(e)}")
    
    def get_adaptation_suggestions(self, user) -> List[Dict[str, Any]]:
        """
        Get suggestions for adapting user's current learning paths.
        
        Args:
            user: User instance
            
        Returns:
            List of adaptation suggestions
        """
        try:
            suggestions = []
            
            # Get user's active learning paths
            active_paths = LearningPath.objects.filter(
                user=user,
                status='active'
            ).select_related('learning_graph')
            
            for path in active_paths:
                # Analyze path performance
                performance_analysis = self._analyze_path_performance(path)
                
                # Generate suggestions based on analysis
                if performance_analysis['struggle_rate'] > 0.3:
                    suggestions.append({
                        'path_id': str(path.id),
                        'path_title': path.title,
                        'suggestion_type': 'reduce_difficulty',
                        'description': 'Consider skipping some difficult nodes or reviewing prerequisites',
                        'confidence': 0.8
                    })
                
                if performance_analysis['mastery_rate'] > 0.8:
                    suggestions.append({
                        'path_id': str(path.id),
                        'path_title': path.title,
                        'suggestion_type': 'increase_difficulty',
                        'description': 'User is mastering content quickly - consider advancing to more challenging material',
                        'confidence': 0.7
                    })
                
                if performance_analysis['inactive_days'] > 7:
                    suggestions.append({
                        'path_id': str(path.id),
                        'path_title': path.title,
                        'suggestion_type': 're_engage',
                        'description': 'User hasn\'t been active - consider sending a reminder or adjusting path pacing',
                        'confidence': 0.6
                    })
            
            return suggestions
        except Exception as e:
            raise Exception(f"Error getting adaptation suggestions: {str(e)}")
    
    def adapt_learning_path(self, learning_path: LearningPath) -> Dict[str, Any]:
        """
        Adapt an existing learning path based on user performance.
        
        Args:
            learning_path: LearningPath instance to adapt
            
        Returns:
            Dictionary with adaptation details
        """
        try:
            adaptations = []
            
            # Get user performance metrics
            performance_data = learning_path.performance_metrics
            
            # Analyze current progress
            completed_count = len(learning_path.completed_nodes)
            total_nodes = learning_path.learning_graph.nodes.count()
            progress_ratio = completed_count / total_nodes if total_nodes > 0 else 0
            
            # Determine if adaptation is needed
            if progress_ratio < 0.1 and performance_data.get('struggle_indicators', 0) > 2:
                # User is struggling - suggest prerequisite review
                adaptations.append({
                    'type': 'add_prerequisite_review',
                    'description': 'Add prerequisite concept review nodes',
                    'confidence': 0.8
                })
            
            if progress_ratio > 0.8 and performance_data.get('mastery_indicators', 0) > 3:
                # User is excelling - suggest acceleration
                adaptations.append({
                    'type': 'accelerate_learning',
                    'description': 'Skip some intermediate nodes and focus on advanced concepts',
                    'confidence': 0.7
                })
            
            # Update learning path with adaptations
            adaptation_history = learning_path.adaptation_history or []
            adaptation_history.append({
                'timestamp': timezone.now().isoformat(),
                'adaptations': adaptations,
                'trigger': 'performance_analysis'
            })
            
            learning_path.adaptation_history = adaptation_history
            learning_path.save(update_fields=['adaptation_history'])
            
            return {
                'path_id': str(learning_path.id),
                'adaptations_made': adaptations,
                'progress_ratio': progress_ratio,
                'total_adaptations': len(adaptation_history)
            }
        except Exception as e:
            raise Exception(f"Error adapting learning path: {str(e)}")
    
    def _get_user_knowledge_state(self, user) -> Dict[str, Any]:
        """Get user's current knowledge state."""
        knowledge_states = UserKnowledgeState.objects.filter(user=user)
        
        state_dict = {}
        for state in knowledge_states:
            state_dict[str(state.knowledge_node.id)] = {
                'mastery_level': state.mastery_level,
                'confidence_score': state.confidence_score,
                'learning_velocity': state.learning_velocity,
                'last_reviewed': state.last_reviewed
            }
        
        return state_dict
    
    def _generate_static_path(self, user, learning_graph: LearningGraph) -> LearningPath:
        """Generate a static learning path (sequential order)."""
        path = LearningPath(
            user=user,
            learning_graph=learning_graph,
            title=f"Static Path: {learning_graph.title}",
            adaptation_type='static',
            status='active'
        )
        
        # Get nodes in display order
        graph_nodes = learning_graph.learninggraphnode_set.order_by('display_order')
        
        # Set initial node if available
        if graph_nodes.exists():
            path.current_node = graph_nodes.first().knowledge_node
        
        return path
    
    def _generate_adaptive_path(self, user, learning_graph: LearningGraph, 
                              user_knowledge: Dict[str, Any]) -> LearningPath:
        """Generate an adaptive learning path."""
        path = LearningPath(
            user=user,
            learning_graph=learning_graph,
            title=f"Adaptive Path: {learning_graph.title}",
            adaptation_type='adaptive',
            status='active'
        )
        
        # Find appropriate starting node based on user knowledge
        start_node = self._find_appropriate_start_node(learning_graph, user_knowledge)
        if start_node:
            path.current_node = start_node
        
        return path
    
    def _generate_personalized_path(self, user, learning_graph: LearningGraph,
                                  user_knowledge: Dict[str, Any], 
                                  preferences: Dict[str, Any]) -> LearningPath:
        """Generate a personalized learning path."""
        path = LearningPath(
            user=user,
            learning_graph=learning_graph,
            title=f"Personalized Path: {learning_graph.title}",
            adaptation_type='personalized',
            status='active'
        )
        
        # Apply user preferences to path generation
        customized_start = self._customize_path_start(learning_graph, preferences, user_knowledge)
        if customized_start:
            path.current_node = customized_start
        
        return path
    
    def _generate_ai_path(self, user, learning_graph: LearningGraph,
                         user_knowledge: Dict[str, Any], preferences: Dict[str, Any],
                         constraints: Dict[str, Any]) -> LearningPath:
        """Generate AI-optimized learning path."""
        path = LearningPath(
            user=user,
            learning_graph=learning_graph,
            title=f"AI-Optimized Path: {learning_graph.title}",
            adaptation_type='ai_generated',
            status='active'
        )
        
        # Apply ML-based optimization
        optimal_start = self._find_optimal_start_node(learning_graph, user_knowledge, preferences, constraints)
        if optimal_start:
            path.current_node = optimal_start
        
        return path
    
    def _identify_knowledge_gaps(self, user) -> List[Dict[str, Any]]:
        """Identify knowledge gaps for a user."""
        gaps = []
        
        # Get user's mastery levels
        knowledge_states = UserKnowledgeState.objects.filter(user=user)
        
        for state in knowledge_states:
            if state.mastery_level in ['novice', 'beginner'] and state.confidence_score < 0.5:
                gaps.append({
                    'node_id': str(state.knowledge_node.id),
                    'concept': state.knowledge_node.title,
                    'gap_severity': 'high',
                    'current_mastery': state.mastery_level
                })
        
        return gaps
    
    def _get_user_preferences(self, user) -> Dict[str, Any]:
        """Get user's learning preferences (placeholder implementation)."""
        # This would typically come from user profile or preference settings
        return {
            'preferred_difficulty': 'intermediate',
            'learning_pace': 'moderate',
            'content_types': ['concept', 'skill'],
            'session_length': 30  # minutes
        }
    
    def _find_relevant_graphs(self, knowledge_gaps, preferences) -> List[LearningGraph]:
        """Find relevant learning graphs based on gaps and preferences."""
        # Simple implementation - filter by subject area and status
        graphs = LearningGraph.objects.filter(
            status='active'
        )
        
        # Filter by user's preferred difficulty
        if preferences.get('preferred_difficulty'):
            # This would require additional logic to match user level with graph difficulty
            # For now, we'll skip this filter as it needs additional model fields
            pass
        
        return graphs[:10]  # Return top 10
    
    def _assess_graph_difficulty(self, graph: LearningGraph, user) -> str:
        """Assess graph difficulty for user."""
        # Simple implementation based on graph metadata
        return graph.target_audience or 'intermediate'
    
    def _calculate_relevance_score(self, graph: LearningGraph, knowledge_gaps, preferences) -> float:
        """Calculate relevance score for a graph."""
        score = 0.0
        
        # Base score from graph completion rate
        score += graph.completion_rate * 0.3
        
        # Score from subject area match
        if preferences.get('subject_area') == graph.subject_area:
            score += 0.4
        
        # Score from graph type match
        if preferences.get('preferred_graph_type') == graph.graph_type:
            score += 0.3
        
        return min(score, 1.0)
    
    def _generate_recommendation_reason(self, graph: LearningGraph, knowledge_gaps) -> str:
        """Generate human-readable recommendation reason."""
        reasons = []
        
        if graph.completion_rate > 0.8:
            reasons.append("high completion rate")
        
        if graph.graph_type == 'course':
            reasons.append("comprehensive course structure")
        
        if graph.subject_area:
            reasons.append(f"focuses on {graph.subject_area}")
        
        return "Recommended because " + ", ".join(reasons) if reasons else "Good fit for your learning goals"
    
    def _get_graph_prerequisites(self, graph: LearningGraph) -> List[str]:
        """Get prerequisites for a learning graph."""
        # This would extract prerequisite information from the graph
        return []
    
    def _get_graph_learning_outcomes(self, graph: LearningGraph) -> List[str]:
        """Get learning outcomes for a learning graph."""
        # This would extract learning outcomes from the graph
        return []
    
    def _analyze_path_performance(self, path: LearningPath) -> Dict[str, Any]:
        """Analyze performance metrics for a learning path."""
        performance_data = path.performance_metrics or {}
        
        # Calculate metrics
        completed_nodes = len(path.completed_nodes)
        total_nodes = path.learning_graph.nodes.count()
        progress_ratio = completed_nodes / total_nodes if total_nodes > 0 else 0
        
        # Get struggle and mastery indicators
        struggle_rate = performance_data.get('struggle_indicators', 0) / max(completed_nodes, 1)
        mastery_rate = performance_data.get('mastery_indicators', 0) / max(completed_nodes, 1)
        
        # Calculate inactive days
        inactive_days = (timezone.now() - path.last_activity).days
        
        return {
            'progress_ratio': progress_ratio,
            'struggle_rate': struggle_rate,
            'mastery_rate': mastery_rate,
            'inactive_days': inactive_days,
            'completed_nodes': completed_nodes,
            'total_nodes': total_nodes
        }
    
    def _find_appropriate_start_node(self, learning_graph: LearningGraph, 
                                   user_knowledge: Dict[str, Any]) -> KnowledgeNode:
        """Find appropriate starting node based on user knowledge."""
        # Get graph nodes sorted by display order
        graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node').order_by('display_order')
        
        for graph_node in graph_nodes:
            node = graph_node.knowledge_node
            node_id = str(node.id)
            
            # Check if user already knows this concept
            if node_id in user_knowledge:
                mastery_level = user_knowledge[node_id]['mastery_level']
                if mastery_level in ['proficient', 'expert']:
                    continue  # Skip if user already knows this
            
            # Return first appropriate node
            return node
        
        # Return first node if no suitable node found
        return graph_nodes.first().knowledge_node if graph_nodes.exists() else None
    
    def _customize_path_start(self, learning_graph: LearningGraph, preferences: Dict[str, Any],
                            user_knowledge: Dict[str, Any]) -> KnowledgeNode:
        """Customize path start based on user preferences."""
        # Start with appropriate node
        start_node = self._find_appropriate_start_node(learning_graph, user_knowledge)
        
        # Apply preference-based customization
        if preferences.get('preferred_difficulty') == 'beginner':
            # Try to find a beginner-level node
            beginner_nodes = learning_graph.learninggraphnode_set.filter(
                knowledge_node__difficulty_level='beginner'
            ).select_related('knowledge_node')
            
            if beginner_nodes.exists():
                return beginner_nodes.first().knowledge_node
        
        return start_node
    
    def _find_optimal_start_node(self, learning_graph: LearningGraph, user_knowledge: Dict[str, Any],
                               preferences: Dict[str, Any], constraints: Dict[str, Any]) -> KnowledgeNode:
        """Find optimal starting node using advanced algorithms."""
        # Advanced ML-based optimization would go here
        # For now, use the same logic as personalized path
        return self._customize_path_start(learning_graph, preferences, user_knowledge)


# Import required modules at the end to avoid circular imports
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime
    timezone = type('timezone', (), {'now': lambda: datetime.now()})()