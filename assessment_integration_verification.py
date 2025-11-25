#!/usr/bin/env python3
"""
Assessment Integration Verification Script
Author: Cavin Otieno
Date: 2025-11-25

This script verifies the assessment frontend-to-backend integration.
"""

import os
import json
import re
from typing import Dict, List, Any

class AssessmentIntegrationVerifier:
    def __init__(self):
        self.workspace_path = '/workspace'
        self.frontend_path = '/workspace/frontend/src'
        self.results = []
        
    def log_result(self, category: str, test: str, status: str, details: str = ""):
        """Log verification result"""
        result = {
            'category': category,
            'test': test,
            'status': status,
            'details': details
        }
        self.results.append(result)
        
        status_colors = {
            'PASS': '✅',
            'FAIL': '❌',
            'INFO': 'ℹ️',
            'WARN': '⚠️'
        }
        
        icon = status_colors.get(status, '❓')
        print(f"{icon} [{status}] {category}: {test}")
        if details:
            print(f"    → {details}")
    
    def verify_assessment_detail_integration(self):
        """Verify AssessmentDetail.tsx backend integration"""
        print("\n🔍 Verifying AssessmentDetail.tsx Integration...")
        
        detail_file = os.path.join(self.frontend_path, 'pages', 'assessments', 'AssessmentDetail.tsx')
        
        if os.path.exists(detail_file):
            with open(detail_file, 'r') as f:
                content = f.read()
            
            # Check for mock data removal
            if 'mockQuiz' not in content:
                self.log_result('AssessmentDetail', 'Mock Data Removal', 'PASS', 'No mock data found')
            else:
                self.log_result('AssessmentDetail', 'Mock Data Removal', 'FAIL', 'Still contains mock data')
            
            # Check for API integration
            if 'learningService.getQuiz' in content:
                self.log_result('AssessmentDetail', 'Quiz API Integration', 'PASS', 'Uses learningService.getQuiz')
            else:
                self.log_result('AssessmentDetail', 'Quiz API Integration', 'FAIL', 'No quiz API integration')
            
            # Check for attempt management
            if 'startQuizAttempt' in content:
                self.log_result('AssessmentDetail', 'Attempt Management', 'PASS', 'Uses startQuizAttempt')
            else:
                self.log_result('AssessmentDetail', 'Attempt Management', 'FAIL', 'No attempt management')
            
            # Check for submission handling
            if 'submitQuizAttempt' in content:
                self.log_result('AssessmentDetail', 'Submission Handling', 'PASS', 'Uses submitQuizAttempt')
            else:
                self.log_result('AssessmentDetail', 'Submission Handling', 'FAIL', 'No submission handling')
            
            # Check for error handling
            if 'error' in content and 'try' in content:
                self.log_result('AssessmentDetail', 'Error Handling', 'PASS', 'Has error handling')
            else:
                self.log_result('AssessmentDetail', 'Error Handling', 'WARN', 'Error handling check needed')
            
            # Check for loading states
            if 'loading' in content and 'setLoading' in content:
                self.log_result('AssessmentDetail', 'Loading States', 'PASS', 'Has loading state management')
            else:
                self.log_result('AssessmentDetail', 'Loading States', 'WARN', 'Loading states check needed')
        else:
            self.log_result('AssessmentDetail', 'File Existence', 'FAIL', 'AssessmentDetail.tsx not found')
    
    def verify_assessments_overview_integration(self):
        """Verify Assessments.tsx (overview) integration"""
        print("\n🔍 Verifying Assessments.tsx Integration...")
        
        overview_file = os.path.join(self.frontend_path, 'pages', 'assessments', 'Assessments.tsx')
        
        if os.path.exists(overview_file):
            with open(overview_file, 'r') as f:
                content = f.read()
            
            # Check for Redux integration
            if 'fetchQuizzes' in content and 'fetchUserAttempts' in content:
                self.log_result('AssessmentsOverview', 'Redux Integration', 'PASS', 'Uses Redux async thunks')
            else:
                self.log_result('AssessmentsOverview', 'Redux Integration', 'FAIL', 'Missing Redux integration')
            
            # Check for service integration
            if 'learningService' in content:
                self.log_result('AssessmentsOverview', 'Service Integration', 'PASS', 'Uses learningService')
            else:
                self.log_result('AssessmentsOverview', 'Service Integration', 'FAIL', 'No service integration')
            
            # Check for real data usage
            if 'useSelector' in content and 'selectQuizzes' in content:
                self.log_result('AssessmentsOverview', 'Real Data Usage', 'PASS', 'Uses Redux selectors')
            else:
                self.log_result('AssessmentsOverview', 'Real Data Usage', 'WARN', 'Real data usage check needed')
        else:
            self.log_result('AssessmentsOverview', 'File Existence', 'FAIL', 'Assessments.tsx not found')
    
    def verify_learning_service_enhancements(self):
        """Verify learningService.ts assessment methods"""
        print("\n🔍 Verifying LearningService Assessment Methods...")
        
        service_file = os.path.join(self.frontend_path, 'services', 'learningService.ts')
        
        if os.path.exists(service_file):
            with open(service_file, 'r') as f:
                content = f.read()
            
            # Check for assessment methods
            assessment_methods = [
                'getQuizzes',
                'getQuiz',
                'startQuizAttempt', 
                'getUserAttempts',
                'submitAttempt',
                'getAssessmentStats'
            ]
            
            found_methods = []
            for method in assessment_methods:
                if method in content:
                    found_methods.append(method)
            
            if len(found_methods) == len(assessment_methods):
                self.log_result('LearningService', 'Assessment Methods', 'PASS', f'All {len(found_methods)} methods found')
            else:
                self.log_result('LearningService', 'Assessment Methods', 'WARN', 
                              f'Found {len(found_methods)}/{len(assessment_methods)} methods: {found_methods}')
            
            # Check for enhanced assessment APIs
            enhanced_apis = [
                'getAssessmentQuestions',
                'getAssessmentAttempt', 
                'checkAssessmentAnswer'
            ]
            
            enhanced_found = []
            for api in enhanced_apis:
                if api in content:
                    enhanced_found.append(api)
            
            if enhanced_found:
                self.log_result('LearningService', 'Enhanced Assessment APIs', 'PASS', 
                              f'Found enhanced APIs: {enhanced_found}')
            else:
                self.log_result('LearningService', 'Enhanced Assessment APIs', 'INFO', 
                              'No enhanced assessment APIs found')
        else:
            self.log_result('LearningService', 'File Existence', 'FAIL', 'learningService.ts not found')
    
    def verify_redux_integration(self):
        """Verify Redux assessment slice integration"""
        print("\n🔍 Verifying Redux Assessment Integration...")
        
        slice_file = os.path.join(self.frontend_path, 'store', 'slices', 'assessmentSlice.ts')
        
        if os.path.exists(slice_file):
            with open(slice_file, 'r') as f:
                content = f.read()
            
            # Check for async thunks
            async_thunks = [
                'fetchQuizzes',
                'fetchUserAttempts', 
                'startQuizAttempt',
                'submitQuizAttempt',
                'fetchAssessmentStats'
            ]
            
            found_thunks = []
            for thunk in async_thunks:
                if thunk in content:
                    found_thunks.append(thunk)
            
            if len(found_thunks) == len(async_thunks):
                self.log_result('Redux', 'Assessment Async Thunks', 'PASS', f'All {len(found_thunks)} thunks found')
            else:
                self.log_result('Redux', 'Assessment Async Thunks', 'WARN', 
                              f'Found {len(found_thunks)}/{len(async_thunks)} thunks: {found_thunks}')
            
            # Check for service integration
            if 'learningService' in content:
                self.log_result('Redux', 'Service Integration', 'PASS', 'Integrates with learningService')
            else:
                self.log_result('Redux', 'Service Integration', 'FAIL', 'No service integration found')
        else:
            self.log_result('Redux', 'File Existence', 'FAIL', 'assessmentSlice.ts not found')
    
    def verify_backend_api_compatibility(self):
        """Verify backend API structure"""
        print("\n🔍 Verifying Backend API Compatibility...")
        
        # Check backend assessment views
        views_file = os.path.join(self.workspace_path, 'backend', 'apps', 'assessments', 'views.py')
        urls_file = os.path.join(self.workspace_path, 'backend', 'apps', 'assessments', 'urls.py')
        
        backend_score = 0
        total_checks = 4
        
        if os.path.exists(views_file):
            with open(views_file, 'r') as f:
                content = f.read()
            
            # Check for key views
            if 'AssessmentQuestionViewSet' in content:
                self.log_result('Backend', 'Question ViewSet', 'PASS', 'AssessmentQuestionViewSet found')
                backend_score += 1
            else:
                self.log_result('Backend', 'Question ViewSet', 'FAIL', 'AssessmentQuestionViewSet not found')
            
            if 'AssessmentAttemptViewSet' in content:
                self.log_result('Backend', 'Attempt ViewSet', 'PASS', 'AssessmentAttemptViewSet found')
                backend_score += 1
            else:
                self.log_result('Backend', 'Attempt ViewSet', 'FAIL', 'AssessmentAttemptViewSet not found')
            
            # Check for API methods
            if 'submit' in content and 'start' in content:
                self.log_result('Backend', 'Attempt Methods', 'PASS', 'Submit and start methods found')
                backend_score += 1
            else:
                self.log_result('Backend', 'Attempt Methods', 'FAIL', 'Missing submit/start methods')
        else:
            self.log_result('Backend', 'Views File', 'FAIL', 'views.py not found')
        
        if os.path.exists(urls_file):
            with open(urls_file, 'r') as f:
                content = f.read()
            
            if 'questions' in content and 'attempts' in content:
                self.log_result('Backend', 'URL Routing', 'PASS', 'Questions and attempts endpoints configured')
                backend_score += 1
            else:
                self.log_result('Backend', 'URL Routing', 'FAIL', 'Missing endpoint configuration')
        else:
            self.log_result('Backend', 'URLs File', 'FAIL', 'urls.py not found')
        
        if backend_score == total_checks:
            self.log_result('Backend', 'Overall Compatibility', 'PASS', f'Score: {backend_score}/{total_checks}')
        else:
            self.log_result('Backend', 'Overall Compatibility', 'WARN', f'Score: {backend_score}/{total_checks}')
    
    def generate_assessment_integration_report(self):
        """Generate comprehensive assessment integration report"""
        print("\n" + "="*80)
        print("ASSESSMENT INTEGRATION VERIFICATION SUMMARY")
        print("="*80)
        
        # Count results by status
        status_counts = {}
        for result in self.results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total_tests = len(self.results)
        print(f"Total Checks: {total_tests}")
        print(f"✅ Passed: {status_counts.get('PASS', 0)}")
        print(f"❌ Failed: {status_counts.get('FAIL', 0)}")
        print(f"⚠️  Warnings: {status_counts.get('WARN', 0)}")
        print(f"ℹ️  Info: {status_counts.get('INFO', 0)}")
        
        # Calculate success rate
        passed = status_counts.get('PASS', 0)
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Category breakdown
        print("\n" + "="*80)
        print("CATEGORY BREAKDOWN")
        print("="*80)
        
        categories = {}
        for result in self.results:
            category = result['category']
            if category not in categories:
                categories[category] = {'PASS': 0, 'FAIL': 0, 'WARN': 0, 'INFO': 0}
            categories[category][result['status']] += 1
        
        for category, counts in categories.items():
            total_cat = sum(counts.values())
            passed_cat = counts.get('PASS', 0)
            cat_rate = (passed_cat / total_cat * 100) if total_cat > 0 else 0
            
            print(f"\n{category}:")
            print(f"  Total: {total_cat}, Passed: {passed_cat}, Success Rate: {cat_rate:.1f}%")
        
        # Save detailed report
        report_data = {
            'summary': {
                'total_tests': total_tests,
                'passed': status_counts.get('PASS', 0),
                'failed': status_counts.get('FAIL', 0),
                'warnings': status_counts.get('WARN', 0),
                'info': status_counts.get('INFO', 0),
                'success_rate': success_rate
            },
            'categories': categories,
            'detailed_results': self.results,
            'assessment_integration_status': 'COMPLETE' if success_rate >= 80 else 'INCOMPLETE'
        }
        
        report_file = os.path.join(self.workspace_path, 'assessment_integration_verification_report.json')
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Final assessment
        print("\n" + "="*80)
        print("ASSESSMENT INTEGRATION ASSESSMENT")
        print("="*80)
        
        if success_rate >= 90:
            print("✅ EXCELLENT: Assessment integration is highly successful")
        elif success_rate >= 75:
            print("✅ GOOD: Assessment integration is mostly complete")  
        else:
            print("⚠️  NEEDS ATTENTION: Some integration issues require resolution")
        
        failed_tests = [r for r in self.results if r['status'] == 'FAIL']
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  - {test['category']}: {test['test']}")
        
        warn_tests = [r for r in self.results if r['status'] == 'WARN']
        if warn_tests:
            print(f"\n⚠️  Warnings ({len(warn_tests)}):")
            for test in warn_tests:
                print(f"  - {test['category']}: {test['test']}")

def main():
    """Main verification function"""
    print("="*80)
    print("ASSESSMENT FRONTEND-TO-BACKEND INTEGRATION VERIFICATION")
    print("Author: Cavin Otieno")
    print("Date: 2025-11-25")
    print("="*80)
    
    verifier = AssessmentIntegrationVerifier()
    
    # Run verifications
    verifier.verify_assessment_detail_integration()
    verifier.verify_assessments_overview_integration()
    verifier.verify_learning_service_enhancements()
    verifier.verify_redux_integration()
    verifier.verify_backend_api_compatibility()
    
    # Generate report
    verifier.generate_assessment_integration_report()
    
    print("\n" + "="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
