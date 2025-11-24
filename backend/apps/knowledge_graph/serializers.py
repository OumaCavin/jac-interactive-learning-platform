"""
Serializers for Knowledge Graph API endpoints.

This module provides serializers for converting Django model instances
to JSON and vice versa for the knowledge graph API.
"""

from rest_framework import serializers
from .models import (
    KnowledgeNode, KnowledgeEdge, ConceptRelation, LearningGraph,
    LearningGraphNode, LearningGraphEdge, LearningPath, UserKnowledgeState
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']


class KnowledgeNodeSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeNode model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    outgoing_edges_count = serializers.IntegerField(source='outgoing_edges.count', read_only=True)
    incoming_edges_count = serializers.IntegerField(source='incoming_edges.count', read_only=True)
    
    class Meta:
        model = KnowledgeNode
        fields = [
            'id', 'title', 'description', 'node_type', 'difficulty_level',
            'x_position', 'y_position', 'z_position', 'width', 'height',
            'content_uri', 'jac_code', 'learning_objectives', 'prerequisites',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'is_active', 'view_count', 'outgoing_edges_count', 'incoming_edges_count'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at', 'view_count',
            'outgoing_edges_count', 'incoming_edges_count'
        ]
    
    def validate_learning_objectives(self, value):
        """Validate learning objectives format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Learning objectives must be a list")
        return value
    
    def validate_prerequisites(self, value):
        """Validate prerequisites format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Prerequisites must be a list")
        return value


class KnowledgeEdgeSerializer(serializers.ModelSerializer):
    """Serializer for KnowledgeEdge model"""
    
    source_node_title = serializers.CharField(source='source_node.title', read_only=True)
    target_node_title = serializers.CharField(source='target_node.title', read_only=True)
    source_node_id = serializers.CharField(source='source_node.id', read_only=True)
    target_node_id = serializers.CharField(source='target_node.id', read_only=True)
    
    class Meta:
        model = KnowledgeEdge
        fields = [
            'id', 'source_node', 'source_node_title', 'source_node_id',
            'target_node', 'target_node_title', 'target_node_id',
            'edge_type', 'strength', 'curve_points', 'edge_weight',
            'description', 'examples', 'traversal_count',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = [
            'id', 'traversal_count', 'created_at', 'updated_at',
            'source_node_title', 'target_node_title', 'source_node_id', 'target_node_id'
        ]


class KnowledgeEdgeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating KnowledgeEdge instances"""
    
    class Meta:
        model = KnowledgeEdge
        fields = ['source_node', 'target_node', 'edge_type', 'strength', 'description']
    
    def validate(self, data):
        """Validate edge creation data"""
        source_node = data.get('source_node')
        target_node = data.get('target_node')
        edge_type = data.get('edge_type')
        
        if source_node and target_node and source_node.id == target_node.id:
            raise serializers.ValidationError("Cannot create edge from node to itself")
        
        # Check for existing edge of same type
        existing_edge = KnowledgeEdge.objects.filter(
            source_node=source_node,
            target_node=target_node,
            edge_type=edge_type,
            is_active=True
        ).first()
        
        if existing_edge:
            raise serializers.ValidationError(
                f"Edge of type '{edge_type}' already exists between these nodes"
            )
        
        return data


class ConceptRelationSerializer(serializers.ModelSerializer):
    """Serializer for ConceptRelation model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    related_nodes_detail = KnowledgeNodeSerializer(
        source='related_nodes', 
        many=True, 
        read_only=True
    )
    
    class Meta:
        model = ConceptRelation
        fields = [
            'id', 'concept_a', 'concept_b', 'relation_type', 'domain',
            'description', 'confidence_score', 'related_nodes',
            'related_nodes_detail', 'created_by', 'created_by_username',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'created_by_username', 'related_nodes_detail'
        ]


class LearningGraphNodeSerializer(serializers.ModelSerializer):
    """Serializer for LearningGraphNode through model"""
    
    knowledge_node_detail = KnowledgeNodeSerializer(source='knowledge_node', read_only=True)
    knowledge_node_id = serializers.CharField(source='knowledge_node.id', read_only=True)
    knowledge_node_title = serializers.CharField(source='knowledge_node.title', read_only=True)
    
    class Meta:
        model = LearningGraphNode
        fields = [
            'learning_graph', 'knowledge_node', 'knowledge_node_id', 'knowledge_node_title',
            'knowledge_node_detail', 'display_order', 'is_mandatory', 'node_weight',
            'custom_x', 'custom_y', 'estimated_time', 'prerequisite_score'
        ]
        read_only_fields = ['knowledge_node_detail', 'knowledge_node_id', 'knowledge_node_title']


class LearningGraphEdgeSerializer(serializers.ModelSerializer):
    """Serializer for LearningGraphEdge through model"""
    
    knowledge_edge_detail = KnowledgeEdgeSerializer(source='knowledge_edge', read_only=True)
    knowledge_edge_id = serializers.CharField(source='knowledge_edge.id', read_only=True)
    
    class Meta:
        model = LearningGraphEdge
        fields = [
            'learning_graph', 'knowledge_edge', 'knowledge_edge_id',
            'knowledge_edge_detail', 'display_order', 'is_mandatory',
            'edge_priority', 'unlock_conditions', 'recommended_for', 'custom_path'
        ]
        read_only_fields = ['knowledge_edge_detail', 'knowledge_edge_id']


class LearningGraphSerializer(serializers.ModelSerializer):
    """Serializer for LearningGraph model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    nodes_detail = KnowledgeNodeSerializer(
        source='learninggraphnode_set.knowledge_node',
        many=True,
        read_only=True
    )
    edges_detail = KnowledgeEdgeSerializer(
        source='learninggraphedge_set.knowledge_edge',
        many=True,
        read_only=True
    )
    nodes_count = serializers.IntegerField(source='nodes.count', read_only=True)
    edges_count = serializers.IntegerField(source='edges.count', read_only=True)
    completion_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningGraph
        fields = [
            'id', 'title', 'description', 'graph_type', 'status', 'subject_area',
            'target_audience', 'estimated_duration', 'nodes', 'edges',
            'nodes_detail', 'edges_detail', 'nodes_count', 'edges_count',
            'layout_config', 'view_box', 'adaptive_rules', 'difficulty_progression',
            'completion_rate', 'average_completion_time', 'total_attempts',
            'successful_completions', 'completion_percentage',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'version', 'tags'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at',
            'created_by_username', 'nodes_detail', 'edges_detail',
            'nodes_count', 'edges_count', 'completion_percentage'
        ]
    
    def get_completion_percentage(self, obj):
        """Calculate completion percentage"""
        return obj.get_completion_percentage()
    
    def validate_tags(self, value):
        """Validate tags format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list")
        return value


class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for LearningPath model"""
    
    user_detail = UserSerializer(source='user', read_only=True)
    learning_graph_detail = LearningGraphSerializer(source='learning_graph', read_only=True)
    current_node_detail = KnowledgeNodeSerializer(source='current_node', read_only=True)
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'user', 'user_detail', 'learning_graph', 'learning_graph_detail',
            'title', 'adaptation_type', 'status', 'current_node', 'current_node_detail',
            'completed_nodes', 'progress_percentage', 'started_at', 'completed_at',
            'last_activity', 'total_time_spent', 'performance_metrics', 'adaptation_history'
        ]
        read_only_fields = [
            'id', 'user_detail', 'learning_graph_detail', 'current_node_detail',
            'started_at', 'completed_at', 'last_activity'
        ]
    
    def validate_completed_nodes(self, value):
        """Validate completed nodes format"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Completed nodes must be a list")
        return value


class UserKnowledgeStateSerializer(serializers.ModelSerializer):
    """Serializer for UserKnowledgeState model"""
    
    user_detail = UserSerializer(source='user', read_only=True)
    knowledge_node_detail = KnowledgeNodeSerializer(source='knowledge_node', read_only=True)
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = UserKnowledgeState
        fields = [
            'id', 'user', 'user_detail', 'knowledge_node', 'knowledge_node_detail',
            'mastery_level', 'confidence_score', 'first_exposure', 'last_reviewed',
            'total_time_spent', 'assessment_scores', 'practice_attempts',
            'successful_attempts', 'next_review_date', 'review_interval',
            'learning_velocity', 'difficulty_adjustment', 'success_rate'
        ]
        read_only_fields = [
            'id', 'user_detail', 'knowledge_node_detail', 'first_exposure',
            'last_reviewed', 'success_rate'
        ]
    
    def get_success_rate(self, obj):
        """Calculate success rate"""
        return obj.get_success_rate()


class GraphDataSerializer(serializers.Serializer):
    """Serializer for complete graph data response"""
    
    nodes = KnowledgeNodeSerializer(many=True)
    edges = KnowledgeEdgeSerializer(many=True)
    meta = serializers.DictField()
    
    def create(self, validated_data):
        pass  # Graph data is read-only from API perspective
    
    def update(self, instance, validated_data):
        pass  # Graph data is read-only from API perspective


class TopicGraphSerializer(serializers.Serializer):
    """Serializer for topic-specific graph data"""
    
    topic = serializers.CharField()
    nodes = KnowledgeNodeSerializer(many=True)
    edges = KnowledgeEdgeSerializer(many=True)
    statistics = serializers.DictField()
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass


class ConceptRelationshipsSerializer(serializers.Serializer):
    """Serializer for concept relationship data"""
    
    concept = serializers.CharField()
    related_concepts = serializers.ListField(
        child=serializers.DictField()
    )
    concept_relations = ConceptRelationSerializer(many=True)
    learning_paths = serializers.ListField(
        child=serializers.DictField()
    )
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass


class LearningPathRecommendationSerializer(serializers.Serializer):
    """Serializer for learning path recommendations"""
    
    user_id = serializers.IntegerField()
    learning_paths = LearningPathSerializer(many=True)
    recommendations = serializers.ListField(
        child=serializers.DictField()
    )
    adaptation_suggestions = serializers.ListField(
        child=serializers.DictField()
    )
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass


class GraphAnalyticsSerializer(serializers.Serializer):
    """Serializer for graph analytics data"""
    
    total_nodes = serializers.IntegerField()
    total_edges = serializers.IntegerField()
    node_types = serializers.DictField()
    edge_types = serializers.DictField()
    difficulty_distribution = serializers.DictField()
    completion_statistics = serializers.DictField()
    popular_paths = serializers.ListField(
        child=serializers.DictField()
    )
    
    def create(self, validated_data):
        pass
    
    def update(self, instance, validated_data):
        pass


# Write Operations Serializers

class KnowledgeNodeCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating KnowledgeNode instances"""
    
    class Meta:
        model = KnowledgeNode
        fields = [
            'title', 'description', 'node_type', 'difficulty_level',
            'x_position', 'y_position', 'z_position', 'width', 'height',
            'content_uri', 'jac_code', 'learning_objectives', 'prerequisites'
        ]
    
    def validate_learning_objectives(self, value):
        """Validate learning objectives"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Learning objectives must be a list")
        return value


class LearningPathUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating LearningPath instances"""
    
    class Meta:
        model = LearningPath
        fields = [
            'status', 'current_node', 'completed_nodes', 'progress_percentage',
            'performance_metrics', 'adaptation_history'
        ]
    
    def validate_completed_nodes(self, value):
        """Validate completed nodes"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Completed nodes must be a list")
        return value
    
    def validate_progress_percentage(self, value):
        """Validate progress percentage"""
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Progress percentage must be between 0 and 100")
        return value


class UserKnowledgeStateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating UserKnowledgeState instances"""
    
    class Meta:
        model = UserKnowledgeState
        fields = [
            'mastery_level', 'confidence_score', 'practice_attempts',
            'successful_attempts', 'difficulty_adjustment'
        ]


class GraphSearchSerializer(serializers.Serializer):
    """Serializer for graph search queries"""
    
    query = serializers.CharField(help_text="Search query string")
    node_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Filter by node types"
    )
    difficulty_levels = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        help_text="Filter by difficulty levels"
    )
    max_results = serializers.IntegerField(
        default=50,
        help_text="Maximum number of results to return"
    )
    
    def validate_node_types(self, value):
        """Validate node types filter"""
        valid_types = dict(KnowledgeNode.NODE_TYPES).keys()
        for node_type in value:
            if node_type not in valid_types:
                raise serializers.ValidationError(f"Invalid node type: {node_type}")
        return value
    
    def validate_difficulty_levels(self, value):
        """Validate difficulty levels filter"""
        valid_levels = dict(KnowledgeNode.DIFFICULTY_LEVELS).keys()
        for level in value:
            if level not in valid_levels:
                raise serializers.ValidationError(f"Invalid difficulty level: {level}")
        return value


class LearningPathGenerateSerializer(serializers.Serializer):
    """Serializer for learning path generation requests"""
    
    user_id = serializers.IntegerField()
    learning_graph_id = serializers.CharField()
    adaptation_type = serializers.ChoiceField(
        choices=LearningPath.ADAPTATION_TYPES,
        default='adaptive'
    )
    preferences = serializers.DictField(
        required=False,
        help_text="User preferences for path generation"
    )
    constraints = serializers.DictField(
        required=False,
        help_text="Constraints for path generation"
    )
    
    def validate_learning_graph_id(self, value):
        """Validate learning graph ID"""
        try:
            LearningGraph.objects.get(id=value)
        except LearningGraph.DoesNotExist:
            raise serializers.ValidationError("Learning graph not found")
        return value