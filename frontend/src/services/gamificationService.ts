// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Gamification Service - JAC Learning Platform Frontend
 * 
 * Service for gamification features including achievements, badges, points, and streaks.
 * Connects React frontend to Django backend gamification API.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import api from './learningService';

// Types for gamification system
export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  difficulty: string;
  requirements: Record<string, any>;
  minimum_points: number;
  unlock_conditions: Record<string, any>;
  rarity: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserBadge {
  id: string;
  badge: Badge;
  earned_at: string;
  progress_data: Record<string, any>;
  earned_through: string;
  is_verified: boolean;
  verified_at?: string;
  earned_days_ago: number;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  difficulty: string;
  rarity?: string;
  criteria_type: string;
  criteria_value: number;
  criteria_operator: string;
  points_reward: number;
  badge?: Badge;
  is_active: boolean;
  unlock_order: number;
  created_at: string;
  updated_at: string;
}

export interface UserAchievement {
  id: string;
  achievement: Achievement;
  current_progress: number;
  target_progress: number;
  progress_percentage: number;
  progress_percentage_formatted: string;
  is_completed: boolean;
  completed_at?: string;
  started_at: string;
  points_earned: number;
  badge_earned?: UserBadge;
  progress_history: Array<{
    timestamp: string;
    progress: number;
    percentage: number;
  }>;
  last_progress_update: string;
  days_in_progress: number;
}

export interface UserPoints {
  id: string;
  total_points: number;
  available_points: number;
  lifetime_points: number;
  learning_points: number;
  coding_points: number;
  assessment_points: number;
  engagement_points: number;
  points_by_category: {
    learning: number;
    coding: number;
    assessment: number;
    engagement: number;
  };
  last_earned?: string;
  last_spent?: string;
  updated_at: string;
}

export interface PointTransaction {
  id: string;
  amount: number;
  transaction_type: 'earned' | 'spent' | 'bonus' | 'penalty';
  source: string;
  description: string;
  metadata: Record<string, any>;
  balance_after: number;
  created_at: string;
}

export interface UserLevel {
  id: string;
  current_level: number;
  current_xp: number;
  total_xp: number;
  xp_to_next_level: number;
  progress_percentage: number;
  xp_for_next_level: number;
  level_up_notifications: Array<{
    level: number;
    timestamp: string;
    xp_earned: number;
  }>;
  last_level_up?: string;
  updated_at: string;
}

export interface LearningStreak {
  id: string;
  current_streak: number;
  longest_streak: number;
  last_activity_date?: string;
  streak_multiplier: number;
  streak_multiplier_display: string;
  streak_history: Array<{
    date: string;
    streak_count: number;
    streak_multiplier: number;
  }>;
  streak_breaks: Array<{
    broken_streak: number;
    date: string;
    gap_days: number;
  }>;
  days_since_last_activity?: number;
  created_at: string;
  updated_at: string;
}

export interface GamificationOverview {
  total_points: number;
  current_level: number;
  current_streak: number;
  total_achievements: number;
  completed_achievements: number;
  total_badges: number;
  earned_badges: number;
  recent_achievements: UserAchievement[];
  recent_badges: UserBadge[];
  current_level_info: UserLevel;
  streak_info: LearningStreak;
}

export interface LeaderboardEntry {
  user: string;
  rank: number;
  total_points: number;
  current_level: number;
  current_streak: number;
}

export interface GamificationStats {
  total_users: number;
  active_users_today: number;
  total_achievements_completed: number;
  total_badges_earned: number;
  average_streak: number;
  total_points_earned: number;
  top_users_by_points: LeaderboardEntry[];
  top_users_by_streak: LeaderboardEntry[];
  recent_achievements: UserAchievement[];
  recent_badges: UserBadge[];
}

// Gamification API Service
export const gamificationService = {
  // Badge Management
  getBadges: (): Promise<Badge[]> =>
    api.get('/gamification/badges/').then(res => res.data),

  getBadge: (id: string): Promise<Badge> =>
    api.get(`/gamification/badges/${id}/`).then(res => res.data),

  claimBadge: (id: string): Promise<UserBadge> =>
    api.post(`/gamification/badges/${id}/claim/`).then(res => res.data),

  // User Badge Management
  getUserBadges: (): Promise<UserBadge[]> =>
    api.get('/gamification/user-badges/').then(res => res.data),

  getUserBadgesByCategory: (): Promise<Record<string, UserBadge[]>> =>
    api.get('/gamification/user-badges/by_category/').then(res => res.data),

  getRecentBadges: (): Promise<UserBadge[]> =>
    api.get('/gamification/user-badges/recent/').then(res => res.data),

  // Achievement Management
  getAchievements: (): Promise<Achievement[]> =>
    api.get('/gamification/achievements/').then(res => res.data),

  getAchievement: (id: string): Promise<Achievement> =>
    api.get(`/gamification/achievements/${id}/`).then(res => res.data),

  startAchievementTracking: (id: string): Promise<any> =>
    api.post(`/gamification/achievements/${id}/start_tracking/`).then(res => res.data),

  // User Achievement Management
  getUserAchievements: (): Promise<UserAchievement[]> =>
    api.get('/gamification/user-achievements/').then(res => res.data),

  getUserAchievementsInProgress: (): Promise<UserAchievement[]> =>
    api.get('/gamification/user-achievements/in_progress/').then(res => res.data),

  getUserAchievementsCompleted: (): Promise<UserAchievement[]> =>
    api.get('/gamification/user-achievements/completed/').then(res => res.data),

  getUserAchievementsByCategory: (): Promise<Record<string, UserAchievement[]>> =>
    api.get('/gamification/user-achievements/by_category/').then(res => res.data),

  // User Points Management
  getUserPoints: (): Promise<UserPoints> =>
    api.get('/gamification/user-points/').then(res => res.data),

  addPoints: (amount: number, source: string, metadata?: Record<string, any>): Promise<any> =>
    api.post('/gamification/user-points/add_points/', {
      amount,
      source,
      metadata: metadata || {}
    }).then(res => res.data),

  spendPoints: (amount: number, purpose: string, metadata?: Record<string, any>): Promise<any> =>
    api.post('/gamification/user-points/spend_points/', {
      amount,
      purpose,
      metadata: metadata || {}
    }).then(res => res.data),

  getPointTransactions: (): Promise<PointTransaction[]> =>
    api.get('/gamification/user-points/transactions/').then(res => res.data),

  // User Level Management
  getUserLevel: (): Promise<UserLevel> =>
    api.get('/gamification/user-level/').then(res => res.data),

  addXP: (amount: number): Promise<any> =>
    api.post('/gamification/user-level/add_xp/', { amount }).then(res => res.data),

  // Learning Streak Management
  getLearningStreak: (): Promise<LearningStreak> =>
    api.get('/gamification/learning-streak/').then(res => res.data),

  recordStreakActivity: (activityDate?: string, context?: Record<string, any>): Promise<any> =>
    api.post('/gamification/learning-streak/record_activity/', {
      activity_date: activityDate,
      context: context || {}
    }).then(res => res.data),

  // Comprehensive Endpoints
  getGamificationOverview: (): Promise<GamificationOverview> =>
    api.get('/gamification/overview/').then(res => res.data),

  getLeaderboard: (type: 'points' | 'streak' | 'level' = 'points', limit: number = 10): Promise<LeaderboardEntry[]> => {
    const params = new URLSearchParams({
      type,
      limit: limit.toString()
    });
    return api.get(`/gamification/leaderboard/?${params}`).then(res => res.data);
  },

  getGamificationStats: (): Promise<GamificationStats> =>
    api.get('/gamification/stats/').then(res => res.data),

  // Integration endpoints
  awardPoints: (amount: number, source: string, metadata?: Record<string, any>): Promise<any> =>
    api.post('/gamification/integration/award_points/', {
      amount,
      source,
      metadata: metadata || {}
    }).then(res => res.data),

  updateStreak: (): Promise<any> =>
    api.post('/gamification/integration/update_streak/').then(res => res.data),

  checkAchievements: (type: string, value: number): Promise<any> =>
    api.post('/gamification/integration/check_achievements/', {
      type,
      value
    }).then(res => res.data),

  // Achievement Progress Tracking
  getAchievementProgress: (): Promise<any[]> =>
    api.get('/gamification/achievement-progress/').then(res => res.data),

  incrementAchievementProgress: (id: string, incrementBy: number = 1, context?: Record<string, any>): Promise<any> =>
    api.post(`/gamification/achievement-progress/${id}/increment/`, {
      increment_by: incrementBy,
      context: context || {}
    }).then(res => res.data),

  // Filtered queries
  getBadgesByCategory: (category: string): Promise<Badge[]> =>
    api.get(`/gamification/badges/?category=${category}`).then(res => res.data),

  getBadgesByDifficulty: (difficulty: string): Promise<Badge[]> =>
    api.get(`/gamification/badges/?difficulty=${difficulty}`).then(res => res.data),

  getAchievementsByCategory: (category: string): Promise<Achievement[]> =>
    api.get(`/gamification/achievements/?category=${category}`).then(res => res.data),

  getAchievementsByDifficulty: (difficulty: string): Promise<Achievement[]> =>
    api.get(`/gamification/achievements/?difficulty=${difficulty}`).then(res => res.data),

  // Helper methods for gamification triggers
  triggerModuleCompletion: async (moduleId: string, moduleTitle: string, learningPathId?: string): Promise<void> => {
    try {
      await gamificationService.awardPoints(50, 'module_completion', {
        module_id: moduleId,
        module_title: moduleTitle,
        learning_path_id: learningPathId
      });
      await gamificationService.updateStreak();
      await gamificationService.checkAchievements('modules_completed', 1);
    } catch (error) {
      console.warn('Failed to trigger module completion gamification:', error);
    }
  },

  triggerAssessmentCompletion: async (assessmentId: string, score: number, attemptNumber: number): Promise<void> => {
    try {
      const points = score >= 90 ? 100 : score >= 70 ? 75 : score >= 50 ? 50 : 25;
      const source = score >= 90 ? 'assessment_perfect' : 
                    score >= 70 ? 'assessment_good' : 
                    score >= 50 ? 'assessment_passed' : 'assessment_attempted';

      await gamificationService.awardPoints(points, source, {
        assessment_id: assessmentId,
        score,
        attempt_number: attemptNumber
      });
      await gamificationService.updateStreak();
      await gamificationService.checkAchievements('assessments_completed', 1);
      
      if (score === 100) {
        await gamificationService.checkAchievements('perfect_scores', 1);
      }
    } catch (error) {
      console.warn('Failed to trigger assessment completion gamification:', error);
    }
  },

  triggerCodeExecution: async (codeExecutionId: string, language: string, executionTime?: number): Promise<void> => {
    try {
      await gamificationService.awardPoints(25, 'code_execution', {
        code_execution_id: codeExecutionId,
        language,
        execution_time: executionTime
      });
      await gamificationService.checkAchievements('code_executions', 1);
    } catch (error) {
      console.warn('Failed to trigger code execution gamification:', error);
    }
  },

  triggerAIChat: async (agentId: string, agentType: string): Promise<void> => {
    try {
      await gamificationService.awardPoints(10, 'ai_chat', {
        agent_id: agentId,
        agent_type: agentType
      });
      await gamificationService.checkAchievements('ai_conversations', 1);
    } catch (error) {
      console.warn('Failed to trigger AI chat gamification:', error);
    }
  },

  triggerKnowledgeGraphActivity: async (nodeId: string, nodeType: string): Promise<void> => {
    try {
      await gamificationService.awardPoints(15, 'knowledge_graph', {
        node_id: nodeId,
        node_type: nodeType
      });
      await gamificationService.checkAchievements('knowledge_nodes_created', 1);
    } catch (error) {
      console.warn('Failed to trigger knowledge graph gamification:', error);
    }
  }
};

export default gamificationService;