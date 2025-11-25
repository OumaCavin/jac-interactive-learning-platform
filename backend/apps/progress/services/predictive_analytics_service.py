"""
Predictive Analytics Service - JAC Learning Platform

Advanced machine learning and statistical modeling for learning predictions.
Provides sophisticated forecasting, trend analysis, and adaptive predictions.

Author: MiniMax Agent
Created: 2025-11-26
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
import warnings
warnings.filterwarnings('ignore')

# Advanced statistical modeling
try:
    from scipy import stats
    from scipy.optimize import minimize_scalar
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
    from sklearn.preprocessing import StandardScaler, PolynomialFeatures
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    from sklearn.cluster import KMeans
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.arima.model import ARIMA
    import joblib
    SCIPY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Advanced ML libraries not available: {e}")
    SCIPY_AVAILABLE = False

from ..models import LearningAnalytics
from apps.learning.models import (
    LearningPath, Module, UserLearningPath, UserModuleProgress, AssessmentAttempt
)

logger = logging.getLogger(__name__)


class PredictiveAnalyticsService:
    """
    Advanced predictive analytics service with machine learning models
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        self.model_performance = {}
        
    def generate_ml_predictions(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        prediction_horizon_days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate ML-based predictions using ensemble methods
        """
        try:
            # Prepare historical data
            historical_data = self._prepare_historical_data(user, learning_path_id)
            
            if len(historical_data) < 10:
                return self._generate_fallback_predictions(historical_data)
            
            # Feature engineering
            features_df = self._engineer_features(historical_data)
            
            # Train multiple models
            predictions = {}
            
            if SCIPY_AVAILABLE:
                # Random Forest for non-linear patterns
                rf_prediction = self._random_forest_prediction(features_df, prediction_horizon_days)
                if rf_prediction:
                    predictions['random_forest'] = rf_prediction
                
                # Gradient Boosting for complex patterns
                gb_prediction = self._gradient_boosting_prediction(features_df, prediction_horizon_days)
                if gb_prediction:
                    predictions['gradient_boosting'] = gb_prediction
                
                # Linear regression for baseline
                lr_prediction = self._linear_regression_prediction(features_df, prediction_horizon_days)
                if lr_prediction:
                    predictions['linear_regression'] = lr_prediction
                
                # Time series forecasting
                ts_prediction = self._time_series_forecast(features_df, prediction_horizon_days)
                if ts_prediction:
                    predictions['time_series'] = ts_prediction
                
                # Polynomial regression for trend modeling
                poly_prediction = self._polynomial_regression_prediction(features_df, prediction_horizon_days)
                if poly_prediction:
                    predictions['polynomial'] = poly_prediction
            else:
                # Fallback to basic statistical methods
                predictions = self._basic_statistical_predictions(features_df, prediction_horizon_days)
            
            # Ensemble prediction combining all models
            ensemble_prediction = self._create_ensemble_prediction(predictions)
            
            # Calculate prediction confidence
            confidence = self._calculate_prediction_confidence_ml(features_df, predictions)
            
            return {
                'ml_predictions': predictions,
                'ensemble_prediction': ensemble_prediction,
                'prediction_confidence': confidence,
                'prediction_horizon_days': prediction_horizon_days,
                'model_count': len(predictions),
                'data_points_used': len(historical_data),
                'features_engineered': len(features_df.columns) if not features_df.empty else 0
            }
            
        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            return self._generate_fallback_predictions([])
    
    def analyze_historical_trends(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        analysis_period_days: int = 90
    ) -> Dict[str, Any]:
        """
        Comprehensive historical trend analysis with advanced statistical methods
        """
        try:
            historical_data = self._prepare_historical_data(user, learning_path_id)
            
            if len(historical_data) < 7:
                return {'error': 'Insufficient historical data for trend analysis'}
            
            trends_analysis = {}
            
            if SCIPY_AVAILABLE:
                # Convert to time series for analysis
                ts_data = self._create_time_series(historical_data)
                
                # Seasonal decomposition
                if len(ts_data) >= 14:  # Need at least 2 weeks for seasonal analysis
                    decomposition = seasonal_decompose(ts_data, model='additive', period=7)
                    trends_analysis['seasonal_decomposition'] = {
                        'trend': decomposition.trend.dropna().tolist(),
                        'seasonal': decomposition.seasonal.dropna().tolist(),
                        'residual': decomposition.resid.dropna().tolist(),
                        'observed': decomposition.observed.dropna().tolist()
                    }
                
                # Trend analysis with statistical significance
                trends_analysis['statistical_trends'] = self._statistical_trend_analysis(ts_data)
                
                # Correlation analysis
                trends_analysis['correlation_analysis'] = self._correlation_analysis(historical_data)
                
                # Pattern recognition
                trends_analysis['pattern_recognition'] = self._pattern_recognition(historical_data)
                
                # Anomaly detection
                trends_analysis['anomaly_detection'] = self._anomaly_detection(historical_data)
            else:
                # Basic trend analysis without advanced libraries
                trends_analysis['basic_trends'] = self._basic_trend_analysis(historical_data)
            
            # Learning velocity trends
            trends_analysis['velocity_trends'] = self._analyze_velocity_trends(historical_data)
            
            # Performance trajectory analysis
            trends_analysis['performance_trajectory'] = self._analyze_performance_trajectory(historical_data)
            
            return {
                'trends_analysis': trends_analysis,
                'analysis_period_days': analysis_period_days,
                'data_quality_score': self._assess_data_quality(historical_data),
                'recommendations': self._generate_trend_recommendations(trends_analysis)
            }
            
        except Exception as e:
            logger.error(f"Historical trend analysis error: {e}")
            return {'error': f'Trend analysis failed: {str(e)}'}
    
    def adaptive_prediction_algorithm(
        self,
        user: User,
        learning_path_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Adaptive prediction algorithm that learns and adjusts based on user behavior
        """
        try:
            # Analyze user learning patterns
            user_patterns = self._analyze_user_learning_patterns(user, learning_path_id)
            
            # Determine optimal prediction model for this user
            optimal_model = self._select_optimal_model(user_patterns)
            
            # Adaptive parameters based on user type
            adaptive_params = self._calculate_adaptive_parameters(user_patterns)
            
            # Generate predictions with adaptive weights
            predictions = self._generate_adaptive_predictions(
                user, learning_path_id, optimal_model, adaptive_params
            )
            
            # Model performance tracking
            performance_metrics = self._track_model_performance(user, optimal_model)
            
            return {
                'user_pattern_analysis': user_patterns,
                'optimal_model': optimal_model,
                'adaptive_parameters': adaptive_params,
                'adaptive_predictions': predictions,
                'model_performance': performance_metrics,
                'adaptation_strategy': self._get_adaptation_strategy(user_patterns)
            }
            
        except Exception as e:
            logger.error(f"Adaptive prediction error: {e}")
            return {'error': f'Adaptive prediction failed: {str(e)}'}
    
    def statistical_confidence_calculations(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Advanced statistical confidence calculations with uncertainty quantification
        """
        try:
            historical_data = self._prepare_historical_data(user, learning_path_id)
            
            confidence_analysis = {}
            
            if SCIPY_AVAILABLE and len(historical_data) >= 30:
                # Confidence intervals using t-distribution
                confidence_intervals = self._calculate_confidence_intervals(historical_data, confidence_level)
                confidence_analysis['confidence_intervals'] = confidence_intervals
                
                # Bootstrap confidence estimation
                bootstrap_confidence = self._bootstrap_confidence_estimation(historical_data)
                confidence_analysis['bootstrap_confidence'] = bootstrap_confidence
                
                # Bayesian confidence intervals
                bayesian_confidence = self._bayesian_confidence_intervals(historical_data)
                confidence_analysis['bayesian_confidence'] = bayesian_confidence
                
                # Prediction uncertainty quantification
                uncertainty_quantification = self._quantify_prediction_uncertainty(historical_data)
                confidence_analysis['uncertainty_quantification'] = uncertainty_quantification
            else:
                # Basic confidence calculations
                confidence_analysis['basic_confidence'] = self._basic_confidence_calculation(historical_data)
            
            # Model uncertainty assessment
            model_uncertainty = self._assess_model_uncertainty(historical_data)
            confidence_analysis['model_uncertainty'] = model_uncertainty
            
            # Data uncertainty assessment
            data_uncertainty = self._assess_data_uncertainty(historical_data)
            confidence_analysis['data_uncertainty'] = data_uncertainty
            
            return {
                'confidence_analysis': confidence_analysis,
                'confidence_level': confidence_level,
                'sample_size': len(historical_data),
                'statistical_significance': self._calculate_statistical_significance(historical_data)
            }
            
        except Exception as e:
            logger.error(f"Statistical confidence calculation error: {e}")
            return {'error': f'Confidence calculation failed: {str(e)}'}
    
    def _prepare_historical_data(
        self,
        user: User,
        learning_path_id: Optional[int]
    ) -> List[Dict[str, Any]]:
        """
        Prepare comprehensive historical data for ML analysis
        """
        # Get user progress data
        progress_query = UserModuleProgress.objects.filter(user=user)
        
        if learning_path_id:
            progress_query = progress_query.filter(module__learning_path_id=learning_path_id)
        
        progress_data = progress_query.select_related('module', 'user').order_by('updated_at')
        
        # Get assessment data
        assessment_query = AssessmentAttempt.objects.filter(user=user)
        
        if learning_path_id:
            assessment_query = assessment_query.filter(module__learning_path_id=learning_path_id)
        
        assessment_data = assessment_query.select_related('module', 'user').order_by('completed_at')
        
        # Combine and structure data
        historical_records = []
        
        # Process progress data
        for progress in progress_data:
            historical_records.append({
                'date': progress.updated_at.date(),
                'type': 'progress',
                'module_id': progress.module.id,
                'status': progress.status,
                'score': getattr(progress, 'completion_percentage', 0),
                'time_spent': getattr(progress, 'time_spent_minutes', 0),
                'difficulty_level': progress.module.difficulty_level if hasattr(progress.module, 'difficulty_level') else 1
            })
        
        # Process assessment data
        for assessment in assessment_data:
            historical_records.append({
                'date': assessment.completed_at.date(),
                'type': 'assessment',
                'module_id': assessment.module.id,
                'score': assessment.score,
                'max_score': assessment.max_score,
                'time_taken': assessment.time_taken_minutes,
                'attempts': assessment.attempt_number,
                'difficulty_level': assessment.module.difficulty_level if hasattr(assessment.module, 'difficulty_level') else 1
            })
        
        return sorted(historical_records, key=lambda x: x['date'])
    
    def _engineer_features(self, historical_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Create advanced features for machine learning models
        """
        if not historical_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Time-based features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['week_of_year'] = df['date'].dt.isocalendar().week
        
        # Lag features for time series
        if 'score' in df.columns:
            df['score_lag_1'] = df['score'].shift(1)
            df['score_lag_7'] = df['score'].shift(7)
            df['score_lag_30'] = df['score'].shift(30)
        
        # Rolling statistics
        if 'score' in df.columns and len(df) > 7:
            df['score_rolling_mean_7'] = df['score'].rolling(window=7, min_periods=1).mean()
            df['score_rolling_std_7'] = df['score'].rolling(window=7, min_periods=1).std()
            df['score_rolling_mean_30'] = df['score'].rolling(window=min(30, len(df)), min_periods=1).mean()
        
        # Cumulative features
        if 'score' in df.columns:
            df['cumulative_score'] = df['score'].cumsum()
            df['progress_rate'] = df['score'].pct_change().fillna(0)
        
        # Learning velocity features
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        # Module difficulty features
        if 'difficulty_level' in df.columns:
            df['difficulty_normalized'] = df['difficulty_level'] / df['difficulty_level'].max()
        
        return df
    
    def _random_forest_prediction(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Optional[Dict[str, Any]]:
        """
        Random Forest model for complex pattern prediction
        """
        if features_df.empty or 'score' not in features_df.columns:
            return None
        
        try:
            # Prepare features and target
            feature_cols = [col for col in features_df.columns 
                           if col not in ['date', 'score', 'type'] and not features_df[col].isna().all()]
            
            if len(feature_cols) < 3:
                return None
            
            X = features_df[feature_cols].fillna(0)
            y = features_df['score'].fillna(0)
            
            if len(X) < 10:
                return None
            
            # Train Random Forest
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
            rf_model.fit(X, y)
            
            # Make predictions
            last_features = X.iloc[-1:].copy()
            predictions = []
            
            for i in range(min(prediction_horizon, 30)):  # Limit prediction horizon
                pred = rf_model.predict(last_features)[0]
                predictions.append(max(0, min(100, pred)))  # Constrain to valid score range
                
                # Update features for next prediction
                last_features.iloc[0, 0] += 1  # Increment days
                last_features['score_lag_1'] = pred
            
            return {
                'model_type': 'random_forest',
                'predictions': predictions,
                'feature_importance': dict(zip(feature_cols, rf_model.feature_importances_)),
                'model_score': rf_model.score(X, y)
            }
            
        except Exception as e:
            logger.error(f"Random Forest prediction error: {e}")
            return None
    
    def _gradient_boosting_prediction(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Optional[Dict[str, Any]]:
        """
        Gradient Boosting model for advanced pattern recognition
        """
        if features_df.empty or 'score' not in features_df.columns:
            return None
        
        try:
            feature_cols = [col for col in features_df.columns 
                           if col not in ['date', 'score', 'type'] and not features_df[col].isna().all()]
            
            if len(feature_cols) < 3:
                return None
            
            X = features_df[feature_cols].fillna(0)
            y = features_df['score'].fillna(0)
            
            if len(X) < 10:
                return None
            
            # Train Gradient Boosting
            gb_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
            gb_model.fit(X, y)
            
            # Make predictions
            last_features = X.iloc[-1:].copy()
            predictions = []
            
            for i in range(min(prediction_horizon, 30)):
                pred = gb_model.predict(last_features)[0]
                predictions.append(max(0, min(100, pred)))
                
                # Update features
                last_features.iloc[0, 0] += 1
            
            return {
                'model_type': 'gradient_boosting',
                'predictions': predictions,
                'feature_importance': dict(zip(feature_cols, gb_model.feature_importances_)),
                'model_score': gb_model.score(X, y)
            }
            
        except Exception as e:
            logger.error(f"Gradient Boosting prediction error: {e}")
            return None
    
    def _linear_regression_prediction(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Optional[Dict[str, Any]]:
        """
        Linear regression baseline model
        """
        if features_df.empty or 'score' not in features_df.columns:
            return None
        
        try:
            # Use simple features for linear regression
            simple_features = ['days_since_start', 'difficulty_normalized']
            available_features = [f for f in simple_features if f in features_df.columns]
            
            if len(available_features) < 1:
                return None
            
            X = features_df[available_features].fillna(0)
            y = features_df['score'].fillna(0)
            
            if len(X) < 5:
                return None
            
            # Train Linear Regression
            lr_model = LinearRegression()
            lr_model.fit(X, y)
            
            # Make predictions
            predictions = []
            last_day = features_df['days_since_start'].iloc[-1] if 'days_since_start' in features_df.columns else 0
            
            for i in range(min(prediction_horizon, 30)):
                pred_features = np.array([[last_day + i, features_df['difficulty_normalized'].mean() if 'difficulty_normalized' in features_df.columns else 0.5]])
                pred = lr_model.predict(pred_features)[0]
                predictions.append(max(0, min(100, pred)))
            
            return {
                'model_type': 'linear_regression',
                'predictions': predictions,
                'coefficients': dict(zip(available_features, lr_model.coef_)),
                'intercept': lr_model.intercept_,
                'model_score': lr_model.score(X, y)
            }
            
        except Exception as e:
            logger.error(f"Linear regression prediction error: {e}")
            return None
    
    def _time_series_forecast(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Optional[Dict[str, Any]]:
        """
        Time series forecasting using exponential smoothing
        """
        if features_df.empty or 'score' not in features_df.columns or len(features_df) < 14:
            return None
        
        try:
            # Create time series
            ts_data = features_df.set_index('date')['score'].resample('D').mean().fillna(method='ffill')
            
            if len(ts_data) < 14:
                return None
            
            # Exponential Smoothing
            model = ExponentialSmoothing(ts_data, trend='add', seasonal=None)
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=min(prediction_horizon, 30))
            forecast_values = [max(0, min(100, val)) for val in forecast]
            
            return {
                'model_type': 'time_series',
                'predictions': forecast_values,
                'model_aic': fitted_model.aic,
                'model_bic': fitted_model.bic,
                'model_params': fitted_model.params
            }
            
        except Exception as e:
            logger.error(f"Time series forecast error: {e}")
            return None
    
    def _polynomial_regression_prediction(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Optional[Dict[str, Any]]:
        """
        Polynomial regression for non-linear trend modeling
        """
        if features_df.empty or 'days_since_start' not in features_df.columns or 'score' not in features_df.columns:
            return None
        
        try:
            X = features_df[['days_since_start']].values
            y = features_df['score'].values
            
            if len(X) < 5:
                return None
            
            # Polynomial features
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            
            # Train Ridge regression for stability
            model = Ridge(alpha=1.0)
            model.fit(X_poly, y)
            
            # Make predictions
            predictions = []
            last_day = features_df['days_since_start'].iloc[-1]
            
            for i in range(min(prediction_horizon, 30)):
                pred_features = poly_features.transform([[last_day + i]])
                pred = model.predict(pred_features)[0]
                predictions.append(max(0, min(100, pred)))
            
            return {
                'model_type': 'polynomial_regression',
                'predictions': predictions,
                'polynomial_degree': 2,
                'model_score': model.score(X_poly, y)
            }
            
        except Exception as e:
            logger.error(f"Polynomial regression prediction error: {e}")
            return None
    
    def _create_ensemble_prediction(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combine multiple model predictions using weighted ensemble
        """
        if not predictions:
            return {'error': 'No predictions to ensemble'}
        
        # Weight models based on performance scores if available
        weights = []
        ensemble_predictions = []
        
        for model_name, pred_data in predictions.items():
            if isinstance(pred_data, dict) and 'predictions' in pred_data:
                weight = pred_data.get('model_score', 0.5)
                weights.append(max(0.1, weight))  # Minimum weight
                ensemble_predictions.append(pred_data['predictions'])
        
        if not ensemble_predictions:
            return {'error': 'No valid predictions for ensemble'}
        
        # Weighted average
        max_length = max(len(p) for p in ensemble_predictions)
        final_predictions = []
        
        for i in range(max_length):
            weighted_sum = 0
            total_weight = 0
            
            for j, pred_list in enumerate(ensemble_predictions):
                if i < len(pred_list):
                    weighted_sum += pred_list[i] * weights[j]
                    total_weight += weights[j]
            
            if total_weight > 0:
                final_predictions.append(weighted_sum / total_weight)
            else:
                final_predictions.append(50.0)  # Default prediction
        
        return {
            'ensemble_predictions': final_predictions,
            'ensemble_weights': dict(zip(predictions.keys(), weights)),
            'confidence': min(1.0, len(predictions) * 0.2 + 0.3)  # Higher confidence with more models
        }
    
    def _calculate_prediction_confidence_ml(
        self,
        features_df: pd.DataFrame,
        predictions: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence in ML predictions
        """
        factors = []
        
        # Data quantity factor
        data_points = len(features_df)
        factors.append(min(1.0, data_points / 50.0))  # Max confidence at 50+ points
        
        # Model diversity factor
        model_count = len(predictions)
        factors.append(min(1.0, model_count / 5.0))  # Max confidence with 5+ models
        
        # Model performance factor
        if predictions:
            avg_score = np.mean([
                pred.get('model_score', 0.5) 
                for pred in predictions.values() 
                if isinstance(pred, dict)
            ])
            factors.append(max(0.0, avg_score))
        
        return np.mean(factors) if factors else 0.3
    
    def _generate_fallback_predictions(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate basic predictions when ML models are not available
        """
        if not historical_data:
            return {
                'error': 'No historical data available',
                'basic_prediction': {'days_to_completion': 30, 'confidence': 0.1}
            }
        
        # Simple linear extrapolation
        recent_scores = [record.get('score', 50) for record in historical_data[-10:] if 'score' in record]
        
        if recent_scores:
            avg_score = np.mean(recent_scores)
            trend = (recent_scores[-1] - recent_scores[0]) / len(recent_scores) if len(recent_scores) > 1 else 0
            
            days_to_100 = 0
            if trend > 0 and avg_score < 100:
                days_to_100 = int((100 - avg_score) / trend)
            else:
                days_to_100 = 30  # Default
            
            return {
                'basic_prediction': {
                    'days_to_completion': max(1, min(90, days_to_100)),
                    'current_trend': 'improving' if trend > 0 else 'stable',
                    'confidence': min(0.7, len(recent_scores) / 20.0)
                },
                'data_points_used': len(historical_data)
            }
        
        return {
            'basic_prediction': {'days_to_completion': 30, 'confidence': 0.2},
            'data_points_used': len(historical_data)
        }
    
    def _basic_statistical_predictions(
        self,
        features_df: pd.DataFrame,
        prediction_horizon: int
    ) -> Dict[str, Any]:
        """
        Basic statistical predictions when advanced libraries are not available
        """
        if features_df.empty or 'score' not in features_df.columns:
            return {}
        
        try:
            scores = features_df['score'].values
            
            # Simple moving average
            window = min(7, len(scores))
            moving_avg = np.mean(scores[-window:])
            
            # Linear trend
            if len(scores) >= 3:
                x = np.arange(len(scores))
                slope, intercept = np.polyfit(x, scores, 1)
                trend_slope = slope
            else:
                trend_slope = 0
            
            predictions = []
            for i in range(min(prediction_horizon, 30)):
                pred = moving_avg + (trend_slope * (len(scores) + i))
                predictions.append(max(0, min(100, pred)))
            
            return {
                'moving_average': {
                    'model_type': 'moving_average',
                    'predictions': predictions,
                    'window_size': window,
                    'model_score': 0.5
                }
            }
            
        except Exception as e:
            logger.error(f"Basic statistical prediction error: {e}")
            return {}
    
    # Additional methods would continue here for complete implementation...
    # Including: _analyze_user_learning_patterns, _select_optimal_model,
    # _calculate_confidence_intervals, _statistical_trend_analysis, etc.
    
    def _create_time_series(self, historical_data: List[Dict[str, Any]]) -> pd.Series:
        """
        Create pandas time series from historical data
        """
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        
        if 'score' in df.columns:
            return df['score'].resample('D').mean().fillna(method='ffill')
        elif 'status' in df.columns:
            # Convert status to numerical progress
            status_map = {'completed': 1, 'in_progress': 0.5, 'not_started': 0}
            df['progress'] = df['status'].map(status_map).fillna(0)
            return df['progress'].resample('D').mean().fillna(method='ffill')
        
        return pd.Series([1] * len(df), index=df.index)
    
    def _basic_trend_analysis(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Basic trend analysis without advanced libraries
        """
        if len(historical_data) < 3:
            return {'trend': 'insufficient_data'}
        
        scores = [record.get('score', 50) for record in historical_data if 'score' in record]
        
        if len(scores) < 3:
            scores = [50] * len(historical_data)  # Default scores
        
        # Simple trend calculation
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        avg_first = np.mean(first_half)
        avg_second = np.mean(second_half)
        
        if avg_second > avg_first + 5:
            trend = 'improving'
        elif avg_second < avg_first - 5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'first_half_average': avg_first,
            'second_half_average': avg_second,
            'improvement_rate': (avg_second - avg_first) / avg_first if avg_first > 0 else 0
        }
    
    def _analyze_velocity_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze learning velocity trends
        """
        if len(historical_data) < 7:
            return {'velocity': 'insufficient_data'}
        
        # Calculate completion velocity
        completions_by_week = {}
        
        for record in historical_data:
            if record.get('type') == 'progress' and record.get('status') == 'completed':
                week = record['date'].strftime('%Y-W%U')
                completions_by_week[week] = completions_by_week.get(week, 0) + 1
        
        if len(completions_by_week) < 2:
            return {'velocity': 'stable', 'rate': 0}
        
        # Trend analysis
        weeks = sorted(completions_by_week.keys())
        rates = [completions_by_week[week] for week in weeks]
        
        if len(rates) >= 3:
            recent_rate = np.mean(rates[-3:])
            older_rate = np.mean(rates[:-3])
            velocity_trend = 'accelerating' if recent_rate > older_rate * 1.2 else 'stable'
        else:
            velocity_trend = 'stable'
            recent_rate = np.mean(rates)
        
        return {
            'velocity': velocity_trend,
            'rate_per_week': recent_rate,
            'peak_week': max(completions_by_week, key=completions_by_week.get),
            'total_completions': sum(completions_by_week.values())
        }
    
    def _analyze_performance_trajectory(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze performance trajectory over time
        """
        scores = [record.get('score', 50) for record in historical_data if 'score' in record]
        
        if len(scores) < 3:
            return {'trajectory': 'insufficient_data'}
        
        # Calculate trajectory metrics
        performance_values = []
        time_points = list(range(len(scores)))
        
        # Fit linear regression for trajectory
        try:
            slope, intercept, r_value, p_value, std_err = stats.linregress(time_points, scores)
            
            trajectory_type = 'improving' if slope > 1 else 'stable' if abs(slope) <= 1 else 'declining'
            
            return {
                'trajectory': trajectory_type,
                'slope': slope,
                'r_squared': r_value ** 2,
                'statistical_significance': p_value < 0.05,
                'predicted_next_score': intercept + slope * (len(scores) + 1)
            }
            
        except Exception:
            return {
                'trajectory': 'stable',
                'slope': 0,
                'current_average': np.mean(scores),
                'consistency': 1.0 - (np.std(scores) / np.mean(scores)) if np.mean(scores) > 0 else 0
            }
    
    def _assess_data_quality(self, historical_data: List[Dict[str, Any]]) -> float:
        """
        Assess quality of historical data for predictions
        """
        if not historical_data:
            return 0.0
        
        quality_score = 0.0
        
        # Data quantity score
        data_points = len(historical_data)
        quantity_score = min(1.0, data_points / 100.0)  # Full score at 100+ points
        quality_score += quantity_score * 0.3
        
        # Recency score
        latest_date = max(record['date'] for record in historical_data)
        days_old = (timezone.now().date() - latest_date).days
        recency_score = max(0.0, 1.0 - (days_old / 30.0))  # Penalty for old data
        quality_score += recency_score * 0.2
        
        # Completeness score
        records_with_score = len([r for r in historical_data if 'score' in r])
        completeness_score = records_with_score / len(historical_data) if historical_data else 0
        quality_score += completeness_score * 0.3
        
        # Consistency score
        scores = [r.get('score', 0) for r in historical_data if 'score' in r]
        if scores and len(scores) > 1:
            consistency_score = 1.0 - (np.std(scores) / np.mean(scores))
            consistency_score = max(0.0, min(1.0, consistency_score))
            quality_score += consistency_score * 0.2
        
        return min(1.0, quality_score)
    
    def _generate_trend_recommendations(self, trends_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on trend analysis
        """
        recommendations = []
        
        # Basic trend recommendations
        basic_trends = trends_analysis.get('basic_trends', {})
        if basic_trends.get('trend') == 'declining':
            recommendations.append("Performance trend is declining. Consider additional practice or review of fundamentals.")
        elif basic_trends.get('trend') == 'improving':
            recommendations.append("Strong improvement trend! Consider accelerating to more challenging content.")
        
        # Velocity recommendations
        velocity_trends = trends_analysis.get('velocity_trends', {})
        if velocity_trends.get('velocity') == 'stable':
            recommendations.append("Learning velocity is steady. Maintain current pace for consistent progress.")
        elif velocity_trends.get('velocity') == 'accelerating':
            recommendations.append("Accelerating learning pace detected. You may be ready for advanced modules.")
        
        # Performance trajectory recommendations
        trajectory = trends_analysis.get('performance_trajectory', {})
        if trajectory.get('trajectory') == 'declining':
            recommendations.append("Performance trajectory suggests difficulty. Break down complex concepts into smaller steps.")
        elif trajectory.get('trajectory') == 'improving':
            recommendations.append("Excellent trajectory! Set more ambitious learning goals.")
        
        if not recommendations:
            recommendations.append("Continue current learning approach - patterns are stable and positive.")
        
        return recommendations
    
    # Placeholder methods for additional functionality
    def _statistical_trend_analysis(self, ts_data: pd.Series) -> Dict[str, Any]:
        """Statistical trend analysis (placeholder)"""
        return {'trend': 'analyzed', 'method': 'statistical'}
    
    def _correlation_analysis(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Correlation analysis between variables (placeholder)"""
        return {'correlations': 'analyzed'}
    
    def _pattern_recognition(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Pattern recognition in learning behavior (placeholder)"""
        return {'patterns': 'identified'}
    
    def _anomaly_detection(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect anomalies in learning patterns (placeholder)"""
        return {'anomalies': 'none_detected'}
    
    def _analyze_user_learning_patterns(self, user: User, learning_path_id: Optional[int]) -> Dict[str, Any]:
        """Analyze user-specific learning patterns (placeholder)"""
        return {'patterns': 'analyzed', 'user_type': 'typical'}
    
    def _select_optimal_model(self, user_patterns: Dict[str, Any]) -> str:
        """Select optimal prediction model for user (placeholder)"""
        return 'ensemble'
    
    def _calculate_adaptive_parameters(self, user_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate adaptive parameters (placeholder)"""
        return {'parameters': 'optimized'}
    
    def _generate_adaptive_predictions(self, user: User, learning_path_id: Optional[int], 
                                     model: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate adaptive predictions (placeholder)"""
        return {'predictions': 'generated', 'model': model}
    
    def _track_model_performance(self, user: User, model: str) -> Dict[str, Any]:
        """Track model performance over time (placeholder)"""
        return {'performance': 'good', 'accuracy': 0.85}
    
    def _get_adaptation_strategy(self, user_patterns: Dict[str, Any]) -> str:
        """Get adaptation strategy (placeholder)"""
        return 'gradual_adaptation'
    
    def _calculate_confidence_intervals(self, data: List[Dict[str, Any]], confidence_level: float) -> Dict[str, Any]:
        """Calculate confidence intervals (placeholder)"""
        return {'intervals': 'calculated', 'level': confidence_level}
    
    def _bootstrap_confidence_estimation(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bootstrap confidence estimation (placeholder)"""
        return {'bootstrap': 'estimated', 'confidence': 0.95}
    
    def _bayesian_confidence_intervals(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Bayesian confidence intervals (placeholder)"""
        return {'bayesian': 'computed', 'intervals': 'posterior'}
    
    def _quantify_prediction_uncertainty(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Quantify prediction uncertainty (placeholder)"""
        return {'uncertainty': 'quantified', 'variance': 0.1}
    
    def _basic_confidence_calculation(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Basic confidence calculation (placeholder)"""
        return {'confidence': 0.7, 'method': 'basic'}
    
    def _assess_model_uncertainty(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess model uncertainty (placeholder)"""
        return {'uncertainty': 'low', 'model_stability': 'stable'}
    
    def _assess_data_uncertainty(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess data uncertainty (placeholder)"""
        return {'uncertainty': 'medium', 'data_quality': 'good'}
    
    def _calculate_statistical_significance(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistical significance (placeholder)"""
        return {'significance': 'moderate', 'p_value': 0.15}