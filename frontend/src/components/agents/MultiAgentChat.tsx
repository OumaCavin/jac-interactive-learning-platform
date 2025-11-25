/**
 * Multi-Agent Chat Interface - JAC Learning Platform
 * 
 * Comprehensive chat interface that allows users to interact with all 6 AI agents.
 * Features agent selection, real-time switching, and unified chat experience.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, Badge, Button, Tabs } from '../ui';
import {
  ContentCuratorChat,
  QuizMasterChat,
  EvaluatorChat,
  ProgressTrackerChat,
  MotivatorChat,
  SystemOrchestratorChat
} from './index';

interface AgentInfo {
  id: string;
  name: string;
  icon: string;
  description: string;
  color: string;
  component: React.ComponentType<any>;
  isActive: boolean;
}

interface MultiAgentChatProps {
  defaultAgent?: string;
  onAgentSwitch?: (agentId: string) => void;
  onMessageSent?: (agentId: string, message: string) => void;
  onResponseReceived?: (agentId: string, response: string) => void;
}

const MultiAgentChat: React.FC<MultiAgentChatProps> = ({
  defaultAgent = 'content_curator',
  onAgentSwitch,
  onMessageSent,
  onResponseReceived
}) => {
  const [activeAgent, setActiveAgent] = useState(defaultAgent);
  const [sessionId] = useState(() => `multi-agent-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  
  const agents: AgentInfo[] = [
    {
      id: 'content_curator',
      name: 'Content Curator',
      icon: '📚',
      description: 'Organize and optimize your learning content',
      color: 'from-blue-500 to-purple-600',
      component: ContentCuratorChat,
      isActive: true
    },
    {
      id: 'quiz_master',
      name: 'Quiz Master',
      icon: '❓',
      description: 'Create quizzes and test your knowledge',
      color: 'from-green-500 to-teal-600',
      component: QuizMasterChat,
      isActive: true
    },
    {
      id: 'evaluator',
      name: 'Evaluator',
      icon: '✅',
      description: 'Assess progress and provide feedback',
      color: 'from-orange-500 to-red-600',
      component: EvaluatorChat,
      isActive: true
    },
    {
      id: 'progress_tracker',
      name: 'Progress Tracker',
      icon: '📊',
      description: 'Track learning analytics and insights',
      color: 'from-purple-500 to-pink-600',
      component: ProgressTrackerChat,
      isActive: true
    },
    {
      id: 'motivator',
      name: 'Motivator',
      icon: '💪',
      description: 'Keep you motivated and on track',
      color: 'from-yellow-500 to-orange-600',
      component: MotivatorChat,
      isActive: true
    },
    {
      id: 'system_orchestrator',
      name: 'System Orchestrator',
      icon: '🎯',
      description: 'Coordinate your entire learning system',
      color: 'from-indigo-500 to-blue-600',
      component: SystemOrchestratorChat,
      isActive: true
    }
  ];
  
  const activeAgentInfo = agents.find(agent => agent.id === activeAgent) || agents[0];
  const ActiveComponent = activeAgentInfo.component;
  
  useEffect(() => {
    if (onAgentSwitch) {
      onAgentSwitch(activeAgent);
    }
  }, [activeAgent, onAgentSwitch]);
  
  const handleAgentSelect = (agentId: string) => {
    setActiveAgent(agentId);
  };
  
  const handleMessageSent = (message: string) => {
    if (onMessageSent) {
      onMessageSent(activeAgent, message);
    }
  };
  
  const handleResponseReceived = (response: string) => {
    if (onResponseReceived) {
      onResponseReceived(activeAgent, response);
    }
  };
  
  const getStatusColor = (isActive: boolean) => {
    return isActive ? 'success' : 'error';
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-3xl font-bold text-white mb-4 flex items-center justify-center space-x-3">
          <span>🤖</span>
          <span>AI Learning Assistants</span>
        </h1>
        <p className="text-white/80 max-w-2xl mx-auto">
          Chat with specialized AI agents to enhance your learning experience. Each agent has unique capabilities to help you succeed.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-200px)]">
        {/* Agent Selection Sidebar */}
        <div className="lg:col-span-1">
          <Card variant="glass" padding="md" className="h-full">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
              <span>🤖</span>
              <span>Available Agents</span>
              <Badge variant="info" size="sm">
                {agents.filter(a => a.isActive).length}
              </Badge>
            </h3>
            
            <div className="space-y-3">
              {agents.map((agent) => (
                <motion.button
                  key={agent.id}
                  onClick={() => handleAgentSelect(agent.id)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full text-left p-4 rounded-lg transition-all duration-300 ${
                    activeAgent === agent.id
                      ? 'bg-white/20 border border-white/30 shadow-lg'
                      : 'bg-white/5 border border-transparent hover:bg-white/10'
                  } ${!agent.isActive ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={!agent.isActive}
                >
                  <div className="flex items-start space-x-3">
                    <div className={`text-2xl p-2 rounded-full bg-gradient-to-r ${agent.color}`}>
                      {agent.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-white truncate">
                        {agent.name}
                      </div>
                      <div className="text-xs text-white/80 mt-1 line-clamp-2">
                        {agent.description}
                      </div>
                      <div className="flex items-center space-x-2 mt-2">
                        <Badge 
                          variant={getStatusColor(agent.isActive)} 
                          size="sm" 
                        >
                          {agent.isActive ? 'Active' : 'Offline'}
                        </Badge>
                        {activeAgent === agent.id && (
                          <Badge variant="info" size="sm">
                            Selected
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </motion.button>
              ))}
            </div>
            
            {/* Agent Capabilities */}
            {activeAgentInfo && (
              <div className="mt-6 pt-6 border-t border-white/20">
                <h4 className="text-sm font-medium text-white mb-3">Current Agent Capabilities</h4>
                <div className="text-xs text-white/70 space-y-1">
                  {activeAgentInfo.description}
                </div>
              </div>
            )}
          </Card>
        </div>

        {/* Chat Interface */}
        <div className="lg:col-span-3">
          <Card variant="glass" padding="none" className="h-full flex flex-col">
            {/* Active Agent Header */}
            <div className="p-4 border-b border-white/20 bg-gradient-to-r from-white/5 to-white/10">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`text-3xl p-3 rounded-full bg-gradient-to-r ${activeAgentInfo.color}`}>
                    {activeAgentInfo.icon}
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-white">
                      {activeAgentInfo.name}
                    </h2>
                    <p className="text-sm text-white/80">
                      {activeAgentInfo.description}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2">
                  <Badge 
                    variant={getStatusColor(activeAgentInfo.isActive)}
                    className="animate-pulse"
                  >
                    {activeAgentInfo.isActive ? 'Ready to Chat' : 'Currently Offline'}
                  </Badge>
                </div>
              </div>
            </div>

            {/* Agent Chat Component */}
            <div className="flex-1 overflow-hidden">
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeAgent}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="h-full"
                >
                  {activeAgentInfo.isActive ? (
                    <ActiveComponent
                      sessionId={sessionId}
                      onMessageSent={handleMessageSent}
                      onResponseReceived={handleResponseReceived}
                    />
                  ) : (
                    <div className="h-full flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-4xl mb-4">😴</div>
                        <h3 className="text-lg font-semibold text-white mb-2">
                          {activeAgentInfo.name} is Offline
                        </h3>
                        <p className="text-white/70">
                          This agent is currently unavailable. Please try again later or select another agent.
                        </p>
                      </div>
                    </div>
                  )}
                </motion.div>
              </AnimatePresence>
            </div>
          </Card>
        </div>
      </div>
      
      {/* Quick Actions */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-6 flex justify-center"
      >
        <Card variant="glass" padding="md" className="text-center">
          <h4 className="text-sm font-medium text-white mb-3">Quick Tips</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-white/70">
            <div>
              <span className="font-medium">💡 Ask specific questions</span><br/>
              Get better responses with clear requests
            </div>
            <div>
              <span className="font-medium">🔄 Switch agents easily</span><br/>
              Each agent has unique expertise
            </div>
            <div>
              <span className="font-medium">📈 Track your progress</span><br/>
              Your interactions help improve the system
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
};

export default MultiAgentChat;