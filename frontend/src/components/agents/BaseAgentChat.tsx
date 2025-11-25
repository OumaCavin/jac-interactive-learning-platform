/**
 * Base Agent Chat Component - JAC Learning Platform
 * 
 * Reusable base component for individual agent chat interfaces.
 * Handles common chat functionality, WebSocket integration, and UI patterns.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button, Input, Badge } from '../ui';
import { webSocketService, WebSocketMessage } from '../../services/websocketService';
import gamificationService from '../../services/gamificationService';
import { useAppSelector } from '../../store/store';

interface ChatMessage {
  id: string;
  agent_id: string;
  user_id: string;
  content: string;
  type: 'text' | 'code' | 'image' | 'file';
  timestamp: string;
  is_read: boolean;
  metadata?: Record<string, any>;
}

interface BaseAgentChatProps {
  agentId: string;
  agentType: string;
  agentName: string;
  agentIcon: string;
  agentDescription: string;
  agentCapabilities: string[];
  agentColor: string;
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const BaseAgentChat: React.FC<BaseAgentChatProps> = ({
  agentId,
  agentType,
  agentName,
  agentIcon,
  agentDescription,
  agentCapabilities,
  agentColor,
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Generate session ID if not provided
  const actualSessionId = sessionId || `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  
  // Get agent state from store
  const agent = useAppSelector(state => 
    state.agents?.agents?.find(a => a.id === agentId)
  );
  
  const isAgentTyping = useAppSelector(state => 
    state.agents?.typing?.[agentId] || false
  );

  // Initialize WebSocket connection
  useEffect(() => {
    if (agentId && agentType) {
      // Connect to agent-specific room
      webSocketService.connectAgentChat(agentId, agentType, actualSessionId);
      setIsConnected(true);
      
      // Subscribe to agent events
      webSocketService.subscribeToAgent(agentId, 'message', handleAgentMessage);
      webSocketService.subscribeToAgent(agentId, 'typing', handleAgentTyping);
      webSocketService.subscribeToAgent(agentId, 'status', handleAgentStatus);
      
      return () => {
        webSocketService.leaveAgentChat(agentId, agentType, actualSessionId);
        webSocketService.unsubscribeFromAgent(agentId, 'message', handleAgentMessage);
        webSocketService.unsubscribeFromAgent(agentId, 'typing', handleAgentTyping);
        webSocketService.unsubscribeFromAgent(agentId, 'status', handleAgentStatus);
      };
    }
  }, [agentId, agentType, actualSessionId]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load chat history on component mount
  useEffect(() => {
    loadChatHistory();
  }, [agentId, actualSessionId]);

  const handleAgentMessage = (data: any) => {
    if (data.content && data.agent_id === agentId) {
      const newMessage: ChatMessage = {
        id: `agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        agent_id: data.agent_id,
        user_id: 'agent',
        content: data.content,
        type: 'text',
        timestamp: data.timestamp || new Date().toISOString(),
        is_read: true,
        metadata: data.metadata
      };
      
      setMessages(prev => [...prev, newMessage]);
      setIsTyping(false);
      
      if (onResponseReceived) {
        onResponseReceived(data.content);
      }
      
      // Trigger gamification for AI chat
      gamificationService.triggerAIChat(agentId, agentType).catch(console.warn);
    }
  };

  const handleAgentTyping = (data: any) => {
    if (data.agent_id === agentId) {
      setIsTyping(data.is_typing);
    }
  };

  const handleAgentStatus = (data: any) => {
    if (data.agent_id === agentId) {
      setIsConnected(data.status === 'active');
    }
  };

  const loadChatHistory = async () => {
    try {
      // This would be replaced with actual API call
      // const history = await agentService.getChatHistory(actualSessionId);
      // For now, add a welcome message
      const welcomeMessage: ChatMessage = {
        id: 'welcome',
        agent_id: agentId,
        user_id: 'agent',
        content: `Hello! I'm ${agentName}. ${agentDescription} How can I help you today?`,
        type: 'text',
        timestamp: new Date().toISOString(),
        is_read: true
      };
      
      setMessages([welcomeMessage]);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!currentMessage.trim() || isLoading || !isConnected) {
      return;
    }

    const messageContent = currentMessage.trim();
    setCurrentMessage('');
    setIsLoading(true);

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      agent_id: agentId,
      user_id: 'current-user',
      content: messageContent,
      type: 'text',
      timestamp: new Date().toISOString(),
      is_read: true
    };

    setMessages(prev => [...prev, userMessage]);
    
    // Show typing indicator
    setIsTyping(true);

    try {
      // Send message via WebSocket
      webSocketService.sendAgentMessage(agentId, agentType, messageContent, actualSessionId);
      
      if (onMessageSent) {
        onMessageSent(messageContent);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        agent_id: agentId,
        user_id: 'agent',
        content: 'Sorry, I encountered an error. Please try again.',
        type: 'text',
        timestamp: new Date().toISOString(),
        is_read: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(e);
    }
  };

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'busy': return 'warning';
      case 'inactive': return 'error';
      default: return 'info';
    }
  };

  const quickSuggestions = getQuickSuggestions(agentType);

  return (
    <div className="flex flex-col h-full bg-white/10 backdrop-blur-lg rounded-lg border border-white/20">
      {/* Agent Header */}
      <div className="p-4 border-b border-white/20">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`text-2xl p-2 rounded-full bg-gradient-to-r ${agentColor}`}>
              {agentIcon}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">
                {agentName}
              </h3>
              <p className="text-sm text-white/80 capitalize">
                {agentType.replace('_', ' ')}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Badge 
              variant={isConnected ? getStatusColor('active') : getStatusColor('inactive')}
              size="sm"
            >
              {isConnected ? 'Connected' : 'Offline'}
            </Badge>
            {isTyping && (
              <Badge variant="info" size="sm" animate>
                Typing...
              </Badge>
            )}
          </div>
        </div>
        
        {/* Agent Capabilities */}
        <div className="mt-3">
          <p className="text-xs text-white/60 mb-2">Capabilities:</p>
          <div className="flex flex-wrap gap-1">
            {agentCapabilities.map((capability, index) => (
              <Badge key={index} variant="info" size="sm">
                {capability}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
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
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Typing Indicator */}
        <AnimatePresence>
          {(isTyping || isAgentTyping) && (
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
        <form onSubmit={sendMessage} className="flex space-x-3">
          <input
            ref={inputRef}
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={`Ask ${agentName} anything...`}
            disabled={!isConnected || isLoading}
            className="flex-1 glass rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent disabled:opacity-50"
          />
          <Button
            type="submit"
            variant="primary"
            disabled={!isConnected || !currentMessage.trim() || isLoading}
            isLoading={isLoading}
          >
            Send
          </Button>
        </form>
        
        {/* Quick Suggestions */}
        {quickSuggestions.length > 0 && messages.length <= 1 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {quickSuggestions.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => setCurrentMessage(suggestion)}
                className="text-xs px-3 py-1 bg-white/10 hover:bg-white/20 text-white hover:text-white rounded-full transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Get quick suggestions based on agent type
const getQuickSuggestions = (agentType: string): string[] => {
  const suggestions: Record<string, string[]> = {
    'content_curator': [
      'Help me create a learning plan',
      'Recommend study materials',
      'Organize my content',
      'Suggest next topics'
    ],
    'quiz_master': [
      'Create a practice quiz',
      'Generate coding challenges',
      'Test my knowledge',
      'Explain difficult concepts'
    ],
    'evaluator': [
      'Assess my progress',
      'Review my code',
      'Check my understanding',
      'Provide feedback'
    ],
    'progress_tracker': [
      'Track my learning',
      'Show my statistics',
      'Analyze my performance',
      'Set learning goals'
    ],
    'motivator': [
      'Encourage me',
      'Set daily goals',
      'Remind me to practice',
      'Celebrate my progress'
    ],
    'system_orchestrator': [
      'Coordinate my learning',
      'Manage my schedule',
      'Optimize my path',
      'Coordinate agents'
    ]
  };
  
  return suggestions[agentType] || ['Ask me anything!', 'How can I help?', 'What would you like to know?'];
};

export default BaseAgentChat;