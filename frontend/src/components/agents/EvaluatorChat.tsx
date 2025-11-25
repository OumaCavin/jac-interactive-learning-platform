/**
 * Evaluator Agent Chat - JAC Learning Platform
 * 
 * Specialized chat interface for the Evaluator AI Agent.
 * Focuses on assessment, progress evaluation, and detailed feedback.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React from 'react';
import BaseAgentChat from './BaseAgentChat';
import gamificationService from '../../services/gamificationService';

interface EvaluatorChatProps {
  sessionId?: string;
  onMessageSent?: (message: string) => void;
  onResponseReceived?: (response: string) => void;
}

const EvaluatorChat: React.FC<EvaluatorChatProps> = ({
  sessionId,
  onMessageSent,
  onResponseReceived
}) => {
  const handleMessageSent = async (message: string) => {
    try {
      await gamificationService.awardPoints(10, 'evaluator_interaction', {
        message_type: 'chat_interaction',
        agent_type: 'evaluator'
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
      agentId="evaluator"
      agentType="evaluator"
      agentName="Evaluator"
      agentIcon="✅"
      agentDescription="I'll assess your progress, provide detailed feedback, and help you understand your strengths and areas for improvement."
      agentCapabilities={[
        'Progress Assessment',
        'Detailed Feedback',
        'Performance Analysis',
        'Skill Evaluation',
        'Knowledge Retention Testing',
        'Application Ability Assessment',
        'Coding Proficiency Evaluation',
        'Problem-Solving Analysis'
      ]}
      agentColor="from-orange-500 to-red-600"
      sessionId={sessionId}
      onMessageSent={handleMessageSent}
      onResponseReceived={handleResponseReceived}
    />
  );
};

export default EvaluatorChat;