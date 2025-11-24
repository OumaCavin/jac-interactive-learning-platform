"""
Assessment views for Django REST Framework
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Avg, Count, Q, F, Max, Min
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.shortcuts import get_object_or_404
import uuid

from .models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult
from .serializers import (
    AssessmentAttemptSerializer, AssessmentAttemptCreateSerializer,
    AssessmentAttemptSubmitSerializer, AssessmentQuestionSerializer,
    AssessmentQuestionListSerializer, UserAssessmentResultSerializer,
    AssessmentStatsSerializer, AssessmentQuestionSubmissionSerializer
)
from apps.learning.models import Module


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assessment questions
    """
    queryset = AssessmentQuestion.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AssessmentQuestionListSerializer
        return AssessmentQuestionSerializer
    
    def get_queryset(self):
        """Filter questions based on user permissions and parameters"""
        queryset = AssessmentQuestion.objects.select_related('module')
        
        # Filter by module if provided
        module_id = self.request.query_params.get('module_id')
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by question type
        question_type = self.request.query_params.get('question_type')
        if question_type:
            queryset = queryset.filter(question_type=question_type)
        
        # Filter by active status (default to active only)
        active_only = self.request.query_params.get('active_only', 'true').lower()
        if active_only == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('module', 'difficulty', 'created_at')
    
    @action(detail=False, methods=['get'])
    def by_module(self, request):
        """Get questions grouped by module"""
        module_id = request.query_params.get('module_id')
        if not module_id:
            return Response(
                {'error': 'module_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        questions = self.get_queryset().filter(module_id=module_id)
        serializer = self.get_serializer(questions, many=True)
        
        return Response({
            'module_id': module_id,
            'questions': serializer.data,
            'count': questions.count()
        })
    
    @action(detail=True, methods=['post'])
    def check_answer(self, request, pk=None):
        """Check if an answer is correct for a specific question"""
        question = self.get_object()
        serializer = AssessmentQuestionSubmissionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_answer = serializer.validated_data['answer']
        is_correct = self._check_answer_correctness(question, user_answer)
        
        return Response({
            'question_id': question.question_id,
            'is_correct': is_correct,
            'correct_answer': question.correct_answer,
            'explanation': question.explanation,
            'points_earned': question.points if is_correct else 0
        })
    
    def _check_answer_correctness(self, question, user_answer):
        """Check if user answer is correct based on question type"""
        if question.question_type == 'multiple_choice':
            return user_answer == question.correct_answer
        elif question.question_type == 'true_false':
            return user_answer.lower() == question.correct_answer.lower()
        elif question.question_type in ['short_answer', 'essay']:
            # For text answers, do basic case-insensitive comparison
            # In a real implementation, you might want more sophisticated checking
            return user_answer.strip().lower() == question.correct_answer.strip().lower()
        else:
            return False


class AssessmentAttemptViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assessment attempts
    """
    queryset = AssessmentAttempt.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssessmentAttemptCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AssessmentAttemptSubmitSerializer
        return AssessmentAttemptSerializer
    
    def get_queryset(self):
        """Filter attempts based on user permissions"""
        user = self.request.user
        
        # Users can only see their own attempts unless they're staff
        if user.is_staff:
            return AssessmentAttempt.objects.select_related('user', 'module').all()
        else:
            return AssessmentAttempt.objects.select_related('user', 'module').filter(user=user)
    
    def perform_create(self, serializer):
        """Create new assessment attempt"""
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit assessment attempt with answers"""
        attempt = self.get_object()
        serializer = AssessmentAttemptSubmitSerializer(attempt, data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Update attempt with submitted answers
        answers = serializer.validated_data['answers']
        
        # Calculate score
        score_data = self._calculate_score(attempt, answers)
        
        # Update attempt
        attempt.answers = answers
        attempt.score = score_data['score']
        attempt.feedback = score_data['feedback']
        attempt.status = 'completed'
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Update or create user result record
        self._update_user_result(attempt)
        
        # Return updated attempt
        response_serializer = AssessmentAttemptSerializer(attempt)
        return Response(response_serializer.data)
    
    @action(detail=True, methods=['post'])
    def abandon(self, request, pk=None):
        """Mark attempt as abandoned"""
        attempt = self.get_object()
        
        if attempt.status != 'in_progress':
            return Response(
                {'error': 'Only in-progress attempts can be abandoned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attempt.status = 'abandoned'
        attempt.completed_at = timezone.now()
        attempt.save()
        
        serializer = AssessmentAttemptSerializer(attempt)
        return Response(serializer.data)
    
    def _calculate_score(self, attempt, answers):
        """Calculate score and generate feedback for attempt"""
        questions = AssessmentQuestion.objects.filter(
            module=attempt.module,
            is_active=True
        )
        
        total_possible_points = sum(q.points for q in questions)
        earned_points = 0
        feedback = {}
        
        for question in questions:
            question_id = str(question.question_id)
            user_answer = answers.get(question_id, '')
            
            if user_answer:
                is_correct = self._check_answer_correctness(question, user_answer)
                points_earned = question.points if is_correct else 0
                earned_points += points_earned
                
                feedback[question_id] = {
                    'is_correct': is_correct,
                    'points_earned': points_earned,
                    'user_answer': user_answer,
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation
                }
            else:
                feedback[question_id] = {
                    'is_correct': False,
                    'points_earned': 0,
                    'user_answer': '',
                    'correct_answer': question.correct_answer,
                    'explanation': question.explanation
                }
        
        # Calculate percentage score
        if total_possible_points > 0:
            score_percentage = (earned_points / total_possible_points) * 100
        else:
            score_percentage = 0
        
        return {
            'score': round(score_percentage, 2),
            'feedback': feedback,
            'earned_points': earned_points,
            'total_possible_points': total_possible_points
        }
    
    def _check_answer_correctness(self, question, user_answer):
        """Check if user answer is correct"""
        if question.question_type == 'multiple_choice':
            return user_answer == question.correct_answer
        elif question.question_type == 'true_false':
            return user_answer.lower() == question.correct_answer.lower()
        elif question.question_type in ['short_answer', 'essay']:
            return user_answer.strip().lower() == question.correct_answer.strip().lower()
        else:
            return False
    
    def _update_user_result(self, attempt):
        """Update or create user assessment result"""
        result_type = 'module_completion'
        
        # Calculate aggregated statistics
        user_attempts = AssessmentAttempt.objects.filter(
            user=attempt.user,
            module=attempt.module,
            status='completed'
        )
        
        if user_attempts.exists():
            stats = user_attempts.aggregate(
                total_attempts=Count('attempt_id'),
                best_score=Max('score'),
                average_score=Avg('score'),
                avg_duration=Avg(
                    (F('completed_at') - F('started_at')).total_seconds() / 60
                )
            )
            
            # Create or update result record
            UserAssessmentResult.objects.update_or_create(
                user=attempt.user,
                module=attempt.module,
                result_type=result_type,
                defaults={
                    'total_attempts': stats['total_attempts'],
                    'best_score': stats['best_score'],
                    'average_score': stats['average_score'],
                    'average_time_minutes': stats['avg_duration'],
                }
            )


class AssessmentStatsAPIView(viewsets.ViewSet):
    """
    API View for assessment statistics
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get assessment statistics"""
        module_id = request.query_params.get('module_id')
        
        if module_id:
            # Get statistics for specific module
            stats = self._get_module_stats(module_id)
            serializer = AssessmentStatsSerializer(stats)
            return Response(serializer.data)
        else:
            # Get overall statistics
            stats = self._get_overall_stats()
            return Response(stats)
    
    def _get_module_stats(self, module_id):
        """Get statistics for a specific module"""
        try:
            module = Module.objects.get(module_id=uuid.UUID(module_id))
        except (Module.DoesNotExist, ValueError):
            return Response(
                {'error': 'Module not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        attempts = AssessmentAttempt.objects.filter(module=module)
        questions = AssessmentQuestion.objects.filter(module=module, is_active=True)
        
        completed_attempts = attempts.filter(status='completed')
        
        stats = {
            'module_id': module_id,
            'module_title': module.title,
            'total_attempts': attempts.count(),
            'completed_attempts': completed_attempts.count(),
            'average_score': completed_attempts.aggregate(
                avg_score=Avg('score')
            )['avg_score'] or 0,
            'pass_rate': self._calculate_pass_rate(completed_attempts),
            'average_duration': completed_attempts.aggregate(
                avg_duration=Avg(
                    (F('completed_at') - F('started_at')).total_seconds() / 60
                )
            )['avg_duration'] or 0,
            'fastest_attempt': self._get_fastest_attempt(completed_attempts),
            'slowest_attempt': self._get_slowest_attempt(completed_attempts),
            'total_questions': questions.count(),
            'questions_attempted': len(self._get_attempted_questions(attempts)),
            'unique_users': attempts.values('user').distinct().count(),
            'returning_users': self._calculate_returning_users(attempts)
        }
        
        return stats
    
    def _get_overall_stats(self):
        """Get overall assessment statistics"""
        all_attempts = AssessmentAttempt.objects.all()
        completed_attempts = all_attempts.filter(status='completed')
        
        return {
            'total_attempts': all_attempts.count(),
            'completed_attempts': completed_attempts.count(),
            'active_modules': Module.objects.filter(
                assessment_attempts__isnull=False
            ).distinct().count(),
            'total_questions': AssessmentQuestion.objects.filter(is_active=True).count(),
            'average_score': completed_attempts.aggregate(
                avg_score=Avg('score')
            )['avg_score'] or 0,
            'unique_users': all_attempts.values('user').distinct().count()
        }
    
    def _calculate_pass_rate(self, completed_attempts):
        """Calculate pass rate for completed attempts"""
        if not completed_attempts.exists():
            return 0
        
        passed_attempts = completed_attempts.filter(
            score__gte=F('passing_score')
        )
        
        return (passed_attempts.count() / completed_attempts.count()) * 100
    
    def _get_fastest_attempt(self, completed_attempts):
        """Get fastest attempt duration in minutes"""
        if not completed_attempts.exists():
            return 0
        
        fastest = completed_attempts.annotate(
            duration_minutes=(
                (F('completed_at') - F('started_at')).total_seconds() / 60
            )
        ).aggregate(min_duration=Min('duration_minutes'))['min_duration']
        
        return fastest or 0
    
    def _get_slowest_attempt(self, completed_attempts):
        """Get slowest attempt duration in minutes"""
        if not completed_attempts.exists():
            return 0
        
        slowest = completed_attempts.annotate(
            duration_minutes=(
                (F('completed_at') - F('started_at')).total_seconds() / 60
            )
        ).aggregate(max_duration=Max('duration_minutes'))['max_duration']
        
        return slowest or 0
    
    def _get_attempted_questions(self, attempts):
        """Get list of question IDs that have been attempted"""
        attempted_questions = set()
        
        for attempt in attempts:
            if attempt.answers:
                attempted_questions.update(attempt.answers.keys())
        
        return list(attempted_questions)
    
    def _calculate_returning_users(self, attempts):
        """Calculate number of users with multiple attempts"""
        user_attempt_counts = attempts.values('user').annotate(
            attempt_count=Count('attempt_id')
        ).filter(attempt_count__gt=1)
        
        return user_attempt_counts.count()