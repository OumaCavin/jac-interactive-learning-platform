// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import { apiClient } from './apiClient';

export interface AssessmentAttempt {
  id: string;
  user: number;
  module: number;
  status: 'in_progress' | 'completed' | 'abandoned' | 'timed_out';
  started_at: string;
  completed_at?: string;
  score?: number;
  max_score: number;
  passing_score: number;
  time_spent?: number;
  answers: Record<string, any>;
  feedback: Record<string, any>;
}

export interface AssessmentQuestion {
  id: string;
  module: number;
  title: string;
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'short_answer' | 'code_question' | 'essay';
  options?: string[];
  correct_answer: string;
  explanation?: string;
  points: number;
  difficulty_level: 'easy' | 'medium' | 'hard';
  order: number;
  tags: string[];
}

export interface UserAssessmentResult {
  id: string;
  user: number;
  module: number;
  average_score: number;
  best_score: number;
  total_attempts: number;
  questions_attempted: number;
  topics_covered: string[];
  learning_objectives_met: string[];
  created_at: string;
  updated_at: string;
}

class AssessmentService {
  private baseURL = '/api/assessment';

  // Assessment Attempts - Matches expected endpoint: GET /api/assessment/attempts/
  async getAttempts(userId?: number): Promise<AssessmentAttempt[]> {
    const params = userId ? { user_id: userId } : {};
    const response = await apiClient.get(`${this.baseURL}/attempts/`, { params });
    return response.data;
  }

  // Alias for backward compatibility
  async getUserAttempts(userId: number): Promise<AssessmentAttempt[]> {
    return this.getAttempts(userId);
  }

  async startAttempt(userId: number, moduleId: number): Promise<AssessmentAttempt> {
    const response = await apiClient.post(`${this.baseURL}/attempts/`, {
      user: userId,
      module: moduleId
    });
    return response.data;
  }

  async submitAttempt(attemptId: string, answers: Record<string, any>): Promise<AssessmentAttempt> {
    const response = await apiClient.post(`${this.baseURL}/attempts/${attemptId}/submit/`, {
      answers
    });
    return response.data;
  }

  async abandonAttempt(attemptId: string): Promise<AssessmentAttempt> {
    const response = await apiClient.post(`${this.baseURL}/attempts/${attemptId}/abandon/`);
    return response.data;
  }

  async getAttempt(attemptId: string): Promise<AssessmentAttempt> {
    const response = await apiClient.get(`${this.baseURL}/attempts/${attemptId}/`);
    return response.data;
  }

  // Assessment Quizzes (Questions) - Matches expected endpoint: GET /api/assessment/quizzes/
  async getQuizzes(moduleId?: number, filters?: {
    difficulty?: string;
    question_type?: string;
    active_only?: boolean;
  }): Promise<AssessmentQuestion[]> {
    const params: any = {};
    
    if (moduleId) params.module_id = moduleId;
    if (filters?.difficulty) params.difficulty = filters.difficulty;
    if (filters?.question_type) params.question_type = filters.question_type;
    if (filters?.active_only !== undefined) params.active_only = filters.active_only.toString();
    
    const response = await apiClient.get(`${this.baseURL}/questions/`, { params });
    return response.data;
  }

  // Alias for backward compatibility  
  async getQuestionsByModule(moduleId: number): Promise<AssessmentQuestion[]> {
    return this.getQuizzes(moduleId);
  }

  async getQuiz(quizId: string): Promise<AssessmentQuestion> {
    const response = await apiClient.get(`${this.baseURL}/questions/${quizId}/`);
    return response.data;
  }

  async getQuestionsByModuleGrouped(moduleId: number): Promise<{
    module_id: string;
    questions: AssessmentQuestion[];
    count: number;
  }> {
    const response = await apiClient.get(`${this.baseURL}/questions/by_module/`, {
      params: { module_id: moduleId }
    });
    return response.data;
  }

  async checkAnswer(questionId: string, answer: string): Promise<{
    question_id: string;
    is_correct: boolean;
    correct_answer: string;
    explanation?: string;
    points_earned: number;
  }> {
    const response = await apiClient.post(`${this.baseURL}/questions/${questionId}/check_answer/`, {
      answer
    });
    return response.data;
  }

  // Assessment Results
  async getUserResults(userId: number): Promise<UserAssessmentResult[]> {
    const response = await apiClient.get(`${this.baseURL}/results/`, {
      params: { user_id: userId }
    });
    return response.data;
  }

  // Assessment Statistics - Matches expected endpoint: GET /api/assessment/stats/
  async getStats(moduleId?: string): Promise<any> {
    const params = moduleId ? { module_id: moduleId } : {};
    const response = await apiClient.get(`${this.baseURL}/stats/`, { params });
    return response.data;
  }

  // Additional utility methods
  async getAssessmentOverview(): Promise<{
    total_attempts: number;
    completed_attempts: number;
    active_modules: number;
    total_questions: number;
    average_score: number;
    unique_users: number;
  }> {
    const response = await apiClient.get(`${this.baseURL}/stats/`);
    return response.data;
  }

  async getModuleStats(moduleId: string): Promise<{
    module_id: string;
    module_title: string;
    total_attempts: number;
    completed_attempts: number;
    average_score: number;
    pass_rate: number;
    average_duration: number;
    fastest_attempt: number;
    slowest_attempt: number;
    total_questions: number;
    questions_attempted: number;
    unique_users: number;
    returning_users: number;
  }> {
    const response = await apiClient.get(`${this.baseURL}/stats/`, {
      params: { module_id: moduleId }
    });
    return response.data;
  }

  // Health check for assessment service
  async checkHealth(): Promise<{ status: string; message: string }> {
    try {
      await this.getStats();
      return { status: 'healthy', message: 'Assessment service is operational' };
    } catch (error) {
      return { status: 'unhealthy', message: 'Assessment service is not responding' };
    }
  }
}

export const assessmentService = new AssessmentService();
export default assessmentService;
