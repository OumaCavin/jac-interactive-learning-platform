"""
Progress App Views - JAC Learning Platform

This module provides Django REST Framework views for progress tracking,
analytics, and user progress management in the JAC Interactive Learning Platform.

ViewSets:
- ProgressSnapshotViewSet: Manage user progress snapshots
- LearningAnalyticsViewSet: Handle learning analytics data
- AchievementViewSet: Manage achievements and user achievements
- UserProgressMetricViewSet: Track individual user metrics
- ProgressGoalViewSet: Manage user learning goals
- ProgressNotificationViewSet: Handle progress notifications

API Views:
- ProgressSummaryAPIView: Get comprehensive progress summary
- ProgressAnalyticsAPIView: Generate advanced analytics
- CreateProgressSnapshotAPIView: Create new progress snapshots
- TrackUserProgressAPIView: Track real-time user progress

Author: Cavin Otieno
Created: 2025-11-25
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Avg, Count, Q, Sum, Max, Min
from django.db.models.functions import TruncDate
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import PermissionDenied

from .models import (
    ProgressSnapshot, LearningAnalytics, Achievement, UserProgressMetric,
    ProgressGoal, ProgressNotification
)
from .serializers import (
    ProgressSnapshotSerializer, LearningAnalyticsSerializer, AchievementSerializer,
    UserProgressMetricSerializer, ProgressGoalSerializer, ProgressNotificationSerializer,
    ProgressSummarySerializer, ProgressAnalyticsSerializer,
    ProgressSnapshotCreateSerializer, LearningAnalyticsCreateSerializer,
    ProgressGoalCreateSerializer
)
from .services.progress_service import ProgressService
from .services.analytics_service import AnalyticsService


class ProgressSnapshotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user progress snapshots
    """
    serializer_class = ProgressSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = ProgressSnapshot.objects.filter(user=user)
        
        # Filter by learning path
        learning_path_id = self.request.query_params.get('learning_path_id')
        if learning_path_id:
            queryset = queryset.filter(learning_path_id=learning_path_id)
        
        # Filter by module
        module_id = self.request.query_params.get('module_id')
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(snapshot_date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(snapshot_date__lte=end_date)
            except ValueError:
                pass
        
        # Only return milestones if requested
        milestones_only = self.request.query_params.get('milestones_only')
        if milestones_only == 'true':
            queryset = queryset.filter(is_milestone=True)
        
        return queryset.order_by('-snapshot_date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_snapshot(self, request):
        """
        Create a new progress snapshot for the current user
        """
        serializer = ProgressSnapshotCreateSerializer(data=request.data)
        if serializer.is_valid():
            progress_service = ProgressService()
            snapshot = progress_service.create_user_snapshot(
                user=request.user,
                learning_path_id=serializer.validated_data.get('learning_path_id'),
                module_id=serializer.validated_data.get('module_id'),
                force=serializer.validated_data.get('force_snapshot', False)
            )
            
            response_serializer = ProgressSnapshotSerializer(snapshot)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest progress snapshot
        """
        latest_snapshot = self.get_queryset().first()
        if latest_snapshot:
            serializer = self.get_serializer(latest_snapshot)
            return Response(serializer.data)
        return Response({"message": "No snapshots found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        Get progress trends over time
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No progress data available"})
        
        # Group by date and calculate averages
        trends_data = queryset.annotate(
            date=TruncDate('snapshot_date')
        ).values('date').annotate(
            avg_completion=Avg('completion_percentage'),
            avg_score=Avg('average_score'),
            total_snapshots=Count('id')
        ).order_by('date')
        
        return Response(list(trends_data))


class LearningAnalyticsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for learning analytics data
    """
    serializer_class = LearningAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = LearningAnalytics.objects.filter(user=user)
        
        # Filter by learning path
        learning_path_id = self.request.query_params.get('learning_path_id')
        if learning_path_id:
            queryset = queryset.filter(learning_path_id=learning_path_id)
        
        # Filter by time period
        period_days = self.request.query_params.get('period_days')
        if period_days:
            try:
                days = int(period_days)
                start_date = timezone.now() - timedelta(days=days)
                queryset = queryset.filter(period_start__gte=start_date)
            except ValueError:
                pass
        
        return queryset.order_by('-period_end')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_analytics(self, request):
        """
        Generate new learning analytics for the current user
        """
        serializer = LearningAnalyticsCreateSerializer(data=request.data)
        if serializer.is_valid():
            analytics_service = AnalyticsService()
            analytics = analytics_service.generate_user_analytics(
                user=request.user,
                learning_path_id=serializer.validated_data.get('learning_path_id'),
                time_period_days=serializer.validated_data.get('time_period_days', 30),
                analytics_type=serializer.validated_data.get('analytics_type', 'comprehensive')
            )
            
            response_serializer = LearningAnalyticsSerializer(analytics)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest analytics report
        """
        latest_analytics = self.get_queryset().first()
        if latest_analytics:
            serializer = self.get_serializer(latest_analytics)
            return Response(serializer.data)
        return Response({"message": "No analytics data found"}, status=status.HTTP_404_NOT_FOUND)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing achievements (read-only for now)
    """
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Achievement.objects.filter(is_active=True)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.order_by('category', 'difficulty', 'name')
    
    @action(detail=False, methods=['get'])
    def my_achievements(self, request):
        """
        Get current user's achievements (placeholder implementation)
        """
        # This would be implemented when UserAchievement model exists
        return Response({"message": "Achievement tracking not yet implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED)


class UserProgressMetricViewSet(viewsets.ModelViewSet):
    """
    ViewSet for individual user progress metrics
    """
    serializer_class = UserProgressMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = UserProgressMetric.objects.filter(user=user)
        
        # Filter by learning path
        learning_path_id = self.request.query_params.get('learning_path_id')
        if learning_path_id:
            queryset = queryset.filter(learning_path_id=learning_path_id)
        
        # Filter by metric type
        metric_type = self.request.query_params.get('metric_type')
        if metric_type:
            queryset = queryset.filter(metric_type=metric_type)
        
        return queryset.order_by('-last_updated')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get summary of all user metrics
        """
        metrics = self.get_queryset()
        if not metrics.exists():
            return Response({"message": "No progress metrics found"}, status=status.HTTP_404_NOT_FOUND)
        
        summary_data = {}
        for metric in metrics:
            metric_type = metric.metric_type
            summary_data[metric_type] = {
                'current_value': metric.current_value,
                'target_value': metric.target_value,
                'progress_percentage': metric.progress_percentage,
                'trend_direction': metric.trend_direction,
                'is_improving': metric.is_improving
            }
        
        return Response(summary_data)


class ProgressGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user progress goals
    """
    serializer_class = ProgressGoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = ProgressGoal.objects.filter(user=user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by learning path
        learning_path_id = self.request.query_params.get('learning_path_id')
        if learning_path_id:
            queryset = queryset.filter(learning_path_id=learning_path_id)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter overdue goals
        overdue_only = self.request.query_params.get('overdue_only')
        if overdue_only == 'true':
            queryset = queryset.filter(
                status='active',
                target_date__lt=timezone.now().date()
            )
        
        return queryset.order_by('priority', 'target_date')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProgressGoalCreateSerializer
        return ProgressGoalSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Mark a goal as completed
        """
        goal = self.get_object()
        goal.status = 'completed'
        goal.completed_date = timezone.now().date()
        goal.current_value = goal.target_value
        goal.save()
        
        serializer = self.get_serializer(goal)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        """
        Update goal progress
        """
        goal = self.get_object()
        new_value = request.data.get('current_value')
        
        if new_value is not None:
            try:
                goal.current_value = int(new_value)
                if goal.current_value >= goal.target_value:
                    goal.status = 'completed'
                    goal.completed_date = timezone.now().date()
                goal.save()
                
                serializer = self.get_serializer(goal)
                return Response(serializer.data)
            except (ValueError, TypeError):
                return Response(
                    {"error": "Invalid current_value provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {"error": "current_value is required"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """
        Get goal dashboard data
        """
        goals = self.get_queryset()
        
        dashboard_data = {
            'total_goals': goals.count(),
            'active_goals': goals.filter(status='active').count(),
            'completed_goals': goals.filter(status='completed').count(),
            'overdue_goals': goals.filter(
                status='active',
                target_date__lt=timezone.now().date()
            ).count(),
            'high_priority_goals': goals.filter(priority='high', status='active').count(),
            'goals_by_category': {}
        }
        
        # Group goals by learning path
        for goal in goals:
            path_title = goal.learning_path.title if goal.learning_path else 'General'
            if path_title not in dashboard_data['goals_by_category']:
                dashboard_data['goals_by_category'][path_title] = 0
            dashboard_data['goals_by_category'][path_title] += 1
        
        return Response(dashboard_data)


class ProgressNotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for progress notifications
    """
    serializer_class = ProgressNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = ProgressNotification.objects.filter(user=user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by notification type
        notification_type = self.request.query_params.get('notification_type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Only show unexpired notifications
        queryset = queryset.filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
        )
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark notification as read
        """
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Mark all user notifications as read
        """
        notifications = self.get_queryset().filter(is_read=False)
        count = notifications.update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            "message": f"Marked {count} notifications as read"
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications
        """
        unread_count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": unread_count})


class ProgressSummaryAPIView(APIView):
    """
    API View for comprehensive progress summary
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get comprehensive progress summary for the current user
        """
        progress_service = ProgressService()
        summary_data = progress_service.generate_comprehensive_summary(
            user=request.user
        )
        
        serializer = ProgressSummarySerializer(summary_data)
        return Response(serializer.data)


class ProgressAnalyticsAPIView(APIView):
    """
    API View for advanced progress analytics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get advanced progress analytics for the current user
        """
        learning_path_id = request.query_params.get('learning_path_id')
        time_period_days = int(request.query_params.get('time_period_days', 30))
        analytics_type = request.query_params.get('analytics_type', 'comprehensive')
        
        analytics_service = AnalyticsService()
        analytics_data = analytics_service.generate_comprehensive_analytics(
            user=request.user,
            learning_path_id=learning_path_id,
            time_period_days=time_period_days,
            analytics_type=analytics_type
        )
        
        serializer = ProgressAnalyticsSerializer(analytics_data)
        return Response(serializer.data)


class CreateProgressSnapshotAPIView(APIView):
    """
    API View for creating progress snapshots
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Create a new progress snapshot
        """
        serializer = ProgressSnapshotCreateSerializer(data=request.data)
        if serializer.is_valid():
            progress_service = ProgressService()
            snapshot = progress_service.create_user_snapshot(
                user=request.user,
                learning_path_id=serializer.validated_data.get('learning_path_id'),
                module_id=serializer.validated_data.get('module_id'),
                force=serializer.validated_data.get('force_snapshot', False)
            )
            
            response_serializer = ProgressSnapshotSerializer(snapshot)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackUserProgressAPIView(APIView):
    """
    API View for real-time progress tracking
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Track user progress in real-time
        """
        activity_type = request.data.get('activity_type')
        entity_id = request.data.get('entity_id')
        score = request.data.get('score')
        time_spent = request.data.get('time_spent')
        
        if not activity_type or not entity_id:
            return Response(
                {"error": "activity_type and entity_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        progress_service = ProgressService()
        result = progress_service.track_user_activity(
            user=request.user,
            activity_type=activity_type,
            entity_id=entity_id,
            score=score,
            time_spent=time_spent
        )
        
        return Response(result)


# Utility functions for ViewSet methods
def get_object_or_404(queryset, **kwargs):
    """
    Utility function to get object or return 404
    """
    try:
        return queryset.get(**kwargs)
    except queryset.model.DoesNotExist:
        from django.shortcuts import get_object_or_404 as django_get_object_or_404
        return django_get_object_or_404(queryset, **kwargs)