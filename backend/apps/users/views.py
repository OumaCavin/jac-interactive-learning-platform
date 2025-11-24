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
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

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
            
            # Generate verification URL
            current_site = get_current_site(request)
            verification_url = f"{request.scheme}://{current_site.domain}/api/users/verify-email/?token={user.verification_token}"
            
            # Send verification email via Celery task
            try:
                from config.celery import send_email_verification_task
                send_email_verification_task.delay(user.id, verification_url)
            except Exception as e:
                # If Celery task fails, log the error but don't fail registration
                print(f"Failed to queue email verification task: {e}")
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'Account created successfully! Please check your email to verify your account.'
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
        
        # Use UserSerializer to return complete user settings data
        serializer = UserSerializer(user)
        settings_data = serializer.data
        
        # Return complete user settings including all required fields
        return Response(settings_data)
    
    def put(self, request):
        """Update user settings."""
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            # Return the updated user data
            updated_user = UserSerializer(user)
            return Response(updated_user.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        """Partially update user settings."""
        return self.put(request)
    
    def post(self, request):
        """Reset user settings to defaults."""
        user = request.user
        
        # Reset settings to defaults
        user.learning_style = 'visual'
        user.preferred_difficulty = 'beginner'
        user.learning_pace = 'moderate'
        user.agent_interaction_level = 'moderate'
        user.preferred_feedback_style = 'detailed'
        user.dark_mode = True
        user.notifications_enabled = True
        user.email_notifications = True
        user.push_notifications = True
        user.current_goal = ''
        user.goal_deadline = None
        
        user.save()
        
        # Return the reset settings
        serializer = UserSerializer(user)
        return Response({
            'message': 'Settings reset to defaults successfully',
            'settings': serializer.data
        })


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
        # Check if refresh token is provided
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            # If no refresh token, just clear session and return success
            return Response({
                "message": "Logged out successfully"
            }, status=status.HTTP_200_OK)
        
        # Try to blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            "message": "Logged out successfully"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        # Even if blacklisting fails, we should still consider logout successful
        # This prevents users from being stuck in logged-out state
        return Response({
            "message": "Logged out successfully"
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request):
    """Verify user email address using verification token."""
    token = request.GET.get('token')
    
    if not token:
        return Response({
            'error': 'Verification token is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Find user by verification token
        user = User.objects.get(verification_token=token)
        
        # Check if token is expired (24 hours)
        if user.verification_token_expires_at and user.verification_token_expires_at < timezone.now():
            return Response({
                'error': 'Verification token has expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark user as verified
        user.is_verified = True
        user.verification_token = None  # Clear the token
        user.verification_token_expires_at = None
        user.save()
        
        return Response({
            'message': 'Email verified successfully! You can now login to your account.',
            'verified': True
        }, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response({
            'error': 'Invalid verification token'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def resend_verification_email(request):
    """Resend email verification to user."""
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email address is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email.lower())
        
        if user.is_verified:
            return Response({
                'message': 'Email is already verified.'
            }, status=status.HTTP_200_OK)
        
        # Generate new verification URL
        current_site = get_current_site(request)
        verification_url = f"{request.scheme}://{current_site.domain}/api/users/verify-email/?token={user.verification_token}"
        
        # Send verification email via Celery task
        try:
            from config.celery import send_email_verification_task
            send_email_verification_task.delay(user.id, verification_url)
            
            return Response({
                'message': 'Verification email has been sent. Please check your inbox.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to send verification email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except User.DoesNotExist:
        return Response({
            'message': 'If an account with this email exists, a verification email has been sent.'
        }, status=status.HTTP_200_OK)