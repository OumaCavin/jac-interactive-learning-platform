// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useSelector } from 'react-redux';
import { Card, Badge, Tabs, LoadingSpinner } from '../components/ui';
import { 
  GamificationOverview,
  Achievement, 
  UserAchievement, 
  Badge as BadgeType, 
  UserBadge,
  UserPoints,
  UserLevel,
  LearningStreak
} from '../services/gamificationService';
import gamificationService from '../services/gamificationService';
import { authService } from '../services/authService';

// Achievement and Badge types are imported from gamificationService
// Local interfaces for UI state
interface AchievementWithProgress extends Achievement {
  unlocked: boolean;
  unlockedAt?: string;
  progress?: number;
  target?: number;
  user_achievement?: UserAchievement;
}

const categories = [
  { id: 'all', label: 'All Achievements', icon: '🏆' },
  { id: 'learning', label: 'Learning', icon: '📚' },
  { id: 'coding', label: 'Coding', icon: '💻' },
  { id: 'streak', label: 'Streaks', icon: '🔥' },
  { id: 'special', label: 'Special', icon: '✨' },
  { id: 'milestone', label: 'Milestones', icon: '🎯' }
];

const difficulties = [
  { id: 'all', label: 'All Levels', color: 'bg-gradient-to-r from-blue-500 to-purple-500' },
  { id: 'bronze', label: 'Bronze', color: 'bg-gradient-to-r from-orange-400 to-orange-600' },
  { id: 'silver', label: 'Silver', color: 'bg-gradient-to-r from-gray-300 to-gray-500' },
  { id: 'gold', label: 'Gold', color: 'bg-gradient-to-r from-yellow-400 to-yellow-600' },
  { id: 'platinum', label: 'Platinum', color: 'bg-gradient-to-r from-purple-400 to-pink-500' }
];

const rarities = {
  common: { color: 'text-gray-400', label: 'Common' },
  rare: { color: 'text-blue-400', label: 'Rare' },
  epic: { color: 'text-purple-400', label: 'Epic' },
  legendary: { color: 'text-yellow-400', label: 'Legendary' }
};

const Achievements: React.FC = () => {
  // State management
  const [overview, setOverview] = useState<GamificationOverview | null>(null);
  const [achievements, setAchievements] = useState<AchievementWithProgress[]>([]);
  const [badges, setBadges] = useState<UserBadge[]>([]);
  const [allBadges, setAllBadges] = useState<BadgeType[]>([]);
  const [userPoints, setUserPoints] = useState<UserPoints | null>(null);
  const [userLevel, setUserLevel] = useState<UserLevel | null>(null);
  const [streak, setStreak] = useState<LearningStreak | null>(null);
  
  // UI state
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeDifficulty, setActiveDifficulty] = useState('all');
  const [showUnlockedOnly, setShowUnlockedOnly] = useState(false);
  const [selectedAchievement, setSelectedAchievement] = useState<AchievementWithProgress | null>(null);
  const [viewMode, setViewMode] = useState<'achievements' | 'badges'>('achievements');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const user = useSelector((state: any) => state.auth.user) || authService.getCurrentUser();

  // Load gamification data on component mount
  useEffect(() => {
    loadGamificationData();
  }, []);

  // Load all gamification data from API
  const loadGamificationData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Load overview data
      const overviewData = await gamificationService.getGamificationOverview();
      setOverview(overviewData);
      
      // Load achievements
      const achievementsData = await gamificationService.getUserAchievements();
      setAchievements(formatAchievements(achievementsData));
      
      // Load badges
      const userBadgesData = await gamificationService.getUserBadges();
      setBadges(userBadgesData);
      
      const allBadgesData = await gamificationService.getBadges();
      setAllBadges(allBadgesData);
      
      // Load user stats
      const pointsData = await gamificationService.getUserPoints();
      setUserPoints(pointsData);
      
      const levelData = await gamificationService.getUserLevel();
      setUserLevel(levelData);
      
      const streakData = await gamificationService.getLearningStreak();
      setStreak(streakData);
      
    } catch (err) {
      console.error('Failed to load gamification data:', err);
      setError('Failed to load achievements and badges. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Format achievements with progress data
  const formatAchievements = (userAchievements: UserAchievement[]): AchievementWithProgress[] => {
    return userAchievements.map(userAchievement => ({
      ...userAchievement.achievement,
      unlocked: userAchievement.is_completed,
      unlockedAt: userAchievement.completed_at,
      progress: userAchievement.current_progress,
      target: userAchievement.target_progress,
      user_achievement: userAchievement
    }));
  };

  // Filter achievements based on current filters
  const filteredAchievements = achievements.filter(achievement => {
    const categoryMatch = activeCategory === 'all' || achievement.category === activeCategory;
    const difficultyMatch = activeDifficulty === 'all' || achievement.difficulty === activeDifficulty;
    const unlockedMatch = !showUnlockedOnly || achievement.unlocked;
    
    return categoryMatch && difficultyMatch && unlockedMatch;
  });

  // Calculate statistics
  const stats = overview ? {
    total: achievements.length,
    unlocked: achievements.filter(a => a.unlocked).length,
    totalPoints: overview.total_points,
    byCategory: {
      learning: achievements.filter(a => a.category === 'learning' && a.unlocked).length,
      coding: achievements.filter(a => a.category === 'coding' && a.unlocked).length,
      streak: achievements.filter(a => a.category === 'streak' && a.unlocked).length,
      special: achievements.filter(a => a.category === 'special' && a.unlocked).length,
      milestone: achievements.filter(a => a.category === 'milestone' && a.unlocked).length
    },
    byDifficulty: {
      bronze: achievements.filter(a => a.difficulty === 'bronze' && a.unlocked).length,
      silver: achievements.filter(a => a.difficulty === 'silver' && a.unlocked).length,
      gold: achievements.filter(a => a.difficulty === 'gold' && a.unlocked).length,
      platinum: achievements.filter(a => a.difficulty === 'platinum' && a.unlocked).length
    }
  } : {
    total: 0,
    unlocked: 0,
    totalPoints: 0,
    byCategory: { learning: 0, coding: 0, streak: 0, special: 0, milestone: 0 },
    byDifficulty: { bronze: 0, silver: 0, gold: 0, platinum: 0 }
  };

  const completionPercentage = stats.total > 0 ? Math.round((stats.unlocked / stats.total) * 100) : 0;

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'bronze': return 'from-orange-400 to-orange-600';
      case 'silver': return 'from-gray-300 to-gray-500';
      case 'gold': return 'from-yellow-400 to-yellow-600';
      case 'platinum': return 'from-purple-400 to-pink-500';
      default: return 'from-gray-400 to-gray-600';
    }
  };

  const getRarityGradient = (rarity: string) => {
    switch (rarity) {
      case 'common': return 'from-gray-600/50 to-gray-800/50';
      case 'rare': return 'from-blue-600/50 to-blue-800/50';
      case 'epic': return 'from-purple-600/50 to-purple-800/50';
      case 'legendary': return 'from-yellow-600/50 to-yellow-800/50';
      default: return 'from-gray-600/50 to-gray-800/50';
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <Card variant="glass" padding="lg" className="text-center">
            <LoadingSpinner size="lg" />
            <h2 className="text-xl font-semibold text-white mt-4">
              Loading Achievements...
            </h2>
            <p className="text-white/80">
              Fetching your gamification data
            </p>
          </Card>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <Card variant="glass" padding="lg" className="text-center">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-white mb-2">
              Unable to Load Achievements
            </h2>
            <p className="text-white/80 mb-4">
              {error}
            </p>
            <button
              onClick={loadGamificationData}
              className="px-6 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-lg transition-colors"
            >
              Try Again
            </button>
          </Card>
        </div>
      </div>
    );
  }

  const renderAchievementCard = (achievement: AchievementWithProgress) => (
    <motion.div
      key={achievement.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className={`bg-white/10 backdrop-blur-lg rounded-lg p-6 cursor-pointer transition-all duration-300 ${
        achievement.unlocked ? 'border border-white/20' : 'border border-white/10 opacity-75'
      } ${achievement.unlocked ? 'hover:bg-white/20' : ''}`}
      onClick={() => setSelectedAchievement(achievement)}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`text-4xl p-3 rounded-full bg-gradient-to-r ${getDifficultyColor(achievement.difficulty)} ${
            achievement.unlocked ? '' : 'grayscale'
          }`}>
            {achievement.icon}
          </div>
          <div>
            <h3 className={`text-lg font-semibold ${achievement.unlocked ? 'text-gray-900' : 'text-gray-700'}`}>
              {achievement.title}
            </h3>
            <p className={`text-sm ${achievement.unlocked ? 'text-gray-700' : 'text-gray-500'}`}>
              {achievement.description}
            </p>
          </div>
        </div>
        <div className="flex flex-col items-end space-y-2">
          <span className={`text-xs px-2 py-1 rounded-full bg-gradient-to-r ${getDifficultyColor(achievement.difficulty)} text-white font-medium`}>
            {achievement.difficulty.toUpperCase()}
          </span>
          <span className={`text-xs px-2 py-1 rounded-full ${achievement.rarity ? rarities[achievement.rarity].color : 'text-gray-400'} font-medium`}>
            {achievement.rarity || 'common'}
          </span>
        </div>
      </div>

      {achievement.unlocked ? (
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-yellow-400 font-bold">{achievement.points_reward || 0}</span>
            <span className="text-white/60 text-sm">points</span>
          </div>
          {achievement.unlockedAt && (
            <span className="text-white/60 text-sm">
              Unlocked {formatDate(achievement.unlockedAt)}
            </span>
          )}
        </div>
      ) : (
        <div className="space-y-2">
          {achievement.progress !== undefined && achievement.target && (
            <div>
              <div className="flex justify-between text-sm text-white/80 mb-1">
                <span>Progress</span>
                <span>{achievement.progress} / {achievement.target}</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getDifficultyColor(achievement.difficulty)}`}
                  style={{ width: `${(achievement.progress / achievement.target) * 100}%` }}
                ></div>
              </div>
            </div>
          )}
          <div className="flex justify-between items-center">
            <span className="text-white/60 text-sm">{achievement.points_reward || 0} points</span>
            <span className="text-white/50 text-sm">Locked</span>
          </div>
        </div>
      )}

      <div className="mt-3 pt-3 border-t border-white/10">
        <p className="text-xs text-white/60">
          <strong>Requirements:</strong> {achievement.criteria_type.replace('_', ' ')} {achievement.criteria_value}
        </p>
      </div>
    </motion.div>
  );

  const renderBadge = (userBadge: UserBadge) => (
    <motion.div
      key={userBadge.id}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05 }}
      className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center transition-all duration-300 border border-white/20"
    >
      <div className="text-4xl mb-3">
        {userBadge.badge.icon}
      </div>
      <h3 className="font-semibold mb-2 text-white">
        {userBadge.badge.name}
      </h3>
      <p className="text-sm mb-3 text-white/80">
        {userBadge.badge.description}
      </p>
      <div className="flex flex-col items-center space-y-2">
        <span className={`text-xs px-3 py-1 rounded-full ${
          userBadge.badge.difficulty === 'bronze' ? 'bg-orange-500/20 text-orange-300' :
          userBadge.badge.difficulty === 'silver' ? 'bg-gray-500/20 text-gray-300' :
          userBadge.badge.difficulty === 'gold' ? 'bg-yellow-500/20 text-yellow-300' :
          'bg-purple-500/20 text-purple-300'
        }`}>
          {userBadge.badge.difficulty}
        </span>
        {userBadge.earnedAt && (
          <span className="text-xs text-white/60">
            Earned {formatDate(userBadge.earnedAt)}
          </span>
        )}
      </div>
    </motion.div>
  );

  const renderStatsOverview = () => (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/10 backdrop-blur-lg rounded-lg p-4 text-center"
      >
        <div className="text-2xl font-bold text-gray-900 mb-1">{stats.unlocked}</div>
        <div className="text-sm text-gray-700">Unlocked</div>
      </motion.div>
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white/10 backdrop-blur-lg rounded-lg p-4 text-center"
      >
        <div className="text-2xl font-bold text-gray-900 mb-1">{stats.totalPoints}</div>
        <div className="text-sm text-gray-700">Total Points</div>
      </motion.div>
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white/10 backdrop-blur-lg rounded-lg p-4 text-center"
      >
        <div className="text-2xl font-bold text-green-400 mb-1">{completionPercentage}%</div>
        <div className="text-sm text-gray-700">Completed</div>
      </motion.div>
      
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white/10 backdrop-blur-lg rounded-lg p-4 text-center"
      >
        <div className="text-2xl font-bold text-purple-400 mb-1">{stats.byDifficulty.gold + stats.byDifficulty.platinum}</div>
        <div className="text-sm text-gray-700">Rare+</div>
      </motion.div>
    </div>
  );

  const renderCategoryProgress = () => (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 mb-8">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress by Category</h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        {Object.entries(stats.byCategory).map(([category, count]) => (
          <div key={category} className="text-center">
            <div className="text-xl mb-2">
              {category === 'learning' ? '📚' :
               category === 'coding' ? '💻' :
               category === 'streak' ? '🔥' :
               category === 'special' ? '✨' :
               category === 'milestone' ? '🎯' : '🏆'}
            </div>
            <div className="text-lg font-bold text-gray-900">{count}</div>
            <div className="text-sm text-gray-700 capitalize">{category}</div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8" role="main" aria-label="Achievements and Badges dashboard">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Achievements & Badges</h1>
        <p className="text-gray-700 max-w-2xl mx-auto">
          Track your learning progress and unlock achievements as you advance through your JAC journey
        </p>
      </motion.div>

      {/* Stats Overview */}
      {renderStatsOverview()}

      {/* Category Progress */}
      {renderCategoryProgress()}

      {/* View Toggle */}
      <div className="flex justify-center mb-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-1">
          <button
            onClick={() => setViewMode('achievements')}
            className={`px-6 py-2 rounded-md transition-all duration-300 ${
              viewMode === 'achievements' 
                ? 'bg-white/20 text-white' 
                : 'text-white/70 hover:text-white'
            }`}
          >
            🏆 Achievements
          </button>
          <button
            onClick={() => setViewMode('badges')}
            className={`px-6 py-2 rounded-md transition-all duration-300 ${
              viewMode === 'badges' 
                ? 'bg-white/20 text-white' 
                : 'text-white/70 hover:text-white'
            }`}
          >
            🏅 Badges
          </button>
        </div>
      </div>

      {viewMode === 'achievements' ? (
        <>
          {/* Filters */}
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Category Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
                <select
                  value={activeCategory}
                  onChange={(e) => setActiveCategory(e.target.value)}
                  className="w-full bg-white/90 border border-gray-300 rounded-lg px-3 py-2 text-gray-900"
                >
                  {categories.map(category => (
                    <option key={category.id} value={category.id} className="bg-gray-800">
                      {category.icon} {category.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Difficulty Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
                <select
                  value={activeDifficulty}
                  onChange={(e) => setActiveDifficulty(e.target.value)}
                  className="w-full bg-white/90 border border-gray-300 rounded-lg px-3 py-2 text-gray-900"
                >
                  {difficulties.map(difficulty => (
                    <option key={difficulty.id} value={difficulty.id} className="bg-gray-800">
                      {difficulty.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Unlocked Only Toggle */}
              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="unlockedOnly"
                  checked={showUnlockedOnly}
                  onChange={(e) => setShowUnlockedOnly(e.target.checked)}
                  className="rounded bg-white/10 border-white/20"
                />
                <label htmlFor="unlockedOnly" className="text-white/80 text-sm">
                  Show unlocked only
                </label>
              </div>

              {/* Results Count */}
              <div className="flex items-center justify-end">
                <span className="text-white/60 text-sm">
                  {filteredAchievements.length} of {achievements.length} achievements
                </span>
              </div>
            </div>
          </div>

          {/* Achievements Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAchievements.map(renderAchievementCard)}
          </div>

          {filteredAchievements.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🏆</div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No achievements found</h3>
              <p className="text-gray-700">Try adjusting your filters to see more achievements</p>
            </div>
          )}
        </>
      ) : (
        /* Badges View */
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
          {badges.map(renderBadge)}
        </div>
      )}

      {/* Achievement Detail Modal */}
      {selectedAchievement && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gray-900/95 backdrop-blur-lg rounded-lg p-6 max-w-md w-full border border-white/20"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`text-4xl p-3 rounded-full bg-gradient-to-r ${getDifficultyColor(selectedAchievement.difficulty)} ${
                  selectedAchievement.unlocked ? '' : 'grayscale'
                }`}>
                  {selectedAchievement.icon}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-900">{selectedAchievement.title}</h2>
                  <span className={`text-xs px-2 py-1 rounded-full bg-gradient-to-r ${getDifficultyColor(selectedAchievement.difficulty)} text-white font-medium`}>
                    {selectedAchievement.difficulty.toUpperCase()}
                  </span>
                </div>
              </div>
              <button
                onClick={() => setSelectedAchievement(null)}
                className="text-white/60 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>

            <p className="text-gray-700 mb-4">{selectedAchievement.description}</p>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-white/60">Points:</span>
                <span className="text-yellow-400 font-bold">{selectedAchievement.points}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white/60">Rarity:</span>
                <span className={`font-medium ${rarities[selectedAchievement.rarity].color}`}>
                  {selectedAchievement.rarity.charAt(0).toUpperCase() + selectedAchievement.rarity.slice(1)}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-white/60">Status:</span>
                <span className={selectedAchievement.unlocked ? 'text-green-400' : 'text-white/50'}>
                  {selectedAchievement.unlocked ? 'Unlocked' : 'Locked'}
                </span>
              </div>

              {selectedAchievement.unlocked && selectedAchievement.unlockedAt && (
                <div className="flex items-center justify-between">
                  <span className="text-white/60">Unlocked:</span>
                  <span className="text-white/80">{formatDate(selectedAchievement.unlockedAt)}</span>
                </div>
              )}

              {!selectedAchievement.unlocked && selectedAchievement.progress !== undefined && selectedAchievement.target && (
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white/60">Progress:</span>
                    <span className="text-white/80">{selectedAchievement.progress} / {selectedAchievement.target}</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${getDifficultyColor(selectedAchievement.difficulty)}`}
                      style={{ width: `${(selectedAchievement.progress / selectedAchievement.target) * 100}%` }}
                    ></div>
                  </div>
                </div>
              )}
            </div>

            <div className="mt-4 pt-4 border-t border-white/20">
              <p className="text-sm text-white/60">
                <strong>Requirements:</strong> {selectedAchievement.requirements.join(', ')}
              </p>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default Achievements;