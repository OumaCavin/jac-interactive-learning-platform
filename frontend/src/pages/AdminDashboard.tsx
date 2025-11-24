import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  AcademicCapIcon,
  UserGroupIcon,
  DocumentTextIcon,
  PlusIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store';

interface AdminStats {
  totalUsers: number;
  totalPaths: number;
  totalModules: number;
  totalLessons: number;
  activeUsers: number;
  completionRate: number;
}

interface RecentActivity {
  id: string;
  type: 'user_registration' | 'path_completion' | 'module_completion';
  message: string;
  timestamp: string;
  user?: string;
}

const AdminDashboard: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState<AdminStats>({
    totalUsers: 0,
    totalPaths: 0,
    totalModules: 0,
    totalLessons: 0,
    activeUsers: 0,
    completionRate: 0,
  });
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Load admin data (AdminRoute already checked admin privileges)
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setIsLoading(true);
    
    // Mock data - replace with actual API calls
    setTimeout(() => {
      setStats({
        totalUsers: 1247,
        totalPaths: 23,
        totalModules: 156,
        totalLessons: 423,
        activeUsers: 342,
        completionRate: 78.5,
      });
      
      setRecentActivity([
        {
          id: '1',
          type: 'user_registration',
          message: 'New user registered',
          timestamp: '2025-11-23T03:45:00Z',
          user: 'john.doe@example.com',
        },
        {
          id: '2',
          type: 'path_completion',
          message: 'JAC Programming Fundamentals completed',
          timestamp: '2025-11-23T03:30:00Z',
          user: 'jane.smith@example.com',
        },
        {
          id: '3',
          type: 'module_completion',
          message: 'Variables and Data Types module completed',
          timestamp: '2025-11-23T03:15:00Z',
          user: 'alex.johnson@example.com',
        },
      ]);
      
      setIsLoading(false);
    }, 1000);
  };

  // Admin privileges are already checked by AdminRoute component

  const tabs = [
    { id: 'overview', name: 'Overview', icon: ChartBarIcon },
    { id: 'users', name: 'Users', icon: UserGroupIcon },
    { id: 'content', name: 'Content', icon: DocumentTextIcon },
    { id: 'learning', name: 'Learning Paths', icon: AcademicCapIcon },
  ];

  const statCards = [
    {
      name: 'Total Users',
      value: stats.totalUsers,
      change: '+12%',
      changeType: 'increase',
      icon: UserGroupIcon,
    },
    {
      name: 'Learning Paths',
      value: stats.totalPaths,
      change: '+3',
      changeType: 'increase',
      icon: AcademicCapIcon,
    },
    {
      name: 'Total Modules',
      value: stats.totalModules,
      change: '+8',
      changeType: 'increase',
      icon: DocumentTextIcon,
    },
    {
      name: 'Active Users',
      value: stats.activeUsers,
      change: '+5%',
      changeType: 'increase',
      icon: CheckCircleIcon,
    },
  ];

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-3xl font-bold text-gray-900">{stat.value.toLocaleString()}</p>
                <p className={`text-sm ${
                  stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                }`}>
                  {stat.change} from last month
                </p>
              </div>
              <stat.icon className="h-8 w-8 text-gray-400" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        </div>
        <div className="divide-y divide-gray-200">
          {recentActivity.map((activity) => (
            <div key={activity.id} className="px-6 py-4">
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  {activity.type === 'user_registration' && (
                    <UserGroupIcon className="h-5 w-5 text-blue-500" />
                  )}
                  {activity.type === 'path_completion' && (
                    <AcademicCapIcon className="h-5 w-5 text-green-500" />
                  )}
                  {activity.type === 'module_completion' && (
                    <CheckCircleIcon className="h-5 w-5 text-purple-500" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-900">
                    <span className="font-medium">{activity.user}</span> {activity.message}
                  </p>
                  <p className="text-sm text-gray-500">
                    {new Date(activity.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Learning Progress Overview */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Learning Progress Overview</h3>
          <p className="text-sm text-gray-500">Key metrics and performance indicators</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Completion Statistics */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-900">Path Completion Statistics</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Completed Paths</span>
                  <span className="text-sm font-medium">156 users (45.6%)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">In Progress</span>
                  <span className="text-sm font-medium">142 users (41.5%)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Not Started</span>
                  <span className="text-sm font-medium">44 users (12.9%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '45.6%' }} />
                </div>
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-900">Performance Metrics</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Avg. Study Time</span>
                  <span className="text-sm font-medium">4.2 hours per path</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Code Success Rate</span>
                  <span className="text-sm font-medium">92.1%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Module Completion</span>
                  <span className="text-sm font-medium">78.5%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Avg. Score</span>
                  <span className="text-sm font-medium">87.3%</span>
                </div>
              </div>
            </div>

            {/* Engagement Metrics */}
            <div className="space-y-4">
              <h4 className="text-sm font-medium text-gray-900">Engagement Metrics</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Daily Active Users</span>
                  <span className="text-sm font-medium">89 users</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Weekly Active Users</span>
                  <span className="text-sm font-medium">234 users</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Code Submissions</span>
                  <span className="text-sm font-medium">1,247 this week</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Avg. Sessions/Day</span>
                  <span className="text-sm font-medium">2.3 sessions</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderLearningPaths = () => (
    <div className="space-y-6">
      {/* Learning Path Analytics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Completion Rate</p>
              <p className="text-3xl font-bold text-green-600">78.5%</p>
              <p className="text-sm text-gray-500">+5.2% from last month</p>
            </div>
            <CheckCircleIcon className="h-8 w-8 text-green-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Learners</p>
              <p className="text-3xl font-bold text-blue-600">342</p>
              <p className="text-sm text-gray-500">+18 this week</p>
            </div>
            <UserGroupIcon className="h-8 w-8 text-blue-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg. Study Time</p>
              <p className="text-3xl font-bold text-purple-600">4.2h</p>
              <p className="text-sm text-gray-500">per path</p>
            </div>
            <ClockIcon className="h-8 w-8 text-purple-400" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-3xl font-bold text-orange-600">92.1%</p>
              <p className="text-sm text-gray-500">code submissions</p>
            </div>
            <ChartBarIcon className="h-8 w-8 text-orange-400" />
          </div>
        </motion.div>
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Completion Rate Trends */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Completion Rate Trends</h3>
            <p className="text-sm text-gray-500">Monthly progress over time</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {[
                { month: 'Nov 2025', rate: 78.5, users: 342 },
                { month: 'Oct 2025', rate: 73.3, users: 324 },
                { month: 'Sep 2025', rate: 68.1, users: 298 },
                { month: 'Aug 2025', rate: 64.2, users: 287 },
                { month: 'Jul 2025', rate: 59.8, users: 265 },
              ].map((data, index) => (
                <div key={data.month} className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{data.month}</span>
                      <span className="text-gray-600">{data.rate}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${data.rate}%` }}
                        transition={{ delay: index * 0.1 }}
                        className="bg-green-500 h-2 rounded-full"
                      />
                    </div>
                  </div>
                  <span className="ml-4 text-sm text-gray-500">{data.users} users</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Top Performing Paths */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Top Performing Paths</h3>
            <p className="text-sm text-gray-500">Highest completion rates</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {[
                { name: 'JAC Programming Fundamentals', completion: 89.2, learners: 156, rating: 4.8 },
                { name: 'JAC Web Development', completion: 82.7, learners: 143, rating: 4.6 },
                { name: 'Advanced JAC Concepts', completion: 76.4, learners: 89, rating: 4.7 },
                { name: 'JAC Data Structures', completion: 71.8, learners: 67, rating: 4.5 },
              ].map((path, index) => (
                <div key={path.name} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{path.name}</h4>
                    <div className="flex items-center space-x-4 mt-1">
                      <span className="text-sm text-gray-600">{path.learners} learners</span>
                      <div className="flex items-center">
                        <span className="text-sm text-yellow-500">★</span>
                        <span className="text-sm text-gray-600 ml-1">{path.rating}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-green-600">{path.completion}%</p>
                    <p className="text-xs text-gray-500">completion</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Learning Path Management */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-medium text-gray-900">Learning Path Management</h3>
              <p className="text-sm text-gray-500">Manage course structure and content</p>
            </div>
            <div className="flex space-x-2">
              <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
                <PlusIcon className="h-4 w-4" />
                <span>New Path</span>
              </button>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
                <DocumentTextIcon className="h-4 w-4" />
                <span>Bulk Edit</span>
              </button>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Learning Path
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Modules
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Completion Rate
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Learners
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Avg. Score
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {[
                { 
                  name: 'JAC Programming Fundamentals', 
                  modules: 8, 
                  status: 'Published', 
                  completion: 89.2, 
                  learners: 156, 
                  score: 87.3,
                  lastUpdated: '2 hours ago'
                },
                { 
                  name: 'Advanced JAC Concepts', 
                  modules: 12, 
                  status: 'Published', 
                  completion: 76.4, 
                  learners: 89, 
                  score: 82.1,
                  lastUpdated: '1 day ago'
                },
                { 
                  name: 'JAC Web Development', 
                  modules: 15, 
                  status: 'Published', 
                  completion: 82.7, 
                  learners: 143, 
                  score: 84.6,
                  lastUpdated: '3 hours ago'
                },
                { 
                  name: 'JAC Data Structures', 
                  modules: 10, 
                  status: 'Draft', 
                  completion: 0, 
                  learners: 0, 
                  score: 0,
                  lastUpdated: '5 days ago'
                },
              ].map((path, index) => (
                <motion.tr
                  key={path.name}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.1 }}
                  className="hover:bg-gray-50"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{path.name}</div>
                      <div className="text-sm text-gray-500">Updated {path.lastUpdated}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{path.modules} modules</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      path.status === 'Published' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {path.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{path.completion}%</div>
                    <div className="w-full bg-gray-200 rounded-full h-1">
                      <div 
                        className="bg-green-500 h-1 rounded-full"
                        style={{ width: `${path.completion}%` }}
                      />
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{path.learners}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {path.score > 0 ? `${path.score}%` : 'N/A'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900 mr-3">
                      <EyeIcon className="h-4 w-4" />
                    </button>
                    <button className="text-blue-600 hover:text-blue-900 mr-3">
                      <PencilIcon className="h-4 w-4" />
                    </button>
                    <button className="text-green-600 hover:text-green-900 mr-3">
                      <AcademicCapIcon className="h-4 w-4" />
                    </button>
                    <button className="text-red-600 hover:text-red-900">
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Course Structure Editor */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Course Structure</h3>
            <p className="text-sm text-gray-500">Drag to reorder modules</p>
          </div>
          <div className="p-6">
            <div className="space-y-2">
              {[
                { title: 'Module 1: Introduction to JAC', duration: '45 min', status: 'published' },
                { title: 'Module 2: Variables and Data Types', duration: '60 min', status: 'published' },
                { title: 'Module 3: Control Structures', duration: '75 min', status: 'published' },
                { title: 'Module 4: Functions and Methods', duration: '90 min', status: 'draft' },
                { title: 'Module 5: Object-Oriented Programming', duration: '120 min', status: 'draft' },
              ].map((module, index) => (
                <motion.div
                  key={module.title}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-move"
                >
                  <div className="flex items-center space-x-3">
                    <div className="flex-shrink-0">
                      <div className="w-6 h-6 bg-gray-200 rounded flex items-center justify-center text-xs font-medium">
                        {index + 1}
                      </div>
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-900">{module.title}</h4>
                      <p className="text-xs text-gray-500">{module.duration}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      module.status === 'published' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {module.status}
                    </span>
                    <button className="text-gray-400 hover:text-gray-600">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">User Journey Analytics</h3>
            <p className="text-sm text-gray-500">Completion funnel and drop-off points</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {[
                { stage: 'Started Path', users: 342, percentage: 100 },
                { stage: 'Completed Module 1', users: 298, percentage: 87.1 },
                { stage: 'Completed Module 2', users: 267, percentage: 78.1 },
                { stage: 'Completed Module 3', users: 234, percentage: 68.4 },
                { stage: 'Completed Module 4', users: 198, percentage: 57.9 },
                { stage: 'Completed Path', users: 156, percentage: 45.6 },
              ].map((stage, index) => (
                <div key={stage.stage} className="relative">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium text-gray-900">{stage.stage}</span>
                    <span className="text-gray-600">{stage.users} users ({stage.percentage}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${stage.percentage}%` }}
                      transition={{ delay: index * 0.1 }}
                      className="bg-blue-500 h-2 rounded-full"
                    />
                  </div>
                  {index > 0 && (
                    <div className="text-xs text-red-500 mt-1">
                      Drop-off: {Math.round(100 - (stage.percentage))}%
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Performance Insights */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Performance Insights & Recommendations</h3>
          <p className="text-sm text-gray-500">AI-powered analysis and suggestions</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              {
                type: 'warning',
                title: 'High Drop-off Rate',
                description: 'Module 3 has 12.8% drop-off rate. Consider adding more interactive content.',
                action: 'Review Module 3',
                icon: XCircleIcon,
              },
              {
                type: 'success',
                title: 'Popular Content',
                description: 'JAC Programming Fundamentals is the most completed path this month.',
                action: 'View Details',
                icon: CheckCircleIcon,
              },
              {
                type: 'info',
                title: 'Optimization Opportunity',
                description: 'Adding video content could improve completion rates by 15-20%.',
                action: 'Add Videos',
                icon: AcademicCapIcon,
              },
              {
                type: 'warning',
                title: 'Low Engagement',
                description: 'Module 5 needs content enhancement. Users spend 40% less time than average.',
                action: 'Enhance Content',
                icon: ClockIcon,
              },
              {
                type: 'success',
                title: 'High Performance',
                description: 'Average code submission score increased to 87.3% this month.',
                action: 'View Report',
                icon: ChartBarIcon,
              },
              {
                type: 'info',
                title: 'User Feedback',
                description: '23 users requested additional practice exercises for Advanced JAC Concepts.',
                action: 'Add Exercises',
                icon: DocumentTextIcon,
              },
            ].map((insight, index) => (
              <motion.div
                key={insight.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-4 border border-gray-200 rounded-lg"
              >
                <div className="flex items-start space-x-3">
                  <insight.icon className={`h-5 w-5 mt-0.5 ${
                    insight.type === 'warning' ? 'text-yellow-500' :
                    insight.type === 'success' ? 'text-green-500' : 'text-blue-500'
                  }`} />
                  <div className="flex-1">
                    <h4 className="text-sm font-medium text-gray-900">{insight.title}</h4>
                    <p className="text-xs text-gray-600 mt-1">{insight.description}</p>
                    <button className="text-xs text-blue-600 hover:text-blue-800 mt-2">
                      {insight.action} →
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const renderUsers = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">User Management</h2>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
          <PlusIcon className="h-4 w-4" />
          <span>Add User</span>
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex space-x-4">
            <input
              type="text"
              placeholder="Search users..."
              className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
              <option>All Users</option>
              <option>Active</option>
              <option>Inactive</option>
              <option>Administrators</option>
            </select>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Role
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Active
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {/* Mock user data */}
              <tr>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">John Doe</div>
                  <div className="text-sm text-gray-500">john.doe@example.com</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs font-semibold bg-blue-100 text-blue-800 rounded-full">
                    Student
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="px-2 py-1 text-xs font-semibold bg-green-100 text-green-800 rounded-full">
                    Active
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  2 hours ago
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-blue-600 hover:text-blue-900 mr-3">
                    <PencilIcon className="h-4 w-4" />
                  </button>
                  <button className="text-red-600 hover:text-red-900">
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderContent = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Content Management</h2>
        <div className="flex space-x-2">
          <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
            <PlusIcon className="h-4 w-4" />
            <span>New Learning Path</span>
          </button>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
            <PlusIcon className="h-4 w-4" />
            <span>New Module</span>
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Learning Paths */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Learning Paths</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {[
                { name: 'JAC Programming Fundamentals', status: 'Published', modules: 8 },
                { name: 'Advanced JAC Concepts', status: 'Draft', modules: 12 },
                { name: 'JAC Web Development', status: 'Published', modules: 15 },
              ].map((path, index) => (
                <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="font-medium text-gray-900">{path.name}</h4>
                    <p className="text-sm text-gray-500">{path.modules} modules</p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      path.status === 'Published' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {path.status}
                    </span>
                    <button className="text-blue-600 hover:text-blue-900">
                      <EyeIcon className="h-4 w-4" />
                    </button>
                    <button className="text-blue-600 hover:text-blue-900">
                      <PencilIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Content Updates</h3>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {[
                { action: 'Updated', content: 'Variables and Data Types', time: '1 hour ago' },
                { action: 'Created', content: 'Functions Module', time: '3 hours ago' },
                { action: 'Published', content: 'Arrays and Lists', time: '1 day ago' },
              ].map((item, index) => (
                <div key={index} className="flex items-center space-x-3">
                  <ClockIcon className="h-4 w-4 text-gray-400" />
                  <div>
                    <span className="text-sm font-medium text-gray-900">
                      {item.action} {item.content}
                    </span>
                    <p className="text-sm text-gray-500">{item.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
              <p className="mt-1 text-sm text-gray-500">
                Manage users, content, and learning materials
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{user?.first_name} {user?.last_name}</p>
                <p className="text-sm text-gray-500">Administrator</p>
              </div>
              <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center">
                <span className="text-white font-medium">
                  {user?.first_name?.[0]}{user?.last_name?.[0]}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">Loading admin data...</span>
          </div>
        ) : (
          <>
            {activeTab === 'overview' && renderOverview()}
            {activeTab === 'users' && renderUsers()}
            {activeTab === 'content' && renderContent()}
            {activeTab === 'learning' && renderLearningPaths()}
          </>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;