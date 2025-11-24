"""
Object-Spatial Programming (OSP) Implementation for Knowledge Graphs.

This module implements OSP concepts for spatial knowledge representation,
including spatial relationships, positioning algorithms, and visual graph layout.
"""

import uuid
import json
import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from django.db.models import Q, Avg, Count
from ..models import KnowledgeNode, KnowledgeEdge, LearningGraph


class OSPProcessor:
    """
    Processes Object-Spatial Programming concepts for knowledge graphs.
    
    Handles spatial positioning, relationships, and visual layout generation.
    """
    
    def __init__(self):
        self.spatial_cache = {}
    
    def generate_spatial_layout(self, nodes: List[KnowledgeNode], 
                               edges: List[KnowledgeEdge],
                               layout_type: str = 'hierarchical') -> Dict[str, Dict[str, float]]:
        """
        Generate spatial positions for knowledge nodes based on OSP principles.
        
        Args:
            nodes: List of KnowledgeNode instances
            edges: List of KnowledgeEdge instances
            layout_type: Type of spatial layout ('hierarchical', 'circular', 'force_directed', 'clustered')
            
        Returns:
            Dictionary mapping node IDs to spatial coordinates
        """
        try:
            if layout_type == 'hierarchical':
                return self._generate_hierarchical_layout(nodes, edges)
            elif layout_type == 'circular':
                return self._generate_circular_layout(nodes, edges)
            elif layout_type == 'force_directed':
                return self._generate_force_directed_layout(nodes, edges)
            elif layout_type == 'clustered':
                return self._generate_clustered_layout(nodes, edges)
            else:
                raise ValueError(f"Unknown layout type: {layout_type}")
        except Exception as e:
            raise Exception(f"Error generating spatial layout: {str(e)}")
    
    def calculate_spatial_relationships(self, node_a: KnowledgeNode, 
                                      node_b: KnowledgeNode) -> Dict[str, Any]:
        """
        Calculate spatial relationships between two nodes based on OSP principles.
        
        Args:
            node_a: First knowledge node
            node_b: Second knowledge node
            
        Returns:
            Dictionary describing spatial relationship
        """
        try:
            # Calculate distance
            distance = self._calculate_distance(node_a, node_b)
            
            # Calculate relative position
            relative_position = self._calculate_relative_position(node_a, node_b)
            
            # Determine spatial relationship type
            relationship_type = self._determine_spatial_relationship(
                node_a, node_b, distance, relative_position
            )
            
            # Calculate spatial coherence score
            coherence_score = self._calculate_spatial_coherence(node_a, node_b)
            
            return {
                'distance': distance,
                'relative_position': relative_position,
                'relationship_type': relationship_type,
                'coherence_score': coherence_score,
                'spatial_properties': {
                    'x_delta': node_b.x_position - node_a.x_position,
                    'y_delta': node_b.y_position - node_a.y_position,
                    'z_delta': node_b.z_position - node_a.z_position,
                    'direction_vector': [
                        node_b.x_position - node_a.x_position,
                        node_b.y_position - node_a.y_position,
                        node_b.z_position - node_a.z_position
                    ]
                }
            }
        except Exception as e:
            raise Exception(f"Error calculating spatial relationships: {str(e)}")
    
    def optimize_graph_layout(self, learning_graph: LearningGraph, 
                            algorithm: str = 'force_directed') -> Dict[str, Any]:
        """
        Optimize the spatial layout of a learning graph.
        
        Args:
            learning_graph: LearningGraph instance
            algorithm: Optimization algorithm to use
            
        Returns:
            Dictionary with optimized layout and metrics
        """
        try:
            # Get all nodes and edges for the graph
            graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
            graph_edges = learning_graph.learninggraphedge_set.select_related('knowledge_edge')
            
            nodes = [gn.knowledge_node for gn in graph_nodes]
            edges = [ge.knowledge_edge for ge in graph_edges]
            
            # Apply spatial optimization
            if algorithm == 'force_directed':
                optimized_layout = self._force_directed_optimization(nodes, edges)
            elif algorithm == 'hierarchical':
                optimized_layout = self._hierarchical_optimization(nodes, edges)
            elif algorithm == 'circular':
                optimized_layout = self._circular_optimization(nodes, edges)
            else:
                optimized_layout = self._generate_spatial_layout(nodes, edges, algorithm)
            
            # Calculate layout quality metrics
            quality_metrics = self._calculate_layout_quality(optimized_layout, nodes, edges)
            
            # Update node positions if needed
            position_updates = self._prepare_position_updates(optimized_layout, learning_graph)
            
            return {
                'layout': optimized_layout,
                'quality_metrics': quality_metrics,
                'position_updates': position_updates,
                'optimization_algorithm': algorithm,
                'nodes_count': len(nodes),
                'edges_count': len(edges)
            }
        except Exception as e:
            raise Exception(f"Error optimizing graph layout: {str(e)}")
    
    def generate_visualization_config(self, learning_graph: LearningGraph,
                                    view_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate configuration for graph visualization.
        
        Args:
            learning_graph: LearningGraph instance
            view_config: Optional view configuration parameters
            
        Returns:
            Dictionary with visualization configuration
        """
        try:
            # Get graph nodes and edges
            graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
            graph_edges = learning_graph.learninggraphedge_set.select_related('knowledge_edge')
            
            nodes = [gn.knowledge_node for gn in graph_nodes]
            edges = [ge.knowledge_edge for ge in graph_edges]
            
            # Set default view configuration
            default_config = {
                'width': 1200,
                'height': 800,
                'zoom_level': 1.0,
                'pan_x': 0,
                'pan_y': 0,
                'show_labels': True,
                'show_edges': True,
                'node_colors': {},
                'edge_colors': {},
                'layout_type': 'force_directed'
            }
            
            if view_config:
                default_config.update(view_config)
            
            # Generate color schemes
            color_schemes = self._generate_color_schemes(nodes, edges)
            
            # Generate node visual properties
            node_visuals = self._generate_node_visuals(nodes, default_config)
            
            # Generate edge visual properties
            edge_visuals = self._generate_edge_visuals(edges, default_config)
            
            # Calculate view box
            view_box = self._calculate_view_box(nodes, default_config)
            
            return {
                'graph_config': default_config,
                'color_schemes': color_schemes,
                'node_visuals': node_visuals,
                'edge_visuals': edge_visuals,
                'view_box': view_box,
                'interaction_config': {
                    'draggable_nodes': True,
                    'zoomable': True,
                    'panable': True,
                    'selectable': True,
                    'highlight_on_hover': True
                },
                'animation_config': {
                    'node_transitions': True,
                    'edge_animations': True,
                    'layout_animations': True
                }
            }
        except Exception as e:
            raise Exception(f"Error generating visualization config: {str(e)}")
    
    def calculate_learning_flow_paths(self, learning_graph: LearningGraph,
                                    start_node: KnowledgeNode = None) -> List[Dict[str, Any]]:
        """
        Calculate optimal learning flow paths through the knowledge graph.
        
        Args:
            learning_graph: LearningGraph instance
            start_node: Optional starting node for path calculation
            
        Returns:
            List of learning flow paths with metadata
        """
        try:
            # Get graph structure
            graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
            graph_edges = learning_graph.learninggraphedge_set.select_related('knowledge_edge')
            
            nodes = [gn.knowledge_node for gn in graph_nodes]
            edges = [ge.knowledge_edge for ge in graph_edges]
            
            # Determine starting point
            if not start_node:
                start_node = self._find_optimal_start_node(nodes, edges)
            
            # Calculate flow paths
            flow_paths = []
            
            # Path 1: Sequential learning path
            sequential_path = self._calculate_sequential_path(nodes, edges, start_node)
            flow_paths.append({
                'path_type': 'sequential',
                'description': 'Follow nodes in logical order',
                'nodes': sequential_path,
                'estimated_duration': self._estimate_path_duration(sequential_path),
                'difficulty_progression': self._calculate_difficulty_progression(sequential_path)
            })
            
            # Path 2: Prerequisite-based path
            prerequisite_path = self._calculate_prerequisite_path(nodes, edges, start_node)
            flow_paths.append({
                'path_type': 'prerequisite',
                'description': 'Follow prerequisite relationships',
                'nodes': prerequisite_path,
                'estimated_duration': self._estimate_path_duration(prerequisite_path),
                'difficulty_progression': self._calculate_difficulty_progression(prerequisite_path)
            })
            
            # Path 3: Adaptive path (if graph has adaptive rules)
            if learning_graph.adaptive_rules:
                adaptive_path = self._calculate_adaptive_path(nodes, edges, learning_graph.adaptive_rules)
                flow_paths.append({
                    'path_type': 'adaptive',
                    'description': 'Path that adapts based on user performance',
                    'nodes': adaptive_path,
                    'estimated_duration': self._estimate_path_duration(adaptive_path),
                    'difficulty_progression': self._calculate_difficulty_progression(adaptive_path)
                })
            
            return flow_paths
        except Exception as e:
            raise Exception(f"Error calculating learning flow paths: {str(e)}")
    
    def _generate_hierarchical_layout(self, nodes: List[KnowledgeNode], 
                                    edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Generate hierarchical spatial layout."""
        layout = {}
        
        # Group nodes by difficulty level (y-coordinate)
        difficulty_levels = ['beginner', 'intermediate', 'advanced', 'expert']
        level_positions = {level: i * 200 for i, level in enumerate(difficulty_levels)}
        
        # Group nodes by node type for x-positioning
        type_groups = defaultdict(list)
        for node in nodes:
            type_groups[node.node_type].append(node)
        
        # Position nodes
        x_spacing = 150
        for node_type, type_nodes in type_groups.items():
            for i, node in enumerate(type_nodes):
                x = i * x_spacing
                y = level_positions.get(node.difficulty_level, 0)
                z = 0  # Default z-position
                
                layout[str(node.id)] = {'x': x, 'y': y, 'z': z}
        
        return layout
    
    def _generate_circular_layout(self, nodes: List[KnowledgeNode], 
                                edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Generate circular spatial layout."""
        layout = {}
        radius = max(300, len(nodes) * 50)
        center_x, center_y = 400, 300
        
        for i, node in enumerate(nodes):
            angle = (2 * math.pi * i) / len(nodes)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            z = 0
            
            layout[str(node.id)] = {'x': x, 'y': y, 'z': z}
        
        return layout
    
    def _generate_force_directed_layout(self, nodes: List[KnowledgeNode], 
                                      edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Generate force-directed spatial layout using simplified algorithm."""
        layout = {}
        
        # Initialize positions randomly
        import random
        for node in nodes:
            layout[str(node.id)] = {
                'x': random.uniform(-400, 400),
                'y': random.uniform(-300, 300),
                'z': random.uniform(-10, 10)
            }
        
        # Apply repulsive forces between all nodes
        for _ in range(50):  # iterations
            for i, node_a in enumerate(nodes):
                for j, node_b in enumerate(nodes[i+1:], i+1):
                    pos_a = layout[str(node_a.id)]
                    pos_b = layout[str(node_b.id)]
                    
                    # Calculate distance
                    dx = pos_b['x'] - pos_a['x']
                    dy = pos_b['y'] - pos_a['y']
                    dz = pos_b['z'] - pos_a['z']
                    distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                    
                    if distance > 0:
                        # Apply repulsive force
                        force = 1000 / (distance * distance)
                        fx = force * dx / distance
                        fy = force * dy / distance
                        fz = force * dz / distance
                        
                        layout[str(node_a.id)]['x'] -= fx * 0.1
                        layout[str(node_a.id)]['y'] -= fy * 0.1
                        layout[str(node_a.id)]['z'] -= fz * 0.1
                        layout[str(node_b.id)]['x'] += fx * 0.1
                        layout[str(node_b.id)]['y'] += fy * 0.1
                        layout[str(node_b.id)]['z'] += fz * 0.1
            
            # Apply attractive forces along edges
            for edge in edges:
                pos_source = layout[str(edge.source_node.id)]
                pos_target = layout[str(edge.target_node.id)]
                
                dx = pos_target['x'] - pos_source['x']
                dy = pos_target['y'] - pos_source['y']
                dz = pos_target['z'] - pos_source['z']
                distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if distance > 0:
                    # Apply attractive force
                    force = distance * 0.001
                    fx = force * dx / distance
                    fy = force * dy / distance
                    fz = force * dz / distance
                    
                    layout[str(edge.source_node.id)]['x'] += fx * 0.1
                    layout[str(edge.source_node.id)]['y'] += fy * 0.1
                    layout[str(edge.source_node.id)]['z'] += fz * 0.1
                    layout[str(edge.target_node.id)]['x'] -= fx * 0.1
                    layout[str(edge.target_node.id)]['y'] -= fy * 0.1
                    layout[str(edge.target_node.id)]['z'] -= fz * 0.1
        
        return layout
    
    def _generate_clustered_layout(self, nodes: List[KnowledgeNode], 
                                 edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Generate clustered spatial layout based on node types."""
        layout = {}
        
        # Group nodes by type
        type_clusters = defaultdict(list)
        for node in nodes:
            type_clusters[node.node_type].append(node)
        
        # Position clusters
        cluster_positions = {
            'concept': (0, 0),
            'skill': (300, 0),
            'topic': (0, 300),
            'objective': (300, 300),
            'assessment': (150, 150),
            'resource': (450, 150)
        }
        
        # Position nodes within clusters
        for node_type, type_nodes in type_clusters.items():
            cluster_x, cluster_y = cluster_positions.get(node_type, (0, 0))
            
            for i, node in enumerate(type_nodes):
                # Arrange nodes in sub-grid within cluster
                subgrid_size = int(math.sqrt(len(type_nodes))) + 1
                subgrid_x = i % subgrid_size
                subgrid_y = i // subgrid_size
                
                x = cluster_x + subgrid_x * 80
                y = cluster_y + subgrid_y * 80
                z = 0
                
                layout[str(node.id)] = {'x': x, 'y': y, 'z': z}
        
        return layout
    
    def _calculate_distance(self, node_a: KnowledgeNode, node_b: KnowledgeNode) -> float:
        """Calculate Euclidean distance between two nodes."""
        dx = node_b.x_position - node_a.x_position
        dy = node_b.y_position - node_a.y_position
        dz = node_b.z_position - node_a.z_position
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def _calculate_relative_position(self, node_a: KnowledgeNode, node_b: KnowledgeNode) -> str:
        """Calculate relative position between two nodes."""
        dx = node_b.x_position - node_a.x_position
        dy = node_b.y_position - node_a.y_position
        
        # Determine relative position based on coordinate differences
        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'above' if dy > 0 else 'below'
    
    def _determine_spatial_relationship(self, node_a: KnowledgeNode, node_b: KnowledgeNode,
                                       distance: float, relative_position: str) -> str:
        """Determine spatial relationship type based on position and distance."""
        # Determine relationship based on distance and relative position
        if distance < 100:
            return 'adjacent'
        elif distance < 300:
            return 'near'
        else:
            return 'distant'
    
    def _calculate_spatial_coherence(self, node_a: KnowledgeNode, node_b: KnowledgeNode) -> float:
        """Calculate spatial coherence score between two nodes."""
        # Score based on similar difficulty levels and node types
        score = 0.0
        
        if node_a.difficulty_level == node_b.difficulty_level:
            score += 0.3
        
        if node_a.node_type == node_b.node_type:
            score += 0.2
        
        # Consider spatial proximity
        distance = self._calculate_distance(node_a, node_b)
        if distance < 200:
            score += 0.3
        elif distance < 400:
            score += 0.1
        
        return min(score, 1.0)
    
    def _force_directed_optimization(self, nodes: List[KnowledgeNode], 
                                   edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Optimize layout using force-directed algorithm."""
        return self._generate_force_directed_layout(nodes, edges)
    
    def _hierarchical_optimization(self, nodes: List[KnowledgeNode], 
                                 edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Optimize layout using hierarchical algorithm."""
        return self._generate_hierarchical_layout(nodes, edges)
    
    def _circular_optimization(self, nodes: List[KnowledgeNode], 
                             edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, float]]:
        """Optimize layout using circular algorithm."""
        return self._generate_circular_layout(nodes, edges)
    
    def _calculate_layout_quality(self, layout: Dict[str, Dict[str, float]], 
                                nodes: List[KnowledgeNode], 
                                edges: List[KnowledgeEdge]) -> Dict[str, float]:
        """Calculate quality metrics for the layout."""
        metrics = {}
        
        # Calculate edge length statistics
        edge_lengths = []
        for edge in edges:
            source_pos = layout[str(edge.source_node.id)]
            target_pos = layout[str(edge.target_node.id)]
            
            dx = target_pos['x'] - source_pos['x']
            dy = target_pos['y'] - source_pos['y']
            dz = target_pos['z'] - source_pos['z']
            length = math.sqrt(dx*dx + dy*dy + dz*dz)
            edge_lengths.append(length)
        
        if edge_lengths:
            metrics['average_edge_length'] = sum(edge_lengths) / len(edge_lengths)
            metrics['min_edge_length'] = min(edge_lengths)
            metrics['max_edge_length'] = max(edge_lengths)
            metrics['edge_length_variance'] = self._calculate_variance(edge_lengths)
        
        # Calculate node distribution metrics
        positions = [layout[str(node.id)] for node in nodes]
        x_coords = [pos['x'] for pos in positions]
        y_coords = [pos['y'] for pos in positions]
        
        metrics['node_distribution_x'] = self._calculate_variance(x_coords)
        metrics['node_distribution_y'] = self._calculate_variance(y_coords)
        
        # Calculate layout balance (how centered the graph is)
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        distances_from_center = []
        for pos in positions:
            dx = pos['x'] - center_x
            dy = pos['y'] - center_y
            distance = math.sqrt(dx*dx + dy*dy)
            distances_from_center.append(distance)
        
        metrics['layout_balance'] = sum(distances_from_center) / len(distances_from_center)
        
        return metrics
    
    def _calculate_variance(self, values: List[float]) -> float:
        """Calculate variance of a list of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance
    
    def _prepare_position_updates(self, layout: Dict[str, Dict[str, float]], 
                                learning_graph: LearningGraph) -> List[Dict[str, Any]]:
        """Prepare position updates for nodes in the learning graph."""
        updates = []
        
        graph_nodes = learning_graph.learninggraphnode_set.select_related('knowledge_node')
        for graph_node in graph_nodes:
            node_id = str(graph_node.knowledge_node.id)
            if node_id in layout:
                position = layout[node_id]
                updates.append({
                    'node_id': node_id,
                    'x_position': position['x'],
                    'y_position': position['y'],
                    'z_position': position['z']
                })
        
        return updates
    
    def _generate_color_schemes(self, nodes: List[KnowledgeNode], 
                              edges: List[KnowledgeEdge]) -> Dict[str, Dict[str, str]]:
        """Generate color schemes for graph visualization."""
        color_schemes = {
            'node_colors': {},
            'edge_colors': {},
            'difficulty_colors': {
                'beginner': '#4CAF50',    # Green
                'intermediate': '#2196F3', # Blue
                'advanced': '#FF9800',    # Orange
                'expert': '#F44336'       # Red
            },
            'type_colors': {
                'concept': '#9C27B0',     # Purple
                'skill': '#3F51B5',       # Indigo
                'topic': '#009688',       # Teal
                'objective': '#795548',   # Brown
                'assessment': '#607D8B',  # Blue Grey
                'resource': '#795548'     # Brown
            }
        }
        
        # Generate node colors based on type and difficulty
        for node in nodes:
            node_colors = color_schemes['node_colors']
            node_colors[str(node.id)] = {
                'primary': color_schemes['type_colors'].get(node.node_type, '#757575'),
                'difficulty': color_schemes['difficulty_colors'].get(node.difficulty_level, '#757575'),
                'border': '#ffffff',
                'text': '#000000'
            }
        
        # Generate edge colors based on type and strength
        for edge in edges:
            edge_colors = color_schemes['edge_colors']
            edge_colors[str(edge.id)] = {
                'primary': self._get_edge_color_by_type(edge.edge_type),
                'strength': self._get_edge_color_by_strength(edge.strength),
                'width': self._get_edge_width_by_strength(edge.strength)
            }
        
        return color_schemes
    
    def _get_edge_color_by_type(self, edge_type: str) -> str:
        """Get color for edge based on type."""
        color_map = {
            'prerequisite': '#F44336',     # Red
            'related': '#2196F3',          # Blue
            'example': '#4CAF50',          # Green
            'depends_on': '#FF9800',       # Orange
            'leads_to': '#9C27B0',         # Purple
            'contradicts': '#E91E63',      # Pink
            'similar_to': '#00BCD4',       # Cyan
            'part_of': '#607D8B',          # Blue Grey
            'contains': '#795548'          # Brown
        }
        return color_map.get(edge_type, '#757575')  # Grey default
    
    def _get_edge_color_by_strength(self, strength: str) -> str:
        """Get color for edge based on strength."""
        strength_map = {
            'weak': '#E0E0E0',             # Light grey
            'moderate': '#757575',         # Grey
            'strong': '#424242',           # Dark grey
            'essential': '#212121'         # Very dark grey
        }
        return strength_map.get(strength, '#757575')
    
    def _get_edge_width_by_strength(self, strength: str) -> float:
        """Get edge width based on strength."""
        width_map = {
            'weak': 1.0,
            'moderate': 2.0,
            'strong': 3.0,
            'essential': 4.0
        }
        return width_map.get(strength, 2.0)
    
    def _generate_node_visuals(self, nodes: List[KnowledgeNode], 
                             config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Generate visual properties for nodes."""
        visuals = {}
        
        for node in nodes:
            visuals[str(node.id)] = {
                'size': self._calculate_node_size(node),
                'shape': self._get_node_shape(node.node_type),
                'opacity': 0.8,
                'stroke_width': 2,
                'label_visible': config.get('show_labels', True),
                'animation': {
                    'on_hover': True,
                    'on_click': True,
                    'pulse_effect': False
                }
            }
        
        return visuals
    
    def _generate_edge_visuals(self, edges: List[KnowledgeEdge], 
                             config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Generate visual properties for edges."""
        visuals = {}
        
        for edge in edges:
            visuals[str(edge.id)] = {
                'stroke_width': self._get_edge_width_by_strength(edge.strength),
                'opacity': 0.6,
                'stroke_dasharray': self._get_edge_dash_pattern(edge.edge_type),
                'curve_factor': 0.1 if edge.curve_points else 0.0,
                'arrow_visible': True,
                'animation': {
                    'on_traversal': True,
                    'flow_animation': True
                }
            }
        
        return visuals
    
    def _calculate_node_size(self, node: KnowledgeNode) -> float:
        """Calculate node size based on content and importance."""
        base_size = 20
        size_modifier = 1.0
        
        # Adjust size based on content
        if node.jac_code:
            size_modifier += len(node.jac_code) / 1000
        
        if node.learning_objectives:
            size_modifier += len(node.learning_objectives) * 0.1
        
        # Adjust size based on node type
        type_modifiers = {
            'concept': 1.0,
            'skill': 1.2,
            'topic': 1.5,
            'objective': 1.1,
            'assessment': 1.3,
            'resource': 0.8
        }
        
        type_modifier = type_modifiers.get(node.node_type, 1.0)
        
        return base_size * size_modifier * type_modifier
    
    def _get_node_shape(self, node_type: str) -> str:
        """Get node shape based on type."""
        shape_map = {
            'concept': 'circle',
            'skill': 'rectangle',
            'topic': 'diamond',
            'objective': 'hexagon',
            'assessment': 'triangle',
            'resource': 'circle'
        }
        return shape_map.get(node_type, 'circle')
    
    def _get_edge_dash_pattern(self, edge_type: str) -> str:
        """Get dash pattern for edge based on type."""
        pattern_map = {
            'prerequisite': '0',                    # Solid
            'related': '5,5',                       # Dashed
            'example': '10,5,2,5',                  # Dash-dot
            'depends_on': '0',                      # Solid
            'leads_to': '0',                        # Solid
            'contradicts': '10,2',                  # Long dashes
            'similar_to': '5,5',                    # Dashed
            'part_of': '2,2',                       # Short dashes
            'contains': '0'                         # Solid
        }
        return pattern_map.get(edge_type, '0')
    
    def _calculate_view_box(self, nodes: List[KnowledgeNode], 
                          config: Dict[str, Any]) -> Dict[str, float]:
        """Calculate view box for graph visualization."""
        if not nodes:
            return {'min_x': -100, 'max_x': 100, 'min_y': -100, 'max_y': 100}
        
        x_coords = [node.x_position for node in nodes]
        y_coords = [node.y_position for node in nodes]
        
        min_x = min(x_coords) - 50
        max_x = max(x_coords) + 50
        min_y = min(y_coords) - 50
        max_y = max(y_coords) + 50
        
        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': max_x - min_x,
            'height': max_y - min_y
        }
    
    def _find_optimal_start_node(self, nodes: List[KnowledgeNode], 
                               edges: List[KnowledgeEdge]) -> KnowledgeNode:
        """Find optimal starting node for learning path."""
        # Find node with no incoming prerequisite edges
        start_candidates = []
        
        for node in nodes:
            has_prerequisite = False
            for edge in edges:
                if (edge.target_node.id == node.id and 
                    edge.edge_type == 'prerequisite'):
                    has_prerequisite = True
                    break
            
            if not has_prerequisite:
                start_candidates.append(node)
        
        # Return first candidate or first node if none found
        return start_candidates[0] if start_candidates else nodes[0]
    
    def _calculate_sequential_path(self, nodes: List[KnowledgeNode], 
                                 edges: List[KnowledgeEdge],
                                 start_node: KnowledgeNode) -> List[KnowledgeNode]:
        """Calculate sequential learning path."""
        path = [start_node]
        visited = {start_node.id}
        
        # Simple sequential traversal - this would be more sophisticated in reality
        remaining_nodes = [node for node in nodes if node.id not in visited]
        
        for node in remaining_nodes[:10]:  # Limit path length
            path.append(node)
            visited.add(node.id)
        
        return path
    
    def _calculate_prerequisite_path(self, nodes: List[KnowledgeNode], 
                                   edges: List[KnowledgeEdge],
                                   start_node: KnowledgeNode) -> List[KnowledgeNode]:
        """Calculate prerequisite-based learning path."""
        # Find all prerequisite relationships
        prerequisites = defaultdict(list)
        for edge in edges:
            if edge.edge_type == 'prerequisite':
                prerequisites[edge.target_node.id].append(edge.source_node.id)
        
        # Build prerequisite path using topological sort
        path = []
        visited = set()
        
        def visit_node(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            
            # Visit prerequisites first
            for prereq_id in prerequisites.get(node_id, []):
                prereq_node = next((n for n in nodes if n.id == prereq_id), None)
                if prereq_node:
                    visit_node(prereq_node.id)
            
            # Add this node to path
            node = next((n for n in nodes if n.id == node_id), None)
            if node:
                path.append(node)
        
        visit_node(start_node.id)
        
        # Add remaining nodes that haven't been visited
        for node in nodes:
            if node.id not in visited:
                visit_node(node.id)
        
        return path
    
    def _calculate_adaptive_path(self, nodes: List[KnowledgeNode], 
                               edges: List[KnowledgeEdge],
                               adaptive_rules: Dict[str, Any]) -> List[KnowledgeNode]:
        """Calculate adaptive learning path based on rules."""
        # This would implement more sophisticated adaptive logic
        # For now, return a simple path
        return nodes[:10]  # First 10 nodes as fallback
    
    def _estimate_path_duration(self, path: List[KnowledgeNode]) -> int:
        """Estimate duration of a learning path in minutes."""
        total_duration = 0
        
        for node in path:
            # Base duration by node type
            type_durations = {
                'concept': 15,
                'skill': 30,
                'topic': 45,
                'objective': 20,
                'assessment': 60,
                'resource': 10
            }
            
            base_duration = type_durations.get(node.node_type, 20)
            
            # Adjust for difficulty
            difficulty_multipliers = {
                'beginner': 1.0,
                'intermediate': 1.5,
                'advanced': 2.0,
                'expert': 3.0
            }
            
            multiplier = difficulty_multipliers.get(node.difficulty_level, 1.0)
            total_duration += int(base_duration * multiplier)
        
        return total_duration
    
    def _calculate_difficulty_progression(self, path: List[KnowledgeNode]) -> List[str]:
        """Calculate difficulty progression along a path."""
        return [node.difficulty_level for node in path]