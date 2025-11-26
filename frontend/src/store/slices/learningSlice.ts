// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Learning slice
 * Manages learning paths, modules, and learning progress state
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Types for learning state
export interface LearningPath {
  id: string;
  name: string;
  description: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  estimated_duration: number;
  module_count: number;
  completed_by_users: number;
  average_rating: number;
  is_featured: boolean;
  cover_image?: string;
  tags: string[];
}

export interface Module {
  id: string;
  title: string;
  description: string;
  learning_path: string;
  order: number;
  duration_minutes: number;
  difficulty_rating: number;
  content: string;
  content_type: 'markdown' | 'html' | 'interactive' | 'jac_code';
  jac_concepts: string[];
  code_examples: any[];
  has_quiz: boolean;
  has_coding_exercise: boolean;
  has_visual_demo: boolean;
  completion_rate: number;
  average_score: number;
}

export interface UserLearningPath {
  id: string;
  learning_path: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'paused';
  progress_percentage: number;
  current_module_order: number;
  started_at?: string;
  completed_at?: string;
  last_activity_at: string;
}

export interface UserModuleProgress {
  id: string;
  module: string;
  status: 'not_started' | 'in_progress' | 'completed' | 'skipped';
  time_spent: string;
  progress_percentage: number;
  quiz_score?: number;
  coding_score?: number;
  overall_score?: number;
  user_notes: string;
  started_at?: string;
  completed_at?: string;
}

export interface LearningState {
  // Data
  learning_paths: LearningPath[];
  modules: { [pathId: string]: Module[] };
  user_learning_paths: UserLearningPath[];
  user_module_progress: UserModuleProgress[];
  
  // Current selection
  current_learning_path: string | null;
  current_module: string | null;
  
  // UI state
  isLoading: boolean;
  error: string | null;
  
  // Filters and search
  filters: {
    difficulty: string[];
    tags: string[];
    duration: string;
  };
  searchQuery: string;
}

// Initial state
const initialState: LearningState = {
  // Data
  learning_paths: [],
  modules: {},
  user_learning_paths: [],
  user_module_progress: [],
  
  // Current selection
  current_learning_path: null,
  current_module: null,
  
  // UI state
  isLoading: false,
  error: null,
  
  // Filters and search
  filters: {
    difficulty: [],
    tags: [],
    duration: '',
  },
  searchQuery: '',
};

// Learning slice
const learningSlice = createSlice({
  name: 'learning',
  initialState,
  reducers: {
    // Data actions
    setLearningPaths: (state, action: PayloadAction<LearningPath[]>) => {
      state.learning_paths = action.payload;
    },
    addLearningPath: (state, action: PayloadAction<LearningPath>) => {
      state.learning_paths.push(action.payload);
    },
    updateLearningPath: (state, action: PayloadAction<LearningPath>) => {
      const index = state.learning_paths.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.learning_paths[index] = action.payload;
      }
    },
    removeLearningPath: (state, action: PayloadAction<string>) => {
      state.learning_paths = state.learning_paths.filter(p => p.id !== action.payload);
    },
    
    setModules: (state, action: PayloadAction<{ pathId: string; modules: Module[] }>) => {
      state.modules[action.payload.pathId] = action.payload.modules;
    },
    addModule: (state, action: PayloadAction<Module>) => {
      const { learning_path } = action.payload;
      if (!state.modules[learning_path]) {
        state.modules[learning_path] = [];
      }
      state.modules[learning_path].push(action.payload);
    },
    
    setUserLearningPaths: (state, action: PayloadAction<UserLearningPath[]>) => {
      state.user_learning_paths = action.payload;
    },
    updateUserLearningPath: (state, action: PayloadAction<UserLearningPath>) => {
      const index = state.user_learning_paths.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.user_learning_paths[index] = action.payload;
      } else {
        state.user_learning_paths.push(action.payload);
      }
    },
    
    setUserModuleProgress: (state, action: PayloadAction<UserModuleProgress[]>) => {
      state.user_module_progress = action.payload;
    },
    updateUserModuleProgress: (state, action: PayloadAction<UserModuleProgress>) => {
      const index = state.user_module_progress.findIndex(p => p.id === action.payload.id);
      if (index !== -1) {
        state.user_module_progress[index] = action.payload;
      } else {
        state.user_module_progress.push(action.payload);
      }
    },
    
    // Current selection
    setCurrentLearningPath: (state, action: PayloadAction<string | null>) => {
      state.current_learning_path = action.payload;
    },
    setCurrentModule: (state, action: PayloadAction<string | null>) => {
      state.current_module = action.payload;
    },
    
    // UI state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    
    // Filters and search
    setFilters: (state, action: PayloadAction<Partial<LearningState['filters']>>) => {
      Object.assign(state.filters, action.payload);
    },
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    clearFilters: (state) => {
      state.filters = {
        difficulty: [],
        tags: [],
        duration: '',
      };
      state.searchQuery = '';
    },
  },
});

// Export actions
export const {
  // Data
  setLearningPaths,
  addLearningPath,
  updateLearningPath,
  removeLearningPath,
  setModules,
  addModule,
  setUserLearningPaths,
  updateUserLearningPath,
  setUserModuleProgress,
  updateUserModuleProgress,
  
  // Current selection
  setCurrentLearningPath,
  setCurrentModule,
  
  // UI state
  setLoading,
  setError,
  clearError,
  
  // Filters and search
  setFilters,
  setSearchQuery,
  clearFilters,
} = learningSlice.actions;

// Selectors
export const selectLearning = (state: { learning: LearningState }) => state.learning;
export const selectLearningPaths = (state: { learning: LearningState }) => state.learning.learning_paths;
export const selectCurrentLearningPath = (state: { learning: LearningState }) => {
  const pathId = state.learning.current_learning_path;
  return pathId ? state.learning.learning_paths.find(p => p.id === pathId) : null;
};
export const selectModules = (state: { learning: LearningState }, pathId: string) => 
  state.learning.modules[pathId] || [];
export const selectCurrentModule = (state: { learning: LearningState }) => {
  const moduleId = state.learning.current_module;
  const pathId = state.learning.current_learning_path;
  if (!moduleId || !pathId) return null;
  
  const modules = state.learning.modules[pathId] || [];
  return modules.find(m => m.id === moduleId) || null;
};
export const selectUserLearningPaths = (state: { learning: LearningState }) => 
  state.learning.user_learning_paths;
export const selectUserModuleProgress = (state: { learning: LearningState }) => 
  state.learning.user_module_progress;
export const selectLearningFilters = (state: { learning: LearningState }) => 
  state.learning.filters;
export const selectLearningSearchQuery = (state: { learning: LearningState }) => 
  state.learning.searchQuery;

// Export reducer
export default learningSlice.reducer;