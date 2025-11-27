# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Agent Models for Django backend

These models track agent instances, tasks, communications, and metrics
in the JAC Interactive Learning Platform.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from enum import Enum
import uuid


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


class Agent(models.Model):
    """Model representing an AI agent instance"""
    
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'agents'
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


class Task(models.Model):
    """Model representing tasks assigned to agents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_id = models.CharField(max_length=100, unique=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tasks')
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
        User, 
        on_delete=models.CASCADE, 
        related_name='assigned_tasks'
    )
    assigned_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'tasks'
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


class AgentCommunication(models.Model):
    """Model for tracking communication between agents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        related_name='sent_communications'
    )
    receiver_agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        related_name='received_communications'
    )
    message_type = models.CharField(max_length=50)
    content = models.JSONField()
    task_reference = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name='communications',
        null=True, 
        blank=True
    )
    sent_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    is_urgent = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'agent_communications'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sender_agent', 'receiver_agent']),
            models.Index(fields=['message_type']),
            models.Index(fields=['sent_at']),
        ]
    
    def __str__(self):
        return f"{self.sender_agent.name} → {self.receiver_agent.name}: {self.message_type}"


class AgentMetrics(models.Model):
    """Model for tracking agent performance metrics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='metrics')
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    metric_type = models.CharField(max_length=50)
    context = models.JSONField(default=dict, blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'agent_metrics'
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['agent', 'metric_name']),
            models.Index(fields=['recorded_at']),
        ]
    
    def __str__(self):
        return f"{self.agent.name}: {self.metric_name} = {self.metric_value}"


class LearningSession(models.Model):
    """Model for tracking learning sessions involving multiple agents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_sessions')
    agents_involved = models.ManyToManyField(Agent, related_name='learning_sessions')
    session_type = models.CharField(max_length=50)
    learning_path = models.ForeignKey(
        'learning.LearningPath',
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    session_data = models.JSONField(default=dict, blank=True)
    performance_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True, 
        blank=True
    )
    
    class Meta:
        db_table = 'learning_sessions'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'session_type']),
            models.Index(fields=['started_at']),
        ]
    
    def __str__(self):
        return f"Session: {self.session_id} ({self.user.username})"
    
    @property
    def duration(self):
        """Calculate session duration in seconds"""
        end_time = self.ended_at or timezone.now()
        return (end_time - self.started_at).total_seconds()
    
    @property
    def is_active(self):
        return self.ended_at is None