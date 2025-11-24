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
    
    # Structure
    order = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()
    difficulty_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Difficulty rating from 1 (easiest) to 5 (hardest)'
    )
    
    # JAC-specific content
    jac_concepts = models.JSONField(default=list, blank=True, help_text='JAC concepts covered in this module')
    code_examples = models.JSONField(default=list, blank=True)
    
    # Interactive elements
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
    def completion_rate(self):
        """Get completion rate for this module."""
        from django.db.models import Count
        total_users = UserModuleProgress.objects.filter(module=self).count()
        if total_users == 0:
            return 0
        completed_users = UserModuleProgress.objects.filter(
            module=self, 
            status='completed'
        ).count()
        return (completed_users / total_users) * 100
    
    @property
    def average_score(self):
        """Get average quiz/score for this module."""
        from django.db.models import Avg
        from apps.assessments.models import AssessmentAttempt
        return AssessmentAttempt.objects.filter(
            module=self
        ).aggregate(avg_score=Avg('score'))['avg_score'] or 0


class Lesson(models.Model):
    """
    Represents a lesson within a module.
    """
    LESSON_TYPE_CHOICES = [
        ('text', 'Text Lesson'),
        ('video', 'Video Lesson'),
        ('interactive', 'Interactive Content'),
        ('code_tutorial', 'Code Tutorial'),
        ('quiz', 'Quiz'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()
    lesson_type = models.CharField(
        max_length=20, 
        choices=LESSON_TYPE_CHOICES, 
        default='text'
    )
    
    # Content
    content = models.TextField(blank=True, help_text='Lesson content in markdown or HTML')
    code_example = models.TextField(blank=True, help_text='Code examples for this lesson')
    
    # Interactive elements
    quiz_questions = models.JSONField(default=list, blank=True, help_text='Quiz questions data')
    interactive_demo = models.JSONField(default=dict, blank=True, help_text='Interactive demo configuration')
    
    # Media
    video_url = models.URLField(blank=True, help_text='URL to lesson video')
    audio_url = models.URLField(blank=True, help_text='URL to lesson audio')
    resources = models.JSONField(default=list, blank=True, help_text='Additional resources for this lesson')
    
    # Publishing
    is_published = models.BooleanField(default=False)
    estimated_duration = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text='Estimated duration in minutes'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_lesson'
        ordering = ['module', 'order']
        unique_together = ['module', 'order']
        indexes = [
            models.Index(fields=['module', 'order']),
            models.Index(fields=['lesson_type']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"
    
    @property
    def module_title(self):
        """Get the title of the parent module."""
        return self.module.title
    
    @property
    def learning_path(self):
        """Get the learning path this lesson belongs to."""
        return self.module.learning_path


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
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessments')
    # Questions are managed through AssessmentQuestion model for proper relationship handling
    
    # Publishing
    is_published = models.BooleanField(default=False)
    
    # Statistics (calculated field)
    average_score = models.FloatField(default=0.0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_assessment'
        ordering = ['title']
        indexes = [
            models.Index(fields=['assessment_type']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['is_published']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.assessment_type})"
    
    @property
    def question_count(self):
        """Get total number of questions in this assessment."""
        return self.questions.count()
    
    @property
    def module_title(self):
        """Get the title of the parent module."""
        return self.module.title


class Question(models.Model):
    """
    Represents a question within an assessment.
    """
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
        ('code', 'Code Challenge'),
        ('drag_drop', 'Drag and Drop'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='question_set')
    question_text = models.TextField()
    
    # Question details
    question_type = models.CharField(
        max_length=20, 
        choices=QUESTION_TYPE_CHOICES, 
        default='multiple_choice'
    )
    difficulty_level = models.CharField(
        max_length=20, 
        choices=DIFFICULTY_CHOICES, 
        default='beginner'
    )
    points = models.FloatField(
        default=1.0, 
        help_text='Points awarded for correct answer'
    )
    
    # Content
    question_options = models.JSONField(
        default=list, 
        blank=True, 
        help_text='Answer options for multiple choice questions'
    )
    correct_answer = models.JSONField(
        default=dict, 
        blank=True, 
        help_text='Correct answer data'
    )
    code_template = models.TextField(
        blank=True, 
        help_text='Code template for coding questions'
    )
    test_cases = models.JSONField(
        default=list, 
        blank=True, 
        help_text='Test cases for code validation'
    )
    
    # Guidance
    explanation = models.TextField(
        blank=True, 
        help_text='Explanation of the correct answer'
    )
    hints = models.JSONField(
        default=list, 
        blank=True, 
        help_text='Hints to help users answer'
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_question'
        ordering = ['assessment', 'id']
        indexes = [
            models.Index(fields=['assessment']),
            models.Index(fields=['question_type']),
            models.Index(fields=['difficulty_level']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Q: {self.question_text[:50]}..."


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
            models.Index(fields=['status', 'last_activity_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.learning_path.name}"
    
    def start_path(self):
        """Mark path as started."""
        if self.status == 'not_started':
            self.status = 'in_progress'
            self.started_at = timezone.now()
            self.save()
    
    def complete_path(self):
        """Mark path as completed."""
        self.status = 'completed'
        self.progress_percentage = 100
        self.completed_at = timezone.now()
        self.save()
    
    def get_completion_percentage(self):
        """Calculate current completion percentage."""
        total_modules = self.learning_path.module_count
        if total_modules == 0:
            return 0
        
        completed_modules = UserModuleProgress.objects.filter(
            user=self.user,
            module__learning_path=self.learning_path,
            status='completed'
        ).count()
        
        return (completed_modules / total_modules) * 100


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
        
        # Update user statistics (commented out for default User model)
        # self.user.total_modules_completed += 1
        # self.user.total_time_spent += self.time_spent
        # self.user.add_points(10)  # Points for completing a module
        # self.user.update_streak()
        # self.user.save()
    
    def add_time_spent(self, minutes):
        """Add time spent to the module."""
        from datetime import timedelta
        self.time_spent += timedelta(minutes=minutes)
        self.save()
        
        # Update user total time (commented out for default User model)
        # self.user.total_time_spent += timedelta(minutes=minutes)
        # self.user.save()


class PathRating(models.Model):
    """
    User ratings and reviews for learning paths.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='path_ratings')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='ratings')
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 (poor) to 5 (excellent)'
    )
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_path_rating'
        unique_together = ['user', 'learning_path']
        indexes = [
            models.Index(fields=['learning_path', 'rating']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.learning_path.name} ({self.rating}/5)"


class LearningRecommendation(models.Model):
    """
    AI-generated learning recommendations for users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    
    recommendation_type = models.CharField(
        max_length=30,
        choices=[
            ('next_module', 'Next Module Recommendation'),
            ('skill_gap', 'Skill Gap Analysis'),
            ('review_topic', 'Review Topic Suggestion'),
            ('challenging_exercise', 'Challenging Exercise'),
        ]
    )
    
    # Recommendation content
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True)
    content = models.JSONField(help_text='Recommendation details and reasoning')
    priority_score = models.FloatField(default=0.0, help_text='AI-calculated priority score')
    
    # Status tracking
    is_dismissed = models.BooleanField(default=False)
    is_acted_upon = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        db_table = 'jac_learning_recommendation'
        indexes = [
            models.Index(fields=['user', 'recommendation_type']),
            models.Index(fields=['user', 'is_dismissed', 'expires_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.recommendation_type}"
    
    def is_expired(self):
        """Check if recommendation has expired."""
        return timezone.now() > self.expires_at
    
    def dismiss(self):
        """Mark recommendation as dismissed."""
        self.is_dismissed = True
        self.save()
    
    def mark_acted_upon(self):
        """Mark recommendation as acted upon."""
        self.is_acted_upon = True
        self.save()


# ============================================================================
# JAC CODE EXECUTION MODELS
# ============================================================================

class CodeSubmission(models.Model):
    """Code submission for JAC code evaluation"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Execution Error'),
        ('timeout', 'Timeout'),
    ]
    
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('jac', 'JAC (Jaseci)'),
        ('javascript', 'JavaScript'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_submissions')
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, null=True, blank=True, related_name='code_submissions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True, related_name='code_submissions')
    
    # Code details
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    
    # Execution results
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_result = models.JSONField(default=dict, blank=True)
    ai_feedback = models.TextField(blank=True)
    score = models.FloatField(null=True, blank=True)
    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.FloatField(null=True, blank=True)
    
    # Metadata
    submitted_at = models.DateTimeField(default=timezone.now)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer_agent_id = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = 'jac_code_submissions'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['language']),
            models.Index(fields=['submission_id']),
        ]
    
    def __str__(self):
        return f"{self.task_title} - {self.user.username} ({self.status})"


class TestCase(models.Model):
    """Test cases for code validation"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='test_cases')
    task_title = models.CharField(max_length=200)
    test_input = models.JSONField(default=dict)
    expected_output = models.JSONField(default=dict)
    test_description = models.TextField(blank=True)
    is_required = models.BooleanField(default=True)
    points = models.FloatField(default=1.0)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'jac_test_cases'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Test for {self.task_title}"


class CodeExecutionLog(models.Model):
    """Detailed logs of code execution for debugging and analytics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='execution_logs')
    execution_id = models.CharField(max_length=100)
    output = models.TextField(blank=True)
    error_output = models.TextField(blank=True)
    execution_time = models.FloatField()
    memory_usage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'jac_code_execution_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['execution_id']),
            models.Index(fields=['submission']),
        ]
    
    def __str__(self):
        return f"Execution {self.execution_id} for {self.submission.submission_id}"


class AICodeReview(models.Model):
    """AI-generated code reviews and feedback"""
    
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
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'jac_ai_code_reviews'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"AI Review - {self.review_type} for {self.submission.submission_id}"


class AssessmentAttempt(models.Model):
    """
    Represents an attempt by a user at taking an assessment.
    """
    ATTEMPT_STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
        ('timed_out', 'Timed Out'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessment_attempts', null=True, blank=True)
    
    # Attempt details
    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=ATTEMPT_STATUS_CHOICES, default='in_progress')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Scoring
    score = models.FloatField(null=True, blank=True)
    max_score = models.FloatField(default=100.0)
    passing_score = models.FloatField(default=70.0)
    is_passed = models.BooleanField(default=False)
    
    # Time tracking
    time_spent = models.DurationField(default=0)
    time_limit = models.PositiveIntegerField(null=True, blank=True, help_text='Time limit in minutes')
    
    # Results
    answers = models.JSONField(default=dict, help_text='User answers for each question')
    feedback = models.TextField(blank=True)
    
    class Meta:
        db_table = 'jac_assessment_attempts'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'assessment']),
            models.Index(fields=['status', 'started_at']),
            models.Index(fields=['assessment', 'attempt_number']),
        ]
        unique_together = ['user', 'assessment', 'attempt_number']
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} (Attempt {self.attempt_number})"
    
    def complete_attempt(self, score: float, answers: dict, feedback: str = ""):
        """Mark attempt as completed with results."""
        self.score = score
        self.answers = answers
        self.feedback = feedback
        self.is_passed = score >= self.passing_score
        self.status = 'completed'
        self.completed_at = timezone.now()
        if self.started_at:
            self.time_spent = self.completed_at - self.started_at
        self.save()


class UserAssessmentResult(models.Model):
    """
    Aggregated results for user's assessment performance across multiple attempts.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_results')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='user_results')
    
    # Aggregated statistics
    best_score = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    total_attempts = models.PositiveIntegerField(default=0)
    passed_attempts = models.PositiveIntegerField(default=0)
    total_time_spent = models.DurationField(default=0)
    
    # Performance metrics
    first_attempt_score = models.FloatField(null=True, blank=True)
    last_attempt_score = models.FloatField(null=True, blank=True)
    improvement_rate = models.FloatField(default=0.0)
    
    # Dates
    first_attempt_date = models.DateTimeField(null=True, blank=True)
    last_attempt_date = models.DateTimeField(null=True, blank=True)
    passed_date = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_user_assessment_results'
        unique_together = ['user', 'assessment']
        indexes = [
            models.Index(fields=['user', 'assessment']),
            models.Index(fields=['is_completed', 'best_score']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.assessment.title} (Best: {self.best_score}%)"
    
    def update_from_attempts(self, attempts_queryset):
        """Update result statistics from related assessment attempts."""
        attempts = list(attempts_queryset.order_by('started_at'))
        
        if not attempts:
            return
        
        self.total_attempts = len(attempts)
        self.first_attempt_date = attempts[0].started_at
        self.last_attempt_date = attempts[-1].started_at
        
        # Calculate scores
        scores = [a.score for a in attempts if a.score is not None]
        if scores:
            self.best_score = max(scores)
            self.average_score = sum(scores) / len(scores)
            self.first_attempt_score = scores[0]
            self.last_attempt_score = scores[-1]
            
            if len(scores) > 1:
                self.improvement_rate = ((scores[-1] - scores[0]) / max(scores[0], 1)) * 100
        
        # Calculate passed attempts
        passed_attempts = [a for a in attempts if a.is_passed]
        self.passed_attempts = len(passed_attempts)
        
        if passed_attempts and not self.passed_date:
            self.passed_date = passed_attempts[0].completed_at
        
        # Calculate total time
        self.total_time_spent = sum((a.time_spent or 0) for a in attempts)
        
        # Check completion
        self.is_completed = any(a.is_passed for a in attempts)
        if self.is_completed and not self.completion_date:
            self.completion_date = self.passed_date
        
        self.save()


class AssessmentQuestion(models.Model):
    """
    Extended question model that links questions to assessments with additional metadata.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='assessment_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='assessment_links')
    
    # Question metadata
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    points = models.FloatField(default=1.0)
    order = models.PositiveIntegerField(default=0)
    
    # Question customization for this assessment
    question_text_override = models.TextField(blank=True, help_text='Override default question text for this assessment')
    options_override = models.JSONField(default=list, blank=True, help_text='Override default options for multiple choice')
    correct_answer_override = models.JSONField(default=list, blank=True, help_text='Override correct answer')
    
    # Statistics (calculated fields)
    total_attempts = models.PositiveIntegerField(default=0)
    correct_attempts = models.PositiveIntegerField(default=0)
    average_time = models.FloatField(default=0.0, help_text='Average time in seconds')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'jac_assessment_questions'
        ordering = ['assessment', 'order']
        unique_together = ['assessment', 'question']
        indexes = [
            models.Index(fields=['assessment', 'order']),
            models.Index(fields=['difficulty_level']),
        ]
    
    def __str__(self):
        return f"{self.assessment.title} - {self.question.question_text[:50]}..."
    
    @property
    def accuracy_rate(self):
        """Calculate accuracy rate for this question."""
        if self.total_attempts == 0:
            return 0.0
        return (self.correct_attempts / self.total_attempts) * 100


class Achievement(models.Model):
    """
    Achievement system for tracking user accomplishments.
    """
    ACHIEVEMENT_TYPE_CHOICES = [
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
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    
    # Achievement requirements
    requirements = models.JSONField(default=dict, help_text='Requirements to unlock this achievement')
    icon = models.CharField(max_length=200, blank=True, help_text='Icon URL or name')
    badge_color = models.CharField(max_length=20, default='blue', help_text='CSS color class')
    
    # Statistics
    unlock_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
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
        return f"{self.name} ({self.rarity})"


class UserAchievement(models.Model):
    """
    Tracks user achievements that have been unlocked.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    
    # Achievement context
    unlocked_at = models.DateTimeField(auto_now_add=True)
    context = models.JSONField(default=dict, help_text='Context when achievement was unlocked')
    progress_at_unlock = models.JSONField(default=dict, help_text='User progress at time of unlock')
    
    class Meta:
        db_table = 'jac_user_achievements'
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at']
        indexes = [
            models.Index(fields=['user', 'unlocked_at']),
            models.Index(fields=['achievement']),
        ]
    
    def __str__(self):
        return f"{self.user.username} unlocked {self.achievement.name}"