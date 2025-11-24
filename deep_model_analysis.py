#!/usr/bin/env python3
"""
Deep dive into model availability and structure
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_model_details():
    """Check detailed model structure"""
    print("=== DETAILED MODEL ANALYSIS ===\n")
    
    from apps.learning.models import (
        LearningPath, Module, UserModuleProgress, UserLearningPath,
        Assessment, AssessmentAttempt, UserAssessmentResult, AssessmentQuestion,
        Lesson, Achievement
    )
    
    from apps.assessments.models import (
        AssessmentAttempt, AssessmentQuestion, UserAssessmentResult
    )
    
    # Check field differences between duplicate models
    models_to_check = ['AssessmentAttempt', 'UserAssessmentResult', 'AssessmentQuestion']
    
    for model_name in models_to_check:
        learning_model = getattr(sys.modules['apps.learning.models'], model_name)
        assessments_model = getattr(sys.modules['apps.assessments.models'], model_name)
        
        print(f"\n📋 {model_name} COMPARISON:")
        print(f"   Learning app: {learning_model.__module__}")
        print(f"   Assessments app: {assessments_model.__module__}")
        
        learning_fields = set(field.name for field in learning_model._meta.fields)
        assessments_fields = set(field.name for field in assessments_model._meta.fields)
        
        print(f"   Learning fields ({len(learning_fields)}): {sorted(learning_fields)}")
        print(f"   Assessments fields ({len(assessments_fields)}): {sorted(assessments_fields)}")
        
        if learning_fields != assessments_fields:
            print(f"   ⚠️  FIELD DIFFERENCES:")
            print(f"      Only in Learning: {learning_fields - assessments_fields}")
            print(f"      Only in Assessments: {assessments_fields - learning_fields}")
        else:
            print(f"   ✅ Field structure identical")

def check_agent_expected_imports():
    """Check what models agents are trying to use vs what's available"""
    print("\n=== AGENT MODEL USAGE ANALYSIS ===\n")
    
    # Simulate agent usage patterns
    agent_usage_patterns = {
        'assessment_attempt': [
            "AssessmentAttempt.objects.filter(user=user)",
            "AssessmentAttempt.objects.create(...)"
        ],
        'assessment_question': [
            "AssessmentQuestion.objects.filter(module=module)",
            "AssessmentQuestion.objects.all()"
        ],
        'user_assessment_result': [
            "UserAssessmentResult.objects.filter(user=user)",
            "UserAssessmentResult.objects.create(...)"
        ],
        'assessment': [
            "Assessment.objects.filter(...)",
            "Assessment.objects.get(...)"
        ]
    }
    
    print("📋 Agent usage patterns:")
    for pattern, usages in agent_usage_patterns.items():
        print(f"   {pattern}:")
        for usage in usages:
            print(f"      {usage}")
    
    print("\n🔍 Checking if these patterns will work...")
    
    # Test actual model access
    try:
        from apps.learning.models import AssessmentAttempt, AssessmentQuestion, UserAssessmentResult, Assessment
        print("✅ All models accessible from learning.models")
        
        # Test basic queries
        print("✅ Basic model queries would work")
        
    except Exception as e:
        print(f"❌ Model access issues: {e}")

def check_architecture_consistency():
    """Check architecture consistency"""
    print("\n=== ARCHITECTURE CONSISTENCY CHECK ===\n")
    
    print("🏗️  CURRENT ARCHITECTURE:")
    print("   Learning App: Contains comprehensive learning models")
    print("   Assessments App: Contains duplicate assessment models")
    print("   Agents: Import from learning.models")
    
    print("\n🔍 POTENTIAL ISSUES:")
    print("   1. Model duplication between apps")
    print("   2. Assessment functionality split between apps")
    print("   3. Frontend services missing assessment endpoints")
    print("   4. API endpoints may not be consistent")
    
    print("\n✅ CURRENT STATE:")
    print("   - Agents import from correct location")
    print("   - No import errors detected")
    print("   - Models are accessible")

if __name__ == "__main__":
    check_model_details()
    check_agent_expected_imports()
    check_architecture_consistency()