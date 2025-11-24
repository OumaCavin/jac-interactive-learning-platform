import React, { useState, useEffect, useRef } from 'react';
import { useDispatch } from 'react-redux';
import { useAppSelector } from '../store/store';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, Button, Badge } from '../components/ui';
import agentService, {
  ChatMessage 
} from '../services/agentService';
import { 
  selectAgents, 
  selectSelectedAgent,
  selectAgentTyping,
  selectConversation,
  selectAgentById,
  setSelectedAgent,
  addMessage,
  setTyping,
  markMessagesAsRead,
  clearError 
} from '../store/slices/agentSlice';

interface ChatState {
  message: string;
  isLoading: boolean;
  sessionId: string;
}

const Chat: React.FC = () => {
  const dispatch = useDispatch();
  const agents = useAppSelector(selectAgents);
  const selectedAgent = useAppSelector(selectSelectedAgent);
  const typing = useAppSelector(state => selectedAgent ? selectAgentTyping(state, selectedAgent.id) : false);
  const conversation = useAppSelector(state => selectedAgent ? selectConversation(state, selectedAgent.id) : []);
  
  const [chatState, setChatState] = useState<ChatState>({
    message: '',
    isLoading: false,
    sessionId: `chat-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  });
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation]);

  // Load agents on component mount
  useEffect(() => {
    const loadAgents = async () => {
      try {
        const agentsData = await agentService.getAgents();
        // Filter for available agents
        const chatAgents = agentsData.filter(agent => 
          agent.status === 'active' || 
          agent.status === 'busy'
        );
        
        // If no chat assistant found, use the first available agent
        if (chatAgents.length > 0 && !selectedAgent) {
          dispatch(setSelectedAgent(chatAgents[0].id));
        }
      } catch (error) {
        // Log error for debugging (will be removed in production)
      }
    };

    loadAgents();
    dispatch(clearError());
  }, [dispatch, selectedAgent]);

  // Load chat history when agent is selected
  useEffect(() => {
    if (selectedAgent && chatState.sessionId) {
      const loadChatHistory = async () => {
        try {
          const history = await agentService.getChatHistory(chatState.sessionId);
          history.forEach((msg: ChatMessage) => {
            // Add user message
            dispatch(addMessage({
              id: `user-${msg.id}`,
              agent_id: msg.agent.toString(),
              user_id: msg.user.toString(),
              content: msg.message,
              type: 'text',
              timestamp: msg.created_at,
              is_read: true
            }));
            
            // Add agent response
            dispatch(addMessage({
              id: `agent-${msg.id}`,
              agent_id: msg.agent.toString(),
              user_id: msg.user.toString(),
              content: msg.response || 'No response',
              type: 'text',
              timestamp: msg.created_at,
              is_read: true
            }));
          });
        } catch (error) {
          // Error loading chat history (will be handled gracefully)
        }
      };

      loadChatHistory();
    }
  }, [selectedAgent, chatState.sessionId, dispatch]);

  // Mark messages as read when component is focused
  useEffect(() => {
    if (selectedAgent) {
      dispatch(markMessagesAsRead({ agentId: selectedAgent.id }));
    }
  }, [selectedAgent, dispatch]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!chatState.message.trim() || !selectedAgent || chatState.isLoading) {
      return;
    }

    const userMessage = chatState.message.trim();
    setChatState(prev => ({ ...prev, message: '', isLoading: true }));
    
    // Add user message to conversation immediately
    dispatch(addMessage({
      id: `user-${Date.now()}`,
      agent_id: selectedAgent.id,
      user_id: 'current-user',
      content: userMessage,
      type: 'text',
      timestamp: new Date().toISOString(),
      is_read: true
    }));

    // Set typing indicator
    dispatch(setTyping({ agentId: selectedAgent.id, isTyping: true }));

    try {
      // Send message to agent
      const response = await agentService.sendChatMessage(userMessage, chatState.sessionId);
      
      // Add agent response to conversation
      dispatch(addMessage({
        id: `agent-${response.id}`,
        agent_id: response.agent.toString(),
        user_id: response.user.toString(),
        content: response.response,
        type: 'text',
        timestamp: response.created_at,
        is_read: true
      }));

    } catch (error) {
      // Handle message sending error gracefully
      // Add error message
      dispatch(addMessage({
        id: `error-${Date.now()}`,
        agent_id: selectedAgent.id,
        user_id: 'current-user',
        content: 'Sorry, I encountered an error. Please try again.',
        type: 'text',
        timestamp: new Date().toISOString(),
        is_read: true
      }));
    } finally {
      setChatState(prev => ({ ...prev, isLoading: false }));
      dispatch(setTyping({ agentId: selectedAgent.id, isTyping: false }));
    }
  };

  const handleRateMessage = async (messageId: string, rating: number) => {
    try {
      await agentService.rateChatResponse(messageId, rating);
      // Show success feedback (could add toast notification here)
    } catch (error) {
      // Error rating response (silent failure acceptable)
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getAgentIcon = (agentType: string) => {
    switch (agentType) {
      case 'content_curator': return '📚';
      case 'quiz_master': return '❓';
      case 'evaluator': return '✅';
      case 'progress_tracker': return '📊';
      case 'motivator': return '💪';
      case 'orchestrator': return '🎯';
      default: return '🤖';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'busy': return 'warning';
      case 'inactive': return 'error';
      default: return 'info';
    }
  };

  // Available agents for chat
  const availableAgents = agents.filter(agent => 
    agent.status === 'active' || 
    agent.status === 'busy'
  );

  if (availableAgents.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <Card variant="glass" padding="lg" className="text-center">
            <div className="text-4xl mb-4">🤖</div>
            <h2 className="text-xl font-semibold text-white mb-2">No AI Agents Available</h2>
            <p className="text-white">
              AI agents are currently offline. Please check back later.
            </p>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white flex items-center space-x-3">
          <span>AI Chat Assistant</span>
          <Badge variant="info" glass={false}>
            {availableAgents.length} Agent{availableAgents.length !== 1 ? 's' : ''} Available
          </Badge>
        </h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-200px)]">
        {/* Agent Selection Sidebar */}
        <div className="lg:col-span-1">
          <Card variant="glass" padding="md" className="h-full">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
              <span>🤖</span>
              <span>Available Agents</span>
            </h3>
            
            <div className="space-y-2">
              {availableAgents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => dispatch(setSelectedAgent(agent.id))}
                  className={`w-full text-left p-3 rounded-lg transition-all duration-200 ${
                    selectedAgent?.id === agent.id
                      ? 'bg-white/20 border border-white/30'
                      : 'bg-white/5 border border-transparent hover:bg-white/10'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="text-xl">
                      {getAgentIcon(agent.type)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-white truncate">
                        {agent.name}
                      </div>
                      <div className="text-xs text-white/80 capitalize">
                        {agent.type.replace('_', ' ')}
                      </div>
                    </div>
                    <Badge 
                      variant={getStatusColor(agent.status)} 
                      size="sm" 
                      glass={false}
                    >
                      {agent.status}
                    </Badge>
                  </div>
                </button>
              ))}
            </div>

            {/* Agent Capabilities */}
            {selectedAgent && (
              <div className="mt-6 pt-6 border-t border-white/20">
                <h4 className="text-sm font-medium text-white mb-3">Capabilities</h4>
                <div className="flex flex-wrap gap-1">
                  {selectedAgent.capabilities?.map((capability, index) => (
                    <Badge key={index} variant="info" size="sm" glass={false}>
                      {capability}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </Card>
        </div>

        {/* Chat Interface */}
        <div className="lg:col-span-3">
          <Card variant="glass" padding="none" className="h-full flex flex-col">
            {/* Chat Header */}
            {selectedAgent && (
              <div className="p-4 border-b border-white/20">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="text-2xl">
                      {getAgentIcon(selectedAgent.type)}
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-white">
                        {selectedAgent.name}
                      </h3>
                      <p className="text-sm text-white/90 capitalize">
                        {selectedAgent.type.replace('_', ' ')}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Badge variant={getStatusColor(selectedAgent.status)} glass={false}>
                      {selectedAgent.status}
                    </Badge>
                  </div>
                </div>
              </div>
            )}

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              <AnimatePresence>
                {conversation.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-4xl mb-4">👋</div>
                    <h3 className="text-lg font-semibold text-white mb-2">
                      Start a conversation
                    </h3>
                    <p className="text-white">
                      Ask me anything about your learning journey, coding, or get personalized recommendations!
                    </p>
                  </div>
                ) : (
                  conversation.map((message, index) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.3 }}
                      className={`flex ${
                        message.user_id === 'current-user' 
                          ? 'justify-end' 
                          : 'justify-start'
                      }`}
                    >
                      <div className={`max-w-[80%] ${
                        message.user_id === 'current-user'
                          ? 'bg-primary-500/20 border-primary-400/30'
                          : 'bg-white/10 border-white/20'
                      } border rounded-2xl px-4 py-3`}>
                        <div className="text-white whitespace-pre-wrap">
                          {message.content}
                        </div>
                        <div className="flex items-center justify-between mt-2">
                          <span className="text-xs text-white/80">
                            {formatTime(message.timestamp)}
                          </span>
                          
                          {message.user_id !== 'current-user' && message.content.includes('?') && (
                            <div className="flex space-x-1">
                              <button
                                onClick={() => handleRateMessage(message.id, 1)}
                                className="text-xs text-success-400 hover:text-success-300"
                                title="Helpful"
                              >
                                👍
                              </button>
                              <button
                                onClick={() => handleRateMessage(message.id, -1)}
                                className="text-xs text-error-400 hover:text-error-300"
                                title="Not helpful"
                              >
                                👎
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))
                )}
                
                {/* Typing Indicator */}
                {typing && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="flex justify-start"
                  >
                    <div className="bg-white/10 border border-white/20 rounded-2xl px-4 py-3">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
              
              <div ref={messagesEndRef} />
            </div>

            {/* Message Input */}
            <div className="p-4 border-t border-white/20">
              <form onSubmit={handleSendMessage} className="flex space-x-3">
                <input
                  ref={inputRef}
                  type="text"
                  value={chatState.message}
                  onChange={(e) => setChatState(prev => ({ ...prev, message: e.target.value }))}
                  onKeyPress={handleKeyPress}
                  placeholder={
                    selectedAgent 
                      ? `Ask ${selectedAgent.name} anything...`
                      : 'Select an agent to start chatting...'
                  }
                  disabled={!selectedAgent || chatState.isLoading}
                  className="flex-1 glass rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent disabled:opacity-50"
                />
                <Button
                  type="submit"
                  variant="primary"
                  disabled={!selectedAgent || !chatState.message.trim() || chatState.isLoading}
                  isLoading={chatState.isLoading}
                >
                  Send
                </Button>
              </form>
              
              {/* Quick Suggestions */}
              <div className="mt-3 flex flex-wrap gap-2">
                {[
                  "Help me with my learning plan",
                  "Explain a concept I don't understand",
                  "Give me coding practice exercises",
                  "Track my progress"
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => setChatState(prev => ({ ...prev, message: suggestion }))}
                    className="text-xs px-3 py-1 bg-white/10 hover:bg-white/20 text-white hover:text-white rounded-full transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Chat;