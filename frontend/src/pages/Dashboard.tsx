// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  BookOpenIcon,
  CodeBracketIcon,
  AcademicCapIcon,
  ChartBarIcon,
  ClockIcon,
  TrophyIcon,
  PlayIcon,
  ArrowRightIcon,
  FireIcon,
  StarIcon,
  SignalIcon,
} from '@heroicons/react/24/outline';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';
import { learningService, LearningPath } from '../services/learningService';
import { WebSocketProvider, ConnectionStatus } from '../components/realtime/WebSocketProvider';
import RealTimeDashboard from '../components/realtime/RealTimeDashboard';
// Note: agentService removed to avoid unused import warning
// import { agentService } from './services/agentService';

interface DashboardStats {
  totalModulesCompleted: number;
  totalTimeSpent: number;
  currentStreak: number;
  averageScore: number;
  completedPaths: number;
}

interface RecentActivity {
  id: string;
  type: 'module_completed' | 'code_executed' | 'assessment_completed';
  title: string;
  description: string;
  timestamp: string;
  score?: number;
}

const QuickActions = [
  {
    name: 'Continue Learning',
    description: 'Resume your current module',
    icon: PlayIcon,
    href: '/learning',
    color: 'bg-blue-500',
  },
  {
    name: 'Code Editor',
    description: 'Practice coding',
    icon: CodeBracketIcon,
    href: '/code-editor',
    color: 'bg-green-500',
  },
  {
    name: 'Take Assessment',
    description: 'Test your knowledge',
    icon: AcademicCapIcon,
    href: '/assessments',
    color: 'bg-purple-500',
  },
  {
    name: 'View Progress',
    description: 'Track your achievements',
    icon: ChartBarIcon,
    href: '/progress',
    color: 'bg-orange-500',
  },
];

const StatCard: React.FC<{
  title: string;
  value: string | number;
  subtitle?: string;
  icon: React.ComponentType<any>;
  color: string;
  trend?: { value: number; isPositive: boolean };
}> = ({ title, value, subtitle, icon: Icon, color, trend }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    className="bg-white rounded-lg p-6 shadow-sm border border-gray-200"
  >
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
      </div>
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
    </div>
    {trend && (
      <div className="mt-4 flex items-center">
        <span className={`text-sm font-medium ${
          trend.isPositive ? 'text-green-600' : 'text-red-600'
        }`}>
          {trend.isPositive ? '+' : ''}{trend.value}%
        </span>
        <span className="text-sm text-gray-500 ml-2">from last week</span>
      </div>
    )}
  </motion.div>
);

const RecentActivityCard: React.FC<{ activity: RecentActivity }> = ({ activity }) => {
  const getActivityIcon = () => {
    switch (activity.type) {
      case 'module_completed':
        return <BookOpenIcon className="h-4 w-4 text-green-600" />;
      case 'code_executed':
        return <CodeBracketIcon className="h-4 w-4 text-blue-600" />;
      case 'assessment_completed':
        return <AcademicCapIcon className="h-4 w-4 text-purple-600" />;
      default:
        return <ClockIcon className="h-4 w-4 text-gray-600" />;
    }
  };

  return (
    <motion.div
      whileHover={{ backgroundColor: '#f9fafb' }}
      className="flex items-start space-x-3 p-3 rounded-lg cursor-pointer transition-colors"
    >
      <div className="flex-shrink-0 p-2 bg-gray-50 rounded-lg">
        {getActivityIcon()}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-900">{activity.title}</p>
        <p className="text-sm text-gray-500">{activity.description}</p>
        <div className="flex items-center mt-1">
          <span className="text-xs text-gray-400">{activity.timestamp}</span>
          {activity.score && (
            <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full ml-2">
              {activity.score}% Score
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
};

const LearningPathCard: React.FC<{ path: LearningPath; progress: number }> = ({ 
  path, 
  progress 
}) => (
  <Link to={`/learning/${path.id}`}>
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 cursor-pointer transition-all hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900">{path.title}</h3>
          <p className="text-gray-600 mt-1 text-sm">{path.description}</p>
          
          <div className="flex items-center mt-4 space-x-4">
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              path.difficulty_level === 'beginner' ? 'bg-green-100 text-green-800' :
              path.difficulty_level === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {path.difficulty_level}
            </span>
            
            <div className="flex items-center text-gray-500 text-sm">
              <ClockIcon className="h-4 w-4 mr-1" />
              {path.estimated_duration}min
            </div>
            
            <div className="flex items-center text-gray-500 text-sm">
              <BookOpenIcon className="h-4 w-4 mr-1" />
              {path.modules_count} modules
            </div>
          </div>
        </div>
        
        <div className="ml-4 flex-shrink-0">
          <div className="w-20 h-20 relative">
            <svg className="w-20 h-20 transform -rotate-90">
              <circle
                cx="40"
                cy="40"
                r="36"
                stroke="#e5e7eb"
                strokeWidth="6"
                fill="transparent"
              />
              <circle
                cx="40"
                cy="40"
                r="36"
                stroke="#3b82f6"
                strokeWidth="6"
                fill="transparent"
                strokeDasharray={`${2 * Math.PI * 36}`}
                strokeDashoffset={`${2 * Math.PI * 36 * (1 - progress / 100)}`}
                className="transition-all duration-300"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-sm font-semibold text-gray-900">
                {Math.round(progress)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  </Link>
);

export const Dashboard: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const [stats, setStats] = useState<DashboardStats>({
    totalModulesCompleted: 0,
    totalTimeSpent: 0,
    currentStreak: 0,
    averageScore: 0,
    completedPaths: 0,
  });
  const [recentActivities, setRecentActivities] = useState<RecentActivity[]>([]);
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      
      // Load learning paths
      const paths = await learningService.getLearningPaths();
      setLearningPaths(paths.slice(0, 3)); // Show top 3 paths
      
      // Simulate user stats (in real app, this would come from API)
      setStats({
        totalModulesCompleted: 12,
        totalTimeSpent: 480, // minutes
        currentStreak: 7,
        averageScore: 85,
        completedPaths: 2,
      });
      
      // Mock recent activities
      setRecentActivities([
        {
          id: '1',
          type: 'module_completed',
          title: 'Introduction to JAC',
          description: 'Completed basic JAC syntax module',
          timestamp: '2 hours ago',
          score: 92,
        },
        {
          id: '2',
          type: 'code_executed',
          title: 'Fibonacci Implementation',
          description: 'Executed Python fibonacci code successfully',
          timestamp: '4 hours ago',
        },
        {
          id: '3',
          type: 'assessment_completed',
          title: 'JAC Fundamentals Quiz',
          description: 'Completed first assessment',
          timestamp: '1 day ago',
          score: 88,
        },
      ]);
      
    } catch (error) {
      // Handle dashboard data loading error gracefully
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <WebSocketProvider autoConnect={true}>
      <div className="space-y-8" role="main" aria-label="Learning dashboard and progress overview">
        {/* Welcome Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-2xl p-8 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">
                Welcome back, {user?.first_name || 'Learner'}!
              </h1>
              <p className="text-primary-100 mt-2 text-lg">
                Ready to continue your JAC learning journey?
              </p>
            </div>
            <div className="hidden lg:flex items-center gap-4">
              <ConnectionStatus />
              <div className="flex items-center space-x-2 text-primary-100">
                <FireIcon className="h-5 w-5" />
                <span className="font-semibold">{stats.currentStreak} day streak!</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Real-time Dashboard */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <RealTimeDashboard className="mb-8" />
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard
            title="Modules Completed"
            value={stats.totalModulesCompleted}
            subtitle="out of 45 total"
            icon={BookOpenIcon}
            color="bg-blue-500"
            trend={{ value: 12, isPositive: true }}
          />
          <StatCard
            title="Time Invested"
            value={formatTime(stats.totalTimeSpent)}
            subtitle="this month"
            icon={ClockIcon}
            color="bg-green-500"
            trend={{ value: 8, isPositive: true }}
          />
          <StatCard
            title="Average Score"
            value={`${stats.averageScore}%`}
            subtitle="across all assessments"
            icon={StarIcon}
            color="bg-yellow-500"
            trend={{ value: 5, isPositive: true }}
          />
          <StatCard
            title="Learning Paths"
            value={stats.completedPaths}
            subtitle="paths completed"
            icon={TrophyIcon}
            color="bg-purple-500"
            trend={{ value: 3, isPositive: true }}
          />
        </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {QuickActions.map((action, index) => (
            <Link key={action.name} to={action.href}>
              <motion.div
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="bg-white rounded-lg p-6 shadow-sm border border-gray-200 cursor-pointer transition-all hover:shadow-md group"
              >
                <div className="flex items-center space-x-4">
                  <div className={`p-3 rounded-lg ${action.color}`}>
                    <action.icon className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
                      {action.name}
                    </h3>
                    <p className="text-gray-600 text-sm">{action.description}</p>
                  </div>
                  <ArrowRightIcon className="h-5 w-5 text-gray-400 group-hover:text-primary-600 transition-colors" />
                </div>
              </motion.div>
            </Link>
          ))}
        </div>
      </motion.div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
          </div>
          <div className="p-6">
            <div className="space-y-3">
              {recentActivities.map((activity) => (
                <RecentActivityCard key={activity.id} activity={activity} />
              ))}
            </div>
            <div className="mt-6">
              <Link
                to="/progress"
                className="text-primary-600 hover:text-primary-700 font-medium text-sm flex items-center"
              >
                View all activity
                <ArrowRightIcon className="h-4 w-4 ml-1" />
              </Link>
            </div>
          </div>
        </motion.div>

        {/* Continue Learning */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200"
        >
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Continue Learning</h2>
          </div>
          <div className="p-6">
            {learningPaths.length > 0 ? (
              <div className="space-y-4">
                {learningPaths.map((path) => (
                  <LearningPathCard
                    key={path.id}
                    path={path}
                    progress={Math.random() * 80 + 10} // Mock progress
                  />
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <BookOpenIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No learning paths available
                </h3>
                <p className="text-gray-600 mb-4">
                  Start your learning journey by exploring available paths
                </p>
                <Link
                  to="/learning"
                  className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
                >
                  Browse Paths
                  <ArrowRightIcon className="h-4 w-4 ml-2" />
                </Link>
              </div>
            )}
          </div>
        </motion.div>
      </div>
      </div>
    </WebSocketProvider>
  );
};

export default Dashboard;