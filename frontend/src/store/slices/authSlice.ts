// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Authentication slice
 * Manages authentication state, user data, and login/logout functionality
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { authService, User, LoginCredentials, RegisterData } from '../../services/authService';
// Note: Notification hooks removed to avoid unused import warnings
// import { useSuccessNotification, useErrorNotification } from '../../components/ui/NotificationProvider';

// Types for auth state
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  tokens: {
    access: string | null;
    refresh: string | null;
  };
}

// Initial state
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  tokens: {
    access: null,
    refresh: null,
  },
};

// Async thunks
export const loginUser = createAsyncThunk(
  'auth/login',
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const response = await authService.login(credentials);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Login failed');
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/register',
  async (data: RegisterData, { rejectWithValue }) => {
    try {
      const response = await authService.register(data);
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Registration failed');
    }
  }
);

export const logoutUser = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      await authService.logout();
      return;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Logout failed');
    }
  }
);

export const updateProfile = createAsyncThunk(
  'auth/updateProfile',
  async (userData: Partial<User>, { rejectWithValue }) => {
    try {
      const updatedUser = await authService.updateProfile(userData);
      return updatedUser;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Profile update failed');
    }
  }
);

export const getUserStats = createAsyncThunk(
  'auth/getUserStats',
  async (_, { rejectWithValue }) => {
    try {
      const stats = await authService.getUserStats();
      return stats;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to get user stats');
    }
  }
);

export const refreshAuthToken = createAsyncThunk(
  'auth/refreshToken',
  async (_, { rejectWithValue }) => {
    try {
      const token = await authService.refreshToken();
      return token;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Token refresh failed');
    }
  }
);

// Auth slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    clearAuth: (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.tokens = { access: null, refresh: null };
    },
    updateUserProgress: (state, action: PayloadAction<{ 
      totalModulesCompleted?: number; 
      totalTimeSpent?: string;
      currentStreak?: number;
      totalPoints?: number;
      level?: number;
    }>) => {
      if (state.user) {
        Object.assign(state.user, action.payload);
      }
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
        state.tokens = action.payload.tokens;
        state.error = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.isAuthenticated = false;
        state.user = null;
      });

    // Register
    builder
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.isAuthenticated = true;
        state.tokens = action.payload.tokens;
        state.error = null;
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.isAuthenticated = false;
        state.user = null;
      });

    // Logout
    builder
      .addCase(logoutUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(logoutUser.fulfilled, (state) => {
        state.isLoading = false;
        state.user = null;
        state.isAuthenticated = false;
        state.tokens = { access: null, refresh: null };
        state.error = null;
      })
      .addCase(logoutUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        // Still clear auth state even if logout request failed
        state.user = null;
        state.isAuthenticated = false;
        state.tokens = { access: null, refresh: null };
      });

    // Update profile
    builder
      .addCase(updateProfile.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.error = null;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Get user stats
    builder
      .addCase(getUserStats.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getUserStats.fulfilled, (state, action) => {
        state.isLoading = false;
        // Update user stats in the user object
        if (state.user) {
          Object.assign(state.user, action.payload);
        }
      })
      .addCase(getUserStats.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Refresh token
    builder
      .addCase(refreshAuthToken.fulfilled, (state, action) => {
        state.tokens.access = action.payload;
      })
      .addCase(refreshAuthToken.rejected, (state) => {
        // If refresh fails, clear auth state
        state.user = null;
        state.isAuthenticated = false;
        state.tokens = { access: null, refresh: null };
      });
  },
});

// Export actions
export const { 
  clearError, 
  setUser, 
  clearAuth, 
  updateUserProgress 
} = authSlice.actions;

// Selectors
export const selectAuth = (state: { auth: AuthState }) => state.auth;
export const selectUser = (state: { auth: AuthState }) => state.auth.user;
export const selectIsAuthenticated = (state: { auth: AuthState }) => state.auth.isAuthenticated;
export const selectIsLoading = (state: { auth: AuthState }) => state.auth.isLoading;
export const selectError = (state: { auth: AuthState }) => state.auth.error;
export const selectTokens = (state: { auth: AuthState }) => state.auth.tokens;

// Export reducer
export default authSlice.reducer;