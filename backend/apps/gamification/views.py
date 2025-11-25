"""
Gamification Views - JAC Learning Platform

API views for gamification system including achievements, badges, points, and streaks.

Author: MiniMax Agent
Created: 2025-11-26
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q, F
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

from .models import (
    Badge, UserBadge, Achievement, UserAchievement,
    UserPoints, PointTransaction, UserLevel, LearningStreak,
    LevelRequirement, AchievementProgress
)
from .serializers import (
    BadgeSerializer, UserBadgeSerializer, AchievementSerializer,
    UserAchievementSerializer, UserPointsSerializer, PointTransactionSerializer,
    UserLevelSerializer, LearningStreakSerializer, LevelRequirementSerializer,
    AchievementProgressSerializer, GamificationOverviewSerializer,
    GamificationStatsSerializer, LeaderboardSerializer,
    AddPointsSerializer, SpendPointsSerializer,
    UpdateAchievementProgressSerializer, RecordStreakActivitySerializer
)


class BadgeViewSet(viewsets.ModelViewSet):
    """Badge CRUD operations"""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter badges based on user permissions and active status"""
        queryset = super().get_queryset()
        
        # Only show active badges to regular users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by category if specified
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty if specified
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.order_by('category', 'difficulty', 'name')
    
    @action(detail=True, methods=['post'])
    def claim(self, request, pk=None):
        """Claim a badge manually (for admin/testing purposes)"""
        badge = self.get_object()
        user = request.user
        
        # Check if user already has this badge
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            return Response(
                {'error': 'Badge already claimed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user meets requirements
        user_points = UserPoints.objects.filter(user=user).first()
        if user_points and user_points.total_points < badge.minimum_points:
            return Response(
                {'error': f'Need {badge.minimum_points} points to claim this badge'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Award badge
        user_badge = UserBadge.objects.create(
            user=user,
            badge=badge,
            earned_through='manual_claim'
        )
        
        return Response(UserBadgeSerializer(user_badge).data, status=status.HTTP_201_CREATED)


class UserBadgeViewSet(viewsets.ModelViewSet):
    """User badge management"""
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's badges"""
        return UserBadge.objects.filter(user=self.request.user).select_related('badge')
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get user's badges grouped by category"""
        badges = self.get_queryset()
        categories = {}
        
        for badge in badges:
            category = badge.badge.category
            if category not in categories:
                categories[category] = []
            categories[category].append(UserBadgeSerializer(badge).data)
        
        return Response(categories)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recently earned badges"""
        recent_badges = self.get_queryset().order_by('-earned_at')[:10]
        return Response(UserBadgeSerializer(recent_badges, many=True).data)


class AchievementViewSet(viewsets.ModelViewSet):
    """Achievement CRUD operations"""
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter achievements based on user permissions and status"""
        queryset = super().get_queryset()
        
        # Only show active achievements to regular users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        
        # Filter by category if specified
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by difficulty if specified
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset.order_by('category', 'difficulty', 'unlock_order', 'title')
    
    @action(detail=True, methods=['post'])
    def start_tracking(self, request, pk=None):
        """Start tracking progress for an achievement"""
        achievement = self.get_object()
        user = request.user
        
        # Create or get achievement progress
        progress, created = AchievementProgress.objects.get_or_create(
            user=user,
            achievement=achievement,
            defaults={'target_count': achievement.criteria_value}
        )
        
        if not created:
            return Response(
                {'error': 'Already tracking this achievement'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(AchievementProgressSerializer(progress).data, status=status.HTTP_201_CREATED)


class UserAchievementViewSet(viewsets.ModelViewSet):
    """User achievement progress management"""
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's achievements"""
        return UserAchievement.objects.filter(user=self.request.user).select_related('achievement', 'badge_earned')
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        """Get achievements currently in progress"""
        achievements = self.get_queryset().filter(is_completed=False)
        return Response(UserAchievementSerializer(achievements, many=True).data)
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed achievements"""
        achievements = self.get_queryset().filter(is_completed=True)
        return Response(UserAchievementSerializer(achievements, many=True).data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get user's achievements grouped by category"""
        achievements = self.get_queryset()
        categories = {}
        
        for achievement in achievements:
            category = achievement.achievement.category
            if category not in categories:
                categories[category] = []
            categories[category].append(UserAchievementSerializer(achievement).data)
        
        return Response(categories)


class UserPointsViewSet(viewsets.ReadOnlyModelViewSet):
    """User points management (read-only for security)"""
    serializer_class = UserPointsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's points"""
        return UserPoints.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_points(self, request):
        """Add points to user account (admin action)"""
        serializer = AddPointsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_points = UserPoints.objects.get_or_create(user=request.user)[0]
                new_total = user_points.add_points(
                    amount=serializer.validated_data['amount'],
                    source=serializer.validated_data['source'],
                    metadata=serializer.validated_data.get('metadata', {})
                )
                
                return Response({
                    'message': f'Added {serializer.validated_data["amount"]} points',
                    'total_points': new_total
                })
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def spend_points(self, request):
        """Spend points from user account"""
        serializer = SpendPointsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user_points = UserPoints.objects.get(user=request.user)
                remaining = user_points.spend_points(
                    amount=serializer.validated_data['amount'],
                    purpose=serializer.validated_data['purpose'],
                    metadata=serializer.validated_data.get('metadata', {})
                )
                
                return Response({
                    'message': f'Spent {serializer.validated_data["amount"]} points',
                    'remaining_points': remaining
                })
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def transactions(self, request):
        """Get user's point transaction history"""
        transactions = PointTransaction.objects.filter(user=request.user).order_by('-created_at')[:50]
        return Response(PointTransactionSerializer(transactions, many=True).data)


class UserLevelViewSet(viewsets.ReadOnlyModelViewSet):
    """User level progression"""
    serializer_class = UserLevelSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's level info"""
        return UserLevel.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_xp(self, request):
        """Add experience points to user (admin action)"""
        amount = request.data.get('amount', 0)
        try:
            amount = int(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            user_level = UserLevel.objects.get_or_create(user=request.user)[0]
            user_level.add_xp(amount)
            
            return Response({
                'message': f'Added {amount} XP',
                'current_level': user_level.current_level,
                'current_xp': user_level.current_xp,
                'total_xp': user_level.total_xp
            })
        except (ValueError, TypeError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LearningStreakViewSet(viewsets.ReadOnlyModelViewSet):
    """Learning streak tracking"""
    serializer_class = LearningStreakSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's streak info"""
        return LearningStreak.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def record_activity(self, request):
        """Record learning activity for streak"""
        serializer = RecordStreakActivitySerializer(data=request.data)
        if serializer.is_valid():
            streak = LearningStreak.objects.get_or_create(user=request.user)[0]
            current_streak = streak.record_activity(
                activity_date=serializer.validated_data.get('activity_date')
            )
            
            return Response({
                'message': 'Activity recorded',
                'current_streak': current_streak,
                'longest_streak': streak.longest_streak
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AchievementProgressViewSet(viewsets.ModelViewSet):
    """Achievement progress tracking"""
    serializer_class = AchievementProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return user's achievement progress"""
        return AchievementProgress.objects.filter(user=self.request.user).select_related('achievement')
    
    @action(detail=True, methods=['post'])
    def increment(self, request, pk=None):
        """Increment achievement progress"""
        progress = self.get_object()
        increment_by = request.data.get('increment_by', 1)
        context = request.data.get('context', {})
        
        try:
            new_count = progress.increment(increment_by, context)
            return Response({
                'message': 'Progress updated',
                'current_count': new_count,
                'target_count': progress.target_count
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GamificationOverviewView(APIView):
    """Comprehensive gamification overview"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get comprehensive gamification overview for user"""
        user = request.user
        
        # Get or create gamification records
        user_points = UserPoints.objects.get_or_create(user=user)[0]
        user_level = UserLevel.objects.get_or_create(user=user)[0]
        streak = LearningStreak.objects.get_or_create(user=user)[0]
        
        # Get achievements stats
        total_achievements = Achievement.objects.filter(is_active=True).count()
        completed_achievements = UserAchievement.objects.filter(user=user, is_completed=True).count()
        
        # Get badges stats
        total_badges = Badge.objects.filter(is_active=True).count()
        earned_badges = UserBadge.objects.filter(user=user).count()
        
        # Get recent activity
        recent_achievements = UserAchievement.objects.filter(
            user=user
        ).select_related('achievement').order_by('-completed_at')[:5]
        
        recent_badges = UserBadge.objects.filter(
            user=user
        ).select_related('badge').order_by('-earned_at')[:5]
        
        data = {
            'total_points': user_points.total_points,
            'current_level': user_level.current_level,
            'current_streak': streak.current_streak,
            'total_achievements': total_achievements,
            'completed_achievements': completed_achievements,
            'total_badges': total_badges,
            'earned_badges': earned_badges,
            'recent_achievements': UserAchievementSerializer(recent_achievements, many=True).data,
            'recent_badges': UserBadgeSerializer(recent_badges, many=True).data,
            'current_level_info': UserLevelSerializer(user_level).data,
            'streak_info': LearningStreakSerializer(streak).data
        }
        
        return Response(data)


class LeaderboardView(APIView):
    """Leaderboard API"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get platform leaderboard"""
        leaderboard_type = request.query_params.get('type', 'points')
        limit = int(request.query_params.get('limit', 10))
        
        if leaderboard_type == 'points':
            users = UserPoints.objects.select_related('user').order_by('-total_points')[:limit]
        elif leaderboard_type == 'streak':
            users = LearningStreak.objects.select_related('user').order_by('-current_streak')[:limit]
        elif leaderboard_type == 'level':
            users = UserLevel.objects.select_related('user').order_by('-current_level', '-total_xp')[:limit]
        else:
            return Response({'error': 'Invalid leaderboard type'}, status=status.HTTP_400_BAD_REQUEST)
        
        leaderboard = []
        for rank, user in enumerate(users, 1):
            if leaderboard_type == 'points':
                leaderboard.append({
                    'user': user.user.username,
                    'rank': rank,
                    'total_points': user.total_points,
                    'current_level': UserLevel.objects.get_or_create(user=user.user)[0].current_level,
                    'current_streak': LearningStreak.objects.get_or_create(user=user.user)[0].current_streak
                })
            elif leaderboard_type == 'streak':
                leaderboard.append({
                    'user': user.user.username,
                    'rank': rank,
                    'total_points': UserPoints.objects.get_or_create(user=user.user)[0].total_points,
                    'current_level': UserLevel.objects.get_or_create(user=user.user)[0].current_level,
                    'current_streak': user.current_streak
                })
            elif leaderboard_type == 'level':
                leaderboard.append({
                    'user': user.user.username,
                    'rank': rank,
                    'total_points': UserPoints.objects.get_or_create(user=user.user)[0].total_points,
                    'current_level': user.current_level,
                    'current_streak': LearningStreak.objects.get_or_create(user=user.user)[0].current_streak
                })
        
        return Response(leaderboard)


class GamificationStatsView(APIView):
    """Platform-wide gamification statistics (admin only)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get platform gamification statistics"""
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        # Calculate statistics
        total_users = request.user.__class__.objects.count()
        active_users_today = request.user.__class__.objects.filter(
            last_login__date=timezone.now().date()
        ).count()
        
        total_achievements_completed = UserAchievement.objects.filter(is_completed=True).count()
        total_badges_earned = UserBadge.objects.count()
        
        avg_streak = LearningStreak.objects.aggregate(avg_streak=Avg('current_streak'))['avg_streak'] or 0
        total_points_earned = UserPoints.objects.aggregate(total_points=Sum('total_points'))['total_points'] or 0
        
        # Top performers
        top_users_points = UserPoints.objects.select_related('user').order_by('-total_points')[:10]
        top_users_streak = LearningStreak.objects.select_related('user').order_by('-current_streak')[:10]
        
        # Recent activity
        recent_achievements = UserAchievement.objects.filter(
            is_completed=True
        ).select_related('user', 'achievement').order_by('-completed_at')[:10]
        
        recent_badges = UserBadge.objects.filter(
            is_verified=True
        ).select_related('user', 'badge').order_by('-earned_at')[:10]
        
        data = {
            'total_users': total_users,
            'active_users_today': active_users_today,
            'total_achievements_completed': total_achievements_completed,
            'total_badges_earned': total_badges_earned,
            'average_streak': round(avg_streak, 1),
            'total_points_earned': total_points_earned,
            'top_users_by_points': [
                {
                    'user': user.user.username,
                    'rank': i + 1,
                    'total_points': user.total_points,
                    'current_level': UserLevel.objects.get_or_create(user=user.user)[0].current_level,
                    'current_streak': LearningStreak.objects.get_or_create(user=user.user)[0].current_streak
                }
                for i, user in enumerate(top_users_points)
            ],
            'top_users_by_streak': [
                {
                    'user': user.user.username,
                    'rank': i + 1,
                    'total_points': UserPoints.objects.get_or_create(user=user.user)[0].total_points,
                    'current_level': UserLevel.objects.get_or_create(user=user.user)[0].current_level,
                    'current_streak': user.current_streak
                }
                for i, user in enumerate(top_users_streak)
            ],
            'recent_achievements': UserAchievementSerializer(recent_achievements, many=True).data,
            'recent_badges': UserBadgeSerializer(recent_badges, many=True).data
        }
        
        return Response(data)


class GamificationIntegrationView(APIView):
    """Integration endpoints for other apps to interact with gamification"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, action):
        """Handle gamification actions from other apps"""
        if action == 'award_points':
            return self.award_points(request)
        elif action == 'update_streak':
            return self.update_streak(request)
        elif action == 'check_achievements':
            return self.check_achievements(request)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    def award_points(self, request):
        """Award points for an action"""
        amount = request.data.get('amount', 0)
        source = request.data.get('source', 'unknown')
        metadata = request.data.get('metadata', {})
        
        try:
            user_points = UserPoints.objects.get_or_create(user=request.user)[0]
            new_total = user_points.add_points(amount, source, metadata)
            
            return Response({
                'message': f'Awarded {amount} points',
                'new_total': new_total
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update_streak(self, request):
        """Update learning streak"""
        streak = LearningStreak.objects.get_or_create(user=request.user)[0]
        current_streak = streak.record_activity()
        
        return Response({
            'message': 'Streak updated',
            'current_streak': current_streak
        })
    
    def check_achievements(self, request):
        """Check and update achievement progress"""
        achievement_type = request.data.get('type')
        value = request.data.get('value', 0)
        
        # Find relevant achievements
        achievements = Achievement.objects.filter(
            criteria_type=achievement_type,
            is_active=True
        )
        
        updated_achievements = []
        
        for achievement in achievements:
            # Create or get achievement progress
            progress, created = AchievementProgress.objects.get_or_create(
                user=request.user,
                achievement=achievement,
                defaults={'target_count': achievement.criteria_value}
            )
            
            # Update progress
            old_count = progress.current_count
            new_count = progress.increment(value)
            
            if new_count > old_count:
                updated_achievements.append({
                    'achievement': achievement.title,
                    'progress': f"{new_count}/{achievement.criteria_value}",
                    'completed': progress.current_count >= progress.target_count
                })
        
        return Response({
            'message': 'Achievement progress updated',
            'updated_achievements': updated_achievements
        })