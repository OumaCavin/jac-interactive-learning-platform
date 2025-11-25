/**
 * Progress Tracker Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the Progress Tracker AI Agent.
 * Focuses on analytics, progress monitoring, and learning insights.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import gamificationService from '../../services/gamificationService';

interface ProgressTrackerChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const ProgressTrackerChat: React.FC<ProgressTrackerChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    try {
      await gamificationService.awardPoints(10, 'progress_tracking', {
        message_type: 'chat_interaction',
        agent_type: 'progress_tracker'
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
      agentId="progress_tracker"
      agentType="progress_tracker"
      agentName="Progress Tracker"
      agentIcon="📊"
      agentDescription="I'll track your learning journey, analyze your progress patterns, and provide insights to optimize your learning experience."
      agentCapabilities={[
        'Progress Analytics',
        'Learning Pattern Analysis',
        'Time Efficiency Tracking',
        'Engagement Level Monitoring',
        'Skill Development Assessment',
        'Performance Trends',
        'Predictive Analytics',
        'Learning Velocity Optimization'
      ]}
      agentColor="from-purple-500 to-pink-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default ProgressTrackerChat;