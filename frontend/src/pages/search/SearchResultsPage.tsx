/**
 * Search Results Page
 * Displays comprehensive search results with filtering and sorting
 */

import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  MagnifyingGlassIcon,
  FunnelIcon,
  AdjustmentsHorizontalIcon,
  ClockIcon,
  TrendingUpIcon,
  BookOpenIcon,
  AcademicCapIcon,
  ChartBarIcon,
  UserIcon,
  DocumentTextIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import { useDispatch, useSelector } from 'react-redux';

import { 
  performSearch, 
  setCurrentQuery, 
  clearSearchResults,
  selectSearch,
  selectCurrentQuery,
  selectSearchResults,
  selectSearchLoading,
  selectTotalResults
} from '../../store/slices/searchSlice';
import { AppDispatch } from '../../store/store';
import searchService from '../../services/searchService';

interface FilterOption {
  key: string;
  label: string;
  icon: React.ComponentType<any>;
  count?: number;
}

const SearchResultsPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Redux selectors
  const { 
    results, 
    isLoading, 
    totalResults,
    currentQuery,
    facets 
  } = useSelector(selectSearch);
  
  // Component state
  const [sortBy, setSortBy] = useState<'relevance' | 'popularity' | 'date'>('relevance');
  const [selectedFilters, setSelectedFilters] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  
  // Get query from URL params
  const query = searchParams.get('q') || '';
  
  // Filter options based on available content types
  const filterOptions: FilterOption[] = [
    {
      key: 'learning_path',
      label: 'Learning Paths',
      icon: BookOpenIcon,
      count: facets?.content_types?.learning_path || 0
    },
    {
      key: 'module',
      label: 'Modules',
      icon: AcademicCapIcon,
      count: facets?.content_types?.module || 0
    },
    {
      key: 'assessment',
      label: 'Assessments',
      icon: ChartBarIcon,
      count: facets?.content_types?.assessment || 0
    },
    {
      key: 'knowledge_node',
      label: 'Knowledge Nodes',
      icon: AcademicCapIcon,
      count: facets?.content_types?.knowledge_node || 0
    },
    {
      key: 'content',
      label: 'Content',
      icon: DocumentTextIcon,
      count: facets?.content_types?.content || 0
    },
    {
      key: 'user',
      label: 'Users',
      icon: UserIcon,
      count: facets?.content_types?.user || 0
    }
  ];
  
  // Perform search on mount and query change
  useEffect(() => {
    if (query) {
      dispatch(setCurrentQuery(query));
      dispatch(performSearch(query));
    } else {
      dispatch(clearSearchResults());
    }
    
    return () => {
      // Cleanup on unmount
      dispatch(clearSearchResults());
    };
  }, [query, dispatch]);
  
  // Handle filter toggle
  const toggleFilter = (filterKey: string) => {
    const newFilters = selectedFilters.includes(filterKey)
      ? selectedFilters.filter(f => f !== filterKey)
      : [...selectedFilters, filterKey];
    
    setSelectedFilters(newFilters);
    
    // Re-search with filters
    if (query) {
      dispatch(performSearch({ 
        query, 
        content_types: newFilters.length > 0 ? newFilters : undefined 
      }));
    }
  };
  
  // Handle sort change
  const handleSortChange = (newSortBy: typeof sortBy) => {
    setSortBy(newSortBy);
  };
  
  // Sort results based on selected sort option
  const sortedResults = [...results].sort((a, b) => {
    switch (sortBy) {
      case 'popularity':
        return b.popularity_score - a.popularity_score;
      case 'relevance':
        return b.relevance_score - a.relevance_score;
      default:
        return b.relevance_score - a.relevance_score;
    }
  });
  
  // Handle result click
  const handleResultClick = (result: any) => {
    searchService.trackClick(query, result.url);
    navigate(result.url);
  };
  
  // Get content type color
  const getContentTypeColor = (contentType: string) => {
    const colors: Record<string, string> = {
      learning_path: 'bg-blue-100 text-blue-800',
      module: 'bg-green-100 text-green-800',
      assessment: 'bg-purple-100 text-purple-800',
      knowledge_node: 'bg-indigo-100 text-indigo-800',
      content: 'bg-gray-100 text-gray-800',
      user: 'bg-orange-100 text-orange-800'
    };
    return colors[contentType] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Search Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center space-x-2 mb-4">
            <MagnifyingGlassIcon className="h-6 w-6 text-gray-400" />
            <h1 className="text-2xl font-bold text-gray-900">
              Search Results
            </h1>
          </div>
          
          {/* Search Query */}
          {query && (
            <div className="mb-4">
              <p className="text-gray-600">
                Showing results for{' '}
                <span className="font-semibold text-gray-900">"{query}"</span>
                {totalResults > 0 && (
                  <span className="ml-2 text-sm text-gray-500">
                    ({totalResults} results found)
                  </span>
                )}
              </p>
            </div>
          )}
          
          {/* Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
            >
              <FunnelIcon className="h-4 w-4" />
              <span>Filters</span>
              {selectedFilters.length > 0 && (
                <span className="bg-primary-100 text-primary-800 text-xs px-2 py-1 rounded-full">
                  {selectedFilters.length}
                </span>
              )}
            </button>
            
            {/* Sort Options */}
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => handleSortChange(e.target.value as typeof sortBy)}
                className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="relevance">Relevance</option>
                <option value="popularity">Popularity</option>
              </select>
            </div>
          </div>
        </div>
        
        {/* Filter Panel */}
        {showFilters && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Content Types</h3>
              <button
                onClick={() => setSelectedFilters([])}
                className="text-sm text-primary-600 hover:text-primary-700"
              >
                Clear all
              </button>
            </div>
            
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
              {filterOptions.map((filter) => {
                const IconComponent = filter.icon;
                const isSelected = selectedFilters.includes(filter.key);
                
                return (
                  <button
                    key={filter.key}
                    onClick={() => toggleFilter(filter.key)}
                    className={`
                      flex items-center space-x-2 p-3 rounded-lg border-2 transition-all
                      ${isSelected 
                        ? 'border-primary-500 bg-primary-50 text-primary-700' 
                        : 'border-gray-200 hover:border-gray-300 text-gray-700'
                      }
                    `}
                  >
                    <IconComponent className="h-5 w-5" />
                    <div className="text-left">
                      <div className="text-sm font-medium">{filter.label}</div>
                      {filter.count !== undefined && (
                        <div className="text-xs text-gray-500">
                          {filter.count} results
                        </div>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </motion.div>
        )}
        
        {/* Results */}
        <div className="space-y-4">
          {isLoading && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Searching...</p>
            </div>
          )}
          
          {!isLoading && sortedResults.length === 0 && query && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
              <MagnifyingGlassIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No results found</h3>
              <p className="text-gray-600 mb-4">
                We couldn't find any content matching your search for "{query}"
              </p>
              <div className="text-sm text-gray-500">
                <p className="mb-2">Try:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Checking your spelling</li>
                  <li>Using different or more general keywords</li>
                  <li>Removing some filters</li>
                </ul>
              </div>
            </div>
          )}
          
          {!isLoading && sortedResults.length > 0 && (
            <div className="space-y-4">
              {sortedResults.map((result, index) => (
                <motion.div
                  key={result.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => handleResultClick(result)}
                >
                  <div className="p-6">
                    <div className="flex items-start space-x-4">
                      {/* Content Type Icon */}
                      <div className="flex-shrink-0 mt-1">
                        <span className="text-2xl">
                          {searchService.getContentTypeIcon(result.content_type)}
                        </span>
                      </div>
                      
                      {/* Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors">
                            <span dangerouslySetInnerHTML={{
                              __html: searchService.highlightSearchTerms(result.title, query)
                            }} />
                          </h3>
                          
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getContentTypeColor(result.content_type)}`}>
                            {searchService.formatContentType(result.content_type)}
                          </span>
                        </div>
                        
                        <p className="text-gray-600 mb-3 line-clamp-2">
                          <span dangerouslySetInnerHTML={{
                            __html: searchService.highlightSearchTerms(result.description, query)
                          }} />
                        </p>
                        
                        {/* Tags */}
                        {result.tags && result.tags.length > 0 && (
                          <div className="flex flex-wrap gap-2 mb-3">
                            {result.tags.slice(0, 3).map((tag, tagIndex) => (
                              <span
                                key={tagIndex}
                                className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700"
                              >
                                {tag}
                              </span>
                            ))}
                            {result.tags.length > 3 && (
                              <span className="text-xs text-gray-500">
                                +{result.tags.length - 3} more
                              </span>
                            )}
                          </div>
                        )}
                        
                        {/* Metadata */}
                        <div className="flex items-center justify-between text-sm text-gray-500">
                          <div className="flex items-center space-x-4">
                            {result.metadata?.difficulty && (
                              <span className="capitalize">
                                {result.metadata.difficulty}
                              </span>
                            )}
                            {result.metadata?.type && (
                              <span className="capitalize">
                                {result.metadata.type}
                              </span>
                            )}
                            {result.metadata?.estimated_hours && (
                              <span>
                                {result.metadata.estimated_hours}h
                              </span>
                            )}
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            {result.relevance_score > 0 && (
                              <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                                {Math.round(result.relevance_score * 100)}% match
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchResultsPage;