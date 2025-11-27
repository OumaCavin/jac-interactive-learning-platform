// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import axios from 'axios';
import { apiClient } from './apiClient';

// Types for agents
export interface Agent {
  id: number;
  name: string;
  type: 'code_evaluator' | 'learning_coordinator' | 'content_generator' | 'progress_tracker' | 'chat_assistant' | 'knowledge_graph';
  status: 'idle' | 'busy' | 'error';
  current_task: string | null;
  isTyping?: boolean;
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
    apiClient.get('/agents/').then(res => res.data),

  getAgent: (id: number): Promise<Agent> =>
    apiClient.get(`/agents/${id}/`).then(res => res.data),

  createAgent: (data: Partial<Agent>): Promise<Agent> =>
    apiClient.post('/agents/', data).then(res => res.data),

  updateAgent: (id: number, data: Partial<Agent>): Promise<Agent> =>
    apiClient.patch(`/agents/${id}/`, data).then(res => res.data),

  deleteAgent: (id: number): Promise<void> =>
    apiClient.delete(`/agents/${id}/`),

  // Task Management
  getTasks: (agentId?: number): Promise<Task[]> => {
    const url = agentId ? `/tasks/?agent=${agentId}` : '/tasks/';
    return apiClient.get(url).then(res => res.data);
  },

  getTask: (id: number): Promise<Task> =>
    apiClient.get(`/tasks/${id}/`).then(res => res.data),

  createTask: (data: Partial<Task>): Promise<Task> =>
    apiClient.post('/tasks/', data).then(res => res.data),

  updateTask: (id: number, data: Partial<Task>): Promise<Task> =>
    apiClient.patch(`/tasks/${id}/`, data).then(res => res.data),

  // Specialized Agent Actions
  evaluateCode: (code: string, language: 'python' | 'jac', testCases?: any[]): Promise<any> =>
    apiClient.post('/agents/code-evaluator/evaluate/', { 
      code, 
      language, 
      test_cases: testCases 
    }).then(res => res.data),

  generateLearningContent: (topic: string, difficulty: string, learningStyle?: string): Promise<any> =>
    apiClient.post('/agents/content-generator/generate/', { 
      topic, 
      difficulty, 
      learning_style: learningStyle 
    }).then(res => res.data),

  trackProgress: (userId: number, moduleId: number, progressData: any): Promise<any> =>
    apiClient.post('/agents/progress-tracker/track/', { 
      user_id: userId, 
      module_id: moduleId, 
      progress_data: progressData 
    }).then(res => res.data),

  // Chat Assistant
  sendChatMessage: (message: string, sessionId?: string): Promise<ChatMessage> =>
    apiClient.post('/agents/chat-assistant/message/', { 
      message, 
      session_id: sessionId 
    }).then(res => res.data),

  getChatHistory: (sessionId: string): Promise<ChatMessage[]> =>
    apiClient.get(`/agents/chat-assistant/history/?session_id=${sessionId}`).then(res => res.data),

  rateChatResponse: (messageId: number, rating: number): Promise<void> =>
    apiClient.post(`/agents/chat-assistant/rate/${messageId}/`, { rating }),

  // Knowledge Graph
  getKnowledgeGraph: (topic?: string): Promise<any> => {
    const url = topic ? `/agents/knowledge-graph/?topic=${topic}` : '/agents/knowledge-graph/';
    return apiClient.get(url).then(res => res.data);
  },

  getConceptRelations: (concept: string): Promise<any> =>
    apiClient.get(`/agents/knowledge-graph/relations/?concept=${concept}`).then(res => res.data),

  // Metrics and Analytics
  getAgentMetrics: (agentId?: number): Promise<AgentMetrics[]> => {
    const url = agentId ? `/agents/${agentId}/metrics/` : '/agents/metrics/';
    return apiClient.get(url).then(res => res.data);
  },

  getSystemMetrics: (): Promise<any> =>
    apiClient.get('/agents/system-metrics/').then(res => res.data),

  // Learning Coordinator
  getLearningPath: (userId: number): Promise<any> =>
    apiClient.post('/agents/learning-coordinator/recommend/', { user_id: userId }).then(res => res.data),

  updateLearningProgress: (userId: number, moduleId: number, completionData: any): Promise<any> =>
    apiClient.post('/agents/learning-coordinator/progress/', { 
      user_id: userId, 
      module_id: moduleId, 
      completion_data: completionData 
    }).then(res => res.data),

  // Utility Methods
  getAvailableAgents: (taskType: string): Promise<Agent[]> =>
    apiClient.get(`/agents/available/?task_type=${taskType}`).then(res => res.data),

  getAgentStatus: (): Promise<any> =>
    apiClient.get('/agents/status/').then(res => res.data),

  restartAgent: (agentId: number): Promise<Agent> =>
    apiClient.post(`/agents/${agentId}/restart/`).then(res => res.data),

  getAgentLogs: (agentId: number, limit?: number): Promise<any[]> => {
    const url = limit ? `/agents/${agentId}/logs/?limit=${limit}` : `/agents/${agentId}/logs/`;
    return apiClient.get(url).then(res => res.data);
  },
};

export default agentService;