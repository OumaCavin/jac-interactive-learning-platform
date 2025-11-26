// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Knowledge Graph Service
 * 
 * Provides API integration for the knowledge graph functionality,
 * connecting frontend to backend knowledge graph endpoints.
 */

import { apiClient } from './apiClient';
import { toast } from 'react-hot-toast';

// Types for knowledge graph API responses
export interface KnowledgeNode {
  id: string;
  title: string;
  description: string;
  node_type: 'learning_path' | 'module' | 'concept' | 'lesson' | 'assessment';
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  x_position: number;
  y_position: number;
  z_position: number;
  width: number;
  height: number;
  content_uri?: string;
  jac_code?: string;
  learning_objectives: string[];
  prerequisites: string[];
  created_by: number;
  created_by_username: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
  view_count: number;
  outgoing_edges_count: number;
  incoming_edges_count: number;
}

export interface KnowledgeEdge {
  id: string;
  source_node: string;
  source_node_title: string;
  source_node_id: string;
  target_node: string;
  target_node_title: string;
  target_node_id: string;
  edge_type: 'prerequisite' | 'contains' | 'related' | 'mastery' | 'prerequisite_of' | 'leads_to';
  strength: number;
  curve_points?: { x: number; y: number; z: number }[];
  edge_weight: number;
  description?: string;
  examples?: string[];
  traversal_count: number;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface GraphData {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  meta: {
    total_nodes: number;
    total_edges: number;
    generated_at: string;
    filter_applied?: string;
  };
}

export interface TopicGraphData {
  topic: string;
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  statistics: {
    node_count: number;
    edge_count: number;
    concept_density: number;
  };
}

export interface ConceptRelationship {
  concept: string;
  related_concepts: Array<{
    concept: string;
    relationship_type: string;
    strength: number;
    description: string;
  }>;
  concept_relations: Array<{
    id: string;
    concept_from: string;
    relation_type: string;
    concept_to: string;
    strength: number;
    description: string;
    created_at: string;
  }>;
  learning_paths: Array<{
    path_id: string;
    path_title: string;
    concept_coverage: number;
    difficulty_progression: string[];
  }>;
}

export interface GraphAnalytics {
  total_nodes: number;
  total_edges: number;
  node_types: Record<string, number>;
  edge_types: Record<string, number>;
  difficulty_distribution: Record<string, number>;
  completion_statistics: {
    completed_paths: number;
    in_progress_paths: number;
    not_started_paths: number;
    average_completion_rate: number;
  };
  popular_paths: Array<{
    path_id: string;
    path_title: string;
    enrollment_count: number;
    completion_rate: number;
    average_rating: number;
  }>;
}

export interface GraphSearchParams {
  query?: string;
  node_types?: string[];
  difficulty_levels?: string[];
  edge_types?: string[];
  topics?: string[];
  limit?: number;
  offset?: number;
}

export interface GraphSearchResult {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  total_results: number;
  search_query: string;
  applied_filters: GraphSearchParams;
}

// Base API class
class KnowledgeGraphServiceClass {
  private readonly baseUrl = '/api/v1';

  /**
   * Get complete knowledge graph data
   * Maps to backend: GET /api/v1/knowledge-graph/
   */
  async getCompleteGraph(): Promise<GraphData> {
    try {
      const response = await apiClient.get<GraphData>(`${this.baseUrl}/knowledge-graph/`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching complete graph:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch knowledge graph');
    }
  }

  /**
   * Get topic-specific knowledge graph
   * Maps to backend: GET /api/v1/knowledge-graph/topic/
   */
  async getTopicGraph(topic: string): Promise<TopicGraphData> {
    try {
      const response = await apiClient.get<TopicGraphData>(
        `${this.baseUrl}/knowledge-graph/topic/`,
        { params: { topic } }
      );
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching topic graph for ${topic}:`, error);
      throw new Error(error.response?.data?.message || `Failed to fetch topic graph for ${topic}`);
    }
  }

  /**
   * Search knowledge graph with filters
   * Maps to backend: POST /api/v1/knowledge-graph/search/
   */
  async searchGraph(searchParams: GraphSearchParams): Promise<GraphSearchResult> {
    try {
      const response = await apiClient.post<GraphSearchResult>(
        `${this.baseUrl}/knowledge-graph/search/`,
        searchParams
      );
      return response.data;
    } catch (error: any) {
      console.error('Error searching graph:', error);
      throw new Error(error.response?.data?.message || 'Failed to search knowledge graph');
    }
  }

  /**
   * Get concept relationships
   * Maps to backend: GET /api/v1/concepts/relationships/
   */
  async getConceptRelationships(conceptId?: string): Promise<ConceptRelationship[]> {
    try {
      const url = conceptId 
        ? `${this.baseUrl}/concepts/relationships/?concept=${conceptId}`
        : `${this.baseUrl}/concepts/relationships/`;
      
      const response = await apiClient.get<ConceptRelationship[]>(url);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching concept relationships:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch concept relationships');
    }
  }

  /**
   * Get graph analytics
   * Maps to backend: GET /api/v1/analytics/
   */
  async getGraphAnalytics(): Promise<GraphAnalytics> {
    try {
      const response = await apiClient.get<GraphAnalytics>(`${this.baseUrl}/analytics/`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching graph analytics:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch graph analytics');
    }
  }

  /**
   * Get learning path recommendations
   * Maps to backend: GET /api/v1/recommendations/
   */
  async getLearningPathRecommendations(userId?: number): Promise<any[]> {
    try {
      const url = userId 
        ? `${this.baseUrl}/recommendations/?user=${userId}`
        : `${this.baseUrl}/recommendations/`;
      
      const response = await apiClient.get(url);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching learning path recommendations:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch learning path recommendations');
    }
  }

  /**
   * Get concept domains
   * Maps to backend: GET /api/v1/concepts/domains/
   */
  async getConceptDomains(): Promise<Array<{ domain: string; node_count: number }>> {
    try {
      const response = await apiClient.get(`${this.baseUrl}/concepts/domains/`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching concept domains:', error);
      throw new Error(error.response?.data?.message || 'Failed to fetch concept domains');
    }
  }

  /**
   * Generate learning paths for a topic
   * Maps to backend: POST /api/v1/paths/generate/
   */
  async generateLearningPaths(params: {
    topic: string;
    difficulty_level?: string;
    learning_style?: string;
    time_estimate?: number;
  }): Promise<any> {
    try {
      const response = await apiClient.post(`${this.baseUrl}/paths/generate/`, params);
      return response.data;
    } catch (error: any) {
      console.error('Error generating learning paths:', error);
      throw new Error(error.response?.data?.message || 'Failed to generate learning paths');
    }
  }

  /**
   * Get nodes for a specific graph
   * Maps to backend: GET /api/v1/graphs/{graph_id}/nodes/
   */
  async getGraphNodes(graphId: string): Promise<KnowledgeNode[]> {
    try {
      const response = await apiClient.get<KnowledgeNode[]>(`${this.baseUrl}/graphs/${graphId}/nodes/`);
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching nodes for graph ${graphId}:`, error);
      throw new Error(error.response?.data?.message || `Failed to fetch nodes for graph ${graphId}`);
    }
  }

  /**
   * Get edges for a specific graph
   * Maps to backend: GET /api/v1/graphs/{graph_id}/edges/
   */
  async getGraphEdges(graphId: string): Promise<KnowledgeEdge[]> {
    try {
      const response = await apiClient.get<KnowledgeEdge[]>(`${this.baseUrl}/graphs/${graphId}/edges/`);
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching edges for graph ${graphId}:`, error);
      throw new Error(error.response?.data?.message || `Failed to fetch edges for graph ${graphId}`);
    }
  }

  /**
   * Increment view count for a node
   * Maps to backend: POST /api/v1/graph/nodes/{node_id}/increment-view/
   */
  async incrementNodeView(nodeId: string): Promise<{ status: string; view_count: number }> {
    try {
      const response = await apiClient.post(`${this.baseUrl}/graph/nodes/${nodeId}/increment-view/`);
      return response.data;
    } catch (error: any) {
      console.error(`Error incrementing view for node ${nodeId}:`, error);
      throw new Error(error.response?.data?.message || `Failed to increment view count for node ${nodeId}`);
    }
  }

  /**
   * Get specific node details
   * Maps to backend: GET /api/v1/nodes/{node_id}/
   */
  async getNode(nodeId: string): Promise<KnowledgeNode> {
    try {
      const response = await apiClient.get<KnowledgeNode>(`${this.baseUrl}/nodes/${nodeId}/`);
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching node ${nodeId}:`, error);
      throw new Error(error.response?.data?.message || `Failed to fetch node ${nodeId}`);
    }
  }

  /**
   * Get edges for a specific node
   * Maps to backend: GET /api/v1/graph/nodes/{node_id}/edges/
   */
  async getNodeEdges(nodeId: string): Promise<KnowledgeEdge[]> {
    try {
      const response = await apiClient.get<KnowledgeEdge[]>(`${this.baseUrl}/graph/nodes/${nodeId}/edges/`);
      return response.data;
    } catch (error: any) {
      console.error(`Error fetching edges for node ${nodeId}:`, error);
      throw new Error(error.response?.data?.message || `Failed to fetch edges for node ${nodeId}`);
    }
  }
}

// Enhanced API endpoints for JAC knowledge graph and AI agents
export const enhancedKnowledgeGraphService = {
  // Get all concepts with filtering and pagination
  getConcepts: async (params: {
    node_type?: string;
    difficulty_level?: string;
    category?: string;
    search?: string;
    limit?: number;
    offset?: number;
  } = {}): Promise<{ success: boolean; data: { concepts: any[]; pagination: any } }> => {
    try {
      const queryParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
      const response = await apiClient.get(`/api/knowledge-graph/api-extended/concepts/?${queryParams.toString()}`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching concepts:', error);
      throw new Error(error.response?.data?.error || 'Failed to fetch concepts');
    }
  },

  // Get concept relationships and connections
  getConceptRelations: async (conceptId: string, params: {
    relation_type?: string;
    depth?: number;
  } = {}): Promise<{ success: boolean; data: { relationships: any[]; depth: number; total_relations: number } }> => {
    try {
      const queryParams = new URLSearchParams({ concept_id: conceptId });
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
      const response = await apiClient.get(`/api/knowledge-graph/api-extended/concept_relations/?${queryParams.toString()}`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching concept relations:', error);
      throw new Error(error.response?.data?.error || 'Failed to fetch concept relations');
    }
  },

  // Get available learning paths
  getLearningPaths: async (params: {
    user_id?: string;
    difficulty_level?: string;
    category?: string;
  } = {}): Promise<{ success: boolean; data: { learning_paths: any[] } }> => {
    try {
      const queryParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
      const response = await apiClient.get(`/api/knowledge-graph/api-extended/learning_paths/?${queryParams.toString()}`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching learning paths:', error);
      throw new Error(error.response?.data?.error || 'Failed to fetch learning paths');
    }
  },

  // Get personalized recommendations
  getPersonalizedRecommendations: async (userId: string): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.get(`/api/knowledge-graph/api-extended/personalized_recommendations/?user_id=${userId}`);
      return response.data;
    } catch (error: any) {
      console.error('Error fetching personalized recommendations:', error);
      throw new Error(error.response?.data?.error || 'Failed to fetch personalized recommendations');
    }
  },

  // Track concept interaction
  trackConceptInteraction: async (data: {
    user_id: string;
    concept_id: string;
    interaction_type: 'view' | 'study' | 'practice' | 'mastered';
  }): Promise<{ success: boolean; message: string; data: any }> => {
    try {
      const response = await apiClient.post('/api/knowledge-graph/api-extended/track_concept_interaction/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error tracking concept interaction:', error);
      throw new Error(error.response?.data?.error || 'Failed to track concept interaction');
    }
  },

  // Populate JAC knowledge graph (admin only)
  populateJACKnowledgeGraph: async (): Promise<{ success: boolean; message: string; data: any }> => {
    try {
      const response = await apiClient.post('/api/knowledge-graph/api-extended/populate_jac_knowledge_graph/');
      return response.data;
    } catch (error: any) {
      console.error('Error populating JAC knowledge graph:', error);
      throw new Error(error.response?.data?.error || 'Failed to populate JAC knowledge graph');
    }
  }
};

// AI Multi-Agent System Service
export const aiAgentsService = {
  // Get available AI agents
  getAvailableAgents: async (): Promise<{ success: boolean; data: { agents: any[]; total_agents: number } }> => {
    try {
      const response = await apiClient.get('/api/ai-agents/ai-agents/available_agents/');
      return response.data;
    } catch (error: any) {
      console.error('Error fetching available agents:', error);
      throw new Error(error.response?.data?.error || 'Failed to fetch available agents');
    }
  },

  // Chat with AI agents
  chat: async (data: {
    message: string;
    agent_type?: string;
    session_id?: string;
    context?: any;
  }): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.post('/api/ai-agents/ai-agents/chat/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error chatting with AI agent:', error);
      throw new Error(error.response?.data?.error || 'Failed to chat with AI agent');
    }
  },

  // Multi-agent collaboration
  multiAgentCollaboration: async (data: {
    message: string;
    context?: any;
  }): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.post('/api/ai-agents/ai-agents/multi_agent_collaboration/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error with multi-agent collaboration:', error);
      throw new Error(error.response?.data?.error || 'Failed with multi-agent collaboration');
    }
  },

  // Generate learning content
  generateLearningContent: async (data: {
    topic: string;
    difficulty?: string;
    content_type?: string;
    learning_objectives?: string[];
    include_examples?: boolean;
  }): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.post('/api/ai-agents/ai-agents/generate_learning_content/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error generating learning content:', error);
      throw new Error(error.response?.data?.error || 'Failed to generate learning content');
    }
  },

  // Review code with AI
  reviewCode: async (data: {
    code: string;
    language?: string;
    review_type?: string;
  }): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.post('/api/ai-agents/ai-agents/review_code/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error getting code review:', error);
      throw new Error(error.response?.data?.error || 'Failed to get code review');
    }
  },

  // Get learning path recommendations
  getLearningPathRecommendation: async (data: {
    learning_goals: string[];
    time_available?: string;
    preferred_difficulty?: string;
  }): Promise<{ success: boolean; data: any }> => {
    try {
      const response = await apiClient.post('/api/ai-agents/ai-agents/get_learning_path_recommendation/', data);
      return response.data;
    } catch (error: any) {
      console.error('Error getting learning path recommendation:', error);
      throw new Error(error.response?.data?.error || 'Failed to get learning path recommendation');
    }
  }
};

// Combined service functions for enhanced functionality
export const enhancedServices = {
  // Get comprehensive learning assistance
  getLearningAssistance: async (userQuery: string, userId: string) => {
    try {
      // Get personalized recommendations
      const recommendations = await enhancedKnowledgeGraphService.getPersonalizedRecommendations(userId);
      
      // Get agent response
      const agentResponse = await aiAgentsService.chat({
        message: userQuery,
        agent_type: 'learning_assistant',
        context: {
          personalized_recommendations: recommendations.data,
          user_id: userId
        }
      });

      return {
        recommendations: recommendations.data,
        agent_response: agentResponse.data,
        success: true
      };
    } catch (error) {
      console.error('Error getting learning assistance:', error);
      return { success: false, error };
    }
  },

  // Get code review with knowledge context
  getCodeReviewWithContext: async (code: string, language: string, userId: string) => {
    try {
      // Get relevant concepts
      const concepts = await enhancedKnowledgeGraphService.getConcepts({
        search: language,
        limit: 5
      });

      // Get code review
      const review = await aiAgentsService.reviewCode({
        code,
        language,
        review_type: 'comprehensive'
      });

      return {
        code_review: review.data,
        relevant_concepts: concepts.data.concepts,
        success: true
      };
    } catch (error) {
      console.error('Error getting code review:', error);
      return { success: false, error };
    }
  },

  // Generate personalized learning path
  generatePersonalizedPath: async (goals: string[], userId: string) => {
    try {
      // Get user knowledge state
      const recommendations = await enhancedKnowledgeGraphService.getPersonalizedRecommendations(userId);
      
      // Get AI path recommendation
      const aiPath = await aiAgentsService.getLearningPathRecommendation({
        learning_goals: goals,
        preferred_difficulty: 'intermediate'
      });

      return {
        ai_path_recommendation: aiPath.data,
        personalized_recommendations: recommendations.data,
        success: true
      };
    } catch (error) {
      console.error('Error generating personalized path:', error);
      return { success: false, error };
    }
  }
};

// Create and export service instances
const knowledgeGraphService = new KnowledgeGraphServiceClass();
export { enhancedKnowledgeGraphService, aiAgentsService, enhancedServices };
export default knowledgeGraphService;