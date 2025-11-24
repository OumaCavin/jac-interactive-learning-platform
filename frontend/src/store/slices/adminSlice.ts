/**
 * Admin analytics slice
 * Manages admin-specific data and analytics for learning path administration
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Admin analytics types
export interface LearningPathAnalytics {
  id: number;
  name: string;
  completion_rate: number;
  total_learners: number;
  average_score: number;
  total_modules: number;
  published_modules: number;
  total_study_time: number;
  last_activity: string;
  performance_score: number;
  user_satisfaction: number;
}

export interface CompletionTrend {
  period: string;
  completion_rate: number;
  learners: number;
  active_users: number;
  new_enrollments: number;
  completions: number;
}

export interface UserJourneyStage {
  stage: string;
  users: number;
  percentage: number;
  dropoff_rate?: number;
}

export interface PerformanceInsight {
  id: string;
  type: 'warning' | 'success' | 'info' | 'error';
  title: string;
  description: string;
  action: string;
  impact: 'high' | 'medium' | 'low';
  path_id?: number;
  created_at: string;
  is_dismissed: boolean;
}

export interface AdminMetrics {
  total_users: number;
  total_learning_paths: number;
  total_modules: number;
  total_lessons: number;
  active_learners: number;
  completion_rate: number;
  average_study_time: number;
  code_success_rate: number;
  user_engagement_score: number;
}

export interface AdminState {
  // Analytics data
  learning_path_analytics: LearningPathAnalytics[];
  completion_trends: CompletionTrend[];
  user_journey: UserJourneyStage[];
  performance_insights: PerformanceInsight[];
  admin_metrics: AdminMetrics;
  
  // Filters and pagination
  analytics_filters: {
    timeframe: 'week' | 'month' | 'quarter' | 'year';
    path_status: string[];
    difficulty_levels: string[];
    search_query: string;
  };
  analytics_pagination: {
    page: number;
    page_size: number;
    total: number;
  };
  
  // UI state
  is_loading: boolean;
  error: string | null;
  
  // Real-time data
  realtime_updates: {
    active_users: number;
    recent_completions: number;
    code_submissions: number;
    last_updated: string;
  };
}

// Initial state
const initialState: AdminState = {
  // Analytics data
  learning_path_analytics: [],
  completion_trends: [],
  user_journey: [],
  performance_insights: [],
  admin_metrics: {
    total_users: 0,
    total_learning_paths: 0,
    total_modules: 0,
    total_lessons: 0,
    active_learners: 0,
    completion_rate: 0,
    average_study_time: 0,
    code_success_rate: 0,
    user_engagement_score: 0,
  },
  
  // Filters and pagination
  analytics_filters: {
    timeframe: 'month',
    path_status: [],
    difficulty_levels: [],
    search_query: '',
  },
  analytics_pagination: {
    page: 1,
    page_size: 10,
    total: 0,
  },
  
  // UI state
  is_loading: false,
  error: null,
  
  // Real-time data
  realtime_updates: {
    active_users: 0,
    recent_completions: 0,
    code_submissions: 0,
    last_updated: new Date().toISOString(),
  },
};

// Admin analytics slice
const adminSlice = createSlice({
  name: 'admin',
  initialState,
  reducers: {
    // Analytics data actions
    setLearningPathAnalytics: (state, action: PayloadAction<LearningPathAnalytics[]>) => {
      state.learning_path_analytics = action.payload;
    },
    
    updateLearningPathAnalytics: (state, action: PayloadAction<LearningPathAnalytics>) => {
      const index = state.learning_path_analytics.findIndex(
        item => item.id === action.payload.id
      );
      if (index !== -1) {
        state.learning_path_analytics[index] = action.payload;
      } else {
        state.learning_path_analytics.push(action.payload);
      }
    },
    
    setCompletionTrends: (state, action: PayloadAction<CompletionTrend[]>) => {
      state.completion_trends = action.payload;
    },
    
    setUserJourney: (state, action: PayloadAction<UserJourneyStage[]>) => {
      state.user_journey = action.payload;
    },
    
    setPerformanceInsights: (state, action: PayloadAction<PerformanceInsight[]>) => {
      state.performance_insights = action.payload;
    },
    
    addPerformanceInsight: (state, action: PayloadAction<PerformanceInsight>) => {
      state.performance_insights.unshift(action.payload);
    },
    
    dismissPerformanceInsight: (state, action: PayloadAction<string>) => {
      const insight = state.performance_insights.find(item => item.id === action.payload);
      if (insight) {
        insight.is_dismissed = true;
      }
    },
    
    setAdminMetrics: (state, action: PayloadAction<AdminMetrics>) => {
      state.admin_metrics = action.payload;
    },
    
    // Filters and pagination
    setAnalyticsFilters: (state, action: PayloadAction<Partial<AdminState['analytics_filters']>>) => {
      Object.assign(state.analytics_filters, action.payload);
    },
    
    setAnalyticsPagination: (state, action: PayloadAction<Partial<AdminState['analytics_pagination']>>) => {
      Object.assign(state.analytics_pagination, action.payload);
    },
    
    // UI state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.is_loading = action.payload;
    },
    
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    // Real-time updates
    updateRealtimeData: (state, action: PayloadAction<Partial<AdminState['realtime_updates']>>) => {
      Object.assign(state.realtime_updates, action.payload);
      state.realtime_updates.last_updated = new Date().toISOString();
    },
    
    // Bulk operations
    bulkUpdateLearningPaths: (state, action: PayloadAction<{ ids: number[]; updates: Partial<LearningPathAnalytics> }>) => {
      action.payload.ids.forEach(id => {
        const index = state.learning_path_analytics.findIndex(item => item.id === id);
        if (index !== -1) {
          Object.assign(state.learning_path_analytics[index], action.payload.updates);
        }
      });
    },
    
    // Reset state
    resetAnalytics: (state) => {
      state.learning_path_analytics = [];
      state.completion_trends = [];
      state.user_journey = [];
      state.performance_insights = [];
      state.analytics_filters = initialState.analytics_filters;
      state.analytics_pagination = initialState.analytics_pagination;
      state.error = null;
    },
  },
});

// Export actions
export const {
  // Analytics data
  setLearningPathAnalytics,
  updateLearningPathAnalytics,
  setCompletionTrends,
  setUserJourney,
  setPerformanceInsights,
  addPerformanceInsight,
  dismissPerformanceInsight,
  setAdminMetrics,
  
  // Filters and pagination
  setAnalyticsFilters,
  setAnalyticsPagination,
  
  // UI state
  setLoading,
  setError,
  clearError,
  
  // Real-time updates
  updateRealtimeData,
  
  // Bulk operations
  bulkUpdateLearningPaths,
  
  // Reset
  resetAnalytics,
} = adminSlice.actions;

// Selectors
export const selectAdmin = (state: { admin: AdminState }) => state.admin;

export const selectLearningPathAnalytics = (state: { admin: AdminState }) => 
  state.admin.learning_path_analytics;

export const selectCompletionTrends = (state: { admin: AdminState }) => 
  state.admin.completion_trends;

export const selectUserJourney = (state: { admin: AdminState }) => 
  state.admin.user_journey;

export const selectPerformanceInsights = (state: { admin: AdminState }) => 
  state.admin.performance_insights.filter(insight => !insight.is_dismissed);

export const selectAdminMetrics = (state: { admin: AdminState }) => 
  state.admin.admin_metrics;

export const selectAnalyticsFilters = (state: { admin: AdminState }) => 
  state.admin.analytics_filters;

export const selectAnalyticsPagination = (state: { admin: AdminState }) => 
  state.admin.analytics_pagination;

export const selectRealtimeUpdates = (state: { admin: AdminState }) => 
  state.admin.realtime_updates;

export const selectIsLoading = (state: { admin: AdminState }) => 
  state.admin.is_loading;

export const selectError = (state: { admin: AdminState }) => 
  state.admin.error;

// Utility selectors
export const selectFilteredAnalytics = (state: { admin: AdminState }) => {
  const { learning_path_analytics, analytics_filters } = state.admin;
  
  return learning_path_analytics.filter(analytics => {
    // Status filter
    if (analytics_filters.path_status.length > 0) {
      // This would need to be mapped from analytics to actual status
      // For now, just return true
    }
    
    // Search query filter
    if (analytics_filters.search_query) {
      const query = analytics_filters.search_query.toLowerCase();
      if (!analytics.name.toLowerCase().includes(query)) {
        return false;
      }
    }
    
    return true;
  });
};

export const selectTopPerformingPaths = (state: { admin: AdminState }, limit: number = 5) => {
  return [...state.admin.learning_path_analytics]
    .sort((a, b) => b.completion_rate - a.completion_rate)
    .slice(0, limit);
};

// Export reducer
export default adminSlice.reducer;