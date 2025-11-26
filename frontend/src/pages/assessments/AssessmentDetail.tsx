// JAC Learning Platform - TypeScript utilities by Cavin Otieno

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useSelector, useDispatch } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { authService } from '../../services/authService';
import { 
  fetchQuiz,
  startQuizAttempt,
  submitQuizAttempt,
  selectAssessmentLoading,
  selectAssessmentSubmitting
} from '../../store/slices/assessmentSlice';
import { learningService } from '../../services/learningService';
import { apiClient } from '../../services/apiClient';

// Types
interface Question {
  id: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer' | 'code_completion' | 'jac_specific';
  question: string;
  options?: string[];
  correct_answer: string | string[];
  explanation?: string;
  jac_concept?: string;
  difficulty: 1 | 2 | 3 | 4 | 5;
  points: number;
}

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
  questions: Question[];
  created_at: string;
  updated_at: string;
}

interface QuizResult {
  id: string;
  score: number;
  maxScore: number;
  percentage: number;
  passed: boolean;
  timeTaken: number; // in minutes
  answers: { [questionId: string]: string | string[] };
  feedback: string;
  detailedResults: {
    questionId: string;
    userAnswer: string | string[];
    correctAnswer: string | string[];
    isCorrect: boolean;
    points: number;
    explanation?: string;
  }[];
}

// API service for assessments
const assessmentService = {
  getQuiz: async (quizId: string): Promise<any> => {
    return await learningService.getQuiz(quizId);
  },
  
  getQuizQuestions: async (moduleId?: string): Promise<Question[]> => {
    const response = await learningService.getAssessmentQuestions(moduleId);
    return response;
  },
  
  startAttempt: async (quizId: string): Promise<any> => {
    // Create attempt via Redux thunk
    const result = await dispatch(startQuizAttempt(quizId)).unwrap();
    return result;
  },
  
  submitAttempt: async (attemptId: string, answers: any): Promise<any> => {
    // Submit attempt via Redux thunk
    const result = await dispatch(submitQuizAttempt({ attemptId, answers })).unwrap();
    return result;
  }
};

const AssessmentDetail: React.FC = () => {
  const { assessmentId } = useParams<{ assessmentId: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<{ [questionId: string]: string | string[] }>({});
  const [timeRemaining, setTimeRemaining] = useState<number | undefined>(undefined);
  const [isTimerActive, setIsTimerActive] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [selectedOptions, setSelectedOptions] = useState<{ [key: string]: Set<number> }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentAttempt, setCurrentAttempt] = useState<any>(null);
  
  const user = useSelector((state: any) => state.auth.user) || authService.getCurrentUser();
  const isLoading = useSelector(selectAssessmentLoading);
  const isAttemptSubmitting = useSelector(selectAssessmentSubmitting);

  useEffect(() => {
    // Load assessment data from backend
    loadAssessmentData();
  }, [assessmentId]);

  const loadAssessmentData = async () => {
    if (!assessmentId) {
      setError('Assessment ID is required');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Load quiz data from backend
      const quizData = await assessmentService.getQuiz(assessmentId);
      
      // Transform backend data to frontend format if needed
      const transformedQuiz: Quiz = {
        id: quizData.id,
        title: quizData.title,
        description: quizData.description,
        learning_path: quizData.learning_path,
        module: quizData.module,
        difficulty: quizData.difficulty_level || 'medium', // Map backend field
        time_limit: quizData.time_limit,
        max_attempts: quizData.max_attempts,
        passing_score: quizData.passing_score,
        created_at: quizData.created_at,
        updated_at: quizData.updated_at,
        questions: transformQuestions(quizData.questions || [])
      };

      setQuiz(transformedQuiz);

      // Initialize timer if quiz has time limit
      if (transformedQuiz.time_limit && !showResults) {
        setTimeRemaining(transformedQuiz.time_limit * 60); // Convert to seconds
        setIsTimerActive(true);
      }

      // Start a new attempt
      try {
        const attemptData = await assessmentService.startAttempt(assessmentId);
        setCurrentAttempt(attemptData);
      } catch (attemptError) {
        console.warn('Failed to start attempt:', attemptError);
        // Continue without attempt for now - user can start attempt manually
      }
      
    } catch (error: any) {
      console.error('Failed to load assessment:', error);
      setError(error.response?.data?.detail || 'Failed to load assessment');
      toast.error('Failed to load assessment');
    } finally {
      setLoading(false);
    }
  };

  const transformQuestions = (backendQuestions: any[]): Question[] => {
    return backendQuestions.map(q => ({
      id: q.question_id || q.id,
      type: mapQuestionType(q.question_type),
      question: q.question_text,
      options: q.options || [],
      correct_answer: q.correct_answer,
      explanation: q.explanation,
      jac_concept: q.tags?.[0] || '', // Use first tag as concept
      difficulty: q.difficulty_level === 'easy' ? 1 : q.difficulty_level === 'medium' ? 2 : 3,
      points: q.points
    }));
  };

  const mapQuestionType = (backendType: string): Question['type'] => {
    const typeMap: { [key: string]: Question['type'] } = {
      'multiple_choice': 'multiple_choice',
      'true_false': 'true_false',
      'short_answer': 'short_answer',
      'code_question': 'code_completion',
      'essay': 'short_answer'
    };
    return typeMap[backendType] || 'multiple_choice';
  };

  useEffect(() => {
    // Timer countdown
    let interval: NodeJS.Timeout;
    if (isTimerActive && timeRemaining && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev && prev <= 1) {
            setIsTimerActive(false);
            if (currentAttempt) {
              handleSubmitQuiz();
            }
            return 0;
          }
          return prev ? prev - 1 : 0;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isTimerActive, timeRemaining, currentAttempt]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const currentQuestion = quiz.questions[currentQuestionIndex];

  const handleAnswerChange = (questionId: string, value: string | string[]) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleMultipleChoiceChange = (questionId: string, optionIndex: number) => {
    setSelectedOptions(prev => {
      const current = prev[questionId] || new Set<number>();
      const newSet = new Set(current);
      
      if (newSet.has(optionIndex)) {
        newSet.delete(optionIndex);
      } else {
        newSet.add(optionIndex);
      }
      
      return {
        ...prev,
        [questionId]: newSet
      };
    });

    // Convert Set to Array for storage
    const selected = selectedOptions[questionId] || new Set<number>();
    const values = Array.from(selected).map(i => quiz.questions.find(q => q.id === questionId)?.options?.[i] || '');
    handleAnswerChange(questionId, values);
  };

  const handleMultipleSelectChange = (questionId: string, optionIndex: number) => {
    handleMultipleChoiceChange(questionId, optionIndex);
  };

  const handleNext = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmitQuiz = async () => {
    if (!currentAttempt || !quiz) {
      toast.error('No active attempt found');
      return;
    }

    setIsSubmitting(true);
    setIsTimerActive(false);

    try {
      // Submit attempt to backend
      const result = await assessmentService.submitAttempt(currentAttempt.attempt_id, answers);
      
      // Transform backend result to frontend format
      const quizResult: QuizResult = {
        id: result.attempt_id,
        score: result.score || 0,
        maxScore: result.max_score || 100,
        percentage: result.score || 0,
        passed: result.is_passed || false,
        timeTaken: result.duration_minutes || 0,
        answers: result.answers || {},
        feedback: result.feedback || '',
        detailedResults: transformDetailedResults(result.feedback || {})
      };

      setQuizResult(quizResult);
      setShowResults(true);
      
      if (quizResult.passed) {
        toast.success('🎉 Congratulations! You passed the assessment!');
      } else {
        toast.error(`You scored ${quizResult.percentage}%. You can retake this assessment.`);
      }
    } catch (error: any) {
      console.error('Error submitting quiz:', error);
      const errorMessage = error.response?.data?.detail || 'Failed to submit assessment. Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  const transformDetailedResults = (backendFeedback: any): QuizResult['detailedResults'] => {
    return Object.entries(backendFeedback).map(([questionId, feedback]: [string, any]) => ({
      questionId,
      userAnswer: feedback.user_answer || '',
      correctAnswer: feedback.correct_answer || '',
      isCorrect: feedback.is_correct || false,
      points: feedback.points_earned || 0,
      explanation: feedback.explanation
    }));
  };

  const handleRetakeQuiz = () => {
    setCurrentQuestionIndex(0);
    setAnswers({});
    setSelectedOptions({});
    setTimeRemaining(quiz.time_limit ? quiz.time_limit * 60 : undefined);
    setIsTimerActive(!!quiz.time_limit);
    setShowResults(false);
    setQuizResult(null);
    // Reload data for new attempt
    loadAssessmentData();
  };

  const getAnsweredCount = () => {
    return Object.keys(answers).length;
  };

  const getUnansweredCount = () => {
    return quiz.questions.length - getAnsweredCount();
  };

  const currentQuestion = quiz.questions[currentQuestionIndex];

  // Loading state
  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white">Loading assessment...</p>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !quiz) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <div className="text-6xl mb-4">❌</div>
          <h1 className="text-2xl font-bold text-white mb-4">Assessment Not Found</h1>
          <p className="text-white/80 mb-6">{error || 'The requested assessment could not be found.'}</p>
          <button
            onClick={() => navigate('/assessments')}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
          >
            ← Back to Assessments
          </button>
        </div>
      </div>
    );
  }

  const renderQuestion = (question: Question, index: number) => {
    const userAnswer = answers[question.id];
    const selected = selectedOptions[question.id] || new Set<number>();

    return (
      <motion.div
        key={question.id}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="bg-white/10 backdrop-blur-lg rounded-lg p-6"
        role="article"
        aria-label={`Question ${index + 1} of ${quiz.questions.length}`}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-white">
            Question {index + 1} of {quiz.questions.length}
          </h3>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-white/70" aria-label={`Question worth ${question.points} points`}>
              {question.points} points
            </span>
            <span className={`px-2 py-1 rounded-full text-xs bg-gradient-to-r ${
              question.difficulty <= 2 ? 'from-green-400 to-green-600' :
              question.difficulty <= 3 ? 'from-yellow-400 to-yellow-600' :
              'from-red-400 to-red-600'
            } text-white`}
                  aria-label={`Difficulty level: ${question.difficulty} out of 5`}>
              Difficulty: {question.difficulty}
            </span>
          </div>
        </div>

        <p className="text-white mb-6 whitespace-pre-line">{question.question}</p>

        <div className="space-y-3">
          {question.type === 'multiple_choice' && question.options && (
            <div className="space-y-2">
              {question.options.map((option, optionIndex) => (
                <label
                  key={optionIndex}
                  className="flex items-center space-x-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
                >
                  <input
                    type="radio"
                    name={question.id}
                    value={option}
                    checked={userAnswer === option}
                    onChange={() => handleAnswerChange(question.id, option)}
                    className="text-blue-500"
                  />
                  <span className="text-white">{option}</span>
                </label>
              ))}
            </div>
          )}

          {question.type === 'true_false' && (
            <div className="space-y-2">
              {['true', 'false'].map((option) => (
                <label
                  key={option}
                  className="flex items-center space-x-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
                >
                  <input
                    type="radio"
                    name={question.id}
                    value={option}
                    checked={userAnswer === option}
                    onChange={() => handleAnswerChange(question.id, option)}
                    className="text-blue-500"
                  />
                  <span className="text-white capitalize">{option}</span>
                </label>
              ))}
            </div>
          )}

          {question.type === 'short_answer' && (
            <textarea
              value={userAnswer as string || ''}
              onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              placeholder="Type your answer here..."
              className="w-full h-32 bg-white/10 border border-white/20 rounded-lg px-3 py-2 text-white placeholder-white/50"
            />
          )}

          {question.type === 'code_completion' && (
            <div className="space-y-2">
              <textarea
                value={userAnswer as string || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                placeholder="Write your JAC code here..."
                className="w-full h-40 bg-gray-900 border border-white/20 rounded-lg px-3 py-2 text-white font-mono placeholder-white/50"
              />
              <p className="text-sm text-white/60">
                Write complete JAC code for this problem.
              </p>
            </div>
          )}

          {question.type === 'jac_specific' && question.options && (
            <div className="space-y-2">
              {question.options.map((option, optionIndex) => (
                <label
                  key={optionIndex}
                  className="flex items-center space-x-3 p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors"
                >
                  <input
                    type="radio"
                    name={question.id}
                    value={option}
                    checked={userAnswer === option}
                    onChange={() => handleAnswerChange(question.id, option)}
                    className="text-blue-500"
                  />
                  <span className="text-white">{option}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        {question.jac_concept && (
          <div className="mt-4 p-3 bg-blue-500/20 rounded-lg">
            <p className="text-sm text-blue-200">
              <strong>JAC Concept:</strong> {question.jac_concept.replace('_', ' ')}
            </p>
          </div>
        )}
      </motion.div>
    );
  };

  const renderResults = () => {
    if (!quizResult) return null;

    return (
      <div className="space-y-6">
        {/* Results Header */}
        <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
          <div className="text-6xl mb-4">
            {quizResult.passed ? '🎉' : '📝'}
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">
            {quizResult.passed ? 'Congratulations!' : 'Assessment Complete'}
          </h2>
          <p className="text-white/80 mb-4">{quizResult.feedback}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white/10 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{quizResult.percentage}%</div>
              <div className="text-sm text-white/70">Score</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{quizResult.score}/{quizResult.maxScore}</div>
              <div className="text-sm text-white/70">Points</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">
                {Math.round(quizResult.timeTaken)} min
              </div>
              <div className="text-sm text-white/70">Time Taken</div>
            </div>
            <div className="bg-white/10 rounded-lg p-4">
              <div className={`text-2xl font-bold ${quizResult.passed ? 'text-green-400' : 'text-red-400'}`}>
                {quizResult.passed ? 'PASS' : 'FAIL'}
              </div>
              <div className="text-sm text-white/70">Result</div>
            </div>
          </div>

          <div className="mt-6">
            <button
              onClick={handleRetakeQuiz}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
            >
              Retake Assessment
            </button>
          </div>
        </div>

        {/* Detailed Results */}
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-white">Detailed Results</h3>
          
          {quizResult.detailedResults.map((result, index) => {
            const question = quiz.questions.find(q => q.id === result.questionId);
            if (!question) return null;

            return (
              <div
                key={result.questionId}
                className={`bg-white/10 backdrop-blur-lg rounded-lg p-6 ${
                  result.isCorrect ? 'border-l-4 border-green-400' : 'border-l-4 border-red-400'
                }`}
              >
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-white font-medium">
                    Question {index + 1}: {question.question.substring(0, 100)}...
                  </h4>
                  <div className="flex items-center space-x-2">
                    <span className={`text-lg ${result.isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                      {result.isCorrect ? '✅' : '❌'}
                    </span>
                    <span className="text-white/70 text-sm">
                      {result.points}/{question.points} points
                    </span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div>
                    <span className="text-white/70">Your answer: </span>
                    <span className={`${result.isCorrect ? 'text-green-400' : 'text-red-400'}`}>
                      {Array.isArray(result.userAnswer) 
                        ? result.userAnswer.join(', ') 
                        : result.userAnswer || 'No answer'}
                    </span>
                  </div>
                  
                  {!result.isCorrect && (
                    <div>
                      <span className="text-white/70">Correct answer: </span>
                      <span className="text-green-400">
                        {Array.isArray(result.correctAnswer) 
                          ? result.correctAnswer.join(', ') 
                          : result.correctAnswer}
                      </span>
                    </div>
                  )}
                  
                  {result.explanation && (
                    <div className="mt-3 p-3 bg-blue-500/20 rounded-lg">
                      <span className="text-blue-200 font-medium">Explanation: </span>
                      <span className="text-blue-100">{result.explanation}</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  if (showResults) {
    return (
      <div className="container mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4">Assessment Results</h1>
            <p className="text-white/80">{quiz.title}</p>
          </div>
          {renderResults()}
        </motion.div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8" role="main" aria-label="Assessment detail page">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">{quiz.title}</h1>
        <p className="text-white/80 mb-4">{quiz.description}</p>
        
        <div className="flex items-center justify-center space-x-6 text-sm">
          <span className="text-white/70" aria-label={`Total questions: ${quiz.questions.length}`}>
            {quiz.questions.length} questions
          </span>
          <span className="text-white/70" aria-label={`Total points: ${quiz.questions.reduce((sum, q) => sum + q.points, 0)}`}>
            {quiz.questions.reduce((sum, q) => sum + q.points, 0)} total points
          </span>
          {quiz.time_limit && (
            <span className={`font-medium ${timeRemaining && timeRemaining < 300 ? 'text-red-400' : 'text-white'}`} 
                  aria-label={`Time remaining: ${timeRemaining ? formatTime(timeRemaining) : formatTime(quiz.time_limit * 60)}`}>
              ⏱️ {timeRemaining ? formatTime(timeRemaining) : formatTime(quiz.time_limit * 60)}
            </span>
          )}
          <span className={`px-3 py-1 rounded-full text-xs bg-gradient-to-r ${quiz.difficulty === 'easy' ? 'from-green-400 to-green-600' : quiz.difficulty === 'medium' ? 'from-yellow-400 to-yellow-600' : 'from-red-400 to-red-600'} text-white`}
                aria-label={`Difficulty level: ${quiz.difficulty}`}>
            {quiz.difficulty.toUpperCase()}
          </span>
        </div>
      </motion.div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-white/70 mb-2">
          <span>Progress</span>
          <span>{currentQuestionIndex + 1} of {quiz.questions.length}</span>
        </div>
        <div className="w-full bg-white/20 rounded-full h-2">
          <div 
            className="h-2 rounded-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / quiz.questions.length) * 100}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-white/60 mt-1">
          <span>{getAnsweredCount()} answered</span>
          <span>{getUnansweredCount()} remaining</span>
        </div>
      </div>

      {/* Question */}
      {renderQuestion(currentQuestion, currentQuestionIndex)}

      {/* Navigation */}
      <div className="flex items-center justify-between mt-8">
        <button
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            currentQuestionIndex === 0
              ? 'bg-white/10 text-white/40 cursor-not-allowed'
              : 'bg-white/10 hover:bg-white/20 text-white'
          }`}
        >
          ← Previous
        </button>

        <div className="flex items-center space-x-4">
          {currentQuestionIndex === quiz.questions.length - 1 ? (
            <button
              onClick={handleSubmitQuiz}
              disabled={isSubmitting}
              className="px-8 py-3 bg-green-500 hover:bg-green-600 disabled:bg-green-500/50 text-white rounded-lg font-medium transition-colors"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Assessment'}
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
            >
              Next →
            </button>
          )}
        </div>
      </div>

      {/* Question Overview (Mini Navigation) */}
      <div className="mt-8 bg-white/10 backdrop-blur-lg rounded-lg p-6">
        <h3 className="text-white font-medium mb-4">Question Overview</h3>
        <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
          {quiz.questions.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentQuestionIndex(index)}
              className={`w-10 h-10 rounded-lg font-medium text-sm transition-colors ${
                index === currentQuestionIndex
                  ? 'bg-blue-500 text-white'
                  : answers[quiz.questions[index].id]
                  ? 'bg-green-500/20 text-green-400 border border-green-400/50'
                  : 'bg-white/10 text-white/70 hover:bg-white/20'
              }`}
            >
              {index + 1}
            </button>
          ))}
        </div>
      </div>

      {isSubmitting && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
            <p className="text-white">Submitting your assessment...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AssessmentDetail;