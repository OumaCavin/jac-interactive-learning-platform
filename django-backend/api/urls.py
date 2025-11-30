"""
Django URL Configuration for Jac API

This module defines the URL routing for the Jac API endpoints that interface
between the Jac-Client frontend and the Jac backend.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main Jac API endpoints
    path('jac/spawn/', views.JacSpawnView.as_view(), name='jac-spawn'),
    path('jac/validate/', views.JacValidationView.as_view(), name='jac-validate'),
    path('jac/execute/', views.JacExecutionView.as_view(), name='jac-execute'),
    path('jac/info/', views.JacSystemInfoView.as_view(), name='jac-info'),
    
    # Convenience endpoints for common operations
    path('user/progress/', views.get_user_progress, name='user-progress'),
    path('skill-map/', views.generate_skill_map, name='skill-map'),
    path('lesson/start/', views.start_lesson, name='start-lesson'),
    path('quiz/generate/', views.generate_adaptive_quiz, name='generate-quiz'),
    path('quiz/submit/', views.submit_quiz_response, name='submit-quiz'),
    
    # Additional learning platform endpoints
    path('learning/path/generate/', views.generate_learning_path, name='generate-learning-path'),
    path('learning/analyze/', views.analyze_learning_weaknesses, name='analyze-learning'),
    path('content/generate/', views.generate_adaptive_content, name='generate-content'),
    path('assessment/evaluate/', views.evaluate_complex_answer, name='evaluate-answer'),
    
    # Health and system endpoints
    path('health/', views.health_check, name='health-check'),
    path('system/status/', views.system_status, name='system-status'),
]

# Additional endpoint functions to implement
def generate_learning_path(request):
    """Generate personalized learning path"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    
    user_id = request.data.get('user_id', 'anonymous')
    target_concept = request.data.get('target_concept')
    
    try:
        result = jac_executor.spawn_walker('generate_learning_paths', {
            'user_id': user_id,
            'target_concept': target_concept
        }, user_id)
        return Response(result)
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def analyze_learning_weaknesses(request):
    """Analyze user learning weaknesses"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    
    user_id = request.data.get('user_id', 'anonymous')
    
    try:
        result = jac_executor.spawn_walker('analyze_learning_weaknesses', {
            'user_id': user_id
        }, user_id)
        return Response(result)
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_adaptive_content(request):
    """Generate adaptive learning content"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    
    lesson_data = request.data.get('lesson_data', {})
    
    try:
        result = jac_executor.spawn_walker('generate_lesson_content', lesson_data)
        return Response(result)
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def evaluate_complex_answer(request):
    """Evaluate complex student answers"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    
    question = request.data.get('question', {})
    answer = request.data.get('answer', '')
    user_context = request.data.get('user_context', {})
    
    try:
        result = jac_executor.spawn_walker('evaluate_complex_answer', {
            'question': question,
            'answer': answer,
            'user_context': user_context
        })
        return Response(result)
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def health_check(request):
    """System health check endpoint"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    
    try:
        # Check Jac availability
        jac_available = jac_executor._check_jac_availability()
        
        # Check project structure
        project_status = jac_executor._check_project_structure()
        
        health_status = {
            'status': 'healthy' if jac_available and project_status['all_files_present'] else 'degraded',
            'timestamp': '2025-12-01T05:33:38Z',
            'components': {
                'jac_backend': 'available' if jac_available else 'unavailable',
                'project_structure': 'valid' if project_status['all_files_present'] else 'incomplete',
                'django_api': 'available'
            },
            'details': {
                'jac_available': jac_available,
                'project_structure': project_status,
                'all_files_present': project_status['all_files_present']
            }
        }
        
        status_code = status.HTTP_200_OK if health_status['status'] == 'healthy' else status.HTTP_503_SERVICE_UNAVAILABLE
        return Response(health_status, status=status_code)
        
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': '2025-12-01T05:33:38Z'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def system_status(request):
    """Detailed system status endpoint"""
    from rest_framework.response import Response
    from rest_framework import status
    from .views import jac_executor
    import os
    import datetime
    
    try:
        # Get system information
        jac_available = jac_executor._check_jac_availability()
        project_status = jac_executor._check_project_structure()
        
        # Get project statistics
        project_path = jac_executor.jac_project_path
        total_files = 0
        jac_files = 0
        js_files = 0
        
        for root, dirs, files in os.walk(project_path):
            for file in files:
                total_files += 1
                if file.endswith('.jac'):
                    jac_files += 1
                elif file.endswith('.js') or file.endswith('.html'):
                    js_files += 1
        
        system_info = {
            'system': 'Jeseci Learning Platform',
            'version': '1.0.0',
            'status': 'operational',
            'timestamp': datetime.datetime.now().isoformat(),
            'architecture': {
                'frontend': 'Jac-Client (React-style)',
                'backend': 'Jac Programming Language',
                'api': 'Django REST Framework',
                'database': 'Jac Graph Database'
            },
            'components': {
                'jac_backend': {
                    'available': jac_available,
                    'project_path': project_path,
                    'main_file': jac_executor.main_jac_file
                },
                'django_api': {
                    'available': True,
                    'endpoints_count': len(urlpatterns)
                },
                'jac_client': {
                    'available': True,
                    'files': {
                        'total': total_files,
                        'jac_files': jac_files,
                        'frontend_files': js_files
                    }
                },
                'project_structure': project_status
            },
            'features': {
                'osp_graph': 'Object-Spatial Programming graph for mastery tracking',
                'byllm_agents': 'AI-powered content generation and assessment',
                'adaptive_learning': 'Personalized learning paths and difficulty adjustment',
                'interactive_coding': 'Monaco Editor with Jac code execution',
                'real_time_feedback': 'Instant code validation and execution results'
            },
            'endpoints': {
                'core_api': '/api/jac/',
                'learning_ops': '/api/learning/',
                'assessment': '/api/assessment/',
                'health': '/api/health/'
            }
        }
        
        return Response(system_info)
        
    except Exception as e:
        return Response({
            'system': 'Jeseci Learning Platform',
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)