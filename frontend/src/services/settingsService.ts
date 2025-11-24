/**
 * Settings service
 * Handles user settings management through the UserSettingsView API
 */

import { AxiosInstance } from 'axios';
import { apiClient } from './apiClient';
import { User } from './authService';

// Settings-specific interfaces
export interface UserSettings {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  bio?: string;
  learning_style: 'visual' | 'auditory' | 'kinesthetic' | 'reading';
  preferred_difficulty: 'beginner' | 'intermediate' | 'advanced';
  learning_pace: 'slow' | 'moderate' | 'fast';
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

export interface UpdateSettingsData {
  first_name?: string;
  last_name?: string;
  email?: string;
  bio?: string;
  learning_style?: 'visual' | 'auditory' | 'kinesthetic' | 'reading';
  preferred_difficulty?: 'beginner' | 'intermediate' | 'advanced';
  learning_pace?: 'slow' | 'moderate' | 'fast';
  current_goal?: string;
  goal_deadline?: string;
  agent_interaction_level?: 'minimal' | 'moderate' | 'high';
  preferred_feedback_style?: 'detailed' | 'brief' | 'encouraging';
  dark_mode?: boolean;
  notifications_enabled?: boolean;
  email_notifications?: boolean;
  push_notifications?: boolean;
}

export interface SettingsUpdateResponse {
  success: boolean;
  message: string;
  data: UserSettings;
}

class SettingsService {
  private baseURL = '/api/users/settings';
  private readonly apiClient: AxiosInstance = apiClient;

  /**
   * Get user settings from the backend
   */
  async getUserSettings(): Promise<UserSettings> {
    try {
      const response = await this.apiClient.get<UserSettings>(this.baseURL);
      return response.data;
    } catch (error: any) {
      console.error('Failed to fetch user settings:', error);
      
      if (error.response?.status === 401) {
        throw new Error('Authentication required. Please log in again.');
      } else if (error.response?.status === 404) {
        throw new Error('Settings not found. Please try again.');
      } else if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else {
        throw new Error('Failed to load settings. Please check your connection.');
      }
    }
  }

  /**
   * Update user settings
   */
  async updateUserSettings(settingsData: UpdateSettingsData): Promise<UserSettings> {
    try {
      const response = await this.apiClient.put<UserSettings>(this.baseURL, settingsData);
      return response.data;
    } catch (error: any) {
      console.error('Failed to update user settings:', error);
      
      if (error.response?.status === 401) {
        throw new Error('Authentication required. Please log in again.');
      } else if (error.response?.status === 403) {
        throw new Error('You do not have permission to update these settings.');
      } else if (error.response?.status === 400) {
        // Handle validation errors
        const validationErrors = error.response.data;
        if (typeof validationErrors === 'object' && validationErrors !== null) {
          const errorMessages = Object.entries(validationErrors)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('; ');
          throw new Error(`Validation failed: ${errorMessages}`);
        }
        throw new Error('Invalid data provided. Please check your inputs.');
      } else if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else {
        throw new Error('Failed to save settings. Please try again.');
      }
    }
  }

  /**
   * Batch update multiple settings at once
   */
  async updateMultipleSettings(settingsData: UpdateSettingsData): Promise<UserSettings> {
    return this.updateUserSettings(settingsData);
  }

  /**
   * Update a single setting field
   */
  async updateSingleSetting(field: keyof UpdateSettingsData, value: any): Promise<UserSettings> {
    const settingsData: UpdateSettingsData = {
      [field]: value
    } as UpdateSettingsData;
    
    return this.updateUserSettings(settingsData);
  }

  /**
   * Reset settings to defaults (server-side defaults)
   */
  async resetToDefaults(): Promise<UserSettings> {
    try {
      const response = await this.apiClient.patch<UserSettings>(`${this.baseURL}/reset`);
      return response.data;
    } catch (error: any) {
      console.error('Failed to reset settings to defaults:', error);
      
      if (error.response?.status === 401) {
        throw new Error('Authentication required. Please log in again.');
      } else if (error.response?.status === 404) {
        throw new Error('Settings not found.');
      } else if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else {
        throw new Error('Failed to reset settings. Please try again.');
      }
    }
  }

  /**
   * Validate settings data before submission
   */
  validateSettingsData(settingsData: UpdateSettingsData): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Email validation
    if (settingsData.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(settingsData.email)) {
        errors.push('Please provide a valid email address.');
      }
    }

    // Goal deadline validation
    if (settingsData.goal_deadline) {
      const deadlineDate = new Date(settingsData.goal_deadline);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      if (deadlineDate < today) {
        errors.push('Goal deadline cannot be in the past.');
      }
    }

    // Bio length validation
    if (settingsData.bio && settingsData.bio.length > 500) {
      errors.push('Bio cannot exceed 500 characters.');
    }

    // Goal length validation
    if (settingsData.current_goal && settingsData.current_goal.length > 200) {
      errors.push('Current goal cannot exceed 200 characters.');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  /**
   * Get default settings values
   */
  getDefaultSettings(): Omit<UserSettings, 'id' | 'username' | 'email' | 'created_at' | 'updated_at'> {
    return {
      first_name: '',
      last_name: '',
      bio: '',
      learning_style: 'visual',
      preferred_difficulty: 'beginner',
      learning_pace: 'moderate',
      current_goal: '',
      goal_deadline: '',
      agent_interaction_level: 'moderate',
      preferred_feedback_style: 'detailed',
      dark_mode: true,
      notifications_enabled: true,
      email_notifications: true,
      push_notifications: true,
    };
  }

  /**
   * Convert User interface to UserSettings interface
   */
  userToSettings(user: User): UserSettings {
    return {
      id: user.id,
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      bio: user.bio,
      learning_style: user.learning_style,
      preferred_difficulty: user.preferred_difficulty,
      learning_pace: user.learning_pace,
      current_goal: user.current_goal,
      goal_deadline: user.goal_deadline,
      agent_interaction_level: user.agent_interaction_level,
      preferred_feedback_style: user.preferred_feedback_style,
      dark_mode: user.dark_mode,
      notifications_enabled: user.notifications_enabled,
      email_notifications: user.email_notifications,
      push_notifications: user.push_notifications,
      created_at: user.created_at,
      updated_at: user.updated_at,
    };
  }
}

// Export singleton instance
export const settingsService = new SettingsService();
export default settingsService;