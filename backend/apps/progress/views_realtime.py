"""
Real-time Progress API Endpoints - JAC Learning Platform

This module provides REST API endpoints for real-time progress monitoring,
performance alerts, predictive analytics, and trend analysis.

Endpoints:
- /api/progress/real-time-dashboard/ - Real-time dashboard data
- /api/progress/predictive-analytics/ - ML-powered predictions
- /api/progress/performance-alerts/ - Live performance alerts  
- /api/progress/trend-analysis/ - Advanced trend analysis

Author: MiniMax Agent
Created: 2025-11-26
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count, Max, Min, Sum
from django.core.cache import cache

from .services.realtime_monitoring_service import RealtimeMonitoringService
from .services.predictive_analytics_service import PredictiveAnalyticsService
from .services.progress_service import ProgressService
from .models import ProgressNotification, LearningAnalytics
from apps.learning.models import UserModuleProgress, AssessmentAttempt


class RealTimeDashboardAPIView(APIView):
    """
    API endpoint for real-time dashboard data
    GET /api/progress/real-time-dashboard/
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.realtime_service = RealtimeMonitoringService()
    
    def get(self, request):
        """Get real-time dashboard data"""
        try:
            user = request.user
            
            # Get current user progress
            progress_service = ProgressService()
            current_progress = progress_service.get_current_user_progress(user.id)
            
            # Get real-time metrics
            realtime_metrics = self._get_realtime_metrics(user)
            
            # Get recent activities
            recent_activities = self._get_recent_activities(user)
            
            # Get performance trends (last 7 days)
            performance_trends = self._get_performance_trends(user)
            
            # Get active goals and milestones
            goals_data = self._get_active_goals_data(user)
            
            # Get learning session data
            session_data = self._get_session_data(user)
            
            dashboard_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'progress_summary': {
                    'overall_progress': current_progress.get('completion_rate', 0),
                    'modules_completed': current_progress.get('completed_modules', 0),
                    'total_modules': current_progress.get('total_modules', 0),
                    'current_level': current_progress.get('level', 'Beginner'),
                    'streak_days': current_progress.get('learning_streak', 0)
                },
                'realtime_metrics': realtime_metrics,
                'recent_activities': recent_activities,
                'performance_trends': performance_trends,
                'goals_data': goals_data,
                'session_data': session_data,
                'insights': self._generate_dashboard_insights(user, realtime_metrics)
            }
            
            return Response(dashboard_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve dashboard data',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_realtime_metrics(self, user: User) -> Dict[str, Any]:
        """Get real-time performance metrics"""
        # Get metrics from cache first
        cache_key = f"realtime_metrics_{user.id}"
        cached_metrics = cache.get(cache_key)
        
        if cached_metrics:
            return cached_metrics
        
        # Calculate fresh metrics
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        week_ago = today - timedelta(days=7)
        
        # Today's activities
        today_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__date=today
        ).count()
        
        today_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__date=today
        ).count()
        
        # Yesterday's activities for comparison
        yesterday_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__date=yesterday
        ).count()
        
        # Recent assessment scores (last 7 days)
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=week_ago,
            score__isnull=False
        )
        
        avg_score = recent_assessments.aggregate(Avg('score'))['score__avg'] or 0
        total_assessments = recent_assessments.count()
        
        # Calculate engagement trend
        progress_change = today_progress - yesterday_progress
        engagement_level = min(100, max(0, today_progress * 10 + 50))
        
        metrics = {
            'daily_activities': today_progress,
            'daily_assessments': today_assessments,
            'weekly_assessments': total_assessments,
            'average_score': round(avg_score, 2),
            'engagement_level': engagement_level,
            'activity_change': progress_change,
            'performance_trend': 'improving' if avg_score > 75 else 'stable' if avg_score > 60 else 'needs_attention',
            'last_updated': timezone.now().isoformat()
        }
        
        # Cache for 2 minutes
        cache.set(cache_key, metrics, timeout=120)
        
        return metrics
    
    def _get_recent_activities(self, user: User, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent user activities"""
        activities = []
        
        # Recent module progress
        recent_progress = UserModuleProgress.objects.filter(
            user=user
        ).order_by('-updated_at')[:5]
        
        for progress in recent_progress:
            activities.append({
                'type': 'module_progress',
                'title': progress.module.title,
                'status': progress.status,
                'score': progress.score,
                'timestamp': progress.updated_at.isoformat()
            })
        
        # Recent assessment attempts
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__isnull=False
        ).order_by('-completed_at')[:5]
        
        for assessment in recent_assessments:
            activities.append({
                'type': 'assessment_completed',
                'title': assessment.assessment.title,
                'score': assessment.score,
                'max_score': assessment.max_score,
                'percentage': round((assessment.score / assessment.max_score) * 100, 2) if assessment.max_score > 0 else 0,
                'timestamp': assessment.completed_at.isoformat()
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return activities[:limit]
    
    def _get_performance_trends(self, user: User) -> Dict[str, Any]:
        """Get performance trends over time"""
        # Get daily performance for last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        daily_scores = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=thirty_days_ago,
            score__isnull=False
        ).extra(
            select={'day': 'date(completed_at)'}
        ).values('day').annotate(
            avg_score=Avg('score'),
            count=Count('id')
        ).order_by('day')
        
        # Prepare trend data
        trend_data = []
        for day_data in daily_scores:
            trend_data.append({
                'date': day_data['day'],
                'average_score': round(day_data['avg_score'], 2),
                'assessment_count': day_data['count']
            })
        
        # Calculate trend direction
        if len(trend_data) >= 2:
            recent_avg = sum(d['average_score'] for d in trend_data[-7:]) / min(7, len(trend_data))
            previous_avg = sum(d['average_score'] for d in trend_data[-14:-7]) / min(7, len(trend_data) - 7) if len(trend_data) > 7 else recent_avg
            
            trend_direction = 'improving' if recent_avg > previous_avg + 2 else 'stable' if abs(recent_avg - previous_avg) <= 2 else 'declining'
        else:
            trend_direction = 'insufficient_data'
        
        return {
            'trend_direction': trend_direction,
            'daily_data': trend_data,
            'overall_average': round(sum(d['average_score'] for d in trend_data) / len(trend_data), 2) if trend_data else 0,
            'data_points': len(trend_data)
        }
    
    def _get_active_goals_data(self, user: User) -> Dict[str, Any]:
        """Get active goals and progress"""
        # This would integrate with a goals system
        # For now, return mock data structure
        
        return {
            'active_goals': [],
            'completed_goals_today': 0,
            'weekly_goal_progress': 0,
            'upcoming_milestones': []
        }
    
    def _get_session_data(self, user: User) -> Dict[str, Any]:
        """Get current learning session data"""
        # Get current session information
        today = timezone.now().date()
        
        # Today's session time (simplified calculation)
        today_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__date=today
        )
        
        estimated_time_spent = today_progress.count() * 15  # Assume 15 min per activity
        
        return {
            'session_start': None,  # Would track actual session start
            'estimated_time_spent': estimated_time_spent,
            'activities_completed': today_progress.count(),
            'focus_level': 'high' if today_progress.count() >= 3 else 'moderate' if today_progress.count() >= 1 else 'low'
        }
    
    def _generate_dashboard_insights(self, user: User, metrics: Dict[str, Any]) -> List[str]:
        """Generate personalized dashboard insights"""
        insights = []
        
        # Performance insights
        avg_score = metrics.get('average_score', 0)
        if avg_score >= 85:
            insights.append("Excellent performance! You're consistently scoring above 85%")
        elif avg_score >= 70:
            insights.append("Good progress! Consider focusing on areas where you scored below 80%")
        else:
            insights.append("Performance needs attention. Review fundamental concepts and practice more")
        
        # Engagement insights
        daily_activities = metrics.get('daily_activities', 0)
        if daily_activities >= 5:
            insights.append("High engagement today! Keep up the great momentum")
        elif daily_activities >= 2:
            insights.append("Moderate activity today. Try to complete at least 3 learning activities")
        else:
            insights.append("Low activity today. Set a goal to complete at least 2 learning sessions")
        
        # Learning streak insights
        streak_days = metrics.get('streak_days', 0)
        if streak_days >= 7:
            insights.append(f"Amazing! You've maintained a {streak_days}-day learning streak")
        elif streak_days >= 3:
            insights.append(f"Good streak! You're on day {streak_days} of continuous learning")
        
        return insights


class PredictiveAnalyticsAPIView(APIView):
    """
    API endpoint for ML-powered predictions
    GET /api/progress/predictive-analytics/
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.predictive_service = PredictiveAnalyticsService()
    
    def get(self, request):
        """Get ML-powered predictions"""
        try:
            user = request.user
            time_horizon = request.GET.get('horizon', '30')  # days
            learning_path_id = request.GET.get('learning_path_id')
            
            # Get comprehensive predictions
            predictions = self._get_comprehensive_predictions(user, int(time_horizon), learning_path_id)
            
            # Get performance forecasts
            performance_forecast = self._get_performance_forecast(user)
            
            # Get learning recommendations
            learning_recommendations = self._get_learning_recommendations(user)
            
            # Get completion predictions
            completion_predictions = self._get_completion_predictions(user)
            
            response_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'prediction_horizon_days': int(time_horizon),
                'comprehensive_predictions': predictions,
                'performance_forecast': performance_forecast,
                'learning_recommendations': learning_recommendations,
                'completion_predictions': completion_predictions,
                'confidence_scores': self._get_prediction_confidence(user),
                'model_insights': self._get_model_insights(user)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to generate predictions',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_comprehensive_predictions(self, user: User, time_horizon: int, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Get comprehensive ML predictions"""
        # Use the predictive analytics service
        try:
            predictions = self.predictive_service.generate_comprehensive_predictions(
                user=user,
                time_horizon_days=time_horizon,
                learning_path_id=learning_path_id
            )
            return predictions
        except Exception as e:
            # Fallback to basic predictions if service fails
            return self._fallback_predictions(user, time_horizon)
    
    def _get_performance_forecast(self, user: User) -> Dict[str, Any]:
        """Get performance forecasting predictions"""
        # Get historical performance data
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            score__isnull=False,
            completed_at__gte=timezone.now() - timedelta(days=60)
        ).order_by('-completed_at')[:50]
        
        if not recent_assessments.exists():
            return {
                'forecast_available': False,
                'message': 'Insufficient data for performance forecasting'
            }
        
        # Calculate trend
        scores = [a.score for a in recent_assessments]
        recent_scores = scores[:10]  # Last 10 scores
        previous_scores = scores[10:20] if len(scores) > 10 else scores[:10]
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        previous_avg = sum(previous_scores) / len(previous_scores)
        
        trend_direction = 'improving' if recent_avg > previous_avg + 2 else 'declining' if recent_avg < previous_avg - 2 else 'stable'
        
        # Simple linear projection
        score_change = recent_avg - previous_avg
        projected_next_score = min(100, max(0, recent_avg + score_change))
        
        return {
            'forecast_available': True,
            'current_trend': trend_direction,
            'recent_average': round(recent_avg, 2),
            'projected_next_score': round(projected_next_score, 2),
            'confidence_level': 'medium' if len(scores) >= 20 else 'low',
            'data_points': len(scores),
            'forecast_factors': self._identify_forecast_factors(user)
        }
    
    def _get_learning_recommendations(self, user: User) -> List[Dict[str, Any]]:
        """Get AI-generated learning recommendations"""
        recommendations = []
        
        # Analyze recent performance
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=14),
            score__isnull=False
        )
        
        if recent_assessments.exists():
            avg_score = recent_assessments.aggregate(Avg('score'))['score__avg'] or 0
            
            if avg_score < 70:
                recommendations.append({
                    'type': 'performance_improvement',
                    'priority': 'high',
                    'title': 'Focus on Practice Exercises',
                    'description': 'Your recent scores suggest need for more practice in core concepts',
                    'action': 'Complete 3 practice exercises in your weakest areas',
                    'expected_impact': '10-15% improvement in next 2 weeks'
                })
            elif avg_score > 85:
                recommendations.append({
                    'type': 'advanced_challenges',
                    'priority': 'medium',
                    'title': 'Challenge Yourself',
                    'description': 'You\'re performing well! Consider tackling advanced materials',
                    'action': 'Explore advanced modules or difficult assessments',
                    'expected_impact': 'Enhanced learning and skill development'
                })
        
        # Learning pace recommendations
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=7)
        )
        
        if recent_progress.count() < 3:
            recommendations.append({
                'type': 'pace_adjustment',
                'priority': 'medium',
                'title': 'Increase Learning Pace',
                'description': 'Consider dedicating more time to learning this week',
                'action': 'Set a goal to complete 5 learning activities this week',
                'expected_impact': 'Improved consistency and retention'
            })
        
        return recommendations
    
    def _get_completion_predictions(self, user: User) -> Dict[str, Any]:
        """Get learning path completion predictions"""
        # Get user's learning path progress
        total_modules = UserModuleProgress.objects.filter(user=user).count()
        completed_modules = UserModuleProgress.objects.filter(
            user=user,
            status='completed'
        ).count()
        
        if total_modules == 0:
            return {
                'prediction_available': False,
                'message': 'No learning path data available'
            }
        
        completion_rate = (completed_modules / total_modules) * 100
        
        # Estimate time to completion based on current pace
        recent_completions = UserModuleProgress.objects.filter(
            user=user,
            status='completed',
            updated_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if recent_completions > 0:
            modules_per_day = recent_completions / 30
            remaining_modules = total_modules - completed_modules
            estimated_days = remaining_modules / modules_per_day if modules_per_day > 0 else 999
        else:
            estimated_days = remaining_modules * 3  # Assume 3 days per module as fallback
        
        return {
            'prediction_available': True,
            'completion_rate': round(completion_rate, 2),
            'modules_completed': completed_modules,
            'modules_remaining': total_modules - completed_modules,
            'estimated_completion_days': round(estimated_days, 0),
            'estimated_completion_date': (timezone.now() + timedelta(days=estimated_days)).date().isoformat(),
            'confidence_level': 'high' if recent_completions >= 10 else 'medium' if recent_completions >= 5 else 'low',
            'pace_factors': {
                'recent_activity': recent_completions > 0,
                'consistency_score': min(100, recent_completions * 10),
                'recommendation': 'increase_pace' if estimated_days > 60 else 'maintain_pace' if estimated_days > 30 else 'excellent_pace'
            }
        }
    
    def _get_prediction_confidence(self, user: User) -> Dict[str, Any]:
        """Get confidence scores for predictions"""
        # Calculate data quality metrics
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=90)
        )
        
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=30)
        )
        
        assessment_confidence = 'high' if recent_assessments.count() >= 15 else 'medium' if recent_assessments.count() >= 5 else 'low'
        activity_confidence = 'high' if recent_progress.count() >= 20 else 'medium' if recent_progress.count() >= 10 else 'low'
        
        return {
            'overall_confidence': 'high' if assessment_confidence == 'high' and activity_confidence == 'high' else 'medium',
            'assessment_data_confidence': assessment_confidence,
            'activity_data_confidence': activity_confidence,
            'data_points': {
                'recent_assessments': recent_assessments.count(),
                'recent_activities': recent_progress.count(),
                'data_recency_days': 0  # How old the oldest data point is
            }
        }
    
    def _get_model_insights(self, user: User) -> List[str]:
        """Get insights about prediction models"""
        insights = []
        
        # Data quality insights
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if recent_assessments < 5:
            insights.append("More assessment data would improve prediction accuracy")
        
        # Learning pattern insights
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if recent_progress == 0:
            insights.append("No recent learning activity - predictions may be less accurate")
        elif recent_progress >= 5:
            insights.append("Strong learning consistency detected - high confidence predictions available")
        
        return insights
    
    def _fallback_predictions(self, user: User, time_horizon: int) -> Dict[str, Any]:
        """Provide basic predictions when advanced service fails"""
        return {
            'performance_prediction': 'stable',
            'engagement_prediction': 'maintain_current_level',
            'completion_estimate': time_horizon // 2,
            'recommendations': [
                'Continue current learning pace',
                'Focus on consistent daily practice'
            ],
            'confidence': 'low'
        }
    
    def _identify_forecast_factors(self, user: User) -> List[str]:
        """Identify factors affecting performance forecast"""
        factors = []
        
        # Activity frequency
        recent_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if recent_activities >= 5:
            factors.append("High recent activity frequency")
        elif recent_activities <= 1:
            factors.append("Low recent activity frequency")
        
        # Performance consistency
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=14),
            score__isnull=False
        )
        
        if recent_assessments.count() >= 3:
            scores = [a.score for a in recent_assessments]
            score_variance = np.var(scores) if len(scores) > 1 else 0
            
            if score_variance < 100:
                factors.append("Consistent performance pattern")
            else:
                factors.append("Variable performance pattern")
        
        return factors


class PerformanceAlertsAPIView(APIView):
    """
    API endpoint for live performance alerts
    GET /api/progress/performance-alerts/
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.realtime_service = RealtimeMonitoringService()
    
    def get(self, request):
        """Get live performance alerts"""
        try:
            user = request.user
            alert_types = request.GET.get('types', 'all')  # performance, engagement, achievements
            severity_filter = request.GET.get('severity', 'all')  # low, medium, high
            
            # Get current alerts
            alerts = self._generate_performance_alerts(user, alert_types)
            
            # Apply severity filter
            if severity_filter != 'all':
                alerts = [alert for alert in alerts if alert.get('severity') == severity_filter]
            
            # Get alert history
            alert_history = self._get_alert_history(user, days=7)
            
            # Get alert statistics
            alert_stats = self._get_alert_statistics(user)
            
            response_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'current_alerts': alerts,
                'alert_history': alert_history,
                'alert_statistics': alert_stats,
                'alert_preferences': self._get_alert_preferences(user),
                'recommendations': self._generate_alert_recommendations(user, alerts)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve performance alerts',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_performance_alerts(self, user: User, alert_types: str) -> List[Dict[str, Any]]:
        """Generate performance-based alerts"""
        alerts = []
        
        # Performance alerts
        if alert_types in ['all', 'performance']:
            performance_alerts = self._check_performance_alerts(user)
            alerts.extend(performance_alerts)
        
        # Engagement alerts
        if alert_types in ['all', 'engagement']:
            engagement_alerts = self._check_engagement_alerts(user)
            alerts.extend(engagement_alerts)
        
        # Achievement alerts
        if alert_types in ['all', 'achievements']:
            achievement_alerts = self._check_achievement_alerts(user)
            alerts.extend(achievement_alerts)
        
        # Goal-based alerts
        if alert_types in ['all', 'goals']:
            goal_alerts = self._check_goal_alerts(user)
            alerts.extend(goal_alerts)
        
        # System alerts
        if alert_types in ['all', 'system']:
            system_alerts = self._check_system_alerts(user)
            alerts.extend(system_alerts)
        
        # Sort by severity and timestamp
        alerts.sort(key=lambda x: (x.get('severity', 'low'), x.get('timestamp')), reverse=True)
        
        return alerts[:20]  # Limit to 20 most recent alerts
    
    def _check_performance_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Check for performance-related alerts"""
        alerts = []
        
        # Check recent assessment performance
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=7),
            score__isnull=False
        )
        
        if recent_assessments.exists():
            avg_score = recent_assessments.aggregate(Avg('score'))['score__avg'] or 0
            lowest_score = recent_assessments.aggregate(Min('score'))['score__min'] or 0
            
            # Low performance alert
            if avg_score < 60:
                alerts.append({
                    'type': 'performance',
                    'severity': 'high',
                    'category': 'low_scores',
                    'title': 'Performance Below Average',
                    'message': f'Your average score this week is {avg_score:.1f}%, which is below the recommended 70% threshold',
                    'current_value': avg_score,
                    'threshold': 70,
                    'recommendation': 'Focus on practice exercises and review fundamental concepts',
                    'timestamp': timezone.now().isoformat(),
                    'actionable': True
                })
            
            # Declining performance alert
            if len(recent_assessments) >= 3:
                scores = [a.score for a in recent_assessments.order_by('-completed_at')[:3]]
                if scores[0] < scores[1] < scores[2]:  # Decreasing trend
                    alerts.append({
                        'type': 'performance',
                        'severity': 'medium',
                        'category': 'declining_trend',
                        'title': 'Declining Performance Trend',
                        'message': f'Your last 3 assessment scores show a declining trend: {scores[2]:.1f}% → {scores[1]:.1f}% → {scores[0]:.1f}%',
                        'trend_data': scores,
                        'recommendation': 'Take a step back and review the concepts you\'re struggling with',
                        'timestamp': timezone.now().isoformat(),
                        'actionable': True
                    })
        
        return alerts
    
    def _check_engagement_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Check for engagement-related alerts"""
        alerts = []
        
        # Check daily activity
        today = timezone.now().date()
        today_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__date=today
        ).count()
        
        if today_activities == 0:
            alerts.append({
                'type': 'engagement',
                'severity': 'medium',
                'category': 'inactive_day',
                'title': 'No Learning Activity Today',
                'message': 'You haven\'t completed any learning activities today',
                'recommendation': 'Try to complete at least one learning module today to maintain momentum',
                'timestamp': timezone.now().isoformat(),
                'actionable': True
            })
        
        # Check weekly engagement
        week_ago = timezone.now() - timedelta(days=7)
        weekly_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=week_ago
        ).count()
        
        if weekly_activities < 3:
            alerts.append({
                'type': 'engagement',
                'severity': 'high',
                'category': 'low_weekly_engagement',
                'title': 'Low Weekly Engagement',
                'message': f'Only {weekly_activities} learning activities completed this week',
                'recommendation': 'Aim for at least 5-7 learning activities per week for optimal progress',
                'timestamp': timezone.now().isoformat(),
                'actionable': True
            })
        
        return alerts
    
    def _check_achievement_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Check for achievement-related alerts"""
        alerts = []
        
        # Check for streak achievements
        streak_days = self._calculate_learning_streak(user)
        
        if streak_days == 7:
            alerts.append({
                'type': 'achievement',
                'severity': 'success',
                'category': 'streak_milestone',
                'title': '7-Day Learning Streak!',
                'message': f'Congratulations! You\'ve maintained a {streak_days}-day learning streak',
                'recommendation': 'Keep up the great work! Try to reach 14 days',
                'timestamp': timezone.now().isoformat(),
                'actionable': False,
                'milestone': '7_days'
            })
        
        elif streak_days == 30:
            alerts.append({
                'type': 'achievement',
                'severity': 'success',
                'category': 'streak_milestone',
                'title': '30-Day Learning Streak!',
                'message': f'Incredible! You\'ve maintained a {streak_days}-day learning streak',
                'recommendation': 'You\'re a learning champion! Consider helping other students',
                'timestamp': timezone.now().isoformat(),
                'actionable': False,
                'milestone': '30_days'
            })
        
        # Check for progress milestones
        completed_modules = UserModuleProgress.objects.filter(
            user=user,
            status='completed'
        ).count()
        
        if completed_modules in [10, 25, 50, 100]:
            alerts.append({
                'type': 'achievement',
                'severity': 'success',
                'category': 'progress_milestone',
                'title': f'{completed_modules} Modules Completed!',
                'message': f'Great job! You\'ve completed {completed_modules} learning modules',
                'recommendation': 'Keep progressing toward your next milestone',
                'timestamp': timezone.now().isoformat(),
                'actionable': False,
                'milestone': f'{completed_modules}_modules'
            })
        
        return alerts
    
    def _check_goal_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Check for goal-related alerts"""
        # This would integrate with a goals system
        # For now, return empty list
        
        return []
    
    def _check_system_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Check for system-level alerts"""
        alerts = []
        
        # Check if user hasn't logged in recently
        if hasattr(user, 'last_login'):
            days_since_login = (timezone.now() - user.last_login).days
            if days_since_login > 3:
                alerts.append({
                    'type': 'system',
                    'severity': 'medium',
                    'category': 'inactive_account',
                    'title': 'Return to Learning',
                    'message': f'It\'s been {days_since_login} days since your last login',
                    'recommendation': 'Come back and continue your learning journey',
                    'timestamp': timezone.now().isoformat(),
                    'actionable': True
                })
        
        return alerts
    
    def _get_alert_history(self, user: User, days: int = 7) -> List[Dict[str, Any]]:
        """Get alert history for the specified period"""
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get alerts from notifications model
        recent_notifications = ProgressNotification.objects.filter(
            user=user,
            created_at__gte=cutoff_date,
            is_sent=True
        ).order_by('-created_at')[:20]
        
        alert_history = []
        for notification in recent_notifications:
            alert_history.append({
                'type': notification.notification_type,
                'title': notification.title,
                'message': notification.message,
                'priority': notification.priority,
                'timestamp': notification.created_at.isoformat(),
                'read': notification.is_read
            })
        
        return alert_history
    
    def _get_alert_statistics(self, user: User) -> Dict[str, Any]:
        """Get statistics about alerts"""
        week_ago = timezone.now() - timedelta(days=7)
        
        recent_alerts = ProgressNotification.objects.filter(
            user=user,
            created_at__gte=week_ago,
            is_sent=True
        )
        
        total_alerts = recent_alerts.count()
        high_priority = recent_alerts.filter(priority='high').count()
        medium_priority = recent_alerts.filter(priority='medium').count()
        low_priority = recent_alerts.filter(priority='low').count()
        
        # Alert frequency by type
        alert_types = {}
        for alert_type in recent_alerts.values_list('notification_type', flat=True).distinct():
            alert_types[alert_type] = recent_alerts.filter(notification_type=alert_type).count()
        
        return {
            'total_alerts_last_week': total_alerts,
            'high_priority_count': high_priority,
            'medium_priority_count': medium_priority,
            'low_priority_count': low_priority,
            'alert_frequency': 'high' if total_alerts >= 10 else 'medium' if total_alerts >= 5 else 'low',
            'alert_types': alert_types,
            'average_alerts_per_day': round(total_alerts / 7, 2)
        }
    
    def _get_alert_preferences(self, user: User) -> Dict[str, Any]:
        """Get user's alert preferences"""
        # This would typically come from user preferences
        # For now, return default preferences
        
        return {
            'performance_alerts_enabled': True,
            'engagement_alerts_enabled': True,
            'achievement_alerts_enabled': True,
            'goal_alerts_enabled': True,
            'email_notifications': True,
            'push_notifications': True,
            'frequency': 'daily',
            'quiet_hours': {
                'enabled': False,
                'start': '22:00',
                'end': '08:00'
            }
        }
    
    def _generate_alert_recommendations(self, user: User, alerts: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on current alerts"""
        recommendations = []
        
        # Count alert types
        performance_alerts = [a for a in alerts if a['type'] == 'performance' and a['severity'] == 'high']
        engagement_alerts = [a for a in alerts if a['type'] == 'engagement']
        achievement_alerts = [a for a in alerts if a['type'] == 'achievement']
        
        if performance_alerts:
            recommendations.append("Focus on improving performance through targeted practice exercises")
        
        if engagement_alerts:
            recommendations.append("Set up a consistent daily learning schedule to improve engagement")
        
        if len(alerts) >= 5:
            recommendations.append("Consider reviewing your learning strategies with a mentor or tutor")
        
        return recommendations
    
    def _calculate_learning_streak(self, user: User) -> int:
        """Calculate current learning streak"""
        streak = 0
        current_date = timezone.now().date()
        
        while True:
            day_activities = UserModuleProgress.objects.filter(
                user=user,
                updated_at__date=current_date - timedelta(days=streak)
            ).exists()
            
            if day_activities:
                streak += 1
            else:
                break
        
        return streak


class TrendAnalysisAPIView(APIView):
    """
    API endpoint for advanced trend analysis
    GET /api/progress/trend-analysis/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get advanced trend analysis"""
        try:
            user = request.user
            analysis_period = request.GET.get('period', '30')  # days
            analysis_type = request.GET.get('type', 'comprehensive')  # performance, engagement, overall
            
            # Get trend analysis data
            trend_data = self._analyze_learning_trends(user, int(analysis_period), analysis_type)
            
            # Get performance trends
            performance_trends = self._analyze_performance_trends(user, int(analysis_period))
            
            # Get engagement trends
            engagement_trends = self._analyze_engagement_trends(user, int(analysis_period))
            
            # Get learning pattern analysis
            pattern_analysis = self._analyze_learning_patterns(user)
            
            # Get predictive trends
            predictive_trends = self._analyze_predictive_trends(user, int(analysis_period))
            
            response_data = {
                'user_id': user.id,
                'timestamp': timezone.now().isoformat(),
                'analysis_period_days': int(analysis_period),
                'analysis_type': analysis_type,
                'comprehensive_trends': trend_data,
                'performance_trends': performance_trends,
                'engagement_trends': engagement_trends,
                'pattern_analysis': pattern_analysis,
                'predictive_trends': predictive_trends,
                'trend_insights': self._generate_trend_insights(user, trend_data),
                'recommendations': self._generate_trend_recommendations(user, trend_data)
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Failed to analyze trends',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _analyze_learning_trends(self, user: User, period_days: int, analysis_type: str) -> Dict[str, Any]:
        """Analyze overall learning trends"""
        start_date = timezone.now() - timedelta(days=period_days)
        
        # Get learning activities over time
        activities_over_time = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date
        ).extra(
            select={'date': 'date(updated_at)'}
        ).values('date').annotate(
            count=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            average_score=Avg('score')
        ).order_by('date')
        
        # Get assessment trends
        assessments_over_time = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=start_date,
            score__isnull=False
        ).extra(
            select={'date': 'date(completed_at)'}
        ).values('date').annotate(
            count=Count('id'),
            average_score=Avg('score')
        ).order_by('date')
        
        # Calculate trend metrics
        total_activities = sum(day['count'] for day in activities_over_time)
        total_completed = sum(day['completed'] for day in activities_over_time)
        completion_rate = (total_completed / max(total_activities, 1)) * 100
        
        # Calculate trend direction
        recent_activity = sum(day['count'] for day in activities_over_time[-7:]) if len(activities_over_time) >= 7 else 0
        previous_activity = sum(day['count'] for day in activities_over_time[-14:-7]) if len(activities_over_time) >= 14 else recent_activity
        
        trend_direction = 'improving' if recent_activity > previous_activity else 'declining' if recent_activity < previous_activity else 'stable'
        
        return {
            'trend_direction': trend_direction,
            'total_activities': total_activities,
            'completion_rate': round(completion_rate, 2),
            'daily_data': [
                {
                    'date': day['date'],
                    'activities': day['count'],
                    'completed': day['completed'],
                    'average_score': round(day['average_score'] or 0, 2)
                }
                for day in activities_over_time
            ],
            'assessment_data': [
                {
                    'date': day['date'],
                    'assessments': day['count'],
                    'average_score': round(day['average_score'], 2)
                }
                for day in assessments_over_time
            ],
            'period_summary': {
                'days_analyzed': period_days,
                'average_daily_activities': round(total_activities / period_days, 2),
                'peak_activity_day': max(activities_over_time, key=lambda x: x['count'])['date'] if activities_over_time else None,
                'consistency_score': self._calculate_consistency_score(activities_over_time, period_days)
            }
        }
    
    def _analyze_performance_trends(self, user: User, period_days: int) -> Dict[str, Any]:
        """Analyze performance-specific trends"""
        start_date = timezone.now() - timedelta(days=period_days)
        
        # Get assessment performance over time
        performance_data = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=start_date,
            score__isnull=False
        ).order_by('completed_at')
        
        if not performance_data.exists():
            return {
                'trend_available': False,
                'message': 'No performance data available for analysis'
            }
        
        # Calculate moving averages
        scores = [attempt.score for attempt in performance_data]
        moving_averages = self._calculate_moving_averages(scores, window=5)
        
        # Calculate performance volatility
        volatility = np.std(scores) if len(scores) > 1 else 0
        
        # Calculate trend slope (simple linear regression)
        trend_slope = self._calculate_trend_slope(scores)
        
        # Performance distribution
        score_ranges = {
            'excellent': sum(1 for score in scores if score >= 90),
            'good': sum(1 for score in scores if 80 <= score < 90),
            'average': sum(1 for score in scores if 70 <= score < 80),
            'below_average': sum(1 for score in scores if score < 70)
        }
        
        return {
            'trend_available': True,
            'trend_slope': round(trend_slope, 4),
            'performance_volatility': round(volatility, 2),
            'current_average': round(np.mean(scores[-5:]) if len(scores) >= 5 else np.mean(scores), 2),
            'overall_average': round(np.mean(scores), 2),
            'score_distribution': score_ranges,
            'moving_averages': moving_averages,
            'performance_rating': self._get_performance_rating(scores),
            'improvement_areas': self._identify_improvement_areas(user, performance_data)
        }
    
    def _analyze_engagement_trends(self, user: User, period_days: int) -> Dict[str, Any]:
        """Analyze engagement-specific trends"""
        start_date = timezone.now() - timedelta(days=period_days)
        
        # Get daily activity counts
        daily_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date
        ).extra(
            select={'date': 'date(updated_at)'}
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        if not daily_activities:
            return {
                'engagement_available': False,
                'message': 'No engagement data available'
            }
        
        # Calculate engagement metrics
        total_days = len(daily_activities)
        active_days = sum(1 for day in daily_activities if day['count'] > 0)
        consistency_rate = (active_days / max(total_days, 1)) * 100
        
        # Weekly patterns
        weekly_pattern = self._analyze_weekly_patterns(user, start_date)
        
        # Engagement level classification
        avg_daily_activities = sum(day['count'] for day in daily_activities) / total_days
        engagement_level = 'high' if avg_daily_activities >= 3 else 'moderate' if avg_daily_activities >= 1 else 'low'
        
        return {
            'engagement_available': True,
            'engagement_level': engagement_level,
            'consistency_rate': round(consistency_rate, 2),
            'active_days': active_days,
            'total_days': total_days,
            'average_daily_activities': round(avg_daily_activities, 2),
            'peak_activity_day': max(daily_activities, key=lambda x: x['count'])['date'],
            'weekly_pattern': weekly_pattern,
            'engagement_trend': self._calculate_engagement_trend(daily_activities),
            'recommended_daily_target': self._recommend_daily_target(user)
        }
    
    def _analyze_learning_patterns(self, user: User) -> Dict[str, Any]:
        """Analyze user's learning patterns and preferences"""
        # Get user's activity patterns
        activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=30)
        )
        
        if not activities.exists():
            return {
                'patterns_available': False,
                'message': 'Insufficient data for pattern analysis'
            }
        
        # Analyze time patterns
        hour_distribution = {}
        day_distribution = {}
        
        for activity in activities:
            hour = activity.updated_at.hour
            day = activity.updated_at.strftime('%A')
            
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
            day_distribution[day] = day_distribution.get(day, 0) + 1
        
        # Find preferred learning times
        preferred_hour = max(hour_distribution, key=hour_distribution.get) if hour_distribution else None
        preferred_day = max(day_distribution, key=day_distribution.get) if day_distribution else None
        
        # Learning session patterns
        session_patterns = self._analyze_session_patterns(user)
        
        return {
            'patterns_available': True,
            'preferred_learning_hour': preferred_hour,
            'preferred_learning_day': preferred_day,
            'hour_distribution': hour_distribution,
            'day_distribution': day_distribution,
            'session_patterns': session_patterns,
            'learning_style_indicators': self._get_learning_style_indicators(user),
            'productivity_peaks': self._identify_productivity_peaks(user)
        }
    
    def _analyze_predictive_trends(self, user: User, period_days: int) -> Dict[str, Any]:
        """Analyze trends for predictive insights"""
        # Get current trends
        current_trend = self._analyze_learning_trends(user, period_days, 'comprehensive')
        
        # Project future trends
        projected_activities = self._project_future_activities(user, current_trend)
        
        # Risk factors analysis
        risk_factors = self._analyze_risk_factors(user)
        
        return {
            'projections': projected_activities,
            'risk_factors': risk_factors,
            'confidence_level': self._calculate_prediction_confidence(user, period_days),
            'key_insights': self._generate_predictive_insights(user, current_trend)
        }
    
    def _generate_trend_insights(self, user: User, trend_data: Dict[str, Any]) -> List[str]:
        """Generate insights based on trend analysis"""
        insights = []
        
        trend_direction = trend_data.get('trend_direction')
        completion_rate = trend_data.get('completion_rate', 0)
        
        if trend_direction == 'improving':
            insights.append("Your learning momentum is increasing - great work!")
        elif trend_direction == 'declining':
            insights.append("Learning activity has decreased recently - consider adjusting your schedule")
        
        if completion_rate >= 80:
            insights.append("Excellent completion rate - you're efficiently finishing what you start")
        elif completion_rate >= 60:
            insights.append("Good completion rate, but there's room to improve")
        else:
            insights.append("Consider focusing on completing started activities")
        
        return insights
    
    def _generate_trend_recommendations(self, user: User, trend_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on trend analysis"""
        recommendations = []
        
        trend_direction = trend_data.get('trend_direction')
        period_summary = trend_data.get('period_summary', {})
        
        if trend_direction == 'declining':
            recommendations.append("Set a specific daily learning goal to rebuild momentum")
            recommendations.append("Consider breaking larger tasks into smaller, manageable chunks")
        elif trend_direction == 'stable':
            recommendations.append("You're maintaining consistent progress - try to gradually increase intensity")
        
        consistency_score = period_summary.get('consistency_score', 0)
        if consistency_score < 50:
            recommendations.append("Focus on developing a more consistent daily learning routine")
        
        return recommendations
    
    def _calculate_moving_averages(self, scores: List[float], window: int = 5) -> List[float]:
        """Calculate moving averages for scores"""
        if len(scores) < window:
            return scores
        
        moving_averages = []
        for i in range(len(scores) - window + 1):
            window_scores = scores[i:i + window]
            moving_averages.append(sum(window_scores) / window)
        
        return moving_averages
    
    def _calculate_trend_slope(self, values: List[float]) -> float:
        """Calculate simple linear trend slope"""
        if len(values) < 2:
            return 0
        
        n = len(values)
        x_values = list(range(n))
        
        # Calculate slope using least squares method
        x_mean = sum(x_values) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0
    
    def _calculate_consistency_score(self, activities_data: List[Dict], period_days: int) -> float:
        """Calculate consistency score based on daily activity distribution"""
        if not activities_data:
            return 0
        
        # Calculate coefficient of variation
        activity_counts = [day['count'] for day in activities_data]
        mean_activities = sum(activity_counts) / len(activity_counts)
        
        if mean_activities == 0:
            return 0
        
        variance = sum((count - mean_activities) ** 2 for count in activity_counts) / len(activity_counts)
        standard_deviation = variance ** 0.5
        
        coefficient_of_variation = standard_deviation / mean_activities
        
        # Convert to consistency score (0-100, higher is better)
        consistency_score = max(0, 100 - (coefficient_of_variation * 100))
        
        return round(consistency_score, 2)
    
    def _get_performance_rating(self, scores: List[float]) -> str:
        """Get overall performance rating"""
        if not scores:
            return 'insufficient_data'
        
        avg_score = np.mean(scores)
        
        if avg_score >= 90:
            return 'excellent'
        elif avg_score >= 80:
            return 'good'
        elif avg_score >= 70:
            return 'satisfactory'
        elif avg_score >= 60:
            return 'needs_improvement'
        else:
            return 'poor'
    
    def _identify_improvement_areas(self, user: User, performance_data) -> List[str]:
        """Identify areas for improvement based on performance data"""
        # This would analyze specific modules or topics
        # For now, return generic improvement areas
        
        return [
            "Focus on practice exercises",
            "Review fundamental concepts",
            "Increase study time consistency"
        ]
    
    def _analyze_weekly_patterns(self, user: User, start_date) -> Dict[str, Any]:
        """Analyze weekly learning patterns"""
        activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date
        )
        
        if not activities.exists():
            return {'pattern_available': False}
        
        # Group by day of week
        day_counts = {}
        for activity in activities:
            day_name = activity.updated_at.strftime('%A')
            day_counts[day_name] = day_counts.get(day_name, 0) + 1
        
        return {
            'pattern_available': True,
            'day_distribution': day_counts,
            'most_active_day': max(day_counts, key=day_counts.get) if day_counts else None,
            'least_active_day': min(day_counts, key=day_counts.get) if day_counts else None
        }
    
    def _calculate_engagement_trend(self, daily_activities: List[Dict]) -> str:
        """Calculate overall engagement trend"""
        if len(daily_activities) < 7:
            return 'insufficient_data'
        
        recent_activity = sum(day['count'] for day in daily_activities[-7:])
        previous_activity = sum(day['count'] for day in daily_activities[-14:-7]) if len(daily_activities) >= 14 else recent_activity
        
        if recent_activity > previous_activity * 1.2:
            return 'increasing'
        elif recent_activity < previous_activity * 0.8:
            return 'decreasing'
        else:
            return 'stable'
    
    def _recommend_daily_target(self, user: User) -> int:
        """Recommend daily activity target"""
        # Get user's average daily activity over last 30 days
        recent_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=30)
        )
        
        if not recent_activities.exists():
            return 2  # Default recommendation
        
        daily_averages = {}
        for activity in recent_activities:
            date_key = activity.updated_at.date()
            daily_averages[date_key] = daily_averages.get(date_key, 0) + 1
        
        avg_daily = sum(daily_averages.values()) / len(daily_averages)
        
        # Recommend 20% more than current average
        recommended = int(avg_daily * 1.2)
        
        return max(1, min(recommended, 5))  # Between 1 and 5 activities per day
    
    def _analyze_session_patterns(self, user: User) -> Dict[str, Any]:
        """Analyze learning session patterns"""
        # This would analyze consecutive activities to identify sessions
        # For now, return basic session data
        
        return {
            'average_session_length': 45,  # minutes
            'sessions_per_day': 2,
            'peak_session_times': [10, 14, 19]  # 10am, 2pm, 7pm
        }
    
    def _get_learning_style_indicators(self, user: User) -> Dict[str, Any]:
        """Get learning style indicators based on activity patterns"""
        # This would analyze preferred learning types
        # For now, return basic indicators
        
        return {
            'visual_learner_score': 75,
            'auditory_learner_score': 60,
            'kinesthetic_learner_score': 80,
            'preferred_style': 'kinesthetic'
        }
    
    def _identify_productivity_peaks(self, user: User) -> List[Dict[str, Any]]:
        """Identify times when user is most productive"""
        activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=30)
        )
        
        hour_performance = {}
        
        for activity in activities:
            hour = activity.updated_at.hour
            if hour not in hour_performance:
                hour_performance[hour] = []
            
            # Use score if available, otherwise give default score
            score = activity.score if activity.score else 70
            hour_performance[hour].append(score)
        
        # Calculate average performance by hour
        peak_hours = []
        for hour, scores in hour_performance.items():
            if len(scores) >= 3:  # Need at least 3 data points
                avg_score = sum(scores) / len(scores)
                peak_hours.append({
                    'hour': hour,
                    'average_score': round(avg_score, 2),
                    'activity_count': len(scores)
                })
        
        # Sort by average score
        peak_hours.sort(key=lambda x: x['average_score'], reverse=True)
        
        return peak_hours[:3]  # Top 3 peak hours
    
    def _project_future_activities(self, user: User, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """Project future learning activities"""
        current_daily_avg = trend_data.get('period_summary', {}).get('average_daily_activities', 0)
        
        # Simple projection based on current trend
        projections = {
            'next_7_days': round(current_daily_avg * 7 * 1.1),  # 10% increase
            'next_30_days': round(current_daily_avg * 30 * 1.05),  # 5% increase
            'confidence': 'medium'
        }
        
        return projections
    
    def _analyze_risk_factors(self, user: User) -> List[str]:
        """Analyze risk factors for learning success"""
        risks = []
        
        # Check engagement level
        recent_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if recent_activities < 2:
            risks.append("Low engagement in recent days")
        
        # Check performance consistency
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=14),
            score__isnull=False
        )
        
        if recent_assessments.count() >= 3:
            scores = [a.score for a in recent_assessments]
            if np.std(scores) > 20:  # High variance
                risks.append("Inconsistent performance")
        
        return risks
    
    def _calculate_prediction_confidence(self, user: User, period_days: int) -> str:
        """Calculate confidence level for predictions"""
        required_data_points = max(10, period_days // 3)
        
        recent_activities = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(days=period_days)
        ).count()
        
        if recent_activities >= required_data_points * 2:
            return 'high'
        elif recent_activities >= required_data_points:
            return 'medium'
        else:
            return 'low'
    
    def _generate_predictive_insights(self, user: User, trend_data: Dict[str, Any]) -> List[str]:
        """Generate insights for predictive analysis"""
        insights = []
        
        trend_direction = trend_data.get('trend_direction')
        
        if trend_direction == 'improving':
            insights.append("Current trajectory suggests continued progress improvement")
        elif trend_direction == 'declining':
            insights.append("Early intervention recommended to prevent further decline")
        
        return insights


# Import numpy for statistical calculations
import numpy as np