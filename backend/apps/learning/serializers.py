"""
Learning Serializers for Django REST Framework

Serializers for learning paths, modules, lessons, and progress tracking
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    LearningPath, Module, Lesson, UserLearningPath, UserModuleProgress,
    PathRating, LearningRecommendation, Assessment, AssessmentQuestion, AssessmentAttempt,
    UserDifficultyProfile, AdaptiveChallenge, UserChallengeAttempt, SpacedRepetitionSession
)


class LearningPathSerializer(serializers.ModelSerializer):
    """Serializer for learning paths"""
    
    modules_count = serializers.SerializerMethodField()
    completed_modules_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningPath
        fields = [
            'id', 'name', 'description', 'difficulty_level', 'estimated_duration_hours',
            'tags', 'is_published', 'created_at', 'updated_at',
            'modules_count', 'completed_modules_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'modules_count', 'completed_modules_count']
    
    def get_modules_count(self, obj):
        return obj.modules.count()
    
    def get_completed_modules_count(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return UserModuleProgress.objects.filter(
                user=user, module__learning_path=obj, status='completed'
            ).count()
        return 0


class LearningPathCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating learning paths"""
    
    class Meta:
        model = LearningPath
        fields = ['name', 'description', 'difficulty_level', 'estimated_duration_hours', 'tags', 'is_published']
    
    def validate_difficulty_level(self, value):
        """Validate difficulty level choice"""
        if value not in [choice[0] for choice in LearningPath._meta.get_field('difficulty_level').choices]:
            raise serializers.ValidationError("Invalid difficulty level.")
        return value


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer for modules"""
    
    learning_path_name = serializers.CharField(source='learning_path.name', read_only=True)
    lessons_count = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = [
            'id', 'title', 'description', 'content', 'content_type', 'order',
            'duration_minutes', 'difficulty_rating', 'jac_concepts',
            'has_quiz', 'has_coding_exercise', 'has_visual_demo',
            'is_published', 'created_at', 'updated_at',
            'learning_path_name', 'lessons_count', 'progress_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'lessons_count', 'progress_percentage']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
    def get_progress_percentage(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            progress = UserModuleProgress.objects.filter(user=user, module=obj).first()
            return progress.completion_percentage if progress else 0
        return 0


class ModuleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating modules"""
    
    class Meta:
        model = Module
        fields = [
            'title', 'description', 'content', 'content_type', 'order',
            'duration_minutes', 'difficulty_rating', 'jac_concepts',
            'has_quiz', 'has_coding_exercise', 'has_visual_demo',
            'is_published', 'learning_path'
        ]
    
    def validate_difficulty_rating(self, value):
        """Validate difficulty rating is between 1 and 5"""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Difficulty rating must be between 1 and 5.")
        return value
    
    def validate_order(self, value):
        """Validate order is positive"""
        if value < 0:
            raise serializers.ValidationError("Order must be a positive integer.")
        return value


class LessonSerializer(serializers.ModelSerializer):
    """Serializer for lessons"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'order', 'lesson_type', 'content', 'code_example',
            'quiz_questions', 'interactive_demo', 'video_url', 'audio_url',
            'resources', 'is_published', 'estimated_duration',
            'created_at', 'updated_at', 'module_title'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_order(self, value):
        """Validate order is positive"""
        if value < 0:
            raise serializers.ValidationError("Order must be a positive integer.")
        return value


class LessonCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating lessons"""
    
    class Meta:
        model = Lesson
        fields = [
            'title', 'order', 'lesson_type', 'content', 'code_example',
            'quiz_questions', 'interactive_demo', 'video_url', 'audio_url',
            'resources', 'is_published', 'estimated_duration', 'module'
        ]


class UserLearningPathSerializer(serializers.ModelSerializer):
    """Serializer for user learning paths"""
    
    learning_path_name = serializers.CharField(source='learning_path.name', read_only=True)
    learning_path_description = serializers.CharField(source='learning_path.description', read_only=True)
    
    class Meta:
        model = UserLearningPath
        fields = [
            'id', 'learning_path', 'learning_path_name', 'learning_path_description',
            'status', 'progress_percentage', 'started_at', 'completed_at',
            'time_spent_minutes', 'last_accessed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'started_at', 'last_accessed', 'created_at', 'updated_at']


class UserModuleProgressSerializer(serializers.ModelSerializer):
    """Serializer for user module progress"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    module_description = serializers.CharField(source='module.description', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserModuleProgress
        fields = [
            'id', 'user', 'user_username', 'module', 'module_title', 'module_description',
            'status', 'completion_percentage', 'time_spent_minutes',
            'quiz_score', 'coding_score', 'overall_score', 'attempts_count',
            'last_accessed', 'estimated_mastery_time', 'learning_velocity',
            'retention_rate', 'difficulty_preference', 'optimal_session_length',
            'learning_style', 'recommended_study_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PathRatingSerializer(serializers.ModelSerializer):
    """Serializer for path ratings"""
    
    learning_path_name = serializers.CharField(source='learning_path.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PathRating
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_name',
            'rating', 'review_text', 'difficulty_rating', 'time_to_complete',
            'helpfulness_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5"""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate_helpfulness_score(self, value):
        """Validate helpfulness score is between 1 and 5"""
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Helpfulness score must be between 1 and 5.")
        return value


class LearningRecommendationSerializer(serializers.ModelSerializer):
    """Serializer for learning recommendations"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    learning_path_name = serializers.CharField(source='learning_path.name', read_only=True)
    
    class Meta:
        model = LearningRecommendation
        fields = [
            'id', 'user', 'user_username', 'learning_path', 'learning_path_name',
            'recommendation_type', 'confidence_score', 'reasoning',
            'is_accepted', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_confidence_score(self, value):
        """Validate confidence score is between 0 and 1"""
        if not 0 <= value <= 1:
            raise serializers.ValidationError("Confidence score must be between 0 and 1.")
        return value


class AssessmentSerializer(serializers.ModelSerializer):
    """Serializer for assessments"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = Assessment
        fields = [
            'id', 'title', 'description', 'assessment_type', 'difficulty_level',
            'time_limit', 'max_attempts', 'passing_score', 'module',
            'is_published', 'average_score', 'created_at', 'updated_at',
            'module_title'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'average_score']


class AssessmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating assessments"""
    
    class Meta:
        model = Assessment
        fields = [
            'title', 'description', 'assessment_type', 'difficulty_level',
            'time_limit', 'max_attempts', 'passing_score', 'module', 'is_published'
        ]


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    """Serializer for assessment questions"""
    
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = AssessmentQuestion
        fields = [
            'question_id', 'assessment', 'assessment_title', 'module', 'module_title',
            'title', 'question_text', 'question_type', 'options', 'correct_answer',
            'explanation', 'points', 'difficulty_level', 'order', 'tags',
            'learning_objectives', 'is_active', 'version', 'created_at', 'updated_at'
        ]
        read_only_fields = ['question_id', 'created_at', 'updated_at']


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    """Serializer for assessment attempts"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    assessment_title = serializers.CharField(source='assessment.title', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = AssessmentAttempt
        fields = [
            'attempt_id', 'user', 'user_username', 'assessment', 'assessment_title',
            'module', 'module_title', 'status', 'started_at', 'completed_at',
            'time_limit_minutes', 'score', 'max_score', 'passing_score',
            'answers', 'feedback', 'duration_minutes'
        ]
        read_only_fields = ['attempt_id', 'started_at', 'duration_minutes']


# Adaptive Learning Serializers

class UserDifficultyProfileSerializer(serializers.ModelSerializer):
    """Serializer for user difficulty profiles"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserDifficultyProfile
        fields = [
            'id', 'user', 'user_username', 'current_difficulty',
            'jac_knowledge_score', 'problem_solving_score', 'coding_skill_score',
            'mastery_levels', 'difficulty_history', 'last_updated',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdaptiveChallengeSerializer(serializers.ModelSerializer):
    """Serializer for adaptive challenges"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    
    class Meta:
        model = AdaptiveChallenge
        fields = [
            'id', 'title', 'challenge_type', 'difficulty_level', 'module',
            'module_title', 'content', 'correct_answer', 'explanation',
            'hints', 'estimated_time_minutes', 'tags', 'generated_by_ai',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdaptiveChallengeDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed adaptive challenge view"""
    
    module_title = serializers.CharField(source='module.title', read_only=True)
    user_attempts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AdaptiveChallenge
        fields = [
            'id', 'title', 'challenge_type', 'difficulty_level', 'module',
            'module_title', 'content', 'correct_answer', 'explanation',
            'hints', 'estimated_time_minutes', 'tags', 'generated_by_ai',
            'created_by', 'created_at', 'updated_at', 'user_attempts_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_attempts_count']
    
    def get_user_attempts_count(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return UserChallengeAttempt.objects.filter(user=user, challenge=obj).count()
        return 0


class UserChallengeAttemptSerializer(serializers.ModelSerializer):
    """Serializer for user challenge attempts"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)
    
    class Meta:
        model = UserChallengeAttempt
        fields = [
            'id', 'user', 'user_username', 'challenge', 'challenge_title',
            'attempt_number', 'status', 'started_at', 'completed_at',
            'time_taken_seconds', 'score', 'feedback', 'user_answer',
            'attempts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'attempt_number', 'created_at', 'updated_at']


class UserChallengeAttemptCreateSerializer(serializers.Serializer):
    """Serializer for creating challenge attempts"""
    
    challenge_id = serializers.UUIDField()
    
    def create(self, validated_data):
        user = self.context['request'].user
        challenge_id = validated_data['challenge_id']
        
        try:
            challenge = AdaptiveChallenge.objects.get(id=challenge_id)
        except AdaptiveChallenge.DoesNotExist:
            raise serializers.ValidationError("Challenge not found.")
        
        # Get or create user attempt
        attempt, created = UserChallengeAttempt.objects.get_or_create(
            user=user,
            challenge=challenge,
            defaults={
                'status': 'in_progress',
                'started_at': timezone.now()
            }
        )
        
        return attempt


class UserChallengeAttemptSubmitSerializer(serializers.Serializer):
    """Serializer for submitting challenge attempts"""
    
    attempt_id = serializers.UUIDField()
    user_answer = serializers.JSONField()
    
    def validate_user_answer(self, value):
        """Validate user answer format"""
        if not isinstance(value, (dict, list, str, int, float)):
            raise serializers.ValidationError("User answer must be in JSON format.")
        return value
    
    def update(self, instance, validated_data):
        user_answer = validated_data['user_answer']
        
        instance.user_answer = user_answer
        instance.completed_at = timezone.now()
        
        # Calculate score
        if instance.challenge.correct_answer == user_answer:
            instance.score = 100.0
            instance.status = 'completed'
        else:
            instance.score = 0.0
            instance.status = 'completed'
        
        instance.feedback = {
            'correct_answer': instance.challenge.correct_answer,
            'explanation': instance.challenge.explanation,
            'score': instance.score
        }
        
        instance.save()
        return instance


class ChallengeSubmissionResponseSerializer(serializers.Serializer):
    """Serializer for challenge submission response"""
    
    score = serializers.FloatField()
    is_correct = serializers.BooleanField()
    feedback = serializers.JSONField()
    next_challenge_suggested = serializers.BooleanField()
    difficulty_adjustment = serializers.JSONField(allow_null=True)


class SpacedRepetitionSessionSerializer(serializers.ModelSerializer):
    """Serializer for spaced repetition sessions"""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)
    
    class Meta:
        model = SpacedRepetitionSession
        fields = [
            'id', 'user', 'user_username', 'challenge', 'challenge_title',
            'scheduled_for', 'review_stage', 'interval_days', 'ease_factor',
            'quality_rating', 'completed_at', 'status', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SpacedRepetitionReviewSerializer(serializers.Serializer):
    """Serializer for spaced repetition review"""
    
    session_id = serializers.UUIDField()
    quality_rating = serializers.IntegerField(min_value=0, max_value=5)
    
    def validate_quality_rating(self, value):
        """Validate quality rating for SM-2 algorithm"""
        if value < 0 or value > 5:
            raise serializers.ValidationError("Quality rating must be between 0 and 5.")
        return value


class ChallengeGenerationRequestSerializer(serializers.Serializer):
    """Serializer for challenge generation requests"""
    
    module_id = serializers.UUIDField()
    challenge_type = serializers.ChoiceField(choices=['quiz', 'coding', 'debugging', 'scenario'])
    difficulty_preference = serializers.ChoiceField(
        choices=['adaptive', 'very_easy', 'easy', 'medium', 'hard', 'very_hard'],
        default='adaptive'
    )


class ChallengeGenerationResponseSerializer(serializers.Serializer):
    """Serializer for challenge generation response"""
    
    challenge_id = serializers.UUIDField()
    title = serializers.CharField()
    content = serializers.JSONField()
    estimated_time_minutes = serializers.IntegerField()
    difficulty_level = serializers.CharField()


class PerformanceAnalysisSerializer(serializers.Serializer):
    """Serializer for performance analysis data"""
    
    total_attempts = serializers.IntegerField()
    success_rate = serializers.FloatField()
    average_score = serializers.FloatField()
    average_time_minutes = serializers.FloatField()
    improvement_trend = serializers.CharField()
    strong_areas = serializers.ListField()
    weak_areas = serializers.ListField()
    recommendations = serializers.ListField()


class DifficultyAdjustmentSerializer(serializers.Serializer):
    """Serializer for difficulty adjustment requests"""
    
    user_id = serializers.UUIDField()
    module_id = serializers.UUIDField()
    recent_performance = serializers.JSONField()
    adjustment_type = serializers.ChoiceField(
        choices=['automatic', 'manual_increase', 'manual_decrease'],
        default='automatic'
    )


class DifficultyAdjustmentResponseSerializer(serializers.Serializer):
    """Serializer for difficulty adjustment response"""
    
    new_difficulty = serializers.CharField()
    adjustment_reason = serializers.CharField()
    confidence_score = serializers.FloatField()
    next_challenge_suggested = serializers.BooleanField()


class DueReviewSerializer(serializers.Serializer):
    """Serializer for due reviews"""
    
    session_id = serializers.UUIDField()
    challenge_title = serializers.CharField()
    content_preview = serializers.CharField()
    difficulty_level = serializers.CharField()
    interval_days = serializers.IntegerField()


class DueReviewsResponseSerializer(serializers.Serializer):
    """Serializer for due reviews response"""
    
    reviews_count = serializers.IntegerField()
    reviews = DueReviewSerializer(many=True)


class UserLearningSummarySerializer(serializers.Serializer):
    """Serializer for user learning summary"""
    
    current_streak = serializers.IntegerField()
    total_time_hours = serializers.FloatField()
    completed_modules = serializers.IntegerField()
    current_level = serializers.CharField()
    next_milestone = serializers.CharField()
    recent_achievements = serializers.ListField()
    weekly_progress = serializers.JSONField()


class ChallengeAnalyticsSerializer(serializers.Serializer):
    """Serializer for challenge analytics"""
    
    total_challenges_generated = serializers.IntegerField()
    average_difficulty_score = serializers.FloatField()
    success_rate_by_type = serializers.JSONField()
    ai_generation_stats = serializers.JSONField()
    user_engagement_metrics = serializers.JSONField()


class LearningProgressSerializer(serializers.Serializer):
    """Serializer for learning progress overview"""
    
    overall_progress = serializers.FloatField()
    current_level = serializers.CharField()
    skill_scores = serializers.JSONField()
    recent_activity = serializers.JSONField()
    upcoming_reviews = serializers.IntegerField()
    learning_velocity = serializers.FloatField()