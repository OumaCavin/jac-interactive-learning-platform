/**
 * Predictive Analytics Frontend Components - JAC Learning Platform
 * 
 * React components for displaying machine learning predictions and advanced analytics.
 * 
 * Author: Cavin Otieno
 * Created: 2025-11-26
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadialBarChart, RadialBar } from 'recharts';
import { apiClient } from '../services/apiClient';

// Predictive Analytics Types
interface MLPrediction {
  ensemble_prediction: {
    ensemble_predictions: number[];
    ensemble_weights: Record<string, number>;
    confidence: number;
  };
  prediction_confidence: number;
  prediction_horizon_days: number;
  model_count: number;
  data_points_used: number;
  features_engineered: number;
  ml_predictions: Record<string, any>;
}

interface HistoricalTrends {
  trends_analysis: {
    basic_trends: {
      trend: string;
      first_half_average: number;
      second_half_average: number;
      improvement_rate: number;
    };
    performance_trajectory: {
      trajectory: string;
      slope: number;
      r_squared: number;
      statistical_significance: boolean;
      predicted_next_score: number;
    };
    velocity_trends: {
      velocity: string;
      rate_per_week: number;
      peak_week: string;
      total_completions: number;
    };
  };
  analysis_period_days: number;
  data_quality_score: number;
  recommendations: string[];
}

interface AdaptivePrediction {
  user_pattern_analysis: {
    patterns: string;
    user_type: string;
  };
  optimal_model: string;
  adaptive_parameters: Record<string, any>;
  adaptive_predictions: Record<string, any>;
  model_performance: {
    performance: string;
    accuracy: number;
  };
  adaptation_strategy: string;
}

interface ConfidenceAnalysis {
  confidence_analysis: {
    basic_confidence: {
      confidence: number;
      method: string;
    };
    model_uncertainty: {
      uncertainty: string;
      model_stability: string;
    };
    data_uncertainty: {
      uncertainty: string;
      data_quality: string;
    };
  };
  confidence_level: number;
  sample_size: number;
  statistical_significance: string;
}

interface ComprehensivePredictiveData {
  ml_predictions: MLPrediction;
  historical_trends: HistoricalTrends;
  adaptive_predictions: AdaptivePrediction;
  confidence_analysis: ConfidenceAnalysis;
  summary_insights: {
    overall_prediction_confidence: string;
    learning_trajectory: string;
    recommendation_priority: string;
    key_insights: string[];
    action_items: string[];
  };
}

// Service functions
export const predictiveAnalyticsService = {
  async getMLPredictions(learningPathId?: string, predictionHorizonDays: number = 30): Promise<MLPrediction> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    params.append('prediction_horizon_days', predictionHorizonDays.toString());
    
    const response = await apiClient.get<{success: boolean; data: MLPrediction}>(`/api/v1/predict/ml/?${params}`);
    return response.data;
  },

  async getHistoricalTrends(learningPathId?: string, analysisPeriodDays: number = 90): Promise<HistoricalTrends> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    params.append('analysis_period_days', analysisPeriodDays.toString());
    
    const response = await apiClient.get<{success: boolean; data: HistoricalTrends}>(`/api/v1/predict/trends/?${params}`);
    return response.data;
  },

  async getAdaptivePredictions(learningPathId?: string): Promise<AdaptivePrediction> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    
    const response = await apiClient.get<{success: boolean; data: AdaptivePrediction}>(`/api/v1/predict/adaptive/?${params}`);
    return response.data;
  },

  async getConfidenceCalculations(learningPathId?: string, confidenceLevel: number = 0.95): Promise<ConfidenceAnalysis> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    params.append('confidence_level', confidenceLevel.toString());
    
    const response = await apiClient.get<{success: boolean; data: ConfidenceAnalysis}>(`/api/v1/predict/confidence/?${params}`);
    return response.data;
  },

  async getComprehensivePredictive(
    learningPathId?: string,
    predictionHorizonDays: number = 30,
    analysisPeriodDays: number = 90,
    confidenceLevel: number = 0.95
  ): Promise<ComprehensivePredictiveData> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    params.append('prediction_horizon_days', predictionHorizonDays.toString());
    params.append('analysis_period_days', analysisPeriodDays.toString());
    params.append('confidence_level', confidenceLevel.toString());
    
    const response = await apiClient.get<{success: boolean; data: ComprehensivePredictiveData}>(`/api/v1/predict/comprehensive/?${params}`);
    return response.data;
  },

  async getPredictiveDashboard(learningPathId?: string, includeCharts: boolean = true): Promise<any> {
    const params = new URLSearchParams();
    if (learningPathId) params.append('learning_path_id', learningPathId);
    params.append('include_charts', includeCharts.toString());
    
    const response = await apiClient.get<{success: boolean; data: any}>(`/api/v1/predict/dashboard/?${params}`);
    return response.data;
  }
};

// Main Predictive Analytics Component
export const PredictiveAnalytics: React.FC<{
  learningPathId?: string;
  onDataUpdate?: (data: ComprehensivePredictiveData) => void;
}> = ({ learningPathId, onDataUpdate }) => {
  const [data, setData] = useState<ComprehensivePredictiveData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [predictionHorizon, setPredictionHorizon] = useState(30);
  const [analysisPeriod, setAnalysisPeriod] = useState(90);

  useEffect(() => {
    loadPredictiveData();
  }, [learningPathId, predictionHorizon, analysisPeriod]);

  const loadPredictiveData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const predictiveData = await predictiveAnalyticsService.getComprehensivePredictive(
        learningPathId,
        predictionHorizon,
        analysisPeriod
      );
      
      setData(predictiveData);
      onDataUpdate?.(predictiveData);
    } catch (err: any) {
      console.error('Failed to load predictive analytics:', err);
      setError(err.message || 'Failed to load predictive analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-white/90">Loading predictive analytics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
        <p className="text-red-400">Error: {error}</p>
        <button 
          onClick={loadPredictiveData}
          className="mt-2 px-4 py-2 bg-red-500/20 text-red-300 rounded hover:bg-red-500/30"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center text-white/70">
        <p>No predictive data available</p>
      </div>
    );
  }

  const { ml_predictions, historical_trends, confidence_analysis, summary_insights } = data;

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="flex flex-wrap gap-4 items-center justify-between bg-white/5 rounded-lg p-4">
        <div className="flex gap-4">
          <div>
            <label className="block text-sm text-white/70 mb-1">Prediction Horizon (days)</label>
            <select 
              value={predictionHorizon} 
              onChange={(e) => setPredictionHorizon(Number(e.target.value))}
              className="bg-white/10 border border-white/20 rounded px-3 py-1 text-white"
            >
              <option value={7}>7 days</option>
              <option value={14}>14 days</option>
              <option value={30}>30 days</option>
              <option value={60}>60 days</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-white/70 mb-1">Analysis Period (days)</label>
            <select 
              value={analysisPeriod} 
              onChange={(e) => setAnalysisPeriod(Number(e.target.value))}
              className="bg-white/10 border border-white/20 rounded px-3 py-1 text-white"
            >
              <option value={30}>30 days</option>
              <option value={60}>60 days</option>
              <option value={90}>90 days</option>
              <option value={180}>180 days</option>
            </select>
          </div>
        </div>
        <button 
          onClick={loadPredictiveData}
          className="px-4 py-2 bg-blue-500/20 text-blue-300 rounded hover:bg-blue-500/30"
        >
          Refresh Data
        </button>
      </div>

      {/* Summary Insights */}
      <div className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20 rounded-lg p-6">
        <h3 className="text-xl font-semibold text-white mb-4">Predictive Insights Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-400">
              {summary_insights.overall_prediction_confidence.toUpperCase()}
            </div>
            <div className="text-white/70 text-sm">Prediction Confidence</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-400">
              {summary_insights.learning_trajectory.toUpperCase()}
            </div>
            <div className="text-white/70 text-sm">Learning Trajectory</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-400">
              {summary_insights.recommendation_priority.toUpperCase()}
            </div>
            <div className="text-white/70 text-sm">Priority Level</div>
          </div>
        </div>
        
        {summary_insights.key_insights.length > 0 && (
          <div className="mb-4">
            <h4 className="text-lg font-medium text-white mb-2">Key Insights</h4>
            <ul className="space-y-1">
              {summary_insights.key_insights.map((insight, index) => (
                <li key={index} className="text-white/80 text-sm flex items-start">
                  <span className="text-purple-400 mr-2">•</span>
                  {insight}
                </li>
              ))}
            </ul>
          </div>
        )}
        
        {summary_insights.action_items.length > 0 && (
          <div>
            <h4 className="text-lg font-medium text-white mb-2">Recommended Actions</h4>
            <ul className="space-y-1">
              {summary_insights.action_items.map((action, index) => (
                <li key={index} className="text-white/80 text-sm flex items-start">
                  <span className="text-green-400 mr-2">→</span>
                  {action}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* ML Predictions Chart */}
      <MLPredictionsChart data={ml_predictions} />

      {/* Historical Trends */}
      <HistoricalTrendsChart data={historical_trends} />

      {/* Confidence Analysis */}
      <ConfidenceAnalysisChart data={confidence_analysis} />

      {/* Model Performance Metrics */}
      <ModelPerformanceMetrics data={data} />
    </div>
  );
};

// ML Predictions Chart Component
const MLPredictionsChart: React.FC<{ data: MLPrediction }> = ({ data }) => {
  const { ensemble_prediction, prediction_confidence, model_count } = data;
  const predictions = ensemble_prediction.ensemble_predictions || [];

  const chartData = predictions.map((pred, index) => ({
    day: index + 1,
    prediction: pred,
    upper_bound: pred * 1.1,
    lower_bound: pred * 0.9
  }));

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-white">Machine Learning Predictions</h3>
        <div className="text-right">
          <div className="text-white/70 text-sm">Confidence: {Math.round(prediction_confidence * 100)}%</div>
          <div className="text-white/70 text-sm">Models Used: {model_count}</div>
        </div>
      </div>
      
      <div className="h-[300px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="day" stroke="rgba(255,255,255,0.7)" />
            <YAxis stroke="rgba(255,255,255,0.7)" domain={[0, 100]} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(0,0,0,0.8)', 
                border: '1px solid rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
            />
            <Area 
              type="monotone" 
              dataKey="upper_bound" 
              stackId="1" 
              stroke="rgba(59, 130, 246, 0.3)" 
              fill="rgba(59, 130, 246, 0.1)" 
            />
            <Area 
              type="monotone" 
              dataKey="lower_bound" 
              stackId="1" 
              stroke="rgba(59, 130, 246, 0.3)" 
              fill="rgba(59, 130, 246, 0.1)" 
            />
            <Line 
              type="monotone" 
              dataKey="prediction" 
              stroke="#3b82f6" 
              strokeWidth={3}
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

// Historical Trends Chart Component
const HistoricalTrendsChart: React.FC<{ data: HistoricalTrends }> = ({ data }) => {
  const { trends_analysis, data_quality_score } = data;
  const basic_trends = trends_analysis.basic_trends;
  const performance_trajectory = trends_analysis.performance_trajectory;

  const trendData = [
    {
      period: 'First Half',
      score: basic_trends.first_half_average,
      color: '#ef4444'
    },
    {
      period: 'Second Half', 
      score: basic_trends.second_half_average,
      color: '#22c55e'
    },
    {
      period: 'Predicted Next',
      score: performance_trajectory.predicted_next_score,
      color: '#3b82f6'
    }
  ];

  const getTrajectoryColor = (trajectory: string) => {
    switch (trajectory) {
      case 'improving': return 'text-green-400';
      case 'declining': return 'text-red-400';
      default: return 'text-yellow-400';
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-white">Historical Trends Analysis</h3>
        <div className="text-right">
          <div className="text-white/70 text-sm">Data Quality: {Math.round(data_quality_score * 100)}%</div>
          <div className={`text-sm font-medium ${getTrajectoryColor(performance_trajectory.trajectory)}`}>
            {performance_trajectory.trajectory.toUpperCase()} trajectory
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trend Comparison Bar Chart */}
        <div>
          <h4 className="text-lg font-medium text-white mb-3">Performance Comparison</h4>
          <div className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="period" stroke="rgba(255,255,255,0.7)" />
                <YAxis stroke="rgba(255,255,255,0.7)" domain={[0, 100]} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(0,0,0,0.8)', 
                    border: '1px solid rgba(255,255,255,0.2)',
                    borderRadius: '8px',
                    color: 'white'
                  }}
                />
                <Bar dataKey="score" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Trend Metrics */}
        <div className="space-y-4">
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-medium mb-2">Trend Metrics</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-white/70">Improvement Rate:</span>
                <span className={`font-medium ${basic_trends.improvement_rate > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {basic_trends.improvement_rate > 0 ? '+' : ''}{(basic_trends.improvement_rate * 100).toFixed(1)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">Statistical Significance:</span>
                <span className={`font-medium ${performance_trajectory.statistical_significance ? 'text-green-400' : 'text-yellow-400'}`}>
                  {performance_trajectory.statistical_significance ? 'Yes' : 'No'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/70">R² Score:</span>
                <span className="text-white font-medium">{performance_trajectory.r_squared.toFixed(3)}</span>
              </div>
            </div>
          </div>
          
          {/* Recommendations */}
          <div className="bg-white/5 rounded-lg p-4">
            <h4 className="text-white font-medium mb-2">Trend Recommendations</h4>
            <ul className="space-y-1">
              {data.recommendations.map((rec, index) => (
                <li key={index} className="text-white/80 text-sm flex items-start">
                  <span className="text-blue-400 mr-2">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Confidence Analysis Chart Component
const ConfidenceAnalysisChart: React.FC<{ data: ConfidenceAnalysis }> = ({ data }) => {
  const { confidence_analysis, sample_size, statistical_significance } = data;
  const basic_confidence = confidence_analysis.basic_confidence;
  const model_uncertainty = confidence_analysis.model_uncertainty;

  const confidenceData = [
    {
      name: 'Confidence',
      value: basic_confidence.confidence * 100,
      fill: '#3b82f6'
    }
  ];

  const getUncertaintyColor = (uncertainty: string) => {
    switch (uncertainty) {
      case 'low': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'high': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-white">Statistical Confidence Analysis</h3>
        <div className="text-right">
          <div className="text-white/70 text-sm">Sample Size: {sample_size}</div>
          <div className="text-white/70 text-sm">Significance: {statistical_significance}</div>
        </div>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Confidence Gauge */}
        <div className="text-center">
          <h4 className="text-white font-medium mb-3">Overall Confidence</h4>
          <div className="h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadialBarChart 
                cx="50%" 
                cy="50%" 
                innerRadius="20%" 
                outerRadius="80%" 
                data={confidenceData}
                startAngle={90}
                endAngle={-270}
              >
                <RadialBar 
                  dataKey="value" 
                  cornerRadius={10} 
                  fill="#3b82f6"
                />
                <text x="50%" y="50%" textAnchor="middle" dominantBaseline="middle" className="fill-white text-2xl font-bold">
                  {Math.round(basic_confidence.confidence * 100)}%
                </text>
              </RadialBarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Uncertainty Analysis */}
        <div className="space-y-4">
          <h4 className="text-white font-medium">Uncertainty Assessment</h4>
          
          <div className="bg-white/5 rounded-lg p-3">
            <div className="flex justify-between items-center mb-2">
              <span className="text-white/70">Model Uncertainty:</span>
              <span className={`font-medium ${getUncertaintyColor(model_uncertainty.uncertainty)}`}>
                {model_uncertainty.uncertainty.toUpperCase()}
              </span>
            </div>
            <div className="text-white/60 text-sm">
              Stability: {model_uncertainty.model_stability}
            </div>
          </div>
          
          <div className="bg-white/5 rounded-lg p-3">
            <div className="flex justify-between items-center mb-2">
              <span className="text-white/70">Method:</span>
              <span className="text-white font-medium">{basic_confidence.method}</span>
            </div>
            <div className="text-white/60 text-sm">
              Confidence Level: {(data.confidence_level * 100).toFixed(0)}%
            </div>
          </div>
        </div>
        
        {/* Statistical Summary */}
        <div className="space-y-4">
          <h4 className="text-white font-medium">Statistical Summary</h4>
          
          <div className="bg-white/5 rounded-lg p-3">
            <div className="text-white/70 text-sm mb-2">Data Quality Indicators</div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-white/60">Sample Size:</span>
                <span className="text-white">{sample_size}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-white/60">Significance:</span>
                <span className={`${statistical_significance === 'significant' ? 'text-green-400' : 'text-yellow-400'}`}>
                  {statistical_significance}
                </span>
              </div>
            </div>
          </div>
          
          <div className="bg-white/5 rounded-lg p-3">
            <div className="text-white/70 text-sm mb-2">Confidence Interpretation</div>
            <div className="text-white/60 text-xs">
              {basic_confidence.confidence > 0.8 
                ? "High confidence in predictions" 
                : basic_confidence.confidence > 0.5 
                ? "Moderate confidence, consider more data"
                : "Low confidence, predictions may be unreliable"
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Model Performance Metrics Component
const ModelPerformanceMetrics: React.FC<{ data: ComprehensivePredictiveData }> = ({ data }) => {
  const { adaptive_predictions, ml_predictions } = data;
  const model_performance = adaptive_predictions.model_performance;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6">
      <h3 className="text-xl font-semibold text-white mb-4">Model Performance & Insights</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white/5 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-400">
            {ml_predictions.model_count}
          </div>
          <div className="text-white/70 text-sm">ML Models Used</div>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-400">
            {Math.round(ml_predictions.data_points_used)}
          </div>
          <div className="text-white/70 text-sm">Data Points</div>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-400">
            {Math.round(ml_predictions.features_engineered)}
          </div>
          <div className="text-white/70 text-sm">Features</div>
        </div>
        
        <div className="bg-white/5 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-orange-400">
            {(model_performance.accuracy * 100).toFixed(1)}%
          </div>
          <div className="text-white/70 text-sm">Model Accuracy</div>
        </div>
      </div>
      
      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h4 className="text-white font-medium mb-3">Optimal Model Strategy</h4>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-white/70">Selected Model:</span>
              <span className="text-white font-medium">{adaptive_predictions.optimal_model}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Adaptation Strategy:</span>
              <span className="text-white font-medium">{adaptive_predictions.adaptation_strategy}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-white/70">Performance:</span>
              <span className="text-green-400 font-medium">{model_performance.performance}</span>
            </div>
          </div>
        </div>
        
        <div>
          <h4 className="text-white font-medium mb-3">Model Ensemble Weights</h4>
          <div className="space-y-2">
            {Object.entries(ml_predictions.ml_predictions).map(([model, pred_data]: [string, any]) => (
              <div key={model} className="flex justify-between items-center">
                <span className="text-white/70 capitalize">{model.replace('_', ' ')}</span>
                <span className="text-white font-medium">
                  {pred_data.model_score ? `${(pred_data.model_score * 100).toFixed(1)}%` : 'N/A'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictiveAnalytics;