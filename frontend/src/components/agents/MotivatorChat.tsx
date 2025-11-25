/**
 * Motivator Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the Motivator AI Agent.
 * Focuses on encouragement, goal setting, and maintaining learning momentum.
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import gamificationService from '../../services/gamificationService';

interface MotivatorChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const MotivatorChat: React.FC<MotivatorChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    try {
      await gamificationService.awardPoints(10, 'motivation_interaction', {
        message_type: 'chat_interaction',
        agent_type: 'motivator'
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
      agentId="motivator"
      agentType="motivator"
      agentName="Motivator"
      agentIcon="💪"
      agentDescription="Your personal learning cheerleader! I'll keep you motivated, set achievable goals, and celebrate your successes."
      agentCapabilities={[
        'Personal Motivation',
        'Goal Setting & Tracking',
        'Achievement Celebration',
        'Learning Streak Maintenance',
        'Confidence Building',
        'Mindset Coaching',
        'Positive Reinforcement',
        'Challenge Adaptation'
      ]}
      agentColor="from-yellow-500 to-orange-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default MotivatorChat;