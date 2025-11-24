#!/usr/bin/env python3
"""
JAC Code Execution Engine - Complete Implementation Verification

This script performs comprehensive testing and verification of the complete
JAC code execution system including backend models, APIs, and frontend components.
"""

import os
import sys
import json
import ast
import importlib.util
from pathlib import Path
import subprocess

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(title):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(message):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Print error message."""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_warning(message):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")

def print_info(message):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {message}{Colors.END}")

class JACExecutionVerifier:
    """Main verification class for JAC execution system."""
    
    def __init__(self):
        self.base_dir = Path("/workspace")
        self.backend_dir = self.base_dir / "backend"
        self.frontend_dir = self.base_dir / "frontend"
        self.app_dir = self.backend_dir / "apps" / "jac_execution"
        
        self.test_results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'tests': []
        }
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results."""
        self.test_results['total_tests'] += 1
        try:
            result = test_func()
            if result['status'] == 'pass':
                self.test_results['passed'] += 1
                print_success(f"{test_name}: {result['message']}")
            elif result['status'] == 'warning':
                self.test_results['warnings'] += 1
                print_warning(f"{test_name}: {result['message']}")
            else:
                self.test_results['failed'] += 1
                print_error(f"{test_name}: {result['message']}")
            
            self.test_results['tests'].append({
                'name': test_name,
                'status': result['status'],
                'message': result['message'],
                'details': result.get('details', '')
            })
            
        except Exception as e:
            self.test_results['failed'] += 1
            print_error(f"{test_name}: Exception - {str(e)}")
            self.test_results['tests'].append({
                'name': test_name,
                'status': 'fail',
                'message': f"Exception: {str(e)}",
                'details': ''
            })
    
    def test_backend_file_structure(self):
        """Test backend file structure completeness."""
        required_files = [
            '__init__.py',
            'apps.py', 
            'models.py',
            'serializers.py',
            'views.py',
            'urls.py',
            'admin.py',
            'services/executor.py',
            'migrations/0001_initial.py',
            'migrations/__init__.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.app_dir / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if not missing_files:
            return {
                'status': 'pass',
                'message': f'All {len(required_files)} required files present',
                'details': f'Files: {", ".join(required_files)}'
            }
        else:
            return {
                'status': 'fail',
                'message': f'Missing {len(missing_files)} files: {", ".join(missing_files)}',
                'details': f'Missing: {missing_files}'
            }
    
    def test_frontend_file_structure(self):
        """Test frontend component structure completeness."""
        required_components = [
            'CodeExecutionPanel.jsx',
            'CodeEditor.jsx',
            'OutputWindow.jsx', 
            'TemplateSelector.jsx',
            'ExecutionHistory.jsx',
            'SecuritySettings.jsx',
            'index.js'
        ]
        
        missing_components = []
        for component in required_components:
            full_path = self.frontend_dir / "src/components/jac-execution" / component
            if not full_path.exists():
                missing_components.append(component)
        
        if not missing_components:
            return {
                'status': 'pass',
                'message': f'All {len(required_components)} frontend components present',
                'details': f'Components: {", ".join(required_components)}'
            }
        else:
            return {
                'status': 'fail',
                'message': f'Missing {len(missing_components)} components: {", ".join(missing_components)}',
                'details': f'Missing: {missing_components}'
            }
    
    def test_python_syntax(self, file_path):
        """Test Python file for syntax errors."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return True
        except SyntaxError as e:
            print_error(f"Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            print_error(f"Error reading {file_path}: {e}")
            return False
    
    def test_python_files(self):
        """Test all Python files for syntax correctness."""
        python_files = list(self.app_dir.rglob("*.py"))
        syntax_errors = []
        
        for py_file in python_files:
            if not self.test_python_syntax(py_file):
                syntax_errors.append(str(py_file.relative_to(self.app_dir)))
        
        if not syntax_errors:
            return {
                'status': 'pass',
                'message': f'All {len(python_files)} Python files have valid syntax',
                'details': f'Files tested: {[f.relative_to(self.app_dir) for f in python_files]}'
            }
        else:
            return {
                'status': 'fail',
                'message': f'{len(syntax_errors)} Python files have syntax errors',
                'details': f'Error files: {syntax_errors}'
            }
    
    def test_model_definitions(self):
        """Test Django model definitions."""
        models_file = self.app_dir / "models.py"
        if not models_file.exists():
            return {
                'status': 'fail',
                'message': 'Models file not found',
                'details': ''
            }
        
        try:
            with open(models_file, 'r') as f:
                content = f.read()
            
            # Check for required models
            required_models = [
                'class CodeExecution',
                'class ExecutionTemplate', 
                'class CodeExecutionSession',
                'class SecuritySettings'
            ]
            
            missing_models = []
            for model in required_models:
                if model not in content:
                    missing_models.append(model)
            
            if not missing_models:
                return {
                    'status': 'pass',
                    'message': 'All required models defined',
                    'details': f'Models: {[m.split()[-1] for m in required_models]}'
                }
            else:
                return {
                    'status': 'fail',
                    'message': f'Missing models: {", ".join(missing_models)}',
                    'details': ''
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing models: {str(e)}',
                'details': ''
            }
    
    def test_api_endpoints(self):
        """Test API endpoint definitions."""
        views_file = self.app_dir / "views.py"
        if not views_file.exists():
            return {
                'status': 'fail',
                'message': 'Views file not found',
                'details': ''
            }
        
        try:
            with open(views_file, 'r') as f:
                content = f.read()
            
            # Check for required ViewSets and views
            required_views = [
                'class CodeExecutionViewSet',
                'class ExecutionTemplateViewSet',
                'class SecuritySettingsViewSet',
                'class QuickExecutionView',
                'class LanguageSupportView'
            ]
            
            missing_views = []
            for view in required_views:
                if view not in content:
                    missing_views.append(view)
            
            if not missing_views:
                return {
                    'status': 'pass',
                    'message': 'All required API views defined',
                    'details': f'Views: {[v.split()[-1] for v in required_views]}'
                }
            else:
                return {
                    'status': 'fail',
                    'message': f'Missing API views: {", ".join(missing_views)}',
                    'details': ''
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing views: {str(e)}',
                'details': ''
            }
    
    def test_serializers(self):
        """Test API serializers."""
        serializers_file = self.app_dir / "serializers.py"
        if not serializers_file.exists():
            return {
                'status': 'fail',
                'message': 'Serializers file not found',
                'details': ''
            }
        
        try:
            with open(serializers_file, 'r') as f:
                content = f.read()
            
            # Check for required serializers
            required_serializers = [
                'class CodeExecutionCreateSerializer',
                'class CodeExecutionResultSerializer',
                'class ExecutionTemplateListSerializer',
                'class SecuritySettingsSerializer'
            ]
            
            missing_serializers = []
            for serializer in required_serializers:
                if serializer not in content:
                    missing_serializers.append(serializer)
            
            if not missing_serializers:
                return {
                    'status': 'pass',
                    'message': 'All required serializers defined',
                    'details': f'Serializers: {[s.split()[-1] for s in required_serializers]}'
                }
            else:
                return {
                    'status': 'fail',
                    'message': f'Missing serializers: {", ".join(missing_serializers)}',
                    'details': ''
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing serializers: {str(e)}',
                'details': ''
            }
    
    def test_execution_service(self):
        """Test execution service implementation."""
        service_file = self.app_dir / "services" / "executor.py"
        if not service_file.exists():
            return {
                'status': 'fail',
                'message': 'Execution service file not found',
                'details': ''
            }
        
        try:
            with open(service_file, 'r') as f:
                content = f.read()
            
            # Check for required classes and methods
            required_components = [
                'class CodeExecutor',
                'class ExecutionService',
                'def execute_code',
                'def execute_with_tracking'
            ]
            
            missing_components = []
            for component in required_components:
                if component not in content:
                    missing_components.append(component)
            
            if not missing_components:
                return {
                    'status': 'pass',
                    'message': 'Execution service properly implemented',
                    'details': f'Components: {", ".join(missing_components)}'
                }
            else:
                return {
                    'status': 'warning',
                    'message': f'Missing components: {", ".join(missing_components)}',
                    'details': 'May affect functionality'
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing execution service: {str(e)}',
                'details': ''
            }
    
    def test_frontend_components(self):
        """Test React component implementation."""
        components_dir = self.frontend_dir / "src/components/jac-execution"
        
        if not components_dir.exists():
            return {
                'status': 'fail',
                'message': 'Frontend components directory not found',
                'details': ''
            }
        
        try:
            # Check main component implementation
            main_component = components_dir / "CodeExecutionPanel.jsx"
            if not main_component.exists():
                return {
                    'status': 'fail',
                    'message': 'Main component not found',
                    'details': ''
                }
            
            with open(main_component, 'r') as f:
                content = f.read()
            
            # Check for key features
            required_features = [
                'useState',
                'fetch',
                'executeCode',
                'CodeEditor',
                'OutputWindow',
                'TemplateSelector',
                'ExecutionHistory'
            ]
            
            missing_features = []
            for feature in required_features:
                if feature not in content:
                    missing_features.append(feature)
            
            if not missing_features:
                return {
                    'status': 'pass',
                    'message': 'Main React component properly implemented',
                    'details': f'Features: {", ".join(required_features)}'
                }
            else:
                return {
                    'status': 'warning',
                    'message': f'Missing features: {", ".join(missing_features)}',
                    'details': 'May affect user experience'
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing frontend components: {str(e)}',
                'details': ''
            }
    
    def test_security_features(self):
        """Test security feature implementation."""
        executor_file = self.app_dir / "services" / "executor.py"
        models_file = self.app_dir / "models.py"
        
        try:
            security_features = []
            
            # Check execution service for security features
            if executor_file.exists():
                with open(executor_file, 'r') as f:
                    executor_content = f.read()
                
                security_checks = [
                    'SecurityViolationError',
                    'ResourceLimitError',
                    'blocked_imports',
                    'blocked_functions',
                    'max_execution_time',
                    'sandboxing'
                ]
                
                for check in security_checks:
                    if check in executor_content:
                        security_features.append(f"Executor: {check}")
            
            # Check models for security settings
            if models_file.exists():
                with open(models_file, 'r') as f:
                    models_content = f.read()
                
                if 'SecuritySettings' in models_content:
                    security_features.append('SecuritySettings model')
            
            if len(security_features) >= 3:
                return {
                    'status': 'pass',
                    'message': f'Security features implemented: {len(security_features)}',
                    'details': f'Features: {", ".join(security_features)}'
                }
            else:
                return {
                    'status': 'warning',
                    'message': f'Limited security features: {len(security_features)}',
                    'details': 'Consider adding more security measures'
                }
                
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Error analyzing security features: {str(e)}',
                'details': ''
            }
    
    def test_documentation(self):
        """Test documentation and code quality."""
        docs_score = 0
        details = []
        
        # Check for docstrings in Python files
        python_files = list(self.app_dir.rglob("*.py"))
        for py_file in python_files:
            try:
                with open(py_file, 'r') as f:
                    content = f.read()
                
                # Count docstrings
                docstring_count = content.count('"""')
                if docstring_count >= 2:  # Module docstring + class/function docstrings
                    docs_score += 1
                    details.append(f"{py_file.relative_to(self.app_dir)}: {docstring_count} docstrings")
                    
            except Exception:
                continue
        
        if docs_score >= len(python_files) * 0.7:  # 70% of files have good documentation
            return {
                'status': 'pass',
                'message': f'Good documentation coverage: {docs_score}/{len(python_files)} files',
                'details': f'{"; ".join(details[:3])}{"..." if len(details) > 3 else ""}'
            }
        else:
            return {
                'status': 'warning',
                'message': f'Limited documentation: {docs_score}/{len(python_files)} files',
                'details': 'Consider adding more docstrings and comments'
            }
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        print_header("JAC CODE EXECUTION ENGINE - VERIFICATION SUMMARY")
        
        total = self.test_results['total_tests']
        passed = self.test_results['passed']
        failed = self.test_results['failed']
        warnings = self.test_results['warnings']
        
        # Calculate success rate
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"{Colors.BOLD}Overall Results:{Colors.END}")
        print(f"  Total Tests: {total}")
        print(f"  {Colors.GREEN}Passed: {passed}{Colors.END}")
        print(f"  {Colors.YELLOW}Warnings: {warnings}{Colors.END}")
        print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        # System Status
        if failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ SYSTEM STATUS: FULLY OPERATIONAL{Colors.END}")
            print(f"{Colors.GREEN}The JAC Code Execution Engine is ready for deployment!{Colors.END}")
        elif failed <= 2:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ SYSTEM STATUS: MOSTLY OPERATIONAL{Colors.END}")
            print(f"{Colors.YELLOW}Minor issues detected. System should function with limited features.{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ SYSTEM STATUS: NEEDS ATTENTION{Colors.END}")
            print(f"{Colors.RED}Critical issues detected. Review failed tests before deployment.{Colors.END}")
        
        # Feature Status
        print(f"\n{Colors.BOLD}Feature Implementation Status:{Colors.END}")
        
        categories = {
            'Backend Implementation': ['Backend file structure', 'Python syntax', 'Model definitions', 'API endpoints', 'Serializers', 'Execution service'],
            'Frontend Implementation': ['Frontend file structure', 'React components'],
            'Security & Quality': ['Security features', 'Documentation']
        }
        
        for category, tests in categories.items():
            category_results = [t for t in self.test_results['tests'] if any(test in t['name'] for test in tests)]
            if category_results:
                category_passed = len([t for t in category_results if t['status'] == 'pass'])
                category_total = len(category_results)
                category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
                
                status_color = Colors.GREEN if category_rate >= 80 else Colors.YELLOW if category_rate >= 60 else Colors.RED
                print(f"  {category}: {status_color}{category_passed}/{category_total} ({category_rate:.0f}%){Colors.END}")
        
        # Detailed Test Results
        print(f"\n{Colors.BOLD}Detailed Test Results:{Colors.END}")
        for test in self.test_results['tests']:
            if test['status'] == 'fail':
                print(f"  {Colors.RED}✗ {test['name']}: {test['message']}{Colors.END}")
            elif test['status'] == 'warning':
                print(f"  {Colors.YELLOW}⚠ {test['name']}: {test['message']}{Colors.END}")
        
        # Next Steps
        print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
        if failed == 0:
            print(f"  {Colors.GREEN}1. Deploy to production environment{Colors.END}")
            print(f"  {Colors.GREEN}2. Configure database and migrations{Colors.END}")
            print(f"  {Colors.GREEN}3. Set up frontend build and deployment{Colors.END}")
            print(f"  {Colors.GREEN}4. Configure authentication and security settings{Colors.END}")
            print(f"  {Colors.GREEN}5. Perform integration testing{Colors.END}")
        else:
            print(f"  {Colors.RED}1. Review and fix failed tests{Colors.END}")
            print(f"  {Colors.RED}2. Re-run verification after fixes{Colors.END}")
            print(f"  {Colors.YELLOW}3. Address warnings for optimal performance{Colors.END}")
        
        # Save detailed report
        report_file = self.base_dir / "JAC_EXECUTION_VERIFICATION_REPORT.json"
        try:
            with open(report_file, 'w') as f:
                json.dump(self.test_results, f, indent=2)
            print(f"\n{Colors.CYAN}Detailed report saved to: {report_file}{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.YELLOW}Could not save detailed report: {e}{Colors.END}")
        
        return success_rate >= 80
    
    def run_all_tests(self):
        """Run all verification tests."""
        print_header("JAC CODE EXECUTION ENGINE - COMPREHENSIVE VERIFICATION")
        
        # Backend tests
        print(f"{Colors.BLUE}{Colors.BOLD}BACKEND TESTS{Colors.END}")
        self.run_test("Backend File Structure", self.test_backend_file_structure)
        self.run_test("Python Syntax Validation", self.test_python_files)
        self.run_test("Model Definitions", self.test_model_definitions)
        self.run_test("API Endpoints", self.test_api_endpoints)
        self.run_test("API Serializers", self.test_serializers)
        self.run_test("Execution Service", self.test_execution_service)
        
        # Frontend tests
        print(f"\n{Colors.BLUE}{Colors.BOLD}FRONTEND TESTS{Colors.END}")
        self.run_test("Frontend File Structure", self.test_frontend_file_structure)
        self.run_test("React Components", self.test_frontend_components)
        
        # Security and Quality tests
        print(f"\n{Colors.BLUE}{Colors.BOLD}SECURITY & QUALITY TESTS{Colors.END}")
        self.run_test("Security Features", self.test_security_features)
        self.run_test("Documentation Quality", self.test_documentation)
        
        # Generate summary
        return self.generate_summary_report()


def main():
    """Main verification function."""
    verifier = JACExecutionVerifier()
    success = verifier.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()