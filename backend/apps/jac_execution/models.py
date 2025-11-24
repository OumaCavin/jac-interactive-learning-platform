"""
Models for JAC Code Execution

This module defines the database models for managing code execution requests,
results, and execution history in the JAC Learning Platform.
"""

from django.db import models
from django.utils import timezone
import uuid
import json

# Use lazy import to avoid circular dependencies
def get_user_model():
    """Get the user model, deferring import to avoid circular dependencies."""
    from django.contrib.auth import get_user_model
    return get_user_model()


class CodeExecution(models.Model):
    """
    Model for tracking code execution requests and results.
    """
    
    LANGUAGE_CHOICES = [
        ('jac', 'JAC'),
        ('python', 'Python'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('timeout', 'Timeout'),
        ('error', 'Error'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('django.contrib.auth.get_user_model()', on_delete=models.CASCADE, related_name='code_executions')
    
    # Code execution details
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='python')
    code = models.TextField()
    stdin = models.TextField(blank=True, null=True)
    
    # Execution results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stdout = models.TextField(blank=True, null=True)
    stderr = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    return_code = models.IntegerField(null=True, blank=True)
    
    # Execution metadata
    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Security and limits
    max_execution_time = models.FloatField(default=5.0)  # seconds
    max_memory = models.IntegerField(default=64)  # MB
    max_output_size = models.IntegerField(default=10240)  # bytes
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Code Execution'
        verbose_name_plural = 'Code Executions'
    
    def __str__(self):
        return f"{self.language} execution by {self.user.username} at {self.created_at}"
    
    @property
    def is_completed(self):
        """Check if execution is completed (successfully or with errors)."""
        return self.status in ['completed', 'failed', 'timeout', 'error']
    
    @property
    def is_successful(self):
        """Check if execution completed successfully."""
        return self.status == 'completed' and self.return_code == 0
    
    def get_execution_summary(self):
        """Get a summary of the execution results."""
        if not self.is_completed:
            return {"status": self.status, "message": "Execution in progress"}
        
        return {
            "status": self.status,
            "language": self.language,
            "execution_time": self.execution_time,
            "return_code": self.return_code,
            "output_length": len(self.stdout or ""),
            "error_length": len(self.stderr or ""),
            "memory_usage": self.memory_usage
        }


class ExecutionTemplate(models.Model):
    """
    Model for storing reusable code templates and examples.
    """
    
    LANGUAGE_CHOICES = [
        ('jac', 'JAC'),
        ('python', 'Python'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    stdin = models.TextField(blank=True, null=True)
    
    # Template metadata
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('django.contrib.auth.get_user_model()', on_delete=models.CASCADE, related_name='execution_templates')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Categories and tags
    category = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Execution Template'
        verbose_name_plural = 'Execution Templates'
    
    def __str__(self):
        return f"{self.name} ({self.language})"
    
    @property
    def tag_list(self):
        """Get tags as a list of strings."""
        return self.tags if isinstance(self.tags, list) else []


class CodeExecutionSession(models.Model):
    """
    Model for tracking user execution sessions and analytics.
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('django.contrib.auth.get_user_model()', on_delete=models.CASCADE, related_name='execution_sessions')
    session_id = models.CharField(max_length=255, unique=True)
    
    # Session statistics
    total_executions = models.IntegerField(default=0)
    successful_executions = models.IntegerField(default=0)
    failed_executions = models.IntegerField(default=0)
    total_execution_time = models.FloatField(default=0.0)
    
    # Session metadata
    started_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Execution Session'
        verbose_name_plural = 'Execution Sessions'
    
    def __str__(self):
        return f"Session {self.session_id} by {self.user.username}"
    
    @property
    def success_rate(self):
        """Calculate success rate as a percentage."""
        if self.total_executions == 0:
            return 0
        return (self.successful_executions / self.total_executions) * 100
    
    def update_statistics(self, execution):
        """Update session statistics based on execution results."""
        self.total_executions += 1
        
        if execution.return_code == 0 and execution.status == 'completed':
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        if execution.execution_time:
            self.total_execution_time += execution.execution_time
        
        self.save()


class SecuritySettings(models.Model):
    """
    Model for global security settings and execution limits.
    """
    
    id = models.AutoField(primary_key=True)
    
    # Execution limits
    max_execution_time = models.FloatField(default=5.0)
    max_memory = models.IntegerField(default=64)
    max_output_size = models.IntegerField(default=10240)
    max_code_size = models.IntegerField(default=102400)  # bytes
    
    # Security settings
    allowed_languages = models.JSONField(default=list)
    enable_sandboxing = models.BooleanField(default=True)
    enable_network_access = models.BooleanField(default=False)
    
    # Rate limiting
    max_executions_per_minute = models.IntegerField(default=60)
    max_executions_per_hour = models.IntegerField(default=1000)
    
    # Blocked imports for Python
    blocked_imports = models.JSONField(default=list)
    blocked_functions = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Security Settings'
        verbose_name_plural = 'Security Settings'
    
    def __str__(self):
        return f"Security Settings (Updated: {self.updated_at})"