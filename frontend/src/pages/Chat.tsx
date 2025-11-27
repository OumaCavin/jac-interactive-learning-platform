// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React from 'react';
import { motion } from 'framer-motion';
import { MultiAgentChat } from '../components/agents';
import gamificationService from '../services/gamificationService';

interface ChatProps {
  // Props for customization if needed
}

const Chat: React.FC<ChatProps> = () => {
  const handleAgentSwitch = async (agentId: string) => {
    try {
      // Track agent switching for gamification
      await gamificationService.awardPoints(5, 'agent_switch', {
        agent_id: agentId,
        action: 'switch_agent'
      });
    } catch (error) {
      console.warn('Failed to trigger gamification for agent switch:', error);
    }
  };

  const handleMessageSent = async (agentId: string, message: string) => {
    try {
      // Track message sending for gamification
      await gamificationService.awardPoints(2, 'message_sent', {
        agent_id: agentId,
        message_length: message.length,
        action: 'send_message'
      });
    } catch (error) {
      console.warn('Failed to trigger gamification for message sent:', error);
    }
  };

  const handleResponseReceived = async (agentId: string, response: string) => {
    try {
      // Track response received for gamification
      await gamificationService.awardPoints(3, 'response_received', {
        agent_id: agentId,
        response_length: response.length,
        action: 'receive_response'
      });
    } catch (error) {
      console.warn('Failed to trigger gamification for response received:', error);
    }
  };


  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <MultiAgentChat
        defaultAgent="content_curator"
        onAgentSwitch={handleAgentSwitch}
        onMessageSent={handleMessageSent}
        onResponseReceived={handleResponseReceived}
      />
    </motion.div>
  );
};

export default Chat;