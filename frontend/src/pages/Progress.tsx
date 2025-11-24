import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useSelector } from 'react-redux';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadialBarChart, RadialBar } from 'recharts';
import { authService } from '../services/authService';
import { learningService } from '../services/learningService';

// Types
interface LearningPathProgress {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  totalModules: number;
  completedModules: number;
  progressPercentage: number;
  timeSpent: string;
  startedAt: string;
  lastActivity: string;
  estimatedCompletion: string;
  averageScore: number;
  status: 'not_started' | 'in_progress' | 'completed' | 'paused';
}

interface ModuleProgress {
  id: string;
  title: string;
  learningPath: string;
  order: number;
  status: 'not_started' | 'in_progress' | 'completed' | 'skipped';
  progressPercentage: number;
  timeSpent: string;
  quizScore?: number;
  codingScore?: number;
  overallScore?: number;
  lastAccessed: string;
  completedAt?: string;
}

interface WeeklyActivity {
  date: string;
  modules: number;
  timeSpent: number;
  score: number;
  streak: boolean;
}

interface LearningStats {
  totalModulesCompleted: number;
  totalTimeSpent: string;
  currentStreak: number;
  longestStreak: number;
  averageScore: number;
  totalPoints: number;
  level: number;
  experienceToNext: number;
  weeklyGoal: number;
  weeklyProgress: number;
}

// Mock data for comprehensive progress tracking
const mockLearningPaths: LearningPathProgress[] = [
  {
    id: '1',
    name: 'JAC Fundamentals',
    description: 'Learn the basics of JAC programming language',
    difficulty: 'beginner',
    totalModules: 15,
    completedModules: 8,
    progressPercentage: 53,
    timeSpent: '4h 30m',
    startedAt: '2025-11-01',
    lastActivity: '2025-11-23',
    estimatedCompletion: '2025-12-15',
    averageScore: 87,
    status: 'in_progress'
  },
  {
    id: '2',
    name: 'Advanced JAC Concepts',
    description: 'Master advanced JAC programming techniques',
    difficulty: 'advanced',
    totalModules: 20,
    completedModules: 3,
    progressPercentage: 15,
    timeSpent: '2h 15m',
    startedAt: '2025-11-20',
    lastActivity: '2025-11-22',
    estimatedCompletion: '2026-01-30',
    averageScore: 92,
    status: 'in_progress'
  },
  {
    id: '3',
    name: 'Python Basics',
    description: 'Introduction to Python programming',
    difficulty: 'beginner',
    totalModules: 12,
    completedModules: 12,
    progressPercentage: 100,
    timeSpent: '6h 45m',
    startedAt: '2025-10-15',
    lastActivity: '2025-11-10',
    estimatedCompletion: 'Completed',
    averageScore: 94,
    status: 'completed'
  }
];

const mockModuleProgress: ModuleProgress[] = [
  {
    id: '1',
    title: 'Variables and Data Types',
    learningPath: 'JAC Fundamentals',
    order: 1,
    status: 'completed',
    progressPercentage: 100,
    timeSpent: '25m',
    quizScore: 95,
    codingScore: 88,
    overallScore: 92,
    lastAccessed: '2025-11-15',
    completedAt: '2025-11-15'
  },
  {
    id: '2',
    title: 'Control Structures',
    learningPath: 'JAC Fundamentals',
    order: 2,
    status: 'completed',
    progressPercentage: 100,
    timeSpent: '35m',
    quizScore: 90,
    codingScore: 85,
    overallScore: 88,
    lastAccessed: '2025-11-17',
    completedAt: '2025-11-17'
  },
  {
    id: '3',
    title: 'Functions and Methods',
    learningPath: 'JAC Fundamentals',
    order: 3,
    status: 'in_progress',
    progressPercentage: 65,
    timeSpent: '20m',
    quizScore: 85,
    codingScore: 78,
    overallScore: 82,
    lastAccessed: '2025-11-23'
  },
  {
    id: '4',
    title: 'Object-Oriented Programming',
    learningPath: 'JAC Fundamentals',
    order: 4,
    status: 'not_started',
    progressPercentage: 0,
    timeSpent: '0m',
    lastAccessed: 'Never'
  },
  {
    id: '5',
    title: 'Error Handling',
    learningPath: 'JAC Fundamentals',
    order: 5,
    status: 'not_started',
    progressPercentage: 0,
    timeSpent: '0m',
    lastAccessed: 'Never'
  }
];

const mockWeeklyActivity: WeeklyActivity[] = [
  { date: 'Mon', modules: 2, timeSpent: 45, score: 88, streak: true },
  { date: 'Tue', modules: 1, timeSpent: 25, score: 92, streak: true },
  { date: 'Wed', modules: 3, timeSpent: 60, score: 85, streak: true },
  { date: 'Thu', modules: 1, timeSpent: 30, score: 90, streak: true },
  { date: 'Fri', modules: 2, timeSpent: 50, score: 87, streak: true },
  { date: 'Sat', modules: 0, timeSpent: 0, score: 0, streak: false },
  { date: 'Sun', modules: 1, timeSpent: 20, score: 89, streak: true }
];

const mockLearningStats: LearningStats = {
  totalModulesCompleted: 23,
  totalTimeSpent: '13h 30m',
  currentStreak: 7,
  longestStreak: 14,
  averageScore: 89,
  totalPoints: 1250,
  level: 3,
  experienceToNext: 250,
  weeklyGoal: 10,
  weeklyProgress: 8
};

const COLORS = ['#8B5CF6', '#06B6D4', '#10B981', '#F59E0B', '#EF4444'];

const difficultyColors = {
  beginner: 'from-green-400 to-green-600',
  intermediate: 'from-yellow-400 to-yellow-600',
  advanced: 'from-red-400 to-red-600'
};

const statusColors = {
  completed: 'text-green-400',
  in_progress: 'text-blue-400',
  not_started: 'text-gray-400',
  paused: 'text-yellow-400',
  skipped: 'text-gray-500'
};

const statusLabels = {
  completed: 'Completed',
  in_progress: 'In Progress',
  not_started: 'Not Started',
  paused: 'Paused',
  skipped: 'Skipped'
};

const Progress: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'paths' | 'modules' | 'analytics'>('overview');
  const [selectedTimeframe, setSelectedTimeframe] = useState<'week' | 'month' | 'year'>('week');
  const [learningPaths, setLearningPaths] = useState<LearningPathProgress[]>(mockLearningPaths);
  const [moduleProgress, setModuleProgress] = useState<ModuleProgress[]>(mockModuleProgress);
  const [weeklyActivity, setWeeklyActivity] = useState<WeeklyActivity[]>(mockWeeklyActivity);
  const [stats, setStats] = useState<LearningStats>(mockLearningStats);
  const [isLoading, setIsLoading] = useState(false);
  
  const user = useSelector((state: any) => state.auth.user) || authService.getCurrentUser();

  useEffect(() => {
    // In a real app, fetch progress data from APIs
    loadProgressData();
  }, []);

  const loadProgressData = async () => {
    setIsLoading(true);
    try {
      // Mock loading delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      // Data is already set as mock data above
    } catch (error) {
      // Handle progress data loading error gracefully
    } finally {
      setIsLoading(false);
    }
  };

  const getOverallProgress = () => {
    const totalModules = learningPaths.reduce((sum, path) => sum + path.totalModules, 0);
    const completedModules = learningPaths.reduce((sum, path) => sum + path.completedModules, 0);
    return Math.round((completedModules / totalModules) * 100);
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'from-green-400 to-green-600';
    if (percentage >= 60) return 'from-blue-400 to-blue-600';
    if (percentage >= 40) return 'from-yellow-400 to-yellow-600';
    return 'from-red-400 to-red-600';
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getStreakIcon = (streak: boolean) => {
    return streak ? '🔥' : '⭕';
  };

  const calculateRadialProgress = (value: number, total: number) => {
    return [{ value: Math.round((value / total) * 100), fill: '#8B5CF6' }];
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'paths', label: 'Learning Paths', icon: '🛤️' },
    { id: 'modules', label: 'Modules', icon: '📚' },
    { id: 'analytics', label: 'Analytics', icon: '📈' }
  ];

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Progress Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Overall Progress</p>
              <p className="text-2xl font-bold text-white">{getOverallProgress()}%</p>
            </div>
            <div className="text-3xl">🎯</div>
          </div>
          <div className="mt-4">
            <div className="w-full bg-white/20 rounded-full h-2">
              <div 
                className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(getOverallProgress())}`}
                style={{ width: `${getOverallProgress()}%` }}
              ></div>
            </div>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Current Streak</p>
              <p className="text-2xl font-bold text-orange-400">{stats.currentStreak} days</p>
            </div>
            <div className="text-3xl">🔥</div>
          </div>
          <p className="text-white/85 text-xs mt-2">Longest: {stats.longestStreak} days</p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Modules Completed</p>
              <p className="text-2xl font-bold text-green-400">{stats.totalModulesCompleted}</p>
            </div>
            <div className="text-3xl">✅</div>
          </div>
          <p className="text-white/85 text-xs mt-2">Average score: {stats.averageScore}%</p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Level {stats.level}</p>
              <p className="text-2xl font-bold text-purple-400">{stats.totalPoints} pts</p>
            </div>
            <div className="text-3xl">⭐</div>
          </div>
          <p className="text-white/85 text-xs mt-2">{stats.experienceToNext} to next level</p>
        </motion.div>
      </div>

      {/* Weekly Activity Chart */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Weekly Activity</h3>
        <div className="h-[300px] flex items-center justify-center text-white/90">
          <div className="text-center">
            <div className="text-4xl mb-4">📊</div>
            <p>Weekly activity chart will be displayed here</p>
            <p className="text-sm mt-2">Chart temporarily disabled due to technical issues</p>
          </div>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Weekly Goal Progress */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Weekly Goal Progress</h4>
          <div className="flex items-center justify-between mb-4">
            <span className="text-white/90">Modules this week</span>
            <span className="text-white font-semibold">{stats.weeklyProgress} / {stats.weeklyGoal}</span>
          </div>
          <div className="w-full bg-white/20 rounded-full h-3">
            <div 
              className={`h-3 rounded-full bg-gradient-to-r ${getProgressColor((stats.weeklyProgress / stats.weeklyGoal) * 100)}`}
              style={{ width: `${(stats.weeklyProgress / stats.weeklyGoal) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Learning Distribution */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Learning Distribution</h4>
          <div className="h-[200px] flex items-center justify-center text-white/90">
            <div className="text-center">
              <div className="text-4xl mb-4">🥧</div>
              <p>Learning distribution chart will be displayed here</p>
              <p className="text-sm mt-2">Chart temporarily disabled due to TypeScript compatibility issues</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderLearningPaths = () => (
    <div className="space-y-6">
      {learningPaths.map((path, index) => (
        <motion.div
          key={path.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-2">
                <h3 className="text-xl font-semibold text-white">{path.name}</h3>
                <span className={`px-3 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${difficultyColors[path.difficulty]} text-white`}>
                  {path.difficulty.toUpperCase()}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[path.status]} bg-white/10`}>
                  {statusLabels[path.status]}
                </span>
              </div>
              <p className="text-white/90 mb-3">{path.description}</p>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-white/85">Progress:</span>
                  <div className="flex items-center space-x-2 mt-1">
                    <div className="w-16 bg-white/20 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(path.progressPercentage)}`}
                        style={{ width: `${path.progressPercentage}%` }}
                      ></div>
                    </div>
                    <span className="text-white font-medium">{path.progressPercentage}%</span>
                  </div>
                </div>
                
                <div>
                  <span className="text-white/85">Modules:</span>
                  <p className="text-white font-medium">{path.completedModules} / {path.totalModules}</p>
                </div>
                
                <div>
                  <span className="text-white/85">Time Spent:</span>
                  <p className="text-white font-medium">{path.timeSpent}</p>
                </div>
                
                <div>
                  <span className="text-white/85">Average Score:</span>
                  <p className="text-white font-medium">{path.averageScore}%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-white/10">
            <div className="text-sm text-white/85">
              <p>Started: {new Date(path.startedAt).toLocaleDateString()}</p>
              <p>Last activity: {new Date(path.lastActivity).toLocaleDateString()}</p>
            </div>
            <div className="text-sm text-white/85">
              <p>Est. completion: {path.estimatedCompletion}</p>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );

  const renderModules = () => (
    <div className="space-y-4">
      {moduleProgress.map((module, index) => (
        <motion.div
          key={module.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.05 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-4"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="text-2xl">
                {module.status === 'completed' ? '✅' : 
                 module.status === 'in_progress' ? '🔄' : 
                 module.status === 'skipped' ? '⏭️' : '⭕'}
              </div>
              
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-1">
                  <h4 className="text-white font-medium">{module.title}</h4>
                  <span className="text-xs text-white/85">{module.learningPath}</span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[module.status]} bg-white/10`}>
                    {statusLabels[module.status]}
                  </span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm text-white/90">
                  <span>Order: {module.order}</span>
                  <span>Time: {module.timeSpent}</span>
                  {module.overallScore && <span>Score: {module.overallScore}%</span>}
                  <span>Last accessed: {module.lastAccessed}</span>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {module.status !== 'not_started' && (
                <div className="text-right">
                  <div className="w-16 bg-white/20 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(module.progressPercentage)}`}
                      style={{ width: `${module.progressPercentage}%` }}
                    ></div>
                  </div>
                  <span className="text-xs text-white/85 mt-1 block">{module.progressPercentage}%</span>
                </div>
              )}
              
              <button className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white text-sm transition-colors">
                {module.status === 'not_started' ? 'Start' : 
                 module.status === 'in_progress' ? 'Continue' : 'Review'}
              </button>
            </div>
          </div>
          
          {module.status === 'in_progress' && (
            <div className="mt-3 pt-3 border-t border-white/10">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                {module.quizScore && (
                  <div>
                    <span className="text-white/60">Quiz Score:</span>
                    <span className="text-white ml-2">{module.quizScore}%</span>
                  </div>
                )}
                {module.codingScore && (
                  <div>
                    <span className="text-white/60">Coding Score:</span>
                    <span className="text-white ml-2">{module.codingScore}%</span>
                  </div>
                )}
                <div>
                  <span className="text-white/60">Completion Date:</span>
                  <span className="text-white ml-2">
                    {module.completedAt ? new Date(module.completedAt).toLocaleDateString() : 'In Progress'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );

  const renderAnalytics = () => (
    <div className="space-y-8">
      {/* Performance Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
          <h4 className="text-lg font-semibold text-white mb-4">Average Score Trend</h4>
          <div className="h-[200px] flex items-center justify-center text-white/90">
            <div className="text-center">
              <div className="text-3xl mb-2">📈</div>
              <p>Score trend chart</p>
              <p className="text-xs mt-1">Temporarily disabled</p>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
          <h4 className="text-lg font-semibold text-white mb-4">Daily Activity</h4>
          <div className="h-[200px] flex items-center justify-center text-white/90">
            <div className="text-center">
              <div className="text-3xl mb-2">📊</div>
              <p>Daily activity chart</p>
              <p className="text-xs mt-1">Temporarily disabled</p>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
          <h4 className="text-lg font-semibold text-white mb-4">Learning Streaks</h4>
          <div className="flex justify-center items-center h-40">
            <div className="text-center">
              <div className="text-4xl font-bold text-orange-400 mb-2">{stats.currentStreak}</div>
              <div className="text-white/90 text-sm">Current Streak</div>
              <div className="text-2xl font-bold text-white/90 mt-4">{stats.longestStreak}</div>
              <div className="text-white/90 text-sm">Longest Streak</div>
            </div>
          </div>
        </div>
      </div>

      {/* Time Spent Analysis */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Time Spent Analysis</h3>
        <div className="flex items-center justify-center h-[300px] text-center">
          <p className="text-white/90">Chart temporarily disabled due to TypeScript compatibility issues. This will be fixed in a future update.</p>
        </div>
      </div>

      {/* Detailed Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Learning Metrics</h4>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-white/90">Total Modules Completed</span>
              <span className="text-white font-semibold">{stats.totalModulesCompleted}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/90">Total Time Spent</span>
              <span className="text-white font-semibold">{stats.totalTimeSpent}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/90">Average Score</span>
              <span className="text-white font-semibold">{stats.averageScore}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/90">Current Level</span>
              <span className="text-white font-semibold">{stats.level}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-white/90">Total Points</span>
              <span className="text-white font-semibold">{stats.totalPoints}</span>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Goal Progress</h4>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-white/90">Weekly Goal</span>
                <span className="text-white">{stats.weeklyProgress}/{stats.weeklyGoal} modules</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor((stats.weeklyProgress / stats.weeklyGoal) * 100)}`}
                  style={{ width: `${(stats.weeklyProgress / stats.weeklyGoal) * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-white/90">Experience to Next Level</span>
                <span className="text-white">{stats.experienceToNext} XP</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className="h-2 rounded-full bg-gradient-to-r from-purple-400 to-purple-600"
                  style={{ width: `${((1000 - stats.experienceToNext) / 1000) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8" role="main" aria-label="Learning progress tracking and analytics">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">Learning Progress</h1>
        <p className="text-white/90 max-w-2xl mx-auto">
          Track your learning journey and monitor your progress across all modules and learning paths
        </p>
      </motion.div>

      {/* Tab Navigation */}
      <div className="flex justify-center mb-8">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-1">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-6 py-3 rounded-md transition-all duration-300 flex items-center space-x-2 ${
                activeTab === tab.id 
                  ? 'bg-white/20 text-white' 
                  : 'text-white/90 hover:text-white hover:bg-white/10'
              }`}
            >
              <span>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Time Range Selector (for analytics) */}
      {activeTab === 'analytics' && (
        <div className="flex justify-end mb-6">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-1">
            {(['week', 'month', 'year'] as const).map(timeframe => (
              <button
                key={timeframe}
                onClick={() => setSelectedTimeframe(timeframe)}
                className={`px-4 py-2 rounded-md transition-all duration-300 ${
                  selectedTimeframe === timeframe 
                    ? 'bg-white/20 text-white' 
                    : 'text-white/70 hover:text-white'
                }`}
              >
                {timeframe.charAt(0).toUpperCase() + timeframe.slice(1)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Content */}
      <div className="min-h-[600px]">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'paths' && renderLearningPaths()}
        {activeTab === 'modules' && renderModules()}
        {activeTab === 'analytics' && renderAnalytics()}
      </div>

      {isLoading && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white">Loading progress data...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Progress;