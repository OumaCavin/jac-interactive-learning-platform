# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Advanced Analytics API Views - JAC Learning Platform

API endpoints for sophisticated statistical analysis, enhanced ML insights,
advanced pattern recognition, and integrated personalized recommendations.

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

from ..services.advanced_analytics_service import AdvancedAnalyticsService
from .serializers import AdvancedAnalyticsSerializer

logger = logging.getLogger(__name__)


class SophisticatedStatisticalAnalysisAPIView(APIView):
    """
    API View for sophisticated statistical analysis
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get sophisticated statistical analysis including multivariate analysis,
        clustering, correlation analysis, and hypothesis testing
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            analysis_type = request.query_params.get('analysis_type', 'comprehensive')
            
            analytics_service = AdvancedAnalyticsService()
            analysis_results = analytics_service.generate_sophisticated_statistical_analysis(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_type=analysis_type
            )
            
            if 'error' in analysis_results:
                return Response({
                    'error': analysis_results['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Serialize results
            serializer = AdvancedAnalyticsSerializer(analysis_results)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in sophisticated statistical analysis API: {str(e)}")
            return Response({
                'error': f'Analysis failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EnhancedMLInsightsAPIView(APIView):
    """
    API View for enhanced ML insights
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get enhanced ML insights including feature importance analysis,
        model interpretability, user segmentation, and pathway optimization
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            
            analytics_service = AdvancedAnalyticsService()
            ml_insights = analytics_service.generate_enhanced_ml_insights(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            if 'error' in ml_insights:
                return Response({
                    'error': ml_insights['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'data': ml_insights,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in enhanced ML insights API: {str(e)}")
            return Response({
                'error': f'Analysis failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvancedPatternRecognitionAPIView(APIView):
    """
    API View for advanced pattern recognition
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get advanced pattern recognition including learning style detection,
        engagement patterns, performance anomalies, and knowledge acquisition patterns
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            
            analytics_service = AdvancedAnalyticsService()
            pattern_results = analytics_service.generate_advanced_pattern_recognition(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            if 'error' in pattern_results:
                return Response({
                    'error': pattern_results['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'data': pattern_results,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in advanced pattern recognition API: {str(e)}")
            return Response({
                'error': f'Analysis failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IntegratedPersonalizedRecommendationsAPIView(APIView):
    """
    API View for integrated personalized recommendations
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get integrated personalized recommendations combining knowledge graph
        recommendations with predictive analytics insights
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            recommendation_type = request.query_params.get('recommendation_type', 'comprehensive')
            
            analytics_service = AdvancedAnalyticsService()
            recommendations = analytics_service.generate_integrated_personalized_recommendations(
                user=request.user,
                learning_path_id=learning_path_id,
                recommendation_type=recommendation_type
            )
            
            if 'error' in recommendations:
                return Response({
                    'error': recommendations['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': True,
                'data': recommendations,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in integrated personalized recommendations API: {str(e)}")
            return Response({
                'error': f'Recommendation generation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdvancedAnalyticsDashboardAPIView(APIView):
    """
    API View for advanced analytics dashboard data
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get comprehensive dashboard data combining all advanced analytics features
        """
        try:
            learning_path_id = request.query_params.get('learning_path_id')
            include_recommendations = request.query_params.get('include_recommendations', 'true').lower() == 'true'
            
            analytics_service = AdvancedAnalyticsService()
            
            # Collect all analytics
            statistical_analysis = analytics_service.generate_sophisticated_statistical_analysis(
                user=request.user,
                learning_path_id=learning_path_id,
                analysis_type='dashboard'
            )
            
            ml_insights = analytics_service.generate_enhanced_ml_insights(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            pattern_recognition = analytics_service.generate_advanced_pattern_recognition(
                user=request.user,
                learning_path_id=learning_path_id
            )
            
            recommendations = {}
            if include_recommendations:
                recommendations = analytics_service.generate_integrated_personalized_recommendations(
                    user=request.user,
                    learning_path_id=learning_path_id,
                    recommendation_type='dashboard'
                )
            
            # Check for errors
            errors = []
            for name, data in [('statistical_analysis', statistical_analysis), 
                              ('ml_insights', ml_insights), 
                              ('pattern_recognition', pattern_recognition)]:
                if 'error' in data:
                    errors.append(f"{name}: {data['error']}")
            
            dashboard_data = {
                'user_id': str(request.user.id),
                'dashboard_timestamp': timezone.now().isoformat(),
                'learning_path_id': learning_path_id,
                'statistical_analysis': statistical_analysis,
                'ml_insights': ml_insights,
                'pattern_recognition': pattern_recognition,
                'integrated_recommendations': recommendations if include_recommendations else {},
                'errors': errors,
                'data_availability': {
                    'statistical_analysis': 'error' not in statistical_analysis,
                    'ml_insights': 'error' not in ml_insights,
                    'pattern_recognition': 'error' not in pattern_recognition,
                    'recommendations': 'error' not in recommendations if include_recommendations else False
                },
                'dashboard_summary': self._generate_dashboard_summary(
                    statistical_analysis, ml_insights, pattern_recognition, recommendations
                )
            }
            
            return Response({
                'success': True,
                'data': dashboard_data,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in advanced analytics dashboard API: {str(e)}")
            return Response({
                'error': f'Dashboard generation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_dashboard_summary(self, statistical_analysis, ml_insights, pattern_recognition, recommendations):
        """Generate a comprehensive dashboard summary."""
        try:
            summary = {
                'overall_data_quality': 'Unknown',
                'key_findings': [],
                'top_recommendations': [],
                'analysis_status': 'Complete',
                'confidence_level': 'Unknown'
            }
            
            # Assess data quality
            if 'error' not in statistical_analysis and 'data_quality_score' in statistical_analysis:
                quality_score = statistical_analysis.get('data_quality_score', 0)
                if quality_score >= 0.8:
                    summary['overall_data_quality'] = 'Excellent'
                elif quality_score >= 0.6:
                    summary['overall_data_quality'] = 'Good'
                elif quality_score >= 0.4:
                    summary['overall_data_quality'] = 'Fair'
                else:
                    summary['overall_data_quality'] = 'Poor'
            
            # Collect key findings
            if 'error' not in statistical_analysis and 'key_statistical_insights' in statistical_analysis:
                summary['key_findings'].extend(statistical_analysis.get('key_statistical_insights', []))
            
            if 'error' not in ml_insights and 'ml_insights_summary' in ml_insights:
                summary['key_findings'].append(f"ML Insights: {ml_insights['ml_insights_summary']}")
            
            if 'error' not in pattern_recognition and 'pattern_recognition_summary' in pattern_recognition:
                summary['key_findings'].append(f"Pattern Analysis: {pattern_recognition['pattern_recognition_summary']}")
            
            # Collect top recommendations
            if 'error' not in recommendations and 'ranked_recommendations' in recommendations:
                top_recs = recommendations['ranked_recommendations'][:3]
                summary['top_recommendations'] = [
                    rec.get('title', rec.get('reason', 'Recommendation')) for rec in top_recs
                ]
            
            # Assess confidence level
            available_analyses = sum(1 for data in [statistical_analysis, ml_insights, pattern_recognition] 
                                   if 'error' not in data)
            if available_analyses >= 3:
                summary['confidence_level'] = 'High'
            elif available_analyses >= 2:
                summary['confidence_level'] = 'Medium'
            else:
                summary['confidence_level'] = 'Low'
            
            # Determine analysis status
            if errors := [name for name, data in [('Statistical', statistical_analysis), 
                                                ('ML', ml_insights), 
                                                ('Pattern', pattern_recognition)] 
                         if 'error' in data]:
                summary['analysis_status'] = f'Partial - Issues with: {", ".join(errors)}'
            else:
                summary['analysis_status'] = 'Complete'
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating dashboard summary: {str(e)}")
            return {
                'overall_data_quality': 'Unknown',
                'key_findings': ['Dashboard summary generation failed'],
                'top_recommendations': [],
                'analysis_status': 'Error',
                'confidence_level': 'Unknown'
            }


# Convenience function for API decorators
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def advanced_analytics_dashboard(request):
    """
    Convenience endpoint for advanced analytics dashboard
    """
    view = AdvancedAnalyticsDashboardAPIView()
    return view.get(request)
