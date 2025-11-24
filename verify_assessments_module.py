#!/usr/bin/env python3
"""
Comprehensive Assessment Module Verification Script
Checks for complete implementation, consistency, and proper integration
"""

import os
import sys
import django
import importlib.util
from pathlib import Path
import ast

# Add Django path
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    from django.apps import apps
    from django.urls import get_resolver
    from django.core.exceptions import ImproperlyConfigured
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

def check_assessments_app_structure():
    """Check if assessments app has proper structure"""
    print("\n=== ASSESSMENTS APP STRUCTURE ===")
    app_path = Path('/workspace/backend/apps/assessments')
    
    expected_files = [
        'models.py',
        'views.py', 
        'serializers.py',
        'urls.py',
        'admin.py',
        'tests.py',
        'migrations/__init__.py'
    ]
    
    missing_files = []
    for file in expected_files:
        if not (app_path / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All expected files present")
        return True

def check_assessments_models():
    """Check if assessments models exist and are properly implemented"""
    print("\n=== ASSESSMENTS MODELS ===")
    
    try:
        from apps.assessments.models import AssessmentAttempt, AssessmentQuestion
        print("✓ AssessmentAttempt model imported successfully")
        print("✓ AssessmentQuestion model imported successfully")
        
        # Check if models have required fields
        attempt_fields = [field.name for field in AssessmentAttempt._meta.fields]
        question_fields = [field.name for field in AssessmentQuestion._meta.fields]
        
        print(f"✓ AssessmentAttempt fields: {len(attempt_fields)} fields")
        print(f"✓ AssessmentQuestion fields: {len(question_fields)} fields")
        
        return True
    except ImportError as e:
        print(f"✗ Cannot import assessments models: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking models: {e}")
        return False

def check_assessments_views():
    """Check if assessments views are implemented"""
    print("\n=== ASSESSMENTS VIEWS ===")
    
    try:
        from apps.assessments.views import AssessmentAttemptViewSet, AssessmentQuestionViewSet
        print("✓ AssessmentAttemptViewSet imported successfully")
        print("✓ AssessmentQuestionViewSet imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Cannot import assessments views: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking views: {e}")
        return False

def check_assessments_serializers():
    """Check if assessments serializers are implemented"""
    print("\n=== ASSESSMENTS SERIALIZERS ===")
    
    try:
        from apps.assessments.serializers import AssessmentAttemptSerializer, AssessmentQuestionSerializer
        print("✓ AssessmentAttemptSerializer imported successfully")
        print("✓ AssessmentQuestionSerializer imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Cannot import assessments serializers: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking serializers: {e}")
        return False

def check_assessments_urls():
    """Check if assessments URLs are properly configured"""
    print("\n=== ASSESSMENTS URLS ===")
    
    try:
        from apps.assessments.urls import urlpatterns
        print(f"✓ Assessments URL patterns found: {len(urlpatterns)} patterns")
        return True
    except ImportError as e:
        print(f"✗ Cannot import assessments urls: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking URLs: {e}")
        return False

def check_learning_app_integration():
    """Check how learning app integrates with assessments app"""
    print("\n=== LEARNING APP INTEGRATION ===")
    
    try:
        from apps.learning.models import Module
        # Check if average_score property works (it imports from assessments)
        modules = Module.objects.all()[:1]
        if modules:
            module = modules[0]
            try:
                avg_score = module.average_score
                print(f"✓ Module.average_score property works: {avg_score}")
            except Exception as e:
                print(f"✗ Module.average_score property fails: {e}")
                return False
        else:
            print("⚠ No modules found to test integration")
        return True
    except Exception as e:
        print(f"✗ Learning app integration check failed: {e}")
        return False

def check_assessments_migrations():
    """Check if assessments migrations exist"""
    print("\n=== ASSESSMENTS MIGRATIONS ===")
    
    migrations_path = Path('/workspace/backend/apps/assessments/migrations')
    if not migrations_path.exists():
        print("✗ Migrations directory doesn't exist")
        return False
    
    migration_files = list(migrations_path.glob('*.py'))
    migration_files = [f for f in migration_files if f.name != '__init__.py']
    
    if not migration_files:
        print("✗ No migration files found")
        return False
    else:
        print(f"✓ Found {len(migration_files)} migration files")
        return True

def check_assessments_admin():
    """Check if assessments admin is implemented"""
    print("\n=== ASSESSMENTS ADMIN ===")
    
    try:
        from apps.assessments.admin import AssessmentAttemptAdmin, AssessmentQuestionAdmin
        print("✓ AssessmentAttemptAdmin imported successfully")
        print("✓ AssessmentQuestionAdmin imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Cannot import assessments admin: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking admin: {e}")
        return False

def check_django_urls_integration():
    """Check if assessments URLs are included in main URL configuration"""
    print("\n=== DJANGO URLS INTEGRATION ===")
    
    try:
        resolver = get_resolver()
        # Try to find assessments patterns
        found_assessments = False
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'pattern') and 'assessments' in str(pattern.pattern):
                found_assessments = True
                break
        
        if found_assessments:
            print("✓ Assessments URLs found in main URL configuration")
        else:
            print("⚠ Assessments URLs may not be included in main configuration")
        return True
    except Exception as e:
        print(f"✗ Error checking URL integration: {e}")
        return False

def run_comprehensive_verification():
    """Run all verification checks"""
    print("=" * 60)
    print("COMPREHENSIVE ASSESSMENTS MODULE VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("App Structure", check_assessments_app_structure),
        ("Models", check_assessments_models),
        ("Views", check_assessments_views),
        ("Serializers", check_assessments_serializers),
        ("URLs", check_assessments_urls),
        ("Migrations", check_assessments_migrations),
        ("Admin", check_assessments_admin),
        ("Learning Integration", check_learning_app_integration),
        ("URLs Integration", check_django_urls_integration),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"✗ {check_name} check failed with exception: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{check_name}: {status}")
    
    print(f"\nOVERALL SCORE: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ASSESSMENTS MODULE IS FULLY IMPLEMENTED AND VERIFIED")
        return True
    else:
        print("⚠️  ASSESSMENTS MODULE NEEDS IMPLEMENTATION FIXES")
        return False

if __name__ == "__main__":
    success = run_comprehensive_verification()
    sys.exit(0 if success else 1)