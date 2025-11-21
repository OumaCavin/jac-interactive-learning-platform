"""
API views for the Users app.
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from .models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, LearningSummarySerializer
)


class UserRegistrationView(APIView):
    """User registration endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    """User login endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        """Authenticate user and return tokens."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Update last login timestamp
            user.last_login_at = timezone.now()
            user.update_streak()
            user.save(update_fields=['last_login_at', 'current_streak', 'longest_streak'])
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
            
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """User profile management endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get current user profile."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        """Update user profile."""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        """Partially update user profile."""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """Detailed user information endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id=None):
        """Get user details by ID or current user."""
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
        
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LearningSummaryView(APIView):
    """Learning progress summary endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id=None):
        """Get learning progress summary."""
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
        
        summary = user.get_learning_summary()
        serializer = LearningSummarySerializer(summary)
        return Response(serializer.data)


class UserSettingsView(APIView):
    """User settings management endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user settings."""
        user = request.user
        settings = {
            'learning_style': user.learning_style,
            'preferred_difficulty': user.preferred_difficulty,
            'learning_pace': user.learning_pace,
            'agent_interaction_level': user.agent_interaction_level,
            'preferred_feedback_style': user.preferred_feedback_style,
            'dark_mode': user.dark_mode,
            'notifications_enabled': user.notifications_enabled,
            'email_notifications': user.email_notifications,
            'push_notifications': user.push_notifications,
        }
        return Response(settings)
    
    def put(self, request):
        """Update user settings."""
        user = request.user
        
        # Update allowed settings
        allowed_settings = [
            'learning_style', 'preferred_difficulty', 'learning_pace',
            'agent_interaction_level', 'preferred_feedback_style',
            'dark_mode', 'notifications_enabled', 'email_notifications', 'push_notifications'
        ]
        
        for setting, value in request.data.items():
            if setting in allowed_settings:
                setattr(user, setting, value)
        
        user.save()
        return Response({'message': 'Settings updated successfully'})


class UserStatsView(APIView):
    """User statistics endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user statistics."""
        user = request.user
        
        stats = {
            'total_points': user.total_points,
            'level': user.level,
            'experience_level': user.experience_level,
            'next_level_points': user.next_level_points,
            'modules_completed': user.total_modules_completed,
            'current_streak': user.current_streak,
            'longest_streak': user.longest_streak,
            'total_time_spent_hours': user.total_time_spent.total_seconds() / 3600,
            'achievements_count': len(user.achievements),
            'badges_count': len(user.badges),
            'created_at': user.created_at,
            'last_activity_at': user.last_activity_at,
        }
        
        return Response(stats)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """Get current authenticated user."""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token."""
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)