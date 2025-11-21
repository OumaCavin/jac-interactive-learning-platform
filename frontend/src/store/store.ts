/**
 * Redux store configuration
 * Centralized state management for the application
 */

import { configureStore } from '@reduxjs/toolkit';
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';

// Import reducers
import authReducer from './slices/authSlice';
import uiReducer from './slices/uiSlice';
import learningReducer from './slices/learningSlice';
import assessmentReducer from './slices/assessmentSlice';
import agentReducer from './slices/agentSlice';

// Configure the Redux store
export const store = configureStore({
  reducer: {
    auth: authReducer,
    ui: uiReducer,
    learning: learningReducer,
    assessments: assessmentReducer,
    agents: agentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types for serialization check
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
        // Ignore these field paths in all actions
        ignoredActionsPaths: ['meta.arg', 'payload.timestamp'],
        // Ignore these paths in the state
        ignoredPaths: ['items.dates'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
});

// Export store types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks for using Redux throughout the app
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;