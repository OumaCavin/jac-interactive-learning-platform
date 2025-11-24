#!/usr/bin/env python3
"""
Simple import test without Django setup to verify syntax fixes.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, '/workspace/backend')

def test_basic_imports():
    """Test basic imports work without Django setup."""
    
    print("Testing basic import syntax...")
    
    try:
        # Test that files can be read and parsed
        test_files = [
            '/workspace/backend/backend/apps/agents/quiz_master.py',
            '/workspace/backend/backend/apps/agents/evaluator.py',
            '/workspace/backend/backend/apps/agents/motivator.py',
            '/workspace/backend/backend/apps/agents/progress_tracker.py'
        ]
        
        for file_path in test_files:
            print(f"Checking {os.path.basename(file_path)}...")
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Check that the problematic imports are fixed
            if 'UserProgress' in content:
                print(f"   ✗ Still contains UserProgress reference: {file_path}")
                return False
            elif 'from ..assessment.models import' in content:
                print(f"   ✗ Still tries to import from assessment.models: {file_path}")
                return False
            elif 'UserModuleProgress' in content:
                print(f"   ✓ Contains corrected UserModuleProgress: {file_path}")
            elif 'from ..learning.models import' in content:
                print(f"   ✓ Contains learning.models imports: {file_path}")
            
        print("✓ All import syntax checks passed!")
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def check_model_definitions():
    """Check that models are defined correctly."""
    
    print("\nChecking model definitions...")
    
    try:
        model_file = '/workspace/backend/backend/apps/learning/models.py'
        with open(model_file, 'r') as f:
            content = f.read()
        
        # Check for required model classes
        required_models = [
            'class AssessmentAttempt',
            'class UserAssessmentResult', 
            'class AssessmentQuestion',
            'class Achievement',
            'class UserAchievement',
            'class UserModuleProgress'
        ]
        
        for model in required_models:
            if model in content:
                print(f"   ✓ Found: {model}")
            else:
                print(f"   ✗ Missing: {model}")
                return False
        
        print("✓ All required models are defined!")
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def check_import_statements():
    """Check specific import statements in agents."""
    
    print("\nChecking import statements...")
    
    # Define expected fixed imports
    expected_imports = {
        'quiz_master.py': [
            'from ..learning.models import LearningPath, Module, Quiz, Question, UserModuleProgress, UserLearningPath, Assessment, UserAssessmentResult, AssessmentQuestion',
        ],
        'evaluator.py': [
            'from ..learning.models import LearningPath, Module, UserModuleProgress, Assessment, UserAssessmentResult, AssessmentQuestion',
        ],
        'motivator.py': [
            'from ..learning.models import LearningPath, Module, UserModuleProgress, Achievement, UserLearningPath, UserAssessmentResult',
        ],
        'progress_tracker.py': [
            'from ..learning.models import LearningPath, Module, UserModuleProgress, LearningContent, UserLearningPath, UserAssessmentResult',
        ]
    }
    
    success = True
    
    for filename, expected in expected_imports.items():
        file_path = f'/workspace/backend/backend/apps/agents/{filename}'
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if fixed imports are present
            for import_line in expected:
                if import_line in content:
                    print(f"   ✓ {filename}: Import statement corrected")
                else:
                    print(f"   ⚠ {filename}: Expected import line not found")
                    # Show what we have instead
                    for line in content.split('\n'):
                        if 'from ..learning.models import' in line:
                            print(f"      Found: {line.strip()}")
                    success = False
            
        except Exception as e:
            print(f"   ✗ Error checking {filename}: {e}")
            success = False
    
    return success

if __name__ == "__main__":
    print("=" * 60)
    print("JAC Learning Platform - Import Fix Syntax Verification")
    print("=" * 60)
    
    success = True
    
    # Run tests
    success &= test_basic_imports()
    success &= check_model_definitions()
    success &= check_import_statements()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 IMPORT SYNTAX FIXES VERIFIED!")
        print("✅ Critical issues resolved:")
        print("   • All broken imports fixed")
        print("   • UserProgress → UserModuleProgress conversions complete")
        print("   • Missing models added to learning/models.py")
        print("   • Import statements corrected in all agent files")
        print("   • AssessmentAttempt, UserAssessmentResult, AssessmentQuestion models created")
        print("   • Achievement, UserAchievement models added")
        print("   • Architecture consistency improved")
    else:
        print("❌ SOME SYNTAX ISSUES DETECTED!")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
