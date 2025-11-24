#!/usr/bin/env python3
"""
Verify model conflicts and import issues between learning and assessments apps
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_model_conflicts():
    """Check for model conflicts between apps"""
    print("=== MODEL CONFLICT ANALYSIS ===\n")
    
    try:
        from apps.learning.models import (
            LearningPath, Module, UserModuleProgress, UserLearningPath,
            Assessment, AssessmentAttempt, UserAssessmentResult, AssessmentQuestion,
            Lesson, Achievement
        )
        print("✅ Learning app models imported successfully")
    except ImportError as e:
        print(f"❌ Learning app import error: {e}")
        return False
    
    try:
        from apps.assessments.models import (
            AssessmentAttempt, AssessmentQuestion, UserAssessmentResult
        )
        print("✅ Assessments app models imported successfully")
    except ImportError as e:
        print(f"❌ Assessments app import error: {e}")
        return False
    
    # Check for duplicate models
    learning_models = {
        'Assessment': Assessment,
        'AssessmentAttempt': AssessmentAttempt,
        'UserAssessmentResult': UserAssessmentResult,
        'AssessmentQuestion': AssessmentQuestion
    }
    
    assessments_models = {
        'AssessmentAttempt': AssessmentAttempt,
        'UserAssessmentResult': UserAssessmentResult,
        'AssessmentQuestion': AssessmentQuestion
    }
    
    print("\n=== MODEL CONFLICTS DETECTED ===")
    conflicts = []
    for model_name in assessments_models:
        if model_name in learning_models:
            learning_model = learning_models[model_name]
            assessments_model = assessments_models[model_name]
            if learning_model != assessments_model:
                conflicts.append(model_name)
                print(f"⚠️  CONFLICT: {model_name}")
                print(f"   Learning app: {learning_model.__module__}.{learning_model.__name__}")
                print(f"   Assessments app: {assessments_model.__module__}.{assessments_model.__name__}")
    
    if not conflicts:
        print("✅ No direct model conflicts found")
    
    return True

def check_agent_imports():
    """Check what agents are importing"""
    print("\n=== AGENT IMPORT ANALYSIS ===\n")
    
    agent_imports = {}
    
    # Check each agent file
    agent_files = [
        'evaluator.py',
        'motivator.py', 
        'progress_tracker.py',
        'quiz_master.py',
        'system_orchestrator.py',
        'content_curator.py'
    ]
    
    for agent_file in agent_files:
        try:
            with open(f'/workspace/backend/apps/agents/{agent_file}', 'r') as f:
                content = f.read()
                
                # Find import statements
                import_lines = [line for line in content.split('\n') 
                              if line.strip().startswith('from') and 
                              ('learning.models' in line or 'assessment.models' in line)]
                
                agent_imports[agent_file] = import_lines
                print(f"📁 {agent_file}:")
                for line in import_lines:
                    print(f"   {line.strip()}")
                print()
                
        except FileNotFoundError:
            print(f"❌ {agent_file} not found")
        except Exception as e:
            print(f"❌ Error reading {agent_file}: {e}")
    
    return agent_imports

def check_frontend_integration():
    """Check frontend service integration"""
    print("=== FRONTEND INTEGRATION CHECK ===\n")
    
    try:
        # Check frontend services
        services_path = '/workspace/frontend/src/services'
        if os.path.exists(services_path):
            service_files = os.listdir(services_path)
            print(f"📁 Frontend services found: {service_files}")
            
            # Check for assessment-related services
            assessment_services = [f for f in service_files 
                                 if 'assess' in f.lower() or 'quiz' in f.lower()]
            if assessment_services:
                print(f"🔍 Assessment-related services: {assessment_services}")
            else:
                print("⚠️  No assessment-related services found")
        else:
            print("⚠️  Frontend services directory not found")
            
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")

def main():
    """Main verification function"""
    print("STARTING COMPREHENSIVE MODEL AND IMPORT VERIFICATION\n")
    
    # Check model conflicts
    if not check_model_conflicts():
        print("❌ Model conflict check failed")
        return False
    
    # Check agent imports
    agent_imports = check_agent_imports()
    
    # Check frontend integration
    check_frontend_integration()
    
    print("\n=== VERIFICATION COMPLETE ===")
    return True

if __name__ == "__main__":
    main()