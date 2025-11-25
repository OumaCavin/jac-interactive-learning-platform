"""
Gamification Models - JAC Learning Platform

Complete gamification system with achievements, badges, points, levels, and streaks.

Models:
- Badge: Badge definitions and metadata
- UserBadge: User badge ownership tracking
- Achievement: Achievement definitions (enhanced from progress)
- UserAchievement: User achievement tracking
- UserPoints: Point system for gamification
- UserLevel: Level system tracking
- LearningStreak: Daily learning streak tracking
- PointTransaction: Point earning/spending history
- LevelRequirement: Level progression requirements
- AchievementProgress: Progress tracking for achievements

Author: Cavin Otieno
Created: 2025-11-26
"""

import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class Badge(models.Model):
    """
    Badge definitions for the gamification system
    """
    DIFFICULTY_LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'), 
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    ]
    
    CATEGORIES = [
        ('learning', 'Learning'),
        ('coding', 'Coding'),
        ('assessment', 'Assessment'),
        ('engagement', 'Engagement'),
        ('consistency', 'Consistency'),
        ('milestone', 'Milestone'),
        ('special', 'Special'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Emoji or icon identifier")
    
    # Classification
    category = models.CharField(max_length=20, choices=CATEGORIES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default='bronze')
    
    # Requirements
    requirements = models.JSONField(default=dict, help_text="Badge unlocking requirements")
    minimum_points = models.PositiveIntegerField(default=0)
    unlock_conditions = models.JSONField(default=dict, blank=True)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ], default='common')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'badge'
        ordering = ['category', 'difficulty', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['rarity']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.icon} {self.name} ({self.difficulty})"


class UserBadge(models.Model):
    """
    User badge ownership tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_owners')
    
    # Achievement Details
    earned_at = models.DateTimeField(auto_now_add=True)
    progress_data = models.JSONField(default=dict, blank=True)
    earned_through = models.CharField(max_length=100, blank=True)  # How the badge was earned
    
    # Verification
    is_verified = models.BooleanField(default=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'user_badge'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
        indexes = [
            models.Index(fields=['user', 'earned_at']),
            models.Index(fields=['badge']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Achievement(models.Model):
    """
    Enhanced achievement system (extends progress Achievement model)
    """
    DIFFICULTY_LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    ]
    
    CATEGORIES = [
        ('completion', 'Completion'),
        ('effort', 'Effort'),
        ('skill', 'Skill'),
        ('assessment', 'Assessment'),
        ('consistency', 'Consistency'),
        ('collaboration', 'Collaboration'),
        ('milestone', 'Milestone'),
        ('special', 'Special'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Achievement icon")
    
    # Classification
    category = models.CharField(max_length=20, choices=CATEGORIES)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_LEVELS, default='bronze')
    
    # Achievement Criteria
    criteria_type = models.CharField(max_length=50)  # modules_completed, perfect_scores, etc.
    criteria_value = models.PositiveIntegerField()
    criteria_operator = models.CharField(max_length=10, choices=[
        ('gte', 'Greater than or equal'),
        ('gt', 'Greater than'),
        ('eq', 'Equal'),
    ], default='gte')
    
    # Gamification
    points_reward = models.PositiveIntegerField(default=10)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='achievements', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    unlock_order = models.PositiveIntegerField(default=0)  # For sequential achievements
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gamification_achievement'
        ordering = ['category', 'difficulty', 'unlock_order', 'title']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['difficulty']),
            models.Index(fields=['is_active']),
            models.Index(fields=['unlock_order']),
        ]
    
    def __str__(self):
        return f"{self.icon} {self.title} ({self.difficulty})"


class UserAchievement(models.Model):
    """
    User achievement progress and completion tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress Tracking
    current_progress = models.PositiveIntegerField(default=0)
    target_progress = models.PositiveIntegerField()
    progress_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    # Completion Status
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    
    # Rewards
    points_earned = models.PositiveIntegerField(default=0)
    badge_earned = models.ForeignKey(UserBadge, on_delete=models.CASCADE, null=True, blank=True)
    
    # Progress History
    progress_history = models.JSONField(default=list, blank=True)
    last_progress_update = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'user_achievement'
        unique_together = ['user', 'achievement']
        ordering = ['-last_progress_update']
        indexes = [
            models.Index(fields=['user', 'is_completed']),
            models.Index(fields=['achievement']),
            models.Index(fields=['completed_at']),
        ]
    
    def __str__(self):
        status = "Completed" if self.is_completed else f"{self.current_progress}/{self.target_progress}"
        return f"{self.user.username} - {self.achievement.title} ({status})"
    
    def update_progress(self, new_progress: int):
        """Update achievement progress and check for completion"""
        self.current_progress = min(new_progress, self.target_progress)
        self.progress_percentage = (self.current_progress / self.target_progress) * 100
        self.last_progress_update = timezone.now()
        
        # Add to progress history
        self.progress_history.append({
            'timestamp': timezone.now().isoformat(),
            'progress': self.current_progress,
            'percentage': self.progress_percentage
        })
        
        # Check if achievement is now complete
        if self.current_progress >= self.target_progress and not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.points_earned = self.achievement.points_reward
        
        self.save()


class UserPoints(models.Model):
    """
    User points tracking for the gamification system
    """
    POINT_SOURCES = [
        ('module_completion', 'Module Completion'),
        ('assessment_perfect', 'Perfect Assessment'),
        ('achievement', 'Achievement Unlock'),
        ('streak_bonus', 'Streak Bonus'),
        ('daily_login', 'Daily Login'),
        ('code_execution', 'Code Execution'),
        ('knowledge_graph', 'Knowledge Graph Activity'),
        ('ai_chat', 'AI Chat Interaction'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_points')
    
    # Current Totals
    total_points = models.PositiveIntegerField(default=0)
    available_points = models.PositiveIntegerField(default=0)
    lifetime_points = models.PositiveIntegerField(default=0)
    
    # Category Breakdown
    learning_points = models.PositiveIntegerField(default=0)
    coding_points = models.PositiveIntegerField(default=0)
    assessment_points = models.PositiveIntegerField(default=0)
    engagement_points = models.PositiveIntegerField(default=0)
    
    # Metadata
    last_earned = models.DateTimeField(null=True, blank=True)
    last_spent = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_points'
        unique_together = ['user']
        indexes = [
            models.Index(fields=['total_points']),
            models.Index(fields=['available_points']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.total_points} points"
    
    def add_points(self, amount: int, source: str, metadata: dict = None):
        """Add points to user account"""
        self.total_points += amount
        self.available_points += amount
        self.lifetime_points += amount
        self.last_earned = timezone.now()
        
        # Categorize points
        if source in ['module_completion', 'assessment_perfect', 'knowledge_graph']:
            self.learning_points += amount
        elif source in ['code_execution', 'ai_chat']:
            self.coding_points += amount
        elif source in ['achievement']:
            self.engagement_points += amount
        
        self.save()
        
        # Record transaction
        PointTransaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='earned',
            source=source,
            metadata=metadata or {},
            balance_after=self.total_points
        )
        
        return self.total_points
    
    def spend_points(self, amount: int, purpose: str, metadata: dict = None):
        """Spend points from user account"""
        if self.available_points < amount:
            raise ValueError("Insufficient points")
        
        self.available_points -= amount
        self.last_spent = timezone.now()
        self.save()
        
        # Record transaction
        PointTransaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='spent',
            source=purpose,
            metadata=metadata or {},
            balance_after=self.total_points
        )
        
        return self.available_points


class PointTransaction(models.Model):
    """
    Point earning and spending transaction history
    """
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('spent', 'Spent'),
        ('bonus', 'Bonus'),
        ('penalty', 'Penalty'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='point_transactions')
    
    # Transaction Details
    amount = models.IntegerField()  # Can be negative for spending
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    source = models.CharField(max_length=50)  # Where points came from/went to
    description = models.CharField(max_length=200, blank=True)
    
    # Context
    metadata = models.JSONField(default=dict, blank=True)
    balance_after = models.PositiveIntegerField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'point_transaction'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['source']),
        ]
    
    def __str__(self):
        sign = '+' if self.amount > 0 else ''
        return f"{sign}{self.amount} points - {self.source}"


class UserLevel(models.Model):
    """
    User level progression system
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_levels')
    
    # Level Information
    current_level = models.PositiveIntegerField(default=1)
    current_xp = models.PositiveIntegerField(default=0)
    total_xp = models.PositiveIntegerField(default=0)
    xp_to_next_level = models.PositiveIntegerField()
    
    # Progress Tracking
    level_up_notifications = models.JSONField(default=list, blank=True)
    last_level_up = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_level'
        unique_together = ['user']
        indexes = [
            models.Index(fields=['current_level']),
            models.Index(fields=['total_xp']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: Level {self.current_level}"
    
    def add_xp(self, amount: int):
        """Add experience points and handle level progression"""
        self.total_xp += amount
        self.current_xp += amount
        
        # Check for level up
        while self.current_xp >= self.xp_to_next_level:
            self.level_up()
        
        self.save()
    
    def level_up(self):
        """Handle level up progression"""
        self.current_level += 1
        self.current_xp = self.current_xp - self.xp_to_next_level
        
        # Calculate XP needed for next level
        self.xp_to_next_level = self.calculate_xp_for_level(self.current_level + 1)
        
        # Record level up
        self.level_up_notifications.append({
            'level': self.current_level,
            'timestamp': timezone.now().isoformat(),
            'xp_earned': self.total_xp
        })
        
        self.last_level_up = timezone.now()
    
    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """Calculate XP required for a given level"""
        # Exponential growth formula
        return int(100 * (1.2 ** (level - 1)))
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress to next level as percentage"""
        if self.xp_to_next_level == 0:
            return 100.0
        return min(100.0, (self.current_xp / self.xp_to_next_level) * 100)


class LearningStreak(models.Model):
    """
    Daily learning streak tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_streaks')
    
    # Streak Information
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Streak History
    streak_history = models.JSONField(default=list, blank=True)
    streak_breaks = models.JSONField(default=list, blank=True)
    
    # Streak Multipliers
    streak_multiplier = models.FloatField(default=1.0, validators=[MinValueValidator(1.0), MaxValueValidator(3.0)])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'learning_streak'
        unique_together = ['user']
        indexes = [
            models.Index(fields=['current_streak']),
            models.Index(fields=['longest_streak']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.current_streak} day streak"
    
    def record_activity(self, activity_date=None):
        """Record learning activity and update streak"""
        if activity_date is None:
            activity_date = timezone.now().date()
        
        # Check if this is a new activity day
        if self.last_activity_date == activity_date:
            return  # Already recorded today
        
        # Calculate days since last activity
        days_diff = (activity_date - self.last_activity_date).days if self.last_activity_date else 1
        
        if days_diff == 1:
            # Consecutive day - increment streak
            self.current_streak += 1
            
            # Apply streak bonus multiplier
            if self.current_streak >= 7:
                self.streak_multiplier = min(3.0, 1.0 + (self.current_streak / 30))
            
        elif days_diff > 1:
            # Streak broken
            self.streak_breaks.append({
                'broken_streak': self.current_streak,
                'date': self.last_activity_date.isoformat() if self.last_activity_date else None,
                'gap_days': days_diff - 1
            })
            self.current_streak = 1
            self.streak_multiplier = 1.0
        
        # Update longest streak
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        
        # Record in history
        self.streak_history.append({
            'date': activity_date.isoformat(),
            'streak_count': self.current_streak,
            'streak_multiplier': self.streak_multiplier
        })
        
        self.last_activity_date = activity_date
        self.save()
        
        return self.current_streak
    
    def break_streak(self):
        """Force break the streak (e.g., for testing or manual reset)"""
        if self.current_streak > 0:
            self.streak_breaks.append({
                'broken_streak': self.current_streak,
                'date': self.last_activity_date.isoformat() if self.last_activity_date else None,
                'gap_days': None
            })
        
        self.current_streak = 0
        self.streak_multiplier = 1.0
        self.save()


class LevelRequirement(models.Model):
    """
    Level progression requirements and rewards
    """
    REQUIREMENT_TYPES = [
        ('points', 'Points'),
        ('xp', 'Experience Points'),
        ('achievements', 'Achievements Count'),
        ('modules', 'Modules Completed'),
        ('assessments', 'Assessments Completed'),
        ('streak', 'Learning Streak'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    level = models.PositiveIntegerField(unique=True)
    
    # Requirements
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)
    requirement_value = models.PositiveIntegerField()
    
    # Rewards
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    unlock_features = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'level_requirement'
        ordering = ['level']
        indexes = [
            models.Index(fields=['level']),
            models.Index(fields=['requirement_type']),
        ]
    
    def __str__(self):
        return f"Level {self.level}: {self.get_requirement_type_display()} {self.requirement_value}"


class AchievementProgress(models.Model):
    """
    Real-time achievement progress tracking
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievement_progress')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_tracking')
    
    # Progress Data
    current_count = models.PositiveIntegerField(default=0)
    target_count = models.PositiveIntegerField()
    last_update = models.DateTimeField(default=timezone.now)
    
    # Context
    context_data = models.JSONField(default=dict, blank=True)  # Module IDs, assessment IDs, etc.
    
    class Meta:
        db_table = 'achievement_progress'
        unique_together = ['user', 'achievement']
        ordering = ['-last_update']
        indexes = [
            models.Index(fields=['user', 'last_update']),
            models.Index(fields=['achievement']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}: {self.current_count}/{self.target_count}"
    
    def increment(self, increment_by: int = 1, context: dict = None):
        """Increment achievement progress"""
        self.current_count += increment_by
        self.last_update = timezone.now()
        
        if context:
            self.context_data.update(context)
        
        self.save()
        
        # Check if achievement should be completed
        if self.current_count >= self.target_count:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=self.user,
                achievement=self.achievement,
                defaults={'target_progress': self.target_count}
            )
            user_achievement.update_progress(self.current_count)
        
        return self.current_count