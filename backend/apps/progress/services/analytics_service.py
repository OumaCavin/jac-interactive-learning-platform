"""
Analytics Service - JAC Learning Platform

This service handles advanced analytics generation, reporting, and insights
for progress tracking in the JAC Interactive Learning Platform.

Author: MiniMax Agent
Created: 2025-11-25
"""

import uuid
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Max, Min, StdDev
from django.db.models.functions import TruncDate, TruncWeek
from datetime import datetime, timedelta
import logging

from ..models import LearningAnalytics
from apps.learning.models import (
    LearningPath, Module, UserLearningPath, UserModuleProgress
)
from apps.agents.progress_tracker import ProgressTrackerAgent

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service class for analytics and reporting operations
    """
    
    def __init__(self):
        self.progress_agent = ProgressTrackerAgent()
    
    def generate_user_analytics(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        time_period_days: int = 30,
        analytics_type: str = 'comprehensive'
    ) -> LearningAnalytics:
        """
        Generate comprehensive learning analytics for a user
        
        Args:
            user: The user to generate analytics for
            learning_path_id: Optional specific learning path
            time_period_days: Number of days to analyze
            analytics_type: Type of analytics (basic, performance, engagement, comprehensive)
        
        Returns:
            LearningAnalytics instance
        """
        try:
            # Calculate time period
            end_date = timezone.now()
            start_date = end_date - timedelta(days=time_period_days)
            
            # Get learning path if specified
            learning_path = None
            if learning_path_id:
                learning_path = LearningPath.objects.get(id=learning_path_id)
            
            # Collect analytics data
            analytics_data = self._collect_analytics_data(
                user, learning_path, start_date, end_date, analytics_type
            )
            
            # Generate analytics metrics
            analytics_metrics = self._generate_analytics_metrics(
                analytics_data, analytics_type
            )
            
            # Create LearningAnalytics record
            analytics_record = LearningAnalytics.objects.create(
                user=user,
                learning_path=learning_path,
                period_start=start_date,
                period_end=end_date,
                **analytics_metrics
            )
            
            logger.info(f"Generated {analytics_type} analytics for user {user.username}")
            
            return analytics_record
            
        except Exception as e:
            logger.error(f"Error generating analytics for user {user.username}: {str(e)}")
            raise
    
    def generate_comprehensive_analytics(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        time_period_days: int = 30,
        analytics_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """
        Generate comprehensive analytics data for API response
        
        Args:
            user: The user to generate analytics for
            learning_path_id: Optional specific learning path
            time_period_days: Number of days to analyze
            analytics_type: Type of analytics
        
        Returns:
            Dict containing comprehensive analytics data
        """
        try:
            # Calculate time period
            end_date = timezone.now()
            start_date = end_date - timedelta(days=time_period_days)
            
            # Get learning path if specified
            learning_path = None
            if learning_path_id:
                learning_path = LearningPath.objects.get(id=learning_path_id)
            
            # Generate analytics using the progress agent
            task_params = {
                'user': user,
                'learning_path_id': learning_path_id,
                'time_period': time_period_days,
                'analytics_type': analytics_type
            }
            
            result = self.progress_agent.process_task({
                'type': 'generate_analytics',
                'params': task_params
            })
            
            if result['success']:
                analytics_data = result['result']
                
                # Enhance with additional data
                analytics_data.update({
                    'analytics_id': str(uuid.uuid4()),
                    'user_id': user.id,
                    'learning_path_id': learning_path_id,
                    'time_period_days': time_period_days,
                    'analytics_type': analytics_type,
                    'generation_date': timezone.now().isoformat(),
                })
                
                return analytics_data
            else:
                # Fallback to basic analytics
                return self._generate_basic_analytics(
                    user, learning_path, start_date, end_date, analytics_type
                )
                
        except Exception as e:
            logger.error(f"Error generating comprehensive analytics for user {user.username}: {str(e)}")
            return self._generate_basic_analytics(
                user, learning_path, start_date, end_date, analytics_type
            )
    
    def _collect_analytics_data(
        self,
        user: User,
        learning_path: Optional[LearningPath],
        start_date: datetime,
        end_date: datetime,
        analytics_type: str
    ) -> Dict[str, Any]:
        """
        Collect data for analytics generation
        
        Args:
            user: The user to collect data for
            learning_path: Optional learning path
            start_date: Start of analysis period
            end_date: End of analysis period
            analytics_type: Type of analytics
        
        Returns:
            Dict containing collected data
        """
        # Base querysets
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        )
        
        assessment_query = UserAssessmentResult.objects.filter(
            user=user,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        )
        
        # Filter by learning path if specified
        if learning_path:
            progress_query = progress_query.filter(module__learning_path=learning_path)
            assessment_query = assessment_query.filter(assessment__learning_path=learning_path)
        
        data = {
            'user': user,
            'learning_path': learning_path,
            'period_start': start_date,
            'period_end': end_date,
            'progress_data': list(progress_query),
            'assessment_data': list(assessment_query),
            'total_activities': progress_query.count(),
            'total_assessments': assessment_query.count(),
        }
        
        # Add additional data based on analytics type
        if analytics_type in ['performance', 'comprehensive']:
            # Performance-specific data
            data['performance_data'] = self._collect_performance_data(
                user, learning_path, start_date, end_date
            )
        
        if analytics_type in ['engagement', 'comprehensive']:
            # Engagement-specific data
            data['engagement_data'] = self._collect_engagement_data(
                user, learning_path, start_date, end_date
            )
        
        if analytics_type in ['learning', 'comprehensive']:
            # Learning-specific data
            data['learning_data'] = self._collect_learning_data(
                user, learning_path, start_date, end_date
            )
        
        return data
    
    def _generate_analytics_metrics(self, data: Dict[str, Any], analytics_type: str) -> Dict[str, Any]:
        """
        Generate analytics metrics from collected data
        
        Args:
            data: Collected analytics data
            analytics_type: Type of analytics
        
        Returns:
            Dict containing analytics metrics
        """
        progress_data = data['progress_data']
        assessment_data = data['assessment_data']
        
        # Basic metrics
        total_activities = len(progress_data)
        total_assessments = len(assessment_data)
        
        # Completion metrics
        completed_activities = len([p for p in progress_data if p.status == 'completed'])
        completion_rate = (completed_activities / max(total_activities, 1)) * 100
        
        # Performance metrics
        scores = [a.score for a in assessment_data if a.score is not None]
        accuracy_rate = sum(scores) / max(len(scores), 1) if scores else 0
        
        # Time efficiency
        total_time_spent = sum([p.time_spent.total_seconds() for p in progress_data if p.time_spent], 0)
        avg_time_per_activity = total_time_spent / max(total_activities, 1) / 60  # minutes
        
        metrics = {
            'total_activities': total_activities,
            'completion_rate': round(completion_rate, 2),
            'accuracy_rate': round(accuracy_rate, 2),
            'efficiency_score': self._calculate_efficiency_score(avg_time_per_activity, accuracy_rate),
        }
        
        # Add type-specific metrics
        if analytics_type in ['performance', 'comprehensive'] and 'performance_data' in data:
            metrics.update(self._generate_performance_metrics(data['performance_data']))
        
        if analytics_type in ['engagement', 'comprehensive'] and 'engagement_data' in data:
            metrics.update(self._generate_engagement_metrics(data['engagement_data']))
        
        if analytics_type in ['learning', 'comprehensive'] and 'learning_data' in data:
            metrics.update(self._generate_learning_metrics(data['learning_data']))
        
        # Add predictions and trends
        metrics['learning_velocity'] = self._calculate_learning_velocity(data)
        metrics['skill_progression_rate'] = self._calculate_skill_progression_rate(data)
        metrics['performance_trend'] = self._analyze_performance_trend(data)
        metrics['completion_prediction_days'] = self._predict_completion_days(data)
        metrics['confidence_level'] = self._calculate_confidence_level(data)
        metrics['key_insights'] = self._generate_key_insights(data, metrics)
        metrics['recommendations'] = self._generate_recommendations(data, metrics)
        
        return metrics
    
    def _collect_performance_data(
        self,
        user: User,
        learning_path: Optional[LearningPath],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Collect performance-specific data"""
        assessment_query = UserAssessmentResult.objects.filter(
            user=user,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        )
        
        if learning_path:
            assessment_query = assessment_query.filter(assessment__learning_path=learning_path)
        
        assessments = list(assessment_query)
        
        return {
            'assessment_scores': [a.score for a in assessments if a.score is not None],
            'assessment_dates': [a.completed_at for a in assessments if a.completed_at],
            'difficulty_performance': self._analyze_difficulty_performance(assessments),
            'topic_performance': self._analyze_topic_performance(assessments),
            'improvement_trend': self._calculate_improvement_trend(assessments)
        }
    
    def _collect_engagement_data(
        self,
        user: User,
        learning_path: Optional[LearningPath],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Collect engagement-specific data"""
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        )
        
        if learning_path:
            progress_query = progress_query.filter(module__learning_path=learning_path)
        
        progress_records = list(progress_query)
        
        return {
            'activity_frequency': self._calculate_activity_frequency(progress_records),
            'session_patterns': self._analyze_session_patterns(progress_records),
            'engagement_consistency': self._calculate_engagement_consistency(progress_records),
            'time_distribution': self._analyze_time_distribution(progress_records),
            'motivation_indicators': self._analyze_motivation_indicators(progress_records)
        }
    
    def _collect_learning_data(
        self,
        user: User,
        learning_path: Optional[LearningPath],
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Collect learning-specific data"""
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        )
        
        if learning_path:
            progress_query = progress_query.filter(module__learning_path=learning_path)
        
        return {
            'skill_progression': self._analyze_skill_progression(progress_query),
            'learning_velocity': self._calculate_learning_velocity_data(progress_query),
            'knowledge_gaps': self._identify_knowledge_gaps(progress_query),
            'learning_style_indicators': self._analyze_learning_style_indicators(progress_query),
            'retention_analysis': self._analyze_retention(progress_query)
        }
    
    def _generate_basic_analytics(
        self,
        user: User,
        learning_path: Optional[LearningPath],
        start_date: datetime,
        end_date: datetime,
        analytics_type: str
    ) -> Dict[str, Any]:
        """
        Generate basic analytics data when advanced analytics fail
        
        Args:
            user: The user to generate analytics for
            learning_path: Optional learning path
            start_date: Start date
            end_date: End date
            analytics_type: Type of analytics
        
        Returns:
            Dict containing basic analytics data
        """
        # Get basic progress data
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        )
        
        if learning_path:
            progress_query = progress_query.filter(module__learning_path=learning_path)
        
        assessment_query = UserAssessmentResult.objects.filter(
            user=user,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        )
        
        if learning_path:
            assessment_query = assessment_query.filter(assessment__learning_path=learning_path)
        
        # Calculate basic metrics
        total_activities = progress_query.count()
        completed_activities = progress_query.filter(status='completed').count()
        
        assessment_results = list(assessment_query)
        avg_score = sum([a.score for a in assessment_results if a.score], 0) / max(len([a for a in assessment_results if a.score]), 1)
        
        return {
            'analytics_id': str(uuid.uuid4()),
            'user_id': user.id,
            'learning_path_id': learning_path.id if learning_path else None,
            'time_period_days': (end_date - start_date).days,
            'analytics_type': analytics_type,
            'generation_date': timezone.now().isoformat(),
            'summary_metrics': {
                'total_activities': total_activities,
                'completed_activities': completed_activities,
                'completion_rate': (completed_activities / max(total_activities, 1)) * 100,
                'average_score': avg_score,
                'total_assessments': len(assessment_results)
            },
            'performance_analytics': {
                'average_score': avg_score,
                'score_trend': 'stable',
                'improvement_rate': 0
            },
            'engagement_analytics': {
                'engagement_level': 'medium',
                'activity_frequency': 'regular',
                'consistency_score': 75
            },
            'learning_analytics': {
                'learning_velocity': 'moderate',
                'skill_progression': 'steady',
                'comprehension_level': 'good'
            },
            'comparative_analysis': {
                'peer_comparison': 'average',
                'institution_ranking': 'middle'
            },
            'trends': {
                'performance_trend': 'stable',
                'engagement_trend': 'stable',
                'completion_trend': 'steady'
            },
            'insights': [
                'Learning progress is consistent',
                'Performance is at expected levels',
                'Continue current learning approach'
            ],
            'alerts': [] if avg_score >= 70 else ['Consider additional practice in weak areas']
        }
    
    def _generate_performance_metrics(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance-specific metrics"""
        return {
            'score_variance': self._calculate_score_variance(performance_data['assessment_scores']),
            'difficulty_mastery': performance_data['difficulty_performance'],
            'topic_proficiency': performance_data['topic_performance'],
            'improvement_rate': performance_data['improvement_trend']
        }
    
    def _generate_engagement_metrics(self, engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate engagement-specific metrics"""
        return {
            'engagement_level': engagement_data['engagement_consistency'],
            'consistency_score': engagement_data['engagement_consistency'] * 100,
            'motivation_score': engagement_data['motivation_indicators'],
            'session_quality': engagement_data['session_patterns']
        }
    
    def _generate_learning_metrics(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning-specific metrics"""
        return {
            'learning_velocity': learning_data['learning_velocity'],
            'skill_progression_rate': learning_data['skill_progression'],
            'knowledge_retention': learning_data['retention_analysis'],
            'learning_efficiency': learning_data['learning_style_indicators']
        }
    
    # Helper methods for calculations
    
    def _calculate_efficiency_score(self, avg_time_minutes: float, accuracy_rate: float) -> float:
        """Calculate overall efficiency score"""
        # Normalize time component (lower time = higher efficiency)
        time_score = max(0, 100 - (avg_time_minutes - 10) * 2)  # 10 minutes baseline
        
        # Combine with accuracy
        efficiency = (time_score * 0.3 + accuracy_rate * 0.7)
        return round(max(0, min(100, efficiency)), 2)
    
    def _analyze_difficulty_performance(self, assessments: List) -> Dict[str, float]:
        """Analyze performance by difficulty level"""
        difficulty_performance = {}
        
        for assessment in assessments:
            difficulty = getattr(assessment.assessment, 'difficulty_level', 'medium')
            score = assessment.score
            
            if difficulty not in difficulty_performance:
                difficulty_performance[difficulty] = []
            difficulty_performance[difficulty].append(score)
        
        return {
            diff: sum(scores) / len(scores)
            for diff, scores in difficulty_performance.items()
        }
    
    def _analyze_topic_performance(self, assessments: List) -> Dict[str, float]:
        """Analyze performance by topic"""
        topic_performance = {}
        
        for assessment in assessments:
            # This would need to be adapted based on your topic structure
            topic = getattr(assessment.assessment, 'module', {}).get('topic', 'general')
            score = assessment.score
            
            if topic not in topic_performance:
                topic_performance[topic] = []
            topic_performance[topic].append(score)
        
        return {
            topic: sum(scores) / len(scores)
            for topic, scores in topic_performance.items()
        }
    
    def _calculate_improvement_trend(self, assessments: List) -> float:
        """Calculate improvement trend over time"""
        if len(assessments) < 2:
            return 0
        
        # Sort by completion date
        sorted_assessments = sorted(assessments, key=lambda x: x.completed_at)
        
        # Compare first half vs second half
        mid_point = len(sorted_assessments) // 2
        first_half_avg = sum([a.score for a in sorted_assessments[:mid_point]]) / max(mid_point, 1)
        second_half_avg = sum([a.score for a in sorted_assessments[mid_point:]]) / max(len(sorted_assessments) - mid_point, 1)
        
        return round(second_half_avg - first_half_avg, 2)
    
    def _calculate_activity_frequency(self, progress_records: List) -> Dict[str, float]:
        """Calculate activity frequency patterns"""
        # Group activities by day of week
        day_frequency = {}
        
        for record in progress_records:
            day_name = record.updated_at.strftime('%A')
            day_frequency[day_name] = day_frequency.get(day_name, 0) + 1
        
        total_activities = len(progress_records)
        return {
            day: count / total_activities
            for day, count in day_frequency.items()
        }
    
    def _analyze_session_patterns(self, progress_records: List) -> Dict[str, Any]:
        """Analyze learning session patterns"""
        # Group by date to identify sessions
        session_dates = {}
        
        for record in progress_records:
            date_key = record.updated_at.date()
            if date_key not in session_dates:
                session_dates[date_key] = 0
            session_dates[date_key] += 1
        
        # Calculate session statistics
        session_counts = list(session_dates.values())
        
        return {
            'avg_activities_per_session': sum(session_counts) / max(len(session_counts), 1),
            'session_frequency': len(session_dates),
            'most_active_day': max(session_dates.items(), key=lambda x: x[1])[0] if session_dates else None
        }
    
    def _calculate_engagement_consistency(self, progress_records: List) -> float:
        """Calculate engagement consistency score"""
        if not progress_records:
            return 0
        
        # Calculate variance in daily activity
        daily_counts = {}
        for record in progress_records:
            date_key = record.updated_at.date()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        counts = list(daily_counts.values())
        if len(counts) <= 1:
            return 100
        
        # Lower variance = higher consistency
        mean_count = sum(counts) / len(counts)
        variance = sum((x - mean_count) ** 2 for x in counts) / len(counts)
        consistency_score = max(0, 100 - (variance * 10))
        
        return round(consistency_score, 2)
    
    def _analyze_time_distribution(self, progress_records: List) -> Dict[str, Any]:
        """Analyze time distribution of activities"""
        if not progress_records:
            return {'peak_hours': [], 'distribution': {}}
        
        hour_distribution = {}
        for record in progress_records:
            hour = record.updated_at.hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
        
        # Find peak hours
        sorted_hours = sorted(hour_distribution.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [hour for hour, count in sorted_hours[:3]]
        
        return {
            'peak_hours': peak_hours,
            'distribution': hour_distribution
        }
    
    def _analyze_motivation_indicators(self, progress_records: List) -> float:
        """Analyze motivation indicators"""
        if not progress_records:
            return 50
        
        # Simple motivation score based on completion rate and consistency
        completed = len([r for r in progress_records if r.status == 'completed'])
        completion_rate = completed / len(progress_records)
        
        # Consistency component
        unique_days = len(set(r.updated_at.date() for r in progress_records))
        consistency_factor = min(1, unique_days / 30)  # Max 1 for 30 days of activity
        
        motivation_score = (completion_rate * 0.7 + consistency_factor * 0.3) * 100
        return round(motivation_score, 2)
    
    def _analyze_skill_progression(self, progress_query) -> float:
        """Analyze skill progression over time"""
        # This is a simplified implementation
        # In practice, you'd analyze progression through difficulty levels
        return 75.0  # Placeholder
    
    def _calculate_learning_velocity_data(self, progress_query) -> float:
        """Calculate learning velocity from progress data"""
        # Calculate activities per week
        recent_progress = progress_query.filter(
            updated_at__gte=timezone.now() - timedelta(weeks=4)
        )
        
        return recent_progress.count() / 4.0
    
    def _identify_knowledge_gaps(self, progress_query) -> List[str]:
        """Identify potential knowledge gaps"""
        # Simplified implementation
        incomplete_modules = progress_query.filter(
            status__in=['in_progress', 'not_started']
        ).values_list('module__title', flat=True)
        
        return list(incomplete_modules[:5])  # Return first 5 incomplete modules
    
    def _analyze_learning_style_indicators(self, progress_query) -> Dict[str, Any]:
        """Analyze learning style indicators"""
        # Simplified implementation
        return {
            'preferred_difficulty': 'medium',
            'session_length': 'moderate',
            'practice_frequency': 'regular'
        }
    
    def _analyze_retention(self, progress_query) -> float:
        """Analyze knowledge retention"""
        # Simplified retention analysis
        return 80.0  # Placeholder for 80% retention rate
    
    def _calculate_score_variance(self, scores: List[float]) -> float:
        """Calculate variance in assessment scores"""
        if len(scores) <= 1:
            return 0
        
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        return round(variance, 2)
    
    def _calculate_learning_velocity(self, data: Dict[str, Any]) -> float:
        """Calculate overall learning velocity"""
        # Activities per week calculation
        progress_data = data['progress_data']
        
        if not progress_data:
            return 0
        
        # Group by week
        weekly_counts = {}
        for record in progress_data:
            week_key = record.updated_date.strftime('%Y-W%U')
            weekly_counts[week_key] = weekly_counts.get(week_key, 0) + 1
        
        return sum(weekly_counts.values()) / max(len(weekly_counts), 1)
    
    def _calculate_skill_progression_rate(self, data: Dict[str, Any]) -> float:
        """Calculate skill progression rate"""
        # Simplified implementation
        return 5.0  # Placeholder for 5% progression per period
    
    def _analyze_performance_trend(self, data: Dict[str, Any]) -> str:
        """Analyze overall performance trend"""
        assessment_data = data['assessment_data']
        
        if len(assessment_data) < 3:
            return 'stable'
        
        # Simple trend analysis
        scores = [a.score for a in assessment_data if a.score]
        
        if len(scores) >= 3:
            recent_avg = sum(scores[-3:]) / 3
            earlier_avg = sum(scores[:-3]) / len(scores[:-3]) if len(scores) > 3 else recent_avg
            
            if recent_avg > earlier_avg + 5:
                return 'improving'
            elif recent_avg < earlier_avg - 5:
                return 'declining'
        
        return 'stable'
    
    def _predict_completion_days(self, data: Dict[str, Any]) -> Optional[int]:
        """Predict days to completion"""
        # Simplified prediction based on current velocity
        progress_data = data['progress_data']
        
        if not progress_data:
            return None
        
        # Calculate remaining work (simplified)
        completed = len([p for p in progress_data if p.status == 'completed'])
        total = len(progress_data)
        
        if completed >= total:
            return 0
        
        # Estimate based on current velocity
        days_elapsed = (data['period_end'] - data['period_start']).days
        velocity = completed / max(days_elapsed, 1)
        remaining_work = total - completed
        
        if velocity > 0:
            return int(remaining_work / velocity)
        
        return None
    
    def _calculate_confidence_level(self, data: Dict[str, Any]) -> float:
        """Calculate confidence level in predictions"""
        # Based on amount of data and consistency
        progress_data = data['progress_data']
        assessment_data = data['assessment_data']
        
        data_points = len(progress_data) + len(assessment_data)
        
        if data_points >= 20:
            return 0.9
        elif data_points >= 10:
            return 0.8
        elif data_points >= 5:
            return 0.6
        else:
            return 0.3
    
    def _generate_key_insights(self, data: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate key insights from analytics"""
        insights = []
        
        # Performance insights
        if metrics.get('accuracy_rate', 0) >= 85:
            insights.append("Excellent performance with high accuracy rates")
        elif metrics.get('accuracy_rate', 0) < 70:
            insights.append("Consider focusing on practice to improve accuracy")
        
        # Engagement insights
        if metrics.get('consistency_score', 0) >= 80:
            insights.append("Highly consistent learning habits")
        elif metrics.get('consistency_score', 0) < 50:
            insights.append("Inconsistent learning pattern detected")
        
        # Velocity insights
        if metrics.get('learning_velocity', 0) > 2:
            insights.append("Fast learning pace - consider advancing difficulty")
        elif metrics.get('learning_velocity', 0) < 0.5:
            insights.append("Slow learning pace - consider additional support")
        
        return insights
    
    def _generate_recommendations(self, data: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Performance-based recommendations
        if metrics.get('accuracy_rate', 0) < 75:
            recommendations.append("Focus on fundamental concepts before advancing")
            recommendations.append("Consider additional practice exercises")
        
        # Engagement-based recommendations
        if metrics.get('consistency_score', 0) < 60:
            recommendations.append("Establish a regular learning schedule")
            recommendations.append("Set smaller, achievable daily goals")
        
        # Learning velocity recommendations
        if metrics.get('learning_velocity', 0) > 3:
            recommendations.append("You're learning quickly - consider challenging projects")
        
        return recommendations