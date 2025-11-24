"""
User models for the JAC Learning Platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for the JAC Learning Platform.
    Extends Django's AbstractUser with platform-specific fields.
    """
    
    # Personal information
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    
    # Learning preferences
    preferred_learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Visual'),
            ('auditory', 'Auditory'),
            ('kinesthetic', 'Kinesthetic'),
            ('reading', 'Reading/Writing'),
        ],
        default='visual'
    )
    
    # Progress tracking
    learning_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='beginner'
    )
    
    # Platform activity
    total_study_time = models.DurationField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)
    streak_days = models.PositiveIntegerField(default=0)
    
    # Preferences
    notifications_enabled = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        """Return the user's full name."""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip() or self.username
    
    def update_activity(self):
        """Update last activity timestamp."""
        from django.utils import timezone
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])


class UserProfile(models.Model):
    """
    Extended user profile with additional learning data.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Bio and personal info
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Learning goals and preferences
    learning_goals = models.TextField(blank=True)
    current_goals = models.JSONField(default=list, blank=True)
    
    # Platform statistics
    modules_completed = models.PositiveIntegerField(default=0)
    lessons_completed = models.PositiveIntegerField(default=0)
    assessments_completed = models.PositiveIntegerField(default=0)
    
    # Achievement tracking
    badges = models.JSONField(default=list, blank=True)
    achievements = models.JSONField(default=list, blank=True)
    
    # Learning analytics
    average_lesson_score = models.FloatField(default=0.0)
    total_points = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users_userprofile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    def add_achievement(self, achievement_type, achievement_data):
        """Add a new achievement."""
        achievements = self.achievements or []
        achievements.append({
            'type': achievement_type,
            'data': achievement_data,
            'timestamp': self.updated_at.isoformat()
        })
        self.achievements = achievements
        self.save(update_fields=['achievements'])
    
    def add_badge(self, badge_name):
        """Add a new badge."""
        badges = self.badges or []
        if badge_name not in badges:
            badges.append(badge_name)
            self.badges = badges
            self.save(update_fields=['badges'])