// JAC Learning Platform - TypeScript utilities by Cavin Otieno

/**
 * Admin utility functions for learning path administration
 */

/**
 * Calculate completion rate percentage
 */
export const calculateCompletionRate = (completed: number, total: number): number => {
  if (total === 0) return 0;
  return Math.round((completed / total) * 100 * 10) / 10; // Round to 1 decimal place
};

/**
 * Calculate drop-off rate between stages
 */
export const calculateDropoffRate = (current: number, previous: number): number => {
  if (previous === 0) return 0;
  return Math.round((1 - current / previous) * 100 * 10) / 10;
};

/**
 * Format duration in minutes to human readable format
 */
export const formatDuration = (minutes: number): string => {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (remainingMinutes === 0) {
    return `${hours}h`;
  }
  return `${hours}h ${remainingMinutes}m`;
};

/**
 * Get status color for learning path status
 */
export const getStatusColor = (status: string): string => {
  switch (status.toLowerCase()) {
    case 'published':
      return 'bg-green-100 text-green-800';
    case 'draft':
      return 'bg-yellow-100 text-yellow-800';
    case 'archived':
      return 'bg-gray-100 text-gray-800';
    case 'in_review':
      return 'bg-blue-100 text-blue-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

/**
 * Generate performance insight based on metrics
 */
export const generatePerformanceInsight = (
  type: 'warning' | 'success' | 'info',
  title: string,
  description: string,
  action: string
) => {
  return {
    type,
    title,
    description,
    action,
    timestamp: new Date().toISOString()
  };
};

/**
 * Sort learning paths by various criteria
 */
export const sortLearningPaths = (
  paths: any[],
  sortBy: 'name' | 'completion_rate' | 'learners' | 'updated',
  order: 'asc' | 'desc' = 'desc'
) => {
  return [...paths].sort((a, b) => {
    let aValue: any, bValue: any;
    
    switch (sortBy) {
      case 'name':
        aValue = a.name.toLowerCase();
        bValue = b.name.toLowerCase();
        break;
      case 'completion_rate':
        aValue = a.completion || 0;
        bValue = b.completion || 0;
        break;
      case 'learners':
        aValue = a.learners || 0;
        bValue = b.learners || 0;
        break;
      case 'updated':
        aValue = new Date(a.lastUpdated);
        bValue = new Date(b.lastUpdated);
        break;
      default:
        return 0;
    }
    
    if (order === 'asc') {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });
};

/**
 * Filter learning paths by criteria
 */
export const filterLearningPaths = (
  paths: any[],
  filters: {
    status?: string[];
    completionRate?: { min: number; max: number };
    learners?: { min: number; max: number };
    searchQuery?: string;
  }
) => {
  return paths.filter(path => {
    // Status filter
    if (filters.status && filters.status.length > 0) {
      if (!filters.status.includes(path.status)) {
        return false;
      }
    }
    
    // Completion rate filter
    if (filters.completionRate) {
      const completion = path.completion || 0;
      if (completion < filters.completionRate.min || completion > filters.completionRate.max) {
        return false;
      }
    }
    
    // Learners filter
    if (filters.learners) {
      const learners = path.learners || 0;
      if (learners < filters.learners.min || learners > filters.learners.max) {
        return false;
      }
    }
    
    // Search query filter
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      if (!path.name.toLowerCase().includes(query)) {
        return false;
      }
    }
    
    return true;
  });
};

/**
 * Export learning path data to CSV format
 */
export const exportLearningPathsToCSV = (paths: any[]): string => {
  const headers = [
    'Name',
    'Status',
    'Modules',
    'Completion Rate',
    'Learners',
    'Average Score',
    'Last Updated'
  ];
  
  const csvContent = [
    headers.join(','),
    ...paths.map(path => [
      `"${path.name}"`,
      path.status,
      path.modules,
      `${path.completion}%`,
      path.learners,
      path.score || 'N/A',
      path.lastUpdated
    ].join(','))
  ].join('\n');
  
  return csvContent;
};

/**
 * Generate mock analytics data for development
 */
export const generateMockAnalytics = () => {
  const timeframe = ['week', 'month', 'quarter', 'year'];
  const learningPaths = [
    'JAC Programming Fundamentals',
    'Advanced JAC Concepts', 
    'JAC Web Development',
    'JAC Data Structures',
    'JAC Algorithms'
  ];
  
  return {
    completionTrends: timeframe.map((period, index) => ({
      period,
      completionRate: 65 + index * 5 + Math.random() * 10,
      learners: 200 + index * 50 + Math.floor(Math.random() * 100),
      activeUsers: 150 + index * 30 + Math.floor(Math.random() * 50)
    })),
    
    userJourney: [
      { stage: 'Started Path', users: 342, percentage: 100 },
      { stage: 'Completed Module 1', users: 298, percentage: 87.1 },
      { stage: 'Completed Module 2', users: 267, percentage: 78.1 },
      { stage: 'Completed Module 3', users: 234, percentage: 68.4 },
      { stage: 'Completed Module 4', users: 198, percentage: 57.9 },
      { stage: 'Completed Path', users: 156, percentage: 45.6 },
    ],
    
    performanceInsights: [
      {
        type: 'warning',
        title: 'High Drop-off Rate',
        description: 'Module 3 has 12.8% drop-off rate. Consider adding more interactive content.',
        action: 'Review Module 3',
        impact: 'medium'
      },
      {
        type: 'success', 
        title: 'Popular Content',
        description: 'JAC Programming Fundamentals is the most completed path this month.',
        action: 'View Details',
        impact: 'positive'
      }
    ],
    
    topPerformingPaths: learningPaths.map((name, index) => ({
      name,
      completionRate: 85 - index * 5 + Math.random() * 8,
      learners: 100 + index * 30 + Math.floor(Math.random() * 50),
      averageScore: 80 + Math.random() * 15,
      rating: 4.5 + Math.random() * 0.5
    }))
  };
};