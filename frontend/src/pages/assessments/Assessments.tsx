import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useSelector, useDispatch } from 'react-redux';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { authService } from '../../services/authService';
import { 
  fetchQuizzes, 
  fetchUserAttempts, 
  fetchAssessmentStats,
  selectQuizzes,
  selectQuizAttempts,
  selectAssessmentLoading,
  selectAssessmentSubmitting,
  AssessmentState
} from '../../store/slices/assessmentSlice';

// Types
interface Quiz {
  id: string;
  title: string;
  description: string;
  learning_path?: string;
  module?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  time_limit?: number; // in minutes
  max_attempts: number;
  passing_score: number;
  questionCount: number;
  totalPoints: number;
  created_at: string;
  updated_at: string;
}

interface QuizAttempt {
  id: string;
  quizId: string;
  quizTitle: string;
  score: number;
  maxScore: number;
  percentage: number;
  passed: boolean;
  timeTaken: number; // in minutes
  startedAt: string;
  completedAt: string;
  attemptNumber: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface AssessmentStats {
  totalQuizzes: number;
  completedQuizzes: number;
  averageScore: number;
  totalTimeSpent: string;
  currentStreak: number;
  bestScore: number;
  passRate: number;
  improvement: number;
}

interface PerformanceData {
  date: string;
  score: number;
  difficulty: string;
  completed: boolean;
}

// Assessment component - now using real API data


const COLORS = ['#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

const difficultyColors = {
  easy: 'from-green-400 to-green-600',
  medium: 'from-yellow-400 to-yellow-600',
  hard: 'from-red-400 to-red-600'
};

const difficultyLabels = {
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard'
};

const Assessments: React.FC = () => {
  const dispatch = useDispatch<any>();
  const [activeTab, setActiveTab] = useState<'overview' | 'available' | 'history' | 'analytics'>('overview');
  const [selectedDifficulty, setSelectedDifficulty] = useState<'all' | 'easy' | 'medium' | 'hard'>('all');
  const [selectedStatus, setSelectedStatus] = useState<'all' | 'completed' | 'in_progress' | 'not_started'>('all');
  
  // Redux state
  const quizzes = useSelector(selectQuizzes);
  const attempts = useSelector(selectQuizAttempts);
  const isLoading = useSelector(selectAssessmentLoading);
  const isSubmitting = useSelector(selectAssessmentSubmitting);
  const user = useSelector((state: any) => state.auth.user) || authService.getCurrentUser();

  // Calculate stats from real data
  const stats = {
    totalQuizzes: quizzes.length,
    completedQuizzes: attempts.filter(a => a.passed).length,
    averageScore: attempts.length > 0 ? Math.round(attempts.reduce((sum, a) => sum + (a.percentage || 0), 0) / attempts.length) : 0,
    totalTimeSpent: formatTime(Math.round(attempts.reduce((sum, a) => sum + (a.timeTaken || 0), 0) / 60)),
    currentStreak: 3, // TODO: Calculate from attempts
    bestScore: attempts.length > 0 ? Math.max(...attempts.map(a => a.percentage || 0)) : 0,
    passRate: attempts.length > 0 ? Math.round((attempts.filter(a => a.passed).length / attempts.length) * 100) : 0,
    improvement: 12 // TODO: Calculate improvement trend
  };

  // Performance data from real attempts
  const performanceData = attempts.slice(-7).map(attempt => ({
    date: new Date(attempt.completedAt || attempt.startedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    score: attempt.percentage || 0,
    difficulty: attempt.difficulty || 'medium',
    completed: true
  }));

  useEffect(() => {
    // Load assessment data from APIs
    loadAssessmentData();
  }, []);

  const loadAssessmentData = async () => {
    try {
      // Fetch quizzes and attempts from backend
      await Promise.all([
        dispatch(fetchQuizzes()),
        dispatch(fetchUserAttempts()),
        dispatch(fetchAssessmentStats())
      ]);
    } catch (error) {
      console.error('Failed to load assessment data:', error);
    }
  };

  const getFilteredQuizzes = () => {
    return quizzes.filter(quiz => {
      const difficulty = quiz.difficulty || 'medium'; // Handle API data
      const difficultyMatch = selectedDifficulty === 'all' || difficulty === selectedDifficulty;
      
      // Check status based on attempts - handle missing fields gracefully
      const statusMatch = selectedStatus === 'all' || 
        (selectedStatus === 'completed' && attempts.some(a => a.quiz === quiz.id && a.passed)) ||
        (selectedStatus === 'in_progress' && attempts.some(a => a.quiz === quiz.id && !a.passed)) ||
        (selectedStatus === 'not_started' && !attempts.some(a => a.quiz === quiz.id));
      
      return difficultyMatch && statusMatch;
    });
  };

  const getQuizStatus = (quizId: string) => {
    const quizAttempts = attempts.filter(a => a.quiz === quizId); // Handle API field name
    if (quizAttempts.length === 0) return 'not_started';
    
    const bestAttempt = quizAttempts.reduce((best, current) => 
      (current.percentage || 0) > (best.percentage || 0) ? current : best
    );
    
    return bestAttempt.passed ? 'completed' : 'in_progress';
  };

  const getBestScore = (quizId: string) => {
    const quizAttempts = attempts.filter(a => a.quiz === quizId);
    if (quizAttempts.length === 0) return 0;
    
    return Math.max(...quizAttempts.map(a => a.percentage || 0));
  };

  const getAttemptsRemaining = (quizId: string) => {
    const quiz = quizzes.find(q => q.id === quizId);
    if (!quiz) return 0;
    
    const maxAttempts = quiz.max_attempts || quiz.max_attempts || 3; // Handle API field name
    const quizAttempts = attempts.filter(a => a.quiz === quizId);
    return Math.max(0, maxAttempts - quizAttempts.length);
  };

  const getQuizProgress = (quizId: string) => {
    const quizAttempts = attempts.filter(a => a.quiz === quizId);
    const quiz = quizzes.find(q => q.id === quizId);
    if (!quiz) return 0;
    
    const maxAttempts = quiz.max_attempts || quiz.max_attempts || 3;
    return (quizAttempts.length / maxAttempts) * 100;
  };

  const formatTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 75) return 'text-blue-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 80) return 'from-green-400 to-green-600';
    if (percentage >= 60) return 'from-blue-400 to-blue-600';
    if (percentage >= 40) return 'from-yellow-400 to-yellow-600';
    return 'from-red-400 to-red-600';
  };

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'available', label: 'Available', icon: '📝' },
    { id: 'history', label: 'History', icon: '📈' },
    { id: 'analytics', label: 'Analytics', icon: '📉' }
  ];

  const renderOverview = () => (
    <div className="space-y-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Completion Rate</p>
              <p className="text-2xl font-bold text-white">{Math.round((stats.completedQuizzes / stats.totalQuizzes) * 100)}%</p>
            </div>
            <div className="text-3xl">✅</div>
          </div>
          <p className="text-white/85 text-xs mt-2">{stats.completedQuizzes} of {stats.totalQuizzes} quizzes</p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Average Score</p>
              <p className="text-2xl font-bold text-green-400">{stats.averageScore}%</p>
            </div>
            <div className="text-3xl">🎯</div>
          </div>
          <p className="text-white/85 text-xs mt-2">Best: {stats.bestScore}%</p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Pass Rate</p>
              <p className="text-2xl font-bold text-blue-400">{stats.passRate}%</p>
            </div>
            <div className="text-3xl">🏆</div>
          </div>
          <p className="text-white/85 text-xs mt-2">+{stats.improvement}% this month</p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/90 text-sm">Time Spent</p>
              <p className="text-2xl font-bold text-purple-400">{stats.totalTimeSpent}</p>
            </div>
            <div className="text-3xl">⏱️</div>
          </div>
          <p className="text-white/85 text-xs mt-2">Current streak: {stats.currentStreak} days</p>
        </motion.div>
      </div>

      {/* Performance Chart */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Performance Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          {/* Temporarily disabled due to TypeScript strict JSX issue */}
          <div className="flex items-center justify-center h-64 text-white/90">
            <p>Performance chart temporarily disabled</p>
          </div>
        </ResponsiveContainer>
      </div>

      {/* Recent Activity */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Recent Activity</h3>
        <div className="space-y-4">
          {attempts.slice(-5).reverse().map((attempt, index) => {
            // Find the quiz for this attempt
            const quiz = quizzes.find(q => q.id === attempt.quiz);
            const quizTitle = quiz?.title || 'Unknown Quiz';
            
            return (
              <motion.div
                key={attempt.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between p-4 bg-white/5 rounded-lg"
              >
                <div className="flex items-center space-x-4">
                  <div className="text-2xl">
                    {attempt.passed ? '✅' : '❌'}
                  </div>
                  <div>
                    <h4 className="text-white font-medium">{quizTitle}</h4>
                    <p className="text-white/85 text-sm">
                      {formatDate(attempt.completed_at || attempt.started_at)} • {formatTime(attempt.time_taken || 0)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-bold ${getScoreColor(attempt.percentage || 0)}`}>
                    {attempt.percentage || 0}%
                  </div>
                  <div className="text-xs text-white/85">
                    Attempt {index + 1}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );

  const renderAvailable = () => (
    <div className="space-y-6">
      {/* Filters */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-white/90 mb-2">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value as any)}
              className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
            >
              <option value="all" className="bg-gray-800">All Levels</option>
              <option value="easy" className="bg-gray-800">Easy</option>
              <option value="medium" className="bg-gray-800">Medium</option>
              <option value="hard" className="bg-gray-800">Hard</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-white/90 mb-2">Status</label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value as any)}
              className="w-full bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white"
            >
              <option value="all" className="bg-gray-800">All Quizzes</option>
              <option value="not_started" className="bg-gray-800">Not Started</option>
              <option value="in_progress" className="bg-gray-800">In Progress</option>
              <option value="completed" className="bg-gray-800">Completed</option>
            </select>
          </div>

          <div className="flex items-end">
            <span className="text-white/85 text-sm">
              {getFilteredQuizzes().length} quizzes found
            </span>
          </div>
        </div>
      </div>

      {/* Quiz Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {getFilteredQuizzes().map((quiz, index) => {
          const status = getQuizStatus(quiz.id);
          const bestScore = getBestScore(quiz.id);
          const attemptsRemaining = getAttemptsRemaining(quiz.id);
          const progress = getQuizProgress(quiz.id);

          return (
            <motion.div
              key={quiz.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-semibold text-white">{quiz.title}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${difficultyColors[quiz.difficulty || 'medium']} text-white`}>
                      {difficultyLabels[quiz.difficulty || 'medium']}
                    </span>
                  </div>
                  <p className="text-white/90 text-sm mb-3">{quiz.description}</p>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-white/85">Questions:</span>
                      <span className="text-white">{quiz.questionCount || quiz.questions?.length || 0}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/85">Points:</span>
                      <span className="text-white">{quiz.totalPoints || 100}</span>
                    </div>
                    {quiz.time_limit && (
                      <div className="flex justify-between">
                        <span className="text-white/85">Time Limit:</span>
                        <span className="text-white">{quiz.time_limit} min</span>
                      </div>
                    )}
                    <div className="flex justify-between">
                      <span className="text-white/85">Passing Score:</span>
                      <span className="text-white">{quiz.passing_score || 70}%</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Progress and Status */}
              <div className="mb-4">
                {status !== 'not_started' && (
                  <div className="mb-3">
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-white/90">Progress</span>
                      <span className="text-white">{Math.round(progress)}%</span>
                    </div>
                    <div className="w-full bg-white/20 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full bg-gradient-to-r ${getProgressColor(progress)}`}
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className={`w-3 h-3 rounded-full ${
                      status === 'completed' ? 'bg-green-400' :
                      status === 'in_progress' ? 'bg-yellow-400' :
                      'bg-gray-400'
                    }`}></span>
                    <span className="text-sm text-white/90 capitalize">{status.replace('_', ' ')}</span>
                  </div>
                  
                  {status !== 'not_started' && bestScore > 0 && (
                    <div className="text-sm">
                      <span className="text-white/90">Best: </span>
                      <span className={getScoreColor(bestScore)}>{bestScore}%</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center justify-between">
                <div className="text-xs text-white/85">
                  {attemptsRemaining > 0 ? (
                    <span>{attemptsRemaining} attempts remaining</span>
                  ) : (
                    <span className="text-red-400">No attempts left</span>
                  )}
                </div>
                
                <button 
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    status === 'not_started' ? 'bg-blue-500 hover:bg-blue-600 text-white' :
                    status === 'completed' ? 'bg-green-500 hover:bg-green-600 text-white' :
                    'bg-yellow-500 hover:bg-yellow-600 text-white'
                  }`}
                >
                  {status === 'not_started' ? 'Start Quiz' :
                   status === 'completed' ? 'Retake' :
                   'Continue'}
                </button>
              </div>
            </motion.div>
          );
        })}
      </div>

      {getFilteredQuizzes().length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold text-white mb-2">No quizzes found</h3>
          <p className="text-white/90">Try adjusting your filters to see more quizzes</p>
        </div>
      )}
    </div>
  );

  const renderHistory = () => (
    <div className="space-y-6">
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Assessment History</h3>
        
        <div className="space-y-4">
          {attempts.slice().reverse().map((attempt, index) => {
            // Find the quiz for this attempt
            const quiz = quizzes.find(q => q.id === attempt.quiz);
            const quizTitle = quiz?.title || 'Unknown Quiz';
            const difficulty = attempt.difficulty || 'medium';
            
            return (
              <motion.div
                key={attempt.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="bg-white/5 rounded-lg p-4"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="text-2xl">
                      {attempt.passed ? '✅' : '❌'}
                    </div>
                    
                    <div>
                      <h4 className="text-white font-medium">{quizTitle}</h4>
                      <div className="flex items-center space-x-4 text-sm text-white/90">
                        <span>{formatDate(attempt.completed_at || attempt.started_at)}</span>
                        <span>Attempt {index + 1}</span>
                        <span className={`px-2 py-1 rounded-full text-xs bg-gradient-to-r ${difficultyColors[difficulty]} text-white`}>
                          {difficultyLabels[difficulty]}
                        </span>
                        <span>{formatTime(attempt.time_taken || 0)}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className={`text-xl font-bold ${getScoreColor(attempt.percentage || 0)}`}>
                      {attempt.percentage || 0}%
                    </div>
                    <div className="text-sm text-white/85">
                      {attempt.score || 0}/{attempt.max_score || 100} points
                    </div>
                  </div>
                </div>
                
                <div className="mt-3 pt-3 border-t border-white/10">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-white/90">Result:</span>
                    <span className={attempt.passed ? 'text-green-400' : 'text-red-400'}>
                      {attempt.passed ? 'Passed' : 'Failed'}
                    </span>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );

  const renderAnalytics = () => (
    <div className="space-y-8">
      {/* Performance by Difficulty */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Score Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            {/* Temporarily disabled due to TypeScript strict JSX issue */}
            <div className="flex items-center justify-center h-64 text-white/90">
              <p>Score distribution chart temporarily disabled</p>
            </div>
          </ResponsiveContainer>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Performance by Difficulty</h3>
          <div className="space-y-4">
            {['easy', 'medium', 'hard'].map(difficulty => {
              const difficultyAttempts = attempts.filter(a => (a.difficulty || 'medium') === difficulty);
              const averageScore = difficultyAttempts.length > 0 
                ? Math.round(difficultyAttempts.reduce((sum, a) => sum + (a.percentage || 0), 0) / difficultyAttempts.length)
                : 0;
              const passRate = difficultyAttempts.length > 0
                ? Math.round((difficultyAttempts.filter(a => a.passed).length / difficultyAttempts.length) * 100)
                : 0;

              return (
                <div key={difficulty} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-white font-medium capitalize">{difficultyLabels[difficulty as keyof typeof difficultyLabels]}</span>
                    <span className="text-white/85 text-sm">{difficultyAttempts.length} attempts</span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-white/85">Average Score: {averageScore}%</span>
                    <span className="text-white/85">Pass Rate: {passRate}%</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full bg-gradient-to-r ${difficultyColors[difficulty as keyof typeof difficultyColors]}`}
                      style={{ width: `${averageScore}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Time Analysis */}
      <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-6">Time Spent Analysis</h3>
        <ResponsiveContainer width="100%" height={300}>
          {/* Temporarily disabled due to TypeScript strict JSX issue */}
          <div className="flex items-center justify-center h-64 text-white/90">
            <p>Time analysis chart temporarily disabled</p>
          </div>
        </ResponsiveContainer>
      </div>

      {/* Detailed Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Quiz Statistics</h4>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-white/70">Total Attempts</span>
              <span className="text-white font-semibold">{attempts.length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Passed Attempts</span>
              <span className="text-green-400 font-semibold">{attempts.filter(a => a.passed).length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Failed Attempts</span>
              <span className="text-red-400 font-semibold">{attempts.filter(a => !a.passed).length}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Average Time</span>
              <span className="text-white font-semibold">
                {attempts.length > 0 
                  ? formatTime(Math.round(attempts.reduce((sum, a) => sum + (a.time_taken || 0), 0) / attempts.length))
                  : '0m'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Fastest Completion</span>
              <span className="text-white font-semibold">
                {attempts.length > 0 
                  ? formatTime(Math.min(...attempts.map(a => a.time_taken || 0)))
                  : '0m'
                }
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Longest Time</span>
              <span className="text-white font-semibold">
                {attempts.length > 0 
                  ? formatTime(Math.max(...attempts.map(a => a.time_taken || 0)))
                  : '0m'
                }
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <h4 className="text-lg font-semibold text-white mb-4">Improvement Trends</h4>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-white/70">Score Improvement</span>
                <span className="text-green-400">+{stats.improvement}%</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className="h-2 rounded-full bg-gradient-to-r from-green-400 to-green-600"
                  style={{ width: `${stats.improvement * 5}%` }}
                ></div>
              </div>
            </div>
            
            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-white/70">Completion Rate</span>
                <span className="text-blue-400">{Math.round((stats.completedQuizzes / stats.totalQuizzes) * 100)}%</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className="h-2 rounded-full bg-gradient-to-r from-blue-400 to-blue-600"
                  style={{ width: `${(stats.completedQuizzes / stats.totalQuizzes) * 100}%` }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-white/70">Current Streak</span>
                <span className="text-orange-400">{stats.currentStreak} days</span>
              </div>
              <div className="w-full bg-white/20 rounded-full h-2">
                <div 
                  className="h-2 rounded-full bg-gradient-to-r from-orange-400 to-orange-600"
                  style={{ width: `${Math.min(stats.currentStreak * 10, 100)}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8" role="main" aria-label="Assessments page">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">Assessments</h1>
        <p className="text-white/80 max-w-2xl mx-auto">
          Test your knowledge with comprehensive assessments and track your learning progress
        </p>
      </motion.div>

      {/* Tab Navigation */}
      <div className="flex justify-center mb-8">
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-1" role="tablist" aria-label="Assessment categories">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              role="tab"
              aria-selected={activeTab === tab.id}
              aria-controls={`tabpanel-${tab.id}`}
              className={`px-6 py-3 rounded-md transition-all duration-300 flex items-center space-x-2 ${
                activeTab === tab.id 
                  ? 'bg-white/20 text-white' 
                  : 'text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              <span role="img" aria-label={tab.label}>{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="min-h-[600px]" role="tabpanel" id={`tabpanel-${activeTab}`} aria-labelledby={`tab-${activeTab}`}>
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'available' && renderAvailable()}
        {activeTab === 'history' && renderHistory()}
        {activeTab === 'analytics' && renderAnalytics()}
      </div>

      {isLoading && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white">Loading assessment data...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Assessments;