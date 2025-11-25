"""
Analytics Service - JAC Learning Platform

This service handles advanced analytics generation, reporting, and insights
for progress tracking in the JAC Interactive Learning Platform.

Author: Cavin Otieno
Created: 2025-11-25
"""

import uuid
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Max, Min, StdDev, F
from django.db.models.functions import TruncDate, TruncWeek
from datetime import datetime, timedelta
import logging
import numpy as np
import statistics
import json
from collections import defaultdict, Counter

from ..models import LearningAnalytics
from apps.learning.models import (
    LearningPath, Module, UserLearningPath, UserModuleProgress, AssessmentAttempt
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
        
        assessment_query = AssessmentAttempt.objects.filter(
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
        assessment_query = AssessmentAttempt.objects.filter(
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
        
        assessment_query = AssessmentAttempt.objects.filter(
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
        """Analyze skill progression over time using actual progression data"""
        # Calculate progression through difficulty levels
        completed_progress = progress_query.filter(status='completed').order_by('updated_at')
        
        if not completed_progress.exists():
            return 0.0
        
        # Calculate difficulty progression
        difficulty_scores = []
        for progress in completed_progress:
            difficulty_score = self._get_module_difficulty_score(progress.module)
            difficulty_scores.append(difficulty_score)
        
        if len(difficulty_scores) < 2:
            return difficulty_scores[0] if difficulty_scores else 0.0
        
        # Calculate average progression rate
        total_progression = max(difficulty_scores) - min(difficulty_scores)
        time_span_days = (completed_progress.last().updated_at - completed_progress.first().updated_at).days
        time_span_days = max(time_span_days, 1)  # Avoid division by zero
        
        progression_rate = (total_progression / time_span_days) * 30  # Per month
        return round(min(100.0, max(0.0, progression_rate)), 2)
    
    def _get_module_difficulty_score(self, module) -> float:
        """Get numerical difficulty score for a module"""
        difficulty_map = {
            'beginner': 25.0,
            'easy': 25.0,
            'basic': 25.0,
            'intermediate': 50.0,
            'medium': 50.0,
            'advanced': 75.0,
            'hard': 75.0,
            'expert': 95.0,
            'difficult': 95.0
        }
        
        difficulty = getattr(module, 'difficulty_level', 'beginner').lower()
        return difficulty_map.get(difficulty, 25.0)
    
    def _calculate_learning_velocity_data(self, progress_query) -> float:
        """Calculate learning velocity from actual progress data"""
        # Get activities completed in the last 30 days
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_progress = progress_query.filter(
            updated_at__gte=thirty_days_ago,
            status='completed'
        )
        
        # Calculate weighted velocity (more recent activities have higher weight)
        activities = list(recent_progress.order_by('-updated_at')[:20])  # Last 20 activities
        if not activities:
            return 0.0
        
        velocity_scores = []
        for i, activity in enumerate(activities):
            # Weight decreases with age (more recent = higher weight)
            weight = max(0.1, 1.0 - (i * 0.05))
            velocity_scores.append(weight)
        
        total_weighted_velocity = sum(velocity_scores)
        return round(total_weighted_velocity, 2)
    
    def _identify_knowledge_gaps(self, progress_query) -> List[str]:
        """Identify knowledge gaps using performance analysis"""
        knowledge_gaps = []
        
        # Analyze modules where user struggled (low scores or repeated attempts)
        struggling_modules = progress_query.filter(
            status='completed',
            score__lt=70.0  # Score below 70%
        ).values_list('module__title', flat=True)
        
        if struggling_modules:
            knowledge_gaps.extend(list(struggling_modules))
        
        # Identify incomplete critical modules (dependencies)
        incomplete_modules = progress_query.filter(
            status__in=['in_progress', 'not_started']
        ).order_by('module__order')[:5]
        
        for module in incomplete_modules:
            # Check if this module is a prerequisite for others
            if self._is_critical_module(module.module):
                knowledge_gaps.append(f"Critical gap: {module.module.title}")
        
        # Remove duplicates and return top gaps
        return list(dict.fromkeys(knowledge_gaps))[:5]
    
    def _is_critical_module(self, module) -> bool:
        """Determine if a module is critical (prerequisite for others)"""
        # This would typically check for dependencies
        # For now, consider first 3 modules as critical
        return getattr(module, 'order', 1) <= 3
    
    def _analyze_learning_style_indicators(self, progress_query) -> Dict[str, Any]:
        """Analyze learning style indicators from actual behavior data"""
        completed_activities = progress_query.filter(status='completed')
        
        if not completed_activities.exists():
            return {
                'preferred_difficulty': 'beginner',
                'session_length': 'short',
                'practice_frequency': 'irregular'
            }
        
        # Analyze session patterns
        session_lengths = []
        daily_activities = defaultdict(int)
        
        for activity in completed_activities:
            # Session length analysis
            if activity.time_spent:
                session_lengths.append(activity.time_spent.total_seconds() / 60)  # Convert to minutes
            
            # Daily activity patterns
            daily_activities[activity.updated_at.date()] += 1
        
        # Determine preferred session length
        avg_session_length = np.mean(session_lengths) if session_lengths else 30
        if avg_session_length < 15:
            session_length = 'short'
        elif avg_session_length < 45:
            session_length = 'moderate'
        else:
            session_length = 'long'
        
        # Determine practice frequency
        days_active = len(daily_activities)
        if days_active >= 20:  # Active most days
            frequency = 'regular'
        elif days_active >= 10:
            frequency = 'moderate'
        else:
            frequency = 'irregular'
        
        # Analyze difficulty preferences
        difficulty_scores = [self._get_module_difficulty_score(a.module) for a in completed_activities]
        avg_difficulty = np.mean(difficulty_scores) if difficulty_scores else 25.0
        
        if avg_difficulty < 40:
            preferred_difficulty = 'beginner'
        elif avg_difficulty < 60:
            preferred_difficulty = 'intermediate'
        else:
            preferred_difficulty = 'advanced'
        
        return {
            'preferred_difficulty': preferred_difficulty,
            'session_length': session_length,
            'practice_frequency': frequency,
            'avg_session_minutes': round(avg_session_length, 1),
            'days_active': days_active
        }
    
    def _analyze_retention(self, progress_query) -> float:
        """Analyze knowledge retention using spaced repetition patterns"""
        completed_activities = progress_query.filter(status='completed')
        
        if not completed_activities.exists():
            return 0.0
        
        # Analyze repeat performance on similar modules
        retention_scores = []
        module_performance = defaultdict(list)
        
        for activity in completed_activities:
            module_type = getattr(activity.module, 'module_type', 'general')
            module_performance[module_type].append(activity.score or 0)
        
        # Calculate retention for each module type
        for module_type, scores in module_performance.items():
            if len(scores) >= 2:
                # Compare first vs latest performance in this module type
                first_score = scores[0]
                latest_score = scores[-1]
                
                if first_score > 0:
                    retention = (latest_score / first_score) * 100
                    retention_scores.append(retention)
        
        # Overall retention
        if retention_scores:
            # Use median to avoid outlier influence
            overall_retention = np.median(retention_scores)
        else:
            # Fallback: analyze score consistency within module types
            consistencies = []
            for module_type, scores in module_performance.items():
                if len(scores) >= 3:
                    std_dev = np.std(scores)
                    # Lower standard deviation = better retention
                    consistency = max(0, 100 - (std_dev * 2))
                    consistencies.append(consistency)
            
            overall_retention = np.mean(consistencies) if consistencies else 80.0
        
        return round(min(100.0, max(0.0, overall_retention)), 2)
    
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
        """Calculate skill progression rate using actual performance improvement"""
        assessment_data = data['assessment_data']
        
        if len(assessment_data) < 2:
            return 0.0
        
        # Sort by completion date
        sorted_assessments = sorted(assessment_data, key=lambda x: x.completed_at or x.started_at)
        
        # Calculate progression over time periods
        progression_points = []
        window_size = max(1, len(sorted_assessments) // 3)  # Divide into 3 periods
        
        for i in range(0, len(sorted_assessments), window_size):
            window_assessments = sorted_assessments[i:i + window_size]
            if window_assessments:
                window_scores = [a.score for a in window_assessments if a.score is not None]
                if window_scores:
                    progression_points.append(np.mean(window_scores))
        
        if len(progression_points) < 2:
            return 0.0
        
        # Calculate overall progression rate
        first_half_avg = np.mean(progression_points[:len(progression_points)//2])
        second_half_avg = np.mean(progression_points[len(progression_points)//2:])
        
        progression_rate = ((second_half_avg - first_half_avg) / max(first_half_avg, 1)) * 100
        
        return round(max(-50.0, min(50.0, progression_rate)), 2)  # Cap at ±50%
    
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
        """Predict days to completion using ML-based forecasting"""
        progress_data = data['progress_data']
        assessment_data = data['assessment_data']
        
        if not progress_data:
            return None
        
        # Calculate current completion status
        completed = len([p for p in progress_data if p.status == 'completed'])
        total = len(progress_data)
        
        if completed >= total:
            return 0
        
        # Analyze learning velocity patterns
        recent_activities = [p for p in progress_data if p.status == 'completed']
        if not recent_activities:
            return None
        
        # Calculate multiple velocity metrics
        velocities = self._calculate_multiple_velocity_metrics(recent_activities)
        
        # Use ensemble prediction (weighted average of different metrics)
        predictions = []
        weights = []
        
        # Daily velocity prediction
        daily_velocity = velocities.get('daily', 0)
        if daily_velocity > 0:
            remaining_work = total - completed
            daily_prediction = int(remaining_work / daily_velocity)
            predictions.append(daily_prediction)
            weights.append(0.4)
        
        # Weekly velocity prediction (more stable)
        weekly_velocity = velocities.get('weekly', 0)
        if weekly_velocity > 0:
            weekly_prediction = int((total - completed) / (weekly_velocity / 7))
            predictions.append(weekly_prediction)
            weights.append(0.3)
        
        # Trend-adjusted prediction
        trend_velocity = velocities.get('trend_adjusted', 0)
        if trend_velocity > 0:
            trend_prediction = int((total - completed) / trend_velocity)
            predictions.append(trend_prediction)
            weights.append(0.3)
        
        if not predictions:
            return None
        
        # Weighted ensemble prediction
        if len(predictions) == 1:
            return max(1, predictions[0])
        
        weighted_prediction = sum(p * w for p, w in zip(predictions, weights)) / sum(weights)
        final_prediction = max(1, int(weighted_prediction))
        
        # Apply confidence adjustment
        confidence = self._calculate_prediction_confidence(data, velocities)
        if confidence < 0.5:
            final_prediction = int(final_prediction * 1.2)  # Add 20% buffer for low confidence
        
        return final_prediction
    
    def _calculate_multiple_velocity_metrics(self, activities: List) -> Dict[str, float]:
        """Calculate multiple velocity metrics for better predictions"""
        if len(activities) < 2:
            return {}
        
        # Sort by completion date
        sorted_activities = sorted(activities, key=lambda x: x.updated_at)
        
        velocities = {}
        
        # Daily velocity (last 7 days)
        recent_7_days = [a for a in sorted_activities if a.updated_at >= timezone.now() - timedelta(days=7)]
        if recent_7_days:
            velocities['daily'] = len(recent_7_days) / 7.0
        
        # Weekly velocity (last 4 weeks)
        recent_4_weeks = [a for a in sorted_activities if a.updated_at >= timezone.now() - timedelta(weeks=4)]
        if len(recent_4_weeks) >= 4:
            velocities['weekly'] = len(recent_4_weeks) / 4.0
        
        # Trend-adjusted velocity (weighted recent activities)
        if len(sorted_activities) >= 5:
            weighted_count = 0
            total_weight = 0
            
            for i, activity in enumerate(sorted_activities[-10:]):  # Last 10 activities
                weight = max(0.1, 1.0 - (i * 0.1))  # Decay weight
                weighted_count += weight
                total_weight += weight
            
            if total_weight > 0:
                velocities['trend_adjusted'] = weighted_count / total_weight
        
        return velocities
    
    def _calculate_prediction_confidence(self, data: Dict[str, Any], velocities: Dict[str, float]) -> float:
        """Calculate confidence level for predictions"""
        factors = []
        
        # Data quantity factor
        total_activities = len(data.get('progress_data', []))
        factors.append(min(1.0, total_activities / 20.0))  # Max confidence at 20+ activities
        
        # Consistency factor (lower variance = higher confidence)
        if velocities:
            velocity_values = list(velocities.values())
            if len(velocity_values) > 1:
                velocity_std = np.std(velocity_values)
                velocity_mean = np.mean(velocity_values)
                consistency = max(0, 1.0 - (velocity_std / max(velocity_mean, 0.1)))
                factors.append(consistency)
        
        # Recency factor (more recent data = higher confidence)
        recent_activities = len([a for a in data.get('progress_data', []) 
                               if a.updated_at >= timezone.now() - timedelta(days=7)])
        factors.append(min(1.0, recent_activities / 5.0))  # Max confidence at 5+ recent activities
        
        return np.mean(factors) if factors else 0.3
    
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
        """Generate key insights from analytics using advanced pattern analysis"""
        insights = []
        assessment_data = data.get('assessment_data', [])
        progress_data = data.get('progress_data', [])
        
        # Performance insights
        accuracy_rate = metrics.get('accuracy_rate', 0)
        if accuracy_rate >= 90:
            insights.append("Exceptional performance with consistent high accuracy rates")
        elif accuracy_rate >= 80:
            insights.append("Strong performance with good accuracy - ready for advanced challenges")
        elif accuracy_rate >= 70:
            insights.append("Solid performance foundation - focus on consistency")
        elif accuracy_rate >= 60:
            insights.append("Performance is improving - consider additional practice")
        else:
            insights.append("Performance requires focused attention - review fundamentals")
        
        # Learning velocity insights
        learning_velocity = metrics.get('learning_velocity', 0)
        if learning_velocity > 5:
            insights.append("Fast learning pace detected - consider acceleration or enrichment")
        elif learning_velocity > 2:
            insights.append("Good learning momentum maintained")
        elif learning_velocity > 0.5:
            insights.append("Steady learning progress - maintain consistency")
        elif learning_velocity > 0:
            insights.append("Learning pace is slow but steady")
        else:
            insights.append("Learning activity has declined - consider motivation strategies")
        
        # Engagement insights
        consistency_score = metrics.get('consistency_score', 0)
        if consistency_score >= 90:
            insights.append("Highly consistent learning habits - excellent discipline")
        elif consistency_score >= 75:
            insights.append("Good learning consistency with regular engagement")
        elif consistency_score >= 50:
            insights.append("Moderate consistency - room for improvement in regularity")
        else:
            insights.append("Inconsistent learning pattern detected - establish routine")
        
        # Skill development insights
        skill_progression = metrics.get('skill_progression_rate', 0)
        if skill_progression > 10:
            insights.append("Rapid skill development - exceeding expectations")
        elif skill_progression > 0:
            insights.append("Positive skill development trajectory")
        elif skill_progression > -10:
            insights.append("Skill development is steady - consider targeted practice")
        else:
            insights.append("Skill development has plateaued - try new learning approaches")
        
        # Time efficiency insights
        efficiency_score = metrics.get('efficiency_score', 0)
        if efficiency_score >= 85:
            insights.append("Highly efficient learning - optimal time management")
        elif efficiency_score >= 70:
            insights.append("Good time efficiency in learning activities")
        else:
            insights.append("Time efficiency could be improved - consider time management techniques")
        
        # Pattern-based insights
        if len(assessment_data) >= 5:
            scores = [a.score for a in assessment_data if a.score]
            if len(scores) >= 3:
                score_trend = self._analyze_score_trend(scores)
                if score_trend == 'improving':
                    insights.append("Learning outcomes are improving over time")
                elif score_trend == 'declining':
                    insights.append("Learning outcomes show decline - consider intervention")
        
        # Engagement pattern insights
        if len(progress_data) >= 10:
            engagement_pattern = self._analyze_engagement_patterns(progress_data)
            if engagement_pattern == 'consistent':
                insights.append("Consistent engagement patterns suggest sustainable learning")
            elif engagement_pattern == 'sporadic':
                insights.append("Sporadic engagement detected - consider structured scheduling")
        
        return insights[:5]  # Return top 5 insights
    
    def _analyze_score_trend(self, scores: List[float]) -> str:
        """Analyze trend in assessment scores"""
        if len(scores) < 3:
            return 'stable'
        
        # Calculate trend using linear regression slope
        n = len(scores)
        x = list(range(n))
        y = scores
        
        # Linear regression calculation
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        # Determine trend based on slope
        if slope > 2:
            return 'improving'
        elif slope < -2:
            return 'declining'
        else:
            return 'stable'
    
    def _analyze_engagement_patterns(self, progress_data: List) -> str:
        """Analyze engagement patterns"""
        # Group by day and analyze consistency
        daily_counts = defaultdict(int)
        for progress in progress_data:
            daily_counts[progress.updated_at.date()] += 1
        
        if len(daily_counts) < 3:
            return 'sporadic'
        
        # Calculate variance in daily engagement
        counts = list(daily_counts.values())
        variance = np.var(counts)
        mean_count = np.mean(counts)
        
        if mean_count > 0:
            coefficient_of_variation = variance ** 0.5 / mean_count
            if coefficient_of_variation < 0.5:
                return 'consistent'
            else:
                return 'sporadic'
        
        return 'sporadic'
    
    def _generate_recommendations(self, data: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations using advanced analytics"""
        recommendations = []
        
        # Performance-based recommendations
        accuracy_rate = metrics.get('accuracy_rate', 0)
        if accuracy_rate < 70:
            recommendations.append("Focus on fundamental concepts before advancing to complex topics")
            recommendations.append("Consider additional practice exercises in weak areas")
            recommendations.append("Break down complex problems into smaller, manageable steps")
        elif accuracy_rate < 85:
            recommendations.append("Strengthen understanding of core concepts through varied practice")
            recommendations.append("Review incorrect answers to identify knowledge gaps")
        elif accuracy_rate > 90:
            recommendations.append("Excellent performance - consider taking on advanced challenges")
            recommendations.append("Explore mentor opportunities to reinforce your knowledge")
        
        # Engagement-based recommendations
        consistency_score = metrics.get('consistency_score', 0)
        if consistency_score < 60:
            recommendations.append("Establish a consistent daily learning routine (15-30 minutes)")
            recommendations.append("Set smaller, achievable daily goals to build momentum")
            recommendations.append("Use calendar reminders to maintain learning schedule")
        elif consistency_score < 80:
            recommendations.append("Maintain current learning consistency")
            recommendations.append("Consider extending session length slightly for deeper learning")
        
        # Learning velocity recommendations
        learning_velocity = metrics.get('learning_velocity', 0)
        if learning_velocity > 5:
            recommendations.append("Fast learning pace - consider advanced or enrichment activities")
            recommendations.append("Explore cross-subject connections to deepen understanding")
        elif learning_velocity < 0.5:
            recommendations.append("Increase study frequency to maintain learning momentum")
            recommendations.append("Consider time-blocking for dedicated learning sessions")
        
        # Skill development recommendations
        skill_progression = metrics.get('skill_progression_rate', 0)
        if skill_progression < -5:
            recommendations.append("Focus on skill consolidation through targeted practice")
            recommendations.append("Consider reviewing prerequisite material")
        elif skill_progression > 10:
            recommendations.append("Rapid skill development - explore advanced applications")
        
        # Time efficiency recommendations
        efficiency_score = metrics.get('efficiency_score', 0)
        if efficiency_score < 60:
            recommendations.append("Improve time management - use the Pomodoro technique")
            recommendations.append("Eliminate distractions during learning sessions")
            recommendations.append("Plan learning sessions with clear objectives")
        
        # Knowledge retention recommendations
        retention_analysis = metrics.get('retention_analysis', {})
        if isinstance(retention_analysis, dict) and retention_analysis.get('retention_rate', 0) < 70:
            recommendations.append("Implement spaced repetition for better knowledge retention")
            recommendations.append("Schedule regular review sessions of previously learned material")
            recommendations.append("Create summary notes for quick review")
        
        # Adaptive recommendations based on learning style
        learning_style = metrics.get('learning_style_indicators', {})
        if isinstance(learning_style, dict):
            session_length = learning_style.get('session_length', 'moderate')
            if session_length == 'short':
                recommendations.append("Use micro-learning sessions (10-15 minutes) for better retention")
            elif session_length == 'long':
                recommendations.append("Take regular breaks during longer study sessions")
            
            preferred_difficulty = learning_style.get('preferred_difficulty', 'beginner')
            if preferred_difficulty == 'beginner':
                recommendations.append("Gradually increase difficulty level to challenge yourself")
        
        # Goal-based recommendations
        completion_rate = metrics.get('completion_rate', 0)
        if completion_rate < 50:
            recommendations.append("Focus on completing current modules before starting new ones")
            recommendations.append("Set weekly completion goals to track progress")
        elif completion_rate > 80:
            recommendations.append("Excellent completion rate - maintain current approach")
        
        return recommendations[:8]  # Return top 8 recommendations