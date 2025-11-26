// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Agent slice
 * Manages multi-agent system state and agent interactions
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Types for agent state
export interface Agent {
  id: string;
  name: string;
  type: 'content_curator' | 'quiz_master' | 'evaluator' | 'progress_tracker' | 'motivator' | 'orchestrator';
  description: string;
  status: 'active' | 'inactive' | 'busy';
  isTyping?: boolean;
  capabilities: string[];
  personality: {
    tone: 'friendly' | 'professional' | 'encouraging' | 'analytical';
    communication_style: 'verbose' | 'concise' | 'adaptive';
  };
}

export interface AgentMessage {
  id: string;
  agent_id: string;
  user_id: string;
  content: string;
  type: 'text' | 'code' | 'recommendation' | 'feedback' | 'explanation';
  timestamp: string;
  metadata?: any;
  is_read: boolean;
}

export interface AgentRecommendation {
  id: string;
  agent_id: string;
  user_id: string;
  type: 'content' | 'exercise' | 'review' | 'goal' | 'difficulty';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'pending' | 'accepted' | 'dismissed' | 'expired';
  expires_at: string;
  metadata?: any;
  created_at: string;
}

export interface AgentTask {
  id: string;
  agent_id: string;
  user_id: string;
  task_type: 'content_generation' | 'assessment_creation' | 'progress_analysis' | 'code_evaluation' | 'motivation';
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  input: any;
  output?: any;
  created_at: string;
  completed_at?: string;
  error_message?: string;
}

export interface AgentState {
  // Agents
  agents: Agent[];
  active_agents: string[];
  
  // Messages and conversations
  conversations: { [agentId: string]: AgentMessage[] };
  unread_counts: { [agentId: string]: number };
  
  // Recommendations
  recommendations: AgentRecommendation[];
  pending_recommendations: AgentRecommendation[];
  
  // Tasks
  tasks: AgentTask[];
  active_tasks: AgentTask[];
  
  // UI state
  isLoading: boolean;
  isTyping: { [agentId: string]: boolean };
  error: string | null;
  
  // Chat interface
  selected_agent: string | null;
  chat_visible: boolean;
}

// Initial state
const initialState: AgentState = {
  // Agents
  agents: [],
  active_agents: [],
  
  // Messages and conversations
  conversations: {},
  unread_counts: {},
  
  // Recommendations
  recommendations: [],
  pending_recommendations: [],
  
  // Tasks
  tasks: [],
  active_tasks: [],
  
  // UI state
  isLoading: false,
  isTyping: {},
  error: null,
  
  // Chat interface
  selected_agent: null,
  chat_visible: false,
};

// Agent slice
const agentSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    // Agent management
    setAgents: (state, action: PayloadAction<Agent[]>) => {
      state.agents = action.payload;
    },
    addAgent: (state, action: PayloadAction<Agent>) => {
      state.agents.push(action.payload);
    },
    updateAgent: (state, action: PayloadAction<Agent>) => {
      const index = state.agents.findIndex(a => a.id === action.payload.id);
      if (index !== -1) {
        state.agents[index] = action.payload;
      }
    },
    setActiveAgents: (state, action: PayloadAction<string[]>) => {
      state.active_agents = action.payload;
    },
    setAgentStatus: (state, action: PayloadAction<{ agentId: string; status: Agent['status'] }>) => {
      const agent = state.agents.find(a => a.id === action.payload.agentId);
      if (agent) {
        agent.status = action.payload.status;
      }
    },
    
    // Messages and conversations
    addMessage: (state, action: PayloadAction<AgentMessage>) => {
      const { agent_id, is_read } = action.payload;
      
      if (!state.conversations[agent_id]) {
        state.conversations[agent_id] = [];
      }
      
      state.conversations[agent_id].push(action.payload);
      
      // Update unread count if message is from agent
      if (!is_read && action.payload.agent_id) {
        if (!state.unread_counts[agent_id]) {
          state.unread_counts[agent_id] = 0;
        }
        state.unread_counts[agent_id] += 1;
      }
    },
    markMessagesAsRead: (state, action: PayloadAction<{ agentId: string }>) => {
      const { agentId } = action.payload;
      if (state.conversations[agentId]) {
        state.conversations[agentId] = state.conversations[agentId].map(msg => ({
          ...msg,
          is_read: true,
        }));
        state.unread_counts[agentId] = 0;
      }
    },
    clearConversation: (state, action: PayloadAction<string>) => {
      const agentId = action.payload;
      delete state.conversations[agentId];
      delete state.unread_counts[agentId];
    },
    
    // Recommendations
    setRecommendations: (state, action: PayloadAction<AgentRecommendation[]>) => {
      state.recommendations = action.payload;
      state.pending_recommendations = action.payload.filter(r => r.status === 'pending');
    },
    addRecommendation: (state, action: PayloadAction<AgentRecommendation>) => {
      state.recommendations.push(action.payload);
      if (action.payload.status === 'pending') {
        state.pending_recommendations.push(action.payload);
      }
    },
    updateRecommendation: (state, action: PayloadAction<AgentRecommendation>) => {
      const index = state.recommendations.findIndex(r => r.id === action.payload.id);
      if (index !== -1) {
        state.recommendations[index] = action.payload;
        
        // Update pending recommendations
        const pendingIndex = state.pending_recommendations.findIndex(r => r.id === action.payload.id);
        if (action.payload.status === 'pending') {
          if (pendingIndex !== -1) {
            state.pending_recommendations[pendingIndex] = action.payload;
          } else {
            state.pending_recommendations.push(action.payload);
          }
        } else if (pendingIndex !== -1) {
          state.pending_recommendations.splice(pendingIndex, 1);
        }
      }
    },
    dismissRecommendation: (state, action: PayloadAction<string>) => {
      const recommendation = state.recommendations.find(r => r.id === action.payload);
      if (recommendation) {
        recommendation.status = 'dismissed';
        state.pending_recommendations = state.pending_recommendations.filter(r => r.id !== action.payload);
      }
    },
    
    // Tasks
    setTasks: (state, action: PayloadAction<AgentTask[]>) => {
      state.tasks = action.payload;
      state.active_tasks = action.payload.filter(t => 
        t.status === 'pending' || t.status === 'in_progress'
      );
    },
    addTask: (state, action: PayloadAction<AgentTask>) => {
      state.tasks.push(action.payload);
      if (action.payload.status === 'pending' || action.payload.status === 'in_progress') {
        state.active_tasks.push(action.payload);
      }
    },
    updateTask: (state, action: PayloadAction<AgentTask>) => {
      const index = state.tasks.findIndex(t => t.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
        
        // Update active tasks
        if (action.payload.status === 'pending' || action.payload.status === 'in_progress') {
          const activeIndex = state.active_tasks.findIndex(t => t.id === action.payload.id);
          if (activeIndex !== -1) {
            state.active_tasks[activeIndex] = action.payload;
          } else {
            state.active_tasks.push(action.payload);
          }
        } else {
          state.active_tasks = state.active_tasks.filter(t => t.id !== action.payload.id);
        }
      }
    },
    
    // UI state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setTyping: (state, action: PayloadAction<{ agentId: string; isTyping: boolean }>) => {
      state.isTyping[action.payload.agentId] = action.payload.isTyping;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    
    // Chat interface
    setSelectedAgent: (state, action: PayloadAction<string | null>) => {
      state.selected_agent = action.payload;
      if (action.payload) {
        // Mark messages as read when agent is selected
        agentSlice.caseReducers.markMessagesAsRead(state, { 
          payload: { agentId: action.payload } 
        } as any);
      }
    },
    setChatVisible: (state, action: PayloadAction<boolean>) => {
      state.chat_visible = action.payload;
    },
    toggleChat: (state) => {
      state.chat_visible = !state.chat_visible;
    },
    
    // Cleanup
    clearAgentData: (state) => {
      state.conversations = {};
      state.unread_counts = {};
      state.recommendations = [];
      state.pending_recommendations = [];
      state.tasks = [];
      state.active_tasks = [];
      state.selected_agent = null;
      state.chat_visible = false;
    },
  },
});

// Export actions
export const {
  // Agent management
  setAgents,
  addAgent,
  updateAgent,
  setActiveAgents,
  setAgentStatus,
  
  // Messages and conversations
  addMessage,
  markMessagesAsRead,
  clearConversation,
  
  // Recommendations
  setRecommendations,
  addRecommendation,
  updateRecommendation,
  dismissRecommendation,
  
  // Tasks
  setTasks,
  addTask,
  updateTask,
  
  // UI state
  setLoading,
  setTyping,
  setError,
  clearError,
  
  // Chat interface
  setSelectedAgent,
  setChatVisible,
  toggleChat,
  
  // Cleanup
  clearAgentData,
} = agentSlice.actions;

// Selectors
export const selectAgents = (state: RootState) => state.agents.agents;
export const selectActiveAgents = (state: RootState) => 
  state.agents.agents.filter(a => state.agents.active_agents.includes(a.id));
export const selectAgentById = (state: RootState, agentId: string) => 
  state.agents.agents.find(a => a.id === agentId);
export const selectConversations = (state: RootState) => state.agents.conversations;
export const selectConversation = (state: RootState, agentId: string) => 
  state.agents.conversations[agentId] || [];
export const selectUnreadCounts = (state: RootState) => state.agents.unread_counts;
export const selectRecommendations = (state: RootState) => state.agents.recommendations;
export const selectPendingRecommendations = (state: RootState) => 
  state.agents.pending_recommendations;
export const selectTasks = (state: RootState) => state.agents.tasks;
export const selectActiveTasks = (state: RootState) => state.agents.active_tasks;
export const selectSelectedAgent = (state: RootState) => {
  const agentId = state.agents.selected_agent;
  return agentId ? state.agents.agents.find(a => a.id === agentId) : null;
};
export const selectChatVisible = (state: RootState) => state.agents.chat_visible;
export const selectAgentTyping = (state: RootState, agentId: string) => 
  state.agents.isTyping[agentId] || false;

// Export reducer
export default agentSlice.reducer;