"""
OSP-based Knowledge Graph Models for JAC Learning Platform

This module implements Object-Spatial Programming (OSP) concepts for knowledge
representation and adaptive learning paths in the JAC Learning Platform.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid
import json


class KnowledgeNode(models.Model):
    """
    Represents a knowledge node in the OSP-based knowledge graph.
    
    Each node represents a concept, skill, or learning objective in the
    knowledge graph structure.
    """
    
    NODE_TYPES = (
        ('concept', 'Concept'),
        ('skill', 'Skill'),
        ('topic', 'Topic'),
        ('objective', 'Learning Objective'),
        ('assessment', 'Assessment'),
        ('resource', 'Learning Resource'),
    )
    
    DIFFICULTY_LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text="Human-readable title for this knowledge node")
    description = models.TextField(blank=True, help_text="Detailed description of the knowledge concept")
    node_type = models.CharField(max_length=20, choices=NODE_TYPES, help_text="Type of knowledge node")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    
    # OSP Spatial Properties
    x_position = models.FloatField(default=0.0, help_text="X coordinate for spatial positioning")
    y_position = models.FloatField(default=0.0, help_text="Y coordinate for spatial positioning")
    z_position = models.FloatField(default=0.0, help_text="Z coordinate for spatial positioning (layer)")
    width = models.FloatField(default=1.0, help_text="Visual width in graph space")
    height = models.FloatField(default=1.0, help_text="Visual height in graph space")
    
    # Content Properties
    content_uri = models.CharField(max_length=500, blank=True, help_text="URI to related content")
    jac_code = models.TextField(blank=True, help_text="Associated JAC code if applicable")
    learning_objectives = models.JSONField(default=list, blank=True, help_text="List of learning objectives")
    prerequisites = models.JSONField(default=list, blank=True, help_text="Required prior knowledge")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0, help_text="Number of times this node has been viewed")
    
    class Meta:
        db_table = 'knowledge_node'
        ordering = ['title']
        indexes = [
            models.Index(fields=['node_type']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_active']),
            models.Index(fields=['x_position', 'y_position']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.node_type})"
    
    def increment_view_count(self):
        """Increment the view count for this knowledge node"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class KnowledgeEdge(models.Model):
    """
    Represents relationships between knowledge nodes in the OSP graph.
    
    Edges define the connections and relationships between different
    knowledge concepts, enabling pathfinding and learning flow.
    """
    
    EDGE_TYPES = (
        ('prerequisite', 'Prerequisite - Must learn before'),
        ('related', 'Related - Connected concepts'),
        ('example', 'Example - Shows application of'),
        ('depends_on', 'Depends On - Requires understanding of'),
        ('leads_to', 'Leads To - Next logical step'),
        ('contradicts', 'Contradicts - Opposite concepts'),
        ('similar_to', 'Similar To - Related concepts'),
        ('part_of', 'Part Of - Component of larger concept'),
        ('contains', 'Contains - Includes sub-concepts'),
    )
    
    STRENGTH_LEVELS = (
        ('weak', 'Weak Connection'),
        ('moderate', 'Moderate Connection'),
        ('strong', 'Strong Connection'),
        ('essential', 'Essential Connection'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_node = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE, related_name='outgoing_edges')
    target_node = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE, related_name='incoming_edges')
    edge_type = models.CharField(max_length=20, choices=EDGE_TYPES)
    strength = models.CharField(max_length=20, choices=STRENGTH_LEVELS, default='moderate')
    
    # OSP Spatial Properties
    curve_points = models.JSONField(default=list, help_text="Control points for curved edges")
    edge_weight = models.FloatField(default=1.0, help_text="Numerical weight for pathfinding algorithms")
    
    # Relationship Metadata
    description = models.TextField(blank=True, help_text="Description of the relationship")
    examples = models.JSONField(default=list, blank=True, help_text="Examples illustrating this relationship")
    
    # Analytics
    traversal_count = models.IntegerField(default=0, help_text="Number of times this edge has been traversed")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'knowledge_edge'
        unique_together = ['source_node', 'target_node', 'edge_type']
        ordering = ['-traversal_count', 'edge_type']
        indexes = [
            models.Index(fields=['source_node']),
            models.Index(fields=['target_node']),
            models.Index(fields=['edge_type']),
            models.Index(fields=['strength']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.source_node.title} → {self.target_node.title} ({self.edge_type})"
    
    def increment_traversal(self):
        """Increment traversal count when this edge is used in learning path"""
        self.traversal_count += 1
        self.save(update_fields=['traversal_count'])


class ConceptRelation(models.Model):
    """
    High-level concept relationships that span across multiple knowledge nodes.
    
    These represent semantic relationships between abstract concepts rather
    than just direct node connections.
    """
    
    RELATION_TYPES = (
        ('inherits', 'Inheritance - Concept A inherits from B'),
        ('implements', 'Implementation - A implements B'),
        ('depends', 'Dependency - A depends on B'),
        ('conflicts', 'Conflict - A conflicts with B'),
        ('complements', 'Complement - A complements B'),
        ('alternatives', 'Alternative - A is alternative to B'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concept_a = models.CharField(max_length=200, help_text="First concept in the relationship")
    concept_b = models.CharField(max_length=200, help_text="Second concept in the relationship")
    relation_type = models.CharField(max_length=20, choices=RELATION_TYPES)
    
    # Context and Description
    domain = models.CharField(max_length=100, help_text="Domain this relationship applies to")
    description = models.TextField(help_text="Explanation of the relationship")
    confidence_score = models.FloatField(
        default=0.8,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence score for this relationship (0.0 to 1.0)"
    )
    
    # Linked Nodes
    related_nodes = models.ManyToManyField(KnowledgeNode, blank=True, help_text="Knowledge nodes that demonstrate this relationship")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'concept_relation'
        unique_together = ['concept_a', 'concept_b', 'relation_type', 'domain']
        ordering = ['domain', 'relation_type', 'concept_a']
        indexes = [
            models.Index(fields=['relation_type']),
            models.Index(fields=['domain']),
            models.Index(fields=['confidence_score']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.concept_a} {self.relation_type} {self.concept_b} ({self.domain})"


class LearningGraph(models.Model):
    """
    Complete learning graphs that represent comprehensive knowledge structures.
    
    Each learning graph represents a coherent set of knowledge nodes and edges
    that form a complete learning path or curriculum section.
    """
    
    GRAPH_TYPES = (
        ('course', 'Complete Course Curriculum'),
        ('module', 'Learning Module'),
        ('topic', 'Topic-Specific Graph'),
        ('skill_tree', 'Skill Development Tree'),
        ('concept_map', 'Concept Relationship Map'),
        ('assessment_path', 'Assessment Preparation Path'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Draft - Under Development'),
        ('active', 'Active - Available for Learning'),
        ('archived', 'Archived - No Longer Active'),
        ('review', 'In Review - Being Evaluated'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, help_text="Title of the learning graph")
    description = models.TextField(help_text="Comprehensive description of this learning graph")
    graph_type = models.CharField(max_length=20, choices=GRAPH_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Content and Scope
    subject_area = models.CharField(max_length=100, help_text="Primary subject area")
    target_audience = models.CharField(max_length=100, help_text="Intended audience level")
    estimated_duration = models.DurationField(null=True, blank=True, help_text="Estimated time to complete")
    
    # Knowledge Structure
    nodes = models.ManyToManyField(KnowledgeNode, through='LearningGraphNode', blank=True)
    edges = models.ManyToManyField(KnowledgeEdge, through='LearningGraphEdge', blank=True)
    
    # Graph Properties (OSP Spatial Layout)
    layout_config = models.JSONField(default=dict, help_text="Configuration for graph visualization layout")
    view_box = models.JSONField(default=dict, help_text="View box coordinates for graph display")
    
    # Adaptive Learning Configuration
    adaptive_rules = models.JSONField(default=dict, help_text="Rules for adaptive path generation")
    difficulty_progression = models.JSONField(default=list, help_text="Configured difficulty progression path")
    
    # Analytics and Tracking
    completion_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    average_completion_time = models.DurationField(null=True, blank=True)
    total_attempts = models.IntegerField(default=0)
    successful_completions = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=20, default='1.0.0')
    tags = models.JSONField(default=list, help_text="Tags for categorization and search")
    
    class Meta:
        db_table = 'learning_graph'
        ordering = ['title']
        indexes = [
            models.Index(fields=['graph_type']),
            models.Index(fields=['status']),
            models.Index(fields=['subject_area']),
            models.Index(fields=['target_audience']),
            models.Index(fields=['completion_rate']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.graph_type})"
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on attempts vs successful completions"""
        if self.total_attempts == 0:
            return 0.0
        return (self.successful_completions / self.total_attempts) * 100
    
    def update_analytics(self):
        """Update analytics based on learning progress"""
        self.completion_rate = self.get_completion_percentage()
        self.save(update_fields=['completion_rate', 'updated_at'])


class LearningGraphNode(models.Model):
    """
    Through model for many-to-many relationship between LearningGraph and KnowledgeNode.
    Includes additional metadata specific to the node's role in this graph.
    """
    
    learning_graph = models.ForeignKey(LearningGraph, on_delete=models.CASCADE)
    knowledge_node = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE)
    
    # Node-specific metadata in this graph context
    display_order = models.IntegerField(default=0, help_text="Order for sequential display")
    is_mandatory = models.BooleanField(default=True, help_text="Whether this node is required for completion")
    node_weight = models.FloatField(default=1.0, help_text="Importance weight in this graph")
    
    # Visual properties specific to this graph
    custom_x = models.FloatField(null=True, blank=True, help_text="Custom X position for this node in this graph")
    custom_y = models.FloatField(null=True, blank=True, help_text="Custom Y position for this node in this graph")
    
    # Learning path metadata
    estimated_time = models.DurationField(null=True, blank=True, help_text="Time estimated to learn this node")
    prerequisite_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Score required before this node becomes available"
    )
    
    class Meta:
        db_table = 'learning_graph_node'
        unique_together = ['learning_graph', 'knowledge_node']
        ordering = ['display_order', 'knowledge_node__title']
        indexes = [
            models.Index(fields=['learning_graph']),
            models.Index(fields=['knowledge_node']),
            models.Index(fields=['display_order']),
            models.Index(fields=['is_mandatory']),
        ]
    
    def __str__(self):
        return f"{self.learning_graph.title} → {self.knowledge_node.title}"


class LearningGraphEdge(models.Model):
    """
    Through model for many-to-many relationship between LearningGraph and KnowledgeEdge.
    Includes metadata specific to the edge's role in this learning graph.
    """
    
    learning_graph = models.ForeignKey(LearningGraph, on_delete=models.CASCADE)
    knowledge_edge = models.ForeignKey(KnowledgeEdge, on_delete=models.CASCADE)
    
    # Edge-specific metadata in this graph context
    display_order = models.IntegerField(default=0, help_text="Order for display")
    is_mandatory = models.BooleanField(default=False, help_text="Whether this edge must be traversed")
    edge_priority = models.IntegerField(default=1, help_text="Priority for pathfinding (lower = higher priority)")
    
    # Adaptive learning rules
    unlock_conditions = models.JSONField(default=dict, help_text="Conditions that must be met before this edge becomes available")
    recommended_for = models.JSONField(default=list, help_text="User profiles this edge is recommended for")
    
    # Visual properties
    custom_path = models.JSONField(default=list, help_text="Custom path points for this edge in this graph")
    
    class Meta:
        db_table = 'learning_graph_edge'
        unique_together = ['learning_graph', 'knowledge_edge']
        ordering = ['display_order', 'edge_priority']
        indexes = [
            models.Index(fields=['learning_graph']),
            models.Index(fields=['knowledge_edge']),
            models.Index(fields=['display_order']),
            models.Index(fields=['edge_priority'], name='edge_priority_idx'),
        ]
    
    def __str__(self):
        return f"{self.learning_graph.title} → {self.knowledge_edge}"


class LearningPath(models.Model):
    """
    Generated learning paths for individual users based on their progress and goals.
    
    These represent adaptive, personalized sequences of knowledge nodes that
    guide users through their learning journey.
    """
    
    PATH_STATUS = (
        ('active', 'Active - Currently Following'),
        ('completed', 'Completed Successfully'),
        ('paused', 'Paused - Temporarily Stopped'),
        ('abandoned', 'Abandoned - No Longer Following'),
        ('failed', 'Failed - Unable to Complete'),
    )
    
    ADAPTATION_TYPES = (
        ('static', 'Static - Fixed Path'),
        ('adaptive', 'Adaptive - Adjusts Based on Performance'),
        ('personalized', 'Personalized - Based on User Profile'),
        ('ai_generated', 'AI Generated - ML-Optimized'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="User following this learning path")
    learning_graph = models.ForeignKey(LearningGraph, on_delete=models.CASCADE, help_text="Source learning graph")
    
    # Path Configuration
    title = models.CharField(max_length=200, help_text="Title for this specific learning path")
    adaptation_type = models.CharField(max_length=20, choices=ADAPTATION_TYPES, default='adaptive')
    status = models.CharField(max_length=20, choices=PATH_STATUS, default='active')
    
    # Progress Tracking
    current_node = models.ForeignKey(
        KnowledgeNode, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Node the user is currently working on"
    )
    completed_nodes = models.JSONField(default=list, help_text="List of completed node IDs")
    progress_percentage = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Overall completion percentage"
    )
    
    # Path Metadata
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)
    total_time_spent = models.DurationField(default=timezone.timedelta)
    
    # Adaptive Learning Data
    performance_metrics = models.JSONField(default=dict, help_text="User performance data for path adaptation")
    adaptation_history = models.JSONField(default=list, help_text="History of path adaptations made")
    
    class Meta:
        db_table = 'learning_path'
        ordering = ['-last_activity']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['learning_graph']),
            models.Index(fields=['status']),
            models.Index(fields=['adaptation_type']),
            models.Index(fields=['progress_percentage']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.progress_percentage:.1f}%)"
    
    def update_progress(self, completed_node_id):
        """Update learning path progress when a node is completed"""
        if completed_node_id not in self.completed_nodes:
            self.completed_nodes.append(completed_node_id)
            self.update_progress_percentage()
            self.last_activity = timezone.now()
            self.save(update_fields=['completed_nodes', 'progress_percentage', 'last_activity'])
    
    def update_progress_percentage(self):
        """Calculate and update the overall progress percentage"""
        total_nodes = self.learning_graph.nodes.count()
        if total_nodes > 0:
            self.progress_percentage = (len(self.completed_nodes) / total_nodes) * 100
        
        # Mark as completed if all mandatory nodes are done
        mandatory_nodes = self.learning_graph.learninggraphnode_set.filter(is_mandatory=True).count()
        completed_mandatory = len([
            node for node in self.completed_nodes 
            if self.learning_graph.learninggraphnode_set.filter(
                knowledge_node_id=node,
                is_mandatory=True
            ).exists()
        ])
        
        if mandatory_nodes > 0 and completed_mandatory >= mandatory_nodes:
            if self.status == 'active':
                self.status = 'completed'
                self.completed_at = timezone.now()
    
    def add_time_spent(self, duration):
        """Add time spent learning to the total"""
        self.total_time_spent += duration
        self.last_activity = timezone.now()
        self.save(update_fields=['total_time_spent', 'last_activity'])


class UserKnowledgeState(models.Model):
    """
    Tracks individual user's knowledge state and mastery levels across concepts.
    
    This enables personalized learning paths and adaptive recommendations
    based on user's demonstrated understanding.
    """
    
    MASTERY_LEVELS = (
        ('novice', 'Novice - No Understanding'),
        ('beginner', 'Beginner - Basic Awareness'),
        ('developing', 'Developing - Growing Understanding'),
        ('proficient', 'Proficient - Good Understanding'),
        ('expert', 'Expert - Deep Understanding'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="User whose knowledge state is being tracked")
    knowledge_node = models.ForeignKey(KnowledgeNode, on_delete=models.CASCADE, help_text="Knowledge concept being tracked")
    
    # Knowledge State
    mastery_level = models.CharField(max_length=20, choices=MASTERY_LEVELS, default='novice')
    confidence_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Confidence in mastery level (0.0 to 1.0)"
    )
    
    # Learning Analytics
    first_exposure = models.DateTimeField(default=timezone.now, help_text="When user first encountered this concept")
    last_reviewed = models.DateTimeField(default=timezone.now, help_text="Last time this concept was reviewed")
    total_time_spent = models.DurationField(default=timezone.timedelta, help_text="Total time spent learning this concept")
    
    # Performance Metrics
    assessment_scores = models.JSONField(default=list, help_text="Scores from assessments on this concept")
    practice_attempts = models.IntegerField(default=0, help_text="Number of practice attempts")
    successful_attempts = models.IntegerField(default=0, help_text="Number of successful practice attempts")
    
    # Spaced Repetition
    next_review_date = models.DateTimeField(null=True, blank=True, help_text="Next scheduled review for spaced repetition")
    review_interval = models.DurationField(default=timezone.timedelta(days=1), help_text="Current review interval")
    
    # Adaptive Learning Data
    learning_velocity = models.FloatField(default=0.0, help_text="Rate of learning progress for this concept")
    difficulty_adjustment = models.FloatField(default=0.0, help_text="Difficulty adjustment factor based on performance")
    
    class Meta:
        db_table = 'user_knowledge_state'
        unique_together = ['user', 'knowledge_node']
        ordering = ['user', 'knowledge_node__title']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['knowledge_node']),
            models.Index(fields=['mastery_level']),
            models.Index(fields=['confidence_score']),
            models.Index(fields=['next_review_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.knowledge_node.title} ({self.mastery_level})"
    
    def update_mastery(self, new_mastery_level, confidence=None):
        """Update user's mastery level for this concept"""
        self.mastery_level = new_mastery_level
        if confidence is not None:
            self.confidence_score = confidence
        self.last_reviewed = timezone.now()
        
        # Calculate learning velocity
        time_diff = self.last_reviewed - self.first_exposure
        if time_diff.total_seconds() > 0:
            mastery_scores = {'novice': 1, 'beginner': 2, 'developing': 3, 'proficient': 4, 'expert': 5}
            current_score = mastery_scores.get(new_mastery_level, 1)
            self.learning_velocity = current_score / (time_diff.days + 1)
        
        self.save(update_fields=['mastery_level', 'confidence_score', 'last_reviewed', 'learning_velocity'])
    
    def add_assessment_score(self, score, max_score=100):
        """Add an assessment score and update metrics"""
        normalized_score = score / max_score if max_score > 0 else 0.0
        self.assessment_scores.append({
            'score': score,
            'max_score': max_score,
            'normalized_score': normalized_score,
            'timestamp': timezone.now().isoformat()
        })
        
        # Update confidence based on recent assessments
        if len(self.assessment_scores) >= 3:
            recent_scores = [s['normalized_score'] for s in self.assessment_scores[-3:]]
            self.confidence_score = sum(recent_scores) / len(recent_scores)
        
        self.last_reviewed = timezone.now()
        self.save(update_fields=['assessment_scores', 'confidence_score', 'last_reviewed'])
    
    def get_success_rate(self):
        """Calculate success rate for practice attempts"""
        if self.practice_attempts == 0:
            return 0.0
        return (self.successful_attempts / self.practice_attempts) * 100