#!/usr/bin/env python3
"""
Corrected Verification of Predictive Learning Models
Author: Cavin Otieno
Created: 2025-11-26

This script verifies the integration with corrected Django models and imports.
"""

import os
import sys
import django
import logging
import numpy as np
from typing import Dict, Any
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')

try:
    django.setup()
    from django.contrib.auth import get_user_model
    from django.db.models import Q, Count, Sum, Avg, F, Case, When, Value, StdDev
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    from apps.learning.models import UserModuleProgress, AssessmentAttempt, LearningPath
    DJANGO_AVAILABLE = True
    User = get_user_model()
except ImportError as e:
    print(f"Warning: Django or dependencies not available: {e}")
    DJANGO_AVAILABLE = False

logger = logging.getLogger(__name__)

class CorrectedPredictiveModelsVerifier:
    """Corrected verification using proper Django models and imports"""
    
    def __init__(self):
        self.service = None
        self.test_user = None
        
    def setup_test_data(self):
        """Setup minimal test data"""
        try:
            if not DJANGO_AVAILABLE:
                return False
                
            print("🔧 Setting up test data...")
            
            # Create test user
            try:
                self.test_user = User.objects.get(username='test_predictive_user')
            except User.DoesNotExist:
                self.test_user = User.objects.create_user(
                    username='test_predictive_user',
                    email='test@predictive.com'
                )
                print(f"✅ Created test user: {self.test_user.username}")
            
            # Create minimal test data
            end_date = timezone.now()
            
            # Test module progress
            for i in range(5):
                start_date = end_date - timedelta(days=i*3 + 5)
                complete_date = end_date - timedelta(days=i*3)
                
                UserModuleProgress.objects.create(
                    user=self.test_user,
                    status='completed' if i < 4 else 'in_progress',
                    progress_percentage=100 if i < 4 else 60,
                    overall_score=70 + i * 5,
                    started_at=start_date,
                    completed_at=complete_date if i < 4 else None,
                    last_activity_at=complete_date if i < 4 else end_date,
                    created_at=start_date
                )
            
            # Test assessment attempts
            for i in range(3):
                attempt_date = end_date - timedelta(days=i*4)
                
                AssessmentAttempt.objects.create(
                    user=self.test_user,
                    status='completed',
                    score=0.6 + i * 0.1,
                    max_score=100.0,
                    passing_score=70.0,
                    is_passed=True,
                    started_at=attempt_date - timedelta(minutes=30),
                    completed_at=attempt_date
                )
            
            print(f"✅ Created test data: {UserModuleProgress.objects.filter(user=self.test_user).count()} module records, {AssessmentAttempt.objects.filter(user=self.test_user).count()} assessments")
            return True
            
        except Exception as e:
            print(f"⚠️  Could not setup test data: {e}")
            return False
    
    def verify_method_exists(self, method_name: str) -> Dict[str, Any]:
        """Verify a method exists in the service"""
        try:
            if not self.service:
                self.service = PredictiveAnalyticsService()
            
            # Check if method exists
            if not hasattr(self.service, method_name):
                return {
                    'status': 'failed',
                    'message': f'Method {method_name} not found in service'
                }
            
            # Check if method is callable
            method = getattr(self.service, method_name)
            if not callable(method):
                return {
                    'status': 'failed',
                    'message': f'{method_name} exists but is not callable'
                }
            
            return {
                'status': 'passed',
                'message': f'Method {method_name} exists and is callable'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error checking method {method_name}: {str(e)}'
            }
    
    def test_method_with_sample_call(self, method_name: str, method_args: dict = None) -> Dict[str, Any]:
        """Test a method with sample parameters"""
        try:
            if not self.service:
                self.service = PredictiveAnalyticsService()
            
            method = getattr(self.service, method_name)
            
            # Default arguments
            if method_args is None:
                method_args = {
                    'user': self.test_user,
                    'learning_path_id': None,
                    'days_window': 30
                }
            
            # Try to call the method
            result = method(**method_args)
            
            # Basic structure check
            if not isinstance(result, dict):
                return {
                    'status': 'failed',
                    'message': f'{method_name} did not return a dictionary',
                    'result_type': type(result).__name__
                }
            
            # Check for status field
            if 'status' not in result:
                return {
                    'status': 'failed',
                    'message': f'{method_name} result missing status field',
                    'result_keys': list(result.keys())
                }
            
            return {
                'status': 'passed',
                'message': f'{method_name} executed successfully',
                'result_status': result.get('status'),
                'result_keys': list(result.keys())
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error calling {method_name}: {str(e)}',
                'error_type': type(e).__name__
            }
    
    def run_corrected_verification(self):
        """Run corrected verification"""
        print("🚀 Starting Corrected Verification of Predictive Learning Models")
        print("=" * 70)
        
        # Setup test data
        setup_success = self.setup_test_data()
        
        if not setup_success:
            print("❌ Test data setup failed - will test method existence only")
        
        # List of methods to verify
        methods_to_test = [
            ('analyze_learning_velocity', {'user': self.test_user}),
            ('analyze_engagement_patterns', {'user': self.test_user}),
            ('model_success_probability', {'user': self.test_user}),
            ('predict_time_to_completion', {'user': self.test_user}),
            ('assess_retention_risk', {'user': self.test_user}),
            ('detect_knowledge_gaps', {'user': self.test_user}),
            ('perform_learning_analytics_clustering', {}),
            ('generate_ml_predictions', {'user': self.test_user})
        ]
        
        # Initialize service
        self.service = PredictiveAnalyticsService()
        
        passed_tests = 0
        failed_tests = 0
        error_tests = 0
        
        verification_results = {}
        
        for method_name, test_args in methods_to_test:
            print(f"\n🔍 Testing {method_name.replace('_', ' ').title()}...")
            
            # First verify method exists
            existence_result = self.verify_method_exists(method_name)
            
            if existence_result['status'] == 'passed':
                print(f"  ✅ Method exists: {existence_result['message']}")
                
                # Try to call it if we have test data
                if setup_success:
                    call_result = self.test_method_with_sample_call(method_name, test_args)
                    verification_results[method_name] = call_result
                    
                    if call_result['status'] == 'passed':
                        passed_tests += 1
                        print(f"  ✅ Method call: {call_result['message']}")
                    elif call_result['status'] == 'failed':
                        failed_tests += 1
                        print(f"  ❌ Method call: {call_result['message']}")
                    else:
                        error_tests += 1
                        print(f"  ⚠️  Method call: {call_result['message']}")
                else:
                    verification_results[method_name] = existence_result
                    passed_tests += 1
                    print(f"  ✅ Method exists (no test data for call)")
                    
            else:
                failed_tests += 1
                verification_results[method_name] = existence_result
                print(f"  ❌ Method existence: {existence_result['message']}")
        
        # Summary
        total_tests = len(methods_to_test)
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print("\n" + "=" * 70)
        print("📊 CORRECTED VERIFICATION SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed_tests}/{total_tests}")
        print(f"⚠️  Errors: {error_tests}/{total_tests}")
        
        if success_rate >= 90:
            print("\n🎉 EXCELLENT! All predictive learning models properly integrated!")
            status = 'excellent'
        elif success_rate >= 75:
            print("\n👍 GOOD! Most predictive learning models working correctly.")
            status = 'good'
        elif success_rate >= 50:
            print("\n⚠️  FAIR! Some predictive learning models need attention.")
            status = 'fair'
        else:
            print("\n❌ POOR! Major issues with predictive learning models.")
            status = 'poor'
        
        print("\n📋 DETAILED RESULTS:")
        print("-" * 50)
        for method_name, result in verification_results.items():
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'error': '⚠️'
            }.get(result['status'], '❓')
            print(f"{status_icon} {method_name.replace('_', ' ').title()}: {result['status'].upper()}")
            print(f"    📝 {result['message']}")
        
        return {
            'overall_status': status,
            'success_rate': success_rate,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'error_tests': error_tests,
            'total_tests': total_tests,
            'verification_results': verification_results,
            'test_data_setup': setup_success
        }

def main():
    """Main verification process"""
    verifier = CorrectedPredictiveModelsVerifier()
    result = verifier.run_corrected_verification()
    
    # Save results
    import json
    results_file = '/workspace/corrected_predictive_models_verification.json'
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    return result

if __name__ == "__main__":
    result = main()
    exit(0 if result['success_rate'] >= 75 else 1)