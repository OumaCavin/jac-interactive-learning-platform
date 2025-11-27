#!/usr/bin/env python3 
"""
Comprehensive Verification Script for Frontend Pages
Verifies all remaining page files in frontend/src/pages/ directory

Pages to verify:
- Achievements.tsx (733 lines)
- AdminDashboard.tsx (1552 lines) 
- Chat.tsx (479 lines)
- CodeEditor.tsx (501 lines)
- Dashboard.tsx (469 lines)
- KnowledgeGraph.tsx (759 lines)
- Profile.tsx (539 lines)
- Progress.tsx (739 lines)
- Settings.tsx (591 lines)
"""

import os
import re
import ast
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class VerificationStatus(Enum):
    PASS = "✅ PASS"
    FAIL = "❌ FAIL"
    WARNING = "⚠️ WARNING"
    INFO = "ℹ️ INFO"

@dataclass
class VerificationResult:
    file_name: str
    check_name: str
    status: VerificationStatus
    message: str
    details: str = ""
    line_number: int = 0

@dataclass
class PageVerification:
    file_name: str
    total_lines: int
    results: List[VerificationResult]
    score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warnings: int

class PageVerifier:
    def __init__(self):
        self.pages_dir = "frontend/src/pages"
        self.results: List[VerificationResult] = []
        
        # Define all pages to verify
        self.pages_to_verify = [
            "Achievements.tsx",
            "AdminDashboard.tsx", 
            "Chat.tsx",
            "CodeEditor.tsx",
            "Dashboard.tsx",
            "KnowledgeGraph.tsx",
            "Profile.tsx",
            "Progress.tsx",
            "Settings.tsx"
        ]
        
        # Common React patterns
        self.react_import_patterns = [
            r'import\s+React',
            r'import\s+.*\s+from\s+[\'"]react[\'"]',
            r'import\s+\{.*useState.*\}\s+from\s+[\'"]react[\'"]',
            r'import\s+\{.*useEffect.*\}\s+from\s+[\'"]react[\'"]',
            r'import\s+\{.*useDispatch.*\}\s+from\s+[\'"]react-redux[\'"]',
            r'import\s+\{.*useSelector.*\}\s+from\s+[\'"]react-redux[\'"]',
        ]
        
        # TypeScript interface patterns
        self.interface_patterns = [
            r'interface\s+\w+',
            r'type\s+\w+\s*=',
        ]
        
        # Redux patterns
        self.redux_patterns = [
            r'useSelector',
            r'useDispatch',
            r'createSlice',
            r'createAsyncThunk',
            r'selectAuth',
            r'RootState',
        ]
        
        # Router patterns
        self.router_patterns = [
            r'useParams',
            r'useNavigate',
            r'Link\s+from',
            r'createBrowserRouter',
            r'createRoutesFromElements',
        ]
        
        # Service patterns
        self.service_patterns = [
            r'from.*services/',
            r'learningService',
            r'authService',
            r'agentService',
        ]
        
        # UI component patterns
        self.ui_patterns = [
            r'from.*components/ui',
            r'Card',
            r'Button',
            r'Badge',
            r'ProgressBar',
            r'Input',
        ]

    def verify_file_exists(self, file_path: str) -> VerificationResult:
        """Check if the file exists"""
        file_name = os.path.basename(file_path)
        if os.path.exists(file_path):
            return VerificationResult(
                file_name=file_name,
                check_name="File Exists",
                status=VerificationStatus.PASS,
                message=f"File {file_name} exists",
                details=f"Full path: {file_path}"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="File Exists",
                status=VerificationStatus.FAIL,
                message=f"File {file_name} not found",
                details=f"Expected path: {file_path}"
            )

    def read_file_content(self, file_path: str) -> Tuple[str, int]:
        """Read file content and return content and line count"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, len(content.split('\n'))
        except Exception as e:
            return f"Error reading file: {str(e)}", 0

    def verify_react_component_structure(self, content: str, file_name: str) -> VerificationResult:
        """Verify React component structure"""
        # Check for export default
        export_pattern = r'export\s+default\s+\w+'
        has_export = bool(re.search(export_pattern, content))
        
        # Check for component declaration
        component_patterns = [
            r'const\s+\w+:\s*React\.FC',
            r'function\s+\w+\(\)',
            r'export\s+const\s+\w+:\s*React\.FC',
        ]
        
        has_component = any(re.search(pattern, content) for pattern in component_patterns)
        
        if has_export and has_component:
            return VerificationResult(
                file_name=file_name,
                check_name="React Component Structure",
                status=VerificationStatus.PASS,
                message="Proper React component structure with export",
                details="Contains component declaration and export statement"
            )
        else:
            issues = []
            if not has_export:
                issues.append("Missing export default statement")
            if not has_component:
                issues.append("Missing proper component declaration")
            
            return VerificationResult(
                file_name=file_name,
                check_name="React Component Structure",
                status=VerificationStatus.FAIL,
                message="Invalid React component structure",
                details="; ".join(issues)
            )

    def verify_react_imports(self, content: str, file_name: str) -> VerificationResult:
        """Verify React imports"""
        react_imports_found = []
        for pattern in self.react_import_patterns:
            if re.search(pattern, content):
                react_imports_found.append(pattern)
        
        if len(react_imports_found) >= 2:  # At least basic React and one hook
            return VerificationResult(
                file_name=file_name,
                check_name="React Imports",
                status=VerificationStatus.PASS,
                message="Proper React imports detected",
                details=f"Found {len(react_imports_found)} React-related imports"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="React Imports",
                status=VerificationStatus.WARNING,
                message="Limited React imports",
                details="May be missing essential React imports"
            )

    def verify_typescript_interfaces(self, content: str, file_name: str) -> VerificationResult:
        """Verify TypeScript interfaces"""
        interfaces_found = []
        for pattern in self.interface_patterns:
            matches = re.findall(pattern, content)
            if matches:
                interfaces_found.extend(matches)
        
        if interfaces_found:
            return VerificationResult(
                file_name=file_name,
                check_name="TypeScript Interfaces",
                status=VerificationStatus.PASS,
                message="TypeScript interfaces/types defined",
                details=f"Found {len(interfaces_found)} interfaces/types"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="TypeScript Interfaces",
                status=VerificationStatus.WARNING,
                message="No TypeScript interfaces found",
                details="Consider adding interfaces for better type safety"
            )

    def verify_redux_integration(self, content: str, file_name: str) -> VerificationResult:
        """Verify Redux integration"""
        redux_usage = []
        for pattern in self.redux_patterns:
            if re.search(pattern, content):
                redux_usage.append(pattern)
        
        if redux_usage:
            return VerificationResult(
                file_name=file_name,
                check_name="Redux Integration",
                status=VerificationStatus.PASS,
                message="Redux integration detected",
                details=f"Found Redux patterns: {len(redux_usage)}"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Redux Integration",
                status=VerificationStatus.INFO,
                message="No Redux integration",
                details="This page may not require Redux state management"
            )

    def verify_router_hooks(self, content: str, file_name: str) -> VerificationResult:
        """Verify React Router hooks usage"""
        router_usage = []
        for pattern in self.router_patterns:
            if re.search(pattern, content):
                router_usage.append(pattern)
        
        if router_usage:
            return VerificationResult(
                file_name=file_name,
                check_name="React Router Integration",
                status=VerificationStatus.PASS,
                message="React Router integration detected",
                details=f"Found router patterns: {len(router_usage)}"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="React Router Integration",
                status=VerificationStatus.INFO,
                message="No React Router hooks detected",
                details="This page may not require routing functionality"
            )

    def verify_service_integrations(self, content: str, file_name: str) -> VerificationResult:
        """Verify service integrations"""
        services_found = []
        for pattern in self.service_patterns:
            if re.search(pattern, content):
                services_found.append(pattern)
        
        if services_found:
            return VerificationResult(
                file_name=file_name,
                check_name="Service Integrations",
                status=VerificationStatus.PASS,
                message="Service integrations detected",
                details=f"Found {len(services_found)} service integrations"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Service Integrations",
                status=VerificationStatus.WARNING,
                message="No service integrations found",
                details="May need API service integrations"
            )

    def verify_ui_components(self, content: str, file_name: str) -> VerificationResult:
        """Verify UI component usage"""
        ui_components_found = []
        for pattern in self.ui_patterns:
            if re.search(pattern, content):
                ui_components_found.append(pattern)
        
        if ui_components_found:
            return VerificationResult(
                file_name=file_name,
                check_name="UI Components Usage",
                status=VerificationStatus.PASS,
                message="UI components properly integrated",
                details=f"Found {len(ui_components_found)} UI component patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="UI Components Usage",
                status=VerificationStatus.WARNING,
                message="Limited UI component usage",
                details="Consider using design system components"
            )

    def verify_error_handling(self, content: str, file_name: str) -> VerificationResult:
        """Verify error handling patterns"""
        error_patterns = [
            r'try\s*{',
            r'catch\s*\(',
            r'error',
            r'throw',
            r'toast\.error',
            r'console\.error',
        ]
        
        error_handling_found = []
        for pattern in error_patterns:
            if re.search(pattern, content):
                error_handling_found.append(pattern)
        
        if len(error_handling_found) >= 2:
            return VerificationResult(
                file_name=file_name,
                check_name="Error Handling",
                status=VerificationStatus.PASS,
                message="Error handling implemented",
                details=f"Found {len(error_handling_found)} error handling patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Error Handling",
                status=VerificationStatus.WARNING,
                message="Limited error handling",
                details="Consider adding proper error handling"
            )

    def verify_performance_patterns(self, content: str, file_name: str) -> VerificationResult:
        """Verify performance optimization patterns"""
        performance_patterns = [
            r'useCallback',
            r'useMemo',
            r'React\.lazy',
            r'memo\(',
            r'LazyLoad',
        ]
        
        performance_found = []
        for pattern in performance_patterns:
            if re.search(pattern, content):
                performance_found.append(pattern)
        
        if performance_found:
            return VerificationResult(
                file_name=file_name,
                check_name="Performance Optimization",
                status=VerificationStatus.PASS,
                message="Performance optimizations detected",
                details=f"Found {len(performance_found)} performance patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Performance Optimization",
                status=VerificationStatus.INFO,
                message="No performance optimizations detected",
                details="Complex components may benefit from optimizations"
            )

    def verify_accessibility(self, content: str, file_name: str) -> VerificationResult:
        """Verify accessibility features"""
        accessibility_patterns = [
            r'role=',
            r'aria-label',
            r'aria-labelledby',
            r'aria-describedby',
            r'aria-expanded',
            r'aria-hidden',
            r'tabIndex',
            r'focus',
        ]
        
        accessibility_found = []
        for pattern in accessibility_patterns:
            if re.search(pattern, content):
                accessibility_found.append(pattern)
        
        if accessibility_found:
            return VerificationResult(
                file_name=file_name,
                check_name="Accessibility Features",
                status=VerificationStatus.PASS,
                message="Accessibility features detected",
                details=f"Found {len(accessibility_found)} accessibility patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Accessibility Features",
                status=VerificationStatus.WARNING,
                message="No accessibility features detected",
                details="Consider adding ARIA labels and roles for screen readers"
            )

    def verify_code_quality(self, content: str, file_name: str) -> VerificationResult:
        """Verify code quality indicators"""
        # Check for console.log statements
        console_log_count = len(re.findall(r'console\.log', content))
        console_error_count = len(re.findall(r'console\.error', content))
        debug_statements = console_log_count + console_error_count
        
        # Check for TODO/FIXME comments
        todo_count = len(re.findall(r'// TODO|FIXME|HACK', content, re.IGNORECASE))
        
        if debug_statements == 0 and todo_count <= 2:
            status = VerificationStatus.PASS
            message = "Good code quality"
            details = "No debug statements, minimal TODO comments"
        elif debug_statements <= 3 and todo_count <= 5:
            status = VerificationStatus.WARNING
            message = "Moderate code quality"
            details = f"Some debug statements ({debug_statements}) or TODO comments ({todo_count})"
        else:
            status = VerificationStatus.FAIL
            message = "Poor code quality"
            details = f"Too many debug statements ({debug_statements}) or TODO comments ({todo_count})"
        
        return VerificationResult(
            file_name=file_name,
            check_name="Code Quality",
            status=status,
            message=message,
            details=details
        )

    def verify_mock_data_quality(self, content: str, file_name: str) -> VerificationResult:
        """Verify mock data implementation"""
        # Check for mock data patterns
        mock_patterns = [
            r'const\s+mock\w+\s*=\s*\[',
            r'mock\w+\s*:\s*{',
            r'// Mock',
            r'# Mock',
            r'MOCK_',
        ]
        
        mock_data_found = []
        for pattern in mock_patterns:
            matches = re.findall(pattern, content)
            if matches:
                mock_data_found.extend(matches)
        
        if mock_data_found:
            return VerificationResult(
                file_name=file_name,
                check_name="Mock Data Quality",
                status=VerificationStatus.PASS,
                message="Mock data implementation found",
                details=f"Found {len(mock_data_found)} mock data patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="Mock Data Quality",
                status=VerificationStatus.INFO,
                message="No mock data detected",
                details="May be using real API data or no data needed"
            )

    def verify_state_management(self, content: str, file_name: str) -> VerificationResult:
        """Verify state management implementation"""
        state_patterns = [
            r'useState',
            r'setState',
            r'createSlice',
            r'reducer',
            r'initialState',
        ]
        
        state_found = []
        for pattern in state_patterns:
            if re.search(pattern, content):
                state_found.append(pattern)
        
        if state_found:
            return VerificationResult(
                file_name=file_name,
                check_name="State Management",
                status=VerificationStatus.PASS,
                message="State management implemented",
                details=f"Found {len(state_found)} state management patterns"
            )
        else:
            return VerificationResult(
                file_name=file_name,
                check_name="State Management",
                status=VerificationStatus.WARNING,
                message="No state management detected",
                details="Component may need internal state management"
            )

    def verify_single_page(self, file_name: str) -> PageVerification:
        """Verify a single page file"""
        print(f"\n🔍 Verifying {file_name}...")
        
        file_path = os.path.join(self.pages_dir, file_name)
        results = []
        
        # Basic file existence check
        file_result = self.verify_file_exists(file_path)
        results.append(file_result)
        
        if file_result.status == VerificationStatus.FAIL:
            # Create a minimal result for missing files
            return PageVerification(
                file_name=file_name,
                total_lines=0,
                results=results,
                score=0.0,
                total_checks=1,
                passed_checks=0,
                failed_checks=1,
                warnings=0
            )
        
        # Read file content
        content, line_count = self.read_file_content(file_path)
        
        # Run all verification checks
        checks = [
            self.verify_react_component_structure,
            self.verify_react_imports,
            self.verify_typescript_interfaces,
            self.verify_redux_integration,
            self.verify_router_hooks,
            self.verify_service_integrations,
            self.verify_ui_components,
            self.verify_error_handling,
            self.verify_performance_patterns,
            self.verify_accessibility,
            self.verify_code_quality,
            self.verify_mock_data_quality,
            self.verify_state_management,
        ]
        
        for check_func in checks:
            result = check_func(content, file_name)
            results.append(result)
        
        # Calculate scores
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r.status == VerificationStatus.PASS)
        failed_checks = sum(1 for r in results if r.status == VerificationStatus.FAIL)
        warnings = sum(1 for r in results if r.status == VerificationStatus.WARNING)
        
        # Calculate score (passes = 2 points, warnings = 1 point, fails = 0 points)
        score = ((passed_checks * 2) + (warnings * 1)) / (total_checks * 2) * 100
        
        return PageVerification(
            file_name=file_name,
            total_lines=line_count,
            results=results,
            score=score,
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warnings=warnings
        )

    def verify_all_pages(self) -> Dict[str, PageVerification]:
        """Verify all page files"""
        print("🚀 Starting comprehensive page verification...")
        print(f"📁 Pages directory: {self.pages_dir}")
        print(f"📋 Pages to verify: {len(self.pages_to_verify)}")
        
        verification_results = {}
        
        for page_file in self.pages_to_verify:
            page_result = self.verify_single_page(page_file)
            verification_results[page_file] = page_result
        
        return verification_results

    def generate_report(self, results: Dict[str, PageVerification]) -> str:
        """Generate comprehensive verification report"""
        report_lines = []
        
        # Header
        report_lines.append("=" * 80)
        report_lines.append("FRONTEND PAGES VERIFICATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Summary
        total_files = len(results)
        total_lines = sum(r.total_lines for r in results.values())
        total_checks = sum(r.total_checks for r in results.values())
        total_passed = sum(r.passed_checks for r in results.values())
        total_failed = sum(r.failed_checks for r in results.values())
        total_warnings = sum(r.warnings for r in results.values())
        overall_score = sum(r.score for r in results.values()) / total_files if total_files > 0 else 0
        
        report_lines.append("📊 OVERVIEW")
        report_lines.append("-" * 40)
        report_lines.append(f"Total Files Verified: {total_files}")
        report_lines.append(f"Total Lines of Code: {total_lines:,}")
        report_lines.append(f"Total Checks Performed: {total_checks}")
        report_lines.append(f"✅ Passed Checks: {total_passed}")
        report_lines.append(f"❌ Failed Checks: {total_failed}")
        report_lines.append(f"⚠️  Warnings: {total_warnings}")
        report_lines.append(f"🎯 Overall Score: {overall_score:.1f}%")
        report_lines.append("")
        
        # Individual file reports
        report_lines.append("📄 INDIVIDUAL FILE REPORTS")
        report_lines.append("=" * 80)
        
        for file_name, verification in results.items():
            report_lines.append(f"\n📁 {file_name}")
            report_lines.append("-" * 60)
            report_lines.append(f"Lines of Code: {verification.total_lines:,}")
            report_lines.append(f"Score: {verification.score:.1f}%")
            report_lines.append(f"Checks: {verification.passed_checks}/{verification.total_checks} passed")
            report_lines.append(f"Status: ✅ {verification.passed_checks} | ❌ {verification.failed_checks} | ⚠️ {verification.warnings}")
            
            # Detailed results
            report_lines.append("\nDetailed Results:")
            for result in verification.results:
                status_emoji = "✅" if result.status == VerificationStatus.PASS else \
                              "❌" if result.status == VerificationStatus.FAIL else \
                              "⚠️" if result.status == VerificationStatus.WARNING else "ℹ️"
                report_lines.append(f"  {status_emoji} {result.check_name}: {result.message}")
                if result.details:
                    report_lines.append(f"    📝 {result.details}")
        
        # Issues summary
        report_lines.append("\n" + "=" * 80)
        report_lines.append("🚨 ISSUES REQUIRING ATTENTION")
        report_lines.append("=" * 80)
        
        all_issues = []
        for verification in results.values():
            for result in verification.results:
                if result.status in [VerificationStatus.FAIL, VerificationStatus.WARNING]:
                    all_issues.append((verification.file_name, result.check_name, result.message, result.details))
        
        if all_issues:
            for file_name, check_name, message, details in all_issues:
                report_lines.append(f"\n📄 {file_name} - {check_name}")
                report_lines.append(f"   {message}")
                if details:
                    report_lines.append(f"   Details: {details}")
        else:
            report_lines.append("\n🎉 No issues found! All pages are in excellent condition.")
        
        # Recommendations
        report_lines.append("\n" + "=" * 80)
        report_lines.append("💡 RECOMMENDATIONS")
        report_lines.append("=" * 80)
        
        recommendations = []
        
        # Analyze patterns across all files
        accessibility_count = 0
        error_handling_count = 0
        performance_count = 0
        code_quality_issues = 0
        
        for verification in results.values():
            for result in verification.results:
                if result.check_name == "Accessibility Features" and result.status == VerificationStatus.PASS:
                    accessibility_count += 1
                elif result.check_name == "Error Handling" and result.status == VerificationStatus.PASS:
                    error_handling_count += 1
                elif result.check_name == "Performance Optimization" and result.status == VerificationStatus.PASS:
                    performance_count += 1
                elif result.check_name == "Code Quality" and result.status in [VerificationStatus.WARNING, VerificationStatus.FAIL]:
                    code_quality_issues += 1
        
        if accessibility_count < len(results) * 0.5:
            recommendations.append("🔧 Improve accessibility by adding ARIA labels, roles, and semantic HTML")
        
        if error_handling_count < len(results) * 0.7:
            recommendations.append("🔧 Enhance error handling with try-catch blocks and proper error states")
        
        if performance_count < len(results) * 0.3:
            recommendations.append("🔧 Consider adding performance optimizations like React.memo, useMemo, useCallback")
        
        if code_quality_issues > len(results) * 0.3:
            recommendations.append("🔧 Clean up debug statements and TODO comments for production readiness")
        
        if not recommendations:
            recommendations.append("✨ Great job! All pages are well-implemented and follow best practices.")
        
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("VERIFICATION COMPLETE")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)

    def run_verification(self):
        """Run the complete verification process"""
        try:
            results = self.verify_all_pages()
            report = self.generate_report(results)
            
            # Write report to file
            report_file = "REMAINING_PAGES_VERIFICATION_REPORT.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"\n📊 Verification complete! Report saved to {report_file}")
            
            # Print summary to console
            print("\n" + "="*60)
            print("QUICK SUMMARY")
            print("="*60)
            
            total_files = len(results)
            overall_score = sum(r.score for r in results.values()) / total_files if total_files > 0 else 0
            
            print(f"Files Verified: {total_files}")
            print(f"Overall Score: {overall_score:.1f}%")
            
            # Status breakdown
            excellent = sum(1 for r in results.values() if r.score >= 90)
            good = sum(1 for r in results.values() if 70 <= r.score < 90)
            needs_work = sum(1 for r in results.values() if r.score < 70)
            
            print(f"Excellent (≥90%): {excellent} files")
            print(f"Good (70-89%): {good} files")  
            print(f"Needs Work (<70%): {needs_work} files")
            
            if overall_score >= 90:
                print("\n🎉 Outstanding! All pages are production-ready!")
            elif overall_score >= 70:
                print("\n👍 Good progress! Minor improvements needed.")
            else:
                print("\n⚠️  Attention required. Several issues need addressing.")
            
            return results
            
        except Exception as e:
            print(f"❌ Error during verification: {str(e)}")
            return {}

def main():
    """Main function"""
    print("🔍 Frontend Pages Verification Tool")
    print("=" * 50)
    
    verifier = PageVerifier()
    results = verifier.run_verification()
    
    if results:
        print(f"\n✅ Verification completed successfully!")
        print(f"📋 Check the detailed report: REMAINING_PAGES_VERIFICATION_REPORT.md")
    else:
        print(f"\n❌ Verification failed!")

if __name__ == "__main__":
    main()
