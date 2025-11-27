# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Progress Service - JAC Learning Platform

This service handles core progress tracking functionality including
snapshot creation, progress calculation, and real-time activity tracking.

Author: Cavin Otieno
Created: 2025-11-25
"""

import uuid
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
import logging

from ..models import ProgressSnapshot, ProgressNotification, UserProgressMetric
from apps.learning.models import (
    LearningPath, Module, Lesson, UserLearningPath, UserModuleProgress
)
from apps.assessments.models import AssessmentAttempt

logger = logging.getLogger(__name__)


class ProgressService:
    """
    Service class for progress tracking operations
    """
    
    def __init__(self):
        self.snapshot_threshold_hours = 6  # Minimum hours between automatic snapshots
    
    def create_user_snapshot(
        self,
        user: User,
        learning_path_id: Optional[int] = None,
        module_id: Optional[int] = None,
        force: bool = False
    ) -> ProgressSnapshot:
        """
        Create a comprehensive progress snapshot for a user
        
        Args:
            user: The user to create snapshot for
            learning_path_id: Optional specific learning path
            module_id: Optional specific module
            force: Whether to force create snapshot regardless of timing
        
        Returns:
            ProgressSnapshot instance
        """
        # Check if we should create a new snapshot
        if not force:
            latest_snapshot = ProgressSnapshot.objects.filter(
                user=user,
                learning_path_id=learning_path_id,
                module_id=module_id
            ).order_by('-snapshot_date').first()
            
            if latest_snapshot:
                time_diff = timezone.now() - latest_snapshot.snapshot_date
                if time_diff < timedelta(hours=self.snapshot_threshold_hours):
                    logger.info(f"Snapshot not created - too recent for user {user.username}")
                    return latest_snapshot
        
        # Get context objects
        learning_path = None
        module = None
        
        if learning_path_id:
            learning_path = LearningPath.objects.get(id=learning_path_id)
        
        if module_id:
            module = Module.objects.get(id=module_id)
        
        # Calculate progress metrics
        metrics = self._calculate_progress_metrics(user, learning_path, module)
        
        # Create snapshot
        snapshot = ProgressSnapshot.objects.create(
            user=user,
            learning_path=learning_path,
            module=module,
            **metrics
        )
        
        logger.info(f"Created progress snapshot {snapshot.id} for user {user.username}")
        
        # Check for milestone achievements
        if self._is_milestone_snapshot(snapshot):
            snapshot.is_milestone = True
            snapshot.save()
            self._trigger_milestone_notifications(user, snapshot)
        
        return snapshot
    
    def track_user_activity(
        self,
        user: User,
        activity_type: str,
        entity_id: int,
        score: Optional[float] = None,
        time_spent: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Track user activity in real-time
        
        Args:
            user: The user performing the activity
            activity_type: Type of activity (lesson_completed, assessment_completed, etc.)
            entity_id: ID of the related entity
            score: Optional score achieved
            time_spent: Optional time spent in seconds
        
        Returns:
            Dict with tracking results
        """
        activity_data = {
            'user_id': user.id,
            'activity_type': activity_type,
            'entity_id': entity_id,
            'score': score,
            'time_spent': time_spent,
            'timestamp': timezone.now().isoformat()
        }
        
        try:
            # Handle different activity types
            if activity_type == 'lesson_completed':
                result = self._handle_lesson_completion(user, entity_id, score, time_spent)
            elif activity_type == 'assessment_completed':
                result = self._handle_assessment_completion(user, entity_id, score, time_spent)
            elif activity_type == 'module_completed':
                result = self._handle_module_completion(user, entity_id)
            else:
                result = {'status': 'tracked', 'message': 'Activity tracked but type not recognized'}
            
            # Update user progress metrics
            self._update_user_metrics(user, activity_type, score, time_spent)
            
            # Check if we should create a snapshot
            self._maybe_create_automatic_snapshot(user)
            
            activity_data.update(result)
            logger.info(f"Tracked activity {activity_type} for user {user.username}")
            
            return {
                'success': True,
                'activity_data': activity_data,
                'result': result
            }
            
        except Exception as e:
            logger.error(f"Error tracking activity for user {user.username}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'activity_data': activity_data
            }
    
    def generate_comprehensive_summary(self, user: User) -> Dict[str, Any]:
        """
        Generate comprehensive progress summary for a user
        
        Args:
            user: The user to generate summary for
        
        Returns:
            Dict containing comprehensive summary data
        """
        try:
            # Get user's learning paths
            user_learning_paths = UserLearningPath.objects.filter(user=user)
            
            # Calculate overall progress
            total_modules = Module.objects.filter(
                learning_path__in=user_learning_paths.values('learning_path')
            ).count()
            
            completed_modules = UserModuleProgress.objects.filter(
                user=user,
                status='completed',
                module__learning_path__in=user_learning_paths.values('learning_path')
            ).count()
            
            overall_completion = (completed_modules / total_modules * 100) if total_modules > 0 else 0
            
            # Calculate performance metrics
            assessment_results = UserAssessmentResult.objects.filter(user=user)
            avg_score = assessment_results.aggregate(Avg('score'))['score__avg'] or 0
            best_score = assessment_results.aggregate(Max('score'))['score__max'] or 0
            
            # Calculate time spent
            total_time = UserModuleProgress.objects.filter(
                user=user,
                time_spent__isnull=False
            ).aggregate(Sum('time_spent'))['time_spent__sum'] or timedelta(0)
            
            # Get engagement metrics
            days_active = self._calculate_days_active(user)
            current_streak = self._calculate_current_streak(user)
            longest_streak = self._calculate_longest_streak(user)
            
            # Get recent snapshots
            recent_snapshots = ProgressSnapshot.objects.filter(
                user=user
            ).order_by('-snapshot_date')[:10]
            
            # Get goals data
            goals = user.progress_goals.all()
            active_goals = goals.filter(status='active').count()
            completed_goals = goals.filter(status='completed').count()
            overdue_goals = goals.filter(
                status='active',
                target_date__lt=timezone.now().date()
            ).count()
            
            # Determine current level
            current_level = self._determine_learning_level(overall_completion, avg_score)
            
            # Get next milestone
            next_milestone = self._get_next_milestone(overall_completion)
            
            # Get achievements (placeholder)
            total_achievements = 0
            recent_achievements = []
            
            # Get analytics summary
            performance_trend = self._calculate_performance_trend(user)
            engagement_level = self._calculate_engagement_level(user, days_active)
            learning_velocity = self._calculate_learning_velocity(user)
            
            return {
                'user_id': user.id,
                'username': user.username,
                'overall_completion': round(overall_completion, 2),
                'total_modules': total_modules,
                'completed_modules': completed_modules,
                'current_level': current_level,
                'next_milestone': next_milestone,
                'average_score': round(avg_score, 2),
                'best_score': round(best_score, 2),
                'total_time_spent': total_time,
                'days_active': days_active,
                'current_streak': current_streak,
                'longest_streak': longest_streak,
                'recent_snapshots': [
                    {
                        'id': str(s.id),
                        'snapshot_date': s.snapshot_date.isoformat(),
                        'completion_percentage': s.completion_percentage,
                        'average_score': s.average_score,
                        'is_milestone': s.is_milestone
                    }
                    for s in recent_snapshots
                ],
                'active_goals': active_goals,
                'completed_goals': completed_goals,
                'overdue_goals': overdue_goals,
                'total_achievements': total_achievements,
                'recent_achievements': recent_achievements,
                'performance_trend': performance_trend,
                'engagement_level': round(engagement_level, 2),
                'learning_velocity': round(learning_velocity, 2)
            }
            
        except Exception as e:
            logger.error(f"Error generating comprehensive summary for user {user.username}: {str(e)}")
            raise
    
    def _calculate_progress_metrics(
        self,
        user: User,
        learning_path: Optional[LearningPath] = None,
        module: Optional[Module] = None
    ) -> Dict[str, float]:
        """
        Calculate comprehensive progress metrics for a user
        
        Args:
            user: The user to calculate metrics for
            learning_path: Optional specific learning path
            module: Optional specific module
        
        Returns:
            Dict containing calculated metrics
        """
        queryset = UserModuleProgress.objects.filter(user=user)
        
        if learning_path:
            queryset = queryset.filter(module__learning_path=learning_path)
        
        if module:
            queryset = queryset.filter(module=module)
        
        # Count modules
        total_modules = Module.objects.filter(
            learning_path__in=queryset.values('module__learning_path')
        ).distinct().count()
        
        completed_modules = queryset.filter(status='completed').count()
        
        # Calculate assessment metrics
        assessment_query = UserAssessmentResult.objects.filter(user=user)
        
        if learning_path:
            assessment_query = assessment_query.filter(
                assessment__learning_path=learning_path
            )
        
        if module:
            assessment_query = assessment_query.filter(
                assessment__module=module
            )
        
        total_assessments = assessment_query.count()
        completed_assessments = assessment_query.filter(completed_at__isnull=False).count()
        
        # Calculate scores
        avg_score = assessment_query.aggregate(Avg('score'))['score__avg'] or 0
        best_score = assessment_query.aggregate(Max('score'))['score__max'] or 0
        
        # Calculate time spent
        total_time = queryset.aggregate(Sum('time_spent'))['time_spent__sum'] or timedelta(0)
        
        # Calculate engagement metrics
        days_active = self._calculate_days_active(user, learning_path)
        session_count = self._calculate_session_count(user, learning_path)
        streak_days = self._calculate_current_streak(user, learning_path)
        
        # Calculate completion percentage
        completion_percentage = (completed_modules / total_modules * 100) if total_modules > 0 else 0
        
        return {
            'completion_percentage': round(completion_percentage, 2),
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'total_assessments': total_assessments,
            'completed_assessments': completed_assessments,
            'average_score': round(avg_score, 2),
            'best_score': round(best_score, 2),
            'total_time_spent': total_time,
            'days_active': days_active,
            'session_count': session_count,
            'streak_days': streak_days
        }
    
    def _handle_lesson_completion(
        self,
        user: User,
        lesson_id: int,
        score: Optional[float],
        time_spent: Optional[int]
    ) -> Dict[str, Any]:
        """Handle lesson completion activity"""
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            
            # Update or create progress record
            progress, created = UserModuleProgress.objects.update_or_create(
                user=user,
                module=lesson.module,
                defaults={
                    'status': 'completed',
                    'score': score,
                    'time_spent': timedelta(seconds=time_spent) if time_spent else None,
                    'completed_at': timezone.now()
                }
            )
            
            return {
                'status': 'lesson_completed',
                'lesson_id': lesson_id,
                'module_id': lesson.module.id,
                'progress_id': str(progress.id),
                'created': created
            }
        except Lesson.DoesNotExist:
            raise ValueError(f"Lesson with ID {lesson_id} not found")
    
    def _handle_assessment_completion(
        self,
        user: User,
        assessment_id: int,
        score: Optional[float],
        time_spent: Optional[int]
    ) -> Dict[str, Any]:
        """Handle assessment completion activity"""
        try:
            assessment = Assessment.objects.get(id=assessment_id)
            
            # Create assessment result
            result = UserAssessmentResult.objects.create(
                user=user,
                assessment=assessment,
                score=score,
                time_spent=timedelta(seconds=time_spent) if time_spent else None,
                completed_at=timezone.now()
            )
            
            return {
                'status': 'assessment_completed',
                'assessment_id': assessment_id,
                'result_id': str(result.id),
                'score': score
            }
        except Assessment.DoesNotExist:
            raise ValueError(f"Assessment with ID {assessment_id} not found")
    
    def _handle_module_completion(self, user: User, module_id: int) -> Dict[str, Any]:
        """Handle module completion activity"""
        try:
            module = Module.objects.get(id=module_id)
            
            # Update progress to completed if all lessons are done
            progress = UserModuleProgress.objects.get(user=user, module=module)
            
            # Check if all lessons are completed
            completed_lessons = UserModuleProgress.objects.filter(
                user=user,
                module__parent_module=module,
                status='completed'
            ).count()
            
            total_lessons = module.get_all_lessons().count()
            
            if completed_lessons == total_lessons:
                progress.status = 'completed'
                progress.completed_at = timezone.now()
                progress.save()
            
            return {
                'status': 'module_completed',
                'module_id': module_id,
                'progress_id': str(progress.id)
            }
        except Module.DoesNotExist:
            raise ValueError(f"Module with ID {module_id} not found")
    
    def _update_user_metrics(
        self,
        user: User,
        activity_type: str,
        score: Optional[float],
        time_spent: Optional[int]
    ):
        """Update user's progress metrics"""
        metrics_to_update = []
        
        if activity_type in ['lesson_completed', 'module_completed']:
            metrics_to_update.append('completion_rate')
        
        if activity_type == 'assessment_completed' and score is not None:
            metrics_to_update.append('accuracy_rate')
        
        for metric_type in metrics_to_update:
            # Get or create metric
            metric, created = UserProgressMetric.objects.get_or_create(
                user=user,
                metric_type=metric_type,
                defaults={'target_value': 100}
            )
            
            # Update current value based on activity
            if metric_type == 'completion_rate':
                # Recalculate completion rate
                completed = UserModuleProgress.objects.filter(
                    user=user,
                    status='completed'
                ).count()
                total = Module.objects.filter(
                    learning_path__userlearningpath__user=user
                ).count()
                metric.current_value = (completed / total * 100) if total > 0 else 0
            
            elif metric_type == 'accuracy_rate' and score is not None:
                # Update accuracy rate with new score
                scores = list(UserAssessmentResult.objects.filter(
                    user=user,
                    score__isnull=False
                ).values_list('score', flat=True))
                
                if scores:
                    metric.current_value = sum(scores) / len(scores)
            
            metric.last_updated = timezone.now()
            metric.save()
    
    def _maybe_create_automatic_snapshot(self, user: User):
        """Create automatic snapshot if conditions are met"""
        # Check if enough time has passed since last snapshot
        latest_snapshot = ProgressSnapshot.objects.filter(user=user).order_by('-snapshot_date').first()
        
        if not latest_snapshot or (timezone.now() - latest_snapshot.snapshot_date) >= timedelta(hours=self.snapshot_threshold_hours):
            self.create_user_snapshot(user)
    
    def _calculate_days_active(self, user: User, learning_path: Optional[LearningPath] = None) -> int:
        """Calculate number of days user has been active"""
        queryset = UserModuleProgress.objects.filter(user=user)
        
        if learning_path:
            queryset = queryset.filter(module__learning_path=learning_path)
        
        # Count distinct days with activity
        active_days = queryset.dates('updated_at', 'day').count()
        return active_days
    
    def _calculate_session_count(self, user: User, learning_path: Optional[LearningPath] = None) -> int:
        """Calculate number of learning sessions"""
        queryset = UserModuleProgress.objects.filter(user=user)
        
        if learning_path:
            queryset = queryset.filter(module__learning_path=learning_path)
        
        # Group by date to count sessions
        sessions = queryset.annotate(
            date=TruncDate('updated_at')
        ).values('date').distinct().count()
        
        return sessions
    
    def _calculate_current_streak(self, user: User, learning_path: Optional[LearningPath] = None) -> int:
        """Calculate current learning streak in days"""
        queryset = UserModuleProgress.objects.filter(user=user)
        
        if learning_path:
            queryset = queryset.filter(module__learning_path=learning_path)
        
        # Get dates with activity, ordered descending
        activity_dates = queryset.dates('updated_at', 'day').order_by('-day')
        
        if not activity_dates:
            return 0
        
        # Calculate streak
        streak = 1
        current_date = activity_dates[0]
        
        for activity_date in activity_dates[1:]:
            if (current_date - activity_date).days == 1:
                streak += 1
                current_date = activity_date
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self, user: User, learning_path: Optional[LearningPath] = None) -> int:
        """Calculate longest learning streak"""
        queryset = UserModuleProgress.objects.filter(user=user)
        
        if learning_path:
            queryset = queryset.filter(module__learning_path=learning_path)
        
        activity_dates = list(queryset.dates('updated_at', 'day').order_by('day'))
        
        if not activity_dates:
            return 0
        
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(activity_dates)):
            if (activity_dates[i] - activity_dates[i-1]).days == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        
        return max_streak
    
    def _determine_learning_level(self, completion_percentage: float, avg_score: float) -> str:
        """Determine user's current learning level"""
        if completion_percentage >= 90 and avg_score >= 85:
            return 'Expert'
        elif completion_percentage >= 75 and avg_score >= 80:
            return 'Advanced'
        elif completion_percentage >= 60 and avg_score >= 70:
            return 'Intermediate'
        elif completion_percentage >= 40 and avg_score >= 60:
            return 'Developing'
        else:
            return 'Beginner'
    
    def _get_next_milestone(self, completion_percentage: float) -> str:
        """Get the next learning milestone"""
        if completion_percentage < 25:
            return "Complete your first module"
        elif completion_percentage < 50:
            return "Reach 50% completion"
        elif completion_percentage < 75:
            return "Complete 75% of the learning path"
        elif completion_percentage < 100:
            return "Complete the learning path"
        else:
            return "Explore advanced concepts"
    
    def _is_milestone_snapshot(self, snapshot: ProgressSnapshot) -> bool:
        """Check if snapshot represents a milestone"""
        milestones = [25, 50, 75, 100]
        completion = snapshot.completion_percentage
        
        for milestone in milestones:
            if abs(completion - milestone) <= 2:  # Within 2% of milestone
                return True
        
        # Check for perfect scores
        if snapshot.average_score >= 95:
            return True
        
        # Check for completion of first module
        if snapshot.completed_modules == 1 and snapshot.total_modules > 1:
            return True
        
        return False
    
    def _trigger_milestone_notifications(self, user: User, snapshot: ProgressSnapshot):
        """Trigger notifications for milestone achievements"""
        notification_data = []
        
        if snapshot.completion_percentage >= 100:
            notification_data.append({
                'notification_type': 'milestone_achieved',
                'title': 'Learning Path Completed!',
                'message': f"Congratulations! You've completed your learning path with {snapshot.average_score:.1f}% average score.",
                'priority': 'high'
            })
        
        if snapshot.average_score >= 95:
            notification_data.append({
                'notification_type': 'achievement_unlocked',
                'title': 'High Performance Achievement',
                'message': f"Outstanding! You've achieved an average score of {snapshot.average_score:.1f}%.",
                'priority': 'normal'
            })
        
        # Create notifications
        for data in notification_data:
            ProgressNotification.objects.create(
                user=user,
                **data,
                data={'snapshot_id': str(snapshot.id)}
            )
    
    def _calculate_performance_trend(self, user: User) -> str:
        """Calculate user's performance trend"""
        # This is a simplified implementation
        # In a real application, you'd analyze historical data
        recent_snapshots = ProgressSnapshot.objects.filter(
            user=user
        ).order_by('-snapshot_date')[:5]
        
        if len(recent_snapshots) < 2:
            return 'stable'
        
        scores = [s.average_score for s in recent_snapshots]
        
        if len(scores) >= 3:
            # Calculate trend over last 3 snapshots
            recent_avg = sum(scores[:3]) / 3
            older_avg = sum(scores[3:]) / len(scores[3:]) if len(scores) > 3 else recent_avg
            
            if recent_avg > older_avg + 5:
                return 'improving'
            elif recent_avg < older_avg - 5:
                return 'declining'
        
        return 'stable'
    
    def _calculate_engagement_level(self, user: User, days_active: int) -> float:
        """Calculate user's engagement level (0-100)"""
        # Calculate engagement based on activity frequency
        if days_active >= 21:  # 3+ weeks of regular activity
            return 90.0
        elif days_active >= 14:  # 2+ weeks
            return 75.0
        elif days_active >= 7:  # 1+ week
            return 60.0
        elif days_active >= 3:  # Several days
            return 40.0
        else:
            return 20.0
    
    def _calculate_learning_velocity(self, user: User) -> float:
        """Calculate user's learning velocity (modules per week)"""
        # This is a simplified implementation
        # In reality, you'd calculate this over a specific time period
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=timezone.now() - timedelta(weeks=4)
        ).count()
        
        return recent_progress / 4.0  # Modules per week