# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Assessment serializers for Django REST Framework
"""

from rest_framework import serializers
from .models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for assessment questions
    """
    class Meta:
        model = AssessmentQuestion
        fields = [
            'question_id', 'module', 'title', 'question_text', 'question_type',
            'difficulty', 'options', 'correct_answer', 'explanation', 'points',
            'tags', 'learning_objectives', 'is_active', 'version',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['question_id', 'created_at', 'updated_at']
    
    def validate_options(self, value):
        """Validate options for multiple choice questions"""
        question_type = self.initial_data.get('question_type', '')
        if question_type == 'multiple_choice' and not value:
            raise serializers.ValidationError(
                "Options are required for multiple choice questions"
            )
        return value
    
    def validate_points(self, value):
        """Validate points are positive"""
        if value <= 0:
            raise serializers.ValidationError("Points must be greater than 0")
        return value


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for assessment attempts
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    # Calculated fields
    is_passed = serializers.ReadOnlyField()
    duration_minutes = serializers.ReadOnlyField()
    
    class Meta:
        model = AssessmentAttempt
        fields = [
            'attempt_id', 'user', 'user_username', 'module', 'module_title',
            'status', 'started_at', 'completed_at', 'time_limit_minutes',
            'score', 'max_score', 'passing_score', 'answers', 'feedback',
            'is_passed', 'duration_minutes'
        ]
        read_only_fields = [
            'attempt_id', 'started_at', 'completed_at', 'is_passed', 'duration_minutes'
        ]
    
    def validate_score(self, value):
        """Validate score is within valid range"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Score must be between 0 and 100")
        return value
    
    def validate_time_limit_minutes(self, value):
        """Validate time limit is reasonable"""
        if value <= 0 or value > 480:  # Max 8 hours
            raise serializers.ValidationError(
                "Time limit must be between 1 and 480 minutes"
            )
        return value


class AssessmentAttemptCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new assessment attempts
    """
    class Meta:
        model = AssessmentAttempt
        fields = ['module', 'time_limit_minutes']
    
    def create(self, validated_data):
        """Create new assessment attempt with UUID"""
        import uuid
        
        user = self.context['request'].user
        attempt_id = uuid.uuid4()
        
        return AssessmentAttempt.objects.create(
            attempt_id=attempt_id,
            user=user,
            **validated_data
        )


class AssessmentAttemptSubmitSerializer(serializers.ModelSerializer):
    """
    Serializer for submitting assessment attempts with answers
    """
    class Meta:
        model = AssessmentAttempt
        fields = ['answers']
    
    def validate_answers(self, value):
        """Validate answers format"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Answers must be a dictionary")
        return value


class UserAssessmentResultSerializer(serializers.ModelSerializer):
    """
    Serializer for user assessment results
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = UserAssessmentResult
        fields = [
            'result_id', 'user', 'user_username', 'module', 'module_title',
            'result_type', 'total_attempts', 'best_score', 'average_score',
            'average_time_minutes', 'questions_attempted', 'topics_covered',
            'learning_objectives_met', 'created_at', 'updated_at'
        ]
        read_only_fields = ['result_id', 'created_at', 'updated_at']


class AssessmentQuestionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing assessment questions
    """
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = AssessmentQuestion
        fields = [
            'question_id', 'module', 'module_title', 'title', 'question_type',
            'difficulty', 'points', 'is_active', 'created_at'
        ]


class AssessmentStatsSerializer(serializers.Serializer):
    """
    Serializer for assessment statistics
    """
    module_id = serializers.UUIDField()
    module_title = serializers.CharField()
    
    # Attempt statistics
    total_attempts = serializers.IntegerField()
    completed_attempts = serializers.IntegerField()
    average_score = serializers.FloatField()
    pass_rate = serializers.FloatField()
    
    # Time statistics
    average_duration = serializers.FloatField()
    fastest_attempt = serializers.FloatField()
    slowest_attempt = serializers.FloatField()
    
    # Question statistics
    total_questions = serializers.IntegerField()
    questions_attempted = serializers.IntegerField()
    
    # User statistics
    unique_users = serializers.IntegerField()
    returning_users = serializers.IntegerField()
    
    class Meta:
        fields = [
            'module_id', 'module_title', 'total_attempts', 'completed_attempts',
            'average_score', 'pass_rate', 'average_duration', 'fastest_attempt',
            'slowest_attempt', 'total_questions', 'questions_attempted',
            'unique_users', 'returning_users'
        ]


class AssessmentQuestionSubmissionSerializer(serializers.Serializer):
    """
    Serializer for submitting individual question answers
    """
    question_id = serializers.UUIDField()
    answer = serializers.CharField(allow_blank=True)
    
    def validate_question_id(self, value):
        """Validate question exists"""
        try:
            AssessmentQuestion.objects.get(question_id=value)
            return value
        except AssessmentQuestion.DoesNotExist:
            raise serializers.ValidationError("Question not found")
    
    def validate(self, data):
        """Validate answer format matches question type"""
        question_id = data['question_id']
        answer = data['answer']
        
        try:
            question = AssessmentQuestion.objects.get(question_id=question_id)
            
            if question.question_type == 'multiple_choice':
                if answer not in question.options:
                    raise serializers.ValidationError({
                        'answer': 'Answer must be one of the provided options'
                    })
            elif question.question_type in ['true_false']:
                if answer not in ['true', 'false']:
                    raise serializers.ValidationError({
                        'answer': 'Answer must be "true" or "false"'
                    })
            elif question.question_type in ['short_answer', 'essay']:
                if not answer.strip():
                    raise serializers.ValidationError({
                        'answer': 'Answer cannot be empty'
                    })
        
        except AssessmentQuestion.DoesNotExist:
            pass  # Already validated above
        
        return data