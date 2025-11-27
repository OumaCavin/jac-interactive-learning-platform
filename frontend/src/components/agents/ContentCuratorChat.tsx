// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Content Curator Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the Content Curator AI Agent.
 * Focuses on content organization, learning path creation, and material recommendations.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import { webSocketService } from '../../services/websocketService';
import gamificationService from '../../services/gamificationService';

interface ContentCuratorChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const ContentCuratorChat: React.FC<ContentCuratorChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    // Trigger gamification for content curation activity
    try {
      await gamificationService.awardPoints(10, 'content_curation', {
        message_type: 'chat_interaction',
        agent_type: 'content_curator'
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
      agentId="content_curator"
      agentType="content_curator"
      agentName="Content Curator"
      agentIcon="📚"
      agentDescription="I'll help you organize, curate, and optimize your learning content for maximum engagement and effectiveness."
      agentCapabilities={[
        'Content Organization',
        'Learning Path Creation',
        'Material Recommendation',
        'Content Difficulty Analysis',
        'Personalized Curation',
        'Content Performance Tracking',
        'Adaptive Content Delivery',
        'Knowledge Gap Identification'
      ]}
      agentColor="from-blue-500 to-purple-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default ContentCuratorChat;