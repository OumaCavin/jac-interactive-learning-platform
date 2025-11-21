import axios from 'axios';
import api from './learningService';

// Types for agents
export interface Agent {
  id: number;
  name: string;
  type: 'code_evaluator' | 'learning_coordinator' | 'content_generator' | 'progress_tracker' | 'chat_assistant' | 'knowledge_graph';
  status: 'idle' | 'busy' | 'error';
  current_task: string | null;
  performance_metrics: {
    tasks_completed: number;
    average_response_time: number;
    success_rate: number;
  };
  capabilities: string[];
  created_at: string;
}

export interface Task {
  id: number;
  agent: number;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  input_data: any;
  output_data: any;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  estimated_duration: number;
  actual_duration: number | null;
}

export interface ChatMessage {
  id: number;
  agent: number;
  user: number;
  message: string;
  response: string;
  session_id: string;
  created_at: string;
  feedback_rating: number | null;
}

export interface AgentMetrics {
  agent_id: number;
  total_requests: number;
  successful_requests: number;
  average_response_time: number;
  total_execution_time: number;
  memory_usage: {
    peak: number;
    average: number;
  };
  error_rate: number;
  last_updated: string;
}

// Agent API Service
export const agentService = {
  // Agent Management
  getAgents: (): Promise<Agent[]> =>
    api.get('/agents/').then(res => res.data),

  getAgent: (id: number): Promise<Agent> =>
    api.get(`/agents/${id}/`).then(res => res.data),

  createAgent: (data: Partial<Agent>): Promise<Agent> =>
    api.post('/agents/', data).then(res => res.data),

  updateAgent: (id: number, data: Partial<Agent>): Promise<Agent> =>
    api.patch(`/agents/${id}/`, data).then(res => res.data),

  deleteAgent: (id: number): Promise<void> =>
    api.delete(`/agents/${id}/`),

  // Task Management
  getTasks: (agentId?: number): Promise<Task[]> => {
    const url = agentId ? `/tasks/?agent=${agentId}` : '/tasks/';
    return api.get(url).then(res => res.data);
  },

  getTask: (id: number): Promise<Task> =>
    api.get(`/tasks/${id}/`).then(res => res.data),

  createTask: (data: Partial<Task>): Promise<Task> =>
    api.post('/tasks/', data).then(res => res.data),

  updateTask: (id: number, data: Partial<Task>): Promise<Task> =>
    api.patch(`/tasks/${id}/`, data).then(res => res.data),

  // Specialized Agent Actions
  evaluateCode: (code: string, language: 'python' | 'jac', testCases?: any[]): Promise<any> =>
    api.post('/agents/code-evaluator/evaluate/', { 
      code, 
      language, 
      test_cases: testCases 
    }).then(res => res.data),

  generateLearningContent: (topic: string, difficulty: string, learningStyle?: string): Promise<any> =>
    api.post('/agents/content-generator/generate/', { 
      topic, 
      difficulty, 
      learning_style: learningStyle 
    }).then(res => res.data),

  trackProgress: (userId: number, moduleId: number, progressData: any): Promise<any> =>
    api.post('/agents/progress-tracker/track/', { 
      user_id: userId, 
      module_id: moduleId, 
      progress_data: progressData 
    }).then(res => res.data),

  // Chat Assistant
  sendChatMessage: (message: string, sessionId?: string): Promise<ChatMessage> =>
    api.post('/agents/chat-assistant/message/', { 
      message, 
      session_id: sessionId 
    }).then(res => res.data),

  getChatHistory: (sessionId: string): Promise<ChatMessage[]> =>
    api.get(`/agents/chat-assistant/history/?session_id=${sessionId}`).then(res => res.data),

  rateChatResponse: (messageId: number, rating: number): Promise<void> =>
    api.post(`/agents/chat-assistant/rate/${messageId}/`, { rating }),

  // Knowledge Graph
  getKnowledgeGraph: (topic?: string): Promise<any> => {
    const url = topic ? `/agents/knowledge-graph/?topic=${topic}` : '/agents/knowledge-graph/';
    return api.get(url).then(res => res.data);
  },

  getConceptRelations: (concept: string): Promise<any> =>
    api.get(`/agents/knowledge-graph/relations/?concept=${concept}`).then(res => res.data),

  // Metrics and Analytics
  getAgentMetrics: (agentId?: number): Promise<AgentMetrics[]> => {
    const url = agentId ? `/agents/${agentId}/metrics/` : '/agents/metrics/';
    return api.get(url).then(res => res.data);
  },

  getSystemMetrics: (): Promise<any> =>
    api.get('/agents/system-metrics/').then(res => res.data),

  // Learning Coordinator
  getLearningPath: (userId: number): Promise<any> =>
    api.post('/agents/learning-coordinator/recommend/', { user_id: userId }).then(res => res.data),

  updateLearningProgress: (userId: number, moduleId: number, completionData: any): Promise<any> =>
    api.post('/agents/learning-coordinator/progress/', { 
      user_id: userId, 
      module_id: moduleId, 
      completion_data: completionData 
    }).then(res => res.data),

  // Utility Methods
  getAvailableAgents: (taskType: string): Promise<Agent[]> =>
    api.get(`/agents/available/?task_type=${taskType}`).then(res => res.data),

  getAgentStatus: (): Promise<any> =>
    api.get('/agents/status/').then(res => res.data),

  restartAgent: (agentId: number): Promise<Agent> =>
    api.post(`/agents/${agentId}/restart/`).then(res => res.data),

  getAgentLogs: (agentId: number, limit?: number): Promise<any[]> => {
    const url = limit ? `/agents/${agentId}/logs/?limit=${limit}` : `/agents/${agentId}/logs/`;
    return api.get(url).then(res => res.data);
  },
};

export default agentService;