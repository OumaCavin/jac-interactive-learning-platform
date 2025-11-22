/**
 * Authentication service
 * Handles user authentication, token management, and user session
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
   * Register a new user
   */
  async register(data: RegisterData): Promise<AuthResponse> {
    try {
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
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  /**
   * Login user
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      // Mock login for demo purposes
      if (credentials.username === 'demo@example.com' && credentials.password === 'demo123') {
        const mockUser: User = {
          id: '1',
          username: 'demo_user',
          email: credentials.username,
          first_name: 'Demo',
          last_name: 'User',
          bio: 'Demo user for JAC Learning Platform',
          profile_image: undefined,
          learning_style: 'visual',
          preferred_difficulty: 'beginner',
          learning_pace: 'moderate',
          total_modules_completed: 12,
          total_time_spent: '480 minutes',
          current_streak: 7,
          longest_streak: 14,
          total_points: 1250,
          level: 3,
          experience_level: 75,
          next_level_points: 1500,
          achievements: [],
          badges: [],
          current_goal: 'Complete JAC Fundamentals',
          goal_deadline: '2025-12-31',
          agent_interaction_level: 'moderate',
          preferred_feedback_style: 'detailed',
          dark_mode: false,
          notifications_enabled: true,
          email_notifications: true,
          push_notifications: false,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2025-11-21T21:24:42Z',
        };

        const mockTokens: AuthTokens = {
          access: 'mock-jwt-token-' + Date.now(),
          refresh: 'mock-refresh-token-' + Date.now(),
        };

        // Store tokens and user
        localStorage.setItem('token', mockTokens.access);
        localStorage.setItem('access_token', mockTokens.access);
        localStorage.setItem('refresh_token', mockTokens.refresh);
        this.saveUserToStorage(mockUser);

        return { user: mockUser, tokens: mockTokens };
      }

      // Real API login
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
      throw new Error(error.response?.data?.message || 'Login failed');
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
   */
  isAuthenticated(): boolean {
    try {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      if (!token) return false;

      // For mock tokens (simple check)
      if (token.startsWith('mock-jwt-token-')) {
        return true;
      }
      
      // For real JWT tokens (decode to check expiration)
      const tokenParts = token.split('.');
      if (tokenParts.length === 3) {
        try {
          const payload = JSON.parse(atob(tokenParts[1]));
          const currentTime = Date.now() / 1000;
          return payload.exp > currentTime;
        } catch (decodeError) {
          console.warn('Failed to decode JWT token:', decodeError);
          return false;
        }
      }
      
      return false;
    } catch (error) {
      console.error('Error checking authentication:', error);
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