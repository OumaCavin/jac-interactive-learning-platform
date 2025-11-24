"""
Simplified Agent Models for Django backend (without external dependencies)

These models track basic agent instances without dependencies on other apps.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from enum import Enum
import uuid

# Defer user model import to avoid AppRegistryNotReady errors
def get_user_model():
    """Get the user model, deferring import to avoid circular dependencies."""
    from django.contrib.auth import get_user_model
    return get_user_model()

User = None  # Will be set lazily


class AgentType(models.TextChoices):
    """Types of agents available in the system"""
    CONTENT_CURATOR = 'content_curator', 'Content Curator'
    QUIZ_MASTER = 'quiz_master', 'Quiz Master'
    EVALUATOR = 'evaluator', 'Evaluator'
    PROGRESS_TRACKER = 'progress_tracker', 'Progress Tracker'
    MOTIVATOR = 'motivator', 'Motivator'
    SYSTEM_ORCHESTRATOR = 'system_orchestrator', 'System Orchestrator'


class TaskStatus(models.TextChoices):
    """Task status options"""
    PENDING = 'pending', 'Pending'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    CANCELLED = 'cancelled', 'Cancelled'


class TaskPriority(models.TextChoices):
    """Task priority levels"""
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    CRITICAL = 'critical', 'Critical'


class SimpleAgent(models.Model):
    """Model representing a simplified AI agent instance"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_id = models.CharField(max_length=100, unique=True)
    agent_type = models.CharField(
        max_length=50,
        choices=AgentType.choices,
        db_index=True
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='idle')
    config = models.JSONField(default=dict, blank=True)
    capabilities = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey('django.contrib.auth.get_user_model()', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'simple_agents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['agent_type']),
            models.Index(fields=['status']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.agent_type})"
    
    @property
    def is_idle(self):
        return self.status == 'idle'
    
    @property
    def is_active_agent(self):
        return self.is_active and self.status in ['idle', 'active', 'processing']


class SimpleTask(models.Model):
    """Model representing simplified tasks assigned to agents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_id = models.CharField(max_length=100, unique=True)
    agent = models.ForeignKey(SimpleAgent, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    priority = models.CharField(
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM
    )
    assigned_by = models.ForeignKey(
        'django.contrib.auth.get_user_model()', 
        on_delete=models.CASCADE, 
        related_name='assigned_tasks',
        null=True, 
        blank=True
    )
    assigned_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'simple_tasks'
        ordering = ['-assigned_at', '-priority']
        indexes = [
            models.Index(fields=['agent', 'status']),
            models.Index(fields=['task_type']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_at']),
        ]
    
    def __str__(self):
        return f"Task: {self.title} ({self.status})"
    
    @property
    def duration(self):
        """Calculate task duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    @property
    def is_completed(self):
        return self.status == TaskStatus.COMPLETED
    
    @property
    def has_failed(self):
        return self.status == TaskStatus.FAILED


class SimpleAgentMetrics(models.Model):
    """Model for tracking simplified agent performance metrics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(SimpleAgent, on_delete=models.CASCADE, related_name='metrics')
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    metric_type = models.CharField(max_length=50)
    context = models.JSONField(default=dict, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'simple_agent_metrics'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['agent', 'metric_name']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.agent.name}: {self.metric_name} = {self.metric_value}"


class ChatMessage(models.Model):
    """Model for storing chat conversations with agents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('django.contrib.auth.get_user_model()', on_delete=models.CASCADE, related_name='chat_messages')
    session_id = models.CharField(max_length=100, db_index=True)
    message = models.TextField(help_text='User message')
    response = models.TextField(help_text='Agent response')
    agent_type = models.CharField(
        max_length=50,
        choices=AgentType.choices,
        default=AgentType.SYSTEM_ORCHESTRATOR
    )
    message_type = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User Message'),
            ('agent', 'Agent Response'),
            ('system', 'System Message'),
        ],
        default='user'
    )
    metadata = models.JSONField(default=dict, blank=True, help_text='Additional message metadata')
    feedback_rating = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='User rating from 1-5'
    )
    feedback_comment = models.TextField(blank=True, help_text='User feedback comment')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'chat_messages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'session_id']),
            models.Index(fields=['session_id', 'created_at']),
            models.Index(fields=['agent_type']),
            models.Index(fields=['feedback_rating']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.agent_type} ({self.session_id})"
    
    @property
    def is_user_message(self):
        return self.message_type == 'user'
    
    @property
    def is_agent_response(self):
        return self.message_type == 'agent'
    
    @property
    def rating_stars(self):
        """Return star representation of rating"""
        if self.feedback_rating:
            return '⭐' * self.feedback_rating
        return ''