"""
Learning Serializers for Django REST Framework

Serializers for code submissions, learning paths, and progress tracking
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    LearningPath, Module, Lesson, UserLearningPath, UserModuleProgress,
    PathRating, LearningRecommendation, CodeSubmission, TestCase,
    CodeExecutionLog, AICodeReview
)


class CodeSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for code submissions"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_title = serializers.CharField(source='learning_path.name', read_only=True, allow_null=True)
    module_title = serializers.CharField(source='module.title', read_only=True, allow_null=True)
    
    class Meta:
        model = CodeSubmission
        fields = [
            'id', 'submission_id', 'user', 'user_username', 'learning_path', 'learning_path_title',
            'module', 'module_title', 'task_title', 'task_description', 'code', 'language',
            'status', 'execution_result', 'ai_feedback', 'score', 'execution_time',
            'memory_usage', 'submitted_at', 'reviewed_at', 'reviewer_agent_id'
        ]
        read_only_fields = [
            'id', 'submission_id', 'submitted_at', 'reviewed_at', 'status', 
            'execution_result', 'ai_feedback', 'score', 'execution_time', 'memory_usage'
        ]


class CodeSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating code submissions"""
    
    class Meta:
        model = CodeSubmission
        fields = [
            'learning_path', 'module', 'task_title', 'task_description',
            'code', 'language'
        ]
    
    def create(self, validated_data):
        import uuid
        user = self.context['request'].user
        submission_id = f"sub_{uuid.uuid4().hex[:12]}"
        
        return CodeSubmission.objects.create(
            user=user,
            submission_id=submission_id,
            **validated_data
        )


class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for learning paths"""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    module_count = serializers.ReadOnlyField()
    completed_by_users = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'name', 'description', 'difficulty_level', 'estimated_duration',
            'prerequisites', 'cover_image', 'tags', 'is_published', 'is_featured',
            'created_by', 'created_by_username', 'created_at', 'updated_at',
            'module_count', 'completed_by_users', 'average_rating'
        ]
        read_only_fields = [
            'id', 'created_by_username', 'created_at', 'updated_at',
            'module_count', 'completed_by_users', 'average_rating'
        ]


class LearningPathCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating learning paths"""
    
    class Meta:
        model = LearningPath
        fields = [
            'name', 'description', 'difficulty_level', 'estimated_duration',
            'prerequisites', 'tags', 'is_published', 'is_featured'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        return LearningPath.objects.create(
            created_by=user,
            **validated_data
        )


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for learning modules"""
    
    learning_path_name = serializers.CharField(source='learning_path.name', read_only=True)
    completion_rate = serializers.ReadOnlyField()
    average_score = serializers.ReadOnlyField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'learning_path', 'learning_path_name', 'title', 'description',
            'content', 'content_type', 'order', 'duration_minutes', 'difficulty_rating',
            'jac_concepts', 'code_examples', 'has_quiz', 'has_coding_exercise',
            'has_visual_demo', 'is_published', 'created_at', 'updated_at',
            'completion_rate', 'average_score'
        ]
        read_only_fields = [
            'id', 'learning_path_name', 'completion_rate', 'average_score',
            'created_at', 'updated_at'
        ]


class ModuleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating modules"""
    
    class Meta:
        model = Module
        fields = [
            'learning_path', 'title', 'description', 'content', 'content_type',
            'order', 'duration_minutes', 'difficulty_rating', 'jac_concepts',
            'code_examples', 'has_quiz', 'has_coding_exercise', 'has_visual_demo'
        ]


class UserLearningPathSerializer(serializers.ModelSerializer):
    """Serializer for user learning path progress"""
    
    learning_path_details = LearningPathSerializer(source='learning_path', read_only=True)
    
    class Meta:
        model = UserLearningPath
        fields = [
            'id', 'user', 'learning_path', 'learning_path_details',
            'status', 'progress_percentage', 'current_module_order',
            'started_at', 'completed_at', 'last_activity_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'started_at', 'last_activity_at', 'created_at', 'updated_at'
        ]


class UserModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for user module progress"""
    
    module_details = ModuleSerializer(source='module', read_only=True)
    
    class Meta:
        model = UserModuleProgress
        fields = [
            'id', 'user', 'module', 'module_details', 'status', 'time_spent',
            'progress_percentage', 'quiz_score', 'coding_score', 'overall_score',
            'user_notes', 'feedback', 'started_at', 'completed_at',
            'last_activity_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'started_at', 'last_activity_at', 'created_at', 'updated_at'
        ]


class PathRatingSerializer(serializers.ModelSerializer):
    """Serializer for path ratings"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_title = serializers.CharField(source='learning_path.name', read_only=True)
    
    class Meta:
        model = PathRating
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_title',
            'rating', 'review', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user_username', 'learning_path_title', 'created_at', 'updated_at'
        ]


class LearningRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for learning recommendations"""
    
    learning_path_title = serializers.CharField(source='learning_path.name', read_only=True, allow_null=True)
    module_title = serializers.CharField(source='module.title', read_only=True, allow_null=True)
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = LearningRecommendation
        fields = [
            'id', 'user', 'recommendation_type', 'learning_path', 'learning_path_title',
            'module', 'module_title', 'content', 'priority_score', 'is_dismissed',
            'is_acted_upon', 'created_at', 'expires_at', 'is_expired'
        ]
        read_only_fields = [
            'id', 'created_at', 'is_expired'
        ]


class TestCaseSerializer(serializers.ModelSerializer):
    """Serializer for test cases"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = TestCase
        fields = [
            'id', 'module', 'module_title', 'task_title', 'test_input',
            'expected_output', 'test_description', 'is_required', 'points',
            'created_at'
        ]
        read_only_fields = [
            'id', 'module_title', 'created_at'
        ]


class CodeExecutionLogSerializer(serializers.ModelSerializer):
    """Serializer for code execution logs"""
    
    submission_id = serializers.CharField(source='submission.submission_id', read_only=True)
    
    class Meta:
        model = CodeExecutionLog
        fields = [
            'id', 'submission', 'submission_id', 'execution_id', 'output',
            'error_output', 'execution_time', 'memory_usage', 'created_at'
        ]
        read_only_fields = [
            'id', 'submission_id', 'created_at'
        ]


class AICodeReviewSerializer(serializers.ModelSerializer):
    """Serializer for AI code reviews"""
    
    submission_id = serializers.CharField(source='submission.submission_id', read_only=True)
    
    class Meta:
        model = AICodeReview
        fields = [
            'id', 'submission', 'submission_id', 'review_type', 'findings',
            'suggestions', 'score', 'agent_id', 'created_at'
        ]
        read_only_fields = [
            'id', 'submission_id', 'created_at'
        ]


class CodeSubmissionReviewSerializer(serializers.Serializer):
    """Serializer for reviewing code submissions"""
    
    status = serializers.ChoiceField(choices=CodeSubmission.STATUS_CHOICES)
    ai_feedback = serializers.CharField(required=False, allow_blank=True)
    score = serializers.FloatField(required=False, allow_null=True)
    execution_time = serializers.FloatField(required=False, allow_null=True)
    memory_usage = serializers.FloatField(required=False, allow_null=True)
    execution_result = serializers.JSONField(required=False)
    reviewer_agent_id = serializers.CharField(required=False, allow_blank=True)


class LearningProgressSerializer(serializers.Serializer):
    """Serializer for learning progress overview"""
    
    total_paths = serializers.IntegerField()
    completed_paths = serializers.IntegerField()
    in_progress_paths = serializers.IntegerField()
    total_modules = serializers.IntegerField()
    completed_modules = serializers.IntegerField()
    total_code_submissions = serializers.IntegerField()
    successful_submissions = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_study_time = serializers.FloatField()  # in hours


class CodeExecutionRequestSerializer(serializers.Serializer):
    """Serializer for code execution requests"""
    
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=[
        ('python', 'Python'),
        ('jac', 'JAC (Jaseci)'),
        ('javascript', 'JavaScript')
    ])
    task_id = serializers.CharField(required=False, allow_blank=True)
    timeout = serializers.IntegerField(default=30, min_value=1, max_value=300)
    memory_limit = serializers.IntegerField(default=128, min_value=32, max_value=1024)
    allow_network = serializers.BooleanField(default=False)
    test_cases = serializers.ListField(
        child=serializers.JSONField(),
        required=False
    )


class CodeExecutionResponseSerializer(serializers.Serializer):
    """Serializer for code execution responses"""
    
    execution_id = serializers.CharField()
    status = serializers.CharField()
    success = serializers.BooleanField()
    output = serializers.CharField()
    error = serializers.CharField(allow_null=True)
    execution_time = serializers.FloatField()
    timestamp = serializers.DateTimeField()
    code_analysis = serializers.JSONField()
    security_assessment = serializers.JSONField()
    performance_metrics = serializers.JSONField()
    recommendations = serializers.ListField(
        child=serializers.CharField()
    )


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lessons"""
    
    learning_path_name = serializers.CharField(source='module.learning_path.name', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'module', 'learning_path_name', 'module_title', 'lesson_type',
            'title', 'content', 'code_examples', 'quiz_questions', 'interactive_demo',
            'media_urls', 'estimated_duration_minutes', 'difficulty_rating',
            'prerequisites', 'learning_objectives', 'is_published', 'order_index',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LessonCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating lessons"""
    
    class Meta:
        model = Lesson
        fields = [
            'module', 'lesson_type', 'title', 'content', 'code_examples',
            'quiz_questions', 'interactive_demo', 'media_urls',
            'estimated_duration_minutes', 'difficulty_rating', 'prerequisites',
            'learning_objectives', 'is_published', 'order_index'
        ]


class AssessmentSerializer(serializers.ModelSerializer):
    """Serializer for assessments"""
    
    learning_path_name = serializers.CharField(source='module.learning_path.name', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'module', 'learning_path_name', 'module_title', 'assessment_type',
            'title', 'description', 'time_limit_minutes', 'max_attempts',
            'passing_score_percentage', 'instructions', 'rubric_criteria',
            'is_published', 'is_mandatory', 'order_index', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AssessmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating assessments"""
    
    class Meta:
        model = Assessment
        fields = [
            'module', 'assessment_type', 'title', 'description',
            'time_limit_minutes', 'max_attempts', 'passing_score_percentage',
            'instructions', 'rubric_criteria', 'is_published', 'is_mandatory',
            'order_index'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for questions"""
    
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'assessment', 'assessment_title', 'question_type', 'question_text',
            'question_data', 'answer_options', 'correct_answer', 'explanation',
            'hints', 'code_template', 'test_cases', 'points_value', 'difficulty_level',
            'order_index', 'time_limit_seconds', 'is_required', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating questions"""
    
    class Meta:
        model = Question
        fields = [
            'assessment', 'question_type', 'question_text', 'question_data',
            'answer_options', 'correct_answer', 'explanation', 'hints',
            'code_template', 'test_cases', 'points_value', 'difficulty_level',
            'order_index', 'time_limit_seconds', 'is_required'
        ]