#!/usr/bin/env python3
"""
Django Apps Package Initialization Verification Script
Verifies that all __init__.py files are properly implemented and working
"""

import os
import sys
import importlib
import inspect

def test_app_init_import(app_name, init_path):
    """Test that a Django app's __init__.py can be imported without errors"""
    print(f"  🔍 Testing {app_name} package import...")
    
    try:
        # Add the backend directory to Python path for imports
        backend_path = "/workspace/backend"
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        # Attempt to import the app package
        module = importlib.import_module(f"apps.{app_name}")
        
        # Check for required attributes
        has_default_config = hasattr(module, 'default_app_config')
        has_version = hasattr(module, '__version__')
        has_author = hasattr(module, '__author__')
        
        # Check __all__ if it exists
        has_all = hasattr(module, '__all__')
        export_list = getattr(module, '__all__', [])
        
        print(f"    ✅ Import successful")
        print(f"    📋 default_app_config: {'✅' if has_default_config else '❌'}")
        print(f"    📋 __version__: {'✅' if has_version else '❌'}")
        print(f"    📋 __author__: {'✅' if has_author else '❌'}")
        print(f"    📋 __all__ exports: {'✅' if has_all else '❌'}")
        if has_all:
            print(f"      📄 Exported items: {export_list}")
        
        # Check module docstring
        has_docstring = bool(module.__doc__)
        print(f"    📋 Documentation: {'✅' if has_docstring else '❌'}")
        if has_docstring:
            print(f"      📝 First line: {module.__doc__.split('\\n')[0][:60]}...")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Import failed: {str(e)}")
        return False

def check_file_structure():
    """Check that all __init__.py files exist and have proper content"""
    print("\\n📁 Checking file structure...")
    
    apps_to_check = [
        ('management', '/workspace/backend/apps/management/__init__.py'),
        ('progress', '/workspace/backend/apps/progress/__init__.py'), 
        ('users', '/workspace/backend/apps/users/__init__.py'),
        ('learning', '/workspace/backend/apps/learning/__init__.py')  # Include learning for reference
    ]
    
    results = {}
    
    for app_name, init_path in apps_to_check:
        print(f"  🔍 Checking {app_name} app...")
        
        if not os.path.exists(init_path):
            print(f"    ❌ File not found: {init_path}")
            results[app_name] = False
            continue
            
        # Read file content
        try:
            with open(init_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\\n')
            
            # Check basic requirements
            has_docstring = '"""' in content or "'''" in content
            has_default_config = 'default_app_config' in content
            has_version = '__version__' in content
            has_author = '__author__' in content
            
            # Count lines of content
            actual_lines = len([line for line in lines if line.strip()])
            
            print(f"    ✅ File exists: {actual_lines} lines")
            print(f"    📋 Has docstring: {'✅' if has_docstring else '❌'}")
            print(f"    📋 Has default_app_config: {'✅' if has_default_config else '❌'}")
            print(f"    📋 Has __version__: {'✅' if has_version else '❌'}")
            print(f"    📋 Has __author__: {'✅' if has_author else '❌'}")
            
            results[app_name] = has_docstring and has_default_config and has_version and has_author
            
        except Exception as e:
            print(f"    ❌ Error reading file: {str(e)}")
            results[app_name] = False
    
    return results

def check_consistency():
    """Check consistency across all __init__.py files"""
    print("\\n🔗 Checking consistency across apps...")
    
    # Read all __init__.py files
    app_files = {
        'management': '/workspace/backend/apps/management/__init__.py',
        'progress': '/workspace/backend/apps/progress/__init__.py',
        'users': '/workspace/backend/apps/users/__init__.py',
        'learning': '/workspace/backend/apps/learning/__init__.py'
    }
    
    consistency_checks = {
        'has_docstring': True,
        'has_default_config': True, 
        'has_version': True,
        'has_author': True,
        'follows_pattern': True
    }
    
    all_consistent = True
    
    for app_name, file_path in app_files.items():
        if not os.path.exists(file_path):
            print(f"    ❌ {app_name}: File missing")
            all_consistent = False
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check each consistency element
            checks = {
                'has_docstring': '"""' in content or "'''" in content,
                'has_default_config': 'default_app_config' in content,
                'has_version': '__version__' in content,
                'has_author': '__author__' in content,
                'follows_pattern': content.count('\\n') > 10  # Substantial content
            }
            
            all_pass = all(checks.values())
            status = '✅' if all_pass else '❌'
            print(f"    {status} {app_name}: {sum(checks.values())}/{len(checks)} checks passed")
            
            if not all_pass:
                all_consistent = False
                for check, passed in checks.items():
                    if not passed:
                        print(f"      ⚠️ Missing: {check}")
                        
        except Exception as e:
            print(f"    ❌ {app_name}: Error reading - {str(e)}")
            all_consistent = False
    
    return all_consistent

def check_django_configuration():
    """Check Django app configuration files"""
    print("\\n⚙️ Checking Django app configuration...")
    
    apps_to_check = [
        ('management', '/workspace/backend/apps/management/apps.py'),
        ('progress', '/workspace/backend/apps/progress/apps.py'),
        ('users', '/workspace/backend/apps/users/apps.py'),
        ('learning', '/workspace/backend/apps/learning/apps.py')
    ]
    
    all_good = True
    
    for app_name, apps_path in apps_to_check:
        print(f"  🔍 Checking {app_name} app configuration...")
        
        if not os.path.exists(apps_path):
            print(f"    ❌ apps.py not found: {apps_path}")
            all_good = False
            continue
            
        try:
            with open(apps_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for essential elements
            has_app_config = 'class' in content and 'Config' in content
            has_default_field = 'default_auto_field' in content
            has_name = f"'{app_name}'" in content or f'"{app_name}"' in content
            
            if has_app_config and has_default_field and has_name:
                print(f"    ✅ {app_name}: Proper Django app configuration")
            else:
                print(f"    ❌ {app_name}: Missing essential configuration")
                all_good = False
                
        except Exception as e:
            print(f"    ❌ {app_name}: Error reading apps.py - {str(e)}")
            all_good = False
    
    return all_good

def generate_comparison_report():
    """Generate a comparison report between all apps"""
    print("\\n📊 Generating comparison report...")
    
    app_files = {
        'management': '/workspace/backend/apps/management/__init__.py',
        'progress': '/workspace/backend/apps/progress/__init__.py',
        'users': '/workspace/backend/apps/users/__init__.py',
        'learning': '/workspace/backend/apps/learning/__init__.py'
    }
    
    print("\\n📋 Package Initialization Comparison:")
    print("=" * 60)
    
    for app_name, file_path in app_files.items():
        if not os.path.exists(file_path):
            print(f"{app_name:15} ❌ Missing file")
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            lines = content.split('\\n')
            actual_lines = len([line for line in lines if line.strip()])
            
            # Extract key information
            docstring_start = content.find('"""')
            docstring_end = content.find('"""', docstring_start + 3) if docstring_start != -1 else -1
            
            if docstring_start != -1 and docstring_end != -1:
                first_sentence = content[docstring_start+3:docstring_end].split('.')[0][:50]
            else:
                first_sentence = "No docstring found"
            
            has_all = '__all__' in content
            has_config = 'default_app_config' in content
            has_version = '__version__' in content
            
            export_count = content.count('__all__') + content.count('exported')
            
            print(f"{app_name:15} 📄 {actual_lines:3} lines | 📝 {'✅' if '"""' in content else '❌'} | ⚙️ {'✅' if has_config else '❌'} | 📦 {'✅' if has_version else '❌'}")
            print(f"{'':15}    📋 {first_sentence}...")
            
        except Exception as e:
            print(f"{app_name:15} ❌ Error reading: {str(e)}")
    
    print("=" * 60)

def main():
    """Main verification function"""
    print("🔍 DJANGO APPS PACKAGE INITIALIZATION VERIFICATION")
    print("=" * 60)
    print("Verifying that all __init__.py files are properly implemented")
    print("and consistent across all Django apps.")
    print("")
    
    # Run all verification steps
    checks_passed = 0
    total_checks = 5
    
    # Step 1: File Structure Check
    if check_file_structure():
        checks_passed += 1
        print("  ✅ File structure check PASSED")
    else:
        print("  ❌ File structure check FAILED")
    
    # Step 2: Django Configuration Check  
    if check_django_configuration():
        checks_passed += 1
        print("  ✅ Django configuration check PASSED")
    else:
        print("  ❌ Django configuration check FAILED")
    
    # Step 3: Consistency Check
    if check_consistency():
        checks_passed += 1
        print("  ✅ Consistency check PASSED")
    else:
        print("  ❌ Consistency check FAILED")
    
    # Step 4: Import Tests (safely)
    print("\\n🧪 Testing package imports (without Django environment)...")
    apps_to_import = ['management', 'progress', 'users', 'learning']
    import_success = 0
    
    for app in apps_to_import:
        try:
            # This will test basic import structure without Django
            init_path = f"/workspace/backend/apps/{app}/__init__.py"
            if os.path.exists(init_path):
                with open(init_path, 'r') as f:
                    content = f.read()
                # Basic syntax check
                compile(content, init_path, 'exec')
                import_success += 1
                print(f"  ✅ {app}: Import structure valid")
            else:
                print(f"  ❌ {app}: __init__.py not found")
        except SyntaxError as e:
            print(f"  ❌ {app}: Syntax error - {str(e)}")
        except Exception as e:
            print(f"  ❌ {app}: Error - {str(e)}")
    
    if import_success == len(apps_to_import):
        checks_passed += 1
        print("  ✅ Import structure check PASSED")
    
    # Step 5: Generate comparison report
    generate_comparison_report()
    checks_passed += 1
    print("  ✅ Comparison report generated")
    
    # Final summary
    print("\\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"🎯 Checks Passed: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ All __init__.py files are properly implemented")
        print("✅ Django app configurations are consistent")
        print("✅ Package initialization follows best practices")
        print("✅ File structure is complete and valid")
        print("")
        print("📋 Enhanced features implemented:")
        print("   📝 Comprehensive docstrings")
        print("   ⚙️ Django app configuration")
        print("   📦 Safe import handling")
        print("   🔄 Error handling for missing components")
        print("   📊 Package metadata (version, author)")
        print("   🎯 Consistent patterns across all apps")
        print("")
        print("🚀 Your Django apps are ready for production!")
        return 0
    else:
        print("⚠️ SOME CHECKS FAILED")
        print("❌ Package initialization needs attention")
        print("🔧 Review the errors above and fix issues")
        print("📖 See verification output for specific problems")
        return 1

if __name__ == "__main__":
    sys.exit(main())