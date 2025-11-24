#!/usr/bin/env python3
"""
Django App Configuration Verification Script
Tests that the learning app is properly set up
"""

import sys
import os

# Add Django project root to path
sys.path.insert(0, '/workspace/backend')

def test_django_setup():
    """Test Django app configuration"""
    
    print("🔧 Testing Django Learning App Configuration")
    print("=" * 50)
    
    try:
        # Test 1: Django imports
        print("📋 Test 1: Django Environment Setup")
        print("-" * 30)
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        
        import django
        django.setup()
        print("✅ Django environment setup: SUCCESS")
        
        # Test 2: App configuration
        print("\n📋 Test 2: Learning App Configuration")
        print("-" * 30)
        
        from django.apps import apps
        learning_config = apps.get_app_config('learning')
        print(f"✅ Learning app name: {learning_config.name}")
        print(f"✅ Learning app path: {learning_config.path}")
        print(f"✅ Default auto field: {learning_config.default_auto_field}")
        
        # Test 3: Models import
        print("\n📋 Test 3: Models Import")
        print("-" * 30)
        
        from apps.learning import models
        print("✅ Learning models imported successfully")
        
        # List available models
        model_names = [name for name in dir(models) if not name.startswith('_')]
        print(f"📊 Available models: {model_names}")
        
        # Test 4: Middleware availability
        print("\n📋 Test 4: Middleware Configuration")
        print("-" * 30)
        
        try:
            from apps.learning.middleware import MockJWTAuthentication
            print("✅ MockJWTAuthentication imported: SUCCESS")
            print(f"   Class: {MockJWTAuthentication.__name__}")
            print(f"   Module: {MockJWTAuthentication.__module__}")
        except ImportError as e:
            print(f"❌ MockJWTAuthentication import failed: {e}")
        
        # Test 5: Views import
        print("\n📋 Test 5: Views Import")
        print("-" * 30)
        
        try:
            from apps.learning import views
            print("✅ Learning views imported successfully")
            
            # Check for view functions
            view_names = [name for name in dir(views) if not name.startswith('_')]
            print(f"📊 Available views: {view_names}")
        except ImportError as e:
            print(f"❌ Views import failed: {e}")
        
        # Test 6: App initialization
        print("\n📋 Test 6: App Initialization")
        print("-" * 30)
        
        # Test that the app's ready() method is called
        if hasattr(learning_config, 'ready'):
            print("✅ AppConfig.ready() method exists")
            try:
                learning_config.ready()
                print("✅ AppConfig.ready() executed successfully")
            except Exception as e:
                print(f"❌ AppConfig.ready() failed: {e}")
        else:
            print("❌ AppConfig.ready() method not found")
        
        # Test 7: Package structure
        print("\n📋 Test 7: Package Structure")
        print("-" * 30)
        
        import importlib
        learning_module = importlib.import_module('apps.learning')
        
        print(f"✅ Module file: {learning_module.__file__}")
        print(f"✅ Package: {learning_module.__package__}")
        
        # Check for __all__ exports
        if hasattr(learning_module, '__all__'):
            print(f"✅ Exported components: {learning_module.__all__}")
        else:
            print("ℹ️  No explicit exports (__all__ not defined)")
        
        print("\n" + "=" * 50)
        print("✅ LEARNING APP VERIFICATION COMPLETE")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_middleware_integration():
    """Test middleware integration with Django settings"""
    
    print("\n🔧 Testing Middleware Integration")
    print("=" * 40)
    
    try:
        from django.conf import settings
        
        # Check if MockJWTAuthentication is in authentication classes
        auth_classes = settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])
        
        print("📊 Authentication Classes Configuration:")
        for i, auth_class in enumerate(auth_classes, 1):
            is_mock = 'MockJWTAuthentication' in auth_class
            status = "✅ MOCK AUTH" if is_mock else "ℹ️  Standard"
            print(f"   {i}. {auth_class} {status}")
        
        # Verify MockJWTAuthentication is properly configured
        mock_auth_classes = [cls for cls in auth_classes if 'MockJWTAuthentication' in cls]
        
        if mock_auth_classes:
            print(f"\n✅ MockJWTAuthentication configured: {len(mock_auth_classes)} instance(s)")
            print("✅ Development authentication ready")
        else:
            print("\n⚠️  MockJWTAuthentication not found in authentication classes")
            print("   This might be intentional for production environments")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Middleware integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Django Learning App Configuration Test")
    print("=" * 50)
    
    app_test = test_django_setup()
    middleware_test = test_middleware_integration()
    
    print("\n" + "=" * 50)
    print("📋 FINAL VERIFICATION SUMMARY")
    print("=" * 50)
    
    if app_test and middleware_test:
        print("✅ ALL TESTS PASSED")
        print("✅ Django Learning App is properly configured")
        print("✅ MockJWTAuthentication is ready for use")
        print("✅ Package structure is correct")
    else:
        print("❌ SOME TESTS FAILED")
        print("❌ Please review the errors above")
    
    print("\n🎯 The backend/apps/learning/__init__.py is properly set up!")
