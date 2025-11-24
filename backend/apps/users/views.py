"""
Views for the users app.
"""

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    UserUpdateSerializer, UserStatsSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile.
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving user details.
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile details.
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_activity(request):
    """
    Update user activity timestamp.
    """
    user = request.user
    user.update_activity()
    return Response({'status': 'Activity updated'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard(request):
    """
    Get user dashboard data.
    """
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None
    
    data = {
        'user': UserSerializer(user).data,
        'profile': UserProfileSerializer(profile).data if profile else None,
        'activity': {
            'last_activity': user.last_activity,
            'streak_days': user.streak_days,
            'total_study_time': str(user.total_study_time) if user.total_study_time else None
        }
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def user_stats(request):
    """
    Get platform user statistics (admin only).
    """
    from django.db.models import Count, Q
    from datetime import timedelta
    
    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start - timedelta(days=30)
    
    stats = {
        'total_users': User.objects.count(),
        'active_users_today': User.objects.filter(last_activity__gte=today_start).count(),
        'active_users_week': User.objects.filter(last_activity__gte=week_start).count(),
        'active_users_month': User.objects.filter(last_activity__gte=month_start).count(),
        'new_users_today': User.objects.filter(date_joined__gte=today_start).count(),
        'new_users_week': User.objects.filter(date_joined__gte=week_start).count(),
        'new_users_month': User.objects.filter(date_joined__gte=month_start).count(),
    }
    
    serializer = UserStatsSerializer(stats)
    return Response(serializer.data)


class UserListView(generics.ListAPIView):
    """
    List all users (admin only).
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')


class UserSearchView(generics.ListAPIView):
    """
    Search users by username or email (admin only).
    """
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return User.objects.filter(
                Q(username__icontains=query) | 
                Q(email__icontains=query)
            ).order_by('-date_joined')
        return User.objects.none()
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)