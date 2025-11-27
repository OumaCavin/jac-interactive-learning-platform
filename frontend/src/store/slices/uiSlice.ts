// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * UI slice
 * Manages global UI state like theme, sidebar, loading states, etc.
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';

// Types for UI state
export interface UIState {
  // Theme
  theme: 'light' | 'dark' | 'system';
  
  // Layout
  sidebarOpen: boolean;
  sidebarCollapsed: boolean;
  
  // Loading states
  globalLoading: boolean;
  pageLoading: boolean;
  
  // Modals and overlays
  modals: {
    [key: string]: boolean;
  };
  
  // Notifications
  notifications: Array<{
    id: string;
    type: 'success' | 'error' | 'warning' | 'info';
    title: string;
    message?: string;
    timestamp: number;
  }>;
  
  // Breadcrumbs
  breadcrumbs: Array<{
    label: string;
    path?: string;
  }>;
  
  // Current page data
  currentPage: string;
  previousPage?: string;
  
  // Search
  searchQuery: string;
  searchActive: boolean;
  
  // Code editor
  codeEditorOpen: boolean;
  codeEditorSplitView: boolean;
  
  // Knowledge graph
  knowledgeGraphOpen: boolean;
  knowledgeGraphView: '2d' | '3d';
}

// Initial state
const initialState: UIState = {
  // Theme
  theme: 'system',
  
  // Layout
  sidebarOpen: true,
  sidebarCollapsed: false,
  
  // Loading states
  globalLoading: false,
  pageLoading: false,
  
  // Modals and overlays
  modals: {},
  
  // Notifications
  notifications: [],
  
  // Breadcrumbs
  breadcrumbs: [],
  
  // Current page
  currentPage: 'dashboard',
  
  // Search
  searchQuery: '',
  searchActive: false,
  
  // Code editor
  codeEditorOpen: false,
  codeEditorSplitView: false,
  
  // Knowledge graph
  knowledgeGraphOpen: false,
  knowledgeGraphView: '2d',
};

// UI slice
const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    // Theme actions
    setTheme: (state, action: PayloadAction<'light' | 'dark' | 'system'>) => {
      state.theme = action.payload;
    },
    toggleTheme: (state) => {
      state.theme = state.theme === 'dark' ? 'light' : 'dark';
    },
    
    // Layout actions
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarCollapsed: (state, action: PayloadAction<boolean>) => {
      state.sidebarCollapsed = action.payload;
    },
    toggleSidebarCollapsed: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
    },
    
    // Loading actions
    setGlobalLoading: (state, action: PayloadAction<boolean>) => {
      state.globalLoading = action.payload;
    },
    setPageLoading: (state, action: PayloadAction<boolean>) => {
      state.pageLoading = action.payload;
    },
    
    // Modal actions
    openModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = true;
    },
    closeModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = false;
    },
    closeAllModals: (state) => {
      Object.keys(state.modals).forEach(key => {
        state.modals[key] = false;
      });
    },
    
    // Notification actions
    addNotification: (state, action: PayloadAction<{
      type: 'success' | 'error' | 'warning' | 'info';
      title: string;
      message?: string;
    }>) => {
      const notification = {
        id: Date.now().toString(),
        timestamp: Date.now(),
        ...action.payload,
      };
      state.notifications.push(notification);
      
      // Keep only last 10 notifications
      if (state.notifications.length > 10) {
        state.notifications.shift();
      }
    },
    removeNotification: (state, action: PayloadAction<string>) => {
      state.notifications = state.notifications.filter(
        notification => notification.id !== action.payload
      );
    },
    clearAllNotifications: (state) => {
      state.notifications = [];
    },
    
    // Breadcrumb actions
    setBreadcrumbs: (state, action: PayloadAction<Array<{
      label: string;
      path?: string;
    }>>) => {
      state.breadcrumbs = action.payload;
    },
    addBreadcrumb: (state, action: PayloadAction<{
      label: string;
      path?: string;
    }>) => {
      state.breadcrumbs.push(action.payload);
    },
    clearBreadcrumbs: (state) => {
      state.breadcrumbs = [];
    },
    
    // Page actions
    setCurrentPage: (state, action: PayloadAction<string>) => {
      state.previousPage = state.currentPage;
      state.currentPage = action.payload;
    },
    goToPreviousPage: (state) => {
      if (state.previousPage) {
        state.currentPage = state.previousPage;
        state.previousPage = undefined;
      }
    },
    
    // Search actions
    setSearchQuery: (state, action: PayloadAction<string>) => {
      state.searchQuery = action.payload;
    },
    setSearchActive: (state, action: PayloadAction<boolean>) => {
      state.searchActive = action.payload;
    },
    clearSearch: (state) => {
      state.searchQuery = '';
      state.searchActive = false;
    },
    
    // Code editor actions
    setCodeEditorOpen: (state, action: PayloadAction<boolean>) => {
      state.codeEditorOpen = action.payload;
    },
    toggleCodeEditor: (state) => {
      state.codeEditorOpen = !state.codeEditorOpen;
    },
    setCodeEditorSplitView: (state, action: PayloadAction<boolean>) => {
      state.codeEditorSplitView = action.payload;
    },
    toggleCodeEditorSplitView: (state) => {
      state.codeEditorSplitView = !state.codeEditorSplitView;
    },
    
    // Knowledge graph actions
    setKnowledgeGraphOpen: (state, action: PayloadAction<boolean>) => {
      state.knowledgeGraphOpen = action.payload;
    },
    toggleKnowledgeGraph: (state) => {
      state.knowledgeGraphOpen = !state.knowledgeGraphOpen;
    },
    setKnowledgeGraphView: (state, action: PayloadAction<'2d' | '3d'>) => {
      state.knowledgeGraphView = action.payload;
    },
    
    // Reset UI state
    resetUI: (state) => {
      state.globalLoading = false;
      state.pageLoading = false;
      state.modals = {};
      state.notifications = [];
      state.breadcrumbs = [];
      state.searchQuery = '';
      state.searchActive = false;
      state.codeEditorOpen = false;
      state.knowledgeGraphOpen = false;
    },
  },
});

// Export actions
export const {
  // Theme
  setTheme,
  toggleTheme,
  
  // Layout
  setSidebarOpen,
  toggleSidebar,
  setSidebarCollapsed,
  toggleSidebarCollapsed,
  
  // Loading
  setGlobalLoading,
  setPageLoading,
  
  // Modals
  openModal,
  closeModal,
  closeAllModals,
  
  // Notifications
  addNotification,
  removeNotification,
  clearAllNotifications,
  
  // Breadcrumbs
  setBreadcrumbs,
  addBreadcrumb,
  clearBreadcrumbs,
  
  // Pages
  setCurrentPage,
  goToPreviousPage,
  
  // Search
  setSearchQuery,
  setSearchActive,
  clearSearch,
  
  // Code editor
  setCodeEditorOpen,
  toggleCodeEditor,
  setCodeEditorSplitView,
  toggleCodeEditorSplitView,
  
  // Knowledge graph
  setKnowledgeGraphOpen,
  toggleKnowledgeGraph,
  setKnowledgeGraphView,
  
  // Reset
  resetUI,
} = uiSlice.actions;

// Selectors
export const selectUI = (state: { ui: UIState }) => state.ui;
export const selectTheme = (state: { ui: UIState }) => state.ui.theme;
export const selectSidebarOpen = (state: { ui: UIState }) => state.ui.sidebarOpen;
export const selectSidebarCollapsed = (state: { ui: UIState }) => state.ui.sidebarCollapsed;
export const selectGlobalLoading = (state: { ui: UIState }) => state.ui.globalLoading;
export const selectPageLoading = (state: { ui: UIState }) => state.ui.pageLoading;
export const selectCurrentPage = (state: { ui: UIState }) => state.ui.currentPage;
export const selectBreadcrumbs = (state: { ui: UIState }) => state.ui.breadcrumbs;
export const selectSearchQuery = (state: { ui: UIState }) => state.ui.searchQuery;
export const selectSearchActive = (state: { ui: UIState }) => state.ui.searchActive;
export const selectCodeEditorOpen = (state: { ui: UIState }) => state.ui.codeEditorOpen;
export const selectKnowledgeGraphOpen = (state: { ui: UIState }) => state.ui.knowledgeGraphOpen;

// Export reducer
export default uiSlice.reducer;