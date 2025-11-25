import { apiClient } from './apiClient';
import { toast } from 'react-hot-toast';

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || 
                   error.response?.data?.message || 
                   'An error occurred';
    
    toast.error(message);
    return Promise.reject(error);
  }
);

// Types
export interface LearningPath {
  id: number;
  title: string;
  description: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  estimated_duration: number;
  modules_count: number;
  rating: number;
  created_at: string;
  updated_at: string;
}

export interface Module {
  id: number;
  learning_path: number;
  title: string;
  description: string;
  content: string;
  order_index: number;
  estimated_duration: number;
  module_type: 'lesson' | 'exercise' | 'assessment';
  prerequisites: number[];
  created_at: string;
  updated_at: string;
}

export interface CodeSubmission {
  id: number;
  user: number;
  module: number;
  code: string;
  language: 'python' | 'jac';
  status: 'pending' | 'running' | 'completed' | 'failed';
  execution_time: number | null;
  memory_usage: number | null;
  output: string | null;
  error_message: string | null;
  test_cases_passed: number;
  test_cases_total: number;
  score: number;
  created_at: string;
  updated_at: string;
}

export interface CodeExecutionRequest {
  code: string;
  language: 'python' | 'jac';
  test_input?: string;
  timeout?: number;
  memory_limit?: number;
}

export interface CodeExecutionResponse {
  success: boolean;
  output: string;
  execution_time: number;
  memory_usage: number;
  error?: string;
}

export interface UserModuleProgress {
  id: number;
  user: number;
  module: number;
  status: 'not_started' | 'in_progress' | 'completed';
  time_spent: number;
  attempts: number;
  score: number;
  last_accessed: string;
  completed_at: string | null;
}

// Learning API Service
export const learningService = {
  // Learning Paths
  getLearningPaths: (): Promise<LearningPath[]> =>
    apiClient.get('/learning/learning-paths/').then(res => res.data),

  getLearningPath: (id: number): Promise<LearningPath> =>
    apiClient.get(`/learning/learning-paths/${id}/`).then(res => res.data),

  // Modules
  getModules: (pathId: number): Promise<Module[]> =>
    apiClient.get(`/learning/modules/?learning_path=${pathId}`).then(res => res.data),

  getModule: (id: number): Promise<Module> =>
    apiClient.get(`/learning/modules/${id}/`).then(res => res.data),

  // Code Execution
  executeCode: (request: CodeExecutionRequest): Promise<CodeExecutionResponse> =>
    apiClient.post('/learning/code/execute/', request).then(res => res.data),

  // Code Submissions
  createCodeSubmission: (data: Partial<CodeSubmission>): Promise<CodeSubmission> =>
    apiClient.post('/learning/code-submissions/', data).then(res => res.data),

  getCodeSubmission: (id: number): Promise<CodeSubmission> =>
    apiClient.get(`/learning/code-submissions/${id}/`).then(res => res.data),

  getUserSubmissions: (userId: number): Promise<CodeSubmission[]> =>
    apiClient.get(`/learning/code-submissions/?user=${userId}`).then(res => res.data),

  getModuleSubmissions: (moduleId: number): Promise<CodeSubmission[]> =>
    apiClient.get(`/learning/code-submissions/?module=${moduleId}`).then(res => res.data),

  // User Progress
  getUserModuleProgress: (userId: number, moduleId: number): Promise<UserModuleProgress> =>
    apiClient.get(`/learning/user-module-progress/?user=${userId}&module=${moduleId}`).then(res => res.data),

  updateModuleProgress: (userId: number, moduleId: number, data: Partial<UserModuleProgress>): Promise<UserModuleProgress> =>
    apiClient.patch(`/learning/user-module-progress/?user=${userId}&module=${moduleId}`, data).then(res => res.data),

  // AI Code Review
  getAICodeReview: (submissionId: number): Promise<any> =>
    apiClient.get(`/learning/ai-code-reviews/?submission=${submissionId}`).then(res => res.data),

  createAICodeReview: (data: any): Promise<any> =>
    apiClient.post('/learning/ai-code-reviews/', data).then(res => res.data),

  // Test Cases
  getTestCases: (moduleId: number): Promise<any[]> =>
    apiClient.get(`/learning/test-cases/?module=${moduleId}`).then(res => res.data),

  // Assessment APIs
  getQuizzes: (): Promise<any[]> =>
    apiClient.get('/learning/assessment/quizzes/').then(res => res.data),

  getQuiz: (quizId: string): Promise<any> =>
    apiClient.get(`/learning/assessment/quizzes/${quizId}/`).then(res => res.data),

  startQuizAttempt: (quizId: string): Promise<any> =>
    apiClient.post(`/learning/assessment/quizzes/${quizId}/start/`).then(res => res.data),

  getUserAttempts: (): Promise<any[]> =>
    apiClient.get('/learning/assessment/attempts/').then(res => res.data),

  getAttempt: (attemptId: string): Promise<any> =>
    apiClient.get(`/learning/assessment/attempts/${attemptId}/`).then(res => res.data),

  submitAttempt: (attemptId: string, answers: any): Promise<any> =>
    apiClient.post(`/learning/assessment/attempts/${attemptId}/submit/`, { answers }).then(res => res.data),

  getAssessmentStats: (): Promise<any> =>
    apiClient.get('/learning/assessment/stats/').then(res => res.data),

  // Direct Assessment API endpoints
  getAssessmentQuestions: (moduleId?: string): Promise<any[]> =>
    apiClient.get(`/assessments/questions/${moduleId ? `?module_id=${moduleId}` : ''}`).then(res => res.data),

  getAssessmentAttempt: (attemptId: string): Promise<any> =>
    apiClient.get(`/assessments/attempts/${attemptId}/`).then(res => res.data),

  getAssessmentStats: (moduleId?: string): Promise<any> =>
    apiClient.get(`/assessments/stats/${moduleId ? `?module_id=${moduleId}` : ''}`).then(res => res.data),

  checkAssessmentAnswer: (questionId: string, answer: string): Promise<any> =>
    apiClient.post(`/assessments/questions/${questionId}/check_answer/`, { answer }).then(res => res.data),

  // JAC Code Execution (using correct backend endpoints)
  executeCode: (code: string, language: string = 'jac'): Promise<any> =>
    apiClient.post('/jac-execution/api/quick-execute/', { code, language, stdin: '' }).then(res => res.data),

  validateCode: (code: string, language: string = 'jac'): Promise<any> =>
    apiClient.post('/jac-execution/api/validate/', { code, language }).then(res => res.data),

  // JAC-specific execution methods
  executeJacCode: (code: string, language: 'python' | 'jac' = 'jac', testCases?: any[]): Promise<any> =>
    apiClient.post('/jac-execution/api/execute/', { 
      code, 
      language, 
      stdin: '',
      test_cases: testCases 
    }).then(res => res.data),

  validateJacCode: (code: string, language: string = 'jac'): Promise<any> =>
    apiClient.post('/jac-execution/api/validate/', { code, language }).then(res => res.data),

  getJacExecutionHistory: (limit: number = 10): Promise<any> =>
    apiClient.get(`/jac-execution/api/executions/?limit=${limit}`).then(res => res.data),

  getJacTemplates: (): Promise<any> =>
    apiClient.get('/jac-execution/api/templates/').then(res => res.data),

  getSyntaxReference: (): Promise<any> =>
    apiClient.get('/jac-execution/api/syntax-reference/').then(res => res.data),

  // Code Evaluation and Feedback
  evaluateCode: (code: string, testCases?: any[]): Promise<any> =>
    apiClient.post('/jac-execution/api/evaluate/', { code, test_cases: testCases }).then(res => res.data),

  getCodeSuggestions: (code: string): Promise<any> =>
    apiClient.post('/jac-execution/api/suggestions/', { code }).then(res => res.data),

  // Admin Analytics
  getLearningPathAnalytics: (pathId?: number): Promise<any> =>
    apiClient.get(`/learning/admin/analytics/${pathId ? `?path_id=${pathId}` : ''}`).then(res => res.data),

  getCompletionTrends: (timeframe: 'week' | 'month' | 'quarter' | 'year' = 'month'): Promise<any[]> =>
    apiClient.get(`/learning/admin/completion-trends/?timeframe=${timeframe}`).then(res => res.data),

  getUserJourneyAnalytics: (pathId: number): Promise<any> =>
    apiClient.get(`/learning/admin/user-journey/?path_id=${pathId}`).then(res => res.data),

  getPerformanceInsights: (): Promise<any[]> =>
    apiClient.get('/learning/admin/insights/').then(res => res.data),

  bulkUpdateLearningPaths: (pathIds: number[], updates: any): Promise<any> =>
    apiClient.patch('/learning/learning-paths/bulk-update/', { path_ids: pathIds, updates }).then(res => res.data),

  reorderModules: (pathId: number, moduleOrder: number[]): Promise<any> =>
    apiClient.post(`/learning/learning-paths/${pathId}/reorder-modules/`, { module_order: moduleOrder }).then(res => res.data),
};

export default learningService;