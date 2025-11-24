#!/usr/bin/env python3
"""
Simple verification script for assessments module
Tests basic imports and functionality without complex test setup
"""

import os
import sys
import django

# Add Django path
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    django.setup()
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

def test_basic_imports():
    """Test basic model imports"""
    print("\n=== BASIC IMPORTS ===")
    
    try:
        from apps.assessments.models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult
        print("✓ AssessmentAttempt model imported")
        print("✓ AssessmentQuestion model imported")
        print("✓ UserAssessmentResult model imported")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_serializer_imports():
    """Test serializer imports"""
    print("\n=== SERIALIZER IMPORTS ===")
    
    try:
        from apps.assessments.serializers import (
            AssessmentAttemptSerializer, AssessmentQuestionSerializer,
            AssessmentAttemptCreateSerializer
        )
        print("✓ AssessmentAttemptSerializer imported")
        print("✓ AssessmentQuestionSerializer imported")
        print("✓ AssessmentAttemptCreateSerializer imported")
        return True
    except ImportError as e:
        print(f"✗ Serializer import failed: {e}")
        return False

def test_view_imports():
    """Test view imports"""
    print("\n=== VIEW IMPORTS ===")
    
    try:
        from apps.assessments.views import (
            AssessmentAttemptViewSet, AssessmentQuestionViewSet, AssessmentStatsAPIView
        )
        print("✓ AssessmentAttemptViewSet imported")
        print("✓ AssessmentQuestionViewSet imported")
        print("✓ AssessmentStatsAPIView imported")
        return True
    except ImportError as e:
        print(f"✗ View import failed: {e}")
        return False

def test_url_configuration():
    """Test URL configuration"""
    print("\n=== URL CONFIGURATION ===")
    
    try:
        from apps.assessments.urls import urlpatterns
        print(f"✓ Assessments URL patterns loaded: {len(urlpatterns)} patterns")
        return True
    except ImportError as e:
        print(f"✗ URL configuration failed: {e}")
        return False

def test_admin_registration():
    """Test admin registration"""
    print("\n=== ADMIN REGISTRATION ===")
    
    try:
        from django.contrib.admin import site
        from apps.assessments.admin import AssessmentAttemptAdmin, AssessmentQuestionAdmin
        
        # Check if admin classes are registered
        print("✓ AssessmentAttemptAdmin class loaded")
        print("✓ AssessmentQuestionAdmin class loaded")
        return True
    except ImportError as e:
        print(f"✗ Admin import failed: {e}")
        return False

def test_model_fields():
    """Test model field definitions"""
    print("\n=== MODEL FIELDS ===")
    
    try:
        from apps.assessments.models import AssessmentAttempt, AssessmentQuestion
        
        # Check AssessmentAttempt fields
        attempt_fields = [field.name for field in AssessmentAttempt._meta.fields]
        print(f"✓ AssessmentAttempt has {len(attempt_fields)} fields: {attempt_fields[:5]}...")
        
        # Check AssessmentQuestion fields  
        question_fields = [field.name for field in AssessmentQuestion._meta.fields]
        print(f"✓ AssessmentQuestion has {len(question_fields)} fields: {question_fields[:5]}...")
        
        return True
    except Exception as e:
        print(f"✗ Model field check failed: {e}")
        return False

def test_database_tables():
    """Test database table creation"""
    print("\n=== DATABASE TABLES ===")
    
    try:
        from django.db import connection
        from django.core.management.color import no_style
        
        style = no_style()
        sql = connection.ops.sql_table_creation_suffix()
        
        # Try to get table information
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%assessment%'")
            tables = cursor.fetchall()
            
        assessment_tables = [table[0] for table in tables if 'assessment' in table[0].lower()]
        print(f"✓ Found {len(assessment_tables)} assessment-related tables")
        for table in assessment_tables:
            print(f"  - {table}")
            
        return len(assessment_tables) >= 3  # Should have at least 3 assessment tables
    except Exception as e:
        print(f"✗ Database table check failed: {e}")
        return False

def run_simple_verification():
    """Run all simple verification checks"""
    print("=" * 60)
    print("SIMPLE ASSESSMENTS MODULE VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Basic Imports", test_basic_imports),
        ("Serializers", test_serializer_imports),
        ("Views", test_view_imports),
        ("URLs", test_url_configuration),
        ("Admin", test_admin_registration),
        ("Model Fields", test_model_fields),
        ("Database Tables", test_database_tables),
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
        print("🎉 ASSESSMENTS MODULE PASSES SIMPLE VERIFICATION")
        return True
    else:
        print("⚠️  ASSESSMENTS MODULE HAS SOME ISSUES")
        return False

if __name__ == "__main__":
    success = run_simple_verification()
    sys.exit(0 if success else 1)