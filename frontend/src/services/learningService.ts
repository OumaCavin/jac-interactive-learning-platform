import axios from 'axios';
import { toast } from 'react-hot-toast';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
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
    api.get('/learning/learning-paths/').then(res => res.data),

  getLearningPath: (id: number): Promise<LearningPath> =>
    api.get(`/learning/learning-paths/${id}/`).then(res => res.data),

  // Modules
  getModules: (pathId: number): Promise<Module[]> =>
    api.get(`/learning/modules/?learning_path=${pathId}`).then(res => res.data),

  getModule: (id: number): Promise<Module> =>
    api.get(`/learning/modules/${id}/`).then(res => res.data),

  // Code Execution
  executeCode: (request: CodeExecutionRequest): Promise<CodeExecutionResponse> =>
    api.post('/learning/code/execute/', request).then(res => res.data),

  // Code Submissions
  createCodeSubmission: (data: Partial<CodeSubmission>): Promise<CodeSubmission> =>
    api.post('/learning/code-submissions/', data).then(res => res.data),

  getCodeSubmission: (id: number): Promise<CodeSubmission> =>
    api.get(`/learning/code-submissions/${id}/`).then(res => res.data),

  getUserSubmissions: (userId: number): Promise<CodeSubmission[]> =>
    api.get(`/learning/code-submissions/?user=${userId}`).then(res => res.data),

  getModuleSubmissions: (moduleId: number): Promise<CodeSubmission[]> =>
    api.get(`/learning/code-submissions/?module=${moduleId}`).then(res => res.data),

  // User Progress
  getUserModuleProgress: (userId: number, moduleId: number): Promise<UserModuleProgress> =>
    api.get(`/learning/user-module-progress/?user=${userId}&module=${moduleId}`).then(res => res.data),

  updateModuleProgress: (userId: number, moduleId: number, data: Partial<UserModuleProgress>): Promise<UserModuleProgress> =>
    api.patch(`/learning/user-module-progress/?user=${userId}&module=${moduleId}`, data).then(res => res.data),

  // AI Code Review
  getAICodeReview: (submissionId: number): Promise<any> =>
    api.get(`/learning/ai-code-reviews/?submission=${submissionId}`).then(res => res.data),

  createAICodeReview: (data: any): Promise<any> =>
    api.post('/learning/ai-code-reviews/', data).then(res => res.data),

  // Test Cases
  getTestCases: (moduleId: number): Promise<any[]> =>
    api.get(`/learning/test-cases/?module=${moduleId}`).then(res => res.data),
};

  // Admin Analytics
  getLearningPathAnalytics: (pathId?: number): Promise<any> =>
    api.get(`/learning/admin/analytics/${pathId ? `?path_id=${pathId}` : ''}`).then(res => res.data),

  getCompletionTrends: (timeframe: 'week' | 'month' | 'quarter' | 'year' = 'month'): Promise<any[]> =>
    api.get(`/learning/admin/completion-trends/?timeframe=${timeframe}`).then(res => res.data),

  getUserJourneyAnalytics: (pathId: number): Promise<any> =>
    api.get(`/learning/admin/user-journey/?path_id=${pathId}`).then(res => res.data),

  getPerformanceInsights: (): Promise<any[]> =>
    api.get('/learning/admin/insights/').then(res => res.data),

  bulkUpdateLearningPaths: (pathIds: number[], updates: any): Promise<any> =>
    api.patch('/learning/learning-paths/bulk-update/', { path_ids: pathIds, updates }).then(res => res.data),

  reorderModules: (pathId: number, moduleOrder: number[]): Promise<any> =>
    api.post(`/learning/learning-paths/${pathId}/reorder-modules/`, { module_order: moduleOrder }).then(res => res.data),
};

export default api;