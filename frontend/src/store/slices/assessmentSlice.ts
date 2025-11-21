/**
 * Assessment slice
 * Manages quizzes, assessments, and evaluation state
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

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
    // Data actions
    setQuizzes: (state, action: PayloadAction<Quiz[]>) => {
      state.quizzes = action.payload;
    },
    addQuiz: (state, action: PayloadAction<Quiz>) => {
      state.quizzes.push(action.payload);
    },
    updateQuiz: (state, action: PayloadAction<Quiz>) => {
      const index = state.quizzes.findIndex(q => q.id === action.payload.id);
      if (index !== -1) {
        state.quizzes[index] = action.payload;
      }
    },
    removeQuiz: (state, action: PayloadAction<string>) => {
      state.quizzes = state.quizzes.filter(q => q.id !== action.payload);
    },
    
    setQuizAttempts: (state, action: PayloadAction<QuizAttempt[]>) => {
      state.quiz_attempts = action.payload;
    },
    addQuizAttempt: (state, action: PayloadAction<QuizAttempt>) => {
      state.quiz_attempts.push(action.payload);
    },
    updateQuizAttempt: (state, action: PayloadAction<QuizAttempt>) => {
      const index = state.quiz_attempts.findIndex(a => a.id === action.payload.id);
      if (index !== -1) {
        state.quiz_attempts[index] = action.payload;
      }
    },
    
    // Current assessment
    setCurrentQuiz: (state, action: PayloadAction<string | null>) => {
      state.current_quiz = action.payload;
    },
    setCurrentAttempt: (state, action: PayloadAction<string | null>) => {
      state.current_attempt = action.payload;
    },
    
    // UI state
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setSubmitting: (state, action: PayloadAction<boolean>) => {
      state.isSubmitting = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    
    // Timer
    setTimeRemaining: (state, action: PayloadAction<number>) => {
      state.time_remaining = action.payload;
    },
    decrementTimeRemaining: (state) => {
      if (state.time_remaining && state.time_remaining > 0) {
        state.time_remaining -= 1;
      } else {
        state.is_timer_active = false;
      }
    },
    setTimerActive: (state, action: PayloadAction<boolean>) => {
      state.is_timer_active = action.payload;
    },
    startTimer: (state, action: PayloadAction<number>) => {
      state.time_remaining = action.payload;
      state.is_timer_active = true;
    },
    stopTimer: (state) => {
      state.is_timer_active = false;
    },
    
    // Results
    setLastAttemptResult: (state, action: PayloadAction<{
      score: number;
      max_score: number;
      passed: boolean;
      feedback: string;
    }>) => {
      state.last_attempt_result = action.payload;
    },
    clearLastAttemptResult: (state) => {
      state.last_attempt_result = undefined;
    },
    
    // Answer management
    updateAnswer: (state, action: PayloadAction<{ questionId: string; answer: string | string[] }>) => {
      // This would typically be handled in a separate attempt slice
      // For now, we'll store current answers in the current attempt
    },
    
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
});

// Export actions
export const {
  // Data
  setQuizzes,
  addQuiz,
  updateQuiz,
  removeQuiz,
  setQuizAttempts,
  addQuizAttempt,
  updateQuizAttempt,
  
  // Current assessment
  setCurrentQuiz,
  setCurrentAttempt,
  
  // UI state
  setLoading,
  setSubmitting,
  setError,
  clearError,
  
  // Timer
  setTimeRemaining,
  decrementTimeRemaining,
  setTimerActive,
  startTimer,
  stopTimer,
  
  // Results
  setLastAttemptResult,
  clearLastAttemptResult,
  
  // Answer management
  updateAnswer,
  
  // Reset
  resetAssessment,
} = assessmentSlice.actions;

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