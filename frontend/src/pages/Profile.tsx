import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { Card, Button, Badge, ProgressBar } from '../components/ui';
import { selectAuth, getUserStats } from '../store/slices/authSlice';
import { useAppDispatch } from '../store/store';
import type { User } from '../services/authService';

// TypeScript interfaces for Profile component
interface ProfileStats {
  totalModulesCompleted: number;
  totalTimeSpent: string;
  currentStreak: number;
  longestStreak: number;
  averageScore: number;
  totalPoints: number;
  level: number;
  achievements: number;
}

interface Achievement {
  title: string;
  description: string;
  icon?: string;
  earned_date?: string;
}

interface Badge {
  name?: string;
}

interface ProfileForm {
  firstName: string;
  lastName: string;
  email: string;
  bio: string;
}

const Profile: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user, isLoading } = useSelector(selectAuth);
  const [activeTab, setActiveTab] = useState<string>('overview');

  useEffect(() => {
    // Fetch latest user stats when profile loads
    if (user) {
      dispatch(getUserStats());
    }
  }, [dispatch, user]);

  if (!user) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white/80">Loading profile...</p>
          </div>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'achievements', label: 'Achievements', icon: '🏆' },
    { id: 'stats', label: 'Statistics', icon: '📈' },
    { id: 'preferences', label: 'Preferences', icon: '⚙️' },
  ];

  const getProgressToNextLevel = () => {
    if (user.level >= 100) return 100; // Max level
    const currentLevelExp = user.experience_level - (user.level * 100);
    const expNeededForNext = 100;
    return Math.min((currentLevelExp / expNeededForNext) * 100, 100);
  };

  const getProfileCompletion = () => {
    const fields = [
      user.first_name,
      user.last_name,
      user.email,
      user.bio,
      user.profile_image,
      user.learning_style,
      user.preferred_difficulty,
      user.current_goal,
    ];
    const completed = fields.filter(field => field && field.toString().trim() !== '').length;
    return (completed / fields.length) * 100;
  };

  const formatTimeSpent = (timeString: string) => {
    // Assuming timeString is in format "X hours Y minutes"
    return timeString || '0 hours';
  };

  const renderOverview = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      {/* Profile Header */}
      <div className="text-center mb-8">
        <div className="relative inline-block mb-4">
          {user.profile_image ? (
            <img
              src={user.profile_image}
              alt={`${user.first_name} ${user.last_name}`}
              className="w-24 h-24 rounded-full object-cover border-4 border-white/20"
            />
          ) : (
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 flex items-center justify-center text-3xl font-bold text-white border-4 border-white/20">
              {user.first_name?.charAt(0) || user.username?.charAt(0) || 'U'}
            </div>
          )}
          <div className="absolute -bottom-2 -right-2 bg-primary-500 text-white text-xs px-2 py-1 rounded-full font-bold">
            Level {user.level}
          </div>
        </div>
        
        <h2 className="text-2xl font-bold text-white mb-2">
          {user.first_name && user.last_name 
            ? `${user.first_name} ${user.last_name}`
            : user.username
          }
        </h2>
        
        <p className="text-white/70 mb-4">@{user.username}</p>
        
        {user.bio && (
          <p className="text-white/80 max-w-md mx-auto mb-4">{user.bio}</p>
        )}
        
        <div className="flex items-center justify-center space-x-4">
          <Badge variant="success" glass={false}>
            {user.total_points} Points
          </Badge>
          <Badge variant="info" glass={false}>
            {user.current_streak} Day Streak
          </Badge>
        </div>
      </div>

      {/* Progress to Next Level */}
      <Card variant="glass" padding="md">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-white">Level Progress</h3>
          <span className="text-sm text-white/70">
            {user.experience_level} / {user.next_level_points} XP
          </span>
        </div>
        <ProgressBar
          value={getProgressToNextLevel()}
          variant="primary"
          showLabel
          className="mb-2"
        />
        <p className="text-sm text-white/60">
          {user.level >= 100 
            ? '🎉 Maximum level reached!'
            : `${user.next_level_points - user.experience_level} XP to level ${user.level + 1}`
          }
        </p>
      </Card>

      {/* Profile Completion */}
      <Card variant="glass" padding="md">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-lg font-semibold text-white">Profile Completion</h3>
          <span className="text-sm text-white/70">{getProfileCompletion().toFixed(0)}%</span>
        </div>
        <ProgressBar
          value={getProfileCompletion()}
          variant={getProfileCompletion() === 100 ? 'success' : 'primary'}
          showLabel={false}
        />
        <p className="text-sm text-white/60 mt-2">
          {getProfileCompletion() === 100 
            ? '🎉 Profile complete! Great job!'
            : 'Complete your profile to unlock more features'
          }
        </p>
      </Card>

      {/* Current Goal */}
      {user.current_goal && (
        <Card variant="glass" padding="md">
          <h3 className="text-lg font-semibold text-white mb-3 flex items-center space-x-2">
            <span>🎯</span>
            <span>Current Goal</span>
          </h3>
          <p className="text-white/90 mb-2">{user.current_goal}</p>
          {user.goal_deadline && (
            <p className="text-sm text-white/60">
              Deadline: {new Date(user.goal_deadline).toLocaleDateString()}
            </p>
          )}
        </Card>
      )}

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card variant="glass" padding="sm" className="text-center">
          <div className="text-2xl font-bold text-white mb-1">
            {user.total_modules_completed}
          </div>
          <div className="text-xs text-white/70">Modules Completed</div>
        </Card>
        
        <Card variant="glass" padding="sm" className="text-center">
          <div className="text-2xl font-bold text-white mb-1">
            {formatTimeSpent(user.total_time_spent)}
          </div>
          <div className="text-xs text-white/70">Time Spent</div>
        </Card>
        
        <Card variant="glass" padding="sm" className="text-center">
          <div className="text-2xl font-bold text-white mb-1">
            {user.longest_streak}
          </div>
          <div className="text-xs text-white/70">Longest Streak</div>
        </Card>
        
        <Card variant="glass" padding="sm" className="text-center">
          <div className="text-2xl font-bold text-white mb-1">
            {user.achievements?.length || 0}
          </div>
          <div className="text-xs text-white/70">Achievements</div>
        </Card>
      </div>
    </motion.div>
  );

  const renderAchievements = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
        <span>🏆</span>
        <span>Achievements & Badges</span>
      </h3>

      {user.achievements && user.achievements.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {user.achievements.map((achievement: any, index: number) => (
            <Card key={index} variant="glass" padding="md" hover>
              <div className="flex items-center space-x-3">
                <div className="text-2xl">
                  {achievement.icon || '🏆'}
                </div>
                <div>
                  <h4 className="font-semibold text-white">{achievement.title}</h4>
                  <p className="text-sm text-white/70">{achievement.description}</p>
                  {achievement.earned_date && (
                    <p className="text-xs text-white/50">
                      Earned: {new Date(achievement.earned_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card variant="glass" padding="md" className="text-center">
          <p className="text-white/70">No achievements yet. Keep learning to earn your first badge!</p>
        </Card>
      )}

      {user.badges && user.badges.length > 0 && (
        <div>
          <h4 className="text-lg font-semibold text-white mb-3">Badges</h4>
          <div className="flex flex-wrap gap-2">
            {user.badges.map((badge: any, index: number) => (
              <Badge key={index} variant="primary" glass={false}>
                {badge.name || 'Badge'}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );

  const renderStats = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
        <span>📈</span>
        <span>Detailed Statistics</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Learning Metrics */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>📚</span>
            <span>Learning Metrics</span>
          </h4>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/80">Total Points</span>
              <span className="text-white font-semibold">{user.total_points}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-white/80">Current Level</span>
              <span className="text-white font-semibold">{user.level}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-white/80">Experience Level</span>
              <span className="text-white font-semibold">{user.experience_level}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-white/80">Modules Completed</span>
              <span className="text-white font-semibold">{user.total_modules_completed}</span>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-white/80">Total Time Spent</span>
              <span className="text-white font-semibold">{formatTimeSpent(user.total_time_spent)}</span>
            </div>
          </div>
        </Card>

        {/* Streak Information */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>🔥</span>
            <span>Streak Information</span>
          </h4>
          
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/80">Current Streak</span>
              <Badge variant="warning" glass={false}>
                {user.current_streak} days
              </Badge>
            </div>
            
            <div className="flex justify-between items-center">
              <span className="text-white/80">Longest Streak</span>
              <Badge variant="success" glass={false}>
                {user.longest_streak} days
              </Badge>
            </div>
            
            <div className="mt-4">
              <p className="text-sm text-white/70 mb-2">Streak Progress</p>
              <ProgressBar
                value={Math.min((user.current_streak / user.longest_streak) * 100, 100)}
                variant="warning"
                showLabel={false}
              />
            </div>
          </div>
        </Card>
      </div>

      {/* Activity Timeline */}
      <Card variant="glass" padding="md">
        <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
          <span>📅</span>
          <span>Account Activity</span>
        </h4>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-white/80">Member Since</span>
            <span className="text-white">
              {new Date(user.created_at).toLocaleDateString()}
            </span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="text-white/80">Last Updated</span>
            <span className="text-white">
              {new Date(user.updated_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      </Card>
    </motion.div>
  );

  const renderPreferences = () => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
        <span>⚙️</span>
        <span>Learning Preferences</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Learning Style */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>🧠</span>
            <span>Learning Style</span>
          </h4>
          <div className="text-center">
            <div className="text-3xl mb-2">
              {user.learning_style === 'visual' && '👁️'}
              {user.learning_style === 'auditory' && '👂'}
              {user.learning_style === 'kinesthetic' && '✋'}
              {user.learning_style === 'reading' && '📖'}
            </div>
            <p className="text-white font-medium capitalize">{user.learning_style}</p>
          </div>
        </Card>

        {/* Difficulty Level */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>🎚️</span>
            <span>Preferred Difficulty</span>
          </h4>
          <div className="text-center">
            <div className="text-3xl mb-2">
              {user.preferred_difficulty === 'beginner' && '🟢'}
              {user.preferred_difficulty === 'intermediate' && '🟡'}
              {user.preferred_difficulty === 'advanced' && '🔴'}
            </div>
            <p className="text-white font-medium capitalize">{user.preferred_difficulty}</p>
          </div>
        </Card>

        {/* Learning Pace */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>⏱️</span>
            <span>Learning Pace</span>
          </h4>
          <div className="text-center">
            <div className="text-3xl mb-2">
              {user.learning_pace === 'slow' && '🐌'}
              {user.learning_pace === 'moderate' && '🚶'}
              {user.learning_pace === 'fast' && '🏃'}
            </div>
            <p className="text-white font-medium capitalize">{user.learning_pace}</p>
          </div>
        </Card>

        {/* AI Agent Settings */}
        <Card variant="glass" padding="md">
          <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
            <span>🤖</span>
            <span>AI Agent Preferences</span>
          </h4>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-white/80">Interaction Level</span>
              <Badge variant="info" glass={false} className="capitalize">
                {user.agent_interaction_level}
              </Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/80">Feedback Style</span>
              <Badge variant="info" glass={false} className="capitalize">
                {user.preferred_feedback_style}
              </Badge>
            </div>
          </div>
        </Card>
      </div>

      {/* Notification Preferences */}
      <Card variant="glass" padding="md">
        <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
          <span>🔔</span>
          <span>Notification Preferences</span>
        </h4>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-white/80">Notifications Enabled</span>
            <Badge variant={user.notifications_enabled ? 'success' : 'error'} glass={false}>
              {user.notifications_enabled ? 'Enabled' : 'Disabled'}
            </Badge>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-white/80">Email Notifications</span>
            <Badge variant={user.email_notifications ? 'success' : 'error'} glass={false}>
              {user.email_notifications ? 'Enabled' : 'Disabled'}
            </Badge>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-white/80">Push Notifications</span>
            <Badge variant={user.push_notifications ? 'success' : 'error'} glass={false}>
              {user.push_notifications ? 'Enabled' : 'Disabled'}
            </Badge>
          </div>
        </div>
      </Card>

      {/* Display Preferences */}
      <Card variant="glass" padding="md">
        <h4 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
          <span>🎨</span>
          <span>Display Preferences</span>
        </h4>
        <div className="flex justify-between items-center">
          <span className="text-white/80">Dark Mode</span>
          <Badge variant={user.dark_mode ? 'success' : 'info'} glass={false}>
            {user.dark_mode ? 'Enabled' : 'Disabled'}
          </Badge>
        </div>
      </Card>
    </motion.div>
  );

  return (
    <div className="container mx-auto px-4 py-8" role="main" aria-label="User profile and settings">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-white">User Profile</h1>
        <Button
          variant="primary"
          size="sm"
          onClick={() => window.location.href = '/settings'}
        >
          Edit Settings
        </Button>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-8 bg-white/5 p-1 rounded-lg">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 rounded-lg transition-all duration-200 ${
              activeTab === tab.id
                ? 'bg-white/20 text-white shadow-lg'
                : 'text-white/70 hover:text-white hover:bg-white/10'
            }`}
          >
            <span>{tab.icon}</span>
            <span className="font-medium">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="min-h-[600px]">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'achievements' && renderAchievements()}
        {activeTab === 'stats' && renderStats()}
        {activeTab === 'preferences' && renderPreferences()}
      </div>
    </div>
  );
};

export default Profile;