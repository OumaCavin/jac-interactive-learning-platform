"""
Django API Views - Bridge between Jac-Client and Jac Backend

This module handles the API endpoints that Jac-Client frontend uses to call Jac walkers.
It provides a clean interface for the React components to interact with the Jac backend.
"""

import logging
import json
import os
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

# Configure logging
logger = logging.getLogger(__name__)


class JacAPIException(Exception):
    """Custom exception for Jac API errors"""
    pass


class JacAPIExecutor:
    """
    Executor for Jac walkers that interfaces between Django and Jac backend
    """
    
    def __init__(self):
        self.jac_project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'jeseci-learning-platform')
        self.main_jac_file = os.path.join(self.jac_project_path, 'main.jac')
    
    def spawn_walker(self, walker_name: str, data: Dict[str, Any], user_id: str = None) -> Dict[str, Any]:
        """
        Execute a Jac walker via subprocess call
        
        Args:
            walker_name: Name of the walker to execute
            data: Data to pass to the walker
            user_id: User identifier for context
            
        Returns:
            Dict containing walker execution results
        """
        try:
            # Prepare the execution command
            cmd = [
                'jac', 'run', 
                self.main_jac_file,
                walker_name,
                '--data', json.dumps(data),
                '--user_id', user_id or 'anonymous'
            ]
            
            logger.info(f"Executing Jac walker: {walker_name}")
            
            # Execute the walker
            result = subprocess.run(
                cmd,
                cwd=self.jac_project_path,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Jac walker execution failed: {result.stderr}")
                raise JacAPIException(f"Jac execution failed: {result.stderr}")
            
            # Parse the output
            try:
                output = json.loads(result.stdout)
                logger.info(f"Jac walker {walker_name} completed successfully")
                return output
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Jac output: {result.stdout}")
                # Fallback to raw output
                return {
                    'success': True,
                    'output': result.stdout,
                    'walker': walker_name,
                    'data': data
                }
                
        except subprocess.TimeoutExpired:
            logger.error(f"Jac walker {walker_name} timed out")
            raise JacAPIException("Walker execution timed out")
        except subprocess.CalledProcessError as e:
            logger.error(f"Jac walker {walker_name} failed: {e}")
            raise JacAPIException(f"Walker execution failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error executing walker {walker_name}: {e}")
            raise JacAPIException(f"Unexpected error: {str(e)}")
    
    def validate_jac_syntax(self, code: str, concept: str) -> Dict[str, Any]:
        """
        Validate Jac code syntax
        
        Args:
            code: Jac code to validate
            concept: Target concept for validation context
            
        Returns:
            Dict containing validation results
        """
        # Simplified validation - in real implementation would use Jac parser
        errors = []
        is_valid = True
        
        # Basic syntax checks
        if not code.strip():
            errors.append({"line": 1, "column": 1, "message": "Code cannot be empty"})
            is_valid = False
        
        # Check for basic Jac syntax patterns
        jac_keywords = ['walker', 'node', 'edge', 'report', 'spawn', 'with', 'can', 'has']
        has_jac_syntax = any(keyword in code.lower() for keyword in jac_keywords)
        
        if not has_jac_syntax:
            errors.append({"line": 1, "column": 1, "message": "Code should contain Jac syntax keywords"})
            is_valid = False
        
        return {
            'isValid': is_valid,
            'errors': errors,
            'concept': concept,
            'syntax_checks_passed': len(errors) == 0
        }
    
    def execute_jac_code(self, code: str, concept: str, user_id: str = None, exercise_id: str = None) -> Dict[str, Any]:
        """
        Execute Jac code in a safe environment
        
        Args:
            code: Jac code to execute
            concept: Target concept
            user_id: User identifier
            exercise_id: Exercise identifier
            
        Returns:
            Dict containing execution results
        """
        try:
            # Create temporary Jac file for execution
            temp_file = os.path.join(self.jac_project_path, 'temp_execution.jac')
            
            with open(temp_file, 'w') as f:
                f.write(code)
            
            # Execute the code
            cmd = ['jac', 'run', temp_file]
            
            result = subprocess.run(
                cmd,
                cwd=self.jac_project_path,
                capture_output=True,
                text=True,
                timeout=15  # 15 second execution timeout
            )
            
            # Clean up temporary file
            try:
                os.remove(temp_file)
            except OSError:
                pass
            
            execution_result = {
                'success': result.returncode == 0,
                'concept': concept,
                'user_id': user_id,
                'exercise_id': exercise_id,
                'execution_time': datetime.now().isoformat()
            }
            
            if result.returncode == 0:
                execution_result['output'] = result.stdout
                execution_result['error'] = None
            else:
                execution_result['output'] = None
                execution_result['error'] = result.stderr
            
            return execution_result
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'concept': concept,
                'user_id': user_id,
                'exercise_id': exercise_id,
                'output': None,
                'error': 'Code execution timed out',
                'execution_time': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'success': False,
                'concept': concept,
                'user_id': user_id,
                'exercise_id': exercise_id,
                'output': None,
                'error': f'Execution error: {str(e)}',
                'execution_time': datetime.now().isoformat()
            }


# Initialize the executor
jac_executor = JacAPIExecutor()


# API Views
class JacSpawnView(APIView):
    """
    Main endpoint for spawning Jac walkers from the frontend
    """
    permission_classes = [permissions.AllowAny]  # In production, add proper authentication
    
    def post(self, request):
        """
        Spawn a Jac walker with provided data
        
        Expected request format:
        {
            "walker": "walker_name",
            "data": {...},
            "user_id": "user_identifier"
        }
        """
        try:
            walker_name = request.data.get('walker')
            data = request.data.get('data', {})
            user_id = request.data.get('user_id', 'anonymous')
            
            if not walker_name:
                return Response({
                    'error': 'Walker name is required',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Execute the walker
            result = jac_executor.spawn_walker(walker_name, data, user_id)
            
            return Response({
                'success': True,
                'walker': walker_name,
                'data': data,
                'result': result,
                'timestamp': datetime.now().isoformat()
            })
            
        except JacAPIException as e:
            logger.error(f"Jac API error: {e}")
            return Response({
                'error': str(e),
                'success': False,
                'walker': walker_name if 'walker_name' in locals() else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({
                'error': 'Internal server error',
                'success': False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JacValidationView(APIView):
    """
    Endpoint for validating Jac code syntax
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Validate Jac code syntax
        
        Expected request format:
        {
            "code": "jac_code_to_validate",
            "concept": "target_concept"
        }
        """
        try:
            code = request.data.get('code', '')
            concept = request.data.get('concept', 'general')
            
            if not code.strip():
                return Response({
                    'error': 'Code is required',
                    'isValid': False
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate the code
            validation_result = jac_executor.validate_jac_syntax(code, concept)
            
            return Response(validation_result)
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return Response({
                'error': 'Validation failed',
                'isValid': False,
                'errors': [{"message": str(e)}]
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JacExecutionView(APIView):
    """
    Endpoint for executing Jac code
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        """
        Execute Jac code
        
        Expected request format:
        {
            "code": "jac_code_to_execute",
            "concept": "target_concept",
            "user_id": "user_identifier",
            "exercise_id": "exercise_identifier"
        }
        """
        try:
            code = request.data.get('code', '')
            concept = request.data.get('concept', 'general')
            user_id = request.data.get('user_id', 'anonymous')
            exercise_id = request.data.get('exercise_id')
            
            if not code.strip():
                return Response({
                    'error': 'Code is required',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Execute the code
            execution_result = jac_executor.execute_jac_code(code, concept, user_id, exercise_id)
            
            return Response(execution_result)
            
        except Exception as e:
            logger.error(f"Execution error: {e}")
            return Response({
                'error': 'Execution failed',
                'success': False,
                'output': None,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JacSystemInfoView(APIView):
    """
    Endpoint for system information and health checks
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        """
        Get system information and health status
        """
        try:
            # Check Jac installation
            jac_available = self._check_jac_availability()
            
            # Check project structure
            project_status = self._check_project_structure()
            
            return Response({
                'system': 'Jeseci Learning Platform API',
                'version': '1.0.0',
                'status': 'operational',
                'jac_available': jac_available,
                'project_structure': project_status,
                'timestamp': datetime.now().isoformat(),
                'endpoints': {
                    'spawn': '/api/jac/spawn/',
                    'validate': '/api/jac/validate/',
                    'execute': '/api/jac/execute/',
                    'info': '/api/jac/info/'
                }
            })
            
        except Exception as e:
            logger.error(f"System info error: {e}")
            return Response({
                'system': 'Jeseci Learning Platform API',
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _check_jac_availability(self) -> bool:
        """Check if Jac CLI is available"""
        try:
            result = subprocess.run(['jac', '--version'], capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _check_project_structure(self) -> Dict[str, Any]:
        """Check Jac project structure"""
        required_files = [
            'main.jac',
            'jac-core/user_management.jac',
            'jac-core/lesson_system.jac',
            'jac-core/quiz_engine.jac',
            'osp-graph/mastery_graph.jac',
            'byllm-agents/content_generator.jac',
            'jac-client/index.html'
        ]
        
        structure_status = {}
        for file_path in required_files:
            full_path = os.path.join(jac_executor.jac_project_path, file_path)
            structure_status[file_path] = os.path.exists(full_path)
        
        return {
            'all_files_present': all(structure_status.values()),
            'files': structure_status,
            'project_path': jac_executor.jac_project_path
        }


# Convenience functions for common operations
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_user_progress(request):
    """Get user learning progress"""
    user_id = request.data.get('user_id', 'anonymous')
    
    try:
        result = jac_executor.spawn_walker('get_user_progress', {'user_id': user_id}, user_id)
        return Response(result)
    except JacAPIException as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_skill_map(request):
    """Generate skill map visualization data"""
    user_id = request.data.get('user_id', 'anonymous')
    
    try:
        result = jac_executor.spawn_walker('generate_skill_map', {'user_id': user_id}, user_id)
        return Response(result)
    except JacAPIException as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def start_lesson(request):
    """Start a new lesson"""
    user_id = request.data.get('user_id', 'anonymous')
    lesson_id = request.data.get('lesson_id')
    
    if not lesson_id:
        return Response({
            'error': 'Lesson ID is required',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        result = jac_executor.spawn_walker('deliver_lesson', {
            'user_id': user_id,
            'lesson_id': lesson_id
        }, user_id)
        return Response(result)
    except JacAPIException as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def generate_adaptive_quiz(request):
    """Generate an adaptive quiz"""
    user_id = request.data.get('user_id', 'anonymous')
    concept = request.data.get('concept')
    
    if not concept:
        return Response({
            'error': 'Concept is required',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        result = jac_executor.spawn_walker('generate_adaptive_quiz', {
            'user_id': user_id,
            'concept': concept,
            'user_level': request.data.get('user_level', {})
        }, user_id)
        return Response(result)
    except JacAPIException as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def submit_quiz_response(request):
    """Submit quiz response for evaluation"""
    user_id = request.data.get('user_id', 'anonymous')
    quiz_id = request.data.get('quiz_id')
    responses = request.data.get('responses', {})
    
    if not quiz_id or not responses:
        return Response({
            'error': 'Quiz ID and responses are required',
            'success': False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        result = jac_executor.spawn_walker('evaluate_quiz_response', {
            'user_id': user_id,
            'quiz_id': quiz_id,
            'responses': responses
        }, user_id)
        return Response(result)
    except JacAPIException as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)