"""
Learning Serializers for Django REST Framework

Serializers for code submissions, learning paths, and progress tracking
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    LearningPath, Module, Lesson, UserLearningPath, UserModuleProgress,
    PathRating, LearningRecommendation, CodeSubmission, TestCase,
    CodeExecutionLog, AICodeReview, Assessment, Question
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


# ============================================================================
# ASSESSMENT API SERIALIZERS
# ============================================================================

from .models import AssessmentAttempt, UserAssessmentResult
from django.utils import timezone


class QuizListSerializer(serializers.ModelSerializer):
    """Serializer for quiz listing response"""
    
    learning_path_name = serializers.CharField(source='module.learning_path.name', read_only=True, allow_null=True)
    module_title = serializers.CharField(source='module.title', read_only=True, allow_null=True)
    question_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    total_attempts = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'difficulty_level',
            'learning_path_name', 'module_title',
            'time_limit', 'max_attempts', 'passing_score',
            'is_published', 'average_score', 'question_count',
            'total_attempts', 'created_at', 'updated_at'
        ]
    
    def get_question_count(self, obj):
        return obj.questions.count()
    
    def get_average_score(self, obj):
        from django.db.models import Avg
        attempts = AssessmentAttempt.objects.filter(assessment=obj, status='completed')
        if attempts.exists():
            return attempts.aggregate(avg_score=Avg('score'))['avg_score'] or 0
        return 0
    
    def get_total_attempts(self, obj):
        return AssessmentAttempt.objects.filter(assessment=obj).count()


class QuizDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed quiz information"""
    
    learning_path_name = serializers.CharField(source='module.learning_path.name', read_only=True, allow_null=True)
    module_title = serializers.CharField(source='module.title', read_only=True, allow_null=True)
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'difficulty_level',
            'learning_path_name', 'module_title',
            'time_limit', 'max_attempts', 'passing_score',
            'is_published', 'questions', 'created_at', 'updated_at'
        ]
    
    def get_questions(self, obj):
        questions = obj.question_set.all().order_by('id')
        question_data = []
        for question in questions:
            question_data.append({
                'id': str(question.id),
                'type': question.question_type,
                'text': question.question_text,
                'options': question.question_options,
                'difficulty': question.difficulty_level,
                'points': question.points
            })
        return question_data


class AttemptListSerializer(serializers.ModelSerializer):
    """Serializer for listing user assessment attempts"""
    
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    assessment_type = serializers.CharField(source='assessment.assessment_type', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True, allow_null=True)
    percentage_score = serializers.SerializerMethodField()
    is_passed_text = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'assessment', 'assessment_title', 'assessment_type',
            'module', 'module_title', 'attempt_number', 'status',
            'score', 'max_score', 'passing_score', 'is_passed',
            'percentage_score', 'is_passed_text', 'time_spent',
            'started_at', 'completed_at', 'feedback'
        ]
        read_only_fields = [
            'id', 'attempt_number', 'status', 'started_at', 'completed_at'
        ]
    
    def get_percentage_score(self, obj):
        if obj.score is not None and obj.max_score > 0:
            return round((obj.score / obj.max_score) * 100, 2)
        return 0
    
    def get_is_passed_text(self, obj):
        return "Passed" if obj.is_passed else "Failed"


class AttemptDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed attempt information"""
    
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    assessment_type = serializers.CharField(source='assessment.assessment_type', read_only=True)
    percentage_score = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = AssessmentAttempt
        fields = [
            'id', 'assessment', 'assessment_title', 'assessment_type',
            'attempt_number', 'status', 'score', 'max_score',
            'passing_score', 'is_passed', 'percentage_score',
            'time_spent', 'duration_minutes', 'answers', 'feedback',
            'started_at', 'completed_at'
        ]
        read_only_fields = [
            'id', 'attempt_number', 'status', 'started_at', 'completed_at'
        ]
    
    def get_percentage_score(self, obj):
        if obj.score is not None and obj.max_score > 0:
            return round((obj.score / obj.max_score) * 100, 2)
        return 0
    
    def get_duration_minutes(self, obj):
        if obj.time_spent:
            return round(obj.time_spent.total_seconds() / 60, 2)
        return 0


class StartAttemptSerializer(serializers.Serializer):
    """Serializer for starting a new assessment attempt"""
    
    def create(self, validated_data):
        user = self.context['request'].user
        assessment = self.context['assessment']
        
        # Get attempt number
        last_attempt = AssessmentAttempt.objects.filter(
            user=user,
            assessment=assessment
        ).order_by('-attempt_number').first()
        
        attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1
        
        # Check if user has reached max attempts
        if attempt_number > assessment.max_attempts:
            raise serializers.ValidationError(
                f"Maximum attempts ({assessment.max_attempts}) reached for this assessment"
            )
        
        # Create new attempt
        attempt = AssessmentAttempt.objects.create(
            user=user,
            assessment=assessment,
            attempt_number=attempt_number,
            status='in_progress'
        )
        
        return attempt


class SubmitAttemptSerializer(serializers.Serializer):
    """Serializer for submitting an assessment attempt"""
    
    answers = serializers.JSONField()
    time_taken = serializers.IntegerField(required=False, help_text='Time taken in seconds')
    
    def validate(self, data):
        attempt = self.instance
        if attempt.status != 'in_progress':
            raise serializers.ValidationError("Can only submit attempts that are in progress")
        
        return data
    
    def update(self, instance, validated_data):
        from datetime import timedelta
        
        answers = validated_data.get('answers', {})
        time_taken = validated_data.get('time_taken', 0)
        
        # Calculate score (simplified scoring logic)
        score = self._calculate_score(instance.assessment, answers)
        
        # Update attempt
        instance.status = 'completed'
        instance.completed_at = timezone.now()
        instance.score = score
        instance.answers = answers
        instance.time_spent = timedelta(seconds=time_taken)
        instance.is_passed = score >= instance.passing_score
        
        # Add feedback
        if instance.is_passed:
            instance.feedback = f"Congratulations! You passed with {score:.1f}%."
        else:
            instance.feedback = f"You scored {score:.1f}%. The passing score is {instance.passing_score:.1f}%."
        
        instance.save()
        
        return instance
    
    def _calculate_score(self, assessment, answers):
        """Calculate score based on answers (simplified logic)"""
        if not assessment.questions.exists():
            return 0
        
        total_points = 0
        earned_points = 0
        
        for question in assessment.questions.all():
            total_points += question.points
            
            # Get user answer for this question
            user_answer = answers.get(str(question.id))
            if user_answer is not None:
                # Simple scoring - in real implementation, this would be more sophisticated
                if self._is_answer_correct(question, user_answer):
                    earned_points += question.points
        
        if total_points > 0:
            return (earned_points / total_points) * 100
        return 0
    
    def _is_answer_correct(self, question, user_answer):
        """Check if user answer is correct"""
        correct_answer = question.correct_answer
        
        # Handle different question types
        if question.question_type == 'multiple_choice':
            return user_answer in correct_answer
        elif question.question_type == 'true_false':
            return str(user_answer).lower() == str(correct_answer).lower()
        else:
            # For other types, do simple string comparison
            return str(user_answer).strip().lower() == str(correct_answer).strip().lower()


class AssessmentStatsSerializer(serializers.Serializer):
    """Serializer for assessment statistics"""
    
    total_assessments = serializers.IntegerField()
    completed_assessments = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_attempts = serializers.IntegerField()
    passed_attempts = serializers.IntegerField()
    pass_rate = serializers.FloatField()
    total_time_spent = serializers.DurationField()
    best_score = serializers.FloatField()
    recent_attempts = AttemptListSerializer(many=True, read_only=True)


# ============================================================================
# ADAPTIVE LEARNING SERIALIZERS
# ============================================================================

import json


class UserDifficultyProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserDifficultyProfile model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    overall_skill_level = serializers.ReadOnlyField()
    should_increase_difficulty = serializers.ReadOnlyField()
    should_decrease_difficulty = serializers.ReadOnlyField()
    
    class Meta:
        model = UserDifficultyProfile
        fields = [
            'id', 'user', 'user_username', 'current_difficulty', 'jac_knowledge_level',
            'problem_solving_level', 'coding_skill_level', 'learning_speed',
            'retention_rate', 'preferred_challenge_increase', 'challenge_tolerance',
            'recent_accuracy', 'success_streak', 'last_difficulty_change',
            'created_at', 'updated_at', 'overall_skill_level',
            'should_increase_difficulty', 'should_decrease_difficulty'
        ]
        read_only_fields = ['id', 'user', 'user_username', 'last_difficulty_change', 
                           'created_at', 'updated_at', 'overall_skill_level', 
                           'should_increase_difficulty', 'should_decrease_difficulty']


class AdaptiveChallengeSerializer(serializers.ModelSerializer):
    """Serializer for AdaptiveChallenge model."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = AdaptiveChallenge
        fields = [
            'id', 'title', 'description', 'challenge_type', 'content',
            'difficulty_level', 'skill_dimensions', 'estimated_time',
            'generated_by_agent', 'generation_prompt', 'adaptation_rules',
            'success_rate', 'average_completion_time', 'total_attempts',
            'successful_attempts', 'is_active', 'created_by', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'generated_by_agent', 'generation_prompt',
                           'success_rate', 'average_completion_time', 'total_attempts',
                           'successful_attempts', 'created_by', 'created_by_username',
                           'created_at', 'updated_at']


class ChallengeContentField(serializers.Field):
    """Custom field to handle challenge content as JSON."""
    
    def to_representation(self, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return {'content': value}
        return value
    
    def to_internal_value(self, data):
        if isinstance(data, dict):
            return json.dumps(data)
        return str(data)


class AdaptiveChallengeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for AdaptiveChallenge with parsed content."""
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    content = ChallengeContentField()
    
    class Meta:
        model = AdaptiveChallenge
        fields = [
            'id', 'title', 'description', 'challenge_type', 'content',
            'difficulty_level', 'skill_dimensions', 'estimated_time',
            'generated_by_agent', 'adaptation_rules', 'success_rate',
            'average_completion_time', 'total_attempts', 'successful_attempts',
            'is_active', 'created_by', 'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'generated_by_agent', 'success_rate',
                           'average_completion_time', 'total_attempts', 'successful_attempts',
                           'created_by', 'created_by_username', 'created_at', 'updated_at']


class UserChallengeAttemptSerializer(serializers.ModelSerializer):
    """Serializer for UserChallengeAttempt model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)
    difficulty_rating = serializers.ReadOnlyField(source='get_difficulty_rating')
    
    class Meta:
        model = UserChallengeAttempt
        fields = [
            'id', 'user', 'user_username', 'challenge', 'challenge_title',
            'status', 'score', 'time_spent', 'responses', 'feedback',
            'difficulty_feedback', 'learning_insights', 'started_at',
            'completed_at', 'difficulty_rating'
        ]
        read_only_fields = ['id', 'user', 'user_username', 'challenge', 'challenge_title',
                           'started_at', 'completed_at', 'difficulty_rating']


class UserChallengeAttemptCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new challenge attempts."""
    
    class Meta:
        model = UserChallengeAttempt
        fields = ['challenge']
        read_only_fields = ['id', 'user', 'challenge', 'status', 'started_at']


class UserChallengeAttemptSubmitSerializer(serializers.ModelSerializer):
    """Serializer for submitting challenge responses."""
    
    class Meta:
        model = UserChallengeAttempt
        fields = ['responses', 'feedback']


class ChallengeSubmissionResponseSerializer(serializers.Serializer):
    """Serializer for challenge submission response."""
    success = serializers.BooleanField()
    score = serializers.FloatField(required=False)
    feedback = serializers.CharField(required=False, allow_blank=True)
    next_steps = serializers.ListField(child=serializers.CharField(), required=False)
    difficulty_adjustment = serializers.DictField(required=False)


class SpacedRepetitionSessionSerializer(serializers.ModelSerializer):
    """Serializer for SpacedRepetitionSession model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)
    is_due_for_review = serializers.ReadOnlyField()
    
    class Meta:
        model = SpacedRepetitionSession
        fields = [
            'id', 'user', 'user_username', 'challenge', 'challenge_title',
            'review_stage', 'ease_factor', 'interval_days', 'scheduled_for',
            'completed_at', 'quality_rating', 'status', 'created_at', 'updated_at',
            'is_due_for_review'
        ]
        read_only_fields = ['id', 'user', 'user_username', 'challenge', 'challenge_title',
                           'created_at', 'updated_at', 'is_due_for_review']


class SpacedRepetitionReviewSerializer(serializers.Serializer):
    """Serializer for completing spaced repetition reviews."""
    quality_rating = serializers.IntegerField(min_value=0, max_value=5)


class ChallengeGenerationRequestSerializer(serializers.Serializer):
    """Serializer for challenge generation requests."""
    challenge_type = serializers.ChoiceField(
        choices=['quiz', 'coding', 'debug', 'scenario', 'project'],
        required=False, allow_blank=True
    )
    specific_topic = serializers.CharField(max_length=200, required=False, allow_blank=True)


class ChallengeGenerationResponseSerializer(serializers.Serializer):
    """Serializer for challenge generation responses."""
    success = serializers.BooleanField()
    challenge = AdaptiveChallengeDetailSerializer(required=False)
    attempt_id = serializers.UUIDField(required=False)
    personalization = serializers.DictField(required=False)
    error = serializers.CharField(required=False)


class PerformanceAnalysisSerializer(serializers.Serializer):
    """Serializer for performance analysis results."""
    success = serializers.BooleanField()
    user_id = serializers.UUIDField()
    analysis_period = serializers.CharField()
    performance_data = serializers.DictField()
    difficulty_metrics = serializers.DictField()
    learning_patterns = serializers.DictField()
    recommendations = serializers.DictField()
    generated_at = serializers.DateTimeField()


class DifficultyAdjustmentSerializer(serializers.Serializer):
    """Serializer for difficulty adjustment requests."""
    adjustment_type = serializers.ChoiceField(choices=['increase', 'decrease', 'maintain'])


class DifficultyAdjustmentResponseSerializer(serializers.Serializer):
    """Serializer for difficulty adjustment responses."""
    success = serializers.BooleanField()
    adjustment_applied = serializers.BooleanField()
    old_difficulty = serializers.CharField(required=False)
    new_difficulty = serializers.CharField(required=False)
    adjustment_date = serializers.DateTimeField(required=False)
    message = serializers.CharField()


class DueReviewSerializer(serializers.Serializer):
    """Serializer for due review challenges."""
    session_id = serializers.UUIDField()
    challenge = AdaptiveChallengeDetailSerializer()
    review_stage = serializers.IntegerField()
    ease_factor = serializers.FloatField()
    scheduled_for = serializers.DateTimeField()


class DueReviewsResponseSerializer(serializers.Serializer):
    """Serializer for response containing due reviews."""
    reviews = serializers.ListField(child=DueReviewSerializer())


# ===== COMPOSITE SERIALIZERS =====

class UserLearningSummarySerializer(serializers.Serializer):
    """Serializer for user learning summary with adaptive features."""
    user_username = serializers.CharField()
    difficulty_profile = UserDifficultyProfileSerializer()
    recent_attempts = UserChallengeAttemptSerializer(many=True)
    due_reviews = SpacedRepetitionSessionSerializer(many=True)
    performance_summary = serializers.DictField()
    recommendations = LearningRecommendationSerializer(many=True)


class ChallengeAnalyticsSerializer(serializers.Serializer):
    """Serializer for challenge analytics."""
    challenge_id = serializers.UUIDField()
    title = serializers.CharField()
    challenge_type = serializers.CharField()
    difficulty_level = serializers.CharField()
    success_rate = serializers.FloatField()
    average_completion_time = serializers.FloatField()
    total_attempts = serializers.IntegerField()
    user_performance = serializers.DictField()


class LearningProgressSerializer(serializers.Serializer):
    """Serializer for comprehensive learning progress."""
    user_id = serializers.UUIDField()
    current_difficulty = serializers.CharField()
    skill_levels = serializers.DictField()
    recent_performance = serializers.DictField()
    learning_velocity = serializers.FloatField()
    engagement_score = serializers.FloatField()
    next_recommended_challenge = AdaptiveChallengeSerializer()
    spaced_repetition_count = serializers.IntegerField()
    recommendations = LearningRecommendationSerializer(many=True)