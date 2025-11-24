#!/usr/bin/env python3
"""
Test script to verify that agent import fixes work correctly.
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, '/workspace/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_learning_platform.settings')

import django
django.setup()

def test_imports():
    """Test that all agent imports work correctly after fixes."""
    
    print("Testing agent imports...")
    
    try:
        # Test quiz_master.py import
        print("1. Testing Quiz Master Agent import...")
        from backend.apps.agents.quiz_master import QuizMasterAgent
        print("   ✓ QuizMasterAgent imported successfully")
        
        # Test evaluator.py import
        print("2. Testing Evaluator Agent import...")
        from backend.apps.agents.evaluator import EvaluatorAgent
        print("   ✓ EvaluatorAgent imported successfully")
        
        # Test motivator.py import
        print("3. Testing Motivator Agent import...")
        from backend.apps.agents.motivator import MotivatorAgent
        print("   ✓ MotivatorAgent imported successfully")
        
        # Test progress_tracker.py import
        print("4. Testing Progress Tracker Agent import...")
        from backend.apps.agents.progress_tracker import ProgressTrackerAgent
        print("   ✓ ProgressTrackerAgent imported successfully")
        
        print("\n✓ All agent imports successful!")
        return True
        
    except ImportError as e:
        print(f"   ✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

def test_model_imports():
    """Test that all model imports work correctly."""
    
    print("\nTesting model imports...")
    
    try:
        # Test learning models
        print("1. Testing Learning Models import...")
        from backend.apps.learning.models import (
            UserModuleProgress, 
            UserLearningPath, 
            Assessment, 
            Question,
            AssessmentAttempt,
            UserAssessmentResult,
            AssessmentQuestion,
            Achievement,
            UserAchievement
        )
        print("   ✓ All learning models imported successfully")
        
        print("\n✓ All model imports successful!")
        return True
        
    except ImportError as e:
        print(f"   ✗ Model import error: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

def test_agent_instantiation():
    """Test that agents can be instantiated without errors."""
    
    print("\nTesting agent instantiation...")
    
    try:
        # Test agent instantiation
        from backend.apps.agents.quiz_master import QuizMasterAgent
        from backend.apps.agents.evaluator import EvaluatorAgent
        from backend.apps.agents.motivator import MotivatorAgent
        from backend.apps.agents.progress_tracker import ProgressTrackerAgent
        
        agents = [
            ("QuizMasterAgent", QuizMasterAgent),
            ("EvaluatorAgent", EvaluatorAgent),
            ("MotivatorAgent", MotivatorAgent),
            ("ProgressTrackerAgent", ProgressTrackerAgent)
        ]
        
        for name, agent_class in agents:
            print(f"   Testing {name}...")
            agent = agent_class()
            print(f"   ✓ {name} instantiated successfully")
            print(f"     - Agent ID: {agent.agent_id}")
            print(f"     - Agent Type: {agent.agent_type}")
            print(f"     - Status: {agent.status}")
        
        print("\n✓ All agents instantiated successfully!")
        return True
        
    except Exception as e:
        print(f"   ✗ Agent instantiation error: {e}")
        return False

def test_agent_capabilities():
    """Test that agent capabilities methods work."""
    
    print("\nTesting agent capabilities...")
    
    try:
        from backend.apps.agents.quiz_master import QuizMasterAgent
        
        agent = QuizMasterAgent()
        capabilities = agent.get_capabilities()
        specialization = agent.get_specialization_info()
        
        print(f"   ✓ Agent capabilities retrieved:")
        print(f"     - Capabilities count: {len(capabilities)}")
        print(f"     - Agent type: {specialization['agent_type']}")
        print(f"     - Key responsibilities: {len(specialization['key_responsibilities'])}")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Capabilities test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("JAC Learning Platform - Agent Import Fix Verification")
    print("=" * 60)
    
    success = True
    
    # Run all tests
    success &= test_imports()
    success &= test_model_imports()
    success &= test_agent_instantiation()
    success &= test_agent_capabilities()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Agent imports and models are working correctly.")
        print("✅ The critical issues have been fixed:")
        print("   • Fixed broken imports in all agent files")
        print("   • Corrected UserProgress → UserModuleProgress references")
        print("   • Added missing model imports")
        print("   • Created AssessmentAttempt, UserAssessmentResult, AssessmentQuestion models")
        print("   • Added Achievement and UserAchievement models")
        print("   • All agents can be instantiated and used")
    else:
        print("❌ SOME TESTS FAILED! There may still be issues to resolve.")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
