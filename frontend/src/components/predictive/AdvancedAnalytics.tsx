/**
 * Advanced Analytics Frontend Components - JAC Learning Platform
 * 
 * React components for displaying sophisticated statistical analysis, 
 * enhanced ML insights, advanced pattern recognition, and integrated
 * personalized recommendations.
 * 
 * Author: MiniMax Agent
 * Created: 2025-11-26
 */

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  Radar, ScatterChart, Scatter, PieChart, Pie, Cell, ComposedChart
} from 'recharts';
import { apiClient } from '../services/apiClient';

// Advanced Analytics Types
interface SophisticatedStatisticalAnalysis {
  user_id: string;
  analysis_timestamp: string;
  analysis_type: string;
  data_quality_score: number;
  sample_size: number;
  multivariate_analysis: {
    pca_analysis: {
      explained_variance_ratio: number[];
      cumulative_variance_explained: number[];
      principal_components: number[][];
      component_loadings: number[][];
      total_components: number;
    };
    factor_analysis: {
      factors: number[][];
      factor_loadings: number[][];
      number_of_factors: number;
    };
    correlation_analysis: {
      correlation_matrix: number[][];
      feature_names: string[];
      high_correlations: Array<{
        feature1: string;
        feature2: string;
        correlation: number;
        significance: string;
      }>;
    };
    data_summary: {
      total_samples: number;
      total_features: number;
      data_density: number;
    };
  };
  clustering_analysis: {
    kmeans_clustering: {
      labels: number[];
      centers: number[][];
      inertia: number;
      silhouette_score: number;
    };
    dbscan_clustering: {
      labels: number[];
      noise_points: number;
      n_clusters: number;
      silhouette_score: number;
    };
    hierarchical_clustering: {
      labels: number[];
      silhouette_score: number;
    };
    clustering_summary: {
      optimal_cluster_count: number;
      best_method: string;
      cluster_characteristics: Array<{
        cluster_id: number;
        size: number;
        characteristics: string[];
        dominance_features: string[];
      }>;
    };
  };
  correlation_analysis: {
    progress_correlations?: {
      correlation_matrix: number[][];
      feature_names: string[];
      significant_correlations: Array<{
        feature1: string;
        feature2: string;
        correlation: number;
        p_value: number;
      }>;
    };
    assessment_correlations?: {
      correlation_matrix: number[][];
      feature_names: string[];
      significant_correlations: Array<{
        feature1: string;
        feature2: string;
        correlation: number;
        p_value: number;
      }>;
    };
    cross_correlations?: {
      progress_assessment_correlation: number;
      significant_cross_correlations: Array<{
        progress_metric: string;
        assessment_metric: string;
        correlation: number;
        interpretation: string;
      }>;
    };
  };
  hypothesis_testing: {
    [test_name: string]: {
      statistic: number;
      p_value: number;
      significant: boolean;
      interpretation: string;
    };
  };
  outlier_analysis: {
    [method_name: string]: {
      outlier_count: number;
      outlier_percentage: number;
      outlier_indices?: number[];
      interpretation: string;
    };
  };
  statistical_significance_summary: {
    overall_significance: string;
    significant_tests: number;
    total_tests: number;
    confidence_level: number;
  };
  key_statistical_insights: string[];
}

interface EnhancedMLInsights {
  user_id: string;
  analysis_timestamp: string;
  feature_importance_analysis: {
    random_forest_importance: Array<{
      feature: string;
      importance: number;
      rank: number;
    }>;
    gradient_boosting_importance: Array<{
      feature: string;
      importance: number;
      rank: number;
    }>;
    permutation_importance: Array<{
      feature: string;
      importance: number;
      std: number;
    }>;
    feature_interactions: Array<{
      feature1: string;
      feature2: string;
      interaction_strength: number;
    }>;
  };
  user_segmentation: {
    optimal_clusters: number;
    silhouette_score: number;
    segments: Array<{
      segment_id: number;
      size: number;
      characteristics: string[];
      learning_style: string;
      performance_level: string;
      engagement_pattern: string;
    }>;
    segment_characteristics: {
      [segment_id: number]: {
        dominant_features: string[];
        behavior_patterns: string[];
        recommended_interventions: string[];
      };
    };
  };
  model_interpretability: {
    shap_values: Array<{
      feature: string;
      shap_value: number;
      impact: string;
    }>;
    partial_dependence: Array<{
      feature: string;
      values: number[];
      effects: number[];
    }>;
    feature_interpretation: {
      [feature: string]: {
        description: string;
        impact_direction: string;
        confidence: string;
      };
    };
  };
  pathway_optimization: {
    current_pathway_score: number;
    optimized_pathway_score: number;
    improvements: Array<{
      area: string;
      current_approach: string;
      optimized_approach: string;
      expected_improvement: number;
    }>;
    personalized_pathway: {
      next_modules: Array<{
        module_id: string;
        module_title: string;
        priority_score: number;
        reasoning: string;
        prerequisites_met: boolean;
      }>;
      learning_sequence: string[];
      estimated_completion: string;
    };
  };
  ml_insights_summary: string;
  recommendations: string[];
}

interface AdvancedPatternRecognition {
  user_id: string;
  analysis_timestamp: string;
  learning_style_detection: {
    primary_style: string;
    style_scores: {
      visual: number;
      auditory: number;
      kinesthetic: number;
      reading_writing: number;
    };
    confidence_level: string;
    evidence: string[];
    style_evolution: {
      recent_changes: string[];
      stability_score: number;
    };
  };
  engagement_patterns: {
    daily_pattern: Array<{
      hour: number;
      engagement_level: number;
      activity_type: string;
    }>;
    weekly_pattern: Array<{
      day: string;
      engagement_score: number;
      preferred_activities: string[];
    }>;
    session_patterns: {
      optimal_session_length: number;
      break_frequency: number;
      attention_span: number;
      focus_patterns: string[];
    };
    motivation_patterns: {
      intrinsic_factors: string[];
      extrinsic_factors: string[];
      motivation_triggers: string[];
      consistency_score: number;
    };
  };
  performance_anomalies: {
    detected_anomalies: Array<{
      date: string;
      metric: string;
      expected_value: number;
      actual_value: number;
      deviation_percentage: number;
      severity: string;
      probable_causes: string[];
      recommended_actions: string[];
    }>;
    anomaly_trends: {
      frequency: string;
      patterns: string[];
      severity_distribution: string;
    };
    prediction_accuracy: number;
  };
  knowledge_acquisition_patterns: {
    acquisition_speed: {
      fast_learning_topics: string[];
      slow_learning_topics: string[];
      average_acquisition_rate: number;
    };
    retention_patterns: {
      short_term_retention: number;
      long_term_retention: number;
      retention_curve: Array<{
        days: number;
        retention_rate: number;
      }>;
    };
    knowledge_gaps: Array<{
      topic: string;
      severity: number;
      evidence: string[];
      remediation_suggestions: string[];
    }>;
    mastery_progression: {
      current_mastery_level: string;
      progression_rate: number;
      expected_mastery_timeline: string;
    };
  };
  temporal_patterns: {
    learning_calendar: Array<{
      date: string;
      activity_level: number;
      performance_indicators: string[];
      notable_events: string[];
    }>;
    seasonal_patterns: {
      seasonal_influences: Array<{
        season: string;
        impact_on_performance: number;
        preferred_topics: string[];
      }>;
      cyclical_patterns: string[];
    };
    productivity_peaks: {
      peak_learning_times: string[];
      low_productivity_periods: string[];
      optimal_break_schedule: string[];
    };
  };
  pattern_recognition_summary: {
    dominant_patterns: string[];
    pattern_stability: string;
    behavioral_signature: string;
    learning_efficiency_score: number;
  };
  pattern_based_recommendations: string[];
}

interface IntegratedPersonalizedRecommendations {
  user_id: string;
  recommendation_timestamp: string;
  recommendation_type: string;
  knowledge_graph_recommendations: Array<{
    learning_graph_id: string;
    graph_title: string;
    graph_type: string;
    estimated_duration: string;
    difficulty_level: string;
    relevance_score: number;
    reason: string;
    prerequisites: string[];
    learning_outcomes: string[];
  }>;
  predictive_insights: {
    overall_prediction_confidence: string;
    learning_trajectory: string;
    recommendation_priority: string;
    key_predictions: Array<{
      prediction_type: string;
      timeframe: string;
      confidence: number;
      description: string;
    }>;
  };
  statistical_insights: {
    data_quality_assessment: string;
    significant_patterns: string[];
    statistical_strength: string;
    confidence_intervals: Array<{
      metric: string;
      lower_bound: number;
      upper_bound: number;
      confidence_level: number;
    }>;
  };
  ml_insights: {
    user_segment: string;
    key_features: string[];
    model_performance: string;
    prediction_accuracy: number;
  };
  pattern_recognition: {
    dominant_learning_style: string;
    engagement_pattern: string;
    performance_trends: string;
    behavioral_insights: string[];
  };
  integrated_recommendations: Array<{
    id: string;
    type: string;
    title: string;
    description: string;
    priority: number;
    confidence: number;
    source: string[];
    reasoning: string;
    expected_outcome: string;
    implementation_steps: string[];
    timeline: string;
    difficulty_level: string;
  }>;
  ranked_recommendations: Array<{
    id: string;
    title: string;
    description: string;
    priority_score: number;
    confidence_score: number;
    impact_potential: string;
    feasibility: string;
    urgency: string;
    reasoning: string;
  }>;
  recommendation_summary: {
    total_recommendations: number;
    high_priority_count: number;
    medium_priority_count: number;
    low_priority_count: number;
    average_confidence: number;
    top_3_priorities: string[];
    implementation_timeline: string;
  };
  confidence_scores: {
    statistical_confidence: number;
    ml_model_confidence: number;
    pattern_recognition_confidence: number;
    overall_confidence: number;
    confidence_factors: string[];
  };
}

interface AdvancedAnalyticsProps {
  learningPathId?: string;
  onDataUpdate?: (data: any) => void;
  showRecommendations?: boolean;
  compact?: boolean;
}

const AdvancedAnalytics: React.FC<AdvancedAnalyticsProps> = ({ 
  learningPathId, 
  onDataUpdate,
  showRecommendations = true,
  compact = false 
}) => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [statisticalAnalysis, setStatisticalAnalysis] = useState<SophisticatedStatisticalAnalysis | null>(null);
  const [mlInsights, setMLInsights] = useState<EnhancedMLInsights | null>(null);
  const [patternRecognition, setPatternRecognition] = useState<AdvancedPatternRecognition | null>(null);
  const [recommendations, setRecommendations] = useState<IntegratedPersonalizedRecommendations | null>(null);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  useEffect(() => {
    loadAdvancedAnalytics();
  }, [learningPathId, showRecommendations]);

  const loadAdvancedAnalytics = async () => {
    setLoading(true);
    setError(null);
    
    try {
      if (activeTab === 'dashboard') {
        await loadDashboard();
      } else if (activeTab === 'statistical') {
        await loadStatisticalAnalysis();
      } else if (activeTab === 'ml-insights') {
        await loadMLInsights();
      } else if (activeTab === 'patterns') {
        await loadPatternRecognition();
      } else if (activeTab === 'recommendations') {
        await loadRecommendations();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const loadDashboard = async () => {
    const params = new URLSearchParams({
      include_recommendations: showRecommendations.toString(),
      ...(learningPathId && { learning_path_id: learningPathId })
    });

    const response = await apiClient.get(`/api/advanced/dashboard/?${params}`);
    const data = response.data;
    
    if (data.success) {
      setDashboardData(data.data);
      if (onDataUpdate) onDataUpdate(data.data);
    } else {
      throw new Error(data.error || 'Failed to load dashboard');
    }
  };

  const loadStatisticalAnalysis = async () => {
    const params = new URLSearchParams({
      analysis_type: 'comprehensive',
      ...(learningPathId && { learning_path_id: learningPathId })
    });

    const response = await apiClient.get(`/api/advanced/statistical/?${params}`);
    const data = response.data;
    
    if (data.success) {
      setStatisticalAnalysis(data.data);
    } else {
      throw new Error(data.error || 'Failed to load statistical analysis');
    }
  };

  const loadMLInsights = async () => {
    const params = new URLSearchParams(
      learningPathId ? { learning_path_id: learningPathId } : {}
    );

    const response = await apiClient.get(`/api/advanced/ml-insights/?${params}`);
    const data = response.data;
    
    if (data.success) {
      setMLInsights(data.data);
    } else {
      throw new Error(data.error || 'Failed to load ML insights');
    }
  };

  const loadPatternRecognition = async () => {
    const params = new URLSearchParams(
      learningPathId ? { learning_path_id: learningPathId } : {}
    );

    const response = await apiClient.get(`/api/advanced/pattern-recognition/?${params}`);
    const data = response.data;
    
    if (data.success) {
      setPatternRecognition(data.data);
    } else {
      throw new Error(data.error || 'Failed to load pattern recognition');
    }
  };

  const loadRecommendations = async () => {
    const params = new URLSearchParams({
      recommendation_type: 'comprehensive',
      ...(learningPathId && { learning_path_id: learningPathId })
    });

    const response = await apiClient.get(`/api/advanced/personalized-recommendations/?${params}`);
    const data = response.data;
    
    if (data.success) {
      setRecommendations(data.data);
    } else {
      throw new Error(data.error || 'Failed to load recommendations');
    }
  };

  const renderDashboardSummary = () => {
    if (!dashboardData) return null;

    const summary = dashboardData.dashboard_summary;
    
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Analytics Overview</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-blue-600">Data Quality</h4>
            <p className="text-2xl font-bold text-blue-800">{summary.overall_data_quality}</p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-green-600">Confidence Level</h4>
            <p className="text-2xl font-bold text-green-800">{summary.confidence_level}</p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-purple-600">Analysis Status</h4>
            <p className="text-lg font-bold text-purple-800">{summary.analysis_status}</p>
          </div>
          
          <div className="bg-orange-50 rounded-lg p-4">
            <h4 className="text-sm font-medium text-orange-600">Key Findings</h4>
            <p className="text-2xl font-bold text-orange-800">{summary.key_findings.length}</p>
          </div>
        </div>

        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-700 mb-3">Key Findings</h4>
          <ul className="space-y-2">
            {summary.key_findings.map((finding: string, index: number) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></span>
                <span className="text-gray-600">{finding}</span>
              </li>
            ))}
          </ul>
        </div>

        {summary.top_recommendations.length > 0 && (
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-3">Top Recommendations</h4>
            <ul className="space-y-2">
              {summary.top_recommendations.map((rec: string, index: number) => (
                <li key={index} className="flex items-start space-x-2">
                  <span className="flex-shrink-0 w-2 h-2 bg-green-500 rounded-full mt-2"></span>
                  <span className="text-gray-600">{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    );
  };

  const renderStatisticalAnalysis = () => {
    if (!statisticalAnalysis) return null;

    const analysis = statisticalAnalysis.multivariate_analysis;
    const pcaData = analysis.pca_analysis.explained_variance_ratio.map((variance, index) => ({
      component: `PC${index + 1}`,
      variance: (variance * 100).toFixed(1),
      cumulative: (analysis.pca_analysis.cumulative_variance_explained[index] * 100).toFixed(1)
    }));

    return (
      <div className="space-y-6">
        {/* PCA Analysis */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Principal Component Analysis</h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Explained Variance</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={pcaData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="component" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="variance" fill="#8884d8" name="Individual %" />
                  <Bar dataKey="cumulative" fill="#82ca9d" name="Cumulative %" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Data Summary</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Samples:</span>
                  <span className="font-semibold">{analysis.data_summary.total_samples}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Features:</span>
                  <span className="font-semibold">{analysis.data_summary.total_features}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Data Density:</span>
                  <span className="font-semibold">{(analysis.data_summary.data_density * 100).toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Components:</span>
                  <span className="font-semibold">{analysis.pca_analysis.total_components}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Clustering Analysis */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Clustering Analysis</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-blue-700">K-Means</h4>
              <p className="text-sm text-blue-600">Silhouette Score: {statisticalAnalysis.clustering_analysis.kmeans_clustering.silhouette_score.toFixed(3)}</p>
              <p className="text-sm text-blue-600">Inertia: {statisticalAnalysis.clustering_analysis.kmeans_clustering.inertia.toFixed(2)}</p>
            </div>
            
            <div className="bg-green-50 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-green-700">DBSCAN</h4>
              <p className="text-sm text-green-600">Clusters: {statisticalAnalysis.clustering_analysis.dbscan_clustering.n_clusters}</p>
              <p className="text-sm text-green-600">Noise Points: {statisticalAnalysis.clustering_analysis.dbscan_clustering.noise_points}</p>
            </div>
            
            <div className="bg-purple-50 rounded-lg p-4">
              <h4 className="text-lg font-semibold text-purple-700">Best Method</h4>
              <p className="text-lg font-bold text-purple-800">{statisticalAnalysis.clustering_analysis.clustering_summary.best_method}</p>
              <p className="text-sm text-purple-600">Clusters: {statisticalAnalysis.clustering_analysis.clustering_summary.optimal_cluster_count}</p>
            </div>
          </div>
        </div>

        {/* Statistical Insights */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Statistical Insights</h3>
          
          <div className="space-y-4">
            {statisticalAnalysis.key_statistical_insights.map((insight: string, index: number) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                <span className="flex-shrink-0 w-2 h-2 bg-blue-500 rounded-full mt-2"></span>
                <span className="text-gray-700">{insight}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderMLInsights = () => {
    if (!mlInsights) return null;

    const featureImportanceData = mlInsights.feature_importance_analysis.random_forest_importance.slice(0, 8).map(item => ({
      feature: item.feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      importance: (item.importance * 100).toFixed(1),
      rank: item.rank
    }));

    return (
      <div className="space-y-6">
        {/* Feature Importance */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Feature Importance Analysis</h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Random Forest Importance</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={featureImportanceData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="feature" type="category" width={100} />
                  <Tooltip />
                  <Bar dataKey="importance" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">User Segmentation</h4>
              <div className="space-y-4">
                <div className="bg-blue-50 rounded-lg p-4">
                  <h5 className="font-semibold text-blue-700">Optimal Clusters</h5>
                  <p className="text-2xl font-bold text-blue-800">{mlInsights.user_segmentation.optimal_clusters}</p>
                  <p className="text-sm text-blue-600">Silhouette Score: {mlInsights.user_segmentation.silhouette_score.toFixed(3)}</p>
                </div>
                
                <div className="bg-green-50 rounded-lg p-4">
                  <h5 className="font-semibold text-green-700">Learning Style Distribution</h5>
                  {mlInsights.user_segmentation.segments.slice(0, 3).map((segment, index) => (
                    <div key={index} className="mt-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-green-600">Segment {segment.segment_id + 1}</span>
                        <span className="text-sm font-semibold">{segment.size} users</span>
                      </div>
                      <p className="text-xs text-green-500">{segment.learning_style}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Pathway Optimization */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Learning Pathway Optimization</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Score Comparison</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Current Pathway Score:</span>
                  <span className="font-bold text-red-600">{mlInsights.pathway_optimization.current_pathway_score.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Optimized Pathway Score:</span>
                  <span className="font-bold text-green-600">{mlInsights.pathway_optimization.optimized_pathway_score.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between items-center border-t pt-2">
                  <span className="text-gray-600 font-semibold">Improvement:</span>
                  <span className="font-bold text-blue-600">
                    +{(mlInsights.pathway_optimization.optimized_pathway_score - mlInsights.pathway_optimization.current_pathway_score).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Personalized Next Steps</h4>
              <div className="space-y-2">
                {mlInsights.pathway_optimization.personalized_pathway.next_modules.slice(0, 3).map((module, index) => (
                  <div key={index} className="p-3 bg-gray-50 rounded-lg">
                    <h5 className="font-semibold text-gray-700">{module.module_title}</h5>
                    <p className="text-sm text-gray-600">Priority: {(module.priority_score * 100).toFixed(0)}%</p>
                    <p className="text-xs text-gray-500">{module.reasoning}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ML Insights Summary */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">ML Insights Summary</h3>
          <p className="text-gray-700 mb-4">{mlInsights.ml_insights_summary}</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold text-gray-700 mb-2">Key Recommendations</h4>
              <ul className="space-y-1">
                {mlInsights.recommendations.slice(0, 3).map((rec, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                    <span className="flex-shrink-0 w-1 h-1 bg-blue-500 rounded-full mt-2"></span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderPatternRecognition = () => {
    if (!patternRecognition) return null;

    const styleData = [
      { style: 'Visual', score: patternRecognition.learning_style_detection.style_scores.visual },
      { style: 'Auditory', score: patternRecognition.learning_style_detection.style_scores.auditory },
      { style: 'Kinesthetic', score: patternRecognition.learning_style_detection.style_scores.kinesthetic },
      { style: 'Reading/Writing', score: patternRecognition.learning_style_detection.style_scores.reading_writing }
    ];

    return (
      <div className="space-y-6">
        {/* Learning Style Detection */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Learning Style Detection</h3>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Style Scores</h4>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={styleData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="style" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="Style Score" dataKey="score" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Style Analysis</h4>
              <div className="space-y-4">
                <div className="bg-blue-50 rounded-lg p-4">
                  <h5 className="font-semibold text-blue-700">Primary Style</h5>
                  <p className="text-xl font-bold text-blue-800">{patternRecognition.learning_style_detection.primary_style}</p>
                  <p className="text-sm text-blue-600">Confidence: {patternRecognition.learning_style_detection.confidence_level}</p>
                </div>
                
                <div>
                  <h5 className="font-semibold text-gray-700 mb-2">Evidence</h5>
                  <ul className="space-y-1">
                    {patternRecognition.learning_style_detection.evidence.slice(0, 3).map((evidence, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                        <span className="flex-shrink-0 w-1 h-1 bg-green-500 rounded-full mt-2"></span>
                        <span>{evidence}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Engagement Patterns */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Engagement Patterns</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Daily Engagement Pattern</h4>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={patternRecognition.engagement_patterns.daily_pattern}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="hour" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="engagement_level" stroke="#8884d8" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Session Analysis</h4>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Optimal Session Length:</span>
                  <span className="font-semibold">{patternRecognition.engagement_patterns.session_patterns.optimal_session_length} min</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Break Frequency:</span>
                  <span className="font-semibold">Every {patternRecognition.engagement_patterns.session_patterns.break_frequency} min</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Attention Span:</span>
                  <span className="font-semibold">{patternRecognition.engagement_patterns.session_patterns.attention_span} min</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Consistency Score:</span>
                  <span className="font-semibold">{(patternRecognition.engagement_patterns.motivation_patterns.consistency_score * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Anomalies */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Performance Anomalies</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Anomaly Summary</h4>
              <div className="space-y-3">
                <div className="bg-red-50 rounded-lg p-4">
                  <h5 className="font-semibold text-red-700">Detection Summary</h5>
                  <p className="text-sm text-red-600">Frequency: {patternRecognition.performance_anomalies.anomaly_trends.frequency}</p>
                  <p className="text-sm text-red-600">Patterns: {patternRecognition.performance_anomalies.anomaly_trends.patterns.length} identified</p>
                  <p className="text-sm text-red-600">Accuracy: {(patternRecognition.performance_anomalies.prediction_accuracy * 100).toFixed(1)}%</p>
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Recent Anomalies</h4>
              <div className="space-y-2">
                {patternRecognition.performance_anomalies.detected_anomalies.slice(0, 3).map((anomaly, index) => (
                  <div key={index} className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                    <div className="flex justify-between items-start mb-1">
                      <h5 className="font-semibold text-yellow-800">{anomaly.metric}</h5>
                      <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-1 rounded">
                        {anomaly.severity}
                      </span>
                    </div>
                    <p className="text-sm text-yellow-700">
                      Expected: {anomaly.expected_value.toFixed(1)}, Actual: {anomaly.actual_value.toFixed(1)}
                    </p>
                    <p className="text-xs text-yellow-600 mt-1">{anomaly.probable_causes[0]}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Pattern Recognition Summary */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Pattern Recognition Summary</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Key Patterns</h4>
              <ul className="space-y-2">
                {patternRecognition.pattern_recognition_summary.dominant_patterns.map((pattern, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                    <span className="flex-shrink-0 w-2 h-2 bg-purple-500 rounded-full mt-1"></span>
                    <span>{pattern}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Pattern-Based Recommendations</h4>
              <ul className="space-y-2">
                {patternRecognition.pattern_based_recommendations.slice(0, 3).map((rec, index) => (
                  <li key={index} className="text-sm text-gray-600 flex items-start space-x-2">
                    <span className="flex-shrink-0 w-2 h-2 bg-green-500 rounded-full mt-1"></span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderRecommendations = () => {
    if (!recommendations) return null;

    const priorityData = [
      { name: 'High Priority', value: recommendations.recommendation_summary.high_priority_count, fill: '#FF6B6B' },
      { name: 'Medium Priority', value: recommendations.recommendation_summary.medium_priority_count, fill: '#4ECDC4' },
      { name: 'Low Priority', value: recommendations.recommendation_summary.low_priority_count, fill: '#45B7D1' }
    ];

    return (
      <div className="space-y-6">
        {/* Recommendations Overview */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Personalized Recommendations Overview</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-blue-600">Total Recommendations</h4>
              <p className="text-2xl font-bold text-blue-800">{recommendations.recommendation_summary.total_recommendations}</p>
            </div>
            
            <div className="bg-green-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-green-600">Average Confidence</h4>
              <p className="text-2xl font-bold text-green-800">{(recommendations.recommendation_summary.average_confidence * 100).toFixed(0)}%</p>
            </div>
            
            <div className="bg-purple-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-purple-600">High Priority</h4>
              <p className="text-2xl font-bold text-purple-800">{recommendations.recommendation_summary.high_priority_count}</p>
            </div>
            
            <div className="bg-orange-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-orange-600">Implementation Timeline</h4>
              <p className="text-lg font-bold text-orange-800">{recommendations.recommendation_summary.implementation_timeline}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Priority Distribution</h4>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={priorityData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {priorityData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="text-lg font-semibold text-gray-700 mb-3">Confidence Scores</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Statistical Confidence:</span>
                  <span className="font-semibold">{(recommendations.confidence_scores.statistical_confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">ML Model Confidence:</span>
                  <span className="font-semibold">{(recommendations.confidence_scores.ml_model_confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Pattern Recognition:</span>
                  <span className="font-semibold">{(recommendations.confidence_scores.pattern_recognition_confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between items-center border-t pt-2">
                  <span className="text-gray-600 font-semibold">Overall Confidence:</span>
                  <span className="font-bold text-blue-600">{(recommendations.confidence_scores.overall_confidence * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Top Ranked Recommendations */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Top Ranked Recommendations</h3>
          
          <div className="space-y-4">
            {recommendations.ranked_recommendations.slice(0, 5).map((rec, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h4 className="text-lg font-semibold text-gray-800">{rec.title}</h4>
                    <p className="text-gray-600 mt-1">{rec.description}</p>
                  </div>
                  <div className="ml-4 flex flex-col items-end space-y-1">
                    <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      Priority: {(rec.priority_score * 100).toFixed(0)}%
                    </span>
                    <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      Confidence: {(rec.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3 text-sm">
                  <div>
                    <span className="text-gray-500">Impact:</span>
                    <span className="ml-2 font-semibold">{rec.impact_potential}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Feasibility:</span>
                    <span className="ml-2 font-semibold">{rec.feasibility}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Urgency:</span>
                    <span className="ml-2 font-semibold">{rec.urgency}</span>
                  </div>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-3">
                  <h5 className="font-semibold text-gray-700 mb-2">Reasoning:</h5>
                  <p className="text-sm text-gray-600">{rec.reasoning}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Knowledge Graph Recommendations */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Knowledge Graph Recommendations</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.knowledge_graph_recommendations.slice(0, 4).map((rec, index) => (
              <div key={index} className="border rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-2">{rec.graph_title}</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Type:</span>
                    <span className="font-semibold">{rec.graph_type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Duration:</span>
                    <span className="font-semibold">{rec.estimated_duration}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Difficulty:</span>
                    <span className="font-semibold">{rec.difficulty_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Relevance:</span>
                    <span className="font-semibold">{(rec.relevance_score * 100).toFixed(0)}%</span>
                  </div>
                </div>
                <div className="mt-3 p-2 bg-blue-50 rounded text-sm text-blue-700">
                  {rec.reason}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  };

  const renderLoading = () => (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      <span className="ml-3 text-gray-600">Loading advanced analytics...</span>
    </div>
  );

  const renderError = () => (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <div className="flex">
        <span className="text-red-500 text-xl mr-3">⚠️</span>
        <div>
          <h3 className="text-red-800 font-semibold">Error Loading Analytics</h3>
          <p className="text-red-600 mt-1">{error}</p>
          <button 
            onClick={loadAdvancedAnalytics}
            className="mt-2 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    </div>
  );

  if (loading) return renderLoading();
  if (error) return renderError();

  const tabContent = {
    dashboard: renderDashboardSummary(),
    statistical: renderStatisticalAnalysis(),
    'ml-insights': renderMLInsights(),
    patterns: renderPatternRecognition(),
    recommendations: renderRecommendations()
  };

  return (
    <div className="advanced-analytics-container">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Advanced Analytics</h2>
        
        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8">
            {[
              { key: 'dashboard', label: 'Dashboard', icon: '📊' },
              { key: 'statistical', label: 'Statistical Analysis', icon: '📈' },
              { key: 'ml-insights', label: 'ML Insights', icon: '🤖' },
              { key: 'patterns', label: 'Pattern Recognition', icon: '🔍' },
              { key: 'recommendations', label: 'Recommendations', icon: '💡' }
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => {
                  setActiveTab(tab.key);
                  setTimeout(loadAdvancedAnalytics, 100);
                }}
                className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.key
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        {tabContent[activeTab as keyof typeof tabContent]}
      </motion.div>
    </div>
  );
};

export default AdvancedAnalytics;