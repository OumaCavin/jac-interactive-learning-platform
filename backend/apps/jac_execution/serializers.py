"""
Serializers for JAC Code Execution API

This module defines the DRF serializers for converting Django model instances
to JSON and validating input data for the code execution API.
"""

from rest_framework import serializers
from .models import CodeExecution, ExecutionTemplate, CodeExecutionSession, SecuritySettings
import re
import json


class CodeExecutionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating code execution requests.
    """
    
    class Meta:
        model = CodeExecution
        fields = ['language', 'code', 'stdin']
        extra_kwargs = {
            'code': {'required': True, 'min_length': 1},
            'language': {'required': False, 'default': 'python'},
        }
    
    def validate_code(self, value):
        """Validate code length and content."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Code cannot be empty")
        
        # Get global security settings
        try:
            settings = SecuritySettings.objects.get(pk=1)
            if len(value) > settings.max_code_size:
                raise serializers.ValidationError(
                    f"Code size exceeds maximum allowed size of {settings.max_code_size} bytes"
                )
        except SecuritySettings.DoesNotExist:
            # Use default limits if settings don't exist
            if len(value) > 102400:  # 100KB default
                raise serializers.ValidationError("Code size exceeds maximum allowed size")
        
        return value
    
    def validate_language(self, value):
        """Validate supported languages."""
        allowed_languages = ['jac', 'python']
        if value not in allowed_languages:
            raise serializers.ValidationError(
                f"Unsupported language. Allowed languages: {', '.join(allowed_languages)}"
            )
        return value


class CodeExecutionResultSerializer(serializers.ModelSerializer):
    """
    Serializer for code execution results.
    """
    
    execution_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = CodeExecution
        fields = [
            'id', 'language', 'code', 'stdin', 'status',
            'stdout', 'stderr', 'return_code',
            'execution_time', 'memory_usage',
            'created_at', 'completed_at',
            'execution_summary'
        ]
        read_only_fields = fields
    
    def get_execution_summary(self, obj):
        """Get execution summary for display."""
        return obj.get_execution_summary()


class CodeExecutionStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for execution status updates.
    """
    
    class Meta:
        model = CodeExecution
        fields = ['id', 'status', 'execution_time', 'completed_at']
        read_only_fields = ['id', 'status', 'execution_time', 'completed_at']


class ExecutionTemplateListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing execution templates.
    """
    
    creator_name = serializers.CharField(source='created_by.username', read_only=True)
    tag_list = serializers.ListField(source='get_tag_list', read_only=True)
    
    class Meta:
        model = ExecutionTemplate
        fields = [
            'id', 'name', 'description', 'language',
            'is_public', 'category', 'tags',
            'creator_name', 'created_at', 'updated_at',
            'tag_list'
        ]
        read_only_fields = fields


class ExecutionTemplateDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed execution template view.
    """
    
    creator_name = serializers.CharField(source='created_by.username', read_only=True)
    tag_list = serializers.ListField(source='get_tag_list', read_only=True)
    
    class Meta:
        model = ExecutionTemplate
        fields = [
            'id', 'name', 'description', 'language', 'code', 'stdin',
            'is_public', 'category', 'tags',
            'creator_name', 'created_at', 'updated_at',
            'tag_list'
        ]
        read_only_fields = fields


class ExecutionTemplateCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating execution templates.
    """
    
    class Meta:
        model = ExecutionTemplate
        fields = [
            'name', 'description', 'language', 'code', 'stdin',
            'is_public', 'category', 'tags'
        ]
        extra_kwargs = {
            'name': {'required': True, 'max_length': 255},
            'description': {'required': True},
            'code': {'required': True},
            'language': {'required': True},
            'tags': {'required': False, 'default': []},
        }
    
    def validate_tags(self, value):
        """Validate and clean tags."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Tags must be a list of strings")
        
        # Clean and validate tags
        cleaned_tags = []
        for tag in value:
            if isinstance(tag, str) and tag.strip():
                # Clean tag: lowercase, remove special chars except hyphens
                clean_tag = re.sub(r'[^a-zA-Z0-9\-_]', '', tag.strip().lower())
                if clean_tag and clean_tag not in cleaned_tags:
                    cleaned_tags.append(clean_tag)
        
        return cleaned_tags
    
    def validate_code(self, value):
        """Validate template code length."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Code cannot be empty")
        return value


class CodeExecutionSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for execution session statistics.
    """
    
    success_rate = serializers.ReadOnlyField()
    average_execution_time = serializers.SerializerMethodField()
    
    class Meta:
        model = CodeExecutionSession
        fields = [
            'id', 'session_id', 'total_executions', 'successful_executions',
            'failed_executions', 'total_execution_time', 'success_rate',
            'average_execution_time', 'started_at', 'last_activity',
            'is_active'
        ]
        read_only_fields = fields
    
    def get_average_execution_time(self, obj):
        """Calculate average execution time."""
        if obj.total_executions == 0:
            return 0.0
        return obj.total_execution_time / obj.total_executions


class SecuritySettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for security settings configuration.
    """
    
    class Meta:
        model = SecuritySettings
        fields = [
            'id', 'max_execution_time', 'max_memory', 'max_output_size',
            'max_code_size', 'allowed_languages', 'enable_sandboxing',
            'enable_network_access', 'max_executions_per_minute',
            'max_executions_per_hour', 'blocked_imports', 'blocked_functions',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuickExecutionSerializer(serializers.Serializer):
    """
    Serializer for quick code execution without storing in database.
    """
    
    language = serializers.ChoiceField(choices=[('jac', 'JAC'), ('python', 'Python')])
    code = serializers.CharField()
    stdin = serializers.CharField(required=False, allow_blank=True)
    
    def validate_code(self, value):
        """Validate code for quick execution."""
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Code cannot be empty")
        
        # Quick execution has stricter limits
        if len(value) > 50000:  # 50KB for quick execution
            raise serializers.ValidationError("Code size exceeds quick execution limit")
        
        return value


class ExecutionHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for execution history with filtering options.
    """
    
    execution_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = CodeExecution
        fields = [
            'id', 'language', 'status', 'execution_time',
            'created_at', 'execution_summary'
        ]
        read_only_fields = fields
    
    def get_execution_summary(self, obj):
        """Get concise execution summary."""
        return {
            "status": obj.status,
            "execution_time": obj.execution_time,
            "language": obj.language,
            "has_output": bool(obj.stdout),
            "has_error": bool(obj.stderr)
        }