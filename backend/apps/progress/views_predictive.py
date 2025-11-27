# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

import uuid
import asyncio
"""
Predictive Analytics API Views - JAC Learning Platform

API endpoints for advanced machine learning and predictive analytics.

Author: Cavin Otieno
Created: 2025-11-26
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Avg, Count, Q, Sum, Max, Min
from django.conf import settings
from datetime import datetime, timedelta
import logging

from ..services.predictive_analytics_service import PredictiveAnalyticsService
from .serializers import PredictiveAnalyticsSerializer

logger = logging.getLogger(__name__)


class MLPredictionsAPIView(APIView):
    """
    API View for machine learning predictions
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get ML-based predictions for user learning progress
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            prediction_horizon = int(request.query_params.get('prediction_horizon_days', 30))
            
            # Validate prediction horizon
            if prediction_horizon > 90:
                return Response({
                    'error': 'Prediction horizon cannot exceed 90 days'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            predictive_service = PredictiveAnalyticsService()
            ml_predictions = predictive_service.generate_ml_predictions(
                user=request.user,
                learning_path_id=learning_path_id,
                prediction_horizon_days=prediction_horizon
            )
            
            return Response({
                'success': True,
                'data': ml_predictions,
                'timestamp': timezone.now(),
                'user_id': request.user.id
            })
            
        except Exception as e:
            logger.error(f"ML Predictions API error: {e}")
            return Response({
                'error': f'Failed to generate ML predictions: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoricalTrendsAPIView(APIView):
    """
    API View for comprehensive historical trend analysis
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get advanced historical trend analysis
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            analysis_period = int(request.query_params.get('analysis_period_days', 90))
            
            # Validate analysis period
            if analysis_period > 365:
                return Response({
                    'error': 'Analysis period cannot exceed 365 days'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            predictive_service = PredictiveAnalyticsService()
            trends_analysis = predictive_service.analyze_historical_trends(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_period_days=analysis_period
            )
            
            return Response({
                'success': True,
                'data': trends_analysis,
                'timestamp': timezone.now(),
                'user_id': request.user.id
            })
            
        except Exception as e:
            logger.error(f"Historical Trends API error: {e}")
            return Response({
                'error': f'Failed to analyze trends: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdaptivePredictionsAPIView(APIView):
    """
    API View for adaptive prediction algorithms
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get adaptive predictions based on user learning patterns
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            
            predictive_service = PredictiveAnalyticsService()
            adaptive_predictions = predictive_service.adaptive_prediction_algorithm(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            return Response({
                'success': True,
                'data': adaptive_predictions,
                'timestamp': timezone.now(),
                'user_id': request.user.id
            })
            
        except Exception as e:
            logger.error(f"Adaptive Predictions API error: {e}")
            return Response({
                'error': f'Failed to generate adaptive predictions: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfidenceCalculationsAPIView(APIView):
    """
    API View for statistical confidence calculations
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get advanced statistical confidence calculations
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            confidence_level = float(request.query_params.get('confidence_level', 0.95))
            
            # Validate confidence level
            if not (0.5 <= confidence_level <= 0.99):
                return Response({
                    'error': 'Confidence level must be between 0.5 and 0.99'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            predictive_service = PredictiveAnalyticsService()
            confidence_analysis = predictive_service.statistical_confidence_calculations(
                user=request.user,
                learning_path_id=learning_path_id,
                confidence_level=confidence_level
            )
            
            return Response({
                'success': True,
                'data': confidence_analysis,
                'timestamp': timezone.now(),
                'user_id': request.user.id
            })
            
        except Exception as e:
            logger.error(f"Confidence Calculations API error: {e}")
            return Response({
                'error': f'Failed to calculate confidence: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ComprehensivePredictiveAnalyticsAPIView(APIView):
    """
    Comprehensive predictive analytics API combining all services
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get comprehensive predictive analytics report
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            prediction_horizon = int(request.query_params.get('prediction_horizon_days', 30))
            analysis_period = int(request.query_params.get('analysis_period_days', 90))
            confidence_level = float(request.query_params.get('confidence_level', 0.95))
            
            predictive_service = PredictiveAnalyticsService()
            
            # Generate all analytics components
            results = {}
            
            # ML Predictions
            results['ml_predictions'] = predictive_service.generate_ml_predictions(
                user=request.user,
                learning_path_id=learning_path_id,
                prediction_horizon_days=prediction_horizon
            )
            
            # Historical Trends
            results['historical_trends'] = predictive_service.analyze_historical_trends(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_period_days=analysis_period
            )
            
            # Adaptive Predictions
            results['adaptive_predictions'] = predictive_service.adaptive_prediction_algorithm(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            # Confidence Calculations
            results['confidence_analysis'] = predictive_service.statistical_confidence_calculations(
                user=request.user,
                learning_path_id=learning_path_id,
                confidence_level=confidence_level
            )
            
            # Learning Velocity Analysis (NEW)
            results['learning_velocity'] = predictive_service.analyze_learning_velocity(
                user=request.user,
                learning_path_id=learning_path_id,
                days_window=min(analysis_period, 30)
            )
            
            # Engagement Pattern Analysis (NEW)
            results['engagement_patterns'] = predictive_service.analyze_engagement_patterns(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_depth='comprehensive'
            )
            
            # Success Probability Modeling (NEW)
            results['success_probability'] = predictive_service.model_success_probability(
                user=request.user,
                learning_path_id=learning_path_id,
                time_horizon_days=prediction_horizon
            )
            
            # Time-to-Completion Prediction (NEW)
            results['time_to_completion'] = predictive_service.predict_time_to_completion(
                user=request.user,
                learning_path_id=learning_path_id,
                include_holidays=True
            )
            
            # Retention Risk Assessment (NEW)
            results['retention_risk'] = predictive_service.assess_retention_risk(
                user=request.user,
                learning_path_id=learning_path_id,
                risk_horizon_days=prediction_horizon
            )
            
            # Knowledge Gap Detection (NEW)
            results['knowledge_gaps'] = predictive_service.detect_knowledge_gaps(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_depth='comprehensive'
            )
            
            # K-Means Clustering Analysis (NEW)
            results['learning_clusters'] = predictive_service.perform_learning_analytics_clustering(
                learning_path_id=learning_path_id,
                feature_selection='comprehensive'
            )
            
            # Generate summary insights
            results['summary_insights'] = self._generate_summary_insights(results)
            
            return Response({
                'success': True,
                'data': results,
                'metadata': {
                    'prediction_horizon_days': prediction_horizon,
                    'analysis_period_days': analysis_period,
                    'confidence_level': confidence_level,
                    'generated_at': timezone.now(),
                    'user_id': request.user.id
                }
            })
            
        except Exception as e:
            logger.error(f"Comprehensive Predictive Analytics API error: {e}")
            return Response({
                'error': f'Failed to generate comprehensive analytics: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_summary_insights(self, results: dict) -> dict:
        """
        Generate summary insights from all analytics components
        """
        insights = {
            'overall_prediction_confidence': 'low',
            'learning_trajectory': 'stable',
            'recommendation_priority': 'medium',
            'key_insights': [],
            'action_items': []
        }
        
        # Analyze ML predictions confidence
        ml_predictions = results.get('ml_predictions', {})
        if 'prediction_confidence' in ml_predictions:
            confidence = ml_predictions['prediction_confidence']
            if confidence > 0.8:
                insights['overall_prediction_confidence'] = 'high'
            elif confidence > 0.5:
                insights['overall_prediction_confidence'] = 'medium'
        
        # Analyze historical trends trajectory
        trends = results.get('historical_trends', {})
        trends_analysis = trends.get('trends_analysis', {})
        basic_trends = trends_analysis.get('basic_trends', {})
        trajectory = trends_analysis.get('performance_trajectory', {})
        
        if trajectory.get('trajectory') == 'improving':
            insights['learning_trajectory'] = 'improving'
            insights['key_insights'].append("Strong upward learning trajectory detected")
        elif trajectory.get('trajectory') == 'declining':
            insights['learning_trajectory'] = 'declining'
            insights['key_insights'].append("Learning trajectory requires attention")
        
        # Generate action items based on analysis
        if insights['learning_trajectory'] == 'improving':
            insights['action_items'].append("Consider advancing to more challenging content")
            insights['recommendation_priority'] = 'high'
        elif insights['learning_trajectory'] == 'declining':
            insights['action_items'].append("Review fundamental concepts and practice more")
            insights['recommendation_priority'] = 'urgent'
        else:
            insights['action_items'].append("Maintain current learning pace and consistency")
        
        # Add confidence-based insights
        if insights['overall_prediction_confidence'] == 'high':
            insights['key_insights'].append("High confidence in predictions based on substantial data")
        elif insights['overall_prediction_confidence'] == 'low':
            insights['key_insights'].append("Collect more learning data for better predictions")
            insights['action_items'].append("Engage in more learning activities to improve prediction accuracy")
        
        return insights


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def predictive_dashboard_data(request):
    """
    API endpoint for predictive analytics dashboard data
    """
    try:
        learning_path_id = request.query_params.get('learning_path_id')
        include_charts = request.query_params.get('include_charts', 'false').lower() == 'true'
        
        predictive_service = PredictiveAnalyticsService()
        
        # Get core predictive data
        ml_predictions = predictive_service.generate_ml_predictions(
            user=request.user,
            learning_path_id=learning_path_id,
            prediction_horizon_days=30
        )
        
        trends = predictive_service.analyze_historical_trends(
            user=request.user,
            learning_path_id=learning_path_id,
            analysis_period_days=90
        )
        
        confidence = predictive_service.statistical_confidence_calculations(
            user=request.user,
            learning_path_id=learning_path_id
        )
        
        # Prepare dashboard data
        dashboard_data = {
            'predictions': {
                'completion_forecast': ml_predictions.get('ensemble_prediction', {}),
                'confidence_level': ml_predictions.get('prediction_confidence', 0),
                'model_count': ml_predictions.get('model_count', 0),
                'data_quality': ml_predictions.get('data_points_used', 0)
            },
            'trends': {
                'learning_trajectory': trends.get('trends_analysis', {}).get('performance_trajectory', {}),
                'velocity_analysis': trends.get('trends_analysis', {}).get('velocity_trends', {}),
                'data_quality_score': trends.get('data_quality_score', 0)
            },
            'confidence': {
                'overall_confidence': confidence.get('sample_size', 0),
                'statistical_significance': confidence.get('statistical_significance', 'unknown')
            }
        }
        
        if include_charts:
            # Add chart-ready data
            dashboard_data['charts'] = {
                'prediction_chart': self._prepare_prediction_chart_data(ml_predictions),
                'trend_chart': self._prepare_trend_chart_data(trends),
                'confidence_chart': self._prepare_confidence_chart_data(confidence)
            }
        
        return Response({
            'success': True,
            'data': dashboard_data,
            'timestamp': timezone.now()
        })
        
    except Exception as e:
        logger.error(f"Predictive dashboard API error: {e}")
        return Response({
            'error': f'Failed to get dashboard data: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def _prepare_prediction_chart_data(ml_predictions: dict) -> dict:
    """Prepare chart data for predictions"""
    ensemble = ml_predictions.get('ensemble_prediction', {})
    predictions = ensemble.get('ensemble_predictions', [])
    
    return {
        'labels': [f'Day {i+1}' for i in range(len(predictions))],
        'data': predictions,
        'confidence_bands': {
            'upper': [p * 1.1 for p in predictions],
            'lower': [p * 0.9 for p in predictions]
        }
    }

# New Predictive Learning Models API Views
# =======================================

class LearningVelocityAPIView(APIView):
    """API for learning velocity analysis"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get learning velocity analysis"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            days_window = int(request.query_params.get('days_window', 30))
            
            service = PredictiveAnalyticsService()
            result = service.analyze_learning_velocity(
                user=request.user,
                learning_path_id=learning_path_id,
                days_window=days_window
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class EngagementPatternsAPIView(APIView):
    """API for engagement pattern analysis"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get engagement pattern analysis"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            analysis_depth = request.query_params.get('analysis_depth', 'comprehensive')
            
            service = PredictiveAnalyticsService()
            result = service.analyze_engagement_patterns(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_depth=analysis_depth
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class SuccessProbabilityAPIView(APIView):
    """API for success probability modeling"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get success probability prediction"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            target_module_id = request.query_params.get('target_module_id')
            time_horizon_days = int(request.query_params.get('time_horizon_days', 30))
            
            service = PredictiveAnalyticsService()
            result = service.model_success_probability(
                user=request.user,
                learning_path_id=learning_path_id,
                target_module_id=target_module_id,
                time_horizon_days=time_horizon_days
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class TimeToCompletionAPIView(APIView):
    """API for time-to-completion prediction"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get time-to-completion prediction"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            target_module_id = request.query_params.get('target_module_id')
            include_holidays = request.query_params.get('include_holidays', 'true').lower() == 'true'
            
            service = PredictiveAnalyticsService()
            result = service.predict_time_to_completion(
                user=request.user,
                learning_path_id=learning_path_id,
                target_module_id=target_module_id,
                include_holidays=include_holidays
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class RetentionRiskAPIView(APIView):
    """API for retention risk assessment"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get retention risk assessment"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            risk_horizon_days = int(request.query_params.get('risk_horizon_days', 30))
            
            service = PredictiveAnalyticsService()
            result = service.assess_retention_risk(
                user=request.user,
                learning_path_id=learning_path_id,
                risk_horizon_days=risk_horizon_days
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class KnowledgeGapsAPIView(APIView):
    """API for knowledge gap detection"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get knowledge gap detection"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            analysis_depth = request.query_params.get('analysis_depth', 'comprehensive')
            
            service = PredictiveAnalyticsService()
            result = service.detect_knowledge_gaps(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_depth=analysis_depth
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class LearningClustersAPIView(APIView):
    """API for learning analytics clustering"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get learning analytics clustering"""
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            cluster_count = request.query_params.get('cluster_count')
            feature_selection = request.query_params.get('feature_selection', 'comprehensive')
            
            service = PredictiveAnalyticsService()
            result = service.perform_learning_analytics_clustering(
                learning_path_id=learning_path_id,
                cluster_count=int(cluster_count) if cluster_count else None,
                feature_selection=feature_selection
            )
            
            return Response({
                'success': True,
                'data': result
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)


def _prepare_trend_chart_data(trends: dict) -> dict:
    """Prepare chart data for trends"""
    basic_trends = trends.get('trends_analysis', {}).get('basic_trends', {})
    
    return {
        'trend_direction': basic_trends.get('trend', 'stable'),
        'improvement_rate': basic_trends.get('improvement_rate', 0),
        'performance_data': [basic_trends.get('first_half_average', 50), 
                           basic_trends.get('second_half_average', 50)]
    }

def _prepare_confidence_chart_data(confidence: dict) -> dict:
    """Prepare chart data for confidence analysis"""
    return {
        'sample_size': confidence.get('sample_size', 0),
        'confidence_level': confidence.get('confidence_level', 0.95),
        'data_quality': 'good' if confidence.get('sample_size', 0) > 20 else 'limited'
    }