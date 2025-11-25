"""
Learning Views for Django REST Framework

Views for code execution, learning paths, and progress tracking
"""

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Avg, Count, Sum
from datetime import datetime, timedelta
import json

from .models import (
    LearningPath, Module, Lesson, Assessment, AssessmentQuestion, AssessmentAttempt,
    UserLearningPath, UserModuleProgress, PathRating, LearningRecommendation,
    UserDifficultyProfile, AdaptiveChallenge, UserChallengeAttempt, SpacedRepetitionSession
)
from .serializers import (
    LearningPathSerializer, LearningPathCreateSerializer, ModuleSerializer, ModuleCreateSerializer,
    UserLearningPathSerializer, UserModuleProgressSerializer, PathRatingSerializer,
    LearningRecommendationSerializer,
    LearningProgressSerializer, LessonSerializer, LessonCreateSerializer,
    AssessmentSerializer, AssessmentCreateSerializer, AssessmentQuestionSerializer, AssessmentAttemptSerializer,
    UserDifficultyProfileSerializer, AdaptiveChallengeSerializer, AdaptiveChallengeDetailSerializer,
    UserChallengeAttemptSerializer, UserChallengeAttemptCreateSerializer, UserChallengeAttemptSubmitSerializer,
    SpacedRepetitionSessionSerializer, SpacedRepetitionReviewSerializer,
    ChallengeGenerationRequestSerializer, ChallengeGenerationResponseSerializer,
    PerformanceAnalysisSerializer, DifficultyAdjustmentSerializer, DifficultyAdjustmentResponseSerializer,
    DueReviewSerializer, DueReviewsResponseSerializer, UserLearningSummarySerializer,
    ChallengeAnalyticsSerializer
)

# Import our adaptive learning services
from .services.adaptive_challenge_service import AdaptiveChallengeService
from .services.difficulty_adjustment_service import DifficultyAdjustmentService


class LearningPathViewSet(viewsets.ModelViewSet):
    """ViewSet for learning paths"""
    
    queryset = LearningPath.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LearningPathCreateSerializer
        return LearningPathSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LearningPath.objects.all()
        return LearningPath.objects.filter(is_published=True)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll user in learning path"""
        learning_path = self.get_object()
        user = request.user
        
        user_path, created = UserLearningPath.objects.get_or_create(
            user=user,
            learning_path=learning_path
        )
        
        if created:
            user_path.start_path()
            return Response({
                'message': 'Successfully enrolled in learning path',
                'status': user_path.status
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Already enrolled in this learning path',
                'status': user_path.status
            }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get user progress in learning path"""
        learning_path = self.get_object()
        user = request.user
        
        try:
            user_path = UserLearningPath.objects.get(
                user=user,
                learning_path=learning_path
            )
            serializer = UserLearningPathSerializer(user_path)
            return Response(serializer.data)
        except UserLearningPath.DoesNotExist:
            return Response({
                'error': 'User not enrolled in this learning path'
            }, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        """Get all modules for a learning path"""
        learning_path = self.get_object()
        modules = learning_path.modules.filter(is_published=True).order_by('order')
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    """ViewSet for learning modules"""
    
    queryset = Module.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ModuleCreateSerializer
        return ModuleSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Module.objects.all()
        return Module.objects.filter(is_published=True)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a module"""
        module = self.get_object()
        user = request.user
        
        progress, created = UserModuleProgress.objects.get_or_create(
            user=user,
            module=module
        )
        
        progress.start_module()
        serializer = UserModuleProgressSerializer(progress)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a module"""
        module = self.get_object()
        user = request.user
        
        try:
            progress = UserModuleProgress.objects.get(user=user, module=module)
            progress.complete_module()
            serializer = UserModuleProgressSerializer(progress)
            return Response(serializer.data)
        except UserModuleProgress.DoesNotExist:
            return Response({
                'error': 'Module not started'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def test_cases(self, request, pk=None):
        """Get test cases for a module"""
        module = self.get_object()
        # Test cases functionality would be implemented here
        # For now, return empty list as TestCase model doesn't exist
        return Response([])




class LearningProgressAPIView(APIView):
    """API endpoint for learning progress overview"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get comprehensive learning progress for user"""
        user = request.user
        
        # Calculate statistics
        total_paths = UserLearningPath.objects.filter(user=user).count()
        completed_paths = UserLearningPath.objects.filter(
            user=user, status='completed'
        ).count()
        in_progress_paths = UserLearningPath.objects.filter(
            user=user, status='in_progress'
        ).count()
        
        total_modules = UserModuleProgress.objects.filter(user=user).count()
        completed_modules = UserModuleProgress.objects.filter(
            user=user, status='completed'
        ).count()
        
        # Calculate total study time (convert minutes to hours)
        total_time_minutes = UserModuleProgress.objects.filter(
            user=user
        ).aggregate(total_time=Sum('time_spent'))['total_time']
        total_study_time = (total_time_minutes.total_seconds() / 3600) if total_time_minutes else 0.0
        
        progress_data = {
            'total_paths': total_paths,
            'completed_paths': completed_paths,
            'in_progress_paths': in_progress_paths,
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'total_challenges': UserChallengeAttempt.objects.filter(user=user).count(),
            'successful_challenges': UserChallengeAttempt.objects.filter(
                user=user, status='completed'
            ).count(),
            'total_study_time': round(total_study_time, 2)
        }
        
        serializer = LearningProgressSerializer(progress_data)
        return Response(serializer.data)


class UserLearningPathViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user learning path progress (read-only)"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserLearningPathSerializer
    
    def get_queryset(self):
        return UserLearningPath.objects.filter(user=self.request.user)


class UserModuleProgressViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user module progress (read-only)"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserModuleProgressSerializer
    
    def get_queryset(self):
        return UserModuleProgress.objects.filter(user=self.request.user)


class PathRatingViewSet(viewsets.ModelViewSet):
    """ViewSet for path ratings"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PathRatingSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PathRating.objects.all()
        return PathRating.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LearningRecommendationViewSet(viewsets.ModelViewSet):
    """ViewSet for learning recommendations"""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LearningRecommendationSerializer
    
    def get_queryset(self):
        return LearningRecommendation.objects.filter(
            user=self.request.user,
            is_dismissed=False
        ).filter(
            expires_at__gt=timezone.now()
        )
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Dismiss a recommendation"""
        recommendation = self.get_object()
        recommendation.dismiss()
        return Response({'message': 'Recommendation dismissed'})
    
    @action(detail=True, methods=['post'])
    def mark_acted(self, request, pk=None):
        """Mark recommendation as acted upon"""
        recommendation = self.get_object()
        recommendation.mark_acted_upon()
        return Response({'message': 'Recommendation marked as acted upon'})


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet for lessons"""
    
    queryset = Lesson.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LessonCreateSerializer
        return LessonSerializer
    
    def get_queryset(self):
        return Lesson.objects.all().select_related('module', 'module__learning_path')


class AssessmentViewSet(viewsets.ModelViewSet):
    """ViewSet for assessments"""
    
    queryset = Assessment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssessmentCreateSerializer
        return AssessmentSerializer
    
    def get_queryset(self):
        return Assessment.objects.all().select_related('module', 'module__learning_path')






# ============================================================================
# ADAPTIVE LEARNING VIEWS
# ============================================================================

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio

from .models import (
    UserDifficultyProfile, AdaptiveChallenge, UserChallengeAttempt, 
    SpacedRepetitionSession
)
from .serializers import (
    UserDifficultyProfileSerializer, AdaptiveChallengeSerializer, 
    AdaptiveChallengeDetailSerializer, UserChallengeAttemptSerializer,
    UserChallengeAttemptCreateSerializer, UserChallengeAttemptSubmitSerializer,
    ChallengeSubmissionResponseSerializer, SpacedRepetitionSessionSerializer,
    SpacedRepetitionReviewSerializer, ChallengeGenerationRequestSerializer,
    ChallengeGenerationResponseSerializer, PerformanceAnalysisSerializer,
    DifficultyAdjustmentSerializer, DifficultyAdjustmentResponseSerializer,
    DueReviewsResponseSerializer, UserLearningSummarySerializer
)
from .services.adaptive_challenge_service import AdaptiveChallengeService
from .services.difficulty_adjustment_service import DifficultyAdjustmentService

User = get_user_model()


class AdaptiveChallengeViewSet(viewsets.ViewSet):
    """ViewSet for adaptive challenge generation and management"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.challenge_service = AdaptiveChallengeService()
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate a personalized challenge for the user"""
        serializer = ChallengeGenerationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # Run async challenge generation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.challenge_service.generate_personalized_challenge(
                    user_id=str(user.id),
                    challenge_type=serializer.validated_data.get('challenge_type'),
                    specific_topic=serializer.validated_data.get('specific_topic')
                )
            )
            
            response_serializer = ChallengeGenerationResponseSerializer(result)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED if result['success'] else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            loop.close()
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit responses to a challenge attempt"""
        challenge = get_object_or_404(AdaptiveChallenge, pk=pk)
        
        # Get the most recent attempt for this user and challenge
        attempt = get_object_or_404(
            UserChallengeAttempt, 
            challenge=challenge, 
            user=request.user,
            status__in=['started', 'in_progress']
        )
        
        serializer = UserChallengeAttemptSubmitSerializer(attempt, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        responses = serializer.validated_data.get('responses', {})
        feedback = serializer.validated_data.get('feedback', '')
        
        # Run async submission processing
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.challenge_service.submit_challenge_response(
                    attempt_id=str(attempt.id),
                    responses=responses,
                    feedback=feedback
                )
            )
            
            response_serializer = ChallengeSubmissionResponseSerializer(result)
            return Response(response_serializer.data)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            loop.close()
    
    @action(detail=False, methods=['get'])
    def my_attempts(self, request):
        """Get user's challenge attempts"""
        attempts = UserChallengeAttempt.objects.filter(
            user=request.user
        ).select_related('challenge').order_by('-started_at')
        
        serializer = UserChallengeAttemptSerializer(attempts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def due_reviews(self, request):
        """Get challenges due for spaced repetition review"""
        user = request.user
        
        # Run async due reviews fetching
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            reviews = loop.run_until_complete(
                self.challenge_service.get_due_reviews(str(user.id))
            )
            
            response_data = {'reviews': reviews}
            return Response(response_data)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            loop.close()


class UserDifficultyProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user difficulty profiles"""
    
    serializer_class = UserDifficultyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return UserDifficultyProfile.objects.filter(user=user)
    
    def get_object(self):
        user = self.request.user
        profile, created = UserDifficultyProfile.objects.get_or_create(
            user=user,
            defaults={
                'current_difficulty': 'beginner',
                'jac_knowledge_level': 1,
                'problem_solving_level': 1,
                'coding_skill_level': 1
            }
        )
        return profile
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get comprehensive performance analytics for difficulty adjustment"""
        user = request.user
        time_window = int(request.query_params.get('days', 30))
        
        difficulty_service = DifficultyAdjustmentService()
        analysis = difficulty_service.analyze_user_performance(str(user.id), time_window)
        
        serializer = PerformanceAnalysisSerializer(analysis)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def adjust_difficulty(self, request):
        """Adjust user difficulty level"""
        serializer = DifficultyAdjustmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        adjustment_type = serializer.validated_data['adjustment_type']
        
        difficulty_service = DifficultyAdjustmentService()
        result = difficulty_service.apply_difficulty_adjustment(str(user.id), adjustment_type)
        
        response_serializer = DifficultyAdjustmentResponseSerializer(result)
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get user difficulty adjustment history"""
        user = request.user
        
        difficulty_service = DifficultyAdjustmentService()
        history = difficulty_service.get_difficulty_history(str(user.id))
        
        return Response(history)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get comprehensive learning summary for user"""
        user = request.user
        
        # Get difficulty profile
        profile = self.get_object()
        profile_serializer = UserDifficultyProfileSerializer(profile)
        
        # Get recent attempts
        recent_attempts = UserChallengeAttempt.objects.filter(
            user=user
        ).select_related('challenge').order_by('-started_at')[:5]
        attempts_serializer = UserChallengeAttemptSerializer(recent_attempts, many=True)
        
        # Get due reviews
        due_reviews = SpacedRepetitionSession.objects.filter(
            user=user,
            status='ready',
            scheduled_for__lte=timezone.now()
        ).select_related('challenge')[:5]
        reviews_serializer = SpacedRepetitionSessionSerializer(due_reviews, many=True)
        
        # Get learning recommendations
        recommendations = LearningRecommendation.objects.filter(
            user=user,
            is_dismissed=False,
            expires_at__gt=timezone.now()
        ).order_by('-priority_score')[:5]
        recommendations_serializer = LearningRecommendationSerializer(recommendations, many=True)
        
        # Calculate performance summary
        performance_summary = {
            'total_attempts': UserChallengeAttempt.objects.filter(user=user).count(),
            'recent_accuracy': profile.recent_accuracy,
            'current_streak': profile.success_streak,
            'skill_levels': {
                'jac_knowledge': profile.jac_knowledge_level,
                'problem_solving': profile.problem_solving_level,
                'coding_skill': profile.coding_skill_level
            }
        }
        
        summary_data = {
            'user_username': user.username,
            'difficulty_profile': profile_serializer.data,
            'recent_attempts': attempts_serializer.data,
            'due_reviews': reviews_serializer.data,
            'performance_summary': performance_summary,
            'recommendations': recommendations_serializer.data
        }
        
        return Response(summary_data)


class SpacedRepetitionViewSet(viewsets.ViewSet):
    """ViewSet for spaced repetition management"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.challenge_service = AdaptiveChallengeService()
    
    @action(detail=True, methods=['post'])
    def complete_review(self, request, pk=None):
        """Complete a spaced repetition review session"""
        session = get_object_or_404(SpacedRepetitionSession, pk=pk, user=request.user)
        
        serializer = SpacedRepetitionReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        quality_rating = serializer.validated_data['quality_rating']
        
        # Run async review completion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                self.challenge_service.complete_review(str(session.id), quality_rating)
            )
            
            return Response(result)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            loop.close()
    
    @action(detail=False, methods=['get'])
    def due_sessions(self, request):
        """Get all due spaced repetition sessions for user"""
        user = request.user
        
        due_sessions = SpacedRepetitionSession.objects.filter(
            user=user,
            status='ready',
            scheduled_for__lte=timezone.now()
        ).select_related('challenge')
        
        serializer = SpacedRepetitionSessionSerializer(due_sessions, many=True)
        return Response({'sessions': serializer.data})
    
    @action(detail=False, methods=['get'])
    def upcoming_sessions(self, request):
        """Get upcoming spaced repetition sessions for user"""
        user = request.user
        
        upcoming_sessions = SpacedRepetitionSession.objects.filter(
            user=user,
            status='scheduled',
            scheduled_for__gt=timezone.now()
        ).select_related('challenge').order_by('scheduled_for')[:10]
        
        serializer = SpacedRepetitionSessionSerializer(upcoming_sessions, many=True)
        return Response({'sessions': serializer.data})


class PerformanceAnalyticsView(APIView):
    """API View for comprehensive performance analytics"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get performance analytics for user"""
        user = request.user
        time_window = int(request.query_params.get('days', 30))
        
        difficulty_service = DifficultyAdjustmentService()
        analysis = difficulty_service.analyze_user_performance(str(user.id), time_window)
        
        return Response(analysis)
    
    def post(self, request):
        """Get analytics for multiple users (admin only)"""
        if not request.user.is_staff:
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        user_ids = request.data.get('user_ids', [])
        time_window = int(request.data.get('days', 30))
        
        difficulty_service = DifficultyAdjustmentService()
        
        results = {}
        for user_id in user_ids:
            try:
                analysis = difficulty_service.analyze_user_performance(user_id, time_window)
                results[user_id] = analysis
            except Exception as e:
                results[user_id] = {'success': False, 'error': str(e)}
        
        return Response({'analyses': results})


class ChallengeRecommendationsView(APIView):
    """API View for challenge recommendations"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get personalized challenge recommendations for user"""
        user = request.user
        
        # Get user's difficulty profile
        profile = get_object_or_404(UserDifficultyProfile, user=user)
        
        # Get recent attempts to understand performance
        recent_attempts = UserChallengeAttempt.objects.filter(
            user=user
        ).order_by('-started_at')[:10]
        
        # Get due reviews
        due_reviews = SpacedRepetitionSession.objects.filter(
            user=user,
            status='ready',
            scheduled_for__lte=timezone.now()
        ).select_related('challenge')
        
        # Generate recommendations based on performance
        recommendations = []
        
        # If user has low recent accuracy, recommend easier challenges
        if profile.recent_accuracy < 0.6:
            recommendations.append({
                'type': 'difficulty_adjustment',
                'message': 'Consider reviewing fundamentals with easier challenges',
                'priority': 'high'
            })
        
        # If user has high accuracy and streak, recommend harder challenges
        elif profile.recent_accuracy > 0.8 and profile.success_streak >= 3:
            recommendations.append({
                'type': 'difficulty_increase',
                'message': 'You\'re performing well! Ready for more challenging content.',
                'priority': 'medium'
            })
        
        # Check for due reviews
        if due_reviews.exists():
            recommendations.append({
                'type': 'spaced_repetition',
                'message': f'You have {due_reviews.count()} challenges ready for review',
                'priority': 'high'
            })
        
        return Response({
            'recommendations': recommendations,
            'user_profile': {
                'current_difficulty': profile.current_difficulty,
                'recent_accuracy': profile.recent_accuracy,
                'success_streak': profile.success_streak
            },
            'due_reviews_count': due_reviews.count(),
            'recent_attempts_count': recent_attempts.count()
        })