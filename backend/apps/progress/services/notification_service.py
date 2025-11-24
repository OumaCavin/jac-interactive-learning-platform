"""
Notification Service - JAC Learning Platform

This service handles progress-related notifications, alerts, and messaging
for the JAC Interactive Learning Platform.

Author: MiniMax Agent
Created: 2025-11-25
"""

import uuid
from typing import Dict, Any, Optional, List
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta
import logging

from ..models import ProgressNotification
from apps.learning.models import UserModuleProgress, UserAssessmentResult

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service class for progress notification operations
    """
    
    def __init__(self):
        self.notification_templates = {
            'milestone_achieved': {
                'title': 'Milestone Achieved!',
                'message': 'Congratulations on reaching {percentage}% completion!'
            },
            'goal_completed': {
                'title': 'Goal Completed',
                'message': 'Great job! You have completed your goal: {goal_title}'
            },
            'achievement_unlocked': {
                'title': 'Achievement Unlocked',
                'message': 'You have unlocked the "{achievement_name}" achievement!'
            },
            'streak_warning': {
                'title': 'Learning Streak at Risk',
                'message': 'Your {streak_days}-day learning streak is at risk. Keep learning!'
            },
            'completion_prediction': {
                'title': 'Learning Path Completion Prediction',
                'message': 'Based on your progress, you may complete this path in {days} days.'
            }
        }
    
    def create_notification(
        self,
        user: User,
        notification_type: str,
        title: str,
        message: str,
        priority: str = 'normal',
        data: Optional[Dict[str, Any]] = None,
        expires_at: Optional[datetime] = None
    ) -> ProgressNotification:
        """
        Create a new progress notification
        
        Args:
            user: The user to notify
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            priority: Priority level (low, normal, high, urgent)
            data: Additional data for the notification
            expires_at: When notification expires
        
        Returns:
            ProgressNotification instance
        """
        try:
            notification = ProgressNotification.objects.create(
                user=user,
                notification_type=notification_type,
                priority=priority,
                title=title,
                message=message,
                data=data or {},
                expires_at=expires_at
            )
            
            logger.info(f"Created {notification_type} notification for user {user.username}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification for user {user.username}: {str(e)}")
            raise
    
    def send_milestone_notification(
        self,
        user: User,
        milestone_type: str,
        milestone_value: float,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> ProgressNotification:
        """
        Send milestone achievement notification
        
        Args:
            user: The user to notify
            milestone_type: Type of milestone (completion_percentage, score, etc.)
            milestone_value: Value achieved
            additional_data: Additional milestone data
        
        Returns:
            ProgressNotification instance
        """
        if milestone_type == 'completion_percentage':
            title = self.notification_templates['milestone_achieved']['title']
            message = self.notification_templates['milestone_achieved']['message'].format(
                percentage=int(milestone_value)
            )
            priority = 'high' if milestone_value >= 100 else 'normal'
        elif milestone_type == 'perfect_score':
            title = 'Perfect Score Achievement!'
            message = f"Outstanding! You achieved a perfect score of {milestone_value}%."
            priority = 'high'
        else:
            title = 'Achievement Unlocked'
            message = f"You have reached {milestone_value} in {milestone_type}."
            priority = 'normal'
        
        data = {
            'milestone_type': milestone_type,
            'milestone_value': milestone_value,
            **(additional_data or {})
        }
        
        return self.create_notification(
            user=user,
            notification_type='milestone_achieved',
            title=title,
            message=message,
            priority=priority,
            data=data
        )
    
    def send_goal_completion_notification(
        self,
        user: User,
        goal_title: str,
        goal_data: Optional[Dict[str, Any]] = None
    ) -> ProgressNotification:
        """
        Send goal completion notification
        
        Args:
            user: The user to notify
            goal_title: Title of completed goal
            goal_data: Additional goal data
        
        Returns:
            ProgressNotification instance
        """
        title = self.notification_templates['goal_completed']['title']
        message = self.notification_templates['goal_completed']['message'].format(
            goal_title=goal_title
        )
        
        data = {
            'goal_title': goal_title,
            **(goal_data or {})
        }
        
        return self.create_notification(
            user=user,
            notification_type='goal_completed',
            title=title,
            message=message,
            priority='high',
            data=data
        )
    
    def send_achievement_notification(
        self,
        user: User,
        achievement_name: str,
        achievement_data: Optional[Dict[str, Any]] = None
    ) -> ProgressNotification:
        """
        Send achievement unlocked notification
        
        Args:
            user: The user to notify
            achievement_name: Name of unlocked achievement
            achievement_data: Additional achievement data
        
        Returns:
            ProgressNotification instance
        """
        title = self.notification_templates['achievement_unlocked']['title']
        message = self.notification_templates['achievement_unlocked']['message'].format(
            achievement_name=achievement_name
        )
        
        data = {
            'achievement_name': achievement_name,
            **(achievement_data or {})
        }
        
        return self.create_notification(
            user=user,
            notification_type='achievement_unlocked',
            title=title,
            message=message,
            priority='normal',
            data=data
        )
    
    def send_streak_warning_notification(
        self,
        user: User,
        streak_days: int,
        last_activity_date: Optional[datetime] = None
    ) -> ProgressNotification:
        """
        Send learning streak warning notification
        
        Args:
            user: The user to notify
            streak_days: Current streak length
            last_activity_date: Date of last activity
        
        Returns:
            ProgressNotification instance
        """
        title = self.notification_templates['streak_warning']['title']
        message = self.notification_templates['streak_warning']['message'].format(
            streak_days=streak_days
        )
        
        data = {
            'streak_days': streak_days,
            'last_activity_date': last_activity_date.isoformat() if last_activity_date else None,
            'warning_threshold': 3  # Days without activity before warning
        }
        
        # Set expiration for streak warnings (1 day)
        expires_at = timezone.now() + timedelta(days=1)
        
        return self.create_notification(
            user=user,
            notification_type='streak_warning',
            title=title,
            message=message,
            priority='high',
            data=data,
            expires_at=expires_at
        )
    
    def send_completion_prediction_notification(
        self,
        user: User,
        predicted_days: int,
        learning_path_title: str,
        confidence_level: float
    ) -> ProgressNotification:
        """
        Send completion prediction notification
        
        Args:
            user: The user to notify
            predicted_days: Predicted days to completion
            learning_path_title: Title of learning path
            confidence_level: Confidence in prediction (0-1)
        
        Returns:
            ProgressNotification instance
        """
        title = self.notification_templates['completion_prediction']['title']
        message = self.notification_templates['completion_prediction']['message'].format(
            days=predicted_days
        )
        
        # Add confidence-based messaging
        if confidence_level >= 0.8:
            message += " This prediction is highly confident based on your learning pattern."
        elif confidence_level >= 0.5:
            message += " This prediction is moderately confident."
        else:
            message += " This is a rough estimate based on limited data."
        
        data = {
            'predicted_days': predicted_days,
            'learning_path_title': learning_path_title,
            'confidence_level': confidence_level,
            'prediction_date': timezone.now().isoformat()
        }
        
        # Set expiration for predictions (3 days)
        expires_at = timezone.now() + timedelta(days=3)
        
        return self.create_notification(
            user=user,
            notification_type='completion_prediction',
            title=title,
            message=message,
            priority='normal',
            data=data,
            expires_at=expires_at
        )
    
    def check_and_send_streak_warnings(self, user: User) -> List[ProgressNotification]:
        """
        Check user's learning streak and send warnings if needed
        
        Args:
            user: The user to check
        
        Returns:
            List of created notifications
        """
        notifications = []
        
        try:
            # Get last activity date
            last_activity = UserModuleProgress.objects.filter(
                user=user
            ).order_by('-updated_at').first()
            
            if not last_activity:
                return notifications
            
            last_activity_date = last_activity.updated_at.date()
            days_since_activity = (timezone.now().date() - last_activity_date).days
            
            # Send warning if 3 days since last activity and no existing warning
            if days_since_activity == 3:
                existing_warning = ProgressNotification.objects.filter(
                    user=user,
                    notification_type='streak_warning',
                    is_read=False,
                    expires_at__gte=timezone.now()
                ).exists()
                
                if not existing_warning:
                    notification = self.send_streak_warning_notification(
                        user=user,
                        streak_days=days_since_activity,
                        last_activity_date=last_activity.updated_at
                    )
                    notifications.append(notification)
            
        except Exception as e:
            logger.error(f"Error checking streak warnings for user {user.username}: {str(e)}")
        
        return notifications
    
    def send_progress_recommendation(
        self,
        user: User,
        recommendation_text: str,
        recommendation_type: str = 'general',
        priority: str = 'normal'
    ) -> ProgressNotification:
        """
        Send progress recommendation notification
        
        Args:
            user: The user to notify
            recommendation_text: The recommendation message
            recommendation_type: Type of recommendation
            priority: Priority level
        
        Returns:
            ProgressNotification instance
        """
        title = f"Learning Recommendation: {recommendation_type.title()}"
        
        data = {
            'recommendation_type': recommendation_type,
            'recommendation_category': 'progress'
        }
        
        return self.create_notification(
            user=user,
            notification_type='recommendation',
            title=title,
            message=recommendation_text,
            priority=priority,
            data=data,
            expires_at=timezone.now() + timedelta(days=7)  # Expire in 1 week
        )
    
    def get_user_notifications(
        self,
        user: User,
        limit: int = 50,
        unread_only: bool = False,
        notification_type: Optional[str] = None
    ) -> List[ProgressNotification]:
        """
        Get notifications for a user
        
        Args:
            user: The user to get notifications for
            limit: Maximum number of notifications to return
            unread_only: Whether to return only unread notifications
            notification_type: Optional filter by notification type
        
        Returns:
            List of notifications
        """
        queryset = ProgressNotification.objects.filter(
            user=user,
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        )
        
        if unread_only:
            queryset = queryset.filter(is_read=False)
        
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        return list(queryset.order_by('-created_at')[:limit])
    
    def mark_notification_read(self, notification_id: str, user: User) -> bool:
        """
        Mark a notification as read
        
        Args:
            notification_id: ID of the notification
            user: The user who owns the notification
        
        Returns:
            True if successful, False otherwise
        """
        try:
            notification = ProgressNotification.objects.get(
                id=notification_id,
                user=user
            )
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
            return True
        except ProgressNotification.DoesNotExist:
            return False
    
    def mark_all_notifications_read(self, user: User) -> int:
        """
        Mark all user notifications as read
        
        Args:
            user: The user whose notifications to mark as read
        
        Returns:
            Number of notifications marked as read
        """
        updated_count = ProgressNotification.objects.filter(
            user=user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return updated_count
    
    def clean_expired_notifications(self) -> int:
        """
        Clean up expired notifications
        
        Returns:
            Number of notifications cleaned up
        """
        deleted_count = ProgressNotification.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()[0]
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} expired notifications")
        
        return deleted_count
    
    def get_notification_summary(self, user: User) -> Dict[str, Any]:
        """
        Get a summary of user notifications
        
        Args:
            user: The user to get summary for
        
        Returns:
            Dict containing notification summary
        """
        total_notifications = ProgressNotification.objects.filter(
            user=user
        ).count()
        
        unread_notifications = ProgressNotification.objects.filter(
            user=user,
            is_read=False,
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        ).count()
        
        # Group by type
        notifications_by_type = {}
        for notification in ProgressNotification.objects.filter(
            user=user,
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        ):
            notif_type = notification.notification_type
            if notif_type not in notifications_by_type:
                notifications_by_type[notif_type] = 0
            notifications_by_type[notif_type] += 1
        
        # Group by priority
        notifications_by_priority = {}
        for notification in ProgressNotification.objects.filter(
            user=user,
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        ):
            priority = notification.priority
            if priority not in notifications_by_priority:
                notifications_by_priority[priority] = 0
            notifications_by_priority[priority] += 1
        
        return {
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'read_notifications': total_notifications - unread_notifications,
            'notifications_by_type': notifications_by_type,
            'notifications_by_priority': notifications_by_priority,
            'last_notification_date': self._get_last_notification_date(user)
        }
    
    def _get_last_notification_date(self, user: User) -> Optional[str]:
        """Get the date of the last notification for a user"""
        last_notification = ProgressNotification.objects.filter(
            user=user
        ).order_by('-created_at').first()
        
        if last_notification:
            return last_notification.created_at.isoformat()
        return None