# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Models for the Learning app.
Core learning management models for JAC learning platform.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()


class LearningPath(models.Model):
    """
    Represents a learning path - a structured sequence of modules.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    estimated_duration = models.PositiveIntegerField(help_text='Estimated duration in hours')
    prerequisites = models.JSONField(default=list, blank=True, help_text='List of prerequisite module IDs')
    
    # Content
    cover_image = models.ImageField(upload_to='learning-paths/covers/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Metadata
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_paths')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_learning_path'
        ordering = ['name']
        indexes = [
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_published']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def module_count(self):
        """Get total number of modules in this path."""
        return self.modules.count()
    
    @property
    def completed_by_users(self):
        """Get number of users who completed this path."""
        return UserLearningPath.objects.filter(
            learning_path=self, 
            status='completed'
        ).count()
    
    @property
    def average_rating(self):
        """Get average rating for this path."""
        from django.db.models import Avg
        return PathRating.objects.filter(learning_path=self).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0


class Module(models.Model):
    """
    Represents a learning module within a learning path.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Content
    content = models.TextField(help_text='Main module content in markdown or rich text')
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('markdown', 'Markdown'),
            ('html', 'HTML'),
            ('interactive', 'Interactive Content'),
            ('jac_code', 'JAC Code Tutorial'),
        ],
        default='markdown'
    )
    order = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    difficulty_rating = models.PositiveIntegerField(
        help_text='Difficulty rating from 1 (easiest) to 5 (hardest)',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # JAC-specific content
    jac_concepts = models.JSONField(default=list, blank=True, help_text='JAC concepts covered in this module')
    code_examples = models.JSONField(default=list, blank=True)
    
    # Features
    has_quiz = models.BooleanField(default=False)
    has_coding_exercise = models.BooleanField(default=False)
    has_visual_demo = models.BooleanField(default=False)
    
    # Metadata
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_module'
        ordering = ['learning_path', 'order']
        unique_together = ['learning_path', 'order']
        indexes = [
            models.Index(fields=['learning_path', 'order']),
            models.Index(fields=['difficulty_rating']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return f"{self.learning_path.name} - {self.title}"
    
    @property
    def total_users(self):
        """Get total number of users who have started this module."""
        return UserModuleProgress.objects.filter(module=self).count()
    
    @property
    def completed_users(self):
        """Get number of users who completed this module."""
        return UserModuleProgress.objects.filter(
            module=self, 
            status='completed'
        ).count()
    
    @property
    def completion_rate(self):
        """Get completion rate as percentage."""
        total = self.total_users
        if total == 0:
            return 0
        return (self.completed_users / total) * 100


class UserLearningPath(models.Model):
    """
    Tracks user progress through learning paths.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    progress_percentage = models.PositiveIntegerField(default=0)
    current_module_order = models.PositiveIntegerField(default=0)
    time_spent = models.DurationField(default=0)
    
    # Scores
    overall_score = models.PositiveIntegerField(null=True, blank=True)
    
    # Notes and feedback
    user_notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_user_learning_path'
        unique_together = ['user', 'learning_path']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['learning_path', 'status']),
            models.Index(fields=['status', 'last_activity_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.learning_path.name}"
    
    def get_completion_percentage(self):
        """Calculate completion percentage based on completed modules."""
        total_modules = self.learning_path.modules.count()
        if total_modules == 0:
            return 0
        
        completed_modules = UserModuleProgress.objects.filter(
            user=self.user,
            module__learning_path=self.learning_path,
            status='completed'
        ).count()
        
        return int((completed_modules / total_modules) * 100)
    
    def start_learning_path(self):
        """Mark learning path as started."""
        if self.status == 'not_started':
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()
    
    def complete_learning_path(self):
        """Mark learning path as completed."""
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        self.save()


class Lesson(models.Model):
    """
    Individual lessons within a module
    """
    LESSON_TYPE_CHOICES = [
        ('text', 'Text Lesson'),
        ('video', 'Video Lesson'),
        ('interactive', 'Interactive Content'),
        ('code_tutorial', 'Code Tutorial'),
        ('quiz', 'Quiz'),
    ]
    
    # Core identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    
    # Content type and data
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='text')
    content = models.TextField(blank=True, help_text='Lesson content in markdown or HTML')
    code_example = models.TextField(blank=True, help_text='Code examples for this lesson')
    
    # Interactive content
    quiz_questions = models.JSONField(blank=True, default=list, help_text='Quiz questions data')
    interactive_demo = models.JSONField(blank=True, default=dict, help_text='Interactive demo configuration')
    
    # Media resources
    video_url = models.URLField(blank=True, help_text='URL to lesson video')
    audio_url = models.URLField(blank=True, help_text='URL to lesson audio')
    resources = models.JSONField(blank=True, default=list, help_text='Additional resources for this lesson')
    
    # Metadata
    is_published = models.BooleanField(default=False)
    estimated_duration = models.PositiveIntegerField(blank=True, help_text='Estimated duration in minutes', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_lesson'
        ordering = ['module', 'order']
        unique_together = ('module', 'order')
    
    def __str__(self):
        return f"{self.module.title} - Lesson {self.order}: {self.title}"


class UserModuleProgress(models.Model):
    """
    Tracks user progress through individual modules.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_progress')
    
    # Progress tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    time_spent = models.DurationField(default=0)
    progress_percentage = models.PositiveIntegerField(default=0)
    
    # Scores and performance
    quiz_score = models.PositiveIntegerField(null=True, blank=True)
    coding_score = models.PositiveIntegerField(null=True, blank=True)
    overall_score = models.PositiveIntegerField(null=True, blank=True)
    
    # Notes and feedback
    user_notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_activity_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_user_module_progress'
        unique_together = ['user', 'module']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['module', 'status']),
            models.Index(fields=['status', 'last_activity_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.module.title}"
    
    def start_module(self):
        """Mark module as started."""
        if self.status == 'not_started':
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()
    
    def complete_module(self):
        """Mark module as completed."""
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        self.save()
        
        # Update overall path progress
        user_path = UserLearningPath.objects.get(
            user=self.user,
            learning_path=self.module.learning_path
        )
        user_path.progress_percentage = user_path.get_completion_percentage()
        user_path.current_module_order = max(
            user_path.current_module_order, 
            self.module.order
        )
        user_path.save()
    
    def add_time_spent(self, minutes):
        """Add time spent to the module."""
        from datetime import timedelta
        self.time_spent += timedelta(minutes=minutes)
        self.save()


class PathRating(models.Model):
    """
    User ratings and reviews for learning paths.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='path_ratings')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='ratings')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_path_rating'
        unique_together = ['user', 'learning_path']
        indexes = [
            models.Index(fields=['learning_path']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.learning_path.name} ({self.rating} stars)"


class Achievement(models.Model):
    """
    System achievements that users can unlock.
    """
    ACHIEVEMENT_TYPES = [
        ('completion', 'Completion'),
        ('performance', 'Performance'),
        ('streak', 'Streak'),
        ('skill', 'Skill'),
        ('engagement', 'Engagement'),
        ('collaboration', 'Collaboration'),
    ]
    
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    
    # Requirements
    requirements = models.JSONField(default=dict, help_text='Requirements to unlock this achievement')
    icon = models.CharField(max_length=200, blank=True, help_text='Icon URL or name')
    badge_color = models.CharField(max_length=20, default='blue', help_text='CSS color class')
    
    # Statistics
    unlock_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_achievements'
        ordering = ['achievement_type', 'rarity', 'name']
        indexes = [
            models.Index(fields=['achievement_type']),
            models.Index(fields=['rarity']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Assessment(models.Model):
    """
    Represents assessments, quizzes, and exams.
    """
    ASSESSMENT_TYPES = [
        ('quiz', 'Quiz'),
        ('exam', 'Examination'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical Test'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPES, default='quiz')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    
    # Configuration
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text='Time limit in minutes')
    max_attempts = models.PositiveIntegerField(default=3, help_text='Maximum number of attempts allowed')
    passing_score = models.FloatField(default=70.0, help_text='Minimum score to pass (percentage)')
    
    # Metadata
    is_published = models.BooleanField(default=False)
    average_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_assessment'
        ordering = ['title']
    
    def __str__(self):
        return self.title


class AssessmentQuestion(models.Model):
    """
    Questions for assessments.
    """
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    
    # Question data
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='medium')
    points = models.FloatField(default=1.0)
    order = models.PositiveIntegerField(default=0)
    
    # Content (using base64 encoded question data)
    question_data = models.JSONField(default=dict, help_text='Base64 encoded question content')
    
    # Overrides for specific assessments
    question_text_override = models.TextField(blank=True, help_text='Override default question text for this assessment')
    options_override = models.JSONField(blank=True, default=list, help_text='Override default options for multiple choice')
    correct_answer_override = models.JSONField(blank=True, default=list, help_text='Override correct answer')
    
    # Performance tracking
    total_attempts = models.PositiveIntegerField(default=0)
    correct_attempts = models.PositiveIntegerField(default=0)
    average_time = models.FloatField(default=0.0, help_text='Average time in seconds')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_assessment_questions'
        ordering = ['assessment', 'order']
    
    def __str__(self):
        return f"Question {self.order} - {self.assessment.title}"


class AssessmentAttempt(models.Model):
    """
    Tracks user attempts at assessments.
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
        ('timed_out', 'Timed Out'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    
    # Attempt tracking
    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=0)
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text='Time limit in minutes')
    
    # Scores
    score = models.FloatField(null=True, blank=True)
    max_score = models.FloatField(default=100.0)
    passing_score = models.FloatField(default=70.0)
    is_passed = models.BooleanField(default=False)
    
    # Responses
    answers = models.JSONField(default=dict, help_text='User answers for each question')
    feedback = models.TextField(blank=True)
    
    class Meta:
        db_table = 'jac_assessment_attempts'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'assessment']),
            models.Index(fields=['assessment', 'status']),
            models.Index(fields=['started_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} (Attempt {self.attempt_number})"
    
    def calculate_score(self):
        """Calculate final score based on answers."""
        if not self.answers:
            return 0
        
        total_points = 0
        earned_points = 0
        
        for question in self.assessment.questions.all():
            total_points += question.points
            
            if str(question.id) in self.answers:
                user_answer = self.answers[str(question.id)]
                correct_answer = question.correct_answer_override or question.question_data.get('correct_answer', [])
                
                if user_answer in correct_answer:
                    earned_points += question.points
        
        if total_points > 0:
            self.score = (earned_points / total_points) * 100
            self.is_passed = self.score >= self.passing_score
        
        self.save()
        return self.score


class CodeSubmission(models.Model):
    """
    Tracks code submissions for exercises and projects.
    """
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('jac', 'JAC (Jaseci)'),
        ('javascript', 'JavaScript'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Execution Error'),
        ('timeout', 'Timeout'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_submissions')
    
    # Submission details
    submission_id = models.CharField(max_length=100, unique=True)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    
    # Execution results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_result = models.JSONField(blank=True, default=dict)
    ai_feedback = models.TextField(blank=True)
    
    # Performance metrics
    score = models.FloatField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.FloatField(null=True, blank=True)
    
    # Metadata
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer_agent_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'jac_code_submissions'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['submitted_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.task_title}"


class CodeExecutionLog(models.Model):
    """
    Logs code execution attempts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='execution_logs')
    
    execution_id = models.CharField(max_length=100)
    output = models.TextField(blank=True)
    error_output = models.TextField(blank=True)
    execution_time = models.FloatField()
    memory_usage = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'jac_code_execution_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Execution {self.execution_id} - {self.submission.task_title}"


class AICodeReview(models.Model):
    """
    AI-generated code reviews and feedback.
    """
    REVIEW_TYPES = [
        ('syntax', 'Syntax Analysis'),
        ('logic', 'Logic Review'),
        ('performance', 'Performance Analysis'),
        ('security', 'Security Assessment'),
        ('style', 'Code Style'),
        ('best_practices', 'Best Practices'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='ai_reviews')
    
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPES)
    findings = models.JSONField(default=dict)
    suggestions = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)
    
    agent_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'jac_ai_code_reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.review_type} review - {self.submission.task_title}"


class LearningRecommendation(models.Model):
    """
    AI-generated learning recommendations for users.
    """
    RECOMMENDATION_TYPES = [
        ('next_module', 'Next Module Recommendation'),
        ('skill_gap', 'Skill Gap Analysis'),
        ('review_topic', 'Review Topic Suggestion'),
        ('challenging_exercise', 'Challenging Exercise'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_recommendations')
    
    recommendation_type = models.CharField(max_length=30, choices=RECOMMENDATION_TYPES)
    content = models.JSONField(help_text='Recommendation details and reasoning')
    priority_score = models.FloatField(default=0.0, help_text='AI-calculated priority score')
    
    # Status
    is_dismissed = models.BooleanField(default=False)
    is_acted_upon = models.BooleanField(default=False)
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'jac_learning_recommendation'
        ordering = ['-priority_score', '-created_at']
    
    def __str__(self):
        return f"{self.recommendation_type} for {self.user.username}"


# ===== ADAPTIVE LEARNING MODELS =====

class UserDifficultyProfile(models.Model):
    """
    Tracks individual user difficulty profiles for adaptive learning.
    """
    DIFFICULTY_LEVELS = [
        ('very_beginner', 'Very Beginner'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='difficulty_profile')
    
    # Current skill levels
    current_difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    jac_knowledge_level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    problem_solving_level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    coding_skill_level = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    
    # Learning patterns
    learning_speed = models.FloatField(default=1.0, help_text='How quickly user learns new concepts')
    retention_rate = models.FloatField(default=0.8, help_text='How well user retains information')
    preferred_challenge_increase = models.FloatField(default=0.2, help_text='How much difficulty should increase per success')
    challenge_tolerance = models.FloatField(default=0.7, help_text='How much challenge user can handle')
    
    # Performance metrics
    recent_accuracy = models.FloatField(default=0.5, help_text='Recent accuracy percentage')
    success_streak = models.PositiveIntegerField(default=0)
    last_difficulty_change = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_user_difficulty_profile'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['current_difficulty']),
            models.Index(fields=['updated_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.current_difficulty}"
    
    def get_overall_skill_level(self):
        """Calculate overall skill level based on all dimensions."""
        return (self.jac_knowledge_level + self.problem_solving_level + self.coding_skill_level) / 3
    
    def should_increase_difficulty(self):
        """Determine if user difficulty should be increased based on recent performance."""
        if self.recent_accuracy >= 0.8 and self.success_streak >= 3:
            return True
        return False
    
    def should_decrease_difficulty(self):
        """Determine if user difficulty should be decreased based on recent performance."""
        if self.recent_accuracy < 0.5 or self.success_streak == 0:
            return True
        return False
    
    def adjust_difficulty(self, performance_score):
        """Adjust user difficulty based on performance score (0.0 to 1.0)."""
        if performance_score >= 0.8:
            # Increase difficulty
            self._increase_difficulty()
        elif performance_score <= 0.4:
            # Decrease difficulty  
            self._decrease_difficulty()
        
        # Update recent accuracy
        self.recent_accuracy = (self.recent_accuracy * 0.7) + (performance_score * 0.3)
        
        # Update success streak
        if performance_score >= 0.7:
            self.success_streak += 1
        else:
            self.success_streak = 0
            
        self.last_difficulty_change = timezone.now()
        self.save()
        
        return self.current_difficulty
    
    def _increase_difficulty(self):
        """Increase user difficulty level."""
        difficulty_order = ['very_beginner', 'beginner', 'intermediate', 'advanced', 'expert']
        current_index = difficulty_order.index(self.current_difficulty)
        
        if current_index < len(difficulty_order) - 1:
            self.current_difficulty = difficulty_order[current_index + 1]
            # Increase individual skill levels
            self.jac_knowledge_level = min(10, self.jac_knowledge_level + 1)
            self.problem_solving_level = min(10, self.problem_solving_level + 1)
            self.coding_skill_level = min(10, self.coding_skill_level + 1)
    
    def _decrease_difficulty(self):
        """Decrease user difficulty level."""
        difficulty_order = ['very_beginner', 'beginner', 'intermediate', 'advanced', 'expert']
        current_index = difficulty_order.index(self.current_difficulty)
        
        if current_index > 0:
            self.current_difficulty = difficulty_order[current_index - 1]
            # Decrease individual skill levels
            self.jac_knowledge_level = max(1, self.jac_knowledge_level - 1)
            self.problem_solving_level = max(1, self.problem_solving_level - 1)
            self.coding_skill_level = max(1, self.coding_skill_level - 1)


class AdaptiveChallenge(models.Model):
    """
    Stores AI-generated challenges with adaptive difficulty tracking.
    """
    CHALLENGE_TYPES = [
        ('quiz', 'Multiple Choice Quiz'),
        ('coding', 'Coding Exercise'),
        ('debug', 'Debugging Challenge'),
        ('scenario', 'Problem Scenario'),
        ('project', 'Mini Project'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Challenge details
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES)
    content = models.TextField()  # JSON or structured content for the challenge
    
    # Difficulty and adaptation
    difficulty_level = models.CharField(max_length=20, choices=UserDifficultyProfile.DIFFICULTY_LEVELS)
    skill_dimensions = models.JSONField(default=dict, help_text='What skills this challenge targets')
    estimated_time = models.PositiveIntegerField(help_text='Estimated completion time in minutes')
    
    # AI generation metadata
    generated_by_agent = models.CharField(max_length=50, help_text='Which AI agent generated this')
    generation_prompt = models.TextField(help_text='The prompt used to generate this challenge')
    adaptation_rules = models.JSONField(default=dict, help_text='Rules for adapting this challenge')
    
    # Performance tracking
    success_rate = models.FloatField(default=0.0, help_text='Overall success rate for this challenge')
    average_completion_time = models.PositiveIntegerField(default=0, help_text='Average completion time in minutes')
    total_attempts = models.PositiveIntegerField(default=0)
    successful_attempts = models.PositiveIntegerField(default=0)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_adaptive_challenge'
        indexes = [
            models.Index(fields=['challenge_type']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_active']),
            models.Index(fields=['success_rate']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.difficulty_level})"
    
    def update_success_metrics(self, completed, completion_time):
        """Update success metrics based on user performance."""
        self.total_attempts += 1
        if completed:
            self.successful_attempts += 1
            
        # Update average completion time using running average
        if self.total_attempts == 1:
            self.average_completion_time = completion_time
        else:
            self.average_completion_time = int(
                (self.average_completion_time * (self.total_attempts - 1) + completion_time) / self.total_attempts
            )
        
        # Update success rate
        self.success_rate = self.successful_attempts / self.total_attempts
        
        self.save()


class UserChallengeAttempt(models.Model):
    """
    Tracks individual user attempts at adaptive challenges.
    """
    ATTEMPT_STATUS = [
        ('started', 'Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_attempts')
    challenge = models.ForeignKey(AdaptiveChallenge, on_delete=models.CASCADE, related_name='attempts')
    
    # Attempt details
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS, default='started')
    score = models.FloatField(null=True, blank=True, help_text='Final score (0.0 to 1.0)')
    time_spent = models.PositiveIntegerField(help_text='Time spent in minutes')
    responses = models.JSONField(default=dict, help_text='User responses to challenge')
    feedback = models.TextField(blank=True, help_text='AI-generated feedback')
    
    # Adaptive learning feedback
    difficulty_feedback = models.TextField(blank=True, help_text='Was the difficulty appropriate?')
    learning_insights = models.JSONField(default=dict, help_text='AI insights about learning pattern')
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'jac_user_challenge_attempt'
        unique_together = ['user', 'challenge', 'started_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['challenge', 'status']),
            models.Index(fields=['score']),
            models.Index(fields=['started_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.status})"
    
    def complete_attempt(self, score, responses, feedback=None):
        """Mark attempt as completed with scores and feedback."""
        self.status = 'completed'
        self.score = score
        self.responses = responses
        self.feedback = feedback or ""
        self.completed_at = timezone.now()
        self.time_spent = int((self.completed_at - self.started_at).total_seconds() / 60)
        self.save()
        
        # Update challenge metrics
        self.challenge.update_success_metrics(True, self.time_spent)
        
        # Update user difficulty profile
        if hasattr(self.user, 'difficulty_profile'):
            self.user.difficulty_profile.adjust_difficulty(score)
        
        return self.score
    
    def fail_attempt(self, feedback=None):
        """Mark attempt as failed."""
        self.status = 'failed'
        self.feedback = feedback or ""
        self.completed_at = timezone.now()
        self.time_spent = int((self.completed_at - self.started_at).total_seconds() / 60)
        self.save()
        
        # Update challenge metrics
        self.challenge.update_success_metrics(False, self.time_spent)
        
        # Update user difficulty profile
        if hasattr(self.user, 'difficulty_profile'):
            self.user.difficulty_profile.adjust_difficulty(self.score or 0.0)
    
    def get_difficulty_rating(self):
        """Get user's rating of challenge difficulty (1-5 scale)."""
        if 'difficulty_rating' in self.responses:
            return self.responses['difficulty_rating']
        return None


class SpacedRepetitionSession(models.Model):
    """
    Manages spaced repetition sessions for optimal review timing.
    """
    REVIEW_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ready', 'Ready for Review'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spaced_repetition_sessions')
    challenge = models.ForeignKey(AdaptiveChallenge, on_delete=models.CASCADE, related_name='review_sessions')
    
    # Spaced repetition data
    review_stage = models.PositiveIntegerField(default=1)  # 1, 2, 3, etc. based on SM-2 algorithm
    ease_factor = models.FloatField(default=2.5)  # SM-2 ease factor
    interval_days = models.PositiveIntegerField(default=1)  # Days until next review
    
    # Timing
    scheduled_for = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Performance
    quality_rating = models.PositiveIntegerField(null=True, blank=True, help_text='User rating 0-5 for recall quality')
    status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='scheduled')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_spaced_repetition_session'
        indexes = [
            models.Index(fields=['user', 'scheduled_for']),
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_for']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} (Stage {self.review_stage})"
    
    def complete_review(self, quality_rating):
        """Complete review and calculate next review date using SM-2 algorithm."""
        self.quality_rating = quality_rating
        self.completed_at = timezone.now()
        self.status = 'completed'
        
        # SM-2 algorithm implementation
        if quality_rating >= 3:  # Correct response
            if self.review_stage == 1:
                self.interval_days = 1
            elif self.review_stage == 2:
                self.interval_days = 6
            else:
                self.interval_days = round(self.interval_days * self.ease_factor)
            
            self.review_stage += 1
        else:  # Incorrect response - reset
            self.review_stage = 1
            self.interval_days = 1
        
        # Update ease factor
        self.ease_factor = self.ease_factor + (0.1 - (5 - quality_rating) * (0.08 + (5 - quality_rating) * 0.02))
        if self.ease_factor < 1.3:
            self.ease_factor = 1.3
        
        # Schedule next review
        self.scheduled_for = timezone.now() + timezone.timedelta(days=self.interval_days)
        self.status = 'scheduled'
        self.save()
        
        return self.scheduled_for
    
    def is_due_for_review(self):
        """Check if this session is due for review."""
        return self.status == 'ready' and self.scheduled_for <= timezone.now()
    
    def mark_as_ready(self):
        """Mark session as ready for review."""
        self.status = 'ready'
        self.save()