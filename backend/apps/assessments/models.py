"""
Assessment models for JAC Learning Platform
Consolidated and comprehensive assessment system
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()

# Import learning models
from apps.learning.models import Module, Lesson


class Assessment(models.Model):
    """
    Represents an assessment/quiz within a module.
    """
    ASSESSMENT_TYPE_CHOICES = [
        ('quiz', 'Quiz'),
        ('exam', 'Examination'),
        ('assignment', 'Assignment'),
        ('project', 'Project'),
        ('practical', 'Practical Test'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Settings
    assessment_type = models.CharField(
        max_length=20, 
        choices=ASSESSMENT_TYPE_CHOICES, 
        default='quiz'
    )
    difficulty_level = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        default='beginner'
    )
    
    # Timing and scoring
    time_limit = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text='Time limit in minutes'
    )
    max_attempts = models.PositiveIntegerField(
        default=3, 
        help_text='Maximum number of attempts allowed'
    )
    passing_score = models.FloatField(
        default=70.0, 
        help_text='Minimum score to pass (percentage)'
    )
    
    # Relationships
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessment_app_assessments')
    
    # Publishing
    is_published = models.BooleanField(default=False)
    
    # Statistics (calculated field)
    average_score = models.FloatField(default=0.0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessment_app_assessments'
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.module.title}"


class AssessmentAttempt(models.Model):
    """
    Tracks user attempts at assessments/quizzes
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
        ('timed_out', 'Timed Out'),
    ]
    
    # Core identification
    attempt_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    
    # Assessment details
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True, default=None)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessment_attempts')
    
    # Status and timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_limit_minutes = models.IntegerField(default=60)
    
    # Scoring
    score = models.FloatField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text='Final score as percentage (0-100)'
    )
    max_score = models.FloatField(default=100.0)
    passing_score = models.FloatField(default=70.0)
    
    # Metadata
    answers = models.JSONField(default=dict, help_text='User answers to questions')
    feedback = models.JSONField(default=dict, help_text='Detailed feedback for each question')
    
    class Meta:
        db_table = 'assessment_attempts'
        verbose_name = 'Assessment Attempt'
        verbose_name_plural = 'Assessment Attempts'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Attempt {self.attempt_id} - {self.user.username} - {self.assessment.title}"
    
    @property
    def is_passed(self):
        """Check if attempt passed the assessment"""
        if self.score is None:
            return False
        return self.score >= self.passing_score
    
    @property
    def duration_minutes(self):
        """Calculate attempt duration in minutes"""
        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds() / 60
        else:
            from django.utils import timezone
            return (timezone.now() - self.started_at).total_seconds() / 60


class AssessmentQuestion(models.Model):
    """
    Extended question model that links questions to assessments with additional metadata
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('code_question', 'Code Question'),
        ('essay', 'Essay'),
    ]
    
    # Core identification
    question_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='assessment_questions', null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessment_questions')
    
    # Question content
    title = models.CharField(max_length=255)
    question_text = models.TextField()
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    
    # Answer information
    options = models.JSONField(default=list, help_text='Options for multiple choice questions')
    correct_answer = models.TextField(help_text='Correct answer for the question')
    explanation = models.TextField(blank=True, help_text='Explanation for the correct answer')
    
    # Scoring and metadata
    points = models.FloatField(default=1.0, help_text='Points awarded for correct answer')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    order = models.PositiveIntegerField(default=0, help_text='Order of question in assessment')
    
    # Additional metadata
    tags = models.JSONField(default=list, help_text='Tags for categorization')
    learning_objectives = models.JSONField(default=list, help_text='Learning objectives this question addresses')
    
    # Status
    is_active = models.BooleanField(default=True, help_text='Whether this question is active/available')
    version = models.PositiveIntegerField(default=1, help_text='Question version for tracking changes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessment_questions'
        verbose_name = 'Assessment Question'
        verbose_name_plural = 'Assessment Questions'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.title} - {self.assessment.title}"


class UserAssessmentResult(models.Model):
    """
    Aggregated results for user's assessment performance across multiple attempts.
    """
    RESULT_TYPE_CHOICES = [
        ('assessment', 'Single Assessment'),
        ('module', 'Module Assessment'),
        ('learning_path', 'Learning Path Assessment'),
    ]
    
    # Core identification
    result_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_results')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_assessment_results')
    
    # Result type and scope
    result_type = models.CharField(max_length=20, choices=RESULT_TYPE_CHOICES, default='assessment')
    
    # Performance metrics
    total_attempts = models.PositiveIntegerField(default=0)
    best_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    questions_attempted = models.PositiveIntegerField(default=0)
    
    # Content coverage
    topics_covered = models.JSONField(default=list, help_text='Topics covered in assessments')
    learning_objectives_met = models.JSONField(default=list, help_text='Learning objectives achieved')
    
    # Time metrics
    average_time_minutes = models.FloatField(default=0.0, help_text='Average time spent per attempt in minutes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_assessment_results'
        verbose_name = 'User Assessment Result'
        verbose_name_plural = 'User Assessment Results'
        ordering = ['-updated_at']
        unique_together = ('user', 'module', 'result_type')
    
    def __str__(self):
        return f"Result {self.result_id} - {self.user.username} - {self.module.title}"