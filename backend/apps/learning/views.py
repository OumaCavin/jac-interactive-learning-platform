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
    LearningPath, Module, Lesson, Assessment, Question, UserLearningPath, UserModuleProgress,
    PathRating, LearningRecommendation, CodeSubmission, TestCase,
    CodeExecutionLog, AICodeReview
)
from .serializers import (
    LearningPathSerializer, LearningPathCreateSerializer, ModuleSerializer, ModuleCreateSerializer,
    UserLearningPathSerializer, UserModuleProgressSerializer, PathRatingSerializer,
    LearningRecommendationSerializer, CodeSubmissionSerializer, CodeSubmissionCreateSerializer,
    CodeSubmissionReviewSerializer, TestCaseSerializer, CodeExecutionLogSerializer,
    AICodeReviewSerializer, CodeExecutionRequestSerializer, CodeExecutionResponseSerializer,
    LearningProgressSerializer, LessonSerializer, LessonCreateSerializer,
    AssessmentSerializer, AssessmentCreateSerializer, QuestionSerializer, QuestionCreateSerializer
)

# Import our JAC code execution engine
from .jac_code_executor import code_executor, CodeEvaluatorAgent


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
        test_cases = module.test_cases.all()
        serializer = TestCaseSerializer(test_cases, many=True)
        return Response(serializer.data)


class CodeSubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for code submissions"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CodeSubmissionCreateSerializer
        return CodeSubmissionSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CodeSubmission.objects.all()
        return CodeSubmission.objects.filter(user=user)
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """Execute code submission"""
        submission = self.get_object()
        
        if submission.status != 'pending':
            return Response({
                'error': 'Code already executed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update status to processing
        submission.status = 'processing'
        submission.save()
        
        try:
            # Execute code using our JAC code execution engine
            evaluator = CodeEvaluatorAgent(agent_id='evaluator-agent')
            result = evaluator.evaluate_code_submission(
                code=submission.code,
                language=submission.language,
                user_id=request.user.id,
                task_id=submission.submission_id
            )
            
            # Update submission with results
            submission.status = 'passed' if result['success'] else 'failed'
            submission.execution_result = {
                'output': result.get('output', ''),
                'error': result.get('error', ''),
                'status': result.get('status', 'error')
            }
            submission.execution_time = result.get('execution_time', 0.0)
            submission.ai_feedback = json.dumps(result.get('recommendations', []))
            submission.score = result.get('performance_metrics', {}).get('code_complexity', 0)
            submission.reviewed_at = timezone.now()
            submission.reviewer_agent_id = 'evaluator-agent'
            submission.save()
            
            serializer = CodeSubmissionSerializer(submission)
            return Response(serializer.data)
            
        except Exception as e:
            submission.status = 'error'
            submission.execution_result = {'error': str(e)}
            submission.reviewed_at = timezone.now()
            submission.save()
            
            return Response({
                'error': f'Execution failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Manually review code submission"""
        submission = self.get_object()
        serializer = CodeSubmissionReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update submission
            for attr, value in serializer.validated_data.items():
                setattr(submission, attr, value)
            
            submission.reviewed_at = timezone.now()
            submission.save()
            
            result_serializer = CodeSubmissionSerializer(submission)
            return Response(result_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def execution_logs(self, request, pk=None):
        """Get execution logs for submission"""
        submission = self.get_object()
        logs = submission.execution_logs.all()
        serializer = CodeExecutionLogSerializer(logs, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ai_reviews(self, request, pk=None):
        """Get AI reviews for submission"""
        submission = self.get_object()
        reviews = submission.ai_reviews.all()
        serializer = AICodeReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CodeExecutionAPIView(APIView):
    """API endpoint for direct code execution"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Execute code directly without submission"""
        serializer = CodeExecutionRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Execute code using our engine
            request_data = serializer.validated_data
            result = code_executor.execute_code(
                code=request_data['code'],
                language=request_data['language'],
                user_id=request.user.id,
                task_id=request_data.get('task_id')
            )
            
            # Format response
            response_data = {
                'execution_id': result.execution_id,
                'status': result.status,
                'success': result.status == 'success',
                'output': result.output,
                'error': result.error,
                'execution_time': result.execution_time,
                'timestamp': result.created_at.isoformat(),
                'code_analysis': {},  # Could be enhanced
                'security_assessment': {},  # Could be enhanced
                'performance_metrics': {
                    'execution_time': result.execution_time,
                    'memory_usage': result.memory_usage
                },
                'recommendations': []  # Could be enhanced
            }
            
            return Response(response_data)
            
        except Exception as e:
            return Response({
                'error': f'Execution failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        
        total_submissions = CodeSubmission.objects.filter(user=user).count()
        successful_submissions = CodeSubmission.objects.filter(
            user=user, status='passed'
        ).count()
        
        # Calculate average score
        avg_score = CodeSubmission.objects.filter(
            user=user, score__isnull=False
        ).aggregate(avg_score=Avg('score'))['avg_score'] or 0.0
        
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
            'total_code_submissions': total_submissions,
            'successful_submissions': successful_submissions,
            'average_score': round(avg_score, 2),
            'total_study_time': round(total_study_time, 2)
        }
        
        serializer = LearningProgressSerializer(progress_data)
        return Response(serializer.data)


class TestCaseViewSet(viewsets.ModelViewSet):
    """ViewSet for test cases"""
    
    queryset = TestCase.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestCaseSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return TestCase.objects.all()
        return TestCase.objects.filter(module__is_published=True)


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


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for questions"""
    
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        return QuestionSerializer
    
    def get_queryset(self):
        return Question.objects.all().select_related('assessment', 'assessment__module')


# ============================================================================
# ASSESSMENT API VIEWS
# ============================================================================

from .models import AssessmentAttempt, UserAssessmentResult
from .serializers import (
    QuizListSerializer, QuizDetailSerializer, AttemptListSerializer, AttemptDetailSerializer,
    StartAttemptSerializer, SubmitAttemptSerializer, AssessmentStatsSerializer
)


class QuizAPIView(APIView):
    """
    API view for quiz management
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get list of available quizzes
        GET /api/assessment/quizzes/
        """
        # Filter published assessments
        quizzes = Assessment.objects.filter(is_published=True)
        
        # Apply filters
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            quizzes = quizzes.filter(difficulty_level=difficulty)
        
        learning_path = request.query_params.get('learning_path')
        if learning_path:
            quizzes = quizzes.filter(module__learning_path_id=learning_path)
        
        module = request.query_params.get('module')
        if module:
            quizzes = quizzes.filter(module_id=module)
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        quizzes = quizzes[offset:offset + limit]
        
        serializer = QuizListSerializer(quizzes, many=True)
        
        return Response({
            'quizzes': serializer.data,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(serializer.data)
            }
        })


class QuizDetailAPIView(APIView):
    """
    API view for quiz details
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, quiz_id):
        """
        Get detailed quiz information
        GET /api/assessment/quizzes/{id}/
        """
        try:
            quiz = Assessment.objects.get(id=quiz_id, is_published=True)
        except Assessment.DoesNotExist:
            return Response(
                {'error': 'Quiz not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = QuizDetailSerializer(quiz)
        return Response(serializer.data)


class AttemptAPIView(APIView):
    """
    API view for assessment attempts
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get user's assessment attempts
        GET /api/assessment/attempts/
        """
        user = request.user
        
        # Apply filters
        assessment_id = request.query_params.get('assessment')
        if assessment_id:
            attempts = AssessmentAttempt.objects.filter(user=user, assessment_id=assessment_id)
        else:
            attempts = AssessmentAttempt.objects.filter(user=user)
        
        # Order by most recent
        attempts = attempts.order_by('-started_at')
        
        # Pagination
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        attempts = attempts[offset:offset + limit]
        
        serializer = AttemptListSerializer(attempts, many=True)
        
        return Response({
            'attempts': serializer.data,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'count': len(serializer.data)
            }
        })


class StartAttemptAPIView(APIView):
    """
    API view for starting a new assessment attempt
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, quiz_id):
        """
        Start a new attempt for a quiz
        POST /api/assessment/quizzes/{id}/start/
        """
        try:
            quiz = Assessment.objects.get(id=quiz_id, is_published=True)
        except Assessment.DoesNotExist:
            return Response(
                {'error': 'Quiz not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = StartAttemptSerializer(
            data=request.data,
            context={'request': request, 'assessment': quiz}
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        attempt = serializer.save()
        response_serializer = AttemptDetailSerializer(attempt)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class SubmitAttemptAPIView(APIView):
    """
    API view for submitting an assessment attempt
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, attempt_id):
        """
        Submit an assessment attempt
        POST /api/assessment/attempts/{id}/submit/
        """
        try:
            attempt = AssessmentAttempt.objects.get(
                id=attempt_id,
                user=request.user,
                status='in_progress'
            )
        except AssessmentAttempt.DoesNotExist:
            return Response(
                {'error': 'Attempt not found or not in progress'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = SubmitAttemptSerializer(
            data=request.data,
            instance=attempt
        )
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        attempt = serializer.save()
        response_serializer = AttemptDetailSerializer(attempt)
        
        return Response(response_serializer.data)


class AttemptDetailAPIView(APIView):
    """
    API view for detailed attempt information
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, attempt_id):
        """
        Get detailed information about a specific attempt
        GET /api/assessment/attempts/{id}/
        """
        try:
            attempt = AssessmentAttempt.objects.get(
                id=attempt_id,
                user=request.user
            )
        except AssessmentAttempt.DoesNotExist:
            return Response(
                {'error': 'Attempt not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AttemptDetailSerializer(attempt)
        return Response(serializer.data)


class AssessmentStatsAPIView(APIView):
    """
    API view for assessment statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get user's assessment statistics
        GET /api/assessment/stats/
        """
        user = request.user
        
        # Calculate statistics
        total_assessments = Assessment.objects.filter(is_published=True).count()
        user_attempts = AssessmentAttempt.objects.filter(user=user)
        completed_attempts = user_attempts.filter(status='completed')
        
        total_attempts = user_attempts.count()
        passed_attempts = completed_attempts.filter(is_passed=True).count()
        pass_rate = (passed_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        # Average score
        avg_score = completed_attempts.aggregate(
            avg_score=models.Avg('score')
        )['avg_score'] or 0
        
        # Best score
        best_score = completed_attempts.aggregate(
            best_score=models.Max('score')
        )['best_score'] or 0
        
        # Total time spent
        total_time_spent = completed_attempts.aggregate(
            total_time=models.Sum('time_spent')
        )['total_time'] or timezone.timedelta()
        
        # Recent attempts
        recent_attempts = completed_attempts.order_by('-started_at')[:5]
        
        stats_data = {
            'total_assessments': total_assessments,
            'completed_assessments': completed_attempts.values('assessment').distinct().count(),
            'average_score': round(avg_score, 2),
            'total_attempts': total_attempts,
            'passed_attempts': passed_attempts,
            'pass_rate': round(pass_rate, 2),
            'total_time_spent': total_time_spent,
            'best_score': round(best_score, 2),
            'recent_attempts': AttemptListSerializer(recent_attempts, many=True).data
        }
        
        return Response(stats_data)