"""
Agent Views for Django REST Framework

Views for managing agents, tasks, communications, and system orchestration
"""

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import datetime, timedelta
import json

from .models import Agent, Task, AgentMetrics
from .serializers import (
    AgentSerializer, TaskSerializer, 
    AgentMetricsSerializer, 
    # AgentCommunicationSerializer, LearningSessionSerializer, 
    AgentCreateSerializer,
    TaskCreateSerializer, AgentStatusSerializer, AgentHealthCheckSerializer,
    AgentMetricsQuerySerializer, 
    # LearningSessionCreateSerializer,
    AgentWorkflowSerializer, AgentCoordinationSerializer, AgentSystemMonitorSerializer,
    AgentEmergencySerializer, AgentLoadDistributionSerializer,
    AgentValidationSerializer, AgentLifecycleSerializer
)

from .simple_agents_manager import SimpleAgentsManager


class AgentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Agent instances
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter agents based on query parameters"""
        queryset = Agent.objects.all()
        
        # Filter by agent type
        agent_type = self.request.query_params.get('agent_type', None)
        if agent_type:
            queryset = queryset.filter(agent_type=agent_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by activity
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return AgentCreateSerializer
        return AgentSerializer
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update agent status"""
        agent = self.get_object()
        serializer = AgentStatusSerializer(data=request.data)
        
        if serializer.is_valid():
            agent.status = serializer.validated_data['status']
            if 'error_message' in serializer.validated_data:
                # Log error message or update agent config
                agent.config['last_error'] = serializer.validated_data['error_message']
            agent.last_active = timezone.now()
            agent.save()
            
            return Response({
                'message': 'Agent status updated successfully',
                'status': agent.status,
                'last_active': agent.last_active
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def health_check(self, request, pk=None):
        """Get agent health check information"""
        agent = self.get_object()
        
        # Get agent health information
        health_data = {
            'agent_id': agent.agent_id,
            'agent_type': agent.agent_type,
            'status': agent.status,
            'last_active': agent.last_active,
            'queue_size': 0,  # Would need to be calculated from agent manager
            'metrics_count': AgentMetrics.objects.filter(agent=agent).count(),
            'uptime_hours': (timezone.now() - agent.created_at).total_seconds() / 3600
        }
        
        serializer = AgentHealthCheckSerializer(health_data)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def restart(self, request, pk=None):
        """Restart agent instance"""
        agent = self.get_object()
        
        # This would interface with the actual agent manager
        # For now, we'll simulate a restart
        agent.status = 'maintenance'
        agent.save()
        
        # Simulate restart process
        agent.status = 'idle'
        agent.last_active = timezone.now()
        agent.save()
        
        return Response({
            'message': f'Agent {agent.name} restarted successfully',
            'new_status': agent.status
        })
    
    @action(detail=False, methods=['get'])
    def system_overview(self, request):
        """Get system-wide agent overview"""
        agents = Agent.objects.all()
        
        overview = {
            'total_agents': agents.count(),
            'active_agents': agents.filter(is_active=True).count(),
            'idle_agents': agents.filter(status='idle').count(),
            'busy_agents': agents.filter(status='active').count(),
            'error_agents': agents.filter(status='error').count(),
            'agents_by_type': {},
            'recent_activity': []
        }
        
        # Count agents by type
        for agent_type in Agent.AgentType:
            count = agents.filter(agent_type=agent_type).count()
            overview['agents_by_type'][agent_type] = count
        
        # Get recent agent activity
        recent_agents = agents.order_by('-last_active')[:10]
        for agent in recent_agents:
            overview['recent_activity'].append({
                'name': agent.name,
                'type': agent.agent_type,
                'status': agent.status,
                'last_active': agent.last_active
            })
        
        return Response(overview)


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter tasks based on query parameters"""
        queryset = Task.objects.all()
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent', None)
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(assigned_at__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(assigned_at__date__lte=end_date)
            except ValueError:
                pass
        
        return queryset.order_by('-assigned_at', '-priority')
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskSerializer
    
    @action(detail=True, methods=['post'])
    def start_task(self, request, pk=None):
        """Start task execution"""
        task = self.get_object()
        
        if task.status != 'pending':
            return Response({
                'error': 'Task is not in pending status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task.status = 'in_progress'
        task.started_at = timezone.now()
        task.save()
        
        return Response({
            'message': 'Task started successfully',
            'started_at': task.started_at
        })
    
    @action(detail=True, methods=['post'])
    def complete_task(self, request, pk=None):
        """Complete task execution"""
        task = self.get_object()
        
        if task.status not in ['in_progress']:
            return Response({
                'error': 'Task is not in progress'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        output_data = request.data.get('output_data', {})
        task.output_data = output_data
        task.status = 'completed'
        task.completed_at = timezone.now()
        
        # Calculate execution time
        if task.started_at:
            task.execution_time = (task.completed_at - task.started_at).total_seconds()
        
        task.save()
        
        return Response({
            'message': 'Task completed successfully',
            'completed_at': task.completed_at,
            'execution_time': task.execution_time
        })
    
    @action(detail=True, methods=['post'])
    def fail_task(self, request, pk=None):
        """Mark task as failed"""
        task = self.get_object()
        error_message = request.data.get('error_message', 'Task failed')
        
        task.status = 'failed'
        task.error_message = error_message
        task.completed_at = timezone.now()
        
        # Calculate execution time
        if task.started_at:
            task.execution_time = (task.completed_at - task.started_at).total_seconds()
        
        task.save()
        
        return Response({
            'message': 'Task marked as failed',
            'error_message': error_message,
            'completed_at': task.completed_at
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get task statistics"""
        tasks = Task.objects.all()
        
        # Get recent activity (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_tasks = tasks.filter(assigned_at__gte=thirty_days_ago)
        
        stats = {
            'total_tasks': tasks.count(),
            'pending_tasks': tasks.filter(status='pending').count(),
            'in_progress_tasks': tasks.filter(status='in_progress').count(),
            'completed_tasks': tasks.filter(status='completed').count(),
            'failed_tasks': tasks.filter(status='failed').count(),
            'recent_tasks': recent_tasks.count(),
            'average_execution_time': 0,
            'tasks_by_type': {},
            'tasks_by_agent': {},
            'tasks_by_priority': {
                'low': tasks.filter(priority='low').count(),
                'medium': tasks.filter(priority='medium').count(),
                'high': tasks.filter(priority='high').count(),
                'critical': tasks.filter(priority='critical').count()
            }
        }
        
        # Calculate average execution time
        completed_with_time = tasks.filter(
            status='completed',
            execution_time__isnull=False
        )
        if completed_with_time.exists():
            stats['average_execution_time'] = completed_with_time.aggregate(
                Avg('execution_time')
            )['execution_time__avg']
        
        # Tasks by type
        for task_type in tasks.values_list('task_type', flat=True).distinct():
            count = tasks.filter(task_type=task_type).count()
            stats['tasks_by_type'][task_type] = count
        
        # Tasks by agent
        agents = Agent.objects.all()
        for agent in agents:
            count = tasks.filter(agent=agent).count()
            stats['tasks_by_agent'][agent.name] = count
        
        return Response(stats)


# class AgentCommunicationViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     ViewSet for viewing Agent Communications
#     """
#     queryset = AgentCommunication.objects.all()
#     serializer_class = AgentCommunicationSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter communications based on query parameters"""
        queryset = AgentCommunication.objects.all()
        
        # Filter by sender
        sender = self.request.query_params.get('sender', None)
        if sender:
            queryset = queryset.filter(sender_agent_id=sender)
        
        # Filter by receiver
        receiver = self.request.query_params.get('receiver', None)
        if receiver:
            queryset = queryset.filter(receiver_agent_id=receiver)
        
        # Filter by message type
        message_type = self.request.query_params.get('message_type', None)
        if message_type:
            queryset = queryset.filter(message_type=message_type)
        
        # Filter by urgency
        urgent_only = self.request.query_params.get('urgent_only', None)
        if urgent_only and urgent_only.lower() == 'true':
            queryset = queryset.filter(is_urgent=True)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(sent_at__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(sent_at__date__lte=end_date)
            except ValueError:
                pass
        
        return queryset.order_by('-sent_at')
    
    @action(detail=False, methods=['get'])
    def conversation_log(self, request):
        """Get conversation log between two agents"""
        sender_id = request.query_params.get('sender')
        receiver_id = request.query_params.get('receiver')
        
        if not sender_id or not receiver_id:
            return Response({
                'error': 'Both sender and receiver IDs are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get messages in both directions
        messages = AgentCommunication.objects.filter(
            (Q(sender_agent_id=sender_id, receiver_agent_id=receiver_id) |
             Q(sender_agent_id=receiver_id, receiver_agent_id=sender_id))
        ).order_by('sent_at')
        
        serializer = self.get_serializer(messages, many=True)
        return Response({
            'conversation_id': f"{sender_id}-{receiver_id}",
            'messages': serializer.data,
            'message_count': messages.count()
        })


class AgentMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing Agent Metrics
    """
    queryset = AgentMetrics.objects.all()
    serializer_class = AgentMetricsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter metrics based on query parameters"""
        queryset = AgentMetrics.objects.all()
        
        # Filter by agent
        agent_id = self.request.query_params.get('agent', None)
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)
        
        # Filter by metric name
        metric_name = self.request.query_params.get('metric_name', None)
        if metric_name:
            queryset = queryset.filter(metric_name=metric_name)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(recorded_at__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(recorded_at__date__lte=end_date)
            except ValueError:
                pass
        
        return queryset.order_by('-recorded_at')
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get metrics analytics"""
        serializer = AgentMetricsQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        queryset = self.get_queryset()
        
        # Additional filtering based on query params
        if validated_data.get('agent_type'):
            queryset = queryset.filter(agent__agent_type=validated_data['agent_type'])
        
        limit = validated_data.get('limit', 100)
        queryset = queryset[:limit]
        
        # Calculate analytics
        analytics = {
            'total_metrics': queryset.count(),
            'metrics_by_agent': {},
            'metrics_by_type': {},
            'recent_trends': {},
            'summary_statistics': {}
        }
        
        # Group by agent
        for metric in queryset:
            agent_name = metric.agent.name
            if agent_name not in analytics['metrics_by_agent']:
                analytics['metrics_by_agent'][agent_name] = 0
            analytics['metrics_by_agent'][agent_name] += 1
        
        # Group by metric type
        for metric_type in queryset.values_list('metric_type', flat=True).distinct():
            count = queryset.filter(metric_type=metric_type).count()
            analytics['metrics_by_type'][metric_type] = count
        
        return Response(analytics)


# class LearningSessionViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for managing Learning Sessions
#     """
#     queryset = LearningSession.objects.all()
#     serializer_class = LearningSessionSerializer
#     permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter learning sessions based on query parameters"""
        queryset = LearningSession.objects.all()
        
        # Filter by user
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        # Filter by learning path
        learning_path_id = self.request.query_params.get('learning_path', None)
        if learning_path_id:
            queryset = queryset.filter(learning_path_id=learning_path_id)
        
        # Filter by session type
        session_type = self.request.query_params.get('session_type', None)
        if session_type:
            queryset = queryset.filter(session_type=session_type)
        
        # Filter by active sessions
        active_only = self.request.query_params.get('active_only', None)
        if active_only and active_only.lower() == 'true':
            queryset = queryset.filter(ended_at__isnull=True)
        
        return queryset.order_by('-started_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'create':
            return LearningSessionCreateSerializer
        return LearningSessionSerializer
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """End a learning session"""
        session = self.get_object()
        
        if session.ended_at:
            return Response({
                'error': 'Session is already ended'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        session.ended_at = timezone.now()
        
        # Update performance score if provided
        performance_score = request.data.get('performance_score')
        if performance_score is not None:
            session.performance_score = performance_score
        
        session.save()
        
        return Response({
            'message': 'Session ended successfully',
            'ended_at': session.ended_at,
            'duration': session.duration,
            'performance_score': session.performance_score
        })


class AgentWorkflowAPIView(APIView):
    """
    API View for workflow orchestration
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Execute workflow orchestration"""
        serializer = AgentWorkflowSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Get user
        try:
            user = User.objects.get(id=validated_data['user_id'])
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Execute workflow
        workflow_result = agents_manager.orchestrate_workflow(
            workflow_type=validated_data['workflow_type'],
            user=user,
            learning_path_id=validated_data.get('learning_path_id'),
            config=validated_data.get('config', {})
        )
        
        return Response(workflow_result)


class AgentCoordinationAPIView(APIView):
    """
    API View for agent coordination
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Coordinate multiple agents"""
        serializer = AgentCoordinationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Get user
        try:
            user = User.objects.get(id=validated_data['user_id'])
        except User.DoesNotExist:
            return Response({
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Coordinate agents
        coordination_result = agents_manager.coordinate_agents(
            task_description=validated_data['task_description'],
            required_capabilities=validated_data.get('required_capabilities', []),
            user=user,
            coordination_strategy=validated_data.get('strategy', 'sequential')
        )
        
        return Response(coordination_result)


class AgentSystemMonitorAPIView(APIView):
    """
    API View for system monitoring
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Monitor system performance"""
        serializer = AgentSystemMonitorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Monitor system
        monitoring_result = agents_manager.monitor_system(
            scope=validated_data.get('scope', 'comprehensive'),
            duration=validated_data.get('duration', 60)
        )
        
        return Response(monitoring_result)
    
    def get(self, request):
        """Get current system status"""
        # Get basic system overview
        agents = Agent.objects.all()
        
        system_status = {
            'timestamp': timezone.now().isoformat(),
            'agents': {
                'total': agents.count(),
                'active': agents.filter(is_active=True, status__in=['idle', 'active', 'processing']).count(),
                'error': agents.filter(status='error').count(),
                'maintenance': agents.filter(status='maintenance').count()
            },
            'tasks': {
                'pending': Task.objects.filter(status='pending').count(),
                'in_progress': Task.objects.filter(status='in_progress').count(),
                'completed_today': Task.objects.filter(
                    status='completed',
                    completed_at__date=timezone.now().date()
                ).count()
            },
            'system_health': 'healthy'  # Would be calculated based on actual metrics
        }
        
        return Response(system_status)


class AgentEmergencyAPIView(APIView):
    """
    API View for emergency handling
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Handle system emergencies"""
        serializer = AgentEmergencySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Handle emergency
        emergency_result = agents_manager.handle_emergency(
            emergency_type=validated_data['emergency_type'],
            severity=validated_data['severity'],
            affected_components=validated_data.get('affected_components', []),
            emergency_context=validated_data.get('context', {})
        )
        
        return Response(emergency_result)


class AgentLoadDistributionAPIView(APIView):
    """
    API View for load distribution
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Distribute tasks across agents"""
        serializer = AgentLoadDistributionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Distribute load
        distribution_result = agents_manager.distribute_load(
            tasks_to_distribute=validated_data['tasks'],
            distribution_strategy=validated_data.get('strategy', 'optimal'),
            capacity_constraints=validated_data.get('constraints', {})
        )
        
        return Response(distribution_result)


class AgentWorkflowValidationAPIView(APIView):
    """
    API View for workflow validation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Validate workflow execution"""
        serializer = AgentValidationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Validate workflow
        validation_result = agents_manager.validate_workflow(
            workflow_id=validated_data['workflow_id'],
            validation_criteria=validated_data.get('criteria', ['completeness', 'quality']),
            user_id=validated_data.get('user_id')
        )
        
        return Response(validation_result)


class AgentLifecycleAPIView(APIView):
    """
    API View for agent lifecycle management
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Manage agent lifecycle"""
        serializer = AgentLifecycleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Initialize agents manager
        agents_manager = SimpleAgentsManager()
        
        # Manage lifecycle
        lifecycle_result = agents_manager.manage_agent_lifecycle(
            lifecycle_action=validated_data['action'],
            agent_type=validated_data.get('agent_type'),
            agent_config=validated_data.get('config', {})
        )
        
        return Response(lifecycle_result)


# Simple health check function for Docker health checks
def system_health_check(request):
    """
    Simple system health check endpoint
    Used for Docker health checks and monitoring
    """
    from django.http import JsonResponse
    import os
    from django.utils import timezone
    
    # Simple health response without complex dependencies
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'jac-interactive-learning-platform',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'message': 'Backend service is running'
    }
    
    # Only check database if Django is fully loaded
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['database'] = 'healthy'
    except Exception as e:
        health_status['database'] = f'unhealthy: {str(e)}'
        # Don't fail the health check for database issues during startup
    
    # Only check Redis if it seems available
    try:
        import redis
        
        # Get Redis connection details from environment
        redis_host = os.getenv('REDIS_HOST', 'localhost')  # Fallback to localhost
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_password = os.getenv('REDIS_PASSWORD', 'redis_password')
        
        # Try multiple hosts for Docker compatibility
        redis_hosts = [
            redis_host,
            'redis',
            '127.0.0.1',
            'localhost'
        ]
        
        redis_connected = False
        for host in redis_hosts:
            try:
                r = redis.Redis(
                    host=host,
                    port=redis_port,
                    password=redis_password,
                    socket_connect_timeout=3,
                    socket_timeout=3,
                    db=0
                )
                r.ping()
                health_status['redis'] = 'healthy'
                health_status['redis_host'] = host
                redis_connected = True
                break
            except Exception:
                continue
        
        if not redis_connected:
            health_status['redis'] = 'unavailable: Could not connect to any Redis host'
            
    except ImportError:
        health_status['redis'] = 'unavailable: Redis library not installed'
    except Exception as e:
        health_status['redis'] = f'unavailable: {str(e)[:100]}...'  # Truncate error message
    
    return JsonResponse(health_status)


# ============================================================================
# CHAT ASSISTANT API VIEWS
# ============================================================================

from .models import ChatMessage
from .serializers import (
    ChatMessageSerializer, ChatMessageCreateSerializer, ChatMessageRateSerializer,
    ChatHistorySerializer, SendMessageRequestSerializer
)


class ChatAssistantAPIView(APIView):
    """
    Chat Assistant API for handling user interactions with AI agents
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Send a message to the chat assistant
        POST /api/agents/chat-assistant/message/
        """
        serializer = SendMessageRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Generate or use provided session_id
        session_id = data.get('session_id')
        if not session_id:
            session_id = f"session_{request.user.id}_{int(timezone.now().timestamp())}"
        
        # Create user message
        message_data = {
            'session_id': session_id,
            'message': data['message'],
            'agent_type': data.get('agent_type', 'system_orchestrator'),
            'message_type': 'user'
        }
        
        user_message = ChatMessageCreateSerializer(
            data=message_data,
            context={'request': request}
        )
        
        if not user_message.is_valid():
            return Response(user_message.errors, status=status.HTTP_400_BAD_REQUEST)
        
        created_message = user_message.save()
        
        # Get the created message with full serializer data
        response_serializer = ChatMessageSerializer(created_message)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        """
        Get chat history for a session
        GET /api/agents/chat-assistant/history/?session_id=xxx
        """
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response(
                {'error': 'session_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Pagination parameters
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        
        # Get messages for the session
        messages = ChatMessage.objects.filter(
            user=request.user,
            session_id=session_id
        ).order_by('created_at')[offset:offset + limit]
        
        # Get total count for pagination
        total_count = ChatMessage.objects.filter(
            user=request.user,
            session_id=session_id
        ).count()
        
        # Serialize messages
        message_serializer = ChatMessageSerializer(messages, many=True)
        
        # Create response with pagination info
        response_data = {
            'session_id': session_id,
            'messages': message_serializer.data,
            'total_messages': total_count,
            'has_more': (offset + limit) < total_count,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(message_serializer.data)
            }
        }
        
        return Response(response_data)


class RateChatMessageAPIView(APIView):
    """
    API view for rating chat messages
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, message_id):
        """
        Rate a chat message
        POST /api/agents/chat-assistant/rate/{message_id}/
        """
        try:
            message = ChatMessage.objects.get(
                id=message_id,
                user=request.user,
                message_type='agent'
            )
        except ChatMessage.DoesNotExist:
            return Response(
                {'error': 'Chat message not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ChatMessageRateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the message with rating
        for attr, value in serializer.validated_data.items():
            setattr(message, attr, value)
        
        message.save()
        
        return Response({
            'message': 'Rating submitted successfully',
            'feedback_rating': message.feedback_rating,
            'feedback_comment': message.feedback_comment
        })


class ChatSessionListAPIView(APIView):
    """
    API view for listing user's chat sessions
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get list of user's chat sessions with latest message info
        GET /api/agents/chat-assistant/sessions/
        """
        from django.db.models import Max, Count
        
        # Get distinct session IDs with latest message and message count
        sessions = ChatMessage.objects.filter(
            user=request.user
        ).values('session_id').annotate(
            latest_message=Max('created_at'),
            message_count=Count('id')
        ).order_by('-latest_message')
        
        session_list = []
        for session in sessions:
            # Get the first and last message for preview
            session_messages = ChatMessage.objects.filter(
                user=request.user,
                session_id=session['session_id']
            ).order_by('created_at')
            
            first_message = session_messages.first()
            last_message = session_messages.last()
            
            session_data = {
                'session_id': session['session_id'],
                'message_count': session['message_count'],
                'latest_message': session['latest_message'],
                'first_message_preview': first_message.message[:100] if first_message else '',
                'last_message_preview': last_message.message[:100] if last_message else '',
                'agent_type': last_message.agent_type if last_message else 'system_orchestrator'
            }
            session_list.append(session_data)
        
        return Response({
            'sessions': session_list,
            'total_sessions': len(session_list)
        })


class AgentStatusAPIView(APIView):
    """
    API endpoint for getting current status of all agents
    Provides comprehensive agent health and performance information
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current status of all agents"""
        try:
            # Get all agents
            agents = Agent.objects.all()
            agent_status = {}
            
            for agent in agents:
                # Get current task queue size for this agent
                pending_tasks = Task.objects.filter(
                    agent=agent, 
                    status='pending'
                ).count()
                
                # Calculate uptime in hours
                uptime_seconds = (timezone.now() - agent.created_at).total_seconds()
                uptime_hours = round(uptime_seconds / 3600, 2)
                
                # Calculate health score based on recent activity
                health_score = self._calculate_agent_health_score(agent)
                
                agent_status[agent.agent_id] = {
                    'id': agent.id,
                    'name': agent.name,
                    'agent_type': agent.agent_type,
                    'status': agent.status.lower(),
                    'last_active': agent.updated_at.isoformat() if agent.updated_at else agent.created_at.isoformat(),
                    'current_task': agent.current_task,
                    'queue_size': pending_tasks,
                    'uptime_hours': uptime_hours,
                    'health_score': health_score,
                    'capabilities': agent.capabilities or [],
                    'config': agent.config or {}
                }
            
            # Get system-wide metrics
            system_metrics = self._get_system_metrics()
            
            return Response({
                'agents': agent_status,
                'system_metrics': system_metrics,
                'total_agents': len(agent_status),
                'healthy_agents': len([a for a in agent_status.values() if a['health_score'] >= 90]),
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve agent status: {str(e)}',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _calculate_agent_health_score(self, agent):
        """
        Calculate health score for an agent based on various factors
        Returns score from 0-100
        """
        try:
            base_score = 100
            
            # Penalize for old last activity
            if agent.updated_at:
                minutes_since_update = (timezone.now() - agent.updated_at).total_seconds() / 60
                if minutes_since_update > 60:  # 1 hour
                    base_score -= 20
                elif minutes_since_update > 30:  # 30 minutes
                    base_score -= 10
                elif minutes_since_update > 10:  # 10 minutes
                    base_score -= 5
            
            # Penalize for high task queue
            queue_size = Task.objects.filter(agent=agent, status='pending').count()
            if queue_size > 20:
                base_score -= 15
            elif queue_size > 10:
                base_score -= 10
            elif queue_size > 5:
                base_score -= 5
            
            # Bonus for active status
            if agent.status.lower() == 'active':
                base_score += 5
            
            # Ensure score is within bounds
            return max(0, min(100, base_score))
            
        except Exception:
            # Return default score if calculation fails
            return 85
    
    def _get_system_metrics(self):
        """
        Get system-wide metrics and health information
        """
        try:
            total_agents = Agent.objects.count()
            active_agents = Agent.objects.filter(status='active').count()
            total_tasks = Task.objects.count()
            pending_tasks = Task.objects.filter(status='pending').count()
            
            # Get active learning sessions
            try:
                from .models import LearningSession
                active_sessions = LearningSession.objects.filter(status='active').count()
            except ImportError:
                active_sessions = 0
            
            # Calculate overall system health
            if total_agents > 0:
                health_ratio = active_agents / total_agents
                overall_health = 95 if health_ratio >= 0.8 else 85 if health_ratio >= 0.6 else 75
            else:
                overall_health = 0
            
            return {
                'overall_status': 'healthy' if overall_health >= 90 else 'degraded' if overall_health >= 70 else 'unhealthy',
                'health_score': overall_health,
                'total_agents': total_agents,
                'active_agents': active_agents,
                'inactive_agents': total_agents - active_agents,
                'total_tasks': total_tasks,
                'pending_tasks': pending_tasks,
                'active_sessions': active_sessions,
                'system_load': 'low',  # Could be calculated based on active tasks per agent
                'last_updated': timezone.now().isoformat()
            }
            
        except Exception:
            return {
                'overall_status': 'unknown',
                'health_score': 0,
                'total_agents': 0,
                'active_agents': 0,
                'pending_tasks': 0,
                'active_sessions': 0,
                'last_updated': timezone.now().isoformat()
            }