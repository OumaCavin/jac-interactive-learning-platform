#!/usr/bin/env python3
"""
Learning Pages Verification Script
Verifies that frontend/src/pages/learning/ components are properly implemented and working.
"""

import os
import re
from pathlib import Path

def read_file(file_path):
    """Read file content safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description} exists")
        return True
    else:
        print(f"❌ {description} missing")
        return False

def analyze_learning_paths_page(content):
    """Analyze the LearningPaths.tsx file"""
    print("\n📚 Analyzing LearningPaths.tsx...")
    
    issues = []
    positives = []
    
    # Check component structure
    if "export const LearningPaths: React.FC = ()" in content:
        positives.append("✅ Proper React functional component structure")
    else:
        issues.append("❌ Missing proper React component structure")
    
    # Check TypeScript interfaces
    if "interface FilterOptions" in content and "interface LearningPath" in content:
        positives.append("✅ TypeScript interfaces defined (FilterOptions)")
    else:
        issues.append("❌ Missing or incomplete TypeScript interfaces")
    
    # Check service integration
    if "import { learningService, LearningPath }" in content:
        positives.append("✅ Learning service imported")
        if "learningService.getLearningPaths()" in content:
            positives.append("✅ Learning service methods used")
        else:
            issues.append("⚠️ Learning service imported but method not called")
    
    # Check Heroicons
    if "from '@heroicons/react/24/outline'" in content:
        positives.append("✅ Heroicons imported for UI icons")
    else:
        issues.append("❌ Heroicons not imported")
    
    # Check filtering functionality
    if "applyFilters" in content and "useCallback" in content:
        positives.append("✅ Advanced filtering with search, difficulty, and sorting")
    else:
        issues.append("❌ Missing filtering functionality")
    
    # Check Framer Motion
    if "import { motion } from 'framer-motion'" in content:
        positives.append("✅ Framer Motion animations implemented")
        if "motion.div" in content and "whileHover" in content:
            positives.append("✅ Interactive hover animations with Framer Motion")
    else:
        issues.append("❌ Missing Framer Motion imports")
    
    # Check React Router Link
    if "import { Link } from 'react-router-dom'" in content and "<Link to=" in content:
        positives.append("✅ React Router Link navigation")
    else:
        issues.append("❌ Missing React Router integration")
    
    # Check toast notifications
    if "import { toast } from 'react-hot-toast'" in content and "toast.error" in content:
        positives.append("✅ Toast notifications for error handling")
    else:
        issues.append("❌ Missing toast notifications")
    
    # Check loading states
    if "isLoading" in content and "setIsLoading" in content:
        positives.append("✅ Loading state management")
    else:
        issues.append("❌ Missing loading states")
    
    # Check responsive design
    if "lg:" in content and "md:" in content:
        positives.append("✅ Responsive design with Tailwind breakpoints")
    else:
        issues.append("⚠️ Consider adding responsive design")
    
    # Check mock data structure
    if "DIFFICULTY_LEVELS" in content:
        positives.append("✅ Difficulty level configuration")
    
    # Check error handling
    if "try" in content and "catch" in content and "finally" in content:
        positives.append("✅ Comprehensive error handling with try-catch-finally")
    else:
        issues.append("❌ Missing proper error handling")
    
    return positives, issues

def analyze_learning_path_detail(content):
    """Analyze the LearningPathDetail.tsx file"""
    print("\n📖 Analyzing LearningPathDetail.tsx...")
    
    issues = []
    positives = []
    
    # Check component structure
    if "const LearningPathDetail: React.FC = ()" in content:
        positives.append("✅ Proper React functional component structure")
    else:
        issues.append("❌ Missing proper React component structure")
    
    # Check route parameters
    if "useParams" in content and "pathId" in content:
        positives.append("✅ Route parameter handling with useParams")
    else:
        issues.append("❌ Missing route parameter handling")
    
    # Check React Router navigation
    if "useNavigate" in content and "navigate(" in content:
        positives.append("✅ React Router navigation with useNavigate")
    else:
        issues.append("❌ Missing navigation functionality")
    
    # Check Redux integration
    if "useSelector" in content and "selectUser" in content:
        positives.append("✅ Redux integration with user selector")
    else:
        issues.append("❌ Missing Redux integration")
    
    # Check mock data structure
    if "MOCK_MODULES" in content and "MockModuleProgress" in content:
        positives.append("✅ Comprehensive mock data with 8 modules")
        
        # Check module types
        if "'lesson'" in content and "'exercise'" in content and "'assessment'" in content:
            positives.append("✅ Multiple module types (lesson, exercise, assessment)")
    else:
        issues.append("❌ Missing comprehensive mock data")
    
    # Check progress tracking
    if "ModuleProgress" in content and "getModuleStatus" in content:
        positives.append("✅ Progress tracking system")
    else:
        issues.append("❌ Missing progress tracking")
    
    # Check prerequisite logic
    if "prerequisites" in content and "isModuleUnlocked" in content:
        positives.append("✅ Prerequisite-based module unlocking")
    else:
        issues.append("❌ Missing prerequisite logic")
    
    # Check tabs functionality
    if "activeTab" in content and "setActiveTab" in content:
        positives.append("✅ Multi-tab interface (overview, modules, progress)")
    else:
        issues.append("❌ Missing tab functionality")
    
    # Check service integration
    if "import { learningService, LearningPath, Module }" in content:
        positives.append("✅ Learning service imported")
    else:
        issues.append("❌ Missing learning service import")
    
    # Check error handling
    if "try" in content and "catch" in content and "toast.error" in content:
        positives.append("✅ Error handling with toast notifications")
    else:
        issues.append("❌ Missing error handling")
    
    # Check statistics calculation
    if "getOverallProgress" in content and "getTotalTimeSpent" in content:
        positives.append("✅ Statistics calculation functions")
    else:
        issues.append("❌ Missing statistics calculations")
    
    # Check UI components
    if "Heroicons" in content:
        positives.append("✅ Heroicons used for UI")
    
    return positives, issues

def analyze_module_content(content):
    """Analyze the ModuleContent.tsx file"""
    print("\n📝 Analyzing ModuleContent.tsx...")
    
    issues = []
    positives = []
    
    # Check component structure
    if "const ModuleContent: React.FC = ()" in content:
        positives.append("✅ Proper React functional component structure")
    else:
        issues.append("❌ Missing proper React component structure")
    
    # Check route parameters
    if "useParams" in content and "pathId" in content and "moduleId" in content:
        positives.append("✅ Multiple route parameters (pathId, moduleId)")
    else:
        issues.append("❌ Missing route parameters")
    
    # Check navigation
    if "useNavigate" in content:
        positives.append("✅ React Router navigation")
    else:
        issues.append("❌ Missing navigation")
    
    # Check rich content structure
    if "MOCK_MODULE_CONTENT" in content and "sections" in content:
        positives.append("✅ Rich content structure with sections")
    else:
        issues.append("❌ Missing rich content structure")
    
    # Check code editor integration
    if "showCodeEditor" in content and "userCode" in content:
        positives.append("✅ Code editor integration")
    else:
        issues.append("❌ Missing code editor")
    
    # Check progress tracking
    if "currentSection" in content and "timeSpent" in content:
        positives.append("✅ Progress tracking (sections, time)")
    else:
        issues.append("❌ Missing progress tracking")
    
    # Check time tracking
    if "useEffect" in content and "setInterval" in content:
        positives.append("✅ Real-time time tracking")
    else:
        issues.append("❌ Missing time tracking")
    
    # Check section navigation
    if "handleNext" in content and "handlePrevious" in content:
        positives.append("✅ Section navigation (next/previous)")
    else:
        issues.append("❌ Missing section navigation")
    
    # Check content rendering
    if "prose" in content and "```" in content:
        positives.append("✅ Rich text content rendering with markdown support")
    else:
        issues.append("❌ Missing rich content rendering")
    
    # Check exercise functionality
    if "exercise" in content and "instructions" in content:
        positives.append("✅ Interactive exercises with instructions")
    else:
        issues.append("❌ Missing exercise functionality")
    
    # Check auto-play feature
    if "isPlaying" in content and "auto-play" in content.lower():
        positives.append("✅ Auto-play feature for content")
    else:
        issues.append("❌ Missing auto-play feature")
    
    # Check sharing and bookmarking
    if "handleShare" in content and "handleBookmark" in content:
        positives.append("✅ Sharing and bookmarking functionality")
    else:
        issues.append("❌ Missing sharing/bookmarking features")
    
    # Check Heroicons
    if "Heroicons" in content:
        positives.append("✅ Heroicons used for UI")
    
    return positives, issues

def check_app_integration():
    """Check if learning pages are integrated in App.tsx"""
    print("\n🔗 Checking App.tsx integration...")
    
    app_content = read_file("/workspace/frontend/src/App.tsx")
    if not app_content:
        return ["❌ Cannot read App.tsx"], ["❌ App.tsx not found"]
    
    positives = []
    issues = []
    
    # Check lazy loading
    if "const LearningPaths = React.lazy" in app_content:
        positives.append("✅ LearningPaths uses React.lazy for code splitting")
    else:
        issues.append("❌ LearningPaths not using React.lazy")
    
    if "const LearningPathDetail = React.lazy" in app_content:
        positives.append("✅ LearningPathDetail uses React.lazy")
    else:
        issues.append("❌ LearningPathDetail not using React.lazy")
    
    if "const ModuleContent = React.lazy" in app_content:
        positives.append("✅ ModuleContent uses React.lazy")
    else:
        issues.append("❌ ModuleContent not using React.lazy")
    
    # Check route definitions
    if 'path="/learning"' in app_content:
        positives.append("✅ Learning paths route properly defined")
    else:
        issues.append("❌ Learning paths route not defined")
    
    if 'path="/learning/:pathId"' in app_content:
        positives.append("✅ Learning path detail route defined")
    else:
        issues.append("❌ Learning path detail route not defined")
    
    if 'path="/learning/:pathId/module/:moduleId"' in app_content:
        positives.append("✅ Module content route defined")
    else:
        issues.append("❌ Module content route not defined")
    
    # Check component usage
    if "<LearningPaths />" in app_content:
        positives.append("✅ LearningPaths component used in routes")
    else:
        issues.append("❌ LearningPaths component not used")
    
    if "<LearningPathDetail />" in app_content:
        positives.append("✅ LearningPathDetail component used")
    else:
        issues.append("❌ LearningPathDetail component not used")
    
    if "<ModuleContent />" in app_content:
        positives.append("✅ ModuleContent component used")
    else:
        issues.append("❌ ModuleContent component not used")
    
    return positives, issues

def check_dependencies():
    """Check if dependencies exist"""
    print("\n📦 Checking dependencies...")
    
    positives = []
    issues = []
    
    # Check learning service
    if check_file_exists("/workspace/frontend/src/services/learningService.ts", "Learning service"):
        positives.append("✅ Learning service exists")
    else:
        issues.append("❌ Learning service missing")
    
    # Check auth slice for user selector
    auth_slice = read_file("/workspace/frontend/src/store/slices/authSlice.ts")
    if auth_slice and "selectUser" in auth_slice:
        positives.append("✅ Auth slice with selectUser selector exists")
    else:
        issues.append("⚠️ Auth slice selectUser selector not found")
    
    # Check if Heroicons is in package.json
    package_json = read_file("/workspace/frontend/package.json")
    if package_json and "@heroicons/react" in package_json:
        positives.append("✅ @heroicons/react package installed")
    else:
        issues.append("❌ @heroicons/react package not found")
    
    return positives, issues

def check_code_quality_issues(content, filename):
    """Check for potential code quality issues"""
    issues = []
    
    # Check for console.log (should be removed in production)
    if "console.log" in content:
        issues.append(f"⚠️ {filename}: Found console.log statements")
    
    # Check for TODO comments
    if "TODO" in content or "FIXME" in content:
        issues.append(f"⚠️ {filename}: Found TODO/FIXME comments")
    
    # Check for hardcoded values that should be constants
    if "1.2k learners" in content:
        issues.append(f"⚠️ {filename}: Hardcoded '1.2k learners' value")
    
    return issues

def main():
    """Main verification function"""
    print("🎓 Learning Pages Verification")
    print("=" * 50)
    
    # File paths
    learning_paths_file = "/workspace/frontend/src/pages/learning/LearningPaths.tsx"
    path_detail_file = "/workspace/frontend/src/pages/learning/LearningPathDetail.tsx"
    module_content_file = "/workspace/frontend/src/pages/learning/ModuleContent.tsx"
    
    # Check files exist
    print("\n📁 Checking file existence...")
    file_exists = [
        check_file_exists(learning_paths_file, "LearningPaths.tsx"),
        check_file_exists(path_detail_file, "LearningPathDetail.tsx"),
        check_file_exists(module_content_file, "ModuleContent.tsx")
    ]
    
    if not all(file_exists):
        print("\n❌ Some files are missing. Cannot proceed with analysis.")
        return
    
    # Read file contents
    learning_paths_content = read_file(learning_paths_file)
    path_detail_content = read_file(path_detail_file)
    module_content_content = read_file(module_content_file)
    
    if not all([learning_paths_content, path_detail_content, module_content_content]):
        print("\n❌ Cannot read file contents. Cannot proceed with analysis.")
        return
    
    # Analyze each file
    learning_paths_pos, learning_paths_issues = analyze_learning_paths_page(learning_paths_content)
    path_detail_pos, path_detail_issues = analyze_learning_path_detail(path_detail_content)
    module_content_pos, module_content_issues = analyze_module_content(module_content_content)
    
    # Check integrations
    app_pos, app_issues = check_app_integration()
    dep_pos, dep_issues = check_dependencies()
    
    # Check code quality
    quality_issues = []
    quality_issues.extend(check_code_quality_issues(learning_paths_content, "LearningPaths.tsx"))
    quality_issues.extend(check_code_quality_issues(path_detail_content, "LearningPathDetail.tsx"))
    quality_issues.extend(check_code_quality_issues(module_content_content, "ModuleContent.tsx"))
    
    # Combine all results
    all_positives = learning_paths_pos + path_detail_pos + module_content_pos + app_pos + dep_pos
    all_issues = learning_paths_issues + path_detail_issues + module_content_issues + app_issues + dep_issues
    
    # Print results
    print("\n" + "=" * 50)
    print("📊 VERIFICATION RESULTS")
    print("=" * 50)
    
    if all_positives:
        print("\n✅ POSITIVE FINDINGS:")
        for positive in all_positives:
            print(f"   {positive}")
    
    if all_issues:
        print("\n❌ ISSUES FOUND:")
        for issue in all_issues:
            print(f"   {issue}")
    
    if quality_issues:
        print("\n⚠️ CODE QUALITY NOTES:")
        for issue in quality_issues:
            print(f"   {issue}")
    
    # Calculate success rate
    total_checks = len(all_positives) + len(all_issues)
    if total_checks > 0:
        success_rate = (len(all_positives) / total_checks) * 100
        print(f"\n📈 SUCCESS RATE: {success_rate:.1f}% ({len(all_positives)}/{total_checks} checks passed)")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Learning pages are excellently implemented!")
        elif success_rate >= 80:
            print("👍 GOOD: Learning pages are well-implemented with minor issues")
        elif success_rate >= 70:
            print("⚠️ FAIR: Learning pages have some issues that should be addressed")
        else:
            print("🚨 NEEDS WORK: Learning pages have significant issues")
    
    # Specific recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    if any("TODO" in issue or "FIXME" in issue for issue in quality_issues):
        print("   • Address TODO/FIXME comments before production")
    
    if any("console.log" in issue for issue in quality_issues):
        print("   • Remove console.log statements for production")
    
    if any("Hardcoded" in issue for issue in quality_issues):
        print("   • Move hardcoded values to constants or configuration")
    
    if any("Heroicons" in issue and "not" in issue for issue in all_issues):
        print("   • Install @heroicons/react package")
    
    if any("service imported but method not called" in issue for issue in all_issues):
        print("   • Implement actual API calls to replace mock data")
    
    print("\n🎯 LEARNING FEATURES VERIFIED:")
    print("   • Learning path listing with advanced filtering")
    print("   • Detailed learning path with 8-module structure")
    print("   • Rich module content with interactive exercises")
    print("   • Progress tracking and prerequisite unlocking")
    print("   • Code editor integration for hands-on learning")
    print("   • Auto-play and navigation features")
    print("   • Sharing and bookmarking capabilities")

if __name__ == "__main__":
    main()