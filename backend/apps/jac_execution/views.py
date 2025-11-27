# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
API Views for JAC Code Execution

This module provides Django REST Framework views for code execution,
templates, sessions, and security settings.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone
import time

from .models import CodeExecution, ExecutionTemplate, CodeExecutionSession, SecuritySettings
from .serializers import (
    CodeExecutionCreateSerializer, CodeExecutionResultSerializer,
    CodeExecutionStatusSerializer, ExecutionTemplateListSerializer,
    ExecutionTemplateDetailSerializer, ExecutionTemplateCreateSerializer,
    CodeExecutionSessionSerializer, SecuritySettingsSerializer,
    QuickExecutionSerializer, ExecutionHistorySerializer
)
from .services.executor import ExecutionService, CodeExecutionError, SecurityViolationError


class CodeExecutionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing code execution requests and results.
    """
    serializer_class = CodeExecutionResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get executions for the current user."""
        return CodeExecution.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return CodeExecutionCreateSerializer
        elif self.action == 'status':
            return CodeExecutionStatusSerializer
        elif self.action == 'history':
            return ExecutionHistorySerializer
        return CodeExecutionResultSerializer
    
    @action(detail=False, methods=['post'])
    def execute(self, request):
        """
        Execute code and return results.
        """
        serializer = CodeExecutionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate data
        language = serializer.validated_data['language']
        code = serializer.validated_data['code']
        stdin = serializer.validated_data.get('stdin', '')
        
        try:
            # Execute code
            execution_service = ExecutionService()
            result = execution_service.execute_with_tracking(
                user=request.user,
                language=language,
                code=code,
                stdin=stdin,
                save_result=True
            )
            
            # Get the created execution record
            execution = CodeExecution.objects.filter(
                user=request.user,
                language=language,
                code=code
            ).order_by('-created_at').first()
            
            # Serialize result
            result_serializer = CodeExecutionResultSerializer(execution)
            
            return Response({
                'success': True,
                'execution': result_serializer.data,
                'output': {
                    'stdout': result.get('stdout', ''),
                    'stderr': result.get('stderr', ''),
                    'return_code': result.get('return_code', 1),
                    'execution_time': result.get('execution_time', 0)
                }
            })
            
        except CodeExecutionError as e:
            return Response({
                'success': False,
                'error': str(e),
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except SecurityViolationError as e:
            return Response({
                'success': False,
                'error': f'Security violation: {str(e)}',
                'status': 'security_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}',
                'status': 'server_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def quick_execute(self, request):
        """
        Execute code without saving to database.
        """
        serializer = QuickExecutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        language = serializer.validated_data['language']
        code = serializer.validated_data['code']
        stdin = serializer.validated_data.get('stdin', '')
        
        try:
            execution_service = ExecutionService()
            result = execution_service.execute_with_tracking(
                user=request.user,
                language=language,
                code=code,
                stdin=stdin,
                save_result=False
            )
            
            return Response({
                'success': True,
                'output': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Get execution status and results.
        """
        try:
            execution = self.get_object()
            serializer = CodeExecutionStatusSerializer(execution)
            return Response(serializer.data)
        except CodeExecution.DoesNotExist:
            return Response(
                {'error': 'Execution not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get execution history with pagination.
        """
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        language = request.GET.get('language')
        status_filter = request.GET.get('status')
        
        queryset = self.get_queryset()
        
        # Apply filters
        if language:
            queryset = queryset.filter(language=language)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Paginate results
        paginator = Paginator(queryset, per_page)
        executions = paginator.get_page(page)
        
        serializer = ExecutionHistorySerializer(executions, many=True)
        
        return Response({
            'results': serializer.data,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': executions.has_next(),
                'has_previous': executions.has_previous()
            }
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get execution statistics for the user.
        """
        try:
            execution_service = ExecutionService()
            stats = execution_service.get_user_statistics(request.user)
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': f'Failed to get statistics: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['delete'])
    def clear_history(self, request):
        """
        Clear user's execution history.
        """
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        deleted_count, _ = CodeExecution.objects.filter(user=request.user).delete()
        
        return Response({
            'success': True,
            'deleted_count': deleted_count
        })


class ExecutionTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing execution templates.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get templates accessible to the user."""
        user = self.request.user
        return ExecutionTemplate.objects.filter(
            Q(is_public=True) | Q(created_by=user)
        ).order_by('-updated_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ExecutionTemplateCreateSerializer
        elif self.action in ['retrieve', 'list']:
            return ExecutionTemplateDetailSerializer if self.action == 'retrieve' else ExecutionTemplateListSerializer
        return ExecutionTemplateDetailSerializer
    
    def perform_create(self, serializer):
        """Set the creator when creating a template."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """
        Execute a template directly.
        """
        try:
            template = self.get_object()
            
            # Check if user can access this template
            if not template.is_public and template.created_by != request.user:
                return Response(
                    {'error': 'Template not accessible'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Execute the template code
            execution_service = ExecutionService()
            result = execution_service.execute_with_tracking(
                user=request.user,
                language=template.language,
                code=template.code,
                stdin=template.stdin or '',
                save_result=True
            )
            
            return Response({
                'success': True,
                'template': ExecutionTemplateDetailSerializer(template).data,
                'output': result
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get templates grouped by category.
        """
        category = request.GET.get('category')
        language = request.GET.get('language')
        
        queryset = self.get_queryset()
        
        if category:
            queryset = queryset.filter(category=category)
        if language:
            queryset = queryset.filter(language=language)
        
        templates = queryset.order_by('name')
        serializer = ExecutionTemplateListSerializer(templates, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        Get popular templates (ordered by recent updates and public status).
        """
        templates = ExecutionTemplate.objects.filter(
            is_public=True,
            is_active=True
        ).order_by('-updated_at')[:20]
        
        serializer = ExecutionTemplateListSerializer(templates, many=True)
        return Response(serializer.data)


class QuickExecutionView(APIView):
    """
    View for quick code execution without database storage.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Execute code without saving results."""
        serializer = QuickExecutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        language = serializer.validated_data['language']
        code = serializer.validated_data['code']
        stdin = serializer.validated_data.get('stdin', '')
        
        try:
            execution_service = ExecutionService()
            result = execution_service.execute_with_tracking(
                user=request.user,
                language=language,
                code=code,
                stdin=stdin,
                save_result=False
            )
            
            return Response({
                'success': True,
                'output': result
            })
            
        except CodeExecutionError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except SecurityViolationError as e:
            return Response({
                'success': False,
                'error': f'Security violation: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CodeExecutionSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user execution session statistics.
    """
    serializer_class = CodeExecutionSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get sessions for the current user."""
        return CodeExecutionSession.objects.filter(
            user=self.request.user
        ).order_by('-started_at')


class SecuritySettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing security settings.
    Only admins can modify settings.
    """
    serializer_class = SecuritySettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Only return the single security settings instance."""
        if not SecuritySettings.objects.exists():
            SecuritySettings.objects.create()
        return SecuritySettings.objects.all()
    
    @action(detail=False, methods=['put', 'patch'])
    def update_settings(self, request):
        """
        Update security settings (admin only).
        """
        if not request.user.is_staff:
            return Response(
                {'error': 'Admin permissions required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings_obj, created = SecuritySettings.objects.get_or_create(pk=1)
        serializer = SecuritySettingsSerializer(settings_obj, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExecutionStatusView(APIView):
    """
    View for checking execution status by ID.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, execution_id):
        """Get execution status and results."""
        try:
            execution = CodeExecution.objects.get(
                id=execution_id,
                user=request.user
            )
            
            serializer = CodeExecutionResultSerializer(execution)
            return Response(serializer.data)
            
        except CodeExecution.DoesNotExist:
            return Response(
                {'error': 'Execution not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class LanguageSupportView(APIView):
    """
    View for getting supported languages and their capabilities.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """Get supported languages and execution capabilities."""
        try:
            settings_obj = SecuritySettings.objects.get(pk=1)
            allowed_languages = settings_obj.allowed_languages
        except SecuritySettings.DoesNotExist:
            allowed_languages = ['jac', 'python']
        
        language_info = {
            'python': {
                'name': 'Python',
                'version': '3.x',
                'extensions': ['.py'],
                'description': 'Python programming language',
                'features': ['print', 'input', 'math', 'string', 'list', 'dict', 'file I/O'],
                'restrictions': ['No system calls', 'No network access', 'Limited imports']
            },
            'jac': {
                'name': 'JAC',
                'version': 'Latest',
                'extensions': ['.jac'],
                'description': 'JAC programming language',
                'features': ['Variables', 'Functions', 'Control flow', 'Data structures'],
                'restrictions': ['No system access', 'Sandboxed execution']
            }
        }
        
        # Filter to only show allowed languages
        available_languages = {
            lang: info for lang, info in language_info.items()
            if lang in allowed_languages
        }
        
        return Response({
            'supported_languages': available_languages,
            'max_execution_time': getattr(SecuritySettings.objects.first(), 'max_execution_time', 5.0),
            'max_output_size': getattr(SecuritySettings.objects.first(), 'max_output_size', 10240)
        })


# =============================================================================
# Code Translation Views
# =============================================================================

class CodeTranslationViewSet(viewsets.ViewSet):
    """
    ViewSet for code translation operations between JAC and Python.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def translate(self, request):
        """
        Translate code from one language to another.
        """
        from .serializers.translation_serializers import CodeTranslationSerializer
        from .services.translator import CodeTranslator, TranslationDirection
        
        serializer = CodeTranslationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        source_code = serializer.validated_data['source_code']
        source_language = serializer.validated_data['source_language']
        target_language = serializer.validated_data['target_language']
        
        try:
            # Determine translation direction
            if source_language == 'jac' and target_language == 'python':
                direction = TranslationDirection.JAC_TO_PYTHON
            elif source_language == 'python' and target_language == 'jac':
                direction = TranslationDirection.PYTHON_TO_JAC
            else:
                return Response({
                    'error': 'Invalid language combination. Only JAC ↔ Python translation is supported.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform translation
            translator = CodeTranslator()
            result = translator.translate_code(source_code, direction)
            
            # Return result
            response_data = {
                'success': result.success,
                'translated_code': result.translated_code,
                'source_language': result.source_language,
                'target_language': result.target_language,
                'errors': result.errors,
                'warnings': result.warnings,
                'metadata': result.metadata
            }
            
            if result.success:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Translation failed: {str(e)}',
                'source_language': source_language,
                'target_language': target_language,
                'errors': [str(e)],
                'warnings': [],
                'metadata': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def quick_translate(self, request):
        """
        Quick translation without additional validation or metadata.
        """
        from .serializers.translation_serializers import QuickTranslationSerializer
        from .services.translator import CodeTranslator, TranslationDirection
        
        serializer = QuickTranslationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        code = serializer.validated_data['code']
        direction = serializer.validated_data['direction']
        
        try:
            # Determine translation direction
            if direction == 'jac_to_python':
                translation_direction = TranslationDirection.JAC_TO_PYTHON
                source_lang, target_lang = 'JAC', 'Python'
            elif direction == 'python_to_jac':
                translation_direction = TranslationDirection.PYTHON_TO_JAC
                source_lang, target_lang = 'Python', 'JAC'
            else:
                return Response({
                    'error': 'Invalid translation direction'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform translation
            translator = CodeTranslator()
            result = translator.translate_code(code, translation_direction)
            
            return Response({
                'success': result.success,
                'translated_code': result.translated_code,
                'source_language': source_lang,
                'target_language': target_lang,
                'errors': result.errors,
                'warnings': result.warnings
            }, status=status.HTTP_200_OK if result.success else status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Quick translation failed: {str(e)}',
                'translated_code': '',
                'errors': [str(e)],
                'warnings': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def supported_languages(self, request):
        """
        Get supported languages for translation.
        """
        return Response({
            'languages': {
                'jac': {
                    'name': 'JAC',
                    'description': 'JAC Programming Language',
                    'extensions': ['.jac'],
                    'can_translate_to': ['python']
                },
                'python': {
                    'name': 'Python',
                    'description': 'Python Programming Language',
                    'extensions': ['.py'],
                    'can_translate_to': ['jac']
                }
            },
            'translation_pairs': ['jac_to_python', 'python_to_jac'],
            'notes': [
                'Translation preserves functionality but may differ in syntax',
                'Generated code should be tested before use',
                'Some language-specific features may not translate perfectly'
            ]
        })


class QuickTranslationView(APIView):
    """
    Standalone view for quick translation operations.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Perform quick code translation between JAC and Python.
        """
        from .serializers.translation_serializers import QuickTranslationSerializer
        from .services.translator import CodeTranslator, TranslationDirection
        
        serializer = QuickTranslationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        code = serializer.validated_data['code']
        direction = serializer.validated_data['direction']
        
        try:
            # Determine translation direction
            if direction == 'jac_to_python':
                translation_direction = TranslationDirection.JAC_TO_PYTHON
                source_lang, target_lang = 'JAC', 'Python'
            elif direction == 'python_to_jac':
                translation_direction = TranslationDirection.PYTHON_TO_JAC
                source_lang, target_lang = 'Python', 'JAC'
            else:
                return Response({
                    'success': False,
                    'error': 'Invalid translation direction. Use "jac_to_python" or "python_to_jac"'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Perform translation
            translator = CodeTranslator()
            result = translator.translate_code(code, translation_direction)
            
            return Response({
                'success': result.success,
                'translated_code': result.translated_code,
                'source_language': source_lang,
                'target_language': target_lang,
                'errors': result.errors,
                'warnings': result.warnings,
                'metadata': {
                    'original_length': len(code),
                    'translated_length': len(result.translated_code),
                    'direction': direction
                }
            }, status=status.HTTP_200_OK if result.success else status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Translation failed: {str(e)}',
                'translated_code': '',
                'errors': [str(e)],
                'warnings': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# =============================================================================
# JAC-Specific Learning Views
# =============================================================================

# Import the JAC execution service
from .jac_executor import jac_executor


class JACLearningExecutionAPIView(APIView):
    """
    API View for JAC-specific code execution with learning feedback
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Execute JAC code with learning feedback
        POST /api/jac-learning/execute/
        """
        code = request.data.get('code', '')
        language = request.data.get('language', 'jac')
        
        if not code:
            return Response({
                'success': False,
                'error': 'Code is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Execute the code using JAC executor
            result = jac_executor.execute_code(code, language)
            
            return Response({
                'success': result['success'],
                'output': result.get('execution', {}).get('output', []),
                'error': result.get('execution', {}).get('error'),
                'execution_details': {
                    'variables': result.get('execution', {}).get('variables', {}),
                    'graph': result.get('execution', {}).get('graph', {}),
                    'walkers': result.get('execution', {}).get('walkers', {}),
                    'execution_time': result.get('execution', {}).get('execution_time', 0),
                    'memory_usage': result.get('execution', {}).get('memory_usage', 0)
                },
                'suggestions': result.get('suggestions', []),
                'learning_tips': result.get('learning_tips', []),
                'validation': result.get('validation', {}),
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e),
                'output': [],
                'execution_time': 0,
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JACLearningValidationAPIView(APIView):
    """
    API View for JAC code validation
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Validate JAC code syntax
        POST /api/jac-learning/validate/
        """
        code = request.data.get('code', '')
        language = request.data.get('language', 'jac')
        
        if not code:
            return Response({
                'is_valid': False,
                'errors': ['Code is required'],
                'warnings': [],
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate the code using JAC validator
            validation_result = jac_executor.validator.validate_code(code)
            
            return Response({
                'is_valid': validation_result['is_valid'],
                'errors': validation_result['errors'],
                'warnings': validation_result['warnings'],
                'syntax_highlights': validation_result.get('syntax_highlights', {}),
                'line_count': validation_result['line_count'],
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'is_valid': False,
                'errors': [f'Validation failed: {str(e)}'],
                'warnings': [],
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JACLearningSyntaxReferenceAPIView(APIView):
    """
    API View for JAC syntax reference
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get JAC syntax reference
        GET /api/jac-learning/syntax-reference/
        """
        try:
            syntax_reference = jac_executor.get_syntax_reference()
            
            return Response({
                'keywords': syntax_reference['keywords'],
                'operators': syntax_reference['operators'],
                'types': syntax_reference['types'],
                'examples': syntax_reference['examples'],
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to retrieve syntax reference: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JACLearningEvaluationAPIView(APIView):
    """
    API View for JAC code evaluation with AI feedback
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Evaluate JAC code with AI feedback
        POST /api/jac-learning/evaluate/
        """
        code = request.data.get('code', '')
        test_cases = request.data.get('test_cases', [])
        
        if not code:
            return Response({
                'error': 'Code is required',
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Execute the code first
            execution_result = jac_executor.execute_code(code)
            
            # Generate AI feedback based on code analysis
            feedback = self._generate_code_feedback(code, execution_result, test_cases)
            
            return Response({
                'execution_result': execution_result,
                'ai_feedback': feedback,
                'test_results': self._evaluate_test_cases(code, test_cases) if test_cases else [],
                'score': self._calculate_code_score(execution_result, feedback),
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'error': f'Code evaluation failed: {str(e)}',
                'execution_result': {'success': False, 'error': str(e)},
                'ai_feedback': {'error': 'Evaluation could not be completed'},
                'timestamp': timezone.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_code_feedback(self, code: str, execution_result: dict, test_cases: list) -> dict:
        """Generate AI feedback for the code"""
        feedback = {
            'summary': '',
            'strengths': [],
            'improvements': [],
            'suggestions': [],
            'concept_understanding': {},
            'syntax_score': 0,
            'logic_score': 0,
            'style_score': 0
        }
        
        # Analyze syntax
        if execution_result.get('validation', {}).get('is_valid', True):
            feedback['strengths'].append('Correct JAC syntax and structure')
            feedback['syntax_score'] = 90
        else:
            errors = execution_result.get('validation', {}).get('errors', [])
            feedback['improvements'].extend([f'Fix syntax: {error}' for error in errors])
            feedback['syntax_score'] = max(0, 90 - len(errors) * 15)
        
        # Analyze code concepts
        concepts_found = []
        
        if 'node' in code:
            concepts_found.append('Object-oriented programming with nodes')
            feedback['strengths'].append('Good use of JAC node definitions')
        
        if 'edge' in code or any(op in code for op in ['++>', '<++', '<++>']):
            concepts_found.append('Spatial programming with edges')
            feedback['strengths'].append('Excellent use of spatial operators')
        
        if 'walker' in code:
            concepts_found.append('Graph traversal with walkers')
            feedback['strengths'].append('Understanding of JAC walker concept')
        
        if 'with entry' in code:
            concepts_found.append('Program entry points')
            feedback['strengths'].append('Proper use of entry blocks')
        
        if not concepts_found:
            feedback['improvements'].append('Try using more JAC-specific features like nodes, edges, or walkers')
        
        feedback['concept_understanding'] = {
            'concepts_used': concepts_found,
            'recommended_next': self._get_next_concepts(concepts_found)
        }
        
        # Generate overall feedback
        if execution_result.get('success'):
            if len(concepts_found) >= 2:
                feedback['summary'] = 'Excellent work! You\'re using multiple JAC concepts effectively.'
                feedback['logic_score'] = 85
            else:
                feedback['summary'] = 'Good start! Try incorporating more JAC graph features.'
                feedback['logic_score'] = 70
        else:
            feedback['summary'] = 'Let\'s debug this together. Check the execution errors for guidance.'
            feedback['logic_score'] = 50
        
        # Style score (simplified)
        if len(code.split('\n')) > 5:
            feedback['style_score'] = 80
        else:
            feedback['style_score'] = 60
        
        # Add learning suggestions
        feedback['suggestions'] = jac_executor._generate_suggestions(
            code, 
            execution_result.get('validation', {}), 
            execution_result.get('execution', {})
        )
        
        return feedback
    
    def _get_next_concepts(self, concepts_found: list) -> list:
        """Recommend next concepts to learn based on current understanding"""
        concept_paths = {
            'Object-oriented programming with nodes': ['edges', 'spatial operators', 'walker classes'],
            'Spatial programming with edges': ['walker traversal', 'node abilities', 'graph queries'],
            'Graph traversal with walkers': ['walker abilities', 'state management', 'advanced traversal'],
            'Program entry points': ['node definitions', 'variable types', 'basic syntax']
        }
        
        recommendations = set()
        for concept in concepts_found:
            if concept in concept_paths:
                recommendations.update(concept_paths[concept])
        
        return list(recommendations)[:3]
    
    def _evaluate_test_cases(self, code: str, test_cases: list) -> list:
        """Evaluate code against test cases"""
        results = []
        
        for i, test_case in enumerate(test_cases):
            # Simplified test case evaluation
            result = {
                'test_case': i + 1,
                'input': test_case.get('input', {}),
                'expected_output': test_case.get('expected_output', {}),
                'actual_output': {},
                'passed': False,
                'error': None
            }
            results.append(result)
        
        return results
    
    def _calculate_code_score(self, execution_result: dict, feedback: dict) -> int:
        """Calculate overall code score"""
        weights = {
            'syntax': 0.3,
            'logic': 0.4,
            'style': 0.3
        }
        
        syntax_score = feedback.get('syntax_score', 0)
        logic_score = feedback.get('logic_score', 0)
        style_score = feedback.get('style_score', 0)
        
        # Execution bonus/penalty
        exec_score = 100 if execution_result.get('success') else 50
        
        total_score = (
            weights['syntax'] * syntax_score +
            weights['logic'] * logic_score +
            weights['style'] * style_score
        ) * (exec_score / 100)
        
        return max(0, min(100, int(total_score)))


class JACLearningSuggestionsAPIView(APIView):
    """
    API View for JAC code suggestions
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Get code suggestions based on partial code
        POST /api/jac-learning/suggestions/
        """
        code = request.data.get('code', '')
        
        try:
            suggestions = self._analyze_code_for_suggestions(code)
            
            return Response({
                'suggestions': suggestions,
                'autocomplete': self._get_autocomplete_suggestions(code),
                'templates': self._get_code_templates(code),
                'timestamp': timezone.now().isoformat()
            })
            
        except Exception as e:
            return Response({
                'error': f'Failed to generate suggestions: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _analyze_code_for_suggestions(self, code: str) -> list:
        """Analyze code and provide specific suggestions"""
        suggestions = []
        
        # Check for common JAC patterns
        if 'node ' in code and '}' not in code:
            suggestions.append({
                'type': 'syntax',
                'message': 'Don\'t forget to close the node definition with \'}\'',
                'line_suggestion': 'Complete node definition'
            })
        
        if 'walker ' in code and 'can ' not in code:
            suggestions.append({
                'type': 'structure',
                'message': 'Consider adding abilities to your walker with \'can\' statements',
                'line_suggestion': 'Define walker abilities'
            })
        
        if '++>' in code and 'with entry' not in code:
            suggestions.append({
                'type': 'structure',
                'message': 'Wrap your code in a \'with entry {}\' block',
                'line_suggestion': 'Add entry block'
            })
        
        # Add general learning suggestions
        if len(code.split('\n')) < 5:
            suggestions.append({
                'type': 'learning',
                'message': 'Try creating a simple example with nodes and spatial connections',
                'line_suggestion': 'Expand your code'
            })
        
        return suggestions
    
    def _get_autocomplete_suggestions(self, code: str) -> list:
        """Get autocomplete suggestions for current code position"""
        last_line = code.split('\n')[-1].strip()
        
        # Simple autocomplete for JAC keywords
        if last_line.startswith('n'):
            return ['node', 'null']
        elif last_line.startswith('e'):
            return ['edge', 'else']
        elif last_line.startswith('w'):
            return ['walker', 'with', 'while', 'with entry']
        elif last_line.startswith('c'):
            return ['can', 'class']
        elif last_line.startswith('h'):
            return ['has']
        elif last_line.startswith('s'):
            return ['spawn', 'str']
        
        return []
    
    def _get_code_templates(self, code: str) -> list:
        """Get code templates based on current context"""
        templates = []
        
        # Check context to suggest appropriate templates
        if 'node' not in code:
            templates.append({
                'name': 'Basic Node',
                'description': 'Simple node with properties',
                'code': '''node Person {
    has name: str;
    has age: int;
}'''
            })
        
        if 'walker' not in code and 'node' in code:
            templates.append({
                'name': 'Basic Walker',
                'description': 'Simple walker to traverse nodes',
                'code': '''walker GreetPeople {
    can greet with Person entry {
        print(f"Hello, {here.name}!");
        visit [-->];
    }
}'''
            })
        
        if 'spatial' not in code and 'node' in code:
            templates.append({
                'name': 'Graph Creation',
                'description': 'Create a simple graph with connections',
                'code': '''with entry {
    alice = Person(name="Alice", age=25);
    bob = Person(name="Bob", age=30);
    alice ++> bob;
}'''
            })
        
        return templates