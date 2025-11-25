/**
 * System Orchestrator Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the System Orchestrator AI Agent.
 * Focuses on coordination, optimization, and system-wide learning management.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import gamificationService from '../../services/gamificationService';

interface SystemOrchestratorChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const SystemOrchestratorChat: React.FC<SystemOrchestratorChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    try {
      await gamificationService.awardPoints(10, 'system_orchestration', {
        message_type: 'chat_interaction',
        agent_type: 'system_orchestrator'
      });
    } catch (error) {
      console.warn('Failed to trigger gamification:', error);
    }
    
    if (onMessageSent) {
      onMessageSent(message);
    }
  };

  const handleResponseReceived = (response: string) => {
    if (onResponseReceived) {
      onResponseReceived(response);
    }
  };

  return (
    <BaseAgentChat
      agentId="system_orchestrator"
      agentType="system_orchestrator"
      agentName="System Orchestrator"
      agentIcon="🎯"
      agentDescription="I coordinate all learning activities, optimize your entire learning journey, and ensure all agents work together seamlessly for your success."
      agentCapabilities={[
        'Learning Coordination',
        'System Optimization',
        'Multi-Agent Orchestration',
        'Resource Allocation',
        'Workflow Management',
        'Learning Path Optimization',
        'Agent Communication',
        'Performance Monitoring'
      ]}
      agentColor="from-indigo-500 to-blue-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default SystemOrchestratorChat;