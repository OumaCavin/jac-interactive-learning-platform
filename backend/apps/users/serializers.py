"""
Serializers for the users app.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'preferred_learning_style', 'learning_level',
            'total_study_time', 'streak_days', 'notifications_enabled',
            'email_verified', 'date_joined', 'last_login'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'total_study_time',
            'streak_days', 'email_verified'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'bio', 'location', 'website',
            'learning_goals', 'current_goals', 'modules_completed',
            'lessons_completed', 'assessments_completed', 'badges',
            'achievements', 'average_lesson_score', 'total_points',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'user',
            'modules_completed', 'lessons_completed', 'assessments_completed',
            'total_points'
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]
    
    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
            'preferred_learning_style', 'learning_level',
            'notifications_enabled'
        ]
    
    def validate_email(self, value):
        """
        Ensure email is unique.
        """
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class UserStatsSerializer(serializers.Serializer):
    """
    Serializer for user statistics.
    """
    
    total_users = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    active_users_week = serializers.IntegerField()
    active_users_month = serializers.IntegerField()
    new_users_today = serializers.IntegerField()
    new_users_week = serializers.IntegerField()
    new_users_month = serializers.IntegerField()
    
    class Meta:
        fields = [
            'total_users', 'active_users_today', 'active_users_week',
            'active_users_month', 'new_users_today', 'new_users_week',
            'new_users_month'
        ]