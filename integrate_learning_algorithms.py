#!/usr/bin/env python3
"""
Learning Algorithms Integration Script
Adds the missing methods to the PredictiveAnalyticsService

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
import sys
import django

# Setup Django environment
sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🚀 Integrating Learning Algorithms with PredictiveAnalyticsService...")

try:
    # Import the services
    from complete_learning_algorithms_implementation import (
        LearningVelocityAnalyzer,
        EngagementPatternAnalyzer, 
        SuccessProbabilityPredictor,
        CompletionTimePredictor,
        RetentionRiskAssessor,
        KnowledgeGapDetector,
        AdaptiveFeedbackGenerator,
        integrate_learning_algorithms
    )
    
    # Run integration
    integrate_learning_algorithms()
    
    print("✅ Successfully integrated all learning algorithms!")
    
    # Test the integration
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    
    service = PredictiveAnalyticsService()
    
    # Test if methods are available
    test_methods = [
        'analyze_learning_velocity',
        'analyze_engagement_patterns', 
        'predict_success_probability',
        'predict_completion_time',
        'assess_retention_risk',
        'detect_knowledge_gaps',
        'generate_adaptive_feedback'
    ]
    
    print("\n📋 Integration Test Results:")
    print("-" * 40)
    
    for method_name in test_methods:
        if hasattr(service, method_name):
            print(f"✅ {method_name}: Successfully integrated")
        else:
            print(f"❌ {method_name}: Integration failed")
    
    print(f"\n🎉 Learning Algorithms Integration Complete!")
    print(f"Total methods integrated: {sum(1 for method in test_methods if hasattr(service, method))}/{len(test_methods)}")
    
except Exception as e:
    print(f"❌ Integration failed: {e}")
    import traceback
    traceback.print_exc()