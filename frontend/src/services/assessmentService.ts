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
  private baseURL = '/api/assessments';

  // Assessment Attempts
  async getUserAttempts(userId: number): Promise<AssessmentAttempt[]> {
    const response = await apiClient.get(`${this.baseURL}/attempts/user/`, {
      params: { user_id: userId }
    });
    return response.data;
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

  // Assessment Questions
  async getQuestionsByModule(moduleId: number): Promise<AssessmentQuestion[]> {
    const response = await apiClient.get(`${this.baseURL}/questions/by_module/`, {
      params: { module_id: moduleId }
    });
    return response.data;
  }

  async checkAnswer(questionId: string, answer: string): Promise<{
    correct: boolean;
    explanation?: string;
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

  async getAssessmentStats(): Promise<any> {
    const response = await apiClient.get(`${this.baseURL}/stats/`);
    return response.data;
  }
}

export const assessmentService = new AssessmentService();
export default assessmentService;
