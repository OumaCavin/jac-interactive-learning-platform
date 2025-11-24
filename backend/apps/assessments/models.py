"""
Assessment models for JAC Learning Platform
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.learning.models import Module, Lesson

User = get_user_model()


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
        return f"Attempt {self.attempt_id} - {self.user.username} - {self.module.title}"
    
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
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessment_questions')
    
    # Question content
    title = models.CharField(max_length=255)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    
    # Options for multiple choice questions
    options = models.JSONField(
        default=list,
        blank=True,
        help_text='List of options for multiple choice questions'
    )
    
    # Answer details
    correct_answer = models.TextField(help_text='Correct answer or answer key')
    explanation = models.TextField(
        blank=True,
        help_text='Explanation for the correct answer'
    )
    
    # Scoring
    points = models.FloatField(default=1.0, validators=[MinValueValidator(0.1)])
    
    # Metadata
    tags = models.JSONField(default=list, help_text='Topic tags for the question')
    learning_objectives = models.JSONField(
        default=list,
        help_text='Learning objectives this question tests'
    )
    
    # Publishing and versioning
    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assessment_questions'
        verbose_name = 'Assessment Question'
        verbose_name_plural = 'Assessment Questions'
        ordering = ['module', 'difficulty', 'created_at']
        unique_together = ['module', 'version']
    
    def __str__(self):
        return f"{self.title} ({self.difficulty}) - {self.module.title}"


class UserAssessmentResult(models.Model):
    """
    Aggregated results for user assessment performance
    """
    RESULT_TYPE_CHOICES = [
        ('module_completion', 'Module Completion'),
        ('overall_performance', 'Overall Performance'),
        ('topic_mastery', 'Topic Mastery'),
        ('progress_tracking', 'Progress Tracking'),
    ]
    
    # Core identification
    result_id = models.UUIDField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_results')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='user_results')
    
    # Result details
    result_type = models.CharField(max_length=25, choices=RESULT_TYPE_CHOICES)
    
    # Performance metrics
    total_attempts = models.IntegerField(default=0)
    best_score = models.FloatField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)
    average_time_minutes = models.FloatField(null=True, blank=True)
    
    # Progress tracking
    questions_attempted = models.JSONField(default=dict)
    topics_covered = models.JSONField(default=list)
    learning_objectives_met = models.JSONField(default=list)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_assessment_results'
        verbose_name = 'User Assessment Result'
        verbose_name_plural = 'User Assessment Results'
        unique_together = ['user', 'module', 'result_type']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.result_type} - {self.module.title}"