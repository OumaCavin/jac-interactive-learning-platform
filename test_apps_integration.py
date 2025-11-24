#!/usr/bin/env python3
"""
Django Apps Integration Test
Tests that all enhanced __init__.py files work correctly in a Django environment
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_django_apps_import():
    """Test that all app packages can be imported in a Django environment"""
    print("🧪 Testing Django Apps Integration...")
    
    # Create a test script that imports all apps
    test_script_content = '''
import os
import sys
import django
from django.conf import settings

# Add backend to path
sys.path.insert(0, '/workspace/backend')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🚀 Django Apps Import Test")
print("=" * 50)

# Test each app
apps_to_test = [
    'apps.management',
    'apps.progress', 
    'apps.users',
    'apps.learning'
]

success_count = 0

for app_name in apps_to_test:
    try:
        print(f"🔍 Testing {app_name}...")
        module = __import__(app_name, fromlist=[''])
        
        # Check for essential attributes
        has_docstring = bool(module.__doc__)
        has_default_config = hasattr(module, 'default_app_config')
        has_version = hasattr(module, '__version__')
        has_author = hasattr(module, '__author__')
        
        print(f"  ✅ Import successful")
        print(f"  📝 Docstring: {'✅' if has_docstring else '❌'}")
        print(f"  ⚙️ Default Config: {'✅' if has_default_config else '❌'}")
        print(f"  📦 Version: {'✅' if has_version else '❌'}")
        print(f"  👤 Author: {'✅' if has_author else '❌'}")
        
        if has_default_config:
            config = module.default_app_config
            print(f"  🔧 App Config: {config}")
        
        success_count += 1
        
    except Exception as e:
        print(f"  ❌ Import failed: {str(e)}")

print(f"\\n📊 Results: {success_count}/{len(apps_to_test)} apps imported successfully")

if success_count == len(apps_to_test):
    print("🎉 ALL APPS IMPORTED SUCCESSFULLY!")
    sys.exit(0)
else:
    print("❌ Some apps failed to import")
    sys.exit(1)
'''
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script_content)
        test_file_path = f.name
    
    try:
        # Run the test inside Docker container
        result = subprocess.run([
            'docker-compose', 'exec', '-T', 'backend',
            'python', test_file_path
        ], capture_output=True, text=True, timeout=30)
        
        print("🔍 Test Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Test Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Clean up test file
        try:
            os.unlink(test_file_path)
        except:
            pass

def test_app_configs():
    """Test that Django recognizes all app configurations"""
    print("\\n⚙️ Testing Django App Configurations...")
    
    # Create a test script for app configs
    test_script_content = '''
import os
import sys
import django
from django.apps import apps

# Add backend to path
sys.path.insert(0, '/workspace/backend')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 Django App Configuration Test")
print("=" * 50)

# Test each app config
apps_to_test = [
    ('apps.management', 'ManagementConfig'),
    ('apps.progress', 'ProgressConfig'),
    ('apps.users', 'UsersConfig'),
    ('apps.learning', 'LearningConfig')
]

success_count = 0

for app_path, config_name in apps_to_test:
    try:
        print(f"🔍 Testing {app_path}...")
        
        # Get app config
        app_config = apps.get_app_config(app_path.split('.')[1])
        print(f"  ✅ App found: {app_config.name}")
        print(f"  📋 Config class: {app_config.__class__.__name__}")
        print(f"  🔧 Default field: {app_config.default_auto_field}")
        
        # Check if it matches expected config
        if app_config.__class__.__name__ == config_name:
            print(f"  ✅ Correct config class")
            success_count += 1
        else:
            print(f"  ❌ Expected {config_name}, got {app_config.__class__.__name__}")
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

print(f"\\n📊 Results: {success_count}/{len(apps_to_test)} apps configured correctly")

if success_count == len(apps_to_test):
    print("🎉 ALL APP CONFIGS WORKING!")
    sys.exit(0)
else:
    print("❌ Some app configs failed")
    sys.exit(1)
'''
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script_content)
        test_file_path = f.name
    
    try:
        # Run the test inside Docker container
        result = subprocess.run([
            'docker-compose', 'exec', '-T', 'backend',
            'python', test_file_path
        ], capture_output=True, text=True, timeout=30)
        
        print("🔍 Test Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Test Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Clean up test file
        try:
            os.unlink(test_file_path)
        except:
            pass

def test_middleware_import():
    """Test that middleware can be imported from learning app"""
    print("\\n🛡️ Testing Middleware Import...")
    
    test_script_content = '''
import os
import sys
import django

# Add backend to path
sys.path.insert(0, '/workspace/backend')

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🛡️ Middleware Import Test")
print("=" * 30)

try:
    from apps.learning import MockJWTAuthentication
    print("✅ MockJWTAuthentication imported successfully")
    
    # Test middleware class
    middleware = MockJWTAuthentication()
    print(f"✅ Middleware instance created: {type(middleware).__name__}")
    
    print("🎉 Middleware test passed!")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Middleware import failed: {str(e)}")
    sys.exit(1)
'''
    
    # Create temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script_content)
        test_file_path = f.name
    
    try:
        # Run the test inside Docker container
        result = subprocess.run([
            'docker-compose', 'exec', '-T', 'backend',
            'python', test_file_path
        ], capture_output=True, text=True, timeout=30)
        
        print("🔍 Test Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Test Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    finally:
        # Clean up test file
        try:
            os.unlink(test_file_path)
        except:
            pass

def main():
    """Main test function"""
    print("🧪 DJANGO APPS INTEGRATION TEST SUITE")
    print("=" * 60)
    print("Testing that all enhanced __init__.py files work correctly")
    print("in a live Django environment.")
    print("")
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: App Package Imports
    if test_django_apps_import():
        tests_passed += 1
        print("✅ App imports test PASSED")
    else:
        print("❌ App imports test FAILED")
    
    # Test 2: App Configurations
    if test_app_configs():
        tests_passed += 1
        print("✅ App configurations test PASSED")
    else:
        print("❌ App configurations test FAILED")
    
    # Test 3: Middleware Import
    if test_middleware_import():
        tests_passed += 1
        print("✅ Middleware import test PASSED")
    else:
        print("❌ Middleware import test FAILED")
    
    # Final summary
    print("\\n" + "=" * 60)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print(f"🎯 Tests Passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ All __init__.py files work correctly in Django")
        print("✅ App configurations are properly loaded")
        print("✅ Middleware and imports function correctly")
        print("✅ Package initialization is production-ready")
        print("")
        print("🚀 Your Django apps are fully integrated and working!")
        return 0
    else:
        print("⚠️ SOME INTEGRATION TESTS FAILED")
        print("❌ Issues found with app integration")
        print("🔧 Review test output above for specific problems")
        return 1

if __name__ == "__main__":
    sys.exit(main())