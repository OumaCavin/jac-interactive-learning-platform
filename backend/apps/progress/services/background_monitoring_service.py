"""
Background Monitoring Service - JAC Learning Platform

Continuous background monitoring for performance tracking, alerts, and analytics.
Runs as a background service to monitor all users and learning paths.

Author: MiniMax Agent
Created: 2025-11-26
"""

import asyncio
import schedule
import time
from typing import Dict, Any, List
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg, F
from django.core.management.base import BaseCommand

from ..models import ProgressSnapshot, LearningAnalytics, ProgressNotification, UserProgressMetric
from apps.learning.models import UserModuleProgress, AssessmentAttempt
from .analytics_service import AnalyticsService
from .realtime_monitoring_service import RealtimeMonitoringService


class BackgroundMonitoringService:
    """
    Background service for continuous performance monitoring and alerts
    """
    
    def __init__(self):
        self.analytics_service = AnalyticsService()
        self.realtime_service = RealtimeMonitoringService()
        self.monitoring_active = False
        self.monitoring_tasks = []
        
        # Alert thresholds
        self.alert_thresholds = {
            'performance_decline': {
                'score_threshold': 60.0,
                'consecutive_days': 2,
                'severity': 'high'
            },
            'engagement_drop': {
                'activity_threshold': 1,  # Less than 1 activity per day
                'consecutive_days': 3,
                'severity': 'medium'
            },
            'completion_stagnation': {
                'no_progress_days': 5,
                'severity': 'medium'
            },
            'low_consistency': {
                'consistency_threshold': 50.0,
                'measurement_period_days': 7,
                'severity': 'low'
            }
        }
    
    async def start_background_monitoring(self) -> None:
        """Start background monitoring service"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        # Schedule monitoring tasks
        self._schedule_monitoring_tasks()
        
        # Start main monitoring loop
        await self._run_monitoring_loop()
    
    def stop_background_monitoring(self) -> None:
        """Stop background monitoring service"""
        self.monitoring_active = False
        
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            task.cancel()
        
        self.monitoring_tasks.clear()
    
    def _schedule_monitoring_tasks(self) -> None:
        """Schedule periodic monitoring tasks"""
        # Performance monitoring every 15 minutes
        schedule.every(15).minutes.do(self._schedule_async_task, self._monitor_user_performance)
        
        # Engagement monitoring every hour
        schedule.every().hour.do(self._schedule_async_task, self._monitor_user_engagement)
        
        # Daily analytics generation every day at 2 AM
        schedule.every().day.at("02:00").do(self._schedule_async_task, self._generate_daily_analytics)
        
        # Alert cleanup every week
        schedule.every().week.do(self._schedule_async_task, self._cleanup_old_alerts)
        
        # Learning velocity analysis every 6 hours
        schedule.every(6).hours.do(self._schedule_async_task, self._analyze_learning_velocity)
    
    def _schedule_async_task(self, task_func) -> None:
        """Schedule an async task to run"""
        task = asyncio.create_task(task_func())
        self.monitoring_tasks.append(task)
    
    async def _run_monitoring_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                schedule.run_pending()
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _monitor_user_performance(self) -> None:
        """Monitor user performance for potential issues"""
        try:
            # Get all active users (users with recent activity)
            active_users = User.objects.filter(
                learning_assessment_attempts__completed_at__gte=timezone.now() - timedelta(days=30)
            ).distinct()
            
            for user in active_users:
                await self._check_user_performance_trends(user)
                
        except Exception as e:
            print(f"Error monitoring user performance: {e}")
    
    async def _check_user_performance_trends(self, user: User) -> None:
        """Check individual user's performance trends"""
        try:
            # Get recent assessment performance
            recent_assessments = AssessmentAttempt.objects.filter(
                user=user,
                completed_at__gte=timezone.now() - timedelta(days=7),
                status='completed'
            ).order_by('-completed_at')
            
            if recent_assessments.count() < 2:
                return
            
            # Analyze performance trends
            scores = [a.score for a in recent_assessments if a.score is not None]
            
            if len(scores) < 2:
                return
            
            # Check for performance decline
            recent_scores = scores[:3]  # Last 3 scores
            older_scores = scores[3:6] if len(scores) > 3 else scores[:max(1, len(scores)//2)]
            
            if recent_scores and older_scores:
                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores)
                
                decline_threshold = self.alert_thresholds['performance_decline']['score_threshold']
                
                if recent_avg < decline_threshold and recent_avg < older_avg:
                    await self._trigger_performance_alert(user, recent_avg, older_avg)
            
            # Check for consecutive low scores
            consecutive_low_scores = 0
            for score in recent_scores:
                if score < decline_threshold:
                    consecutive_low_scores += 1
                else:
                    break
            
            if consecutive_low_scores >= self.alert_thresholds['performance_decline']['consecutive_days']:
                await self._trigger_consecutive_low_scores_alert(user, consecutive_low_scores)
                
        except Exception as e:
            print(f"Error checking performance trends for user {user.id}: {e}")
    
    async def _trigger_performance_alert(self, user: User, recent_avg: float, older_avg: float) -> None:
        """Trigger performance decline alert"""
        alert_message = f"Performance decline detected: Current average {recent_avg:.1f}% vs previous {older_avg:.1f}%"
        
        await self._create_progress_notification(
            user=user,
            notification_type='progress_alert',
            priority='high',
            title='Performance Decline Alert',
            message=alert_message,
            data={
                'recent_average': recent_avg,
                'previous_average': older_avg,
                'decline_amount': older_avg - recent_avg
            }
        )
    
    async def _trigger_consecutive_low_scores_alert(self, user: User, consecutive_count: int) -> None:
        """Trigger consecutive low scores alert"""
        alert_message = f"Low performance detected in {consecutive_count} consecutive assessments. Consider additional practice."
        
        await self._create_progress_notification(
            user=user,
            notification_type='progress_alert',
            priority='medium',
            title='Consistent Low Performance',
            message=alert_message,
            data={
                'consecutive_low_scores': consecutive_count,
                'suggested_action': 'additional_practice'
            }
        )
    
    async def _monitor_user_engagement(self) -> None:
        """Monitor user engagement levels"""
        try:
            # Get users with activity in the last 30 days
            active_users = User.objects.filter(
                learning_module_progress__updated_at__gte=timezone.now() - timedelta(days=30)
            ).distinct()
            
            for user in active_users:
                await self._check_user_engagement(user)
                
        except Exception as e:
            print(f"Error monitoring user engagement: {e}")
    
    async def _check_user_engagement(self, user: User) -> None:
        """Check individual user's engagement levels"""
        try:
            # Calculate daily activity for the last 7 days
            daily_activities = {}
            for i in range(7):
                date = (timezone.now() - timedelta(days=i)).date()
                activities_count = UserModuleProgress.objects.filter(
                    user=user,
                    updated_at__date=date
                ).count()
                daily_activities[date] = activities_count
            
            # Check for engagement drop
            recent_days_activities = sum(daily_activities[date] for date in list(daily_activities.keys())[:3])
            older_days_activities = sum(daily_activities[date] for date in list(daily_activities.keys())[3:6])
            
            activity_threshold = self.alert_thresholds['engagement_drop']['activity_threshold']
            consecutive_days = self.alert_thresholds['engagement_drop']['consecutive_days']
            
            # Check for multiple consecutive days with low activity
            consecutive_low_days = 0
            for date in sorted(daily_activities.keys(), reverse=True):
                if daily_activities[date] < activity_threshold:
                    consecutive_low_days += 1
                else:
                    break
            
            if consecutive_low_days >= consecutive_days:
                await self._trigger_engagement_alert(user, consecutive_low_days)
            
            # Check for overall engagement drop
            if recent_days_activities == 0 and older_days_activities > 0:
                await self._trigger_engagement_drop_alert(user, older_days_activities)
                
        except Exception as e:
            print(f"Error checking user engagement for user {user.id}: {e}")
    
    async def _trigger_engagement_alert(self, user: User, consecutive_low_days: int) -> None:
        """Trigger engagement alert for consecutive low activity"""
        alert_message = f"Low engagement detected for {consecutive_low_days} consecutive days. Consider setting a regular study schedule."
        
        await self._create_progress_notification(
            user=user,
            notification_type='progress_alert',
            priority='medium',
            title='Engagement Alert',
            message=alert_message,
            data={
                'consecutive_low_days': consecutive_low_days,
                'suggested_action': 'schedule_regular_study'
            }
        )
    
    async def _trigger_engagement_drop_alert(self, user: User, previous_activity: int) -> None:
        """Trigger engagement drop alert"""
        alert_message = f"Learning activity has dropped significantly. Previously averaging {previous_activity/3:.1f} activities per day."
        
        await self._create_progress_notification(
            user=user,
            notification_type='progress_alert',
            priority='medium',
            title='Activity Drop Alert',
            message=alert_message,
            data={
                'previous_daily_average': previous_activity / 3,
                'current_activity': 0
            }
        )
    
    async def _generate_daily_analytics(self) -> None:
        """Generate daily analytics for all active users"""
        try:
            # Get users with recent activity
            active_users = User.objects.filter(
                Q(learning_module_progress__updated_at__gte=timezone.now() - timedelta(days=1)) |
                Q(learning_assessment_attempts__completed_at__gte=timezone.now() - timedelta(days=1))
            ).distinct()
            
            analytics_generated = 0
            
            for user in active_users:
                try:
                    # Generate comprehensive analytics for the past day
                    analytics_data = self.analytics_service.generate_comprehensive_analytics(
                        user=user,
                        time_period_days=1,
                        analytics_type='comprehensive'
                    )
                    
                    if analytics_data:
                        analytics_generated += 1
                        
                        # Store analytics snapshot
                        ProgressSnapshot.objects.create(
                            user=user,
                            snapshot_date=timezone.now(),
                            total_activities=analytics_data.get('summary_metrics', {}).get('total_activities', 0),
                            completed_activities=analytics_data.get('summary_metrics', {}).get('completed_activities', 0)
                        )
                
                except Exception as e:
                    print(f"Error generating analytics for user {user.id}: {e}")
                    continue
            
            print(f"Generated daily analytics for {analytics_generated} users")
            
        except Exception as e:
            print(f"Error in daily analytics generation: {e}")
    
    async def _analyze_learning_velocity(self) -> None:
        """Analyze learning velocity trends across all users"""
        try:
            # Get learning path data for velocity analysis
            learning_paths = UserModuleProgress.objects.filter(
                status='completed'
            ).values('module__learning_path').distinct()
            
            for path_data in learning_paths:
                learning_path_id = path_data['module__learning_path']
                
                # Calculate velocity for this learning path
                await self._analyze_path_velocity(learning_path_id)
                
        except Exception as e:
            print(f"Error analyzing learning velocity: {e}")
    
    async def _analyze_path_velocity(self, learning_path_id: int) -> None:
        """Analyze learning velocity for a specific path"""
        try:
            # Get completion data for the last 30 days
            thirty_days_ago = timezone.now() - timedelta(days=30)
            
            completions_by_day = {}
            for i in range(30):
                date = (thirty_days_ago + timedelta(days=i)).date()
                completions_count = UserModuleProgress.objects.filter(
                    module__learning_path_id=learning_path_id,
                    status='completed',
                    updated_at__date=date
                ).count()
                completions_by_day[date] = completions_count
            
            # Calculate velocity trends
            recent_velocity = sum(completions_by_day[date] for date in list(completions_by_day.keys())[-7:])
            earlier_velocity = sum(completions_by_day[date] for date in list(completions_by_day.keys())[-14:-7])
            
            # Update progress metrics if velocity has changed significantly
            velocity_change = ((recent_velocity - earlier_velocity) / max(earlier_velocity, 1)) * 100
            
            if abs(velocity_change) > 20:  # 20% change threshold
                # This could trigger a path optimization alert
                pass  # Implementation would update learning path metrics
            
        except Exception as e:
            print(f"Error analyzing path velocity for {learning_path_id}: {e}")
    
    async def _cleanup_old_alerts(self) -> None:
        """Clean up old alerts and notifications"""
        try:
            # Delete alerts older than 30 days
            cutoff_date = timezone.now() - timedelta(days=30)
            
            deleted_count = ProgressNotification.objects.filter(
                created_at__lt=cutoff_date,
                is_read=True
            ).delete()[0]
            
            print(f"Cleaned up {deleted_count} old notifications")
            
            # Archive old analytics snapshots
            archive_cutoff = timezone.now() - timedelta(days=90)
            archived_count = ProgressSnapshot.objects.filter(
                snapshot_date__lt=archive_cutoff
            ).update(is_milestone=False)  # Mark as non-milestone for cleanup
            
        except Exception as e:
            print(f"Error cleaning up old alerts: {e}")
    
    async def _create_progress_notification(
        self,
        user: User,
        notification_type: str,
        priority: str,
        title: str,
        message: str,
        data: Dict[str, Any] = None
    ) -> None:
        """Create progress notification"""
        try:
            notification = ProgressNotification.objects.create(
                user=user,
                notification_type=notification_type,
                priority=priority,
                title=title,
                message=message,
                data=data or {},
                is_sent=True,
                sent_at=timezone.now(),
                expires_at=timezone.now() + timedelta(days=7)  # Expire after 7 days
            )
            
            # Send real-time notification if user is active
            # This would integrate with the WebSocket service
            
        except Exception as e:
            print(f"Error creating progress notification: {e}")


class MonitoringManagementCommand(BaseCommand):
    """Django management command for background monitoring"""
    
    help = 'Start background monitoring service'
    
    def handle(self, *args, **options):
        """Handle the management command"""
        monitoring_service = BackgroundMonitoringService()
        
        self.stdout.write(
            self.style.SUCCESS('Starting background monitoring service...')
        )
        
        # Run monitoring service
        asyncio.run(monitoring_service.start_background_monitoring())