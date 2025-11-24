/**
 * Search Service for JAC Learning Platform Frontend
 * Handles search functionality with backend API integration
 */

import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SearchResult {
  id: string;
  content_type: 'learning_path' | 'module' | 'lesson' | 'assessment' | 'knowledge_node' | 'content' | 'user';
  content_id: string;
  title: string;
  description: string;
  url: string;
  tags: string[];
  relevance_score: number;
  popularity_score: number;
  metadata?: Record<string, any>;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total_results: number;
  suggestions: string[];
  facets: {
    content_types: Record<string, number>;
    total_results: number;
  };
}

export interface SearchRequest {
  query: string;
  content_types?: string[];
  limit?: number;
  offset?: number;
}

class SearchService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE) {
    this.baseURL = baseURL;
  }

  /**
   * Configure axios instance with authentication
   */
  private getAxiosInstance() {
    const token = localStorage.getItem('access_token');
    
    return axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` })
      },
    });
  }

  /**
   * Perform a comprehensive search
   */
  async search(request: SearchRequest): Promise<SearchResponse> {
    try {
      const axiosInstance = this.getAxiosInstance();
      const response = await axiosInstance.post('/api/search/search/search/', request);
      return response.data;
    } catch (error: any) {
      console.error('Search API error:', error);
      
      // Return empty results on error
      return {
        query: request.query,
        results: [],
        total_results: 0,
        suggestions: [],
        facets: {
          content_types: {},
          total_results: 0
        }
      };
    }
  }

  /**
   * Get search suggestions for autocomplete
   */
  async getSuggestions(query: string, limit: number = 10): Promise<string[]> {
    if (!query || query.length < 2) {
      return [];
    }

    try {
      const axiosInstance = this.getAxiosInstance();
      const response = await axiosInstance.get('/api/search/search/suggestions/', {
        params: { query, limit }
      });
      return response.data.suggestions || [];
    } catch (error: any) {
      console.error('Search suggestions API error:', error);
      return [];
    }
  }

  /**
   * Track user click on search result
   */
  async trackClick(query: string, resultUrl: string): Promise<void> {
    try {
      const axiosInstance = this.getAxiosInstance();
      await axiosInstance.post('/api/search/search/track_click/', {
        query,
        result_url: resultUrl
      });
    } catch (error: any) {
      console.error('Track click API error:', error);
      // Don't throw error for tracking failures
    }
  }

  /**
   * Get user's search history
   */
  async getSearchHistory(): Promise<any[]> {
    try {
      const axiosInstance = this.getAxiosInstance();
      const response = await axiosInstance.get('/api/search/history/');
      return response.data || [];
    } catch (error: any) {
      console.error('Search history API error:', error);
      return [];
    }
  }

  /**
   * Clear user's search history
   */
  async clearSearchHistory(): Promise<void> {
    try {
      const axiosInstance = this.getAxiosInstance();
      await axiosInstance.delete('/api/search/history/clear/');
    } catch (error: any) {
      console.error('Clear search history API error:', error);
      throw error;
    }
  }

  /**
   * Get popular search terms
   */
  async getPopularSearches(limit: number = 10): Promise<string[]> {
    try {
      const axiosInstance = this.getAxiosInstance();
      const response = await axiosInstance.get('/api/search/popular/popular/', {
        params: { limit }
      });
      return response.data.popular_searches || [];
    } catch (error: any) {
      console.error('Popular searches API error:', error);
      return [];
    }
  }

  /**
   * Get trending search terms
   */
  async getTrendingSearches(limit: number = 10): Promise<string[]> {
    try {
      const axiosInstance = this.getAxiosInstance();
      const response = await axiosInstance.get('/api/search/popular/trending/', {
        params: { limit }
      });
      return response.data.trending_searches || [];
    } catch (error: any) {
      console.error('Trending searches API error:', error);
      return [];
    }
  }

  /**
   * Debounced search function for real-time search
   */
  debounceSearch(
    query: string,
    callback: (results: SearchResponse) => void,
    delay: number = 300
  ): () => void {
    let timeoutId: NodeJS.Timeout;

    return () => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(async () => {
        if (query.trim()) {
          const results = await this.search({ query, limit: 10 });
          callback(results);
        } else {
          callback({
            query: '',
            results: [],
            total_results: 0,
            suggestions: [],
            facets: {
              content_types: {},
              total_results: 0
            }
          });
        }
      }, delay);
    };
  }

  /**
   * Format content type for display
   */
  formatContentType(contentType: string): string {
    const typeMap: Record<string, string> = {
      'learning_path': 'Learning Path',
      'module': 'Module',
      'lesson': 'Lesson',
      'assessment': 'Assessment',
      'knowledge_node': 'Knowledge Node',
      'content': 'Content',
      'user': 'User'
    };
    
    return typeMap[contentType] || contentType;
  }

  /**
   * Get content type icon
   */
  getContentTypeIcon(contentType: string): string {
    const iconMap: Record<string, string> = {
      'learning_path': '📚',
      'module': '📖',
      'lesson': '📝',
      'assessment': '📊',
      'knowledge_node': '🧠',
      'content': '📄',
      'user': '👤'
    };
    
    return iconMap[contentType] || '📄';
  }

  /**
   * Highlight search terms in text
   */
  highlightSearchTerms(text: string, searchQuery: string): string {
    if (!searchQuery.trim()) return text;
    
    const terms = searchQuery.toLowerCase().split(' ').filter(term => term.length > 0);
    let highlightedText = text;
    
    terms.forEach(term => {
      const regex = new RegExp(`(${term})`, 'gi');
      highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
    });
    
    return highlightedText;
  }
}

// Create singleton instance
const searchService = new SearchService();

export default searchService;