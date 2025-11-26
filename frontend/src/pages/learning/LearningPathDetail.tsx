// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  BookOpenIcon,
  ClockIcon,
  StarIcon,
  UserGroupIcon,
  PlayIcon,
  CheckCircleIcon,
  LockClosedIcon,
  AcademicCapIcon,
  CodeBracketIcon,
  ArrowLeftIcon,
  CalendarIcon,
  TrophyIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';
import { learningService, LearningPath, Module } from '../../services/learningService';
import { useSelector } from 'react-redux';
import { selectUser } from '../../store/slices/authSlice';
import { toast } from 'react-hot-toast';

// Mock data for enhanced learning path experience
const MOCK_MODULES: Module[] = [
  {
    id: 1,
    learning_path: 1,
    title: 'Introduction to Variables',
    description: 'Learn about variable declaration, naming conventions, and basic data types in JAC',
    content: 'Variables are containers for storing data values...',
    order_index: 1,
    estimated_duration: 30,
    module_type: 'lesson',
    prerequisites: [],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 2,
    learning_path: 1,
    title: 'Data Types and Operations',
    description: 'Explore different data types and how to perform operations on them',
    content: 'JAC supports various data types including...',
    order_index: 2,
    estimated_duration: 45,
    module_type: 'lesson',
    prerequisites: [1],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 3,
    learning_path: 1,
    title: 'Control Structures',
    description: 'Master if statements, loops, and conditional logic',
    content: 'Control structures help you make decisions...',
    order_index: 3,
    estimated_duration: 60,
    module_type: 'lesson',
    prerequisites: [2],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 4,
    learning_path: 1,
    title: 'Functions and Methods',
    description: 'Create reusable code blocks with functions',
    content: 'Functions allow you to organize and reuse code...',
    order_index: 4,
    estimated_duration: 50,
    module_type: 'exercise',
    prerequisites: [3],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 5,
    learning_path: 1,
    title: 'Arrays and Collections',
    description: 'Work with collections of data using arrays',
    content: 'Arrays help you store multiple values...',
    order_index: 5,
    estimated_duration: 40,
    module_type: 'lesson',
    prerequisites: [4],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 6,
    learning_path: 1,
    title: 'Object-Oriented Programming',
    description: 'Learn OOP concepts with classes and objects',
    content: 'OOP helps you organize code into objects...',
    order_index: 6,
    estimated_duration: 90,
    module_type: 'lesson',
    prerequisites: [5],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 7,
    learning_path: 1,
    title: 'Advanced Topics',
    description: 'Explore advanced JAC programming concepts',
    content: 'Advanced topics include...',
    order_index: 7,
    estimated_duration: 75,
    module_type: 'assessment',
    prerequisites: [6],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: 8,
    learning_path: 1,
    title: 'Final Project',
    description: 'Apply everything you learned in a comprehensive project',
    content: 'Build a complete application...',
    order_index: 8,
    estimated_duration: 120,
    module_type: 'exercise',
    prerequisites: [7],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

interface ModuleProgress {
  id: number;
  status: 'not_started' | 'in_progress' | 'completed';
  time_spent: number;
  attempts: number;
  score?: number;
  last_accessed: string;
  completed_at?: string;
}

const MockModuleProgress: ModuleProgress[] = [
  { id: 1, status: 'completed', time_spent: 35, attempts: 1, score: 95, last_accessed: '2025-11-20', completed_at: '2025-11-20' },
  { id: 2, status: 'completed', time_spent: 42, attempts: 1, score: 88, last_accessed: '2025-11-20', completed_at: '2025-11-20' },
  { id: 3, status: 'in_progress', time_spent: 15, attempts: 1, last_accessed: '2025-11-21' },
  { id: 4, status: 'not_started', time_spent: 0, attempts: 0, last_accessed: '' },
  { id: 5, status: 'not_started', time_spent: 0, attempts: 0, last_accessed: '' },
  { id: 6, status: 'not_started', time_spent: 0, attempts: 0, last_accessed: '' },
  { id: 7, status: 'not_started', time_spent: 0, attempts: 0, last_accessed: '' },
  { id: 8, status: 'not_started', time_spent: 0, attempts: 0, last_accessed: '' },
];

const LearningPathDetail: React.FC = () => {
  const { pathId } = useParams<{ pathId: string }>();
  const navigate = useNavigate();
  const user = useSelector(selectUser);
  
  const [learningPath, setLearningPath] = useState<LearningPath | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [moduleProgress, setModuleProgress] = useState<ModuleProgress[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'modules' | 'progress'>('overview');

  // Mock learning path data
  const mockLearningPath: LearningPath = {
    id: parseInt(pathId || '1'),
    title: 'JAC Programming Fundamentals',
    description: 'Master the basics of JAC programming language with hands-on exercises and real-world projects. This comprehensive course covers variables, data types, control structures, functions, and object-oriented programming concepts.',
    difficulty_level: 'beginner',
    estimated_duration: 450,
    modules_count: 8,
    rating: 4.8,
    created_at: '2025-01-01',
    updated_at: '2025-11-20',
  };

  useEffect(() => {
    loadLearningPathData();
  }, [pathId]);

  const loadLearningPathData = async () => {
    try {
      setIsLoading(true);
      
      // Simulate API calls with mock data
      setLearningPath(mockLearningPath);
      setModules(MOCK_MODULES);
      setModuleProgress(MockModuleProgress);
      
      // In a real app, you would call:
      // const path = await learningService.getLearningPath(parseInt(pathId!));
      // const pathModules = await learningService.getModules(parseInt(pathId!));
      // setLearningPath(path);
      // setModules(pathModules);
      
    } catch (error) {
      console.error('Failed to load learning path:', error);
      toast.error('Failed to load learning path');
    } finally {
      setIsLoading(false);
    }
  };

  const getModuleProgress = (moduleId: number) => {
    return moduleProgress.find(p => p.id === moduleId);
  };

  const getModuleStatus = (module: Module) => {
    const progress = getModuleProgress(module.id);
    if (!progress) return 'not_started';
    
    // Check prerequisites
    const prerequisitesMet = module.prerequisites.every(prereqId => {
      const prereqProgress = getModuleProgress(prereqId);
      return prereqProgress?.status === 'completed';
    });
    
    if (!prerequisitesMet) return 'locked';
    return progress.status;
  };

  const isModuleUnlocked = (module: Module) => {
    if (module.prerequisites.length === 0) return true;
    return module.prerequisites.every(prereqId => {
      const prereqProgress = getModuleProgress(prereqId);
      return prereqProgress?.status === 'completed';
    });
  };

  const getOverallProgress = () => {
    const completedModules = moduleProgress.filter(p => p.status === 'completed').length;
    return modules.length > 0 ? (completedModules / modules.length) * 100 : 0;
  };

  const getTotalTimeSpent = () => {
    return moduleProgress.reduce((total, progress) => total + progress.time_spent, 0);
  };

  const getAverageScore = () => {
    const scores = moduleProgress
      .filter(p => p.score !== undefined)
      .map(p => p.score!);
    
    return scores.length > 0 ? scores.reduce((sum, score) => sum + score, 0) / scores.length : 0;
  };

  const handleStartLearning = (moduleId: number) => {
    navigate(`/learning/${pathId}/module/${moduleId}`);
  };

  const getModuleTypeIcon = (type: string) => {
    switch (type) {
      case 'lesson': return <BookOpenIcon className="w-5 h-5" />;
      case 'exercise': return <CodeBracketIcon className="w-5 h-5" />;
      case 'assessment': return <AcademicCapIcon className="w-5 h-5" />;
      default: return <BookOpenIcon className="w-5 h-5" />;
    }
  };

  const getModuleTypeColor = (type: string) => {
    switch (type) {
      case 'lesson': return 'bg-blue-100 text-blue-800';
      case 'exercise': return 'bg-green-100 text-green-800';
      case 'assessment': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'in_progress': return <PlayIcon className="w-5 h-5 text-blue-500" />;
      case 'locked': return <LockClosedIcon className="w-5 h-5 text-gray-400" />;
      default: return <ClockIcon className="w-5 h-5 text-gray-400" />;
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
      </div>
    );
  }

  if (!learningPath) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Learning Path Not Found</h1>
          <p className="text-gray-600 mb-6">The learning path you're looking for doesn't exist.</p>
          <Link to="/learning" className="text-blue-600 hover:text-blue-800">
            ← Back to Learning Paths
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      {/* Header */}
      <div className="mb-8">
        <Link 
          to="/learning" 
          className="inline-flex items-center text-blue-600 hover:text-blue-800 mb-4"
        >
          <ArrowLeftIcon className="w-4 h-4 mr-2" />
          Back to Learning Paths
        </Link>
        
        <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-4">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                learningPath.difficulty_level === 'beginner' ? 'bg-green-100 text-green-800' :
                learningPath.difficulty_level === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {learningPath.difficulty_level.charAt(0).toUpperCase() + learningPath.difficulty_level.slice(1)}
              </span>
              
              <div className="flex items-center gap-1">
                <StarIcon className="w-4 h-4 text-yellow-500 fill-current" />
                <span className="text-sm text-gray-600">{learningPath.rating}</span>
              </div>
            </div>
            
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{learningPath.title}</h1>
            <p className="text-gray-600 text-lg leading-relaxed">{learningPath.description}</p>
          </div>
          
          {/* Quick Stats */}
          <div className="bg-white rounded-lg border border-gray-200 p-6 min-w-64">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress Overview</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Completion</span>
                <span className="font-semibold">{getOverallProgress().toFixed(0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${getOverallProgress()}%` }}
                />
              </div>
              <div className="flex items-center justify-between text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <ClockIcon className="w-4 h-4" />
                  <span>{getTotalTimeSpent()}min / {learningPath.estimated_duration}min</span>
                </div>
                <div className="flex items-center gap-1">
                  <TrophyIcon className="w-4 h-4" />
                  <span>{getAverageScore().toFixed(0)}% avg</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-8">
        <nav className="flex space-x-8">
          {[
            { id: 'overview', label: 'Overview', icon: <BookOpenIcon className="w-4 h-4" /> },
            { id: 'modules', label: 'Modules', icon: <CodeBracketIcon className="w-4 h-4" /> },
            { id: 'progress', label: 'Progress', icon: <ChartBarIcon className="w-4 h-4" /> },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center gap-2 py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.icon}
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Course Info */}
            <div className="lg:col-span-2 space-y-8">
              {/* What You'll Learn */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">What You'll Learn</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {[
                    'Variable declaration and data types',
                    'Control structures and loops',
                    'Functions and code organization',
                    'Object-oriented programming concepts',
                    'Working with arrays and collections',
                    'Error handling and debugging',
                  ].map((skill, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <CheckCircleIcon className="w-5 h-5 text-green-500" />
                      <span className="text-gray-700">{skill}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Prerequisites */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Prerequisites</h3>
                <div className="space-y-2">
                  <p className="text-gray-600">• Basic understanding of programming concepts</p>
                  <p className="text-gray-600">• Familiarity with command line interfaces</p>
                  <p className="text-gray-600">• No prior JAC experience required</p>
                </div>
              </div>

              {/* Course Structure */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Course Structure</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Total Modules</span>
                    <span className="font-semibold">{learningPath.modules_count}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Estimated Duration</span>
                    <span className="font-semibold">{learningPath.estimated_duration} minutes</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600">Skill Level</span>
                    <span className="font-semibold capitalize">{learningPath.difficulty_level}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Enroll Card */}
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                <h3 className="text-lg font-semibold mb-2">Ready to Start?</h3>
                <p className="text-blue-100 mb-4">
                  Begin your journey to master JAC programming
                </p>
                <button
                  onClick={() => {
                    const firstModule = modules.find(m => isModuleUnlocked(m));
                    if (firstModule) {
                      handleStartLearning(firstModule.id);
                    }
                  }}
                  className="w-full bg-white text-blue-600 font-semibold py-3 px-4 rounded-lg hover:bg-blue-50 transition-colors"
                >
                  Continue Learning
                </button>
              </div>

              {/* Recent Activity */}
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  {moduleProgress
                    .filter(p => p.last_accessed)
                    .sort((a, b) => new Date(b.last_accessed).getTime() - new Date(a.last_accessed).getTime())
                    .slice(0, 3)
                    .map((progress) => {
                      const module = modules.find(m => m.id === progress.id);
                      return (
                        <div key={progress.id} className="flex items-center gap-3">
                          <div className="w-2 h-2 bg-blue-500 rounded-full" />
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900">
                              {module?.title || `Module ${progress.id}`}
                            </p>
                            <p className="text-xs text-gray-500">
                              {new Date(progress.last_accessed).toLocaleDateString()}
                            </p>
                          </div>
                        </div>
                      );
                    })}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'modules' && (
          <div className="space-y-4">
            {modules.map((module, index) => {
              const progress = getModuleProgress(module.id);
              const status = getModuleStatus(module);
              const unlocked = isModuleUnlocked(module);

              return (
                <motion.div
                  key={module.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-lg border border-gray-200 overflow-hidden"
                >
                  <div className="p-6">
                    <div className="flex items-start gap-4">
                      {/* Module Number & Icon */}
                      <div className="flex-shrink-0">
                        <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                          status === 'completed' ? 'bg-green-100' :
                          status === 'in_progress' ? 'bg-blue-100' :
                          unlocked ? 'bg-gray-100' : 'bg-gray-50'
                        }`}>
                          {getStatusIcon(status)}
                        </div>
                        <div className="text-center mt-2">
                          <span className="text-xs font-medium text-gray-500">Module {module.order_index}</span>
                        </div>
                      </div>

                      {/* Module Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-2">
                          <h3 className={`text-lg font-semibold ${
                            !unlocked ? 'text-gray-400' : 'text-gray-900'
                          }`}>
                            {module.title}
                          </h3>
                          
                          <div className="flex items-center gap-2 ml-4">
                            <span className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium ${getModuleTypeColor(module.module_type)}`}>
                              {getModuleTypeIcon(module.module_type)}
                              {module.module_type}
                            </span>
                          </div>
                        </div>

                        <p className={`text-sm mb-4 ${
                          !unlocked ? 'text-gray-400' : 'text-gray-600'
                        }`}>
                          {module.description}
                        </p>

                        <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                          <div className="flex items-center gap-1">
                            <ClockIcon className="w-4 h-4" />
                            <span>{module.estimated_duration} min</span>
                          </div>
                          
                          {progress && (
                            <>
                              <div className="flex items-center gap-1">
                                <UserGroupIcon className="w-4 h-4" />
                                <span>{progress.attempts} attempts</span>
                              </div>
                              
                              {progress.score && (
                                <div className="flex items-center gap-1">
                                  <TrophyIcon className="w-4 h-4" />
                                  <span>{progress.score}% score</span>
                                </div>
                              )}
                            </>
                          )}
                        </div>

                        {/* Progress Bar */}
                        {progress && progress.status !== 'not_started' && (
                          <div className="mb-4">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full transition-all duration-300 ${
                                  progress.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
                                }`}
                                style={{ 
                                  width: progress.status === 'completed' ? '100%' : 
                                         progress.status === 'in_progress' ? '50%' : '0%' 
                                }}
                              />
                            </div>
                          </div>
                        )}

                        {/* Action Button */}
                        <button
                          onClick={() => unlocked && handleStartLearning(module.id)}
                          disabled={!unlocked}
                          className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                            !unlocked
                              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                              : status === 'completed'
                              ? 'bg-green-100 text-green-800 hover:bg-green-200'
                              : status === 'in_progress'
                              ? 'bg-blue-100 text-blue-800 hover:bg-blue-200'
                              : 'bg-blue-600 text-white hover:bg-blue-700'
                          }`}
                        >
                          {status === 'completed' ? 'Review' :
                           status === 'in_progress' ? 'Continue' :
                           status === 'locked' ? 'Locked' : 'Start'}
                          {status !== 'locked' && <PlayIcon className="w-4 h-4" />}
                        </button>
                      </div>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}

        {activeTab === 'progress' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Progress Stats */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Learning Statistics</h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600 mb-1">
                    {moduleProgress.filter(p => p.status === 'completed').length}
                  </div>
                  <div className="text-sm text-gray-600">Completed Modules</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600 mb-1">
                    {getAverageScore().toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600">Average Score</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600 mb-1">
                    {getTotalTimeSpent()}
                  </div>
                  <div className="text-sm text-gray-600">Minutes Spent</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600 mb-1">
                    {getOverallProgress().toFixed(0)}%
                  </div>
                  <div className="text-sm text-gray-600">Overall Progress</div>
                </div>
              </div>
            </div>

            {/* Module Progress Chart */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">Module Progress</h3>
              <div className="space-y-4">
                {modules.map((module) => {
                  const progress = getModuleProgress(module.id);
                  const percentage = progress?.status === 'completed' ? 100 :
                                   progress?.status === 'in_progress' ? 50 : 0;
                  
                  return (
                    <div key={module.id} className="flex items-center gap-4">
                      <div className="w-16 text-sm text-gray-600 font-medium">
                        M{module.order_index}
                      </div>
                      <div className="flex-1">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full transition-all duration-300 ${
                              progress?.status === 'completed' ? 'bg-green-500' :
                              progress?.status === 'in_progress' ? 'bg-blue-500' : 'bg-gray-300'
                            }`}
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                      <div className="w-12 text-sm text-gray-600 text-right">
                        {percentage}%
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default LearningPathDetail;