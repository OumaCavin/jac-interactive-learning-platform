#!/usr/bin/env python3
"""
Frontend-to-Backend Integration Test Suite
Author: Cavin Otieno
Date: 2025-11-25

This script tests the integration between frontend services and backend APIs.
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

class APIIntegrationTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results"""
        result = {
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        
        # Color coding for terminal output
        status_colors = {
            'PASS': '\033[92m',  # Green
            'FAIL': '\033[91m',  # Red
            'SKIP': '\033[93m',  # Yellow
            'INFO': '\033[94m'   # Blue
        }
        color = status_colors.get(status, '')
        reset = '\033[0m'
        
        print(f"{color}[{status}]{reset} {test_name}")
        if details:
            print(f"    → {details}")
    
    def test_backend_availability(self) -> bool:
        """Test if backend server is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/health/", timeout=5)
            if response.status_code == 200:
                self.log_test("Backend Server Availability", "PASS", "Server is running and responding")
                return True
            else:
                self.log_test("Backend Server Availability", "FAIL", f"Server responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            self.log_test("Backend Server Availability", "FAIL", f"Cannot connect to server: {str(e)}")
            return False
    
    def test_user_settings_api(self) -> bool:
        """Test UserSettings API endpoints"""
        print("\n=== Testing UserSettings API ===")
        
        # Test GET /api/users/settings/
        try:
            response = self.session.get(f"{self.base_url}/api/users/settings/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("GET /api/users/settings/", "PASS", f"Settings retrieved successfully")
                
                # Verify expected fields
                expected_fields = [
                    'email', 'bio', 'first_name', 'last_name',
                    'learning_style', 'preferred_difficulty', 'learning_pace',
                    'current_goal', 'goal_deadline',
                    'agent_interaction_level', 'preferred_feedback_style',
                    'dark_mode', 'notifications_enabled', 'email_notifications', 'push_notifications'
                ]
                
                missing_fields = [field for field in expected_fields if field not in data]
                if not missing_fields:
                    self.log_test("Settings Fields Validation", "PASS", "All expected fields present")
                else:
                    self.log_test("Settings Fields Validation", "FAIL", f"Missing fields: {missing_fields}")
                
                return True
            elif response.status_code == 401:
                self.log_test("GET /api/users/settings/", "INFO", "Authentication required (expected for unauthenticated requests)")
                return True
            else:
                self.log_test("GET /api/users/settings/", "FAIL", f"Status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("GET /api/users/settings/", "FAIL", f"Request failed: {str(e)}")
            return False
    
    def test_api_endpoints_structure(self) -> bool:
        """Test API endpoints structure and routing"""
        endpoints_to_test = [
            "/api/users/",
            "/api/users/settings/",
            "/api/learning/",
            "/api/assessments/",
            "/api/search/",
            "/api/agents/"
        ]
        
        print("\n=== Testing API Endpoint Structure ===")
        
        for endpoint in endpoints_to_test:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code in [200, 401, 403]:  # Valid responses
                    self.log_test(f"Endpoint: {endpoint}", "PASS", f"Status: {response.status_code}")
                elif response.status_code == 404:
                    self.log_test(f"Endpoint: {endpoint}", "FAIL", "Endpoint not found")
                else:
                    self.log_test(f"Endpoint: {endpoint}", "INFO", f"Unexpected status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.log_test(f"Endpoint: {endpoint}", "FAIL", f"Request failed: {str(e)}")
        
        return True
    
    def test_service_imports(self) -> bool:
        """Test frontend service imports and basic structure"""
        print("\n=== Testing Frontend Service Integration ===")
        
        # Read service files and verify they exist and have proper structure
        service_files = [
            'authService.ts',
            'settingsService.ts', 
            'learningService.ts',
            'searchService.ts',
            'assessmentService.ts'
        ]
        
        import os
        services_path = '/workspace/frontend/src/services'
        
        for service_file in service_files:
            file_path = os.path.join(services_path, service_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Check for API client import
                    if 'import' in content and 'apiClient' in content:
                        self.log_test(f"Service Import: {service_file}", "PASS", "Has proper API client integration")
                    else:
                        self.log_test(f"Service Import: {service_file}", "INFO", "API client integration check needed")
                        
                    # Check for async methods
                    if 'async' in content:
                        self.log_test(f"Service Methods: {service_file}", "PASS", "Contains async methods")
                    else:
                        self.log_test(f"Service Methods: {service_file}", "INFO", "No async methods found")
                        
                except Exception as e:
                    self.log_test(f"Service Analysis: {service_file}", "FAIL", f"Cannot read file: {str(e)}")
            else:
                self.log_test(f"Service File: {service_file}", "FAIL", "File not found")
        
        return True
    
    def test_redux_integration(self) -> bool:
        """Test Redux store and slice integration"""
        print("\n=== Testing Redux Store Integration ===")
        
        import os
        store_path = '/workspace/frontend/src/store'
        
        # Check store configuration
        store_file = os.path.join(store_path, 'store.ts')
        if os.path.exists(store_file):
            try:
                with open(store_file, 'r') as f:
                    content = f.read()
                    
                # Check for all slice imports
                expected_slices = [
                    'authReducer', 'uiReducer', 'learningReducer',
                    'assessmentReducer', 'agentReducer', 'adminReducer', 'searchReducer'
                ]
                
                missing_slices = []
                for slice_name in expected_slices:
                    if slice_name not in content:
                        missing_slices.append(slice_name)
                
                if not missing_slices:
                    self.log_test("Redux Store Configuration", "PASS", "All slices properly imported")
                else:
                    self.log_test("Redux Store Configuration", "FAIL", f"Missing slices: {missing_slices}")
                    
            except Exception as e:
                self.log_test("Redux Store Analysis", "FAIL", f"Cannot read store file: {str(e)}")
        else:
            self.log_test("Redux Store Configuration", "FAIL", "Store file not found")
        
        # Check individual slices
        slices_path = os.path.join(store_path, 'slices')
        if os.path.exists(slices_path):
            slice_files = [f for f in os.listdir(slices_path) if f.endswith('.ts')]
            self.log_test("Redux Slices Count", "INFO", f"Found {len(slice_files)} slice files")
            
            for slice_file in slice_files:
                file_path = os.path.join(slices_path, slice_file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Check for service integration
                    if 'createAsyncThunk' in content and 'services' in content:
                        self.log_test(f"Slice Integration: {slice_file}", "PASS", "Has async thunks and service integration")
                    else:
                        self.log_test(f"Slice Integration: {slice_file}", "INFO", "Service integration check needed")
                        
                except Exception as e:
                    self.log_test(f"Slice Analysis: {slice_file}", "FAIL", f"Cannot read file: {str(e)}")
        
        return True
    
    def test_utils_integration(self) -> bool:
        """Test utility functions integration"""
        print("\n=== Testing Utils Integration ===")
        
        import os
        utils_path = '/workspace/frontend/src/utils'
        
        if os.path.exists(utils_path):
            utils_files = [f for f in os.listdir(utils_path) if f.endswith('.ts')]
            
            for utils_file in utils_files:
                file_path = os.path.join(utils_path, utils_file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Check for utility functions
                    function_count = content.count('export')
                    self.log_test(f"Utils Analysis: {utils_file}", "INFO", f"Contains {function_count} exports")
                    
                    # Check for specific utility types
                    if 'admin' in utils_file.lower():
                        if any(keyword in content for keyword in ['calculate', 'format', 'generate', 'export']):
                            self.log_test(f"Admin Utils: {utils_file}", "PASS", "Contains administrative utilities")
                        else:
                            self.log_test(f"Admin Utils: {utils_file}", "INFO", "Administrative utilities check needed")
                    
                except Exception as e:
                    self.log_test(f"Utils Analysis: {utils_file}", "FAIL", f"Cannot read file: {str(e)}")
        else:
            self.log_test("Utils Directory", "FAIL", "Utils directory not found")
        
        return True
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIP'])
        info_tests = len([r for r in self.test_results if r['status'] == 'INFO'])
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'skipped': skipped_tests,
                'info': info_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'results': self.test_results,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> list:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if r['status'] == 'FAIL']
        
        if any('Backend' in r['test'] for r in failed_tests):
            recommendations.append("Start Django backend server with: cd /workspace/backend && python manage.py runserver 0.0.0.0:8000")
        
        if any('Settings' in r['test'] for r in failed_tests):
            recommendations.append("Verify UserSettings API implementation and authentication")
        
        if any('Service' in r['test'] for r in failed_tests):
            recommendations.append("Check service file imports and API client configuration")
        
        if any('Slice' in r['test'] for r in failed_tests):
            recommendations.append("Verify Redux slice integration with services")
        
        recommendations.append("Run full integration tests after starting backend server")
        recommendations.append("Test Settings.tsx component with live API")
        
        return recommendations

def main():
    """Main test execution function"""
    print("=" * 80)
    print("FRONTEND-TO-BACKEND INTEGRATION TEST SUITE")
    print("Author: Cavin Otieno")
    print("Date: 2025-11-25")
    print("=" * 80)
    
    tester = APIIntegrationTester()
    
    # Run tests
    print("\n🔍 Running Integration Tests...\n")
    
    # Test backend availability (may fail if server not running)
    tester.test_backend_availability()
    
    # Test API endpoints
    tester.test_user_settings_api()
    tester.test_api_endpoints_structure()
    
    # Test frontend integration
    tester.test_service_imports()
    tester.test_redux_integration()
    tester.test_utils_integration()
    
    # Generate and display report
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)
    
    report = tester.generate_report()
    
    summary = report['summary']
    print(f"Total Tests: {summary['total_tests']}")
    print(f"✅ Passed: {summary['passed']}")
    print(f"❌ Failed: {summary['failed']}")
    print(f"⏭️  Skipped: {summary['skipped']}")
    print(f"ℹ️  Info: {summary['info']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    
    if report['recommendations']:
        print("\n" + "=" * 80)
        print("RECOMMENDATIONS")
        print("=" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"{i}. {rec}")
    
    print("\n" + "=" * 80)
    print("DETAILED TEST RESULTS")
    print("=" * 80)
    
    for result in report['results']:
        status_icon = {
            'PASS': '✅',
            'FAIL': '❌', 
            'SKIP': '⏭️',
            'INFO': 'ℹ️'
        }.get(result['status'], '❓')
        
        print(f"{status_icon} [{result['status']}] {result['test']}")
        if result['details']:
            print(f"    {result['details']}")
        print(f"    Time: {result['timestamp']}\n")
    
    # Save detailed report
    report_file = '/workspace/frontend_backend_integration_test_report.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Detailed report saved to: {report_file}")
    
    # Exit with appropriate code
    if summary['failed'] > 0:
        print(f"\n❌ Integration test completed with {summary['failed']} failures")
        sys.exit(1)
    else:
        print(f"\n✅ Integration test completed successfully")
        sys.exit(0)

if __name__ == "__main__":
    main()
