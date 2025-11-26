// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  BookOpenIcon,
  ClockIcon,
  StarIcon,
  UserGroupIcon,
  ChevronRightIcon,
  FunnelIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import { learningService, LearningPath } from '../../services/learningService';
import { toast } from 'react-hot-toast';
import { useCallback } from 'react';

interface FilterOptions {
  difficulty: string[];
  search: string;
  sortBy: 'title' | 'rating' | 'duration' | 'modules';
  sortOrder: 'asc' | 'desc';
}

const DIFFICULTY_LEVELS = [
  { value: 'beginner', label: 'Beginner', color: 'bg-green-100 text-green-800' },
  { value: 'intermediate', label: 'Intermediate', color: 'bg-yellow-100 text-yellow-800' },
  { value: 'advanced', label: 'Advanced', color: 'bg-red-100 text-red-800' },
];

// Mock learner count - in real app this would come from API
const LEARNER_COUNT = 1200;

const LearningPathCard: React.FC<{ path: LearningPath; delay: number }> = ({ path, delay }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      whileHover={{ y: -5 }}
      className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden group"
    >
      {/* Learning Path Image */}
      <div className="h-48 bg-gradient-to-br from-primary-500 to-secondary-500 relative overflow-hidden">
        {!imageLoaded && (
          <div className="absolute inset-0 bg-gray-200 animate-pulse" />
        )}
        <img
          src={`https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400&h=200&fit=crop&crop=center`}
          alt={path.title}
          className={`w-full h-full object-cover transition-all duration-300 group-hover:scale-105 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setImageLoaded(true)}
          onError={() => setImageLoaded(true)}
        />
        
        {/* Difficulty Badge */}
        <div className="absolute top-4 left-4">
          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
            DIFFICULTY_LEVELS.find(d => d.value === path.difficulty_level)?.color || 'bg-gray-100 text-gray-800'
          }`}>
            {DIFFICULTY_LEVELS.find(d => d.value === path.difficulty_level)?.label || path.difficulty_level}
          </span>
        </div>
        
        {/* Rating Badge */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-2 py-1 flex items-center space-x-1">
          <StarIcon className="h-4 w-4 text-yellow-500 fill-current" />
          <span className="text-sm font-medium text-gray-900">{path.rating.toFixed(1)}</span>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
          {path.title}
        </h3>
        
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {path.description}
        </p>

        {/* Meta Information */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <ClockIcon className="h-4 w-4" />
              <span>{path.estimated_duration}min</span>
            </div>
            <div className="flex items-center space-x-1">
              <BookOpenIcon className="h-4 w-4" />
              <span>{path.modules_count} modules</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-1">
            <UserGroupIcon className="h-4 w-4" />
            <span>{(LEARNER_COUNT / 1000).toFixed(1)}k learners</span>
          </div>
        </div>

        {/* Action Button */}
        <Link to={`/learning/${path.id}`}>
          <button className="w-full flex items-center justify-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors group/btn">
            <span>Start Learning</span>
            <ChevronRightIcon className="h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
          </button>
        </Link>
      </div>
    </motion.div>
  );
};

const FilterPanel: React.FC<{
  filters: FilterOptions;
  onFiltersChange: (filters: FilterOptions) => void;
  isOpen: boolean;
  onToggle: () => void;
}> = ({ filters, onFiltersChange, isOpen, onToggle }) => {
  return (
    <>
      {/* Mobile Filter Toggle */}
      <div className="lg:hidden mb-4">
        <button
          onClick={onToggle}
          className="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <FunnelIcon className="h-4 w-4" />
          <span>Filters</span>
        </button>
      </div>

      {/* Filter Panel */}
      <motion.div
        initial={false}
        animate={{
          height: isOpen ? 'auto' : 0,
          opacity: isOpen ? 1 : 0,
        }}
        transition={{ duration: 0.3 }}
        className="lg:block lg:relative lg:inset-0 lg:bg-transparent overflow-hidden"
      >
        <div className="bg-white rounded-lg border border-gray-200 p-6 mb-6 lg:mb-0">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
          
          {/* Search */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search
            </label>
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                value={filters.search}
                onChange={(e) => onFiltersChange({ ...filters, search: e.target.value })}
                placeholder="Search learning paths..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Difficulty */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <div className="space-y-2">
              {DIFFICULTY_LEVELS.map((level) => (
                <label key={level.value} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.difficulty.includes(level.value)}
                    onChange={(e) => {
                      const newDifficulty = e.target.checked
                        ? [...filters.difficulty, level.value]
                        : filters.difficulty.filter(d => d !== level.value);
                      onFiltersChange({ ...filters, difficulty: newDifficulty });
                    }}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                  <span className="ml-2 text-sm text-gray-700">{level.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Sort By */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sort By
            </label>
            <select
              value={`${filters.sortBy}-${filters.sortOrder}`}
              onChange={(e) => {
                const [sortBy, sortOrder] = e.target.value.split('-') as [FilterOptions['sortBy'], FilterOptions['sortOrder']];
                onFiltersChange({ ...filters, sortBy, sortOrder });
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="title-asc">Title (A-Z)</option>
              <option value="title-desc">Title (Z-A)</option>
              <option value="rating-desc">Rating (High to Low)</option>
              <option value="rating-asc">Rating (Low to High)</option>
              <option value="duration-asc">Duration (Short to Long)</option>
              <option value="duration-desc">Duration (Long to Short)</option>
              <option value="modules-asc">Modules (Few to Many)</option>
              <option value="modules-desc">Modules (Many to Few)</option>
            </select>
          </div>

          {/* Clear Filters */}
          <button
            onClick={() => onFiltersChange({
              difficulty: [],
              search: '',
              sortBy: 'title',
              sortOrder: 'asc',
            })}
            className="w-full px-4 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Clear All Filters
          </button>
        </div>
      </motion.div>
    </>
  );
};

export const LearningPaths: React.FC = () => {
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [filteredPaths, setFilteredPaths] = useState<LearningPath[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [filters, setFilters] = useState<FilterOptions>({
    difficulty: [],
    search: '',
    sortBy: 'title',
    sortOrder: 'asc',
  });

  const applyFilters = useCallback(() => {
    let filtered = [...learningPaths];

    // Apply search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      filtered = filtered.filter(path =>
        path.title.toLowerCase().includes(searchLower) ||
        path.description.toLowerCase().includes(searchLower)
      );
    }

    // Apply difficulty filter
    if (filters.difficulty.length > 0) {
      filtered = filtered.filter(path =>
        filters.difficulty.includes(path.difficulty_level)
      );
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any, bValue: any;

      switch (filters.sortBy) {
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'rating':
          aValue = a.rating;
          bValue = b.rating;
          break;
        case 'duration':
          aValue = a.estimated_duration;
          bValue = b.estimated_duration;
          break;
        case 'modules':
          aValue = a.modules_count;
          bValue = b.modules_count;
          break;
        default:
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
      }

      if (typeof aValue === 'string') {
        return filters.sortOrder === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue);
      } else {
        return filters.sortOrder === 'asc' 
          ? aValue - bValue
          : bValue - aValue;
      }
    });

    setFilteredPaths(filtered);
  }, [filters, learningPaths]);

  useEffect(() => {
    loadLearningPaths();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, learningPaths, applyFilters]);

  const loadLearningPaths = async () => {
    try {
      setIsLoading(true);
      const paths = await learningService.getLearningPaths();
      setLearningPaths(paths);
    } catch (error) {
      console.error('Failed to load learning paths:', error);
      toast.error('Failed to load learning paths');
    } finally {
      setIsLoading(false);
    }
  };


  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Learning Paths</h1>
          <p className="text-gray-600 mt-2">
            Choose from curated learning paths designed to master JAC programming
          </p>
        </div>
        
        <div className="mt-4 lg:mt-0 flex items-center space-x-2">
          <span className="text-sm text-gray-500">
            {filteredPaths.length} of {learningPaths.length} paths
          </span>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Filters Sidebar */}
        <div className="lg:w-80 flex-shrink-0">
          <FilterPanel
            filters={filters}
            onFiltersChange={setFilters}
            isOpen={filtersOpen}
            onToggle={() => setFiltersOpen(!filtersOpen)}
          />
        </div>

        {/* Learning Paths Grid */}
        <div className="flex-1">
          {filteredPaths.length > 0 ? (
            <motion.div
              layout
              className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
            >
              {filteredPaths.map((path, index) => (
                <LearningPathCard
                  key={path.id}
                  path={path}
                  delay={index * 0.1}
                />
              ))}
            </motion.div>
          ) : (
            <div className="text-center py-12">
              <BookOpenIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No learning paths found
              </h3>
              <p className="text-gray-600 mb-6">
                Try adjusting your filters or search terms
              </p>
              <button
                onClick={() => setFilters({
                  difficulty: [],
                  search: '',
                  sortBy: 'title',
                  sortOrder: 'asc',
                })}
                className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
              >
                Clear Filters
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LearningPaths;