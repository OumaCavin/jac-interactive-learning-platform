/**
 * Search Redux Slice
 * Manages search state in the Redux store
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import searchService, { SearchResponse, SearchResult } from '../../services/searchService';

// Search State Interface
interface SearchState {
  // Current search
  currentQuery: string;
  results: SearchResult[];
  totalResults: number;
  isLoading: boolean;
  error: string | null;
  
  // Search history
  history: string[];
  
  // Suggestions
  suggestions: string[];
  showSuggestions: boolean;
  
  // Popular searches
  popularSearches: string[];
  trendingSearches: string[];
  
  // UI state
  isSearchOpen: boolean;
  selectedFilter: string | null;
}

// Initial State
const initialState: SearchState = {
  currentQuery: '',
  results: [],
  totalResults: 0,
  isLoading: false,
  error: null,
  history: [],
  suggestions: [],
  showSuggestions: false,
  popularSearches: [],
  trendingSearches: [],
  isSearchOpen: false,
  selectedFilter: null,
};

// Async Thunks
export const performSearch = createAsyncThunk(
  'search/performSearch',
  async (query: string, { rejectWithValue }) => {
    try {
      const response = await searchService.search({ query, limit: 20 });
      return response;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Search failed');
    }
  }
);

export const fetchSuggestions = createAsyncThunk(
  'search/fetchSuggestions',
  async (query: string, { rejectWithValue }) => {
    try {
      const suggestions = await searchService.getSuggestions(query);
      return suggestions;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch suggestions');
    }
  }
);

export const fetchPopularSearches = createAsyncThunk(
  'search/fetchPopularSearches',
  async (_, { rejectWithValue }) => {
    try {
      const searches = await searchService.getPopularSearches();
      return searches;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch popular searches');
    }
  }
);

export const fetchTrendingSearches = createAsyncThunk(
  'search/fetchTrendingSearches',
  async (_, { rejectWithValue }) => {
    try {
      const searches = await searchService.getTrendingSearches();
      return searches;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch trending searches');
    }
  }
);

export const trackSearchResultClick = createAsyncThunk(
  'search/trackResultClick',
  async ({ query, url }: { query: string; url: string }, { rejectWithValue }) => {
    try {
      await searchService.trackClick(query, url);
      return { query, url };
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to track click');
    }
  }
);

// Search Slice
const searchSlice = createSlice({
  name: 'search',
  initialState,
  reducers: {
    // Update current query
    setCurrentQuery: (state, action: PayloadAction<string>) => {
      state.currentQuery = action.payload;
    },
    
    // Update search results
    setSearchResults: (state, action: PayloadAction<SearchResponse>) => {
      state.results = action.payload.results;
      state.totalResults = action.payload.total_results;
    },
    
    // Clear search results
    clearSearchResults: (state) => {
      state.results = [];
      state.totalResults = 0;
      state.currentQuery = '';
      state.error = null;
    },
    
    // Update loading state
    setSearchLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    
    // Update error state
    setSearchError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    
    // Add to search history
    addToHistory: (state, action: PayloadAction<string>) => {
      const query = action.payload.trim();
      if (query && !state.history.includes(query)) {
        state.history.unshift(query);
        // Keep only last 10 searches
        state.history = state.history.slice(0, 10);
      }
    },
    
    // Clear search history
    clearSearchHistory: (state) => {
      state.history = [];
    },
    
    // Update suggestions
    setSuggestions: (state, action: PayloadAction<string[]>) => {
      state.suggestions = action.payload;
    },
    
    // Show/hide suggestions
    setShowSuggestions: (state, action: PayloadAction<boolean>) => {
      state.showSuggestions = action.payload;
    },
    
    // Toggle search panel
    toggleSearchPanel: (state) => {
      state.isSearchOpen = !state.isSearchOpen;
    },
    
    // Set selected filter
    setSelectedFilter: (state, action: PayloadAction<string | null>) => {
      state.selectedFilter = action.payload;
    },
    
    // Set popular searches
    setPopularSearches: (state, action: PayloadAction<string[]>) => {
      state.popularSearches = action.payload;
    },
    
    // Set trending searches
    setTrendingSearches: (state, action: PayloadAction<string[]>) => {
      state.trendingSearches = action.payload;
    },
    
    // Reset search state
    resetSearchState: (state) => {
      return { ...initialState };
    }
  },
  extraReducers: (builder) => {
    // Perform Search
    builder
      .addCase(performSearch.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(performSearch.fulfilled, (state, action) => {
        state.isLoading = false;
        state.results = action.payload.results;
        state.totalResults = action.payload.total_results;
        
        // Add to history
        if (state.currentQuery.trim()) {
          const query = state.currentQuery.trim();
          if (!state.history.includes(query)) {
            state.history.unshift(query);
            state.history = state.history.slice(0, 10);
          }
        }
      })
      .addCase(performSearch.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.results = [];
        state.totalResults = 0;
      });
    
    // Fetch Suggestions
    builder
      .addCase(fetchSuggestions.fulfilled, (state, action) => {
        state.suggestions = action.payload;
      })
      .addCase(fetchSuggestions.rejected, (state, action) => {
        console.error('Failed to fetch suggestions:', action.payload);
      });
    
    // Fetch Popular Searches
    builder
      .addCase(fetchPopularSearches.fulfilled, (state, action) => {
        state.popularSearches = action.payload;
      })
      .addCase(fetchPopularSearches.rejected, (state, action) => {
        console.error('Failed to fetch popular searches:', action.payload);
      });
    
    // Fetch Trending Searches
    builder
      .addCase(fetchTrendingSearches.fulfilled, (state, action) => {
        state.trendingSearches = action.payload;
      })
      .addCase(fetchTrendingSearches.rejected, (state, action) => {
        console.error('Failed to fetch trending searches:', action.payload);
      });
  },
});

// Export actions
export const {
  setCurrentQuery,
  setSearchResults,
  clearSearchResults,
  setSearchLoading,
  setSearchError,
  addToHistory,
  clearSearchHistory,
  setSuggestions,
  setShowSuggestions,
  toggleSearchPanel,
  setSelectedFilter,
  setPopularSearches,
  setTrendingSearches,
  resetSearchState
} = searchSlice.actions;

// Selectors
export const selectSearch = (state: any) => state.search;
export const selectCurrentQuery = (state: any) => state.search.currentQuery;
export const selectSearchResults = (state: any) => state.search.results;
export const selectSearchLoading = (state: any) => state.search.isLoading;
export const selectSearchError = (state: any) => state.search.error;
export const selectSearchHistory = (state: any) => state.search.history;
export const selectSearchSuggestions = (state: any) => state.search.suggestions;
export const selectShowSuggestions = (state: any) => state.search.showSuggestions;
export const selectPopularSearches = (state: any) => state.search.popularSearches;
export const selectTrendingSearches = (state: any) => state.search.trendingSearches;
export const selectIsSearchOpen = (state: any) => state.search.isSearchOpen;
export const selectTotalResults = (state: any) => state.search.totalResults;

// Export reducer
export default searchSlice.reducer;