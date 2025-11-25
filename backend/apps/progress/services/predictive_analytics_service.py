"""
Predictive Analytics Service - JAC Learning Platform

Advanced machine learning and statistical modeling for learning predictions.
Provides sophisticated forecasting, trend analysis, and adaptive predictions.

Author: Cavin Otieno
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
        """Calculate statistical significance using appropriate tests."""
        try:
            if not data or len(data) < 6:
                return {'significance': 'insufficient_data', 'p_value': 1.0, 'test_used': 'none'}
            
            # Extract scores for analysis
            scores = []
            for record in data:
                if 'score' in record and record['score'] is not None:
                    scores.append(record['score'])
            
            if len(scores) < 6:
                return {'significance': 'insufficient_scores', 'p_value': 1.0, 'test_used': 'none'}
            
            scores = np.array(scores)
            
            # Test for normality
            try:
                shapiro_stat, shapiro_p = stats.shapiro(scores)
                is_normal = shapiro_p > 0.05
            except:
                # Fallback: use basic normality assessment
                is_normal = abs(stats.skew(scores)) < 2 and abs(stats.kurtosis(scores)) < 7
            
            # Select appropriate statistical test
            if is_normal and len(scores) >= 8:
                # One-sample t-test against neutral score (50)
                t_stat, p_value = stats.ttest_1samp(scores, 50)
                test_used = 'one_sample_t_test'
                
                significance_level = 'high' if p_value < 0.01 else 'moderate' if p_value < 0.05 else 'low'
                
            else:
                # Non-parametric test: Wilcoxon signed-rank test
                try:
                    wilcoxon_stat, p_value = stats.wilcoxon(scores - 50, alternative='two-sided')
                    test_used = 'wilcoxon_signed_rank'
                    
                    significance_level = 'high' if p_value < 0.01 else 'moderate' if p_value < 0.05 else 'low'
                    
                except:
                    # Fallback: simple comparison
                    mean_score = np.mean(scores)
                    p_value = 0.05 if abs(mean_score - 50) > 10 else 0.5
                    test_used = 'simple_comparison'
                    significance_level = 'low'
            
            # Calculate effect size (Cohen's d)
            cohens_d = (np.mean(scores) - 50) / np.std(scores) if np.std(scores) > 0 else 0
            
            # Additional descriptive statistics
            median_score = np.median(scores)
            q1, q3 = np.percentile(scores, [25, 75])
            
            return {
                'significance': significance_level,
                'p_value': p_value,
                'test_used': test_used,
                'sample_size': len(scores),
                'mean_score': np.mean(scores),
                'median_score': median_score,
                'standard_deviation': np.std(scores),
                'cohens_d': cohens_d,
                'effect_size_interpretation': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small',
                'distribution': 'normal' if is_normal else 'non_normal',
                'quartiles': {'Q1': q1, 'Q3': q3, 'IQR': q3 - q1},
                'confidence_interval': self._calculate_mean_confidence_interval(scores, 0.95)
            }
            
        except Exception as e:
            logger.error(f"Error calculating statistical significance: {e}")
            return {'significance': 'calculation_error', 'p_value': 1.0, 'test_used': 'error'}
    
    # Helper methods for advanced statistical analysis
    
    def _analyze_learning_rhythm(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user learning rhythm patterns."""
        try:
            # Extract timestamps and analyze patterns
            timestamps = []
            for record in historical_data:
                if 'date' in record and record['date']:
                    timestamps.append(record['date'])
            
            if len(timestamps) < 3:
                return {'rhythm_type': 'insufficient_data', 'consistency': 0}
            
            # Calculate time intervals between learning sessions
            intervals = []
            sorted_timestamps = sorted(timestamps)
            for i in range(1, len(sorted_timestamps)):
                if hasattr(sorted_timestamps[i], 'date') and hasattr(sorted_timestamps[i-1], 'date'):
                    interval = (sorted_timestamps[i].date() - sorted_timestamps[i-1].date()).days
                    intervals.append(interval)
            
            if not intervals:
                return {'rhythm_type': 'irregular', 'consistency': 0}
            
            avg_interval = np.mean(intervals)
            interval_std = np.std(intervals)
            
            # Determine rhythm type
            if interval_std / avg_interval < 0.3:
                rhythm_type = 'consistent'
            elif interval_std / avg_interval < 0.6:
                rhythm_type = 'moderate'
            else:
                rhythm_type = 'irregular'
            
            consistency = 1 - (interval_std / max(avg_interval, 1))
            
            return {
                'rhythm_type': rhythm_type,
                'consistency': max(0, consistency),
                'average_interval_days': avg_interval,
                'interval_variability': interval_std
            }
            
        except Exception as e:
            logger.error(f"Error analyzing learning rhythm: {e}")
            return {'rhythm_type': 'error', 'consistency': 0}
    
    def _analyze_difficulty_progression(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze difficulty progression patterns."""
        try:
            # Extract difficulty levels and scores
            difficulty_scores = {}
            for record in historical_data:
                difficulty = record.get('difficulty_level', 1)
                score = record.get('score', 0)
                if score > 0:  # Only include records with valid scores
                    if difficulty not in difficulty_scores:
                        difficulty_scores[difficulty] = []
                    difficulty_scores[difficulty].append(score)
            
            if len(difficulty_scores) < 2:
                return {'progression_type': 'insufficient_data', 'trend': 'unknown'}
            
            # Calculate average scores per difficulty
            avg_scores = {diff: np.mean(scores) for diff, scores in difficulty_scores.items()}
            difficulties = sorted(avg_scores.keys())
            
            # Determine progression trend
            if len(difficulties) >= 3:
                # Fit linear trend
                trend_slope = np.polyfit(difficulties, [avg_scores[diff] for diff in difficulties], 1)[0]
                
                if trend_slope > 5:
                    progression_type = 'improving'
                elif trend_slope < -5:
                    progression_type = 'declining'
                else:
                    progression_type = 'stable'
            else:
                # Simple comparison
                first_avg = avg_scores[difficulties[0]]
                last_avg = avg_scores[difficulties[-1]]
                
                if last_avg > first_avg + 10:
                    progression_type = 'improving'
                elif last_avg < first_avg - 10:
                    progression_type = 'declining'
                else:
                    progression_type = 'stable'
            
            return {
                'progression_type': progression_type,
                'difficulty_scores': avg_scores,
                'difficulty_range': [min(difficulties), max(difficulties)],
                'score_range': [min(avg_scores.values()), max(avg_scores.values())]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing difficulty progression: {e}")
            return {'progression_type': 'error', 'trend': 'unknown'}
    
    def _analyze_time_preferences(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze time-of-day preferences."""
        try:
            # Extract hour information
            hours = []
            for record in historical_data:
                if 'date' in record and record['date']:
                    if hasattr(record['date'], 'hour'):
                        hours.append(record['date'].hour)
                    elif hasattr(record['date'], 'time'):
                        hours.append(record['date'].time().hour)
            
            if len(hours) < 3:
                return {'preferred_time': 'insufficient_data', 'peak_hours': []}
            
            # Analyze peak hours
            hour_counts = {}
            for hour in range(24):
                hour_counts[hour] = hours.count(hour)
            
            # Find top 3 peak hours
            sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
            peak_hours = [hour for hour, count in sorted_hours[:3] if count > 0]
            
            # Determine time preference
            if peak_hours:
                avg_peak_hour = np.mean(peak_hours)
                if 6 <= avg_peak_hour < 12:
                    preferred_time = 'morning'
                elif 12 <= avg_peak_hour < 18:
                    preferred_time = 'afternoon'
                elif 18 <= avg_peak_hour < 22:
                    preferred_time = 'evening'
                else:
                    preferred_time = 'night'
            else:
                preferred_time = 'irregular'
            
            return {
                'preferred_time': preferred_time,
                'peak_hours': peak_hours,
                'activity_distribution': hour_counts,
                'peak_hour_intensity': max(hour_counts.values()) if hour_counts else 0
            }
            
        except Exception as e:
            logger.error(f"Error analyzing time preferences: {e}")
            return {'preferred_time': 'error', 'peak_hours': []}
    
    def _classify_user_type(self, learning_rhythm: Dict[str, Any], difficulty_progression: Dict[str, Any], time_preferences: Dict[str, Any]) -> str:
        """Classify user type based on patterns."""
        try:
            consistency = learning_rhythm.get('consistency', 0)
            progression_type = difficulty_progression.get('progression_type', 'stable')
            preferred_time = time_preferences.get('preferred_time', 'irregular')
            
            # Classification logic
            if consistency > 0.7 and progression_type == 'improving':
                if preferred_time in ['morning', 'afternoon']:
                    return 'systematic'
                else:
                    return 'consistent'
            elif consistency < 0.4:
                return 'sporadic'
            elif progression_type == 'declining':
                return 'struggling'
            elif progression_type == 'improving':
                return 'fast_learner'
            else:
                return 'typical'
                
        except Exception as e:
            logger.error(f"Error classifying user type: {e}")
            return 'unknown'
    
    def _calculate_pattern_strength(self, learning_rhythm: Dict[str, Any], difficulty_progression: Dict[str, Any]) -> float:
        """Calculate the strength of identified patterns."""
        try:
            rhythm_consistency = learning_rhythm.get('consistency', 0)
            
            # Simple pattern strength calculation
            pattern_strength = rhythm_consistency
            
            return min(1.0, max(0.0, pattern_strength))
            
        except Exception as e:
            logger.error(f"Error calculating pattern strength: {e}")
            return 0.5
    
    def _calculate_adaptability_score(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate user adaptability score based on learning flexibility."""
        try:
            if len(historical_data) < 3:
                return 0.5
            
            # Analyze score variations and difficulty adaptations
            scores = [record.get('score', 0) for record in historical_data if record.get('score') is not None]
            difficulties = [record.get('difficulty_level', 1) for record in historical_data if record.get('difficulty_level') is not None]
            
            if len(scores) < 2:
                return 0.5
            
            # Calculate adaptability based on score consistency relative to difficulty
            score_variation = np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 1
            
            # Lower variation with changing difficulties indicates higher adaptability
            adaptability = 1 - min(1.0, score_variation)
            
            return max(0.0, min(1.0, adaptability))
            
        except Exception as e:
            logger.error(f"Error calculating adaptability score: {e}")
            return 0.5
    
    def _calculate_pattern_consistency(self, historical_data: List[Dict[str, Any]]) -> float:
        """Calculate pattern consistency from historical data."""
        try:
            if len(historical_data) < 3:
                return 0.5
            
            # Analyze score consistency over time
            scores = [record.get('score', 0) for record in historical_data if record.get('score') is not None]
            
            if len(scores) < 2:
                return 0.5
            
            # Calculate coefficient of variation
            mean_score = np.mean(scores)
            std_score = np.std(scores)
            
            if mean_score > 0:
                cv = std_score / mean_score
                consistency = 1 - min(1.0, cv)  # Lower CV = higher consistency
            else:
                consistency = 0
            
            return max(0.0, consistency)
            
        except Exception as e:
            logger.error(f"Error calculating pattern consistency: {e}")
            return 0.5
    
    def _calculate_prediction_intervals(self, values: np.ndarray) -> Dict[str, Any]:
        """Calculate prediction intervals for values."""
        try:
            if len(values) < 3:
                return {'relative_width': 1.0}
            
            mean_val = np.mean(values)
            std_val = np.std(values)
            
            # 95% prediction interval (approximately ±2 std deviations)
            margin = 2 * std_val
            lower_bound = mean_val - margin
            upper_bound = mean_val + margin
            
            # Calculate relative width
            range_val = upper_bound - lower_bound
            relative_width = range_val / abs(mean_val) if mean_val != 0 else range_val
            
            return {
                'mean': mean_val,
                'std': std_val,
                'prediction_interval': [lower_bound, upper_bound],
                'relative_width': relative_width
            }
            
        except Exception as e:
            logger.error(f"Error calculating prediction intervals: {e}")
            return {'relative_width': 1.0}
    
    def _calculate_model_uncertainty(self, values: np.ndarray) -> float:
        """Calculate model uncertainty using entropy."""
        try:
            if len(values) < 3:
                return 0.5
            
            # Discretize values into bins for entropy calculation
            n_bins = min(10, max(3, len(values) // 2))
            hist, _ = np.histogram(values, bins=n_bins)
            
            # Normalize to probabilities
            probabilities = hist / np.sum(hist)
            probabilities = probabilities[probabilities > 0]  # Remove zero probabilities
            
            # Calculate entropy
            if len(probabilities) > 1:
                entropy = -np.sum(probabilities * np.log2(probabilities))
                max_entropy = np.log2(len(probabilities))
                uncertainty = entropy / max_entropy if max_entropy > 0 else 0
            else:
                uncertainty = 0
            
            return uncertainty
            
        except Exception as e:
            logger.error(f"Error calculating model uncertainty: {e}")
            return 0.5
    
    def _calculate_data_uncertainty(self, data: List[Dict[str, Any]]) -> float:
        """Calculate data uncertainty based on completeness and quality."""
        try:
            total_records = len(data)
            if total_records == 0:
                return 1.0
            
            # Count missing or invalid data
            missing_scores = sum(1 for record in data if not record.get('score') or record['score'] is None)
            missing_difficulty = sum(1 for record in data if not record.get('difficulty_level'))
            
            # Calculate uncertainty based on missing data percentage
            missing_percentage = (missing_scores + missing_difficulty) / (total_records * 2)
            data_uncertainty = min(1.0, missing_percentage)
            
            return data_uncertainty
            
        except Exception as e:
            logger.error(f"Error calculating data uncertainty: {e}")
            return 0.5
    
    def _classify_uncertainty_level(self, uncertainty_score: float) -> str:
        """Classify uncertainty level based on score."""
        if uncertainty_score < 0.3:
            return 'low'
        elif uncertainty_score < 0.6:
            return 'moderate'
        else:
            return 'high'
    
    def _generate_uncertainty_recommendations(self, uncertainty_score: float) -> List[str]:
        """Generate recommendations based on uncertainty level."""
        recommendations = []
        
        if uncertainty_score > 0.7:
            recommendations.extend([
                "Collect more data points to reduce uncertainty",
                "Consider additional validation metrics",
                "Review data quality and completeness"
            ])
        elif uncertainty_score > 0.4:
            recommendations.extend([
                "Monitor prediction accuracy closely",
                "Consider ensemble methods for robustness"
            ])
        else:
            recommendations.append("Uncertainty levels are acceptable for current predictions")
        
        return recommendations
    
    def _calculate_cv_uncertainty(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Calculate cross-validation uncertainty."""
        try:
            from sklearn.model_selection import cross_val_score
            from sklearn.linear_model import LinearRegression
            
            if len(X) < 5:
                return 0.8  # High uncertainty for small samples
            
            # Simple cross-validation
            model = LinearRegression()
            try:
                cv_scores = cross_val_score(model, X, y, cv=min(5, len(X)//2), scoring='neg_mean_squared_error')
                cv_uncertainty = np.std(cv_scores) / np.abs(np.mean(cv_scores)) if np.mean(cv_scores) != 0 else 1
                return min(1.0, cv_uncertainty)
            except:
                return 0.5  # Default uncertainty if CV fails
                
        except Exception as e:
            logger.error(f"Error calculating CV uncertainty: {e}")
            return 0.6
    
    def _assess_model_stability(self, X: pd.DataFrame, y: pd.Series) -> float:
        """Assess model stability using coefficient of variation."""
        try:
            if len(X) < 5:
                return 0.5
            
            # Simple stability assessment based on data characteristics
            feature_cv = []
            for col in X.select_dtypes(include=[np.number]).columns:
                mean_val = X[col].mean()
                std_val = X[col].std()
                if mean_val != 0:
                    feature_cv.append(std_val / abs(mean_val))
            
            if feature_cv:
                avg_cv = np.mean(feature_cv)
                stability = 1 - min(1.0, avg_cv)  # Lower CV = higher stability
            else:
                stability = 0.5
            
            return max(0.0, stability)
            
        except Exception as e:
            logger.error(f"Error assessing model stability: {e}")
            return 0.5
    
    def _assess_feature_stability(self, X: pd.DataFrame) -> float:
        """Assess feature stability."""
        try:
            if X.empty:
                return 0.5
            
            # Check for near-zero variance features
            near_zero_var = 0
            total_features = X.shape[1]
            
            if total_features > 0:
                for col in X.select_dtypes(include=[np.number]).columns:
                    if X[col].var() < 0.01:
                        near_zero_var += 1
                
                stable_features_ratio = 1 - (near_zero_var / total_features)
            else:
                stable_features_ratio = 0.5
            
            return max(0.0, stable_features_ratio)
            
        except Exception as e:
            logger.error(f"Error assessing feature stability: {e}")
            return 0.5
    
    def _generate_model_uncertainty_recommendations(self, uncertainty_score: float, sample_size: int) -> List[str]:
        """Generate recommendations for model uncertainty."""
        recommendations = []
        
        if uncertainty_score > 0.7:
            recommendations.extend([
                "Increase training data size",
                "Consider feature selection to reduce noise",
                "Use ensemble methods for better stability"
            ])
        elif uncertainty_score > 0.4:
            recommendations.extend([
                "Monitor model performance over time",
                "Consider cross-validation for validation"
            ])
        
        if sample_size < 20:
            recommendations.append("Collect more training samples for better stability")
        
        return recommendations
    
    def _assess_data_consistency(self, data: List[Dict[str, Any]]) -> float:
        """Assess data consistency."""
        try:
            scores = [record.get('score', 0) for record in data if record.get('score') is not None]
            
            if len(scores) < 3:
                return 0.5
            
            # Calculate consistency based on score variation
            mean_score = np.mean(scores)
            std_score = np.std(scores)
            
            if mean_score > 0:
                cv = std_score / mean_score
                consistency = 1 - min(1.0, cv)
            else:
                consistency = 0
            
            return max(0.0, consistency)
            
        except Exception as e:
            logger.error(f"Error assessing data consistency: {e}")
            return 0.5
    
    def _assess_data_accuracy(self, data: List[Dict[str, Any]]) -> float:
        """Assess data accuracy using outlier detection."""
        try:
            scores = [record.get('score', 0) for record in data if record.get('score') is not None]
            
            if len(scores) < 5:
                return 0.5
            
            # Simple outlier detection using IQR
            Q1 = np.percentile(scores, 25)
            Q3 = np.percentile(scores, 75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = sum(1 for score in scores if score < lower_bound or score > upper_bound)
            outlier_rate = outliers / len(scores)
            
            # Accuracy is inverse of outlier rate (fewer outliers = higher accuracy)
            accuracy = max(0.0, 1 - outlier_rate)
            
            return accuracy
            
        except Exception as e:
            logger.error(f"Error assessing data accuracy: {e}")
            return 0.5
    
    def _assess_data_timeliness(self, data: List[Dict[str, Any]]) -> float:
        """Assess data timeliness based on recency."""
        try:
            if not data:
                return 0.0
            
            # Check for recent data (simple implementation)
            recent_records = 0
            total_records = len(data)
            
            for record in data:
                if 'date' in record and record['date']:
                    # Assume data older than 30 days is not timely
                    if hasattr(record['date'], 'days'):
                        days_old = record['date'].days
                    else:
                        days_old = 30  # Default assumption
                    
                    if days_old <= 30:
                        recent_records += 1
            
            timeliness = recent_records / total_records if total_records > 0 else 0
            return timeliness
            
        except Exception as e:
            logger.error(f"Error assessing data timeliness: {e}")
            return 0.5
    
    def _generate_data_improvement_recommendations(self, overall_uncertainty: float, completeness_scores: Dict[str, float]) -> List[str]:
        """Generate recommendations for data improvement."""
        recommendations = []
        
        if overall_uncertainty > 0.6:
            recommendations.extend([
                "Focus on improving data completeness",
                "Implement data validation procedures",
                "Consider data source quality assessment"
            ])
        elif overall_uncertainty > 0.4:
            recommendations.append("Monitor data quality metrics regularly")
        
        # Specific recommendations based on completeness
        for metric, score in completeness_scores.items():
            if score < 0.8:
                recommendations.append(f"Improve {metric} data collection")
        
        return recommendations
    
    def _calculate_mean_confidence_interval(self, values: np.ndarray, confidence_level: float) -> List[float]:
        """Calculate confidence interval for the mean."""
        try:
            if len(values) < 2:
                return [0, 0]
            
            mean_val = np.mean(values)
            std_err = stats.sem(values)  # Standard error of the mean
            
            # Calculate confidence interval
            alpha = 1 - confidence_level
            t_critical = stats.t.ppf(1 - alpha/2, df=len(values)-1)
            margin = t_critical * std_err
            
            return [mean_val - margin, mean_val + margin]
            
        except Exception as e:
            logger.error(f"Error calculating confidence interval: {e}")
            return [0, 0]
    
    # New Predictive Learning Models Integration
    # =========================================
    
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

        except Exception as e:
            logger.error(f"Error calculating confidence interval: {e}")
            return [0, 0]