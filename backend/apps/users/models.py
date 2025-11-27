# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
User models for the JAC Learning Platform.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone
from datetime import timedelta
import uuid


class User(AbstractUser):
    """
    Custom User model with extended fields for learning platform.
    """
    # Basic Information
    # Note: Using default Django AutoField instead of UUID to match existing database schema
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, max_length=500)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Learning Preferences
    learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', 'Visual Learner'),
            ('auditory', 'Auditory Learner'),
            ('kinesthetic', 'Kinesthetic Learner'),
            ('reading', 'Reading/Writing Learner'),
        ],
        default='visual'
    )
    preferred_difficulty = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    learning_pace = models.CharField(
        max_length=20,
        choices=[
            ('slow', 'Slow & Steady'),
            ('moderate', 'Moderate'),
            ('fast', 'Fast Paced'),
        ],
        default='moderate'
    )
    
    # Progress Tracking
    total_modules_completed = models.PositiveIntegerField(default=0)
    total_time_spent = models.DurationField(default=timedelta)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    
    # Gamification
    achievements = models.JSONField(default=list, blank=True)
    badges = models.JSONField(default=list, blank=True)
    current_goal = models.CharField(max_length=200, blank=True)
    goal_deadline = models.DateTimeField(null=True, blank=True)
    
    # Agent Preferences
    agent_interaction_level = models.CharField(
        max_length=20,
        choices=[
            ('minimal', 'Minimal Interaction'),
            ('moderate', 'Moderate Support'),
            ('high', 'High Support'),
        ],
        default='moderate'
    )
    preferred_feedback_style = models.CharField(
        max_length=20,
        choices=[
            ('detailed', 'Detailed Feedback'),
            ('brief', 'Brief Feedback'),
            ('encouraging', 'Encouraging Only'),
        ],
        default='detailed'
    )
    
    # Platform Preferences
    dark_mode = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    
    # Email Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    verification_token_expires_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table = 'users_user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['level']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_activity_at']),
        ]
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        """Override save to handle level calculations and timestamps."""
        # Update last activity timestamp
        self.last_activity_at = timezone.now()
        
        # Calculate level based on points
        self.level = max(1, self.total_points // 100 + 1)
        
        super().save(*args, **kwargs)
    
    @property
    def experience_level(self):
        """Calculate current experience level based on points."""
        return min(100, self.total_points % 100)
    
    @property
    def next_level_points(self):
        """Calculate points needed for next level."""
        return (self.level * 100) - self.total_points
    
    def add_points(self, points):
        """Add points and update level if necessary."""
        self.total_points += points
        old_level = self.level
        self.save(update_fields=['total_points', 'level'])
        
        # Check for level up
        if self.level > old_level:
            # Award level up achievement
            self.award_achievement(f'Level {self.level} Reached')
    
    def award_achievement(self, achievement):
        """Award an achievement to the user."""
        if achievement not in self.achievements:
            self.achievements.append({
                'name': achievement,
                'timestamp': timezone.now().isoformat(),
                'points_earned': 0
            })
            self.save(update_fields=['achievements'])
    
    def update_streak(self):
        """Update user's learning streak."""
        from datetime import date, timedelta
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        if self.last_activity_at and self.last_activity_at.date() == yesterday:
            # Extend current streak
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        elif self.last_activity_at and self.last_activity_at.date() != today:
            # Reset streak if more than 1 day gap
            self.current_streak = 1
        
        self.save(update_fields=['current_streak', 'longest_streak'])
    
    def get_learning_summary(self):
        """Get a summary of user's learning progress."""
        return {
            'username': self.username,
            'level': self.level,
            'total_points': self.total_points,
            'experience_level': self.experience_level,
            'modules_completed': self.total_modules_completed,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'learning_style': self.learning_style,
            'time_spent_hours': self.total_time_spent.total_seconds() / 3600,
            'achievements_count': len(self.achievements),
        }
    
    def generate_verification_token(self):
        """Generate a unique verification token for email verification."""
        import secrets
        from datetime import timedelta
        
        token = secrets.token_urlsafe(32)
        self.verification_token = token
        self.verification_token_expires_at = timezone.now() + timedelta(hours=24)
        return token


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