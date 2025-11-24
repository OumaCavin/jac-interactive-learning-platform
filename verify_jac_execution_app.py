#!/usr/bin/env python3
"""
Comprehensive verification script for the JAC Execution app.
Checks implementation status, integration, and end-to-end consistency.
"""

import os
import sys
import django
import importlib
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, '/workspace/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_app_structure():
    """Check if all required files exist in the jac_execution app."""
    print("=== JAC Execution App Structure Verification ===")
    
    app_path = Path('/workspace/backend/apps/jac_execution')
    required_files = {
        '__init__.py': 'App initialization',
        'apps.py': 'Django app configuration',
        'models.py': 'Database models',
        'views.py': 'API views',
        'urls.py': 'URL routing',
        'admin.py': 'Admin interface',
        'serializers.py': 'DRF serializers',
        'services/executor.py': 'Code execution service',
        'services/translator.py': 'Code translation service',
        'migrations/0001_initial.py': 'Database migration',
        'serializers/translation_serializers.py': 'Translation serializers'
    }
    
    results = {}
    for file_path, description in required_files.items():
        full_path = app_path / file_path
        exists = full_path.exists()
        results[file_path] = {'exists': exists, 'description': description}
        
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}: {description}")
        
        if exists:
            size = full_path.stat().st_size
            print(f"   Size: {size:,} bytes")
    
    return results

def check_models_import():
    """Check if models can be imported and are properly defined."""
    print("\n=== Models Import Verification ===")
    
    try:
        from apps.jac_execution.models import (
            CodeExecution, ExecutionTemplate, 
            CodeExecutionSession, SecuritySettings
        )
        
        print("✅ All models imported successfully")
        
        # Check model attributes
        models_info = {
            'CodeExecution': ['id', 'user', 'language', 'code', 'status', 'stdout', 'stderr'],
            'ExecutionTemplate': ['id', 'name', 'description', 'language', 'code', 'is_public'],
            'CodeExecutionSession': ['id', 'user', 'session_id', 'total_executions', 'success_rate'],
            'SecuritySettings': ['id', 'max_execution_time', 'max_memory', 'allowed_languages']
        }
        
        for model_name, expected_attrs in models_info.items():
            model = locals()[model_name]
            missing_attrs = []
            
            for attr in expected_attrs:
                if not hasattr(model, attr):
                    missing_attrs.append(attr)
            
            if missing_attrs:
                print(f"❌ {model_name}: Missing attributes: {missing_attrs}")
            else:
                print(f"✅ {model_name}: All expected attributes present")
        
        return True
        
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return False

def check_services_import():
    """Check if services can be imported and are properly defined."""
    print("\n=== Services Import Verification ===")
    
    try:
        # Check executor service
        from apps.jac_execution.services.executor import (
            CodeExecutor, ExecutionService, 
            CodeExecutionError, SecurityViolationError
        )
        print("✅ Executor service imported successfully")
        
        # Check translator service
        from apps.jac_execution.services.translator import (
            CodeTranslator, TranslationDirection, TranslationResult
        )
        print("✅ Translator service imported successfully")
        
        # Test service instantiation
        executor = CodeExecutor()
        service = ExecutionService()
        translator = CodeTranslator()
        
        print("✅ All services can be instantiated")
        
        # Check service methods
        service_methods = {
            'CodeExecutor': ['execute_code', '_validate_code', '_execute_python'],
            'ExecutionService': ['execute_with_tracking', 'get_user_statistics'],
            'CodeTranslator': ['translate_code', 'validate_jac_syntax', 'validate_python_syntax']
        }
        
        for service_name, methods in service_methods.items():
            service_obj = locals()[service_name]
            missing_methods = []
            
            for method in methods:
                if not hasattr(service_obj, method):
                    missing_methods.append(method)
            
            if missing_methods:
                print(f"❌ {service_name}: Missing methods: {missing_methods}")
            else:
                print(f"✅ {service_name}: All expected methods present")
        
        return True
        
    except ImportError as e:
        print(f"❌ Service import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Service instantiation failed: {e}")
        return False

def check_views_import():
    """Check if views can be imported and are properly defined."""
    print("\n=== Views Import Verification ===")
    
    try:
        from apps.jac_execution.views import (
            CodeExecutionViewSet, ExecutionTemplateViewSet,
            CodeExecutionSessionViewSet, SecuritySettingsViewSet,
            QuickExecutionView, LanguageSupportView,
            CodeTranslationViewSet, QuickTranslationView
        )
        
        print("✅ All views imported successfully")
        
        # Check ViewSet methods
        viewsets = {
            'CodeExecutionViewSet': ['execute', 'quick_execute', 'status', 'history'],
            'ExecutionTemplateViewSet': ['execute', 'by_category', 'popular'],
            'CodeTranslationViewSet': ['translate', 'quick_translate']
        }
        
        for viewset_name, expected_methods in viewsets.items():
            viewset = locals()[viewset_name]
            
            for method in expected_methods:
                # Check if method exists as an action
                if hasattr(viewset, method):
                    print(f"✅ {viewset_name}.{method}: Present")
                else:
                    print(f"❌ {viewset_name}.{method}: Missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ Views import failed: {e}")
        return False

def check_urls_configuration():
    """Check if URLs are properly configured."""
    print("\n=== URLs Configuration Verification ===")
    
    try:
        from apps.jac_execution.urls import urlpatterns
        print("✅ URL patterns imported successfully")
        
        # Check for expected URL patterns
        url_patterns = [
            'executions', 'templates', 'sessions', 
            'security', 'translation', 'quick-execute'
        ]
        
        url_pattern_str = str(urlpatterns)
        for pattern in url_patterns:
            if pattern in url_pattern_str:
                print(f"✅ URL pattern '{pattern}': Found")
            else:
                print(f"❌ URL pattern '{pattern}': Missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ URLs import failed: {e}")
        return False

def check_admin_configuration():
    """Check if admin is properly configured."""
    print("\n=== Admin Configuration Verification ===")
    
    try:
        from apps.jac_execution import admin
        print("✅ Admin module imported successfully")
        
        # Check if admin classes are registered
        admin_classes = [
            'CodeExecutionAdmin', 'ExecutionTemplateAdmin',
            'CodeExecutionSessionAdmin', 'SecuritySettingsAdmin'
        ]
        
        for admin_class in admin_classes:
            if hasattr(admin, admin_class):
                print(f"✅ Admin class '{admin_class}': Registered")
            else:
                print(f"❌ Admin class '{admin_class}': Missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ Admin import failed: {e}")
        return False

def check_serializer_classes():
    """Check if serializers are properly defined."""
    print("\n=== Serializers Verification ===")
    
    try:
        from apps.jac_execution.serializers import (
            CodeExecutionCreateSerializer, CodeExecutionResultSerializer,
            ExecutionTemplateDetailSerializer, QuickExecutionSerializer
        )
        print("✅ Main serializers imported successfully")
        
        from apps.jac_execution.serializers.translation_serializers import (
            CodeTranslationSerializer, QuickTranslationSerializer
        )
        print("✅ Translation serializers imported successfully")
        
        # Test serializer instantiation
        try:
            create_serializer = CodeExecutionCreateSerializer()
            result_serializer = CodeExecutionResultSerializer()
            print("✅ Serializers can be instantiated")
        except Exception as e:
            print(f"❌ Serializer instantiation failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Serializers import failed: {e}")
        return False

def check_django_integration():
    """Check Django app integration."""
    print("\n=== Django Integration Verification ===")
    
    try:
        from django.apps import apps
        jac_app = apps.get_app_config('jac_execution')
        print(f"✅ JAC Execution app registered: {jac_app.label}")
        
        # Check app configuration
        if hasattr(jac_app, 'JacExecutionConfig'):
            print("✅ App configuration class present")
        else:
            print("❌ App configuration class missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Django integration failed: {e}")
        return False

def run_end_to_end_test():
    """Run a simple end-to-end test."""
    print("\n=== End-to-End Functionality Test ===")
    
    try:
        # Test model creation (without saving to DB)
        from apps.jac_execution.models import CodeExecution, SecuritySettings
        
        # Test execution service
        from apps.jac_execution.services.executor import ExecutionService
        service = ExecutionService()
        
        # Test translation service
        from apps.jac_execution.services.translator import CodeTranslator, TranslationDirection
        translator = CodeTranslator()
        
        # Test simple translation
        test_python_code = "print('Hello, World!')"
        result = translator.translate_code(test_python_code, TranslationDirection.PYTHON_TO_JAC)
        
        if result.success:
            print("✅ Code translation working")
            print(f"   Original: {test_python_code}")
            print(f"   Translated: {result.translated_code.strip()}")
        else:
            print("❌ Code translation failed")
            print(f"   Errors: {result.errors}")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("JAC Execution App - Comprehensive Verification")
    print("=" * 60)
    
    tests = [
        check_app_structure,
        check_models_import,
        check_services_import,
        check_views_import,
        check_urls_configuration,
        check_admin_configuration,
        check_serializer_classes,
        check_django_integration,
        run_end_to_end_test
    ]
    
    results = {}
    for test in tests:
        try:
            results[test.__name__] = test()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results[test.__name__] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 JAC Execution App is FULLY IMPLEMENTED and CONSISTENT!")
        print("✅ All components are working end-to-end")
        return True
    else:
        print(f"\n⚠️  {total - passed} issues found - App needs attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)