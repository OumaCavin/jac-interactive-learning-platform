// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Quiz Master Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the Quiz Master AI Agent.
 * Focuses on quiz creation, knowledge testing, and interactive learning challenges.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import gamificationService from '../../services/gamificationService';

interface QuizMasterChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const QuizMasterChat: React.FC<QuizMasterChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    try {
      await gamificationService.awardPoints(10, 'quiz_master_interaction', {
        message_type: 'chat_interaction',
        agent_type: 'quiz_master'
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
      agentId="quiz_master"
      agentType="quiz_master"
      agentName="Quiz Master"
      agentIcon="❓"
      agentDescription="Ready to test your knowledge! I'll create engaging quizzes and challenges to help you learn and grow."
      agentCapabilities={[
        'Quiz Generation',
        'Knowledge Assessment',
        'Interactive Challenges',
        'Difficulty Adaptation',
        'Performance Analytics',
        'Concept Reinforcement',
        'Real-time Feedback',
        'Learning Gap Analysis'
      ]}
      agentColor="from-green-500 to-teal-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default QuizMasterChat;