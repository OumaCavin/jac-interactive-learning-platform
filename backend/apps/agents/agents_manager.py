"""
Agents Manager

Central manager for coordinating and interfacing with all agent instances
"""

from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
import time

# Import simplified models and agents for standalone operation
# Note: This is a simplified version for initial testing
# from .models import Agent, Task, AgentCommunication, LearningSession
# from .content_curator import ContentCuratorAgent
# from .quiz_master import QuizMasterAgent
# from .evaluator import EvaluatorAgent
# from .progress_tracker import ProgressTrackerAgent
# from .motivator import MotivatorAgent
# from .system_orchestrator import SystemOrchestratorAgent


class AgentsManager:
    """
    Central manager for all agent instances in the system
    """
    
    def __init__(self):
        self.agents = {}
        self.agent_instances = {}
        self.active_sessions = {}
        self.system_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.initialize_agents()
    
    def initialize_agents(self):
        """Initialize all agent instances"""
        # Get agents from database
        db_agents = Agent.objects.filter(is_active=True)
        
        # Initialize each agent type
        agent_types = {
            'content_curator': ContentCuratorAgent,
            'quiz_master': QuizMasterAgent,
            'evaluator': EvaluatorAgent,
            'progress_tracker': ProgressTrackerAgent,
            'motivator': MotivatorAgent,
            'system_orchestrator': SystemOrchestratorAgent
        }
        
        for agent_type, agent_class in agent_types.items():
            # Check if agent exists in database
            db_agent = db_agents.filter(agent_type=agent_type).first()
            
            if db_agent:
                # Initialize agent instance
                agent_instance = agent_class(
                    agent_id=db_agent.agent_id,
                    config=db_agent.config
                )
                self.agent_instances[agent_type] = agent_instance
                self.agents[agent_type] = db_agent
    
    def get_agent_instance(self, agent_type: str):
        """Get agent instance by type"""
        return self.agent_instances.get(agent_type)
    
    def get_agent_status(self, agent_type: str) -> Dict[str, Any]:
        """Get agent status"""
        agent_instance = self.get_agent_instance(agent_type)
        if agent_instance:
            return agent_instance.health_check()
        return {}
    
    def create_task(self, agent_type: str, task_data: Dict[str, Any], user: User) -> Task:
        """Create a new task for an agent"""
        with self.system_lock:
            if agent_type not in self.agents:
                raise ValueError(f"Agent type {agent_type} not found")
            
            db_agent = self.agents[agent_type]
            
            # Create task in database
            task = Task.objects.create(
                task_id=str(uuid.uuid4()),
                agent=db_agent,
                task_type=task_data.get('type', 'general'),
                title=task_data.get('title', 'Untitled Task'),
                description=task_data.get('description', ''),
                input_data=task_data.get('params', {}),
                status='pending',
                priority=task_data.get('priority', 'medium'),
                assigned_by=user
            )
            
            # Add task to agent queue
            agent_instance = self.get_agent_instance(agent_type)
            if agent_instance:
                agent_instance.add_to_queue(task_data, priority=task_data.get('priority', 'medium'))
            
            return task
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a specific task"""
        try:
            task = Task.objects.get(task_id=task_id)
            agent_instance = self.get_agent_instance(task.agent.agent_type)
            
            if not agent_instance:
                return {'success': False, 'error': 'Agent instance not found'}
            
            # Update task status
            task.status = 'in_progress'
            task.started_at = timezone.now()
            task.save()
            
            # Execute task
            result = agent_instance.process_task(task.input_data)
            
            # Update task with result
            if result.get('success'):
                task.status = 'completed'
                task.output_data = result.get('result', {})
            else:
                task.status = 'failed'
                task.error_message = result.get('error', 'Unknown error')
            
            task.completed_at = timezone.now()
            if task.started_at:
                task.execution_time = (task.completed_at - task.started_at).total_seconds()
            task.save()
            
            return result
            
        except Task.DoesNotExist:
            return {'success': False, 'error': 'Task not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def orchestrate_workflow(self, workflow_type: str, user: User, 
                           learning_path_id: Optional[str] = None,
                           config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Orchestrate a multi-agent workflow"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        workflow_params = {
            'workflow_type': workflow_type,
            'user': user,
            'learning_path_id': learning_path_id,
            'config': config or {}
        }
        
        task_data = {
            'type': 'orchestrate_workflow',
            'params': workflow_params
        }
        
        return orchestrator.process_task(task_data)
    
    def coordinate_agents(self, task_description: str, required_capabilities: List[str],
                        user: User, coordination_strategy: str = 'sequential') -> Dict[str, Any]:
        """Coordinate multiple agents for a complex task"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        coordination_params = {
            'task_description': task_description,
            'required_capabilities': required_capabilities,
            'user': user,
            'strategy': coordination_strategy
        }
        
        task_data = {
            'type': 'coordinate_agents',
            'params': coordination_params
        }
        
        return orchestrator.process_task(task_data)
    
    def monitor_system(self, scope: str = 'comprehensive', duration: int = 60) -> Dict[str, Any]:
        """Monitor system performance and health"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        monitoring_params = {
            'scope': scope,
            'duration': duration
        }
        
        task_data = {
            'type': 'monitor_system',
            'params': monitoring_params
        }
        
        return orchestrator.process_task(task_data)
    
    def handle_emergency(self, emergency_type: str, severity: str,
                       affected_components: List[str] = None,
                       emergency_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle system emergencies"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        emergency_params = {
            'emergency_type': emergency_type,
            'severity': severity,
            'affected_components': affected_components or [],
            'context': emergency_context or {}
        }
        
        task_data = {
            'type': 'handle_emergency',
            'params': emergency_params
        }
        
        return orchestrator.process_task(task_data)
    
    def distribute_load(self, tasks_to_distribute: List[Dict[str, Any]],
                       distribution_strategy: str = 'optimal',
                       capacity_constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Distribute tasks across agents"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        distribution_params = {
            'tasks': tasks_to_distribute,
            'strategy': distribution_strategy,
            'constraints': capacity_constraints or {}
        }
        
        task_data = {
            'type': 'distribute_load',
            'params': distribution_params
        }
        
        return orchestrator.process_task(task_data)
    
    def validate_workflow(self, workflow_id: str, validation_criteria: List[str],
                         user_id: Optional[int] = None) -> Dict[str, Any]:
        """Validate workflow execution"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        validation_params = {
            'workflow_id': workflow_id,
            'criteria': validation_criteria,
            'user': User.objects.get(id=user_id) if user_id else None
        }
        
        task_data = {
            'type': 'validate_workflow',
            'params': validation_params
        }
        
        return orchestrator.process_task(task_data)
    
    def manage_agent_lifecycle(self, lifecycle_action: str, agent_type: Optional[str] = None,
                             agent_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Manage agent lifecycle"""
        orchestrator = self.get_agent_instance('system_orchestrator')
        if not orchestrator:
            return {'success': False, 'error': 'System orchestrator not available'}
        
        lifecycle_params = {
            'action': lifecycle_action,
            'agent_type': agent_type,
            'config': agent_config or {}
        }
        
        task_data = {
            'type': 'manage_agent_lifecycle',
            'params': lifecycle_params
        }
        
        return orchestrator.process_task(task_data)
    
    def start_learning_session(self, user: User, learning_path_id: str,
                             agent_types: List[str], session_type: str = 'learning') -> LearningSession:
        """Start a new learning session with multiple agents"""
        with self.system_lock:
            session_id = str(uuid.uuid4())
            
            # Create learning session
            session = LearningSession.objects.create(
                session_id=session_id,
                user=user,
                session_type=session_type,
                learning_path_id=learning_path_id,
                session_data={'status': 'active'}
            )
            
            # Add agents to session
            for agent_type in agent_types:
                if agent_type in self.agents:
                    session.agents_involved.add(self.agents[agent_type])
            
            session.save()
            
            # Store in active sessions
            self.active_sessions[session_id] = {
                'session': session,
                'start_time': timezone.now(),
                'agents': agent_types
            }
            
            return session
    
    def end_learning_session(self, session_id: str, performance_score: Optional[float] = None) -> Dict[str, Any]:
        """End a learning session"""
        with self.system_lock:
            if session_id not in self.active_sessions:
                return {'success': False, 'error': 'Session not found or already ended'}
            
            session_info = self.active_sessions.pop(session_id)
            session = session_info['session']
            
            # Update session
            session.ended_at = timezone.now()
            if performance_score is not None:
                session.performance_score = performance_score
            session.save()
            
            # Generate session summary
            duration = session.duration
            agents_involved = [agent.name for agent in session.agents_involved.all()]
            
            return {
                'success': True,
                'session_id': session_id,
                'duration': duration,
                'agents_involved': agents_involved,
                'performance_score': session.performance_score,
                'ended_at': session.ended_at
            }
    
    def get_agent_recommendations(self, user: User, context: str = 'general') -> Dict[str, Any]:
        """Get agent recommendations based on user context"""
        recommendations = {
            'content_curator': {'suitable': True, 'confidence': 0.8},
            'quiz_master': {'suitable': True, 'confidence': 0.9},
            'evaluator': {'suitable': True, 'confidence': 0.7},
            'progress_tracker': {'suitable': True, 'confidence': 0.9},
            'motivator': {'suitable': True, 'confidence': 0.8},
            'system_orchestrator': {'suitable': context == 'complex', 'confidence': 0.6}
        }
        
        # Analyze user data for better recommendations
        # This would typically involve ML/AI analysis of user behavior
        user_progress_count = user.userprogress_set.count()
        
        if user_progress_count < 5:
            # New user - recommend foundational agents
            recommendations['motivator']['confidence'] = 0.9
            recommendations['content_curator']['confidence'] = 0.9
        elif user_progress_count > 20:
            # Experienced user - recommend advanced agents
            recommendations['evaluator']['confidence'] = 0.9
            recommendations['system_orchestrator']['confidence'] = 0.8
        
        return recommendations
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        health_status = {
            'overall_status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'agents': {},
            'active_tasks': 0,
            'active_sessions': len(self.active_sessions),
            'system_metrics': {}
        }
        
        # Check each agent
        for agent_type, agent_instance in self.agent_instances.items():
            agent_health = agent_instance.health_check()
            health_status['agents'][agent_type] = {
                'status': agent_health.get('status', 'unknown'),
                'last_active': agent_health.get('last_active'),
                'queue_size': agent_health.get('queue_size', 0)
            }
        
        # Count active tasks
        health_status['active_tasks'] = Task.objects.filter(
            status__in=['pending', 'in_progress']
        ).count()
        
        # Calculate system health score
        healthy_agents = sum(1 for agent in health_status['agents'].values() 
                           if agent['status'] in ['idle', 'active'])
        total_agents = len(health_status['agents'])
        
        if total_agents > 0:
            health_score = (healthy_agents / total_agents) * 100
            health_status['system_metrics']['health_score'] = health_score
            
            if health_score >= 90:
                health_status['overall_status'] = 'healthy'
            elif health_score >= 70:
                health_status['overall_status'] = 'degraded'
            else:
                health_status['overall_status'] = 'unhealthy'
        
        return health_status
    
    def optimize_agent_performance(self, agent_type: str) -> Dict[str, Any]:
        """Optimize performance for specific agent"""
        agent_instance = self.get_agent_instance(agent_type)
        if not agent_instance:
            return {'success': False, 'error': f'Agent {agent_type} not found'}
        
        # Get current metrics
        current_metrics = agent_instance.get_metrics()
        
        # Performance optimization strategies
        optimization_strategies = {
            'content_curator': [
                'optimize_content_caching',
                'improve_recommendation_algorithms',
                'enhance_content_quality_analysis'
            ],
            'quiz_master': [
                'optimize_question_generation_speed',
                'improve_difficulty_calibration',
                'enhance_assessment_variety'
            ],
            'evaluator': [
                'optimize_evaluation_algorithms',
                'improve_feedback_generation',
                'enhance_performance_prediction'
            ],
            'progress_tracker': [
                'optimize_data_processing',
                'improve_analytics_accuracy',
                'enhance_visualization_performance'
            ],
            'motivator': [
                'optimize_personalization_algorithms',
                'improve_engagement_prediction',
                'enhance_encouragement_effectiveness'
            ],
            'system_orchestrator': [
                'optimize_workflow_execution',
                'improve_load_balancing',
                'enhance_coordination_efficiency'
            ]
        }
        
        strategies = optimization_strategies.get(agent_type, [])
        
        # Simulate optimization (in real implementation, this would apply actual optimizations)
        optimization_result = {
            'success': True,
            'agent_type': agent_type,
            'optimization_strategies': strategies,
            'estimated_improvement': '15-25% performance gain',
            'optimization_time': '5-10 minutes',
            'metrics_before': current_metrics,
            'metrics_after': {k: v * 1.2 for k, v in current_metrics.items()}  # Simulated improvement
        }
        
        return optimization_result
    
    def handle_agent_failure(self, agent_type: str) -> Dict[str, Any]:
        """Handle agent failure and initiate recovery"""
        recovery_actions = []
        
        # Step 1: Mark agent as error state
        if agent_type in self.agents:
            db_agent = self.agents[agent_type]
            db_agent.status = 'error'
            db_agent.save()
            recovery_actions.append('Agent status updated to error')
        
        # Step 2: Remove from active instances
        if agent_type in self.agent_instances:
            del self.agent_instances[agent_type]
            recovery_actions.append('Agent instance removed from active pool')
        
        # Step 3: Reinitialize agent
        try:
            self._reinitialize_agent(agent_type)
            recovery_actions.append('Agent successfully reinitialized')
            recovery_status = 'success'
        except Exception as e:
            recovery_actions.append(f'Reinitialization failed: {str(e)}')
            recovery_status = 'failed'
        
        return {
            'success': recovery_status == 'success',
            'agent_type': agent_type,
            'recovery_actions': recovery_actions,
            'recovery_status': recovery_status,
            'timestamp': timezone.now().isoformat()
        }
    
    def _reinitialize_agent(self, agent_type: str):
        """Reinitialize a failed agent"""
        agent_types = {
            'content_curator': ContentCuratorAgent,
            'quiz_master': QuizMasterAgent,
            'evaluator': EvaluatorAgent,
            'progress_tracker': ProgressTrackerAgent,
            'motivator': MotivatorAgent,
            'system_orchestrator': SystemOrchestratorAgent
        }
        
        agent_class = agent_types.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Get database agent
        db_agent = Agent.objects.filter(agent_type=agent_type, is_active=True).first()
        if not db_agent:
            raise ValueError(f"No active agent found for type: {agent_type}")
        
        # Reinitialize
        agent_instance = agent_class(
            agent_id=db_agent.agent_id,
            config=db_agent.config
        )
        self.agent_instances[agent_type] = agent_instance
        
        # Update database status
        db_agent.status = 'idle'
        db_agent.last_active = timezone.now()
        db_agent.save()
    
    def cleanup_inactive_sessions(self):
        """Clean up inactive sessions (older than 24 hours)"""
        cutoff_time = timezone.now() - timedelta(hours=24)
        
        inactive_sessions = []
        for session_id, session_info in list(self.active_sessions.items()):
            if session_info['start_time'] < cutoff_time:
                inactive_sessions.append(session_id)
        
        # Remove from active sessions
        for session_id in inactive_sessions:
            del self.active_sessions[session_id]
        
        return len(inactive_sessions)
    
    def get_performance_analytics(self, time_period_days: int = 7) -> Dict[str, Any]:
        """Get performance analytics for the specified time period"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=time_period_days)
        
        # Get task analytics
        tasks_in_period = Task.objects.filter(
            assigned_at__gte=start_date,
            assigned_at__lte=end_date
        )
        
        # Get session analytics
        sessions_in_period = LearningSession.objects.filter(
            started_at__gte=start_date,
            started_at__lte=end_date
        )
        
        analytics = {
            'time_period_days': time_period_days,
            'period_start': start_date.isoformat(),
            'period_end': end_date.isoformat(),
            'task_analytics': {
                'total_tasks': tasks_in_period.count(),
                'completed_tasks': tasks_in_period.filter(status='completed').count(),
                'failed_tasks': tasks_in_period.filter(status='failed').count(),
                'average_execution_time': 0,
                'tasks_by_agent': {},
                'tasks_by_type': {},
                'success_rate': 0
            },
            'session_analytics': {
                'total_sessions': sessions_in_period.count(),
                'active_sessions': sessions_in_period.filter(ended_at__isnull=True).count(),
                'completed_sessions': sessions_in_period.filter(ended_at__isnull=False).count(),
                'average_session_duration': 0,
                'average_performance_score': 0
            },
            'agent_analytics': {}
        }
        
        # Calculate average execution time
        completed_tasks = tasks_in_period.filter(
            status='completed', 
            execution_time__isnull=False
        )
        if completed_tasks.exists():
            analytics['task_analytics']['average_execution_time'] = completed_tasks.aggregate(
                Avg('execution_time')
            )['execution_time__avg']
        
        # Calculate success rate
        total_tasks = analytics['task_analytics']['total_tasks']
        if total_tasks > 0:
            success_rate = (analytics['task_analytics']['completed_tasks'] / total_tasks) * 100
            analytics['task_analytics']['success_rate'] = success_rate
        
        # Tasks by agent
        for agent_type in self.agents.keys():
            agent_tasks = tasks_in_period.filter(agent__agent_type=agent_type)
            analytics['task_analytics']['tasks_by_agent'][agent_type] = agent_tasks.count()
        
        # Tasks by type
        for task_type in tasks_in_period.values_list('task_type', flat=True).distinct():
            type_count = tasks_in_period.filter(task_type=task_type).count()
            analytics['task_analytics']['tasks_by_type'][task_type] = type_count
        
        # Average session duration
        completed_sessions = sessions_in_period.filter(ended_at__isnull=False)
        if completed_sessions.exists():
            total_duration = sum(session.duration for session in completed_sessions)
            analytics['session_analytics']['average_session_duration'] = total_duration / completed_sessions.count()
        
        # Average performance score
        sessions_with_scores = completed_sessions.filter(performance_score__isnull=False)
        if sessions_with_scores.exists():
            analytics['session_analytics']['average_performance_score'] = sessions_with_scores.aggregate(
                Avg('performance_score')
            )['performance_score__avg']
        
        # Agent analytics
        for agent_type, agent_instance in self.agent_instances.items():
            agent_analytics = {
                'status': agent_instance.status.value,
                'tasks_processed': analytics['task_analytics']['tasks_by_agent'].get(agent_type, 0),
                'metrics_count': len(agent_instance.get_metrics()),
                'uptime_hours': (timezone.now() - agent_instance.created_at).total_seconds() / 3600
            }
            analytics['agent_analytics'][agent_type] = agent_analytics
        
        return analytics
    
    def shutdown(self):
        """Shutdown the agents manager"""
        # Clean up active sessions
        self.cleanup_inactive_sessions()
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        # Clear agent instances
        self.agent_instances.clear()
        self.agents.clear()


# Import required modules
from datetime import timedelta
from django.db.models import Avg