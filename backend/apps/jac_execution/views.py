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