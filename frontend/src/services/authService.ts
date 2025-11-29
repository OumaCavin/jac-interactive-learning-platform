// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Authentication service - Real Django Backend Integration
 * 
 * IMPORTANT CHANGES:
 * - Mock authentication logic has been completely removed
 * - All authentication now uses real Django backend at http://localhost:8000
 * - Requires Django backend to be running for any authentication
 * 
 * REQUIREMENTS:
 * - Django backend must be accessible at REACT_APP_API_URL (default: http://localhost:8000/api)
 * - Users must be created through Django admin or registration endpoint
 * - JWT tokens must be valid and properly formatted
 * 
 * BACKEND ENDPOINTS USED:
 * - POST /users/auth/login/ - User authentication
 * - POST /users/auth/register/ - User registration  
 * - POST /users/auth/logout/ - User logout
 * - POST /users/auth/refresh/ - Token refresh
 * - GET /users/profile/ - Get user profile
 * - PUT /users/profile/ - Update user profile
 * - GET /users/health/ - Backend health check
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Types
export interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff?: boolean; // Admin/staff flag
  bio?: string;
  profile_image?: string;
  learning_style: 'visual' | 'auditory' | 'kinesthetic' | 'reading';
  preferred_difficulty: 'beginner' | 'intermediate' | 'advanced';
  learning_pace: 'slow' | 'moderate' | 'fast';
  total_modules_completed: number;
  total_time_spent: string; // Duration as string
  current_streak: number;
  longest_streak: number;
  total_points: number;
  level: number;
  experience_level: number;
  next_level_points: number;
  achievements: any[];
  badges: any[];
  current_goal?: string;
  goal_deadline?: string;
  agent_interaction_level: 'minimal' | 'moderate' | 'high';
  preferred_feedback_style: 'detailed' | 'brief' | 'encouraging';
  dark_mode: boolean;
  notifications_enabled: boolean;
  email_notifications: boolean;
  push_notifications: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  user: User;
  tokens: AuthTokens;
}

// Create axios instance with base configuration
const createApiClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request interceptor to add auth token
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor to handle token refresh
  client.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;

      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            const response = await axios.post(
              `${process.env.REACT_APP_API_URL}/users/auth/refresh/`,
              { refresh: refreshToken }
            );

            const { access } = response.data;
            localStorage.setItem('access_token', access);

            // Retry original request
            originalRequest.headers.Authorization = `Bearer ${access}`;
            return client(originalRequest);
          }
        } catch (refreshError) {
          // Refresh failed, redirect to login
          authService.logout();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );

  return client;
};

class AuthService {
  private apiClient: AxiosInstance;
  private currentUser: User | null = null;

  constructor() {
    this.apiClient = createApiClient();
    this.loadUserFromStorage();
  }

  /**
   * Load user from localStorage on service initialization
   */
  private loadUserFromStorage(): void {
    try {
      const userStr = localStorage.getItem('current_user');
      if (userStr) {
        // Validate JSON before parsing
        if (typeof userStr === 'string' && userStr.trim().length > 0) {
          this.currentUser = JSON.parse(userStr);
        }
      }
    } catch (error) {
      console.error('Failed to load user from storage:', error);
      // Clear potentially corrupted data
      localStorage.removeItem('current_user');
      localStorage.removeItem('token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }

  /**
   * Save user to localStorage
   */
  private saveUserToStorage(user: User): void {
    try {
      localStorage.setItem('current_user', JSON.stringify(user));
      this.currentUser = user;
    } catch (error) {
      console.error('Failed to save user to storage:', error);
    }
  }

  /**
   * Clear user from localStorage
   */
  private clearUserFromStorage(): void {
    localStorage.removeItem('current_user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.currentUser = null;
  }

  /**
   * Register a new user through Django backend
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    try {
      // Check backend connectivity first
      try {
        await this.apiClient.get('/users/health/');
      } catch (healthError) {
        throw new Error('Backend service is not available. Please ensure Django backend is running on port 8000.');
      }

      const response: AxiosResponse<AuthResponse> = await this.apiClient.post(
        '/users/auth/register/',
        data
      );

      const { user, tokens } = response.data;
      
      // Store tokens and user
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      this.saveUserToStorage(user);

      return response.data;
    } catch (error: any) {
      // Enhanced error handling for registration
      if (error.code === 'ECONNREFUSED') {
        throw new Error('Cannot connect to backend server. Please ensure Django backend is running at http://localhost:8000');
      }
      
      if (error.response?.status === 400) {
        const errors = error.response.data;
        if (errors.username) {
          throw new Error(`Username error: ${errors.username.join(', ')}`);
        }
        if (errors.email) {
          throw new Error(`Email error: ${errors.email.join(', ')}`);
        }
        if (errors.password) {
          throw new Error(`Password error: ${errors.password.join(', ')}`);
        }
        throw new Error(errors.message || 'Invalid registration data. Please check your input.');
      }
      
      if (error.response?.status >= 500) {
        throw new Error('Server error occurred during registration. Please try again later.');
      }
      
      throw new Error(error.response?.data?.message || 'Registration failed. Please check your data and try again.');
    }
  }

  /**
   * Login user - Real Django Backend Integration
   * 
   * NOTE: Mock logic has been removed. All authentication now uses the real Django backend.
   * Users must be registered in the Django admin or through the registration endpoint.
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // =================================================================
      // PRODUCTION BACKEND AUTHENTICATION
      // =================================================================
      // 
      // All authentication now uses the real Django backend API.
      // Users must be created through:
      // 1. Django admin panel at http://localhost:8000/admin/
      // 2. Frontend registration at http://localhost:3000/register
      // 3. API endpoint /users/auth/register/
      //
      // Required for authentication:
      // 1. Django backend running at http://localhost:8000
      // 2. Valid user account in the database
      // 3. JWT tokens from the backend API
      // =================================================================

      // Check backend connectivity first
      try {
        await this.apiClient.get('/users/health/');
      } catch (healthError) {
        throw new Error('Backend service is not available. Please ensure Django backend is running on port 8000.');
      }

      // Real API login to Django backend
      const response: AxiosResponse<AuthResponse> = await this.apiClient.post(
        '/users/auth/login/',
        credentials
      );

      const { user, tokens } = response.data;
      
      // Store tokens and user
      localStorage.setItem('token', tokens.access);
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
      this.saveUserToStorage(user);

      return response.data;
    } catch (error: any) {
      // Enhanced error handling for real backend scenarios
      if (error.code === 'ECONNREFUSED') {
        throw new Error('Cannot connect to backend server. Please ensure Django backend is running at http://localhost:8000');
      }
      
      if (error.response?.status === 401) {
        throw new Error('Invalid username or password. Please check your credentials.');
      }
      
      if (error.response?.status === 404) {
        throw new Error('Authentication endpoint not found. Please check if backend is properly configured.');
      }
      
      if (error.response?.status >= 500) {
        throw new Error('Server error occurred. Please try again later or contact support.');
      }
      
      if (error.response?.data?.non_field_errors) {
        throw new Error(error.response.data.non_field_errors.join(', '));
      }
      
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      }
      
      throw new Error(error.response?.data?.message || 'Login failed. Please check your credentials and ensure the backend is running.');
    }
  }

  /**
   * Check if Django backend is available and responsive
   */
  async checkBackendHealth(): Promise<boolean> {
    try {
      await this.apiClient.get('/users/health/', { timeout: 5000 });
      return true;
    } catch (error) {
      console.warn('Backend health check failed:', error);
      return false;
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          await this.apiClient.post('/users/auth/logout/', { refresh: refreshToken });
        } catch (apiError) {
          // Don't fail logout if backend call fails
          console.warn('Backend logout failed, continuing with local logout:', apiError);
        }
      }
    } catch (error) {
      console.error('Logout error:', error);
      // Don't let logout fail completely
    } finally {
      // Always clear local storage regardless of backend response
      this.clearUserFromStorage();
    }
  }

  /**
   * Check if user is authenticated
   * 
   * NOTE: Mock token checking has been removed. Only validates real JWT tokens.
   */
  isAuthenticated(): boolean {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      if (!token) return false;

      // =================================================================
      // MOCK TOKEN CHECKING REMOVED
      // =================================================================
      // Previously checked for tokens starting with 'mock-jwt-token-'
      // Now only validates real JWT tokens from Django backend
      // =================================================================
      
      // For real JWT tokens (decode to check expiration)
      const tokenParts = token.split('.');
      if (tokenParts.length === 3) {
        try {
          const payload = JSON.parse(atob(tokenParts[1]));
          const currentTime = Date.now() / 1000;
          return payload.exp > currentTime;
        } catch (decodeError) {
          console.warn('Failed to decode JWT token:', decodeError);
          // Clear invalid tokens
          this.clearUserFromStorage();
          return false;
        }
      }
      
      // Clear invalid token format
      this.clearUserFromStorage();
      return false;
    } catch (error) {
      console.error('Error checking authentication:', error);
      this.clearUserFromStorage();
      return false;
    }
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return this.currentUser;
  }

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<string> {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/users/auth/refresh/`,
        { refresh: refreshToken }
      );

      const { access } = response.data;
      localStorage.setItem('access_token', access);
      
      return access;
    } catch (error) {
      this.logout();
      throw error;
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response: AxiosResponse<{ user: User }> = await this.apiClient.put(
        '/users/profile/',
        userData
      );

      const { user } = response.data;
      this.saveUserToStorage(user);
      
      return user;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Profile update failed');
    }
  }

  /**
   * Get user settings
   */
  async getUserSettings(): Promise<any> {
    try {
      const response = await this.apiClient.get('/users/settings/');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to get settings');
    }
  }

  /**
   * Update user settings
   */
  async updateUserSettings(settings: any): Promise<void> {
    try {
      await this.apiClient.put('/users/settings/', settings);
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to update settings');
    }
  }

  /**
   * Get learning summary
   */
  async getLearningSummary(userId?: string): Promise<any> {
    try {
      const url = userId ? `/users/${userId}/learning-summary/` : '/users/learning-summary/';
      const response = await this.apiClient.get(url);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to get learning summary');
    }
  }

  /**
   * Get user statistics
   */
  async getUserStats(): Promise<any> {
    try {
      const response = await this.apiClient.get('/users/stats/');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to get user stats');
    }
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<void> {
    try {
      await this.apiClient.post('/auth/password-reset/', { email });
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Password reset request failed');
    }
  }

  /**
   * Reset password with token
   */
  async resetPassword(token: string, newPassword: string): Promise<void> {
    try {
      await this.apiClient.post('/auth/password-reset/confirm/', {
        token,
        password: newPassword,
      });
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Password reset failed');
    }
  }

  /**
   * Change password
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    try {
      await this.apiClient.post('/auth/password-change/', {
        current_password: currentPassword,
        new_password: newPassword,
      });
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Password change failed');
    }
  }

  /**
   * Get axios client instance (for other services to use)
   */
  getApiClient(): AxiosInstance {
    return this.apiClient;
  }
}

// Create singleton instance
export const authService = new AuthService();