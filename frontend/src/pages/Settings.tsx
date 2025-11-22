import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { Card, Button, Input, Badge } from '../components/ui';
import { updateProfile, selectAuth, clearError } from '../store/slices/authSlice';
import type { User } from '../services/authService';

interface SettingsFormData {
  // Personal Information
  first_name: string;
  last_name: string;
  email: string;
  bio: string;
  
  // Learning Preferences
  learning_style: User['learning_style'];
  preferred_difficulty: User['preferred_difficulty'];
  learning_pace: User['learning_pace'];
  
  // Goal Settings
  current_goal: string;
  goal_deadline: string;
  
  // Agent Settings
  agent_interaction_level: User['agent_interaction_level'];
  preferred_feedback_style: User['preferred_feedback_style'];
  
  // Notification Settings
  notifications_enabled: boolean;
  email_notifications: boolean;
  push_notifications: boolean;
  
  // Display Settings
  dark_mode: boolean;
}

const Settings: React.FC = () => {
  const dispatch = useDispatch();
  const { user, isLoading, error } = useSelector(selectAuth);
  
  const [formData, setFormData] = useState<SettingsFormData>({
    first_name: '',
    last_name: '',
    email: '',
    bio: '',
    learning_style: 'visual',
    preferred_difficulty: 'beginner',
    learning_pace: 'moderate',
    current_goal: '',
    goal_deadline: '',
    agent_interaction_level: 'moderate',
    preferred_feedback_style: 'detailed',
    notifications_enabled: true,
    email_notifications: true,
    push_notifications: true,
    dark_mode: true,
  });
  
  const [activeSection, setActiveSection] = useState<string>('profile');
  const [hasChanges, setHasChanges] = useState(false);

  // Load user data into form
  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        bio: user.bio || '',
        learning_style: user.learning_style || 'visual',
        preferred_difficulty: user.preferred_difficulty || 'beginner',
        learning_pace: user.learning_pace || 'moderate',
        current_goal: user.current_goal || '',
        goal_deadline: user.goal_deadline || '',
        agent_interaction_level: user.agent_interaction_level || 'moderate',
        preferred_feedback_style: user.preferred_feedback_style || 'detailed',
        notifications_enabled: user.notifications_enabled ?? true,
        email_notifications: user.email_notifications ?? true,
        push_notifications: user.push_notifications ?? true,
        dark_mode: user.dark_mode ?? true,
      });
    }
  }, [user]);

  // Clear error when component mounts
  useEffect(() => {
    dispatch(clearError());
  }, [dispatch]);

  // Check for changes
  useEffect(() => {
    if (user) {
      const isChanged = JSON.stringify(formData) !== JSON.stringify({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
        bio: user.bio || '',
        learning_style: user.learning_style || 'visual',
        preferred_difficulty: user.preferred_difficulty || 'beginner',
        learning_pace: user.learning_pace || 'moderate',
        current_goal: user.current_goal || '',
        goal_deadline: user.goal_deadline || '',
        agent_interaction_level: user.agent_interaction_level || 'moderate',
        preferred_feedback_style: user.preferred_feedback_style || 'detailed',
        notifications_enabled: user.notifications_enabled ?? true,
        email_notifications: user.email_notifications ?? true,
        push_notifications: user.push_notifications ?? true,
        dark_mode: user.dark_mode ?? true,
      });
      setHasChanges(isChanged);
    }
  }, [formData, user]);

  const handleInputChange = (field: keyof SettingsFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await dispatch(updateProfile(formData)).unwrap();
      setHasChanges(false);
    } catch (error) {
      console.error('Failed to update settings:', error);
    }
  };

  const settingsSections = [
    { id: 'profile', label: 'Profile Information', icon: '👤' },
    { id: 'learning', label: 'Learning Preferences', icon: '🧠' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'display', label: 'Display & Appearance', icon: '🎨' },
    { id: 'goals', label: 'Goals & Motivation', icon: '🎯' },
    { id: 'agent', label: 'AI Agent Settings', icon: '🤖' },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white">Settings</h1>
        {hasChanges && (
          <Badge variant="warning" glass={false}>
            Unsaved Changes
          </Badge>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Settings Navigation */}
        <div className="lg:col-span-1">
          <Card variant="glass" padding="md">
            <nav className="space-y-2">
              {settingsSections.map((section) => (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-all duration-200 ${
                    activeSection === section.id
                      ? 'bg-white/20 text-white'
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  }`}
                >
                  <span className="text-lg">{section.icon}</span>
                  <span className="text-sm font-medium">{section.label}</span>
                </button>
              ))}
            </nav>
          </Card>
        </div>

        {/* Settings Content */}
        <div className="lg:col-span-3">
          <form onSubmit={handleSubmit}>
            <Card variant="glass" padding="lg">
              {/* Profile Information Section */}
              {activeSection === 'profile' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>👤</span>
                    <span>Profile Information</span>
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <Input
                      label="First Name"
                      value={formData.first_name}
                      onChange={(e) => handleInputChange('first_name', e.target.value)}
                      placeholder="Enter your first name"
                    />
                    <Input
                      label="Last Name"
                      value={formData.last_name}
                      onChange={(e) => handleInputChange('last_name', e.target.value)}
                      placeholder="Enter your last name"
                    />
                  </div>
                  
                  <Input
                    label="Email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    placeholder="Enter your email"
                  />
                  
                  <div>
                    <label className="block text-sm font-medium text-white mb-2">
                      Bio
                    </label>
                    <textarea
                      value={formData.bio}
                      onChange={(e) => handleInputChange('bio', e.target.value)}
                      placeholder="Tell us about yourself..."
                      rows={4}
                      className="glass rounded-xl px-4 py-3 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent w-full resize-none"
                    />
                  </div>
                </motion.div>
              )}

              {/* Learning Preferences Section */}
              {activeSection === 'learning' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>🧠</span>
                    <span>Learning Preferences</span>
                  </h2>
                  
                  <div>
                    <label className="block text-sm font-medium text-white mb-3">
                      Learning Style
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      {(['visual', 'auditory', 'kinesthetic', 'reading'] as const).map((style) => (
                        <button
                          key={style}
                          type="button"
                          onClick={() => handleInputChange('learning_style', style)}
                          className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                            formData.learning_style === style
                              ? 'border-primary-400 bg-primary-500/20 text-white'
                              : 'border-white/20 text-white/70 hover:border-white/40 hover:text-white'
                          }`}
                        >
                          <div className="text-lg mb-1">
                            {style === 'visual' && '👁️'}
                            {style === 'auditory' && '👂'}
                            {style === 'kinesthetic' && '✋'}
                            {style === 'reading' && '📖'}
                          </div>
                          <div className="text-sm font-medium capitalize">{style}</div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-white mb-3">
                        Preferred Difficulty
                      </label>
                      <div className="space-y-2">
                        {(['beginner', 'intermediate', 'advanced'] as const).map((difficulty) => (
                          <button
                            key={difficulty}
                            type="button"
                            onClick={() => handleInputChange('preferred_difficulty', difficulty)}
                            className={`w-full p-2 rounded-lg border text-left transition-all duration-200 ${
                              formData.preferred_difficulty === difficulty
                                ? 'border-primary-400 bg-primary-500/20 text-white'
                                : 'border-white/20 text-white/70 hover:border-white/40 hover:text-white'
                            }`}
                          >
                            <span className="font-medium capitalize">{difficulty}</span>
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-3">
                        Learning Pace
                      </label>
                      <div className="space-y-2">
                        {(['slow', 'moderate', 'fast'] as const).map((pace) => (
                          <button
                            key={pace}
                            type="button"
                            onClick={() => handleInputChange('learning_pace', pace)}
                            className={`w-full p-2 rounded-lg border text-left transition-all duration-200 ${
                              formData.learning_pace === pace
                                ? 'border-primary-400 bg-primary-500/20 text-white'
                                : 'border-white/20 text-white/70 hover:border-white/40 hover:text-white'
                            }`}
                          >
                            <span className="font-medium capitalize">{pace}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Notifications Section */}
              {activeSection === 'notifications' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>🔔</span>
                    <span>Notification Settings</span>
                  </h2>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 rounded-lg border border-white/20">
                      <div>
                        <h3 className="font-medium text-white">Enable Notifications</h3>
                        <p className="text-sm text-white/70">Receive all types of notifications</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleInputChange('notifications_enabled', !formData.notifications_enabled)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          formData.notifications_enabled ? 'bg-primary-500' : 'bg-white/20'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            formData.notifications_enabled ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 rounded-lg border border-white/20">
                      <div>
                        <h3 className="font-medium text-white">Email Notifications</h3>
                        <p className="text-sm text-white/70">Receive notifications via email</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleInputChange('email_notifications', !formData.email_notifications)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          formData.email_notifications ? 'bg-primary-500' : 'bg-white/20'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            formData.email_notifications ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>

                    <div className="flex items-center justify-between p-4 rounded-lg border border-white/20">
                      <div>
                        <h3 className="font-medium text-white">Push Notifications</h3>
                        <p className="text-sm text-white/70">Receive push notifications in browser</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => handleInputChange('push_notifications', !formData.push_notifications)}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                          formData.push_notifications ? 'bg-primary-500' : 'bg-white/20'
                        }`}
                      >
                        <span
                          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                            formData.push_notifications ? 'translate-x-6' : 'translate-x-1'
                          }`}
                        />
                      </button>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Display & Appearance Section */}
              {activeSection === 'display' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>🎨</span>
                    <span>Display & Appearance</span>
                  </h2>
                  
                  <div className="flex items-center justify-between p-4 rounded-lg border border-white/20">
                    <div>
                      <h3 className="font-medium text-white">Dark Mode</h3>
                      <p className="text-sm text-white/70">Use dark theme throughout the application</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleInputChange('dark_mode', !formData.dark_mode)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        formData.dark_mode ? 'bg-primary-500' : 'bg-white/20'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          formData.dark_mode ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Goals Section */}
              {activeSection === 'goals' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>🎯</span>
                    <span>Goals & Motivation</span>
                  </h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Current Goal
                      </label>
                      <Input
                        value={formData.current_goal}
                        onChange={(e) => handleInputChange('current_goal', e.target.value)}
                        placeholder="What do you want to achieve?"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Goal Deadline
                      </label>
                      <Input
                        type="date"
                        value={formData.goal_deadline}
                        onChange={(e) => handleInputChange('goal_deadline', e.target.value)}
                      />
                    </div>
                  </div>
                </motion.div>
              )}

              {/* AI Agent Settings Section */}
              {activeSection === 'agent' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-6"
                >
                  <h2 className="text-xl font-semibold text-white flex items-center space-x-2">
                    <span>🤖</span>
                    <span>AI Agent Settings</span>
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-white mb-3">
                        Interaction Level
                      </label>
                      <div className="space-y-2">
                        {(['minimal', 'moderate', 'high'] as const).map((level) => (
                          <button
                            key={level}
                            type="button"
                            onClick={() => handleInputChange('agent_interaction_level', level)}
                            className={`w-full p-3 rounded-lg border text-left transition-all duration-200 ${
                              formData.agent_interaction_level === level
                                ? 'border-primary-400 bg-primary-500/20 text-white'
                                : 'border-white/20 text-white/70 hover:border-white/40 hover:text-white'
                            }`}
                          >
                            <span className="font-medium capitalize">{level}</span>
                            <p className="text-xs text-white/60 mt-1">
                              {level === 'minimal' && 'AI will provide minimal guidance'}
                              {level === 'moderate' && 'AI will provide balanced assistance'}
                              {level === 'high' && 'AI will be very interactive and helpful'}
                            </p>
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-3">
                        Feedback Style
                      </label>
                      <div className="space-y-2">
                        {(['detailed', 'brief', 'encouraging'] as const).map((style) => (
                          <button
                            key={style}
                            type="button"
                            onClick={() => handleInputChange('preferred_feedback_style', style)}
                            className={`w-full p-3 rounded-lg border text-left transition-all duration-200 ${
                              formData.preferred_feedback_style === style
                                ? 'border-primary-400 bg-primary-500/20 text-white'
                                : 'border-white/20 text-white/70 hover:border-white/40 hover:text-white'
                            }`}
                          >
                            <span className="font-medium capitalize">{style}</span>
                            <p className="text-xs text-white/60 mt-1">
                              {style === 'detailed' && 'Receive comprehensive explanations'}
                              {style === 'brief' && 'Get concise, to-the-point feedback'}
                              {style === 'encouraging' && 'Receive supportive and motivational feedback'}
                            </p>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Form Actions */}
              <div className="flex items-center justify-between pt-6 border-t border-white/20">
                {error && (
                  <p className="text-sm text-error-400">{error}</p>
                )}
                
                <div className="flex space-x-3">
                  <Button
                    type="button"
                    variant="ghost"
                    onClick={() => {
                      if (user) {
                        setFormData({
                          first_name: user.first_name || '',
                          last_name: user.last_name || '',
                          email: user.email || '',
                          bio: user.bio || '',
                          learning_style: user.learning_style || 'visual',
                          preferred_difficulty: user.preferred_difficulty || 'beginner',
                          learning_pace: user.learning_pace || 'moderate',
                          current_goal: user.current_goal || '',
                          goal_deadline: user.goal_deadline || '',
                          agent_interaction_level: user.agent_interaction_level || 'moderate',
                          preferred_feedback_style: user.preferred_feedback_style || 'detailed',
                          notifications_enabled: user.notifications_enabled ?? true,
                          email_notifications: user.email_notifications ?? true,
                          push_notifications: user.push_notifications ?? true,
                          dark_mode: user.dark_mode ?? true,
                        });
                      }
                    }}
                    disabled={isLoading || !hasChanges}
                  >
                    Reset Changes
                  </Button>
                  
                  <Button
                    type="submit"
                    variant="primary"
                    isLoading={isLoading}
                    disabled={!hasChanges}
                  >
                    Save Settings
                  </Button>
                </div>
              </div>
            </Card>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Settings;