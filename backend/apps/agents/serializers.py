"""
Agent Serializers for Django REST Framework

Serializers for the agent models and API interactions
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Agent, Task, AgentMetrics
# from .models import Agent, Task, AgentCommunication, AgentMetrics, LearningSession


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent model"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    is_idle = serializers.BooleanField(read_only=True)
    is_active_agent = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Agent
        fields = [
            'id', 'agent_id', 'agent_type', 'name', 'description', 'status',
            'config', 'capabilities', 'created_by', 'created_by_username',
            'created_at', 'last_active', 'is_active', 'is_idle', 'is_active_agent'
        ]
        read_only_fields = ['id', 'created_at', 'last_active', 'is_idle', 'is_active_agent']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    agent_type = serializers.CharField(source='agent.agent_type', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    duration = serializers.FloatField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    has_failed = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'task_id', 'agent', 'agent_name', 'agent_type', 'task_type',
            'title', 'description', 'input_data', 'output_data', 'status',
            'priority', 'assigned_by', 'assigned_by_username', 'assigned_at',
            'started_at', 'completed_at', 'error_message', 'execution_time',
            'duration', 'is_completed', 'has_failed'
        ]
        read_only_fields = [
            'id', 'task_id', 'assigned_at', 'started_at', 'completed_at',
            'duration', 'is_completed', 'has_failed'
        ]


# class AgentCommunicationSerializer(serializers.ModelSerializer):
#     """Serializer for AgentCommunication model"""
    
#     sender_agent_name = serializers.CharField(source='sender_agent.name', read_only=True)
#     receiver_agent_name = serializers.CharField(source='receiver_agent.name', read_only=True)
#     task_title = serializers.CharField(source='task_reference.title', read_only=True)
    
#     class Meta:
#         model = AgentCommunication
#         fields = [
#             'id', 'sender_agent', 'sender_agent_name', 'receiver_agent',
#             'receiver_agent_name', 'message_type', 'content', 'task_reference',
#             'task_title', 'sent_at', 'processed_at', 'is_urgent'
#         ]
#         read_only_fields = ['id', 'sent_at', 'processed_at']


class AgentMetricsSerializer(serializers.ModelSerializer):
    """Serializer for AgentMetrics model"""
    
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    
    class Meta:
        model = AgentMetrics
        fields = [
            'id', 'agent', 'agent_name', 'metric_name', 'metric_value',
            'metric_type', 'context', 'recorded_at'
        ]
        read_only_fields = ['id', 'recorded_at']


# class LearningSessionSerializer(serializers.ModelSerializer):
#     """Serializer for LearningSession model"""
    
#     user_username = serializers.CharField(source='user.username', read_only=True)
#     learning_path_title = serializers.CharField(source='learning_path.title', read_only=True)
#     agents_involved_names = serializers.SerializerMethodField()
#     duration = serializers.FloatField(read_only=True)
#     is_active = serializers.BooleanField(read_only=True)
    
#     class Meta:
#         model = LearningSession
#         fields = [
#             'id', 'session_id', 'user', 'user_username', 'agents_involved',
#             'agents_involved_names', 'session_type', 'learning_path',
#             'learning_path_title', 'started_at', 'ended_at', 'session_data',
#             'performance_score', 'duration', 'is_active'
#         ]
#         read_only_fields = [
#             'id', 'session_id', 'started_at', 'duration', 'is_active'
#         ]
    
#     def get_agents_involved_names(self, obj):
#         """Get names of agents involved in the session"""
#         return [agent.name for agent in obj.agents_involved.all()]


class AgentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new agents"""
    
    class Meta:
        model = Agent
        fields = [
            'agent_id', 'agent_type', 'name', 'description', 'config',
            'capabilities', 'is_active'
        ]
    
    def validate_agent_id(self, value):
        """Validate unique agent ID"""
        if Agent.objects.filter(agent_id=value).exists():
            raise serializers.ValidationError("Agent ID already exists")
        return value
    
    def validate_agent_type(self, value):
        """Validate agent type"""
        valid_types = ['content_curator', 'quiz_master', 'evaluator', 
                      'progress_tracker', 'motivator', 'system_orchestrator']
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid agent type. Must be one of: {', '.join(valid_types)}")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new tasks"""
    
    class Meta:
        model = Task
        fields = [
            'agent', 'task_type', 'title', 'description', 'input_data',
            'priority'
        ]


class AgentStatusSerializer(serializers.Serializer):
    """Serializer for agent status updates"""
    
    status = serializers.ChoiceField(choices=[
        ('idle', 'Idle'),
        ('active', 'Active'),
        ('processing', 'Processing'),
        ('error', 'Error'),
        ('maintenance', 'Maintenance')
    ])
    error_message = serializers.CharField(required=False, allow_blank=True)


class AgentHealthCheckSerializer(serializers.Serializer):
    """Serializer for agent health check response"""
    
    agent_id = serializers.CharField()
    agent_type = serializers.CharField()
    status = serializers.CharField()
    last_active = serializers.DateTimeField()
    queue_size = serializers.IntegerField()
    metrics_count = serializers.IntegerField()
    uptime_hours = serializers.FloatField()


class AgentMetricsQuerySerializer(serializers.Serializer):
    """Serializer for agent metrics queries"""
    
    agent_id = serializers.CharField(required=False)
    agent_type = serializers.CharField(required=False)
    metric_name = serializers.CharField(required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    limit = serializers.IntegerField(default=100, min_value=1, max_value=1000)


# class LearningSessionCreateSerializer(serializers.ModelSerializer):
#     """Serializer for creating learning sessions"""
    
#     class Meta:
#         model = LearningSession
#         fields = [
#             'session_id', 'user', 'agents_involved', 'session_type',
#             'learning_path', 'session_data'
#         ]
    
#     def validate_session_id(self, value):
#         """Validate unique session ID"""
#         if LearningSession.objects.filter(session_id=value).exists():
#             raise serializers.ValidationError("Session ID already exists")
#         return value


class AgentWorkflowSerializer(serializers.Serializer):
    """Serializer for workflow orchestration requests"""
    
    workflow_type = serializers.ChoiceField(choices=[
        ('learning_session', 'Learning Session'),
        ('assessment_flow', 'Assessment Flow'),
        ('progress_review', 'Progress Review'),
        ('content_creation', 'Content Creation'),
        ('adaptive_learning', 'Adaptive Learning')
    ])
    user_id = serializers.IntegerField()
    learning_path_id = serializers.CharField(required=False)
    config = serializers.JSONField(default=dict)


class AgentCoordinationSerializer(serializers.Serializer):
    """Serializer for agent coordination requests"""
    
    task_description = serializers.CharField()
    required_capabilities = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    user_id = serializers.IntegerField()
    strategy = serializers.ChoiceField(
        choices=[
            ('sequential', 'Sequential'),
            ('parallel', 'Parallel'),
            ('hybrid', 'Hybrid')
        ],
        default='sequential'
    )


class AgentSystemMonitorSerializer(serializers.Serializer):
    """Serializer for system monitoring requests"""
    
    scope = serializers.ChoiceField(
        choices=[
            ('basic', 'Basic'),
            ('agents', 'Agents'),
            ('workflows', 'Workflows'),
            ('comprehensive', 'Comprehensive')
        ],
        default='comprehensive'
    )
    duration = serializers.IntegerField(
        default=60, min_value=10, max_value=300
    )


class AgentEmergencySerializer(serializers.Serializer):
    """Serializer for emergency handling requests"""
    
    emergency_type = serializers.ChoiceField(choices=[
        ('agent_failure', 'Agent Failure'),
        ('system_overload', 'System Overload'),
        ('data_corruption', 'Data Corruption'),
        ('security_breach', 'Security Breach'),
        ('network_issues', 'Network Issues')
    ])
    severity = serializers.ChoiceField(
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        default='high'
    )
    affected_components = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    context = serializers.JSONField(default=dict)


class AgentLoadDistributionSerializer(serializers.Serializer):
    """Serializer for load distribution requests"""
    
    tasks = serializers.ListField(
        child=serializers.JSONField()
    )
    strategy = serializers.ChoiceField(
        choices=[
            ('optimal', 'Optimal'),
            ('round_robin', 'Round Robin'),
            ('load_balanced', 'Load Balanced'),
            ('specialization_based', 'Specialization Based')
        ],
        default='optimal'
    )
    constraints = serializers.JSONField(default=dict)


class AgentValidationSerializer(serializers.Serializer):
    """Serializer for workflow validation requests"""
    
    workflow_id = serializers.CharField()
    criteria = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'completeness', 'quality', 'efficiency', 'performance'
        ]),
        default=['completeness', 'quality']
    )
    user_id = serializers.IntegerField(required=False)


class AgentLifecycleSerializer(serializers.Serializer):
    """Serializer for agent lifecycle management"""
    
    action = serializers.ChoiceField(choices=[
        ('create', 'Create'),
        ('initialize', 'Initialize'),
        ('monitor', 'Monitor'),
        ('terminate', 'Terminate'),
        ('scale', 'Scale'),
        ('status_check', 'Status Check')
    ])
    agent_type = serializers.ChoiceField(
        choices=[
            ('content_curator', 'Content Curator'),
            ('quiz_master', 'Quiz Master'),
            ('evaluator', 'Evaluator'),
            ('progress_tracker', 'Progress Tracker'),
            ('motivator', 'Motivator'),
            ('system_orchestrator', 'System Orchestrator')
        ],
        required=False
    )
    config = serializers.JSONField(default=dict)


# ============================================================================
# CHAT ASSISTANT SERIALIZERS
# ============================================================================

class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for ChatMessage model"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_user_message = serializers.BooleanField(read_only=True)
    is_agent_response = serializers.BooleanField(read_only=True)
    rating_stars = serializers.CharField(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'user', 'user_username', 'session_id', 'message', 'response',
            'agent_type', 'message_type', 'metadata', 'feedback_rating',
            'feedback_comment', 'created_at', 'updated_at', 'is_user_message',
            'is_agent_response', 'rating_stars'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_user_message', 'is_agent_response', 'rating_stars']


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating chat messages"""
    
    class Meta:
        model = ChatMessage
        fields = ['session_id', 'message', 'agent_type']
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['message_type'] = 'user'
        
        # Generate a response based on the message (simplified AI response)
        message = validated_data.get('message', '')
        response = self._generate_mock_response(message)
        validated_data['response'] = response
        
        return ChatMessage.objects.create(**validated_data)
    
    def _generate_mock_response(self, message):
        """Generate a mock AI response based on the user message"""
        message_lower = message.lower()
        
        # Simple response patterns
        if 'hello' in message_lower or 'hi' in message_lower:
            return "Hello! I'm your JAC learning assistant. How can I help you learn JAC programming today?"
        elif 'jac' in message_lower or 'jaseci' in message_lower:
            return "JAC (Jaseci) is a powerful programming language for AI and machine learning. Would you like me to explain some concepts or help you with a specific topic?"
        elif 'help' in message_lower:
            return "I can help you with JAC programming concepts, syntax, best practices, and learning path recommendations. What specific topic would you like to explore?"
        elif 'tutorial' in message_lower or 'learn' in message_lower:
            return "Great! I can guide you through JAC programming tutorials. Are you interested in starting with basics like nodes and edges, or do you have a specific concept in mind?"
        elif 'error' in message_lower or 'bug' in message_lower:
            return "I'd be happy to help debug your JAC code. Could you share the specific error message or code that's causing issues?"
        else:
            return f"That's an interesting question about: '{message}'. While I continue learning, I recommend checking the JAC documentation or asking more specific questions about JAC syntax, nodes, edges, or AI patterns."


class ChatMessageRateSerializer(serializers.ModelSerializer):
    """Serializer for rating chat messages"""
    
    class Meta:
        model = ChatMessage
        fields = ['feedback_rating', 'feedback_comment']


class ChatHistorySerializer(serializers.Serializer):
    """Serializer for chat history response"""
    
    session_id = serializers.CharField()
    messages = ChatMessageSerializer(many=True)
    total_messages = serializers.IntegerField()
    has_more = serializers.BooleanField()


class SendMessageRequestSerializer(serializers.Serializer):
    """Serializer for send message request"""
    
    message = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
    agent_type = serializers.ChoiceField(
        choices=[
            ('content_curator', 'Content Curator'),
            ('quiz_master', 'Quiz Master'),
            ('evaluator', 'Evaluator'),
            ('progress_tracker', 'Progress Tracker'),
            ('motivator', 'Motivator'),
            ('system_orchestrator', 'System Orchestrator')
        ],
        default='system_orchestrator'
    )