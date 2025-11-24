#!/usr/bin/env python3
"""
Comprehensive verification script for the Agents System implementation
Tests end-to-end functionality, integration, and consistency
"""

import os
import sys
import django
from pathlib import Path
import importlib.util
from typing import Dict, List, Any, Optional

# Add the backend path to sys.path for imports
backend_path = Path("/workspace/backend")
sys.path.insert(0, str(backend_path))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.apps import apps
from django.db import connection
from django.core.management import call_command
from django.test.utils import override_settings
import inspect

class AgentsSystemVerifier:
    """Comprehensive verifier for the agents system"""
    
    def __init__(self):
        self.test_results = []
        self.errors = []
        self.warnings = []
    
    def log_result(self, test_name: str, passed: bool, message: str = "", details: str = ""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        self.test_results.append({
            'test': test_name,
            'status': status,
            'message': message,
            'details': details
        })
        print(f"[{status}] {test_name}: {message}")
        if details:
            print(f"      Details: {details}")
    
    def test_package_structure(self) -> bool:
        """Test 1: Verify package structure and imports"""
        print("\n=== Testing Package Structure ===")
        
        try:
            # Test __init__.py exists
            init_path = backend_path / "apps" / "agents" / "__init__.py"
            if not init_path.exists():
                self.log_result("Package Init File", False, "agents/__init__.py does not exist")
                return False
            
            self.log_result("Package Init File", True, "agents/__init__.py exists")
            
            # Test core modules exist
            required_modules = [
                "base_agent.py",
                "agents_manager.py", 
                "models.py",
                "simple_models.py",
                "system_orchestrator.py",
                "content_curator.py",
                "quiz_master.py",
                "evaluator.py",
                "progress_tracker.py",
                "motivator.py",
                "views.py",
                "urls.py",
                "apps.py",
                "serializers.py"
            ]
            
            missing_modules = []
            for module in required_modules:
                module_path = backend_path / "apps" / "agents" / module
                if not module_path.exists():
                    missing_modules.append(module)
            
            if missing_modules:
                self.log_result("Core Modules", False, f"Missing modules: {missing_modules}")
                return False
            
            self.log_result("Core Modules", True, f"All {len(required_modules)} required modules present")
            
            # Test migrations exist
            migrations_dir = backend_path / "apps" / "agents" / "migrations"
            migration_files = list(migrations_dir.glob("*.py"))
            if not migration_files:
                self.log_result("Database Migrations", False, "No migration files found")
                return False
            
            self.log_result("Database Migrations", True, f"{len(migration_files)} migration files found")
            
            return True
            
        except Exception as e:
            self.log_result("Package Structure", False, f"Error: {str(e)}")
            return False
    
    def test_django_app_configuration(self) -> bool:
        """Test 2: Verify Django app configuration"""
        print("\n=== Testing Django App Configuration ===")
        
        try:
            # Test app is registered
            if 'apps.agents' not in settings.INSTALLED_APPS:
                self.log_result("App Registration", False, "apps.agents not in INSTALLED_APPS")
                return False
            
            self.log_result("App Registration", True, "apps.agents registered in INSTALLED_APPS")
            
            # Test app config
            app_config = apps.get_app_config('agents')
            if not app_config:
                self.log_result("App Config", False, "Cannot get app configuration")
                return False
            
            self.log_result("App Config", True, f"App config loaded: {app_config.name}")
            
            # Test app paths
            app_path = Path(app_config.path)
            if not app_path.exists():
                self.log_result("App Path", False, f"App path does not exist: {app_path}")
                return False
            
            self.log_result("App Path", True, f"App path exists: {app_path}")
            
            return True
            
        except Exception as e:
            self.log_result("Django App Configuration", False, f"Error: {str(e)}")
            return False
    
    def test_models_definition(self) -> bool:
        """Test 3: Verify models are properly defined"""
        print("\n=== Testing Models Definition ===")
        
        try:
            # Import models module
            from apps.agents import models, simple_models
            
            # Test SimpleAgent model
            if not hasattr(simple_models, 'SimpleAgent'):
                self.log_result("SimpleAgent Model", False, "SimpleAgent model not found")
                return False
            
            agent_model = simple_models.SimpleAgent
            
            # Test model fields
            required_fields = ['agent_id', 'agent_type', 'name', 'status', 'config']
            missing_fields = []
            for field in required_fields:
                if not hasattr(agent_model, field):
                    missing_fields.append(field)
            
            if missing_fields:
                self.log_result("SimpleAgent Fields", False, f"Missing fields: {missing_fields}")
                return False
            
            self.log_result("SimpleAgent Fields", True, "All required fields present")
            
            # Test Task model
            if not hasattr(simple_models, 'SimpleTask'):
                self.log_result("SimpleTask Model", False, "SimpleTask model not found")
                return False
            
            task_model = simple_models.SimpleTask
            
            # Test task fields
            required_task_fields = ['task_id', 'agent', 'task_type', 'title', 'status']
            missing_task_fields = []
            for field in required_task_fields:
                if not hasattr(task_model, field):
                    missing_task_fields.append(field)
            
            if missing_task_fields:
                self.log_result("SimpleTask Fields", False, f"Missing fields: {missing_task_fields}")
                return False
            
            self.log_result("SimpleTask Fields", True, "All required fields present")
            
            # Test choices enums
            if not hasattr(simple_models, 'AgentType'):
                self.log_result("AgentType Enum", False, "AgentType enum not found")
                return False
            
            self.log_result("AgentType Enum", True, "AgentType enum present")
            
            if not hasattr(simple_models, 'TaskStatus'):
                self.log_result("TaskStatus Enum", False, "TaskStatus enum not found")
                return False
            
            self.log_result("TaskStatus Enum", True, "TaskStatus enum present")
            
            return True
            
        except Exception as e:
            self.log_result("Models Definition", False, f"Error: {str(e)}")
            return False
    
    def test_base_agent_architecture(self) -> bool:
        """Test 4: Verify base agent architecture"""
        print("\n=== Testing Base Agent Architecture ===")
        
        try:
            from apps.agents.base_agent import BaseAgent, AgentStatus, TaskPriority
            
            # Test BaseAgent abstract class
            if not inspect.isabstract(BaseAgent):
                self.log_result("BaseAgent Abstract", False, "BaseAgent is not abstract")
                return False
            
            self.log_result("BaseAgent Abstract", True, "BaseAgent is properly abstract")
            
            # Test required methods
            required_methods = ['process_task', 'get_capabilities', 'get_specialization_info']
            for method in required_methods:
                if not hasattr(BaseAgent, method):
                    self.log_result(f"BaseAgent {method}", False, f"{method} method not found")
                    return False
            
            self.log_result("BaseAgent Methods", True, "All required abstract methods present")
            
            # Test AgentStatus enum
            expected_statuses = ['idle', 'active', 'processing', 'error', 'maintenance']
            actual_statuses = [status.value for status in AgentStatus]
            
            if set(expected_statuses) != set(actual_statuses):
                self.log_result("AgentStatus Enum", False, f"Expected {expected_statuses}, got {actual_statuses}")
                return False
            
            self.log_result("AgentStatus Enum", True, "All expected status values present")
            
            # Test TaskPriority enum
            expected_priorities = [1, 2, 3, 4]
            actual_priorities = [priority.value for priority in TaskPriority]
            
            if set(expected_priorities) != set(actual_priorities):
                self.log_result("TaskPriority Enum", False, f"Expected {expected_priorities}, got {actual_priorities}")
                return False
            
            self.log_result("TaskPriority Enum", True, "All expected priority values present")
            
            return True
            
        except Exception as e:
            self.log_result("Base Agent Architecture", False, f"Error: {str(e)}")
            return False
    
    def test_agents_manager(self) -> bool:
        """Test 5: Verify agents manager implementation"""
        print("\n=== Testing Agents Manager ===")
        
        try:
            from apps.agents.agents_manager import AgentsManager
            
            # Test AgentsManager class
            if not inspect.isclass(AgentsManager):
                self.log_result("AgentsManager Class", False, "AgentsManager is not a class")
                return False
            
            self.log_result("AgentsManager Class", True, "AgentsManager is properly defined")
            
            # Test required methods
            required_methods = [
                'initialize_agents', 'get_agent_instance', 'create_task', 
                'execute_task', 'orchestrate_workflow', 'get_system_health'
            ]
            
            for method in required_methods:
                if not hasattr(AgentsManager, method):
                    self.log_result(f"AgentsManager {method}", False, f"{method} method not found")
                    return False
            
            self.log_result("AgentsManager Methods", True, "All required methods present")
            
            return True
            
        except Exception as e:
            self.log_result("Agents Manager", False, f"Error: {str(e)}")
            return False
    
    def test_specialized_agents(self) -> bool:
        """Test 6: Verify specialized agent implementations"""
        print("\n=== Testing Specialized Agents ===")
        
        try:
            from apps.agents.system_orchestrator import SystemOrchestratorAgent
            from apps.agents.content_curator import ContentCuratorAgent
            from apps.agents.quiz_master import QuizMasterAgent
            
            # Test SystemOrchestratorAgent
            if not issubclass(SystemOrchestratorAgent, 
                             getattr(sys.modules['apps.agents.base_agent'], 'BaseAgent', BaseAgent)):
                self.log_result("SystemOrchestratorAgent Inheritance", False, "Not properly inheriting from BaseAgent")
                return False
            
            self.log_result("SystemOrchestratorAgent", True, "Properly inherits from BaseAgent")
            
            # Test ContentCuratorAgent
            if not issubclass(ContentCuratorAgent,
                             getattr(sys.modules['apps.agents.base_agent'], 'BaseAgent', BaseAgent)):
                self.log_result("ContentCuratorAgent Inheritance", False, "Not properly inheriting from BaseAgent")
                return False
            
            self.log_result("ContentCuratorAgent", True, "Properly inherits from BaseAgent")
            
            # Test QuizMasterAgent
            if not issubclass(QuizMasterAgent,
                             getattr(sys.modules['apps.agents.base_agent'], 'BaseAgent', BaseAgent)):
                self.log_result("QuizMasterAgent Inheritance", False, "Not properly inheriting from BaseAgent")
                return False
            
            self.log_result("QuizMasterAgent", True, "Properly inherits from BaseAgent")
            
            return True
            
        except Exception as e:
            self.log_result("Specialized Agents", False, f"Error: {str(e)}")
            return False
    
    def test_api_views(self) -> bool:
        """Test 7: Verify API views and endpoints"""
        print("\n=== Testing API Views ===")
        
        try:
            from apps.agents import views
            
            # Test ViewSets
            if not hasattr(views, 'AgentViewSet'):
                self.log_result("AgentViewSet", False, "AgentViewSet not found")
                return False
            
            self.log_result("AgentViewSet", True, "AgentViewSet present")
            
            # Test API Views
            api_views = [
                'AgentWorkflowAPIView',
                'AgentCoordinationAPIView', 
                'AgentSystemMonitorAPIView',
                'AgentEmergencyAPIView'
            ]
            
            for view in api_views:
                if not hasattr(views, view):
                    self.log_result(f"{view}", False, f"{view} not found")
                    return False
            
            self.log_result("API Views", True, f"All {len(api_views)} API views present")
            
            return True
            
        except Exception as e:
            self.log_result("API Views", False, f"Error: {str(e)}")
            return False
    
    def test_url_configuration(self) -> bool:
        """Test 8: Verify URL configuration"""
        print("\n=== Testing URL Configuration ===")
        
        try:
            from apps.agents.urls import urlpatterns
            
            # Test urlpatterns exist
            if not urlpatterns:
                self.log_result("URL Patterns", False, "No URL patterns defined")
                return False
            
            self.log_result("URL Patterns", True, f"{len(urlpatterns)} URL patterns defined")
            
            # Test key endpoints
            expected_patterns = [
                'agents/',
                'tasks/',
                'workflow/',
                'coordinate/',
                'monitor/',
                'emergency/',
                'health/'
            ]
            
            pattern_names = [pattern.name for pattern in urlpatterns if hasattr(pattern, 'name')]
            
            missing_patterns = []
            for expected in expected_patterns:
                if not any(expected in name for name in pattern_names):
                    missing_patterns.append(expected)
            
            if missing_patterns:
                self.log_result("URL Endpoints", False, f"Missing endpoints: {missing_patterns}")
                return False
            
            self.log_result("URL Endpoints", True, "All key endpoints present")
            
            return True
            
        except Exception as e:
            self.log_result("URL Configuration", False, f"Error: {str(e)}")
            return False
    
    def test_database_integration(self) -> bool:
        """Test 9: Verify database integration"""
        print("\n=== Testing Database Integration ===")
        
        try:
            # Check if tables exist
            with connection.cursor() as cursor:
                # Check simple_agents table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='simple_agents'")
                if not cursor.fetchone():
                    self.log_result("Database Tables", False, "simple_agents table does not exist")
                    return False
                
                self.log_result("Database Tables", True, "simple_agents table exists")
                
                # Check simple_tasks table
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='simple_tasks'")
                if not cursor.fetchone():
                    self.log_result("Database Tables", False, "simple_tasks table does not exist")
                    return False
                
                self.log_result("Database Tables", True, "simple_tasks table exists")
            
            return True
            
        except Exception as e:
            self.log_result("Database Integration", False, f"Error: {str(e)}")
            return False
    
    def test_import_consistency(self) -> bool:
        """Test 10: Verify import consistency"""
        print("\n=== Testing Import Consistency ===")
        
        try:
            # Test that models.py imports simplified models correctly
            from apps.agents import models
            
            # Check that models.py correctly imports from simple_models
            importlib.util.find_spec("apps.agents.simple_models")
            if "simple_models" not in dir(models):
                self.log_result("Models Import", False, "simple_models not properly imported in models.py")
                return False
            
            self.log_result("Models Import", True, "Models import structure is consistent")
            
            return True
            
        except Exception as e:
            self.log_result("Import Consistency", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all verification tests"""
        print("=" * 60)
        print("AGENTS SYSTEM VERIFICATION")
        print("=" * 60)
        
        # Run all tests
        tests = [
            ("Package Structure", self.test_package_structure),
            ("Django App Configuration", self.test_django_app_configuration),
            ("Models Definition", self.test_models_definition),
            ("Base Agent Architecture", self.test_base_agent_architecture),
            ("Agents Manager", self.test_agents_manager),
            ("Specialized Agents", self.test_specialized_agents),
            ("API Views", self.test_api_views),
            ("URL Configuration", self.test_url_configuration),
            ("Database Integration", self.test_database_integration),
            ("Import Consistency", self.test_import_consistency)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_result(test_name, False, f"Test execution failed: {str(e)}")
        
        # Generate summary
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Print failed tests
        failed_tests = [result for result in self.test_results if result['status'] == 'FAIL']
        if failed_tests:
            print("\nFailed Tests:")
            for test in failed_tests:
                print(f"  - {test['test']}: {test['message']}")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests/total_tests)*100,
            'test_results': self.test_results
        }

if __name__ == "__main__":
    verifier = AgentsSystemVerifier()
    results = verifier.run_all_tests()
    
    # Exit with appropriate code
    if results['failed_tests'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)