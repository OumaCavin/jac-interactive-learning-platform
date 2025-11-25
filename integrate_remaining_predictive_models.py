#!/usr/bin/env python3
"""
Complete Integration of Remaining Predictive Learning Models and K-Means Clustering
Author: Cavin Otieno
Created: 2025-11-26

This script integrates the 6 remaining predictive learning models and K-Means clustering
to complete the ML suite for the JAC Learning Platform.
"""

import os
import sys
import django
import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')

try:
    django.setup()
    from django.contrib.auth.models import User
    from django.db.models import Q, Count, Sum, Avg, Max, Min, F
    from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    from scipy import stats
    from scipy.spatial.distance import cdist
    import matplotlib.pyplot as plt
    import seaborn as sns
    DJANGO_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Django or dependencies not available: {e}")
    DJANGO_AVAILABLE = False

logger = logging.getLogger(__name__)

def setup_matplotlib_for_plotting():
    """Setup matplotlib for plotting with proper configuration."""
    try:
        import warnings
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Ensure warnings are printed
        warnings.filterwarnings('default')

        # Configure matplotlib for non-interactive mode
        plt.switch_backend("Agg")

        # Set chart style
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

        # Configure platform-appropriate fonts for cross-platform compatibility
        plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", "PingFang SC", "Arial Unicode MS", "Hiragino Sans GB"]
        plt.rcParams["axes.unicode_minus"] = False
    except Exception as e:
        print(f"Warning: Could not setup matplotlib: {e}")

setup_matplotlib_for_plotting()

class PredictiveLearningModelsIntegrator:
    """Integrate remaining predictive learning models into the ML suite"""
    
    def __init__(self):
        self.integration_results = {
            'learning_velocity_analysis': False,
            'engagement_pattern_analysis': False, 
            'success_probability_modeling': False,
            'time_to_completion_prediction': False,
            'retention_risk_assessment': False,
            'knowledge_gap_detection': False,
            'kmeans_clustering_algorithm': False
        }
        self.code_blocks = {}
        self.method_signatures = {}
        
    def create_learning_velocity_analysis_method(self) -> str:
        """Create learning velocity analysis method"""
        method_code = '''
    def analyze_learning_velocity(self, user: User, learning_path_id: Optional[int] = None, 
                                 days_window: int = 30) -> Dict[str, Any]:
        """
        Analyze user learning velocity patterns and predict future pace.
        
        Args:
            user: User instance
            learning_path_id: Optional learning path to focus on
            days_window: Days of historical data to analyze
            
        Returns:
            Dict with velocity analysis, trends, and predictions
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=days_window)
            
            # Get user activity data
            query_kwargs = {'user': user, 'created_at__gte': start_date}
            if learning_path_id:
                query_kwargs['learning_path_id'] = learning_path_id
                
            # Collect velocity metrics from multiple sources
            velocity_data = []
            
            # Module completion velocity
            module_data = list(UserModuleProgress.objects.filter(
                **query_kwargs,
                status='completed'
            ).annotate(
                days_since_start=F('completed_at') - F('started_at')
            ).values())
            
            for item in module_data:
                velocity_data.append({
                    'type': 'module_completion',
                    'value': 1 if item.get('days_since_start').days <= 1 else 0.5,
                    'timestamp': item['completed_at'],
                    'difficulty': item.get('difficulty_level', 1.0)
                })
            
            # Assessment velocity
            assessment_data = list(AssessmentAttempt.objects.filter(
                **query_kwargs,
                score__gte=0.7
            ).values())
            
            for item in assessment_data:
                velocity_data.append({
                    'type': 'assessment_success',
                    'value': min(item['score'], 1.0),
                    'timestamp': item['completed_at'],
                    'difficulty': item.get('difficulty_level', 1.0)
                })
            
            if not velocity_data:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough velocity data for analysis',
                    'velocity_score': 0.5,
                    'trend': 'stable',
                    'predicted_pace': 'moderate'
                }
            
            # Analyze velocity trends
            velocity_df = pd.DataFrame(velocity_data)
            velocity_df['timestamp'] = pd.to_datetime(velocity_df['timestamp'])
            velocity_df = velocity_df.sort_values('timestamp')
            
            # Calculate moving average velocity
            velocity_df['moving_avg'] = velocity_df['value'].rolling(window=5, min_periods=1).mean()
            
            # Calculate velocity acceleration
            velocity_df['velocity_change'] = velocity_df['moving_avg'].diff()
            
            # Analyze velocity patterns
            recent_velocity = velocity_df['moving_avg'].tail(10).mean()
            historical_velocity = velocity_df['moving_avg'].head(-10).mean() if len(velocity_df) > 10 else recent_velocity
            
            # Calculate velocity trend
            if len(velocity_df) > 5:
                velocity_trend = np.polyfit(range(len(velocity_df)), velocity_df['moving_avg'], 1)[0]
            else:
                velocity_trend = 0
                
            # Determine trend direction
            if velocity_trend > 0.01:
                trend = 'accelerating'
            elif velocity_trend < -0.01:
                trend = 'decelerating'
            else:
                trend = 'stable'
            
            # Calculate velocity consistency
            velocity_consistency = 1 - (velocity_df['value'].std() / velocity_df['value'].mean()) if velocity_df['value'].mean() > 0 else 0
            
            # Predict future velocity
            if velocity_trend > 0:
                predicted_pace = 'accelerating' if velocity_trend > 0.05 else 'increasing'
            elif velocity_trend < 0:
                predicted_pace = 'decelerating' if velocity_trend < -0.05 else 'decreasing'
            else:
                predicted_pace = 'steady'
            
            # Calculate confidence score
            confidence = min(0.95, len(velocity_data) / 50 + velocity_consistency * 0.3)
            
            # Generate insights and recommendations
            insights = []
            recommendations = []
            
            if trend == 'accelerating':
                insights.append("Learning velocity is increasing - positive momentum detected")
                recommendations.append("Continue current learning approach")
                if velocity_consistency > 0.7:
                    recommendations.append("Consider increasing challenge difficulty")
            elif trend == 'decelerating':
                insights.append("Learning velocity is declining - attention needed")
                recommendations.append("Review learning strategies")
                recommendations.append("Consider shorter study sessions")
            else:
                insights.append("Learning velocity is stable - consistent pace maintained")
                recommendations.append("Maintain current learning rhythm")
            
            return {
                'status': 'success',
                'velocity_score': float(recent_velocity),
                'velocity_trend': trend,
                'predicted_pace': predicted_pace,
                'confidence': float(confidence),
                'consistency': float(velocity_consistency),
                'trend_value': float(velocity_trend),
                'data_points': len(velocity_data),
                'insights': insights,
                'recommendations': recommendations,
                'analysis_period': days_window,
                'methodology': 'Statistical trend analysis with moving averages'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing learning velocity: {e}")
            return {
                'status': 'error',
                'message': f'Velocity analysis failed: {str(e)}',
                'velocity_score': 0.5,
                'trend': 'stable',
                'predicted_pace': 'moderate'
            }
'''
        return method_code
    
    def create_engagement_pattern_analysis_method(self) -> str:
        """Create engagement pattern analysis method"""
        method_code = '''
    def analyze_engagement_patterns(self, user: User, learning_path_id: Optional[int] = None,
                                  analysis_depth: str = 'comprehensive') -> Dict[str, Any]:
        """
        Analyze user engagement patterns across multiple dimensions.
        
        Args:
            user: User instance
            learning_path_id: Optional specific learning path
            analysis_depth: 'basic', 'standard', or 'comprehensive'
            
        Returns:
            Dict with engagement patterns, timing preferences, and optimization suggestions
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=90)  # 3 months of data
            
            # Build comprehensive query
            query_kwargs = {'user': user, 'created_at__gte': start_date}
            if learning_path_id:
                query_kwargs['learning_path_id'] = learning_path_id
            
            # Collect engagement data from multiple sources
            engagement_data = []
            
            # Module interaction patterns
            module_interactions = list(UserModuleProgress.objects.filter(
                **query_kwargs
            ).annotate(
                interaction_duration=F('updated_at') - F('created_at'),
                interaction_frequency=Count('id')
            ).values())
            
            for item in module_interactions:
                if item.get('updated_at') and item.get('created_at'):
                    duration = (item['updated_at'] - item['created_at']).total_seconds() / 60  # minutes
                    engagement_data.append({
                        'type': 'module_interaction',
                        'duration': duration,
                        'timestamp': item['updated_at'],
                        'hour': item['updated_at'].hour if hasattr(item['updated_at'], 'hour') else 12,
                        'day_of_week': item['updated_at'].weekday() if hasattr(item['updated_at'], 'weekday') else 3,
                        'status': item.get('status', 'in_progress')
                    })
            
            # Assessment engagement
            assessment_data = list(AssessmentAttempt.objects.filter(
                **query_kwargs
            ).values())
            
            for item in assessment_data:
                if item.get('completed_at'):
                    duration = item.get('time_spent_seconds', 600) / 60  # minutes
                    engagement_data.append({
                        'type': 'assessment_engagement',
                        'duration': duration,
                        'timestamp': item['completed_at'],
                        'hour': item['completed_at'].hour if hasattr(item['completed_at'], 'hour') else 12,
                        'day_of_week': item['completed_at'].weekday() if hasattr(item['completed_at'], 'weekday') else 3,
                        'score': item.get('score', 0.0)
                    })
            
            if not engagement_data:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough engagement data for pattern analysis',
                    'engagement_score': 0.5,
                    'primary_pattern': 'insufficient_data'
                }
            
            # Analyze patterns
            engagement_df = pd.DataFrame(engagement_data)
            engagement_df['timestamp'] = pd.to_datetime(engagement_df['timestamp'])
            engagement_df = engagement_df.sort_values('timestamp')
            
            # 1. Temporal patterns
            hourly_engagement = engagement_df.groupby('hour').agg({
                'duration': ['mean', 'count'],
                'type': 'first'
            }).round(2)
            
            daily_engagement = engagement_df.groupby('day_of_week').agg({
                'duration': ['mean', 'count'],
                'type': 'first'
            }).round(2)
            
            # Find peak engagement times
            if not hourly_engagement.empty:
                peak_hour = hourly_engagement['duration']['mean'].idxmax()
                peak_day = daily_engagement['duration']['mean'].idxmax()
            else:
                peak_hour = 14  # Default afternoon
                peak_day = 1    # Default Tuesday
            
            # 2. Duration patterns
            avg_session_duration = engagement_df['duration'].mean()
            median_session_duration = engagement_df['duration'].median()
            session_consistency = 1 - (engagement_df['duration'].std() / engagement_df['duration'].mean()) if engagement_df['duration'].mean() > 0 else 0
            
            # 3. Engagement quality metrics
            if 'score' in engagement_df.columns:
                avg_engagement_quality = engagement_df['score'].mean()
            else:
                # Quality proxy based on session completion and duration
                quality_proxy = len(engagement_df[engagement_df['duration'] > avg_session_duration * 0.5]) / len(engagement_df)
                avg_engagement_quality = quality_proxy
            
            # 4. Engagement trends
            if len(engagement_df) > 10:
                # Weekly engagement trend
                engagement_df['week'] = engagement_df['timestamp'].dt.isocalendar().week
                weekly_engagement = engagement_df.groupby('week')['duration'].mean()
                
                if len(weekly_engagement) > 2:
                    engagement_trend = np.polyfit(range(len(weekly_engagement)), weekly_engagement, 1)[0]
                else:
                    engagement_trend = 0
            else:
                engagement_trend = 0
            
            # 5. Pattern classification
            pattern_types = []
            if session_consistency > 0.7:
                pattern_types.append('consistent')
            else:
                pattern_types.append('variable')
            
            if engagement_trend > 0.1:
                pattern_types.append('improving')
            elif engagement_trend < -0.1:
                pattern_types.append('declining')
            else:
                pattern_types.append('stable')
            
            if avg_session_duration > 60:  # More than 1 hour
                pattern_types.append('extended_sessions')
            elif avg_session_duration > 30:
                pattern_types.append('moderate_sessions')
            else:
                pattern_types.append('short_sessions')
            
            # 6. Calculate overall engagement score
            engagement_components = [
                min(1.0, avg_engagement_quality),
                min(1.0, session_consistency),
                min(1.0, len(engagement_data) / 20),  # Activity level
                max(0.0, min(1.0, 1 - abs(engagement_trend)))  # Stability
            ]
            
            overall_engagement_score = np.mean(engagement_components)
            
            # 7. Generate insights and recommendations
            insights = []
            recommendations = []
            
            # Temporal insights
            day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if peak_day < len(day_names):
                insights.append(f"Peak engagement occurs on {day_names[peak_day]}s")
                recommendations.append(f"Schedule important learning activities on {day_names[peak_day]}s")
            
            hour_names = [f"{h}:00" for h in range(24)]
            if peak_hour < len(hour_names):
                insights.append(f"Most engaged time is {hour_names[peak_hour]}")
                recommendations.append(f"Plan intensive study sessions around {hour_names[peak_hour]}")
            
            # Duration insights
            if session_consistency > 0.8:
                insights.append("Highly consistent session durations")
                recommendations.append("Maintain consistent study schedule")
            elif session_consistency < 0.4:
                insights.append("Highly variable session durations")
                recommendations.append("Establish more consistent study routine")
            
            if avg_session_duration > 90:
                insights.append("Prefers extended learning sessions")
                recommendations.append("Consider breaking long sessions into focused blocks")
            elif avg_session_duration < 20:
                insights.append("Prefers short, frequent sessions")
                recommendations.append("Optimize for micro-learning opportunities")
            
            # Trend insights
            if engagement_trend > 0.1:
                insights.append("Engagement is improving over time")
                recommendations.append("Current strategies are working well")
            elif engagement_trend < -0.1:
                insights.append("Engagement is declining over time")
                recommendations.append("Review and adjust learning approach")
            
            return {
                'status': 'success',
                'engagement_score': float(overall_engagement_score),
                'pattern_types': pattern_types,
                'primary_pattern': pattern_types[0] if pattern_types else 'unknown',
                'temporal_preferences': {
                    'peak_hour': int(peak_hour),
                    'peak_day': int(peak_day),
                    'optimal_day': day_names[peak_day] if peak_day < len(day_names) else 'Tuesday',
                    'optimal_time': hour_names[peak_hour] if peak_hour < len(hour_names) else '14:00'
                },
                'session_metrics': {
                    'average_duration': float(avg_session_duration),
                    'median_duration': float(median_session_duration),
                    'consistency': float(session_consistency)
                },
                'quality_metrics': {
                    'engagement_quality': float(avg_engagement_quality),
                    'trend': 'improving' if engagement_trend > 0.1 else 'declining' if engagement_trend < -0.1 else 'stable',
                    'trend_value': float(engagement_trend)
                },
                'activity_summary': {
                    'total_sessions': len(engagement_data),
                    'analysis_period_days': 90,
                    'activity_level': 'high' if len(engagement_data) > 30 else 'moderate' if len(engagement_data) > 10 else 'low'
                },
                'insights': insights,
                'recommendations': recommendations,
                'methodology': 'Multi-dimensional temporal and behavioral pattern analysis'
            }
            
        except Exception as e:
            logger.error(f"Error analyzing engagement patterns: {e}")
            return {
                'status': 'error',
                'message': f'Engagement analysis failed: {str(e)}',
                'engagement_score': 0.5,
                'primary_pattern': 'analysis_failed'
            }
'''
        return method_code
    
    def create_success_probability_modeling_method(self) -> str:
        """Create success probability modeling method"""
        method_code = '''
    def model_success_probability(self, user: User, learning_path_id: Optional[int] = None,
                                target_module_id: Optional[int] = None,
                                time_horizon_days: int = 30) -> Dict[str, Any]:
        """
        Model probability of learning success using ensemble methods.
        
        Args:
            user: User instance
            learning_path_id: Optional learning path to analyze
            target_module_id: Optional specific module for targeted prediction
            time_horizon_days: Days to predict ahead
            
        Returns:
            Dict with success probability, confidence intervals, and risk factors
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=180)  # 6 months of historical data
            
            # Build comprehensive feature set
            features = {}
            
            # Historical performance features
            historical_data = list(UserModuleProgress.objects.filter(
                user=user,
                created_at__gte=start_date,
                **({'learning_path_id': learning_path_id} if learning_path_id else {})
            ).aggregate(
                completion_rate=Avg(Case(When(status='completed', then=Value(1)), default=Value(0))),
                avg_performance=Avg('performance_score'),
                total_modules=Count('id'),
                completed_modules=Count('id', filter=Q(status='completed')),
                avg_session_duration=Avg(F('updated_at') - F('created_at')),
                recent_activity=Count('id', filter=Q(updated_at__gte=end_date - timedelta(days=30)))
            ))
            
            if historical_data:
                features.update(historical_data[0])
            
            # Assessment success patterns
            assessment_data = list(AssessmentAttempt.objects.filter(
                user=user,
                created_at__gte=start_date,
                **({'learning_path_id': learning_path_id} if learning_path_id else {})
            ).aggregate(
                assessment_success_rate=Avg(Case(When(score__gte=0.7, then=Value(1)), default=Value(0))),
                avg_assessment_score=Avg('score'),
                total_assessments=Count('id'),
                recent_assessments=Count('id', filter=Q(completed_at__gte=end_date - timedelta(days=30))),
                assessment_consistency=StdDev('score')
            ))
            
            if assessment_data:
                features.update(assessment_data[0])
            
            # Learning velocity and consistency
            recent_activity = UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=30)
            ).count()
            
            features.update({
                'recent_activity_level': recent_activity,
                'activity_consistency': min(1.0, recent_activity / 10),  # Normalized activity
            })
            
            # Engagement patterns
            engagement_patterns = self.analyze_engagement_patterns(user, learning_path_id)
            if engagement_patterns.get('status') == 'success':
                features.update({
                    'engagement_score': engagement_patterns['engagement_score'],
                    'session_consistency': engagement_patterns.get('session_metrics', {}).get('consistency', 0.5)
                })
            else:
                features.update({
                    'engagement_score': 0.5,
                    'session_consistency': 0.5
                })
            
            # Learning velocity
            velocity_analysis = self.analyze_learning_velocity(user, learning_path_id)
            if velocity_analysis.get('status') == 'success':
                features.update({
                    'velocity_score': velocity_analysis['velocity_score'],
                    'velocity_consistency': velocity_analysis['consistency']
                })
            else:
                features.update({
                    'velocity_score': 0.5,
                    'velocity_consistency': 0.5
                })
            
            # Fill missing values with defaults
            default_values = {
                'completion_rate': 0.5,
                'avg_performance': 0.5,
                'total_modules': 5,
                'completed_modules': 2,
                'avg_assessment_score': 0.5,
                'assessment_success_rate': 0.5,
                'total_assessments': 3,
                'recent_assessments': 1,
                'assessment_consistency': 0.3,
                'engagement_score': 0.5,
                'session_consistency': 0.5,
                'velocity_score': 0.5,
                'velocity_consistency': 0.5,
                'recent_activity_level': 0.5,
                'activity_consistency': 0.5
            }
            
            for key, default_val in default_values.items():
                if key not in features or features[key] is None:
                    features[key] = default_val
            
            # Create feature vector for ML prediction
            feature_vector = np.array([
                features.get('completion_rate', 0.5),
                features.get('avg_performance', 0.5),
                features.get('assessment_success_rate', 0.5),
                features.get('avg_assessment_score', 0.5),
                features.get('engagement_score', 0.5),
                features.get('velocity_score', 0.5),
                features.get('session_consistency', 0.5),
                features.get('velocity_consistency', 0.5),
                features.get('activity_consistency', 0.5),
                min(1.0, features.get('total_modules', 5) / 20),  # Normalized experience
                min(1.0, features.get('total_assessments', 3) / 15)  # Normalized assessments
            ]).reshape(1, -1)
            
            # Use multiple prediction approaches
            
            # 1. Statistical probability calculation
            stat_probability = self._calculate_statistical_success_probability(features)
            
            # 2. Rule-based probability
            rule_probability = self._calculate_rule_based_success_probability(features)
            
            # 3. Ensemble probability (weighted average)
            ensemble_probability = (stat_probability * 0.4 + rule_probability * 0.6)
            
            # Calculate confidence intervals
            uncertainty_factors = [
                1 - abs(features.get('completion_rate', 0.5) - 0.5) * 2,  # Performance certainty
                features.get('session_consistency', 0.5),  # Consistency certainty
                features.get('velocity_consistency', 0.5),  # Velocity certainty
                min(1.0, features.get('total_modules', 5) / 10)  # Data sufficiency
            ]
            
            confidence_score = np.mean(uncertainty_factors)
            
            # Calculate prediction intervals
            std_uncertainty = np.std(uncertainty_factors)
            margin = std_uncertainty * 1.96  # 95% confidence interval
            
            lower_bound = max(0.0, ensemble_probability - margin)
            upper_bound = min(1.0, ensemble_probability + margin)
            
            # Risk factor analysis
            risk_factors = []
            protective_factors = []
            
            # Analyze risk factors
            if features.get('completion_rate', 0.5) < 0.3:
                risk_factors.append("Low historical completion rate")
            elif features.get('completion_rate', 0.5) > 0.7:
                protective_factors.append("Strong historical completion record")
            
            if features.get('engagement_score', 0.5) < 0.4:
                risk_factors.append("Low engagement levels")
            elif features.get('engagement_score', 0.5) > 0.8:
                protective_factors.append("High engagement levels")
            
            if features.get('velocity_consistency', 0.5) < 0.4:
                risk_factors.append("Inconsistent learning pace")
            elif features.get('velocity_consistency', 0.5) > 0.8:
                protective_factors.append("Consistent learning pace")
            
            if features.get('recent_activity_level', 0) < 5:
                risk_factors.append("Low recent activity")
            elif features.get('recent_activity_level', 0) > 15:
                protective_factors.append("High recent activity")
            
            # Generate insights and recommendations
            insights = []
            recommendations = []
            
            if ensemble_probability > 0.7:
                insights.append("High probability of learning success predicted")
                recommendations.append("Continue current learning approach")
            elif ensemble_probability > 0.5:
                insights.append("Moderate probability of learning success")
                recommendations.append("Focus on consistency and engagement")
            else:
                insights.append("Learning success probability needs improvement")
                recommendations.append("Consider additional support and motivation strategies")
            
            if confidence_score < 0.6:
                insights.append("Prediction confidence is low due to limited data")
                recommendations.append("Gather more learning activity data for better predictions")
            
            return {
                'status': 'success',
                'success_probability': float(ensemble_probability),
                'prediction_range': {
                    'lower_bound': float(lower_bound),
                    'upper_bound': float(upper_bound),
                    'confidence_level': 0.95
                },
                'confidence_score': float(confidence_score),
                'methodology': 'Ensemble of statistical and rule-based probability models',
                'contributing_factors': {
                    'statistical_probability': float(stat_probability),
                    'rule_based_probability': float(rule_probability),
                    'ensemble_weight': '60% rule-based, 40% statistical'
                },
                'risk_assessment': {
                    'risk_factors': risk_factors,
                    'protective_factors': protective_factors,
                    'overall_risk_level': 'high' if ensemble_probability < 0.4 else 'medium' if ensemble_probability < 0.7 else 'low'
                },
                'feature_importance': {
                    'performance_history': features.get('completion_rate', 0.5),
                    'engagement_level': features.get('engagement_score', 0.5),
                    'learning_velocity': features.get('velocity_score', 0.5),
                    'consistency': features.get('session_consistency', 0.5)
                },
                'insights': insights,
                'recommendations': recommendations,
                'time_horizon_days': time_horizon_days,
                'prediction_timestamp': end_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error modeling success probability: {e}")
            return {
                'status': 'error',
                'message': f'Success probability modeling failed: {str(e)}',
                'success_probability': 0.5,
                'confidence_score': 0.0
            }
    
    def _calculate_statistical_success_probability(self, features: Dict[str, Any]) -> float:
        """Calculate success probability using statistical methods"""
        try:
            # Performance-based probability
            completion_rate = features.get('completion_rate', 0.5)
            performance_score = features.get('avg_performance', 0.5)
            
            # Engagement factor
            engagement_score = features.get('engagement_score', 0.5)
            session_consistency = features.get('session_consistency', 0.5)
            
            # Activity factor
            recent_activity = min(1.0, features.get('recent_activity_level', 5) / 20)
            activity_consistency = features.get('activity_consistency', 0.5)
            
            # Combine factors with weights
            statistical_probability = (
                completion_rate * 0.25 +
                performance_score * 0.20 +
                engagement_score * 0.20 +
                session_consistency * 0.15 +
                recent_activity * 0.10 +
                activity_consistency * 0.10
            )
            
            return max(0.0, min(1.0, statistical_probability))
            
        except Exception as e:
            logger.error(f"Error in statistical probability calculation: {e}")
            return 0.5
    
    def _calculate_rule_based_success_probability(self, features: Dict[str, Any]) -> float:
        """Calculate success probability using rule-based methods"""
        try:
            probability = 0.5  # Base probability
            
            # Strong performance indicators
            if features.get('completion_rate', 0) > 0.8:
                probability += 0.15
            elif features.get('completion_rate', 0) < 0.2:
                probability -= 0.15
            
            if features.get('assessment_success_rate', 0) > 0.8:
                probability += 0.10
            elif features.get('assessment_success_rate', 0) < 0.3:
                probability -= 0.10
            
            # Engagement indicators
            if features.get('engagement_score', 0) > 0.7:
                probability += 0.10
            elif features.get('engagement_score', 0) < 0.3:
                probability -= 0.10
            
            # Consistency indicators
            if features.get('session_consistency', 0) > 0.7:
                probability += 0.08
            elif features.get('session_consistency', 0) < 0.3:
                probability -= 0.08
            
            # Experience factor
            total_modules = features.get('total_modules', 5)
            if total_modules > 15:
                probability += 0.05  # Experienced learner
            elif total_modules < 3:
                probability -= 0.05  # New learner
            
            return max(0.0, min(1.0, probability))
            
        except Exception as e:
            logger.error(f"Error in rule-based probability calculation: {e}")
            return 0.5
'''
        return method_code
    
    def create_time_to_completion_prediction_method(self) -> str:
        """Create time-to-completion prediction method"""
        method_code = '''
    def predict_time_to_completion(self, user: User, learning_path_id: Optional[int] = None,
                                 target_module_id: Optional[int] = None,
                                 include_holidays: bool = True) -> Dict[str, Any]:
        """
        Predict time required to complete learning objectives.
        
        Args:
            user: User instance
            learning_path_id: Optional learning path for completion prediction
            target_module_id: Optional specific module to focus on
            include_holidays: Whether to account for holidays and breaks
            
        Returns:
            Dict with completion time predictions, confidence intervals, and optimization suggestions
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=180)  # 6 months of data
            
            # Get learning objectives data
            if target_module_id:
                # Single module completion prediction
                modules_to_complete = 1
                query_kwargs = {'id': target_module_id}
                target_type = 'single_module'
            elif learning_path_id:
                # Learning path completion prediction
                total_modules = Module.objects.filter(learning_path_id=learning_path_id).count()
                completed_modules = UserModuleProgress.objects.filter(
                    user=user, learning_path_id=learning_path_id, status='completed'
                ).count()
                modules_to_complete = max(0, total_modules - completed_modules)
                target_type = 'learning_path'
            else:
                # General completion prediction
                completed_modules = UserModuleProgress.objects.filter(
                    user=user, status='completed'
                ).count()
                total_modules = UserModuleProgress.objects.filter(user=user).count()
                modules_to_complete = max(0, total_modules - completed_modules)
                target_type = 'general'
            
            if modules_to_complete == 0:
                return {
                    'status': 'completed',
                    'message': 'All objectives already completed',
                    'completion_status': 'finished',
                    'time_remaining': 0
                }
            
            # Historical completion time analysis
            historical_completions = list(UserModuleProgress.objects.filter(
                user=user,
                status='completed',
                created_at__gte=start_date,
                **({'learning_path_id': learning_path_id} if learning_path_id else {})
            ).annotate(
                completion_time_days=(F('completed_at') - F('started_at'))
            ).values('completion_time_days'))
            
            # Calculate completion velocity
            if historical_completions:
                completion_times = [
                    item['completion_time_days'].total_seconds() / 86400  # Convert to days
                    for item in historical_completions
                    if item['completion_time_days']
                ]
                
                if completion_times:
                    avg_completion_time = np.mean(completion_times)
                    median_completion_time = np.median(completion_times)
                    completion_consistency = 1 - (np.std(completion_times) / np.mean(completion_times)) if np.mean(completion_times) > 0 else 0
                else:
                    avg_completion_time = 14  # Default 2 weeks
                    median_completion_time = 14
                    completion_consistency = 0.5
            else:
                # Estimate based on typical completion patterns
                avg_completion_time = 14  # Default 2 weeks per module
                median_completion_time = 12
                completion_consistency = 0.5
            
            # Factor analysis for time estimation
            
            # 1. Learning velocity adjustment
            velocity_analysis = self.analyze_learning_velocity(user, learning_path_id)
            if velocity_analysis.get('status') == 'success':
                velocity_factor = velocity_analysis.get('velocity_score', 0.5)
                if velocity_factor > 0.7:
                    completion_time_adjustment = 0.8  # 20% faster
                elif velocity_factor < 0.3:
                    completion_time_adjustment = 1.3  # 30% slower
                else:
                    completion_time_adjustment = 1.0
            else:
                completion_time_adjustment = 1.0
            
            # 2. Engagement adjustment
            engagement_analysis = self.analyze_engagement_patterns(user, learning_path_id)
            if engagement_analysis.get('status') == 'success':
                engagement_score = engagement_analysis.get('engagement_score', 0.5)
                session_consistency = engagement_analysis.get('session_metrics', {}).get('consistency', 0.5)
                
                # High engagement and consistency means faster completion
                engagement_factor = (engagement_score + session_consistency) / 2
                if engagement_factor > 0.8:
                    time_reduction = 0.15  # 15% faster
                elif engagement_factor < 0.4:
                    time_increase = 0.25   # 25% slower
                    engagement_factor = 1 + time_increase
                else:
                    engagement_factor = 1.0
            else:
                engagement_factor = 1.0
            
            # 3. Difficulty adjustment based on historical performance
            if historical_completions and 'completion_time_days' in historical_completions[0]:
                # Analyze difficulty progression
                recent_performance = UserModuleProgress.objects.filter(
                    user=user,
                    updated_at__gte=end_date - timedelta(days=30),
                    status='completed'
                ).aggregate(avg_score=Avg('performance_score'))
                
                if recent_performance['avg_score']:
                    performance_factor = recent_performance['avg_score']
                    if performance_factor > 0.9:
                        difficulty_adjustment = 0.9  # Handles harder content faster
                    elif performance_factor < 0.6:
                        difficulty_adjustment = 1.2  # Needs more time for complex topics
                    else:
                        difficulty_adjustment = 1.0
                else:
                    difficulty_adjustment = 1.0
            else:
                difficulty_adjustment = 1.0
            
            # 4. Calculate adjusted completion time per module
            adjusted_time_per_module = (
                median_completion_time * 
                completion_time_adjustment * 
                engagement_factor * 
                difficulty_adjustment
            )
            
            # 5. Calculate total completion time
            base_total_time = adjusted_time_per_module * modules_to_complete
            
            # 6. Account for holidays and breaks if requested
            if include_holidays:
                # Simple holiday adjustment (can be enhanced with calendar data)
                holiday_adjustment = 1.1  # 10% buffer for holidays/breaks
                total_time_with_holidays = base_total_time * holiday_adjustment
            else:
                total_time_with_holidays = base_total_time
            
            # 7. Confidence calculation
            confidence_factors = [
                min(1.0, len(historical_completions) / 10),  # Data sufficiency
                completion_consistency,  # Consistency factor
                engagement_analysis.get('engagement_score', 0.5),  # Engagement reliability
                velocity_analysis.get('confidence', 0.5)  # Velocity reliability
            ]
            
            overall_confidence = np.mean(confidence_factors)
            
            # 8. Prediction intervals
            uncertainty = 1 - overall_confidence
            margin_days = total_time_with_holidays * uncertainty * 0.5
            
            lower_bound = max(0, total_time_with_holidays - margin_days)
            upper_bound = total_time_with_holidays + margin_days
            
            # 9. Milestone predictions
            milestones = []
            if target_type == 'learning_path' and modules_to_complete > 1:
                completion_percentage = completed_modules / (completed_modules + modules_to_complete)
                
                # Predict milestones at 25%, 50%, 75%, and 100% completion
                milestone_points = [0.25, 0.50, 0.75, 1.0]
                for point in milestone_points:
                    if point > completion_percentage:
                        remaining_fraction = (point - completion_percentage) / (1 - completion_percentage)
                        milestone_time = total_time_with_holidays * remaining_fraction
                        milestones.append({
                            'completion_percentage': int(point * 100),
                            'estimated_days': int(milestone_time),
                            'date_estimate': (end_date + timedelta(days=int(milestone_time))).date().isoformat()
                        })
            
            # 10. Optimization suggestions
            optimization_suggestions = []
            
            if overall_confidence < 0.6:
                optimization_suggestions.append("Improve prediction accuracy by maintaining consistent learning schedule")
            
            if velocity_analysis.get('velocity_trend') == 'decelerating':
                optimization_suggestions.append("Focus on maintaining learning momentum")
            
            if engagement_analysis.get('engagement_score', 0.5) < 0.6:
                optimization_suggestions.append("Increase engagement through varied learning activities")
            
            if completion_consistency < 0.4:
                optimization_suggestions.append("Develop more consistent study habits")
            
            # 11. Calculate accelerated completion possibility
            accelerated_completion = {}
            if target_type == 'learning_path' and modules_to_complete > 1:
                # Calculate 25% faster completion
                accelerated_days = total_time_with_holidays * 0.75
                accelerated_completion = {
                    'possible': overall_confidence > 0.5,
                    'estimated_days': int(accelerated_days),
                    'requirements': [
                        "Increase daily study time by 25%",
                        "Maintain high engagement levels",
                        "Focus on high-impact learning activities"
                    ] if overall_confidence > 0.5 else ["Need more consistent learning pattern"]
                }
            
            return {
                'status': 'success',
                'target_type': target_type,
                'completion_status': 'in_progress',
                'time_estimates': {
                    'optimistic': int(total_time_with_holidays * 0.8),
                    'most_likely': int(total_time_with_holidays),
                    'conservative': int(total_time_with_holidays * 1.2),
                    'confidence_interval': {
                        'lower_bound': int(lower_bound),
                        'upper_bound': int(upper_bound),
                        'confidence_level': 0.85
                    }
                },
                'confidence_score': float(overall_confidence),
                'methodology': 'Multi-factor historical analysis with velocity and engagement adjustments',
                'factors_used': {
                    'historical_completion': median_completion_time,
                    'velocity_adjustment': completion_time_adjustment,
                    'engagement_adjustment': engagement_factor,
                    'difficulty_adjustment': difficulty_adjustment,
                    'holiday_buffer': 1.1 if include_holidays else 1.0
                },
                'progress_analysis': {
                    'modules_completed': int(completed_modules),
                    'modules_remaining': int(modules_to_complete),
                    'completion_percentage': float(completed_modules / (completed_modules + modules_to_complete)) if (completed_modules + modules_to_complete) > 0 else 0,
                    'historical_consistency': float(completion_consistency)
                },
                'milestones': milestones,
                'optimization_suggestions': optimization_suggestions,
                'accelerated_completion': accelerated_completion,
                'include_holidays': include_holidays,
                'analysis_timestamp': end_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting time to completion: {e}")
            return {
                'status': 'error',
                'message': f'Completion time prediction failed: {str(e)}',
                'time_estimates': {
                    'most_likely': modules_to_complete * 14 if 'modules_to_complete' in locals() else 14,
                    'confidence_interval': {'lower_bound': 7, 'upper_bound': 21}
                },
                'confidence_score': 0.0
            }
'''
        return method_code
    
    def create_retention_risk_assessment_method(self) -> str:
        """Create retention risk assessment method"""
        method_code = '''
    def assess_retention_risk(self, user: User, learning_path_id: Optional[int] = None,
                            risk_horizon_days: int = 30) -> Dict[str, Any]:
        """
        Assess risk of user dropping out or becoming inactive.
        
        Args:
            user: User instance
            learning_path_id: Optional learning path to focus on
            risk_horizon_days: Days ahead to assess risk
            
        Returns:
            Dict with retention risk assessment, early warning indicators, and intervention suggestions
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=90)  # 3 months of data
            
            # Collect risk indicator data
            risk_indicators = {}
            
            # 1. Activity decline analysis
            recent_activity = UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=30)
            ).count()
            
            older_activity = UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=60),
                updated_at__lt=end_date - timedelta(days=30)
            ).count()
            
            if older_activity > 0:
                activity_trend = (recent_activity - older_activity) / older_activity
            else:
                activity_trend = -1 if recent_activity == 0 else 1
            
            risk_indicators['activity_trend'] = activity_trend
            risk_indicators['recent_activity_level'] = recent_activity
            
            # 2. Engagement decline analysis
            engagement_analysis = self.analyze_engagement_patterns(user, learning_path_id)
            if engagement_analysis.get('status') == 'success':
                current_engagement = engagement_analysis.get('engagement_score', 0.5)
                
                # Compare with historical engagement (simplified)
                historical_engagement = current_engagement  # Would need historical data for proper comparison
                engagement_change = current_engagement - historical_engagement if historical_engagement > 0 else 0
                
                risk_indicators['engagement_level'] = current_engagement
                risk_indicators['engagement_change'] = engagement_change
            else:
                risk_indicators['engagement_level'] = 0.5
                risk_indicators['engagement_change'] = 0
            
            # 3. Performance decline analysis
            recent_performance = UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=30),
                status='completed'
            ).aggregate(avg_score=Avg('performance_score'))
            
            older_performance = UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=60),
                updated_at__lt=end_date - timedelta(days=30),
                status='completed'
            ).aggregate(avg_score=Avg('performance_score'))
            
            current_performance = recent_performance['avg_score'] or 0.5
            past_performance = older_performance['avg_score'] or 0.5
            
            if past_performance > 0:
                performance_change = (current_performance - past_performance) / past_performance
            else:
                performance_change = 0
            
            risk_indicators['performance_level'] = current_performance
            risk_indicators['performance_change'] = performance_change
            
            # 4. Learning velocity analysis
            velocity_analysis = self.analyze_learning_velocity(user, learning_path_id)
            if velocity_analysis.get('status') == 'success':
                risk_indicators.update({
                    'velocity_score': velocity_analysis.get('velocity_score', 0.5),
                    'velocity_trend': velocity_analysis.get('velocity_trend', 'stable'),
                    'learning_consistency': velocity_analysis.get('consistency', 0.5)
                })
            else:
                risk_indicators.update({
                    'velocity_score': 0.5,
                    'velocity_trend': 'stable',
                    'learning_consistency': 0.5
                })
            
            # 5. Streak analysis
            # Calculate learning streak
            learning_dates = list(UserModuleProgress.objects.filter(
                user=user,
                updated_at__gte=end_date - timedelta(days=60)
            ).dates('updated_at', 'day'))
            
            learning_dates.sort()
            
            current_streak = 0
            if learning_dates:
                # Calculate consecutive days ending today
                check_date = end_date.date()
                for date in reversed(learning_dates):
                    if (check_date - date).days <= current_streak + 1:
                        current_streak += 1
                    else:
                        break
            
            # Max historical streak
            max_streak = 0
            temp_streak = 0
            prev_date = None
            
            for date in learning_dates:
                if prev_date and (date - prev_date).days == 1:
                    temp_streak += 1
                else:
                    temp_streak = 1
                
                max_streak = max(max_streak, temp_streak)
                prev_date = date
            
            risk_indicators.update({
                'current_learning_streak': current_streak,
                'max_learning_streak': max_streak,
                'streak_consistency': current_streak / max_streak if max_streak > 0 else 0
            })
            
            # 6. Assessment failure patterns
            failed_assessments = AssessmentAttempt.objects.filter(
                user=user,
                score__lt=0.6,
                completed_at__gte=end_date - timedelta(days=30)
            ).count()
            
            total_assessments = AssessmentAttempt.objects.filter(
                user=user,
                completed_at__gte=end_date - timedelta(days=30)
            ).count()
            
            failure_rate = failed_assessments / total_assessments if total_assessments > 0 else 0
            
            risk_indicators['recent_failure_rate'] = failure_rate
            
            # 7. Calculate composite risk score
            risk_factors = []
            protection_factors = []
            
            # Activity risk factors
            if activity_trend < -0.5:
                risk_factors.append("Significant activity decline")
            elif activity_trend > 0.2:
                protection_factors.append("Strong activity growth")
            
            if recent_activity < 2:
                risk_factors.append("Very low recent activity")
            elif recent_activity > 10:
                protection_factors.append("High recent activity")
            
            # Engagement risk factors
            if risk_indicators['engagement_level'] < 0.3:
                risk_factors.append("Very low engagement")
            elif risk_indicators['engagement_level'] > 0.8:
                protection_factors.append("High engagement")
            
            if risk_indicators['engagement_change'] < -0.2:
                risk_factors.append("Engagement declining")
            elif risk_indicators['engagement_change'] > 0.1:
                protection_factors.append("Engagement improving")
            
            # Performance risk factors
            if risk_indicators['performance_level'] < 0.4:
                risk_factors.append("Poor performance")
            elif risk_indicators['performance_level'] > 0.8:
                protection_factors.append("Strong performance")
            
            if risk_indicators['performance_change'] < -0.2:
                risk_factors.append("Performance declining")
            elif risk_indicators['performance_change'] > 0.1:
                protection_factors.append("Performance improving")
            
            # Velocity risk factors
            if risk_indicators['velocity_trend'] == 'decelerating':
                risk_factors.append("Learning velocity declining")
            elif risk_indicators['velocity_trend'] == 'accelerating':
                protection_factors.append("Learning velocity increasing")
            
            # Streak risk factors
            if current_streak < 3:
                risk_factors.append("Learning streak broken")
            elif current_streak > 7:
                protection_factors.append("Strong learning streak")
            
            # Assessment risk factors
            if failure_rate > 0.5:
                risk_factors.append("High recent failure rate")
            elif failure_rate < 0.2:
                protection_factors.append("Low failure rate")
            
            # Calculate weighted risk score
            base_risk = 0.3  # Base retention risk
            
            # Risk factor weights
            risk_weights = {
                'activity_decline': 0.25,
                'low_activity': 0.20,
                'low_engagement': 0.20,
                'engagement_decline': 0.15,
                'poor_performance': 0.15,
                'performance_decline': 0.15,
                'velocity_decline': 0.10,
                'streak_broken': 0.10,
                'high_failure_rate': 0.10
            }
            
            protection_weights = {
                'activity_growth': -0.15,
                'high_activity': -0.15,
                'high_engagement': -0.15,
                'engagement_improving': -0.10,
                'strong_performance': -0.10,
                'performance_improving': -0.10,
                'velocity_increase': -0.08,
                'strong_streak': -0.12,
                'low_failure_rate': -0.08
            }
            
            risk_score = base_risk
            
            # Apply risk factors
            if "Significant activity decline" in risk_factors:
                risk_score += risk_weights['activity_decline']
            if "Very low recent activity" in risk_factors:
                risk_score += risk_weights['low_activity']
            if "Very low engagement" in risk_factors:
                risk_score += risk_weights['low_engagement']
            if "Engagement declining" in risk_factors:
                risk_score += risk_weights['engagement_decline']
            if "Poor performance" in risk_factors:
                risk_score += risk_weights['poor_performance']
            if "Performance declining" in risk_factors:
                risk_score += risk_weights['performance_decline']
            if "Learning velocity declining" in risk_factors:
                risk_score += risk_weights['velocity_decline']
            if "Learning streak broken" in risk_factors:
                risk_score += risk_weights['streak_broken']
            if "High recent failure rate" in risk_factors:
                risk_score += risk_weights['high_failure_rate']
            
            # Apply protection factors
            if "Strong activity growth" in protection_factors:
                risk_score += protection_weights['activity_growth']
            if "High recent activity" in protection_factors:
                risk_score += protection_weights['high_activity']
            if "High engagement" in protection_factors:
                risk_score += protection_weights['high_engagement']
            if "Engagement improving" in protection_factors:
                risk_score += protection_weights['engagement_improving']
            if "Strong performance" in protection_factors:
                risk_score += protection_weights['strong_performance']
            if "Performance improving" in protection_factors:
                risk_score += protection_weights['performance_improving']
            if "Learning velocity increasing" in protection_factors:
                risk_score += protection_weights['velocity_increase']
            if "Strong learning streak" in protection_factors:
                risk_score += protection_weights['strong_streak']
            if "Low failure rate" in protection_factors:
                risk_score += protection_weights['low_failure_rate']
            
            # Ensure risk score is between 0 and 1
            risk_score = max(0.0, min(1.0, risk_score))
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = 'high'
            elif risk_score > 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            # Calculate confidence based on data availability
            data_factors = [
                min(1.0, recent_activity / 10),  # Activity data
                min(1.0, len(learning_dates) / 20),  # Historical data
                1.0 if engagement_analysis.get('status') == 'success' else 0.5,  # Engagement data
                1.0 if velocity_analysis.get('status') == 'success' else 0.5   # Velocity data
            ]
            
            confidence_score = np.mean(data_factors)
            
            # Early warning indicators
            early_warnings = []
            if risk_score > 0.6:
                early_warnings.append("Multiple risk factors detected")
            if activity_trend < -0.3:
                early_warnings.append("Activity declining rapidly")
            if risk_indicators['engagement_level'] < 0.4:
                early_warnings.append("Engagement below optimal levels")
            if current_streak == 0 and recent_activity == 0:
                early_warnings.append("No recent learning activity")
            
            # Intervention recommendations
            intervention_recommendations = []
            
            if risk_level == 'high':
                intervention_recommendations.extend([
                    "Immediate personal check-in and support",
                    "Provide additional learning resources",
                    "Consider reducing difficulty temporarily",
                    "Schedule regular progress reviews"
                ])
            elif risk_level == 'medium':
                intervention_recommendations.extend([
                    "Send motivational learning tips",
                    "Highlight recent achievements",
                    "Suggest shorter learning sessions",
                    "Provide peer learning opportunities"
                ])
            else:
                intervention_recommendations.extend([
                    "Continue current support level",
                    "Monitor for subtle changes",
                    "Maintain regular engagement"
                ])
            
            # Risk trend prediction
            if len(risk_factors) > len(protection_factors):
                risk_trend = 'increasing'
            elif len(protection_factors) > len(risk_factors):
                risk_trend = 'decreasing'
            else:
                risk_trend = 'stable'
            
            return {
                'status': 'success',
                'risk_assessment': {
                    'overall_risk_score': float(risk_score),
                    'risk_level': risk_level,
                    'risk_trend': risk_trend,
                    'confidence_score': float(confidence_score)
                },
                'risk_factors': risk_factors,
                'protective_factors': protection_factors,
                'early_warning_indicators': early_warnings,
                'intervention_recommendations': intervention_recommendations,
                'detailed_indicators': risk_indicators,
                'risk_horizon_days': risk_horizon_days,
                'assessment_timestamp': end_date.isoformat(),
                'methodology': 'Multi-factor risk analysis with weighted scoring algorithm'
            }
            
        except Exception as e:
            logger.error(f"Error assessing retention risk: {e}")
            return {
                'status': 'error',
                'message': f'Retention risk assessment failed: {str(e)}',
                'risk_assessment': {
                    'overall_risk_score': 0.5,
                    'risk_level': 'unknown',
                    'confidence_score': 0.0
                }
            }
'''
        return method_code
    
    def create_knowledge_gap_detection_method(self) -> str:
        """Create knowledge gap detection method"""
        method_code = '''
    def detect_knowledge_gaps(self, user: User, learning_path_id: Optional[int] = None,
                            analysis_depth: str = 'comprehensive') -> Dict[str, Any]:
        """
        Detect knowledge gaps and learning deficiencies.
        
        Args:
            user: User instance
            learning_path_id: Optional learning path to focus on
            analysis_depth: 'basic', 'standard', or 'comprehensive'
            
        Returns:
            Dict with identified knowledge gaps, proficiency levels, and targeted learning suggestions
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=120)  # 4 months of data
            
            # Get user's learning data
            query_kwargs = {'user': user, 'created_at__gte': start_date}
            if learning_path_id:
                query_kwargs['learning_path_id'] = learning_path_id
            
            # 1. Assessment-based gap analysis
            assessment_results = list(AssessmentAttempt.objects.filter(
                **query_kwargs
            ).values())
            
            # 2. Module performance analysis
            module_performance = list(UserModuleProgress.objects.filter(
                **query_kwargs
            ).values())
            
            knowledge_gaps = []
            proficiency_scores = {}
            
            # 3. Analyze assessment performance by topic/skill
            if assessment_results:
                topic_performance = {}
                
                for assessment in assessment_results:
                    # Extract topic/skills from assessment data (simplified)
                    topic = assessment.get('topic', 'general')
                    score = assessment.get('score', 0)
                    
                    if topic not in topic_performance:
                        topic_performance[topic] = []
                    
                    topic_performance[topic].append(score)
                
                # Identify gaps in each topic
                for topic, scores in topic_performance.items():
                    if scores:
                        avg_score = np.mean(scores)
                        
                        if avg_score < 0.6:  # Below 60%
                            gap_severity = 0.6 - avg_score  # How far below passing
                            
                            knowledge_gaps.append({
                                'topic': topic,
                                'gap_type': 'performance_based',
                                'current_proficiency': float(avg_score),
                                'gap_severity': float(gap_severity),
                                'evidence_count': len(scores),
                                'recent_performance': float(np.mean(scores[-3:])) if len(scores) >= 3 else float(avg_score),
                                'trend': 'improving' if len(scores) >= 3 and np.mean(scores[-3:]) > avg_score else 'declining' if len(scores) >= 3 else 'stable'
                            })
                        
                        proficiency_scores[topic] = float(avg_score)
            
            # 4. Analyze module completion patterns
            if module_performance:
                module_data = {}
                
                for module in module_performance:
                    module_id = module.get('module_id', 'unknown')
                    status = module.get('status', 'in_progress')
                    performance = module.get('performance_score', 0)
                    
                    if module_id not in module_data:
                        module_data[module_id] = {
                            'attempts': [],
                            'status': status,
                            'module_name': module.get('module_name', f'Module {module_id}')
                        }
                    
                    if performance > 0:
                        module_data[module_id]['attempts'].append(performance)
                
                # Identify modules with poor performance or incomplete status
                for module_id, data in module_data.items():
                    if data['attempts']:
                        avg_performance = np.mean(data['attempts'])
                        
                        if avg_performance < 0.7:  # Below 70%
                            knowledge_gaps.append({
                                'topic': data['module_name'],
                                'gap_type': 'module_based',
                                'current_proficiency': float(avg_performance),
                                'gap_severity': float(0.7 - avg_performance),
                                'evidence_count': len(data['attempts']),
                                'recent_performance': float(np.mean(data['attempts'][-3:])) if len(data['attempts']) >= 3 else float(avg_performance),
                                'trend': 'improving' if len(data['attempts']) >= 3 and np.mean(data['attempts'][-3:]) > avg_performance else 'declining' if len(data['attempts']) >= 3 else 'stable'
                            })
                        
                        proficiency_scores[data['module_name']] = float(avg_performance)
                    
                    elif data['status'] in ['in_progress', 'not_started']:
                        knowledge_gaps.append({
                            'topic': data['module_name'],
                            'gap_type': 'completion_based',
                            'current_proficiency': 0.0,
                            'gap_severity': 0.7,  # Assume significant gap for incomplete work
                            'evidence_count': 0,
                            'recent_performance': 0.0,
                            'trend': 'stable',
                            'note': 'Module not completed'
                        })
                        
                        proficiency_scores[data['module_name']] = 0.0
            
            # 5. Analyze skill progression patterns
            if module_performance:
                skill_progression = {}
                
                for module in module_performance:
                    if module.get('difficulty_level') and module.get('performance_score', 0) > 0:
                        difficulty = module['difficulty_level']
                        performance = module['performance_score']
                        
                        if difficulty not in skill_progression:
                            skill_progression[difficulty] = []
                        
                        skill_progression[difficulty].append(performance)
                
                # Find difficulty levels with poor performance
                for difficulty, performances in skill_progression.items():
                    if len(performances) >= 3:  # Need sufficient data
                        avg_performance = np.mean(performances)
                        
                        if avg_performance < 0.6:  # Poor performance at this difficulty
                            knowledge_gaps.append({
                                'topic': f'Skills at difficulty level {difficulty}',
                                'gap_type': 'difficulty_based',
                                'current_proficiency': float(avg_performance),
                                'gap_severity': float(0.6 - avg_performance),
                                'evidence_count': len(performances),
                                'recent_performance': float(np.mean(performances[-3:])) if len(performances) >= 3 else float(avg_performance),
                                'trend': 'improving' if len(performances) >= 3 and np.mean(performances[-3:]) > avg_performance else 'declining' if len(performances) >= 3 else 'stable'
                            })
            
            # 6. Calculate learning velocity impact on gaps
            velocity_analysis = self.analyze_learning_velocity(user, learning_path_id)
            if velocity_analysis.get('status') == 'success':
                velocity_score = velocity_analysis.get('velocity_score', 0.5)
                
                # Higher velocity gaps might indicate rushing through content
                if velocity_score > 0.8 and len(knowledge_gaps) > 0:
                    # Flag potential rushed learning
                    for gap in knowledge_gaps:
                        gap['potential_rushed_learning'] = True
                        gap['velocity_context'] = 'high_velocity_may_cause_superficial_learning'
            else:
                velocity_score = 0.5
            
            # 7. Analyze engagement correlation with gaps
            engagement_analysis = self.analyze_engagement_patterns(user, learning_path_id)
            if engagement_analysis.get('status') == 'success':
                engagement_score = engagement_analysis.get('engagement_score', 0.5)
                
                # Low engagement might correlate with knowledge gaps
                if engagement_score < 0.4 and len(knowledge_gaps) > 0:
                    for gap in knowledge_gaps:
                        gap['potential_engagement_related'] = True
                        gap['engagement_context'] = 'low_engagement_may_contribute_to_gaps'
            else:
                engagement_score = 0.5
            
            # 8. Prioritize gaps by severity and impact
            knowledge_gaps.sort(key=lambda x: x['gap_severity'], reverse=True)
            
            # Calculate overall knowledge coverage
            total_topics = len(proficiency_scores)
            if total_topics > 0:
                avg_proficiency = np.mean(list(proficiency_scores.values()))
                strong_topics = sum(1 for score in proficiency_scores.values() if score >= 0.8)
                weak_topics = sum(1 for score in proficiency_scores.values() if score < 0.6)
                
                knowledge_coverage = {
                    'overall_proficiency': float(avg_proficiency),
                    'strong_topics_count': strong_topics,
                    'weak_topics_count': weak_topics,
                    'coverage_percentage': float(strong_topics / total_topics) if total_topics > 0 else 0,
                    'gap_density': float(len(knowledge_gaps) / total_topics) if total_topics > 0 else 0
                }
            else:
                knowledge_coverage = {
                    'overall_proficiency': 0.0,
                    'strong_topics_count': 0,
                    'weak_topics_count': 0,
                    'coverage_percentage': 0.0,
                    'gap_density': 1.0  # No data means potential gaps
                }
            
            # 9. Generate targeted learning suggestions
            learning_suggestions = []
            
            for gap in knowledge_gaps[:5]:  # Top 5 gaps
                topic = gap['topic']
                gap_severity = gap['gap_severity']
                
                suggestion = {
                    'topic': topic,
                    'priority': 'high' if gap_severity > 0.4 else 'medium' if gap_severity > 0.2 else 'low',
                    'suggested_activities': []
                }
                
                if gap['gap_type'] == 'performance_based':
                    suggestion['suggested_activities'].extend([
                        f"Review {topic} fundamentals",
                        f"Practice {topic} exercises",
                        f"Seek additional {topic} resources"
                    ])
                elif gap['gap_type'] == 'module_based':
                    suggestion['suggested_activities'].extend([
                        f"Retake {topic} module",
                        f"Break down {topic} into smaller concepts",
                        f"Use visual aids for {topic}"
                    ])
                elif gap['gap_type'] == 'completion_based':
                    suggestion['suggested_activities'].extend([
                        f"Start {topic} module",
                        f"Set short-term goals for {topic}",
                        f"Schedule dedicated {topic} study time"
                    ])
                elif gap['gap_type'] == 'difficulty_based':
                    suggestion['suggested_activities'].extend([
                        f"Practice easier {topic} problems first",
                        f"Build foundational {topic} skills",
                        f"Use step-by-step {topic} tutorials"
                    ])
                
                learning_suggestions.append(suggestion)
            
            # 10. Calculate confidence in gap detection
            data_sufficiency_factors = [
                min(1.0, len(assessment_results) / 10),  # Assessment data
                min(1.0, len(module_performance) / 15),  # Module data
                1.0 if velocity_analysis.get('status') == 'success' else 0.5,
                1.0 if engagement_analysis.get('status') == 'success' else 0.5
            ]
            
            detection_confidence = np.mean(data_sufficiency_factors)
            
            return {
                'status': 'success',
                'knowledge_gaps_summary': {
                    'total_gaps_identified': len(knowledge_gaps),
                    'high_priority_gaps': sum(1 for gap in knowledge_gaps if gap['gap_severity'] > 0.4),
                    'medium_priority_gaps': sum(1 for gap in knowledge_gaps if 0.2 < gap['gap_severity'] <= 0.4),
                    'low_priority_gaps': sum(1 for gap in knowledge_gaps if gap['gap_severity'] <= 0.2)
                },
                'knowledge_coverage': knowledge_coverage,
                'detailed_gaps': knowledge_gaps[:10],  # Top 10 most severe gaps
                'proficiency_by_topic': proficiency_scores,
                'learning_suggestions': learning_suggestions,
                'contextual_factors': {
                    'learning_velocity': float(velocity_score),
                    'engagement_level': float(engagement_score),
                    'analysis_depth': analysis_depth
                },
                'detection_confidence': float(detection_confidence),
                'methodology': 'Multi-source performance analysis with gap severity scoring',
                'assessment_timestamp': end_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error detecting knowledge gaps: {e}")
            return {
                'status': 'error',
                'message': f'Knowledge gap detection failed: {str(e)}',
                'knowledge_gaps_summary': {
                    'total_gaps_identified': 0,
                    'high_priority_gaps': 0
                },
                'detection_confidence': 0.0
            }
'''
        return method_code
    
    def create_kmeans_clustering_method(self) -> str:
        """Create K-Means clustering method for learner segmentation"""
        method_code = '''
    def perform_learning_analytics_clustering(self, learning_path_id: Optional[int] = None,
                                           cluster_count: Optional[int] = None,
                                           feature_selection: str = 'comprehensive') -> Dict[str, Any]:
        """
        Perform K-Means clustering analysis for learner segmentation and pattern discovery.
        
        Args:
            learning_path_id: Optional learning path to focus analysis on
            cluster_count: Number of clusters (auto-detected if None)
            feature_selection: 'basic', 'standard', or 'comprehensive'
            
        Returns:
            Dict with cluster analysis, learner segments, and insights
        """
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=90)  # 3 months of data
            
            # Collect learner data for clustering
            users_data = []
            users_metadata = []
            
            query_kwargs = {'created_at__gte': start_date}
            if learning_path_id:
                query_kwargs['learning_path_id'] = learning_path_id
            
            # Get all users with activity in the specified timeframe
            active_users = User.objects.filter(
                id__in=UserModuleProgress.objects.filter(**query_kwargs).values('user_id')
            )
            
            if len(active_users) < 10:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough active users for meaningful clustering analysis',
                    'minimum_required': 10,
                    'current_users': len(active_users)
                }
            
            # Extract features for each user
            for user in active_users[:200]:  # Limit to 200 users for performance
                user_features = self._extract_user_clustering_features(user, learning_path_id, feature_selection)
                if user_features is not None:
                    users_data.append(user_features)
                    users_metadata.append({
                        'user_id': user.id,
                        'username': user.username,
                        'email': user.email
                    })
            
            if len(users_data) < 10:
                return {
                    'status': 'insufficient_data',
                    'message': 'Not enough users with sufficient data for clustering',
                    'processed_users': len(users_data)
                }
            
            # Prepare feature matrix
            feature_matrix = np.array(users_data)
            
            # Handle missing values
            feature_matrix = np.nan_to_num(feature_matrix, nan=0.0, posinf=1.0, neginf=0.0)
            
            # Standardize features
            scaler = StandardScaler()
            feature_matrix_scaled = scaler.fit_transform(feature_matrix)
            
            # Determine optimal number of clusters if not specified
            if cluster_count is None:
                optimal_clusters = self._find_optimal_clusters(feature_matrix_scaled, max_clusters=min(8, len(users_data) // 5))
            else:
                optimal_clusters = cluster_count
            
            # Perform K-Means clustering
            kmeans = KMeans(n_clusters=optimal_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(feature_matrix_scaled)
            
            # Calculate cluster quality metrics
            silhouette_avg = silhouette_score(feature_matrix_scaled, cluster_labels)
            inertia = kmeans.inertia_
            
            # Analyze clusters
            cluster_analysis = {}
            for cluster_id in range(optimal_clusters):
                cluster_mask = cluster_labels == cluster_id
                cluster_users = [users_metadata[i] for i in range(len(users_metadata)) if cluster_mask[i]]
                cluster_features = feature_matrix_scaled[cluster_mask]
                
                if len(cluster_features) > 0:
                    # Calculate cluster characteristics
                    cluster_stats = {
                        'cluster_id': cluster_id,
                        'user_count': len(cluster_users),
                        'percentage_of_total': float(len(cluster_users) / len(users_data) * 100),
                        'feature_means': np.mean(cluster_features, axis=0).tolist(),
                        'feature_stds': np.std(cluster_features, axis=0).tolist()
                    }
                    
                    # Identify dominant features
                    feature_names = self._get_feature_names(feature_selection)
                    dominant_features = []
                    
                    for i, feature_name in enumerate(feature_names):
                        cluster_mean = cluster_stats['feature_means'][i]
                        overall_mean = np.mean(feature_matrix_scaled[:, i])
                        
                        if abs(cluster_mean - overall_mean) > 0.5:  # Significant deviation
                            dominant_features.append({
                                'feature': feature_name,
                                'cluster_value': float(cluster_mean),
                                'overall_mean': float(overall_mean),
                                'deviation': float(cluster_mean - overall_mean),
                                'significance': 'high' if abs(cluster_mean - overall_mean) > 1.0 else 'moderate'
                            })
                    
                    cluster_stats['dominant_features'] = dominant_features
                    
                    # Generate cluster description
                    cluster_description = self._generate_cluster_description(cluster_stats, feature_names)
                    cluster_stats['description'] = cluster_description
                    
                    # Calculate cluster quality
                    if len(cluster_features) > 1:
                        cluster_inertia = np.sum((cluster_features - np.mean(cluster_features, axis=0))**2)
                        cluster_stats['cohesion'] = float(1 - (cluster_inertia / inertia)) if inertia > 0 else 0.5
                    else:
                        cluster_stats['cohesion'] = 1.0
                    
                    cluster_analysis[f'cluster_{cluster_id}'] = cluster_stats
            
            # Feature importance analysis
            feature_importance = self._analyze_feature_importance(feature_matrix_scaled, cluster_labels, feature_names)
            
            # Cross-cluster comparison
            cluster_comparisons = self._compare_clusters(cluster_analysis, feature_names)
            
            # Generate insights and recommendations
            insights = []
            recommendations = []
            
            # Overall clustering insights
            insights.append(f"Identified {optimal_clusters} distinct learner segments")
            insights.append(f"Clustering quality (silhouette score): {silhouette_avg:.3f}")
            
            if silhouette_avg > 0.5:
                insights.append("Strong cluster separation detected")
                recommendations.append("Use clusters for targeted learning interventions")
            elif silhouette_avg > 0.3:
                insights.append("Moderate cluster separation")
                recommendations.append("Consider cluster-based personalization with caution")
            else:
                insights.append("Weak cluster separation - learners are heterogeneous")
                recommendations.append("Focus on individual personalization over cluster-based approaches")
            
            # Specific cluster insights
            for cluster_id, cluster_data in cluster_analysis.items():
                if cluster_data['user_count'] >= 5:  # Only significant clusters
                    insights.append(f"Cluster {cluster_data['cluster_id']}: {cluster_data['description']} ({cluster_data['user_count']} users, {cluster_data['percentage_of_total']:.1f}%)")
            
            # Actionable recommendations
            largest_cluster = max(cluster_analysis.values(), key=lambda x: x['user_count'])
            smallest_cluster = min(cluster_analysis.values(), key=lambda x: x['user_count'])
            
            recommendations.append(f"Focus resources on largest segment: {largest_cluster['cluster_id']} ({largest_cluster['user_count']} users)")
            recommendations.append(f"Provide specialized support for smallest segment: {smallest_cluster['cluster_id']} ({smallest_cluster['user_count']} users)")
            
            return {
                'status': 'success',
                'clustering_results': {
                    'optimal_clusters': optimal_clusters,
                    'actual_clusters': len(cluster_analysis),
                    'total_users_analyzed': len(users_data),
                    'silhouette_score': float(silhouette_avg),
                    'inertia': float(inertia),
                    'clustering_quality': 'excellent' if silhouette_avg > 0.7 else 'good' if silhouette_avg > 0.5 else 'moderate' if silhouette_avg > 0.3 else 'poor'
                },
                'cluster_analysis': cluster_analysis,
                'feature_importance': feature_importance,
                'cross_cluster_comparisons': cluster_comparisons,
                'learner_segments': [
                    {
                        'segment_id': cluster_id,
                        'description': cluster_data['description'],
                        'size': cluster_data['user_count'],
                        'percentage': cluster_data['percentage_of_total'],
                        'key_characteristics': [feat['feature'] for feat in cluster_data['dominant_features'][:3]]
                    }
                    for cluster_id, cluster_data in cluster_analysis.items()
                ],
                'insights': insights,
                'recommendations': recommendations,
                'methodology': 'K-Means clustering with standardized features and silhouette analysis',
                'feature_selection': feature_selection,
                'analysis_timestamp': end_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error performing clustering analysis: {e}")
            return {
                'status': 'error',
                'message': f'Clustering analysis failed: {str(e)}',
                'clustering_results': {
                    'optimal_clusters': 0,
                    'total_users_analyzed': 0
                }
            }
    
    def _extract_user_clustering_features(self, user: User, learning_path_id: Optional[int], 
                                        feature_selection: str) -> Optional[List[float]]:
        """Extract features for clustering from user data"""
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=90)
            
            features = []
            
            query_kwargs = {'user': user, 'created_at__gte': start_date}
            if learning_path_id:
                query_kwargs['learning_path_id'] = learning_path_id
            
            # Basic features (always included)
            if feature_selection in ['basic', 'standard', 'comprehensive']:
                # Completion rate
                total_modules = UserModuleProgress.objects.filter(**query_kwargs).count()
                completed_modules = UserModuleProgress.objects.filter(**query_kwargs, status='completed').count()
                completion_rate = completed_modules / total_modules if total_modules > 0 else 0
                features.append(completion_rate)
                
                # Average performance
                avg_performance = UserModuleProgress.objects.filter(
                    **query_kwargs, performance_score__isnull=False
                ).aggregate(avg_score=Avg('performance_score'))['avg_score'] or 0.5
                features.append(avg_performance)
                
                # Activity level
                activity_level = UserModuleProgress.objects.filter(**query_kwargs).count()
                features.append(min(1.0, activity_level / 50))  # Normalized
                
                # Engagement score
                engagement_analysis = self.analyze_engagement_patterns(user, learning_path_id)
                engagement_score = engagement_analysis.get('engagement_score', 0.5) if engagement_analysis.get('status') == 'success' else 0.5
                features.append(engagement_score)
            
            # Standard features
            if feature_selection in ['standard', 'comprehensive']:
                # Learning velocity
                velocity_analysis = self.analyze_learning_velocity(user, learning_path_id)
                velocity_score = velocity_analysis.get('velocity_score', 0.5) if velocity_analysis.get('status') == 'success' else 0.5
                features.append(velocity_score)
                
                # Assessment success rate
                assessment_data = AssessmentAttempt.objects.filter(**query_kwargs)
                total_assessments = assessment_data.count()
                successful_assessments = assessment_data.filter(score__gte=0.7).count()
                assessment_success_rate = successful_assessments / total_assessments if total_assessments > 0 else 0.5
                features.append(assessment_success_rate)
                
                # Session consistency
                session_consistency = engagement_analysis.get('session_metrics', {}).get('consistency', 0.5) if engagement_analysis.get('status') == 'success' else 0.5
                features.append(session_consistency)
            
            # Comprehensive features
            if feature_selection == 'comprehensive':
                # Retention risk
                retention_analysis = self.assess_retention_risk(user, learning_path_id)
                retention_risk = retention_analysis.get('risk_assessment', {}).get('overall_risk_score', 0.5) if retention_analysis.get('status') == 'success' else 0.5
                features.append(1 - retention_risk)  # Invert for positive feature
                
                # Knowledge gap density
                gap_analysis = self.detect_knowledge_gaps(user, learning_path_id)
                gap_density = gap_analysis.get('knowledge_coverage', {}).get('gap_density', 0.5) if gap_analysis.get('status') == 'success' else 0.5
                features.append(1 - gap_density)  # Invert for positive feature
                
                # Success probability
                success_analysis = self.model_success_probability(user, learning_path_id)
                success_probability = success_analysis.get('success_probability', 0.5) if success_analysis.get('status') == 'success' else 0.5
                features.append(success_probability)
            
            # Ensure we have enough features for clustering
            if len(features) < 3:
                return None
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting clustering features for user {user.id}: {e}")
            return None
    
    def _get_feature_names(self, feature_selection: str) -> List[str]:
        """Get feature names based on selection type"""
        base_features = ['completion_rate', 'avg_performance', 'activity_level', 'engagement_score']
        standard_features = ['velocity_score', 'assessment_success_rate', 'session_consistency']
        comprehensive_features = ['retention_protection', 'knowledge_coverage', 'success_probability']
        
        if feature_selection == 'basic':
            return base_features
        elif feature_selection == 'standard':
            return base_features + standard_features
        else:  # comprehensive
            return base_features + standard_features + comprehensive_features
    
    def _find_optimal_clusters(self, feature_matrix: np.ndarray, max_clusters: int = 8) -> int:
        """Find optimal number of clusters using elbow method and silhouette analysis"""
        try:
            if len(feature_matrix) < 4:
                return 2
            
            max_clusters = min(max_clusters, len(feature_matrix) // 2)
            if max_clusters < 2:
                return 2
            
            inertias = []
            silhouette_scores = []
            k_range = range(2, max_clusters + 1)
            
            for k in k_range:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(feature_matrix)
                
                inertias.append(kmeans.inertia_)
                silhouette_avg = silhouette_score(feature_matrix, cluster_labels)
                silhouette_scores.append(silhouette_avg)
            
            # Find elbow point in inertia
            if len(inertias) >= 3:
                # Simple elbow detection
                deltas = [inertias[i] - inertias[i+1] for i in range(len(inertias)-1)]
                second_deltas = [deltas[i] - deltas[i+1] for i in range(len(deltas)-1)]
                
                if second_deltas:
                    elbow_index = second_deltas.index(max(second_deltas))
                    elbow_clusters = k_range[elbow_index + 1]  # +1 because we start from 2
                else:
                    elbow_clusters = k_range[len(k_range)//2]
            else:
                elbow_clusters = k_range[len(k_range)//2]
            
            # Find best silhouette score
            best_silhouette_index = silhouette_scores.index(max(silhouette_scores))
            silhouette_clusters = k_range[best_silhouette_index]
            
            # Use silhouette score preference if reasonable, otherwise use elbow
            if silhouette_scores[best_silhouette_index] > 0.3:
                return silhouette_clusters
            else:
                return max(2, min(elbow_clusters, silhouette_clusters))
                
        except Exception as e:
            logger.error(f"Error finding optimal clusters: {e}")
            return min(4, max(2, len(feature_matrix) // 10))
    
    def _generate_cluster_description(self, cluster_stats: Dict[str, Any], feature_names: List[str]) -> str:
        """Generate human-readable description for a cluster"""
        try:
            dominant_features = cluster_stats.get('dominant_features', [])
            
            if not dominant_features:
                return "Average learners with typical patterns"
            
            # Identify cluster characteristics
            characteristics = []
            
            for feature in dominant_features[:3]:  # Top 3 features
                feature_name = feature['feature']
                deviation = feature['deviation']
                
                if 'completion_rate' in feature_name:
                    if deviation > 0:
                        characteristics.append("High completion rates")
                    else:
                        characteristics.append("Low completion rates")
                elif 'performance' in feature_name:
                    if deviation > 0:
                        characteristics.append("Strong performance")
                    else:
                        characteristics.append("Weak performance")
                elif 'engagement' in feature_name:
                    if deviation > 0:
                        characteristics.append("High engagement")
                    else:
                        characteristics.append("Low engagement")
                elif 'velocity' in feature_name:
                    if deviation > 0:
                        characteristics.append("Fast learners")
                    else:
                        characteristics.append("Slow learners")
                elif 'consistency' in feature_name:
                    if deviation > 0:
                        characteristics.append("Consistent learners")
                    else:
                        characteristics.append("Inconsistent learners")
            
            if characteristics:
                return " & ".join(characteristics[:2])  # Limit to 2 characteristics
            else:
                return "Moderate learners"
                
        except Exception as e:
            logger.error(f"Error generating cluster description: {e}")
            return "Learner segment"
    
    def _analyze_feature_importance(self, feature_matrix: np.ndarray, cluster_labels: np.ndarray, 
                                  feature_names: List[str]) -> Dict[str, float]:
        """Analyze feature importance for clustering"""
        try:
            feature_importance = {}
            
            for i, feature_name in enumerate(feature_names):
                feature_values = feature_matrix[:, i]
                
                # Calculate feature variance between clusters
                cluster_means = []
                for cluster_id in np.unique(cluster_labels):
                    cluster_mask = cluster_labels == cluster_id
                    cluster_mean = np.mean(feature_values[cluster_mask])
                    cluster_means.append(cluster_mean)
                
                # Importance is variance of cluster means
                if len(cluster_means) > 1:
                    importance = np.var(cluster_means)
                else:
                    importance = 0
                
                feature_importance[feature_name] = float(importance)
            
            # Normalize importance scores
            max_importance = max(feature_importance.values()) if feature_importance.values() else 1
            if max_importance > 0:
                for feature in feature_importance:
                    feature_importance[feature] /= max_importance
            
            return feature_importance
            
        except Exception as e:
            logger.error(f"Error analyzing feature importance: {e}")
            return {name: 1.0/len(feature_names) for name in feature_names}
    
    def _compare_clusters(self, cluster_analysis: Dict[str, Any], feature_names: List[str]) -> Dict[str, Any]:
        """Generate cross-cluster comparisons"""
        try:
            comparisons = {}
            cluster_ids = list(cluster_analysis.keys())
            
            for i, cluster1_id in enumerate(cluster_ids):
                for cluster2_id in cluster_ids[i+1:]:
                    cluster1 = cluster_analysis[cluster1_id]
                    cluster2 = cluster_analysis[cluster2_id]
                    
                    comparison_key = f"{cluster1_id}_vs_{cluster2_id}"
                    
                    # Calculate differences in key features
                    feature_differences = []
                    for j, feature_name in enumerate(feature_names):
                        if j < len(cluster1['feature_means']) and j < len(cluster2['feature_means']):
                            diff = abs(cluster1['feature_means'][j] - cluster2['feature_means'][j])
                            feature_differences.append({
                                'feature': feature_name,
                                'difference': float(diff)
                            })
                    
                    feature_differences.sort(key=lambda x: x['difference'], reverse=True)
                    
                    comparisons[comparison_key] = {
                        'most_different_features': feature_differences[:3],
                        'user_count_difference': cluster2['user_count'] - cluster1['user_count'],
                        'similarity_score': 1 - np.mean([fd['difference'] for fd in feature_differences])
                    }
            
            return comparisons
            
        except Exception as e:
            logger.error(f"Error comparing clusters: {e}")
            return {}
'''
        return method_code
    
    def integrate_all_methods(self) -> Dict[str, Any]:
        """Integrate all 6 predictive learning models and K-Means clustering"""
        try:
            print("🔄 Integrating remaining predictive learning models...")
            
            # Get the file path for predictive analytics service
            service_file_path = '/workspace/backend/apps/progress/services/predictive_analytics_service.py'
            
            # Read existing file
            with open(service_file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Create all method implementations
            methods_to_add = {
                'learning_velocity_analysis': self.create_learning_velocity_analysis_method(),
                'engagement_pattern_analysis': self.create_engagement_pattern_analysis_method(),
                'success_probability_modeling': self.create_success_probability_modeling_method(),
                'time_to_completion_prediction': self.create_time_to_completion_prediction_method(),
                'retention_risk_assessment': self.create_retention_risk_assessment_method(),
                'knowledge_gap_detection': self.create_knowledge_gap_detection_method(),
                'kmeans_clustering_algorithm': self.create_kmeans_clustering_method()
            }
            
            # Insert methods before the last few methods
            insert_position = existing_content.rfind('        except Exception as e:')
            
            if insert_position == -1:
                # Find another suitable insertion point
                insert_position = existing_content.rfind('    def _calculate_mean_confidence_interval(')
                if insert_position == -1:
                    raise ValueError("Could not find suitable insertion point in the file")
            
            # Create the combined methods content
            methods_content = "\n".join(methods_to_add.values())
            
            # Insert the methods
            new_content = (
                existing_content[:insert_position] +
                "\n" + methods_content + "\n" +
                existing_content[insert_position:]
            )
            
            # Write the updated content
            with open(service_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Mark all methods as integrated
            for method_name in methods_to_add.keys():
                self.integration_results[method_name] = True
            
            print("✅ Successfully integrated all 6 predictive learning models and K-Means clustering!")
            
            return {
                'status': 'success',
                'message': 'All predictive learning models integrated successfully',
                'integrated_methods': list(methods_to_add.keys()),
                'integration_results': self.integration_results,
                'file_updated': service_file_path,
                'methods_added': len(methods_to_add)
            }
            
        except Exception as e:
            logger.error(f"Error integrating predictive learning models: {e}")
            return {
                'status': 'error',
                'message': f'Integration failed: {str(e)}',
                'integration_results': self.integration_results
            }

def main():
    """Main integration process"""
    print("🚀 Starting Integration of Remaining Predictive Learning Models")
    print("=" * 70)
    
    # Initialize integrator
    integrator = PredictiveLearningModelsIntegrator()
    
    # Integrate all methods
    result = integrator.integrate_all_methods()
    
    print("\n" + "=" * 70)
    print("📊 INTEGRATION SUMMARY")
    print("=" * 70)
    
    if result['status'] == 'success':
        print(f"✅ Status: {result['status']}")
        print(f"📝 Message: {result['message']}")
        print(f"🔧 Methods Added: {result['methods_added']}")
        print(f"📁 File Updated: {result['file_updated']}")
        
        print("\n📋 INTEGRATED METHODS:")
        for method, integrated in result['integration_results'].items():
            status_icon = "✅" if integrated else "❌"
            print(f"   {status_icon} {method.replace('_', ' ').title()}")
        
        print(f"\n🎯 INTEGRATION SUCCESS: All {result['methods_added']} predictive learning models integrated!")
        
    else:
        print(f"❌ Status: {result['status']}")
        print(f"⚠️  Message: {result['message']}")
        
        print("\n📋 INTEGRATION STATUS:")
        for method, integrated in result['integration_results'].items():
            status_icon = "✅" if integrated else "❌"
            print(f"   {status_icon} {method.replace('_', ' ').title()}")
    
    return result

if __name__ == "__main__":
    result = main()
    exit(0 if result['status'] == 'success' else 1)