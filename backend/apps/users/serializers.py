# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Serializers for the Users app API.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model with learning-specific fields."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    experience_level = serializers.ReadOnlyField()
    next_level_points = serializers.ReadOnlyField()
    time_spent_hours = serializers.ReadOnlyField(source='total_time_spent')
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_image', 'learning_style', 'preferred_difficulty',
            'learning_pace', 'total_modules_completed', 'total_time_spent',
            'time_spent_hours', 'current_streak', 'longest_streak', 'total_points',
            'level', 'experience_level', 'next_level_points', 'achievements', 'badges',
            'current_goal', 'goal_deadline', 'agent_interaction_level',
            'preferred_feedback_style', 'dark_mode', 'notifications_enabled',
            'email_notifications', 'push_notifications', 'password', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_modules_completed', 'total_time_spent', 'current_streak',
            'longest_streak', 'total_points', 'level', 'achievements', 'badges',
            'created_at', 'updated_at'
        ]
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
    def update(self, instance, validated_data):
        """Update user, handling password updates separately."""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password', 'password_confirm'
        ]
    
    def validate(self, data):
        """Validate password confirmation."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user authentication."""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate username and password."""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Must include username and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates."""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'bio', 'profile_image',
            'learning_style', 'preferred_difficulty', 'learning_pace',
            'agent_interaction_level', 'preferred_feedback_style',
            'dark_mode', 'notifications_enabled', 'email_notifications', 'push_notifications',
            'current_goal', 'goal_deadline'
        ]
    
    def validate_learning_style(self, value):
        """Validate learning style choice."""
        valid_styles = ['visual', 'auditory', 'kinesthetic', 'reading']
        if value not in valid_styles:
            raise serializers.ValidationError("Invalid learning style.")
        return value
    
    def validate_preferred_difficulty(self, value):
        """Validate preferred difficulty choice."""
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if value not in valid_difficulties:
            raise serializers.ValidationError("Invalid difficulty level.")
        return value
    
    def validate_agent_interaction_level(self, value):
        """Validate agent interaction level choice."""
        valid_levels = ['minimal', 'moderate', 'high']
        if value not in valid_levels:
            raise serializers.ValidationError("Invalid interaction level.")
        return value
    
    def validate_learning_pace(self, value):
        """Validate learning pace choice."""
        valid_paces = ['slow', 'moderate', 'fast']
        if value not in valid_paces:
            raise serializers.ValidationError("Invalid learning pace.")
        return value
    
    def validate_preferred_feedback_style(self, value):
        """Validate preferred feedback style choice."""
        valid_styles = ['detailed', 'brief', 'encouraging']
        if value not in valid_styles:
            raise serializers.ValidationError("Invalid feedback style.")
        return value
    
    def validate_email(self, value):
        """Validate email format and uniqueness."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        # Check if email is unique (excluding current user)
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return value


class UserProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
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


class LearningSummarySerializer(serializers.Serializer):
    """Serializer for learning progress summary."""
    
    username = serializers.CharField()
    level = serializers.IntegerField()
    total_points = serializers.IntegerField()
    experience_level = serializers.IntegerField()
    modules_completed = serializers.IntegerField()
    current_streak = serializers.IntegerField()
    longest_streak = serializers.IntegerField()
    learning_style = serializers.CharField()
    time_spent_hours = serializers.FloatField()
    achievements_count = serializers.IntegerField()


class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics."""
    
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