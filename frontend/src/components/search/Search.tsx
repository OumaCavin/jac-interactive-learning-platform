/**
 * Search Component
 * Comprehensive search interface with autocomplete and results display
 */

import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon, 
  XMarkIcon,
  ClockIcon,
  ArrowTrendingUpIcon as TrendingUpIcon,
  FireIcon
} from '@heroicons/react/24/outline';
import { useDispatch, useSelector } from 'react-redux';

import { 
  performSearch, 
  fetchSuggestions, 
  fetchPopularSearches, 
  fetchTrendingSearches,
  setCurrentQuery, 
  setShowSuggestions,
  trackSearchResultClick,
  selectSearch,
  selectCurrentQuery,
  selectShowSuggestions,
  selectSearchSuggestions,
  selectSearchHistory,
  selectPopularSearches,
  selectTrendingSearches
} from '../../store/slices/searchSlice';
import { AppDispatch } from '../../store/store';
import searchService from '../../services/searchService';

// Search Component Props
interface SearchProps {
  className?: string;
  placeholder?: string;
  onResultClick?: (result: any) => void;
  showResults?: boolean;
  fullWidth?: boolean;
}

// Main Search Component
export const Search: React.FC<SearchProps> = ({
  className = '',
  placeholder = 'Search learning paths, modules...',
  onResultClick,
  showResults = true,
  fullWidth = false
}) => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  
  // Redux selectors
  const {
    currentQuery,
    results,
    isLoading,
    history,
    popularSearches,
    trendingSearches,
    showSuggestions
  } = useSelector(selectSearch);
  
  const suggestions = useSelector(selectSearchSuggestions);
  const searchHistory = useSelector(selectSearchHistory);
  
  // Component state
  const [localQuery, setLocalQuery] = useState('');
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  // Refs
  const searchInputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchTimeoutRef = useRef<NodeJS.Timeout>();
  
  // Initialize search data
  useEffect(() => {
    dispatch(fetchPopularSearches());
    dispatch(fetchTrendingSearches());
  }, [dispatch]);
  
  // Handle input change with debounced suggestions
  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setLocalQuery(query);
    dispatch(setCurrentQuery(query));
    
    // Clear previous timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    // Fetch suggestions for non-empty queries
    if (query.trim().length >= 2) {
      dispatch(fetchSuggestions(query));
      setShowDropdown(true);
    } else {
      setShowDropdown(false);
    }
    
    // Debounced search
    if (query.trim()) {
      searchTimeoutRef.current = setTimeout(() => {
        dispatch(performSearch(query));
      }, 300);
    }
  }, [dispatch]);
  
  // Handle key navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (!showDropdown && !showSuggestions) return;
    
    const totalItems = suggestions.length + history.length + popularSearches.length;
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % totalItems);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev <= 0 ? totalItems - 1 : prev - 1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0) {
          const item = getItemAtIndex(selectedIndex);
          if (item) {
            handleItemClick(item.type, item.value);
          }
        } else {
          handleSearch(localQuery);
        }
        break;
      case 'Escape':
        setShowDropdown(false);
        setSelectedIndex(-1);
        searchInputRef.current?.blur();
        break;
    }
  }, [selectedIndex, suggestions, history, popularSearches, localQuery]);
  
  // Handle search submission
  const handleSearch = useCallback((query: string) => {
    if (!query.trim()) return;
    
    // Perform search
    dispatch(performSearch(query));
    
    // Close dropdown
    setShowDropdown(false);
    setSelectedIndex(-1);
    
    // Navigate to search results page if not already there
    if (!onResultClick) {
      navigate(`/search?q=${encodeURIComponent(query)}`);
    }
    
    // Call optional callback
    if (onResultClick) {
      onResultClick({ query, type: 'search' });
    }
  }, [dispatch, navigate, onResultClick]);
  
  // Handle dropdown item click
  const handleItemClick = useCallback((type: string, value: string) => {
    switch (type) {
      case 'suggestion':
      case 'history':
      case 'popular':
        setLocalQuery(value);
        dispatch(setCurrentQuery(value));
        handleSearch(value);
        break;
      case 'result':
        // Handle result click
        if (onResultClick) {
          onResultClick({ type: 'result', value });
        }
        break;
    }
  }, [dispatch, handleSearch, onResultClick]);
  
  // Track result click
  const handleResultClick = useCallback((result: any) => {
    dispatch(trackSearchResultClick({ query: currentQuery, url: result.url }));
    
    if (onResultClick) {
      onResultClick(result);
    } else {
      navigate(result.url);
    }
  }, [dispatch, currentQuery, onResultClick, navigate]);
  
  // Get item at index for keyboard navigation
  const getItemAtIndex = (index: number) => {
    if (index < suggestions.length) {
      return { type: 'suggestion', value: suggestions[index] };
    }
    
    const historyStart = suggestions.length;
    if (index < historyStart + searchHistory.length) {
      return { type: 'history', value: searchHistory[index - historyStart] };
    }
    
    const popularStart = historyStart + searchHistory.length;
    if (index < popularStart + popularSearches.length) {
      return { type: 'popular', value: popularSearches[index - popularStart] };
    }
    
    return null;
  };
  
  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
        setSelectedIndex(-1);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);
  
  // Clean up timeout on unmount
  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  return (
    <div className={`relative ${fullWidth ? 'w-full' : 'max-w-lg'} ${className}`}>
      {/* Search Input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        
        <input
          ref={searchInputRef}
          type="text"
          value={localQuery}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => {
            if (localQuery.trim()) {
              setShowDropdown(true);
            }
          }}
          placeholder={placeholder}
          className={`
            block w-full border-0 py-0 pl-10 pr-12 text-gray-900 placeholder:text-gray-400 
            focus:ring-0 sm:text-sm bg-white rounded-md shadow-sm border border-gray-200
            focus:border-primary-500 focus:ring-2 focus:ring-primary-500 focus:ring-opacity-20
            transition-all duration-200
          `}
        />
        
        {/* Clear button */}
        {localQuery && (
          <button
            type="button"
            onClick={() => {
              setLocalQuery('');
              dispatch(setCurrentQuery(''));
              setShowDropdown(false);
              searchInputRef.current?.focus();
            }}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        )}
      </div>

      {/* Search Dropdown */}
      <AnimatePresence>
        {showDropdown && (
          <motion.div
            ref={dropdownRef}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-50 mt-2 w-full bg-white rounded-md shadow-lg border border-gray-200 max-h-96 overflow-y-auto"
          >
            {/* Loading indicator */}
            {isLoading && (
              <div className="px-4 py-2 text-sm text-gray-500 border-b border-gray-100">
                Searching...
              </div>
            )}
            
            {/* Search Results */}
            {showResults && results.length > 0 && (
              <div className="p-2">
                <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  Results ({results.length})
                </div>
                {results.slice(0, 5).map((result, index) => (
                  <button
                    key={`result-${result.id}`}
                    onClick={() => handleResultClick(result)}
                    className={`
                      w-full text-left px-3 py-2 text-sm rounded-md transition-colors
                      hover:bg-gray-50 focus:bg-gray-50 focus:outline-none
                      ${selectedIndex === index ? 'bg-gray-50' : ''}
                    `}
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-lg">{searchService.getContentTypeIcon(result.content_type)}</span>
                      <div className="flex-1 min-w-0">
                        <p 
                          className="font-medium text-gray-900 truncate"
                          dangerouslySetInnerHTML={{
                            __html: searchService.highlightSearchTerms(result.title, localQuery)
                          }}
                        />
                        <p 
                          className="text-gray-500 text-xs truncate"
                          dangerouslySetInnerHTML={{
                            __html: searchService.highlightSearchTerms(result.description, localQuery)
                          }}
                        />
                        <span className="text-xs text-gray-400">
                          {searchService.formatContentType(result.content_type)}
                        </span>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            )}
            
            {/* Search Suggestions */}
            {!isLoading && (suggestions.length > 0 || searchHistory.length > 0 || popularSearches.length > 0) && (
              <div className="p-2 border-t border-gray-100">
                {/* Suggestions */}
                {suggestions.length > 0 && (
                  <div className="mb-3">
                    <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center">
                      <FireIcon className="h-3 w-3 mr-1" />
                      Suggestions
                    </div>
                    {suggestions.map((suggestion, index) => (
                      <button
                        key={`suggestion-${index}`}
                        onClick={() => handleItemClick('suggestion', suggestion)}
                        className={`
                          w-full text-left px-3 py-2 text-sm text-gray-700 rounded-md transition-colors
                          hover:bg-gray-50 focus:bg-gray-50 focus:outline-none
                          ${selectedIndex === index ? 'bg-gray-50' : ''}
                        `}
                      >
                        <div className="flex items-center">
                          <MagnifyingGlassIcon className="h-4 w-4 mr-2 text-gray-400" />
                          <span dangerouslySetInnerHTML={{
                            __html: searchService.highlightSearchTerms(suggestion, localQuery)
                          }} />
                        </div>
                      </button>
                    ))}
                  </div>
                )}
                
                {/* Search History */}
                {searchHistory.length > 0 && (
                  <div className="mb-3">
                    <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center">
                      <ClockIcon className="h-3 w-3 mr-1" />
                      Recent
                    </div>
                    {searchHistory.slice(0, 3).map((historyItem, index) => {
                      const historyIndex = suggestions.length + index;
                      return (
                        <button
                          key={`history-${index}`}
                          onClick={() => handleItemClick('history', historyItem)}
                          className={`
                            w-full text-left px-3 py-2 text-sm text-gray-700 rounded-md transition-colors
                            hover:bg-gray-50 focus:bg-gray-50 focus:outline-none
                            ${selectedIndex === historyIndex ? 'bg-gray-50' : ''}
                          `}
                        >
                          <div className="flex items-center">
                            <ClockIcon className="h-4 w-4 mr-2 text-gray-400" />
                            {historyItem}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
                
                {/* Popular Searches */}
                {popularSearches.length > 0 && (
                  <div>
                    <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center">
                      <TrendingUpIcon className="h-3 w-3 mr-1" />
                      Popular
                    </div>
                    {popularSearches.slice(0, 3).map((popularItem, index) => {
                      const popularIndex = suggestions.length + searchHistory.length + index;
                      return (
                        <button
                          key={`popular-${index}`}
                          onClick={() => handleItemClick('popular', popularItem)}
                          className={`
                            w-full text-left px-3 py-2 text-sm text-gray-700 rounded-md transition-colors
                            hover:bg-gray-50 focus:bg-gray-50 focus:outline-none
                            ${selectedIndex === popularIndex ? 'bg-gray-50' : ''}
                          `}
                        >
                          <div className="flex items-center">
                            <TrendingUpIcon className="h-4 w-4 mr-2 text-gray-400" />
                            {popularItem}
                          </div>
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
            
            {/* No results */}
            {!isLoading && !results.length && !suggestions.length && localQuery.trim() && (
              <div className="px-4 py-3 text-sm text-gray-500 text-center">
                No results found for "{localQuery}"
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Search;