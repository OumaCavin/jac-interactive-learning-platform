// JAC Learning Platform - TypeScript utilities by Cavin Otieno

// Temporary stub for agentService to resolve build issues
// This will be replaced with the actual implementation

export interface ChatMessage {
  id: string;
  agent: string;
  user: string;
  message: string;
  response?: string;
  created_at: string;
}

export interface Agent {
  id: string;
  name: string;
  type: string;
  status: string;
  current_task?: string;
}

export const agentService = {
  getAgents: async (): Promise<Agent[]> => {
    // Return empty array for now
    return [];
  },

  getChatHistory: async (sessionId: string): Promise<ChatMessage[]> => {
    // Return empty array for now
    return [];
  },

  sendChatMessage: async (message: string, sessionId: string): Promise<any> => {
    // Return mock response for now
    return {
      response: "Chat service temporarily unavailable",
      messageId: Date.now().toString()
    };
  },

  rateChatResponse: async (messageId: string, rating: number): Promise<void> => {
    // Do nothing for now
  }
};