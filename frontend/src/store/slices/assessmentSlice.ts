// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Assessment slice
 * Manages quizzes, assessments, and evaluation state
 */

import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import { learningService } from '../../services/learningService';

// Async thunks for API calls
const fetchQuizzes = createAsyncThunk(
  'assessments/fetchQuizzes',
  async (_, { rejectWithValue }) => {
    try {
      const response = await learningService.getQuizzes();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch quizzes');
    }
  }
);

const fetchQuiz = createAsyncThunk(
  'assessments/fetchQuiz',
  async (quizId: string, { rejectWithValue }) => {
    try {
      const response = await learningService.getQuiz(quizId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch quiz');
    }
  }
);

const fetchUserAttempts = createAsyncThunk(
  'assessments/fetchUserAttempts',
  async (_, { rejectWithValue }) => {
    try {
      const response = await learningService.getUserAttempts();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch attempts');
    }
  }
);

const startQuizAttempt = createAsyncThunk(
  'assessments/startQuizAttempt',
  async (quizId: string, { rejectWithValue }) => {
    try {
      const response = await learningService.startQuizAttempt(quizId);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to start attempt');
    }
  }
);

const submitQuizAttempt = createAsyncThunk(
  'assessments/submitQuizAttempt',
  async ({ attemptId, answers }: { attemptId: string; answers: any }, { rejectWithValue }) => {
    try {
      const response = await learningService.submitAttempt(attemptId, answers);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to submit attempt');
    }
  }
);

const fetchAssessmentStats = createAsyncThunk(
  'assessments/fetchAssessmentStats',
  async (_, { rejectWithValue }) => {
    try {
      const response = await learningService.getAssessmentStats();
      return response;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch stats');
    }
  }
);

// Types for assessment state
export interface Quiz {
  id: string;
  title: string;
  description: string;
  learning_path?: string;
  module?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  time_limit?: number; // in minutes
  max_attempts: number;
  passing_score: number;
  questions: Question[];
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer' | 'code_completion' | 'jac_specific';
  question: string;
  options?: string[];
  correct_answer: string | string[];
  explanation?: string;
  jac_concept?: string;
  difficulty: 1 | 2 | 3 | 4 | 5;
  points: number;
}

export interface QuizAttempt {
  id: string;
  quiz: string;
  user: string;
  answers: { [questionId: string]: string | string[] };
  score: number;
  max_score: number;
  passed: boolean;
  time_taken: number; // in seconds
  started_at: string;
  completed_at?: string;
  feedback?: string;
}

export interface AssessmentState {
  // Data
  quizzes: Quiz[];
  quiz_attempts: QuizAttempt[];
  
  // Current assessment
  current_quiz: string | null;
  current_attempt: string | null;
  
  // UI state
  isLoading: boolean;
  isSubmitting: boolean;
  error: string | null;
  
  // Timer
  time_remaining?: number;
  is_timer_active: boolean;
  
  // Results
  last_attempt_result?: {
    score: number;
    max_score: number;
    passed: boolean;
    feedback: string;
  };
}

// Initial state
const initialState: AssessmentState = {
  // Data
  quizzes: [],
  quiz_attempts: [],
  
  // Current assessment
  current_quiz: null,
  current_attempt: null,
  
  // UI state
  isLoading: false,
  isSubmitting: false,
  error: null,
  
  // Timer
  time_remaining: undefined,
  is_timer_active: false,
  
  // Results
  last_attempt_result: undefined,
};

// Assessment slice
const assessmentSlice = createSlice({
  name: 'assessments',
  initialState,
  reducers: {
    // Reset
    resetAssessment: (state) => {
      state.current_quiz = null;
      state.current_attempt = null;
      state.isSubmitting = false;
      state.time_remaining = undefined;
      state.is_timer_active = false;
      state.last_attempt_result = undefined;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Quizzes
      .addCase(fetchQuizzes.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchQuizzes.fulfilled, (state, action) => {
        state.isLoading = false;
        state.quizzes = action.payload;
      })
      .addCase(fetchQuizzes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch User Attempts
      .addCase(fetchUserAttempts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserAttempts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.quiz_attempts = action.payload;
      })
      .addCase(fetchUserAttempts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Fetch Assessment Stats
      .addCase(fetchAssessmentStats.fulfilled, (state, action) => {
        // Store stats in a separate field if needed
        // For now, we'll integrate it with the existing data structure
      })
      
      // Start Quiz Attempt
      .addCase(startQuizAttempt.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(startQuizAttempt.fulfilled, (state, action) => {
        state.isLoading = false;
        state.current_attempt = action.payload.id;
        // Add the new attempt to the list
        state.quiz_attempts.push(action.payload);
      })
      .addCase(startQuizAttempt.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      
      // Submit Quiz Attempt
      .addCase(submitQuizAttempt.pending, (state) => {
        state.isSubmitting = true;
        state.error = null;
      })
      .addCase(submitQuizAttempt.fulfilled, (state, action) => {
        state.isSubmitting = false;
        state.last_attempt_result = {
          score: action.payload.score,
          max_score: action.payload.max_score,
          passed: action.payload.passed,
          feedback: action.payload.feedback || ''
        };
        // Update the attempt in the list
        const index = state.quiz_attempts.findIndex(a => a.id === action.payload.id);
        if (index !== -1) {
          state.quiz_attempts[index] = action.payload;
        }
      })
      .addCase(submitQuizAttempt.rejected, (state, action) => {
        state.isSubmitting = false;
        state.error = action.payload as string;
      });
  },
});

// Export async thunks directly
export { fetchQuizzes, fetchQuiz, fetchUserAttempts, startQuizAttempt, submitQuizAttempt, fetchAssessmentStats };

// Export slice actions
export const { resetAssessment } = assessmentSlice.actions;

// Selectors
export const selectAssessments = (state: { assessments: AssessmentState }) => state.assessments;
export const selectQuizzes = (state: { assessments: AssessmentState }) => state.assessments.quizzes;
export const selectCurrentQuiz = (state: { assessments: AssessmentState }) => {
  const quizId = state.assessments.current_quiz;
  return quizId ? state.assessments.quizzes.find(q => q.id === quizId) : null;
};
export const selectQuizAttempts = (state: { assessments: AssessmentState }) => 
  state.assessments.quiz_attempts;
export const selectCurrentAttempt = (state: { assessments: AssessmentState }) => {
  const attemptId = state.assessments.current_attempt;
  return attemptId ? state.assessments.quiz_attempts.find(a => a.id === attemptId) : null;
};
export const selectAssessmentLoading = (state: { assessments: AssessmentState }) => 
  state.assessments.isLoading;
export const selectAssessmentSubmitting = (state: { assessments: AssessmentState }) => 
  state.assessments.isSubmitting;
export const selectTimeRemaining = (state: { assessments: AssessmentState }) => 
  state.assessments.time_remaining;
export const selectTimerActive = (state: { assessments: AssessmentState }) => 
  state.assessments.is_timer_active;
export const selectLastAttemptResult = (state: { assessments: AssessmentState }) => 
  state.assessments.last_attempt_result;

// Export reducer
export default assessmentSlice.reducer;