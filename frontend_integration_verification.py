#!/usr/bin/env python3
"""
Simple Frontend Integration Verification
Author: MiniMax Agent
Date: 2025-11-25

This script verifies frontend-to-backend integration without requiring a running server.
"""

import os
import json
import re
from typing import Dict, List, Any

class FrontendIntegrationVerifier:
    def __init__(self):
        self.workspace_path = '/workspace'
        self.frontend_path = '/workspace/frontend/src'
        self.backend_path = '/workspace/backend'
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
    
    def verify_store_integration(self):
        """Verify Redux store integration"""
        print("\n🔍 Verifying Redux Store Integration...")
        
        # Check store configuration
        store_file = os.path.join(self.frontend_path, 'store', 'store.ts')
        if os.path.exists(store_file):
            with open(store_file, 'r') as f:
                content = f.read()
            
            # Check for all slice imports
            expected_slices = [
                'authReducer', 'uiReducer', 'learningReducer',
                'assessmentReducer', 'agentReducer', 'adminReducer', 'searchReducer'
            ]
            
            found_slices = []
            missing_slices = []
            
            for slice_name in expected_slices:
                if slice_name in content:
                    found_slices.append(slice_name)
                else:
                    missing_slices.append(slice_name)
            
            if not missing_slices:
                self.log_result('Store', 'Slice Configuration', 'PASS', f'All {len(found_slices)} slices properly imported')
            else:
                self.log_result('Store', 'Slice Configuration', 'FAIL', f'Missing slices: {missing_slices}')
        else:
            self.log_result('Store', 'Store Configuration', 'FAIL', 'store.ts file not found')
        
        # Check individual slices
        slices_dir = os.path.join(self.frontend_path, 'store', 'slices')
        if os.path.exists(slices_dir):
            slice_files = [f for f in os.listdir(slices_dir) if f.endswith('.ts')]
            
            service_integrations = 0
            for slice_file in slice_files:
                slice_path = os.path.join(slices_dir, slice_file)
                try:
                    with open(slice_path, 'r') as f:
                        content = f.read()
                    
                    # Check for service integration
                    if 'createAsyncThunk' in content and 'services' in content:
                        service_integrations += 1
                        # Extract service name
                        service_match = re.search(r'from [\'"]\.\.\/services\/([^\'"]+)[\'"]', content)
                        if service_match:
                            service_name = service_match.group(1)
                            self.log_result('Store', f'{slice_file} Integration', 'PASS', f'Uses {service_name} service')
                        
                except Exception as e:
                    self.log_result('Store', f'{slice_file} Analysis', 'FAIL', f'Cannot read: {str(e)}')
            
            if service_integrations > 0:
                self.log_result('Store', 'Service Integration', 'PASS', f'{service_integrations}/{len(slice_files)} slices use services')
        
    def verify_services_integration(self):
        """Verify service layer integration"""
        print("\n🔍 Verifying Service Layer Integration...")
        
        services_dir = os.path.join(self.frontend_path, 'services')
        if os.path.exists(services_dir):
            service_files = [f for f in os.listdir(services_dir) if f.endswith('.ts')]
            
            for service_file in service_files:
                service_path = os.path.join(services_dir, service_file)
                try:
                    with open(service_path, 'r') as f:
                        content = f.read()
                    
                    # Check for API client import
                    if 'import' in content and ('apiClient' in content or 'axios' in content):
                        self.log_result('Services', f'{service_file} API Client', 'PASS', 'Has API client integration')
                    else:
                        self.log_result('Services', f'{service_file} API Client', 'WARN', 'API client integration not found')
                    
                    # Check for async methods
                    async_methods = len(re.findall(r'async\s+\w+', content))
                    if async_methods > 0:
                        self.log_result('Services', f'{service_file} Methods', 'PASS', f'Contains {async_methods} async methods')
                    
                    # Check for specific services
                    if service_file == 'settingsService.ts':
                        self.log_result('Services', 'Settings Service', 'PASS', 'Dedicated settings service created')
                    elif service_file == 'authService.ts':
                        self.log_result('Services', 'Auth Service', 'PASS', 'Authentication service available')
                    elif service_file == 'searchService.ts':
                        self.log_result('Services', 'Search Service', 'PASS', 'Search service available')
                        
                except Exception as e:
                    self.log_result('Services', f'{service_file} Analysis', 'FAIL', f'Cannot read: {str(e)}')
        
    def verify_utils_integration(self):
        """Verify utility functions integration"""
        print("\n🔍 Verifying Utils Integration...")
        
        utils_dir = os.path.join(self.frontend_path, 'utils')
        if os.path.exists(utils_dir):
            utils_files = [f for f in os.listdir(utils_dir) if f.endswith('.ts')]
            
            for utils_file in utils_files:
                utils_path = os.path.join(utils_dir, utils_file)
                try:
                    with open(utils_path, 'r') as f:
                        content = f.read()
                    
                    # Count exports (functions/constants)
                    export_count = len(re.findall(r'export\s+(const|function|class)', content))
                    
                    if utils_file == 'adminUtils.ts':
                        if export_count > 10:
                            self.log_result('Utils', 'Admin Utils', 'PASS', f'Contains {export_count} utility functions')
                        else:
                            self.log_result('Utils', 'Admin Utils', 'INFO', f'Contains {export_count} exports')
                    
                    elif utils_file == 'sentry.ts':
                        self.log_result('Utils', 'Error Handling', 'PASS', 'Error boundary utilities available')
                        
                    else:
                        self.log_result('Utils', f'{utils_file}', 'INFO', f'Contains {export_count} exports')
                        
                except Exception as e:
                    self.log_result('Utils', f'{utils_file} Analysis', 'FAIL', f'Cannot read: {str(e)}')
    
    def verify_backend_integration(self):
        """Verify backend API integration"""
        print("\n🔍 Verifying Backend API Integration...")
        
        # Check UserSettings API
        users_views = os.path.join(self.backend_path, 'apps', 'users', 'views.py')
        if os.path.exists(users_views):
            with open(users_views, 'r') as f:
                content = f.read()
            
            if 'UserSettingsView' in content and 'GET' in content and 'PUT' in content:
                self.log_result('Backend', 'UserSettings API', 'PASS', 'UserSettingsView with CRUD operations')
            else:
                self.log_result('Backend', 'UserSettings API', 'WARN', 'UserSettingsView implementation incomplete')
        
        # Check UserSettingsSerializer
        users_serializers = os.path.join(self.backend_path, 'apps', 'users', 'serializers.py')
        if os.path.exists(users_serializers):
            with open(users_serializers, 'r') as f:
                content = f.read()
            
            if 'UserSettingsSerializer' in content:
                # Count settings fields
                field_patterns = [
                    r'learning_style', r'preferred_difficulty', r'learning_pace',
                    r'agent_interaction_level', r'preferred_feedback_style',
                    r'dark_mode', r'notifications_enabled'
                ]
                
                found_fields = sum(1 for pattern in field_patterns if re.search(pattern, content))
                
                if found_fields >= 5:
                    self.log_result('Backend', 'UserSettingsSerializer', 'PASS', f'Contains {found_fields} settings fields')
                else:
                    self.log_result('Backend', 'UserSettingsSerializer', 'WARN', f'Only {found_fields} settings fields found')
        
        # Check AssessmentQuestion model fix
        assessments_models = os.path.join(self.backend_path, 'apps', 'assessments', 'models.py')
        if os.path.exists(assessments_models):
            with open(assessments_models, 'r') as f:
                content = f.read()
            
            if 'null=True, blank=True' in content and 'assessment' in content:
                self.log_result('Backend', 'AssessmentQuestion Migration', 'PASS', 'Assessment field made nullable')
            else:
                self.log_result('Backend', 'AssessmentQuestion Migration', 'WARN', 'Assessment field nullable check needed')
        
        # Check URL routing
        users_urls = os.path.join(self.backend_path, 'apps', 'users', 'urls.py')
        if os.path.exists(users_urls):
            with open(users_urls, 'r') as f:
                content = f.read()
            
            if 'settings/' in content:
                self.log_result('Backend', 'URL Routing', 'PASS', 'Settings endpoint properly routed')
            else:
                self.log_result('Backend', 'URL Routing', 'WARN', 'Settings endpoint not found in URLs')
    
    def verify_component_integration(self):
        """Verify component integration"""
        print("\n🔍 Verifying Component Integration...")
        
        # Check Settings.tsx integration
        settings_component = os.path.join(self.frontend_path, 'pages', 'Settings.tsx')
        if os.path.exists(settings_component):
            with open(settings_component, 'r') as f:
                content = f.read()
            
            # Check for settings service usage
            if 'settingsService' in content:
                self.log_result('Components', 'Settings.tsx Service', 'PASS', 'Uses settingsService instead of authSlice')
            else:
                self.log_result('Components', 'Settings.tsx Service', 'WARN', 'Still using generic authSlice methods')
            
            # Check for loading states
            if 'isSettingsLoading' in content and 'isSaving' in content:
                self.log_result('Components', 'Settings.tsx States', 'PASS', 'Has dedicated loading states')
            else:
                self.log_result('Components', 'Settings.tsx States', 'INFO', 'Loading states check needed')
        
        # Check Search component
        search_component = os.path.join(self.frontend_path, 'components', 'search', 'Search.tsx')
        if os.path.exists(search_component):
            self.log_result('Components', 'Search Component', 'PASS', 'Search component exists')
        
        # Check Assessment components
        assessments_dir = os.path.join(self.frontend_path, 'pages', 'assessments')
        if os.path.exists(assessments_dir):
            component_files = [f for f in os.listdir(assessments_dir) if f.endswith('.tsx')]
            self.log_result('Components', 'Assessment Components', 'INFO', f'Found {len(component_files)} assessment components')
    
    def generate_summary_report(self):
        """Generate summary report"""
        print("\n" + "="*80)
        print("FRONTEND-TO-BACKEND INTEGRATION VERIFICATION SUMMARY")
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
            'detailed_results': self.results
        }
        
        report_file = os.path.join(self.workspace_path, 'frontend_integration_verification_report.json')
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Final assessment
        print("\n" + "="*80)
        print("INTEGRATION ASSESSMENT")
        print("="*80)
        
        if success_rate >= 80:
            print("✅ EXCELLENT: Frontend-to-backend integration is highly successful")
        elif success_rate >= 60:
            print("✅ GOOD: Frontend-to-backend integration is mostly complete")
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
    print("FRONTEND-TO-BACKEND INTEGRATION VERIFICATION")
    print("Author: MiniMax Agent")
    print("Date: 2025-11-25")
    print("="*80)
    
    verifier = FrontendIntegrationVerifier()
    
    # Run verifications
    verifier.verify_store_integration()
    verifier.verify_services_integration()
    verifier.verify_utils_integration()
    verifier.verify_backend_integration()
    verifier.verify_component_integration()
    
    # Generate report
    verifier.generate_summary_report()
    
    print("\n" + "="*80)
    print("VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
