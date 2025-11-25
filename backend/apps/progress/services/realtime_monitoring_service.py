"""
Real-time Monitoring Service - JAC Learning Platform

This service provides real-time performance monitoring, WebSocket connections,
and live analytics for dashboard data feeds.

Author: MiniMax Agent
Created: 2025-11-26
"""

import json
import uuid
import asyncio
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ..models import ProgressSnapshot, LearningAnalytics, ProgressNotification
from apps.learning.models import UserModuleProgress, AssessmentAttempt


class RealtimeMonitoringService:
    """
    Service for real-time performance monitoring and dashboard data feeds
    """
    
    def __init__(self):
        self.active_sessions = {}  # Track active user sessions
        self.monitoring_thresholds = {
            'low_performance': 60.0,
            'high_performance': 90.0,
            'engagement_drop': 0.5,
            'consistency_threshold': 70.0
        }
        self.channel_layer = get_channel_layer()
    
    async def start_user_monitoring(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Start real-time monitoring for a user session"""
        try:
            # Initialize session tracking
            if user_id not in self.active_sessions:
                self.active_sessions[user_id] = {}
            
            self.active_sessions[user_id][session_id] = {
                'started_at': timezone.now(),
                'last_activity': timezone.now(),
                'activities': [],
                'performance_metrics': {},
                'alerts_triggered': set()
            }
            
            # Send initial dashboard data
            await self.send_initial_dashboard_data(user_id, session_id)
            
            # Start background monitoring task
            asyncio.create_task(self._monitor_user_session(user_id, session_id))
            
            return {
                'success': True,
                'session_id': session_id,
                'monitoring_started': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    async def stop_user_monitoring(self, user_id: int, session_id: str) -> Dict[str, Any]:
        """Stop real-time monitoring for a user session"""
        try:
            if user_id in self.active_sessions and session_id in self.active_sessions[user_id]:
                # Finalize session data
                await self._finalize_session_data(user_id, session_id)
                
                # Remove session
                del self.active_sessions[user_id][session_id]
                
                if not self.active_sessions[user_id]:
                    del self.active_sessions[user_id]
            
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def send_initial_dashboard_data(self, user_id: int, session_id: str) -> None:
        """Send initial dashboard data to user"""
        try:
            user = User.objects.get(id=user_id)
            
            # Get current progress data
            current_progress = await self._get_current_user_progress(user)
            
            # Get real-time metrics
            realtime_metrics = await self._calculate_realtime_metrics(user)
            
            # Prepare dashboard data
            dashboard_data = {
                'type': 'dashboard_initial_data',
                'session_id': session_id,
                'timestamp': timezone.now().isoformat(),
                'user_id': user_id,
                'progress_summary': current_progress,
                'realtime_metrics': realtime_metrics,
                'alerts': await self._get_user_alerts(user),
                'recommendations': await self._generate_realtime_recommendations(user)
            }
            
            # Send via WebSocket
            await self._send_to_user_channel(user_id, dashboard_data)
            
        except Exception as e:
            print(f"Error sending initial dashboard data: {e}")
    
    async def _monitor_user_session(self, user_id: int, session_id: str) -> None:
        """Background task to monitor user session"""
        monitoring_active = True
        
        while monitoring_active:
            try:
                # Check if session still exists
                if user_id not in self.active_sessions or session_id not in self.active_sessions[user_id]:
                    break
                
                session = self.active_sessions[user_id][session_id]
                
                # Update last activity
                session['last_activity'] = timezone.now()
                
                # Check for new activities
                await self._check_for_new_activities(user_id, session_id)
                
                # Update performance metrics
                await self._update_performance_metrics(user_id, session_id)
                
                # Check alerts and thresholds
                await self._check_alert_conditions(user_id, session_id)
                
                # Send periodic updates
                await self._send_periodic_update(user_id, session_id)
                
                # Sleep for 30 seconds before next check
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"Error in monitoring session {session_id}: {e}")
                await asyncio.sleep(60)  # Wait longer on error
    
    async def _check_for_new_activities(self, user_id: int, session_id: str) -> None:
        """Check for new user activities since last check"""
        session = self.active_sessions[user_id][session_id]
        last_check = session.get('last_activity_check', timezone.now() - timedelta(minutes=1))
        
        # Check for new progress activities
        new_progress = UserModuleProgress.objects.filter(
            user_id=user_id,
            updated_at__gt=last_check
        ).order_by('-updated_at')[:5]
        
        # Check for new assessment attempts
        new_assessments = AssessmentAttempt.objects.filter(
            user_id=user_id,
            completed_at__gt=last_check
        ).order_by('-completed_at')[:3]
        
        new_activities = []
        
        for progress in new_progress:
            new_activities.append({
                'type': 'progress_update',
                'module_id': progress.module.id,
                'module_title': progress.module.title,
                'status': progress.status,
                'score': progress.score,
                'timestamp': progress.updated_at.isoformat()
            })
        
        for assessment in new_assessments:
            new_activities.append({
                'type': 'assessment_completed',
                'assessment_id': assessment.assessment.id,
                'score': assessment.score,
                'max_score': assessment.max_score,
                'time_spent': str(assessment.time_spent),
                'timestamp': assessment.completed_at.isoformat() if assessment.completed_at else None
            })
        
        if new_activities:
            # Send new activities to user
            activity_update = {
                'type': 'new_activities',
                'activities': new_activities,
                'timestamp': timezone.now().isoformat()
            }
            
            await self._send_to_user_channel(user_id, activity_update)
            
            # Add to session activities
            session['activities'].extend(new_activities)
            
            # Keep only last 50 activities in memory
            if len(session['activities']) > 50:
                session['activities'] = session['activities'][-50:]
        
        # Update last check time
        session['last_activity_check'] = timezone.now()
    
    async def _update_performance_metrics(self, user_id: int, session_id: str) -> None:
        """Update real-time performance metrics"""
        try:
            user = User.objects.get(id=user_id)
            
            # Calculate updated metrics
            metrics = await self._calculate_realtime_metrics(user)
            
            # Store in session
            session = self.active_sessions[user_id][session_id]
            session['performance_metrics'] = metrics
            
            # Update cache for persistence
            cache_key = f"realtime_metrics_{user_id}"
            cache.set(cache_key, metrics, timeout=300)  # 5 minutes
            
        except Exception as e:
            print(f"Error updating performance metrics: {e}")
    
    async def _calculate_realtime_metrics(self, user: User) -> Dict[str, Any]:
        """Calculate real-time performance metrics"""
        # Get recent activities (last 24 hours)
        yesterday = timezone.now() - timedelta(days=1)
        
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=yesterday
        )
        
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=yesterday
        )
        
        # Calculate metrics
        daily_activities = recent_progress.count()
        daily_assessments = recent_assessments.count()
        
        # Performance metrics
        recent_scores = [a.score for a in recent_assessments if a.score is not None]
        avg_recent_score = round(np.mean(recent_scores), 2) if recent_scores else 0
        
        # Engagement metrics
        today_activities = recent_progress.filter(
            updated_at__gte=timezone.now().date()
        ).count()
        
        # Calculate trends (compare to previous period)
        two_days_ago = timezone.now() - timedelta(days=2)
        prev_day_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=two_days_ago,
            updated_at__lt=yesterday
        ).count()
        
        activity_trend = 'increasing' if today_activities > prev_day_progress else 'stable' if today_activities == prev_day_progress else 'decreasing'
        
        return {
            'daily_activities': daily_activities,
            'daily_assessments': daily_assessments,
            'average_recent_score': avg_recent_score,
            'activity_trend': activity_trend,
            'engagement_level': min(100, today_activities * 20),  # Simple engagement calculation
            'last_updated': timezone.now().isoformat()
        }
    
    async def _check_alert_conditions(self, user_id: int, session_id: str) -> None:
        """Check for alert conditions and trigger notifications"""
        try:
            user = User.objects.get(id=user_id)
            session = self.active_sessions[user_id][session_id]
            
            alerts = []
            
            # Check performance alert
            avg_recent_score = session['performance_metrics'].get('average_recent_score', 0)
            if avg_recent_score < self.monitoring_thresholds['low_performance'] and 'low_performance' not in session['alerts_triggered']:
                alerts.append({
                    'type': 'performance_alert',
                    'severity': 'warning',
                    'message': f'Recent performance dropped to {avg_recent_score}% - consider additional practice',
                    'timestamp': timezone.now().isoformat()
                })
                session['alerts_triggered'].add('low_performance')
            
            # Check engagement drop
            activity_trend = session['performance_metrics'].get('activity_trend', 'stable')
            if activity_trend == 'decreasing' and 'engagement_drop' not in session['alerts_triggered']:
                alerts.append({
                    'type': 'engagement_alert',
                    'severity': 'info',
                    'message': 'Learning activity has decreased - consider setting a study schedule',
                    'timestamp': timezone.now().isoformat()
                })
                session['alerts_triggered'].add('engagement_drop')
            
            # Check for achievements
            new_achievements = await self._check_new_achievements(user)
            if new_achievements:
                for achievement in new_achievements:
                    alerts.append({
                        'type': 'achievement_alert',
                        'severity': 'success',
                        'message': f'Achievement unlocked: {achievement}',
                        'timestamp': timezone.now().isoformat()
                    })
            
            # Send alerts if any
            if alerts:
                alert_message = {
                    'type': 'alert_notification',
                    'alerts': alerts,
                    'timestamp': timezone.now().isoformat()
                }
                
                await self._send_to_user_channel(user_id, alert_message)
                
                # Also store alerts in database
                for alert in alerts:
                    await self._store_alert_notification(user, alert)
            
        except Exception as e:
            print(f"Error checking alert conditions: {e}")
    
    async def _check_new_achievements(self, user: User) -> List[str]:
        """Check for new achievements based on recent activity"""
        achievements = []
        
        # Get recent progress
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            status='completed',
            updated_at__gte=timezone.now() - timedelta(days=1)
        )
        
        # Check for first completion achievement
        if recent_progress.exists() and not hasattr(user, '_checked_first_completion'):
            total_completed = UserModuleProgress.objects.filter(
                user=user,
                status='completed'
            ).count()
            
            if total_completed == 1:
                achievements.append('First Module Completed')
                user._checked_first_completion = True
        
        # Check for streak achievement
        streak_days = await self._calculate_learning_streak(user)
        if streak_days >= 7 and not hasattr(user, '_checked_week_streak'):
            achievements.append('7-Day Learning Streak')
            user._checked_week_streak = True
        elif streak_days >= 30 and not hasattr(user, '_checked_month_streak'):
            achievements.append('30-Day Learning Streak')
            user._checked_month_streak = True
        
        return achievements
    
    async def _calculate_learning_streak(self, user: User) -> int:
        """Calculate current learning streak in days"""
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
    
    async def _send_periodic_update(self, user_id: int, session_id: str) -> None:
        """Send periodic dashboard updates"""
        try:
            session = self.active_sessions[user_id][session_id]
            
            update_data = {
                'type': 'periodic_update',
                'session_id': session_id,
                'timestamp': timezone.now().isoformat(),
                'metrics': session['performance_metrics'],
                'recent_activities_count': len(session['activities']),
                'session_duration_minutes': int((timezone.now() - session['started_at']).total_seconds() / 60)
            }
            
            await self._send_to_user_channel(user_id, update_data)
            
        except Exception as e:
            print(f"Error sending periodic update: {e}")
    
    async def _send_to_user_channel(self, user_id: int, data: Dict[str, Any]) -> None:
        """Send data to user's WebSocket channel"""
        try:
            channel_name = f"user_{user_id}"
            await self.channel_layer.group_send(
                channel_name,
                {
                    'type': 'send_to_user',
                    'data': data
                }
            )
        except Exception as e:
            print(f"Error sending to user channel {user_id}: {e}")
    
    async def _get_current_user_progress(self, user: User) -> Dict[str, Any]:
        """Get current user progress summary"""
        total_modules = UserModuleProgress.objects.filter(user=user).count()
        completed_modules = UserModuleProgress.objects.filter(user=user, status='completed').count()
        
        progress_percentage = (completed_modules / max(total_modules, 1)) * 100
        
        return {
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'progress_percentage': round(progress_percentage, 2),
            'current_level': self._determine_learning_level(progress_percentage)
        }
    
    def _determine_learning_level(self, progress_percentage: float) -> str:
        """Determine learning level based on progress"""
        if progress_percentage >= 90:
            return 'Expert'
        elif progress_percentage >= 75:
            return 'Advanced'
        elif progress_percentage >= 50:
            return 'Intermediate'
        elif progress_percentage >= 25:
            return 'Developing'
        else:
            return 'Beginner'
    
    async def _get_user_alerts(self, user: User) -> List[Dict[str, Any]]:
        """Get recent alerts for user"""
        recent_notifications = ProgressNotification.objects.filter(
            user=user,
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).order_by('-created_at')[:5]
        
        return [
            {
                'type': notification.notification_type,
                'title': notification.title,
                'message': notification.message,
                'priority': notification.priority,
                'timestamp': notification.created_at.isoformat()
            }
            for notification in recent_notifications
        ]
    
    async def _generate_realtime_recommendations(self, user: User) -> List[str]:
        """Generate real-time recommendations"""
        recommendations = []
        
        # Get recent performance
        recent_assessments = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=timezone.now() - timedelta(days=7)
        )
        
        if recent_assessments.exists():
            avg_score = recent_assessments.aggregate(Avg('score'))['score__avg'] or 0
            
            if avg_score < 70:
                recommendations.append("Focus on practice exercises to improve understanding")
            elif avg_score > 85:
                recommendations.append("Great performance! Consider tackling advanced challenges")
        
        return recommendations
    
    async def _finalize_session_data(self, user_id: int, session_id: str) -> None:
        """Finalize session data before cleanup"""
        try:
            session = self.active_sessions[user_id][session_id]
            
            # Create progress snapshot
            user = User.objects.get(id=user_id)
            
            ProgressSnapshot.objects.create(
                user=user,
                snapshot_date=timezone.now(),
                total_activities=len(session['activities']),
                session_count=1
            )
            
        except Exception as e:
            print(f"Error finalizing session data: {e}")
    
    async def _store_alert_notification(self, user: User, alert_data: Dict[str, Any]) -> None:
        """Store alert notification in database"""
        try:
            ProgressNotification.objects.create(
                user=user,
                notification_type=alert_data['type'],
                priority=alert_data.get('severity', 'normal'),
                title=alert_data.get('message', 'Alert'),
                message=alert_data['message'],
                is_sent=True,
                sent_at=timezone.now()
            )
        except Exception as e:
            print(f"Error storing alert notification: {e}")


import numpy as np
from scipy import stats