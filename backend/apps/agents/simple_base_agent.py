# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Simplified Base Agent Architecture for JAC Interactive Learning Platform

This module provides a simplified foundation for all AI agents without dependencies
on other apps for the initial implementation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from enum import Enum
import json
import uuid
from datetime import datetime


class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    ACTIVE = "active"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class SimpleAgent(ABC):
    """
    Simplified abstract base class for all AI agents in the learning platform.
    
    This version doesn't depend on Django models to allow for standalone testing.
    """
    
    def __init__(self, agent_id: str, agent_type: str, config: Dict[str, Any] = None):
        """
        Initialize the agent with unique identifier and configuration
        
        Args:
            agent_id: Unique identifier for the agent instance
            agent_type: Type/category of the agent
            config: Configuration dictionary for agent-specific settings
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_type = agent_type
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.task_queue = []
        self.metrics = {}
        
    @abstractmethod
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a specific task and return results
        
        Args:
            task: Task dictionary containing action and parameters
            
        Returns:
            Dictionary containing task results or error information
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get list of capabilities this agent provides
        
        Returns:
            List of capability strings
        """
        pass
    
    @abstractmethod
    def get_specialization_info(self) -> Dict[str, Any]:
        """
        Get detailed information about agent specialization
        
        Returns:
            Dictionary containing specialization details
        """
        pass
    
    def update_status(self, status: AgentStatus):
        """Update agent status"""
        self.status = status
        self.last_active = datetime.now()
    
    def add_to_queue(self, task: Dict[str, Any], priority: TaskPriority = TaskPriority.MEDIUM):
        """Add task to the processing queue"""
        task_data = {
            'task': task,
            'priority': priority,
            'timestamp': datetime.now(),
            'task_id': str(uuid.uuid4())
        }
        self.task_queue.append(task_data)
        # Sort queue by priority (higher priority first)
        self.task_queue.sort(key=lambda x: x['priority'].value, reverse=True)
    
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Get next task from queue"""
        if self.task_queue:
            return self.task_queue.pop(0)
        return None
    
    def update_metrics(self, metric_name: str, value: Any):
        """Update agent metrics"""
        self.metrics[metric_name] = {
            'value': value,
            'timestamp': datetime.now()
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current agent metrics"""
        return self.metrics.copy()
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on the agent"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'status': self.status.value,
            'last_active': self.last_active.isoformat(),
            'queue_size': len(self.task_queue),
            'metrics_count': len(self.metrics),
            'uptime_hours': (datetime.now() - self.created_at).total_seconds() / 3600
        }
    
    def __str__(self):
        return f"{self.agent_type}Agent({self.agent_id})"
    
    def __repr__(self):
        return f"<{self.agent_type}Agent id={self.agent_id} status={self.status.value}>"