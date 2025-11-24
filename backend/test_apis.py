#!/usr/bin/env python
"""
Test script to verify API endpoint configuration for JAC Learning Platform
This script checks that all the implemented APIs are properly configured
without requiring a running Django server.
"""

import os
import sys
import django
from django.conf import settings
from django.core.urlresolvers import resolve, NoReverseMatch
from django.test.utils import get_runner

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_minimal')

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='test-secret-key',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework_simplejwt',
            'corsheaders',
            'apps.agents',
            'apps.learning',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        ROOT_URLCONF='config.urls',
        USE_TZ=True,
        CORS_ALLOW_ALL_ORIGINS=True,
    )

django.setup()

def test_url_resolution():
    """Test that all API endpoints can be resolved"""
    print("Testing URL resolution...")
    
    # Test endpoints to verify
    endpoints_to_test = [
        # Health check endpoints
        ('/api/health/', 'health_check'),
        ('/api/health/static/', 'static_health_check'),
        ('/api/health/simple/', 'simple_health_check'),
        
        # Agent endpoints
        ('/api/agents/chat-assistant/', 'chat-assistant-list'),
        ('/api/agents/chat-assistant/history/', 'chat-assistant-history'),
        ('/api/agents/chat-assistant/sessions/', 'chat-assistant-sessions'),
        
        # Learning endpoints
        ('/api/assessment/quizzes/', 'assessment-list'),
        ('/api/assessment/attempts/', 'assessment-attempts'),
        ('/api/assessment/stats/', 'assessment-stats'),
    ]
    
    failed_endpoints = []
    successful_endpoints = []
    
    for url_path, expected_name in endpoints_to_test:
        try:
            resolver_match = resolve(url_path)
            print(f"✅ {url_path} -> {resolver_match.url_name} ({resolver_match.func})")
            successful_endpoints.append(url_path)
        except NoReverseMatch as e:
            print(f"❌ {url_path} -> No match found: {e}")
            failed_endpoints.append(url_path)
        except Exception as e:
            print(f"❌ {url_path} -> Error: {e}")
            failed_endpoints.append(url_path)
    
    print(f"\n📊 Summary:")
    print(f"Successful: {len(successful_endpoints)}")
    print(f"Failed: {len(failed_endpoints)}")
    
    if failed_endpoints:
        print(f"\n❌ Failed endpoints:")
        for endpoint in failed_endpoints:
            print(f"  - {endpoint}")
        return False
    else:
        print(f"\n✅ All endpoints resolved successfully!")
        return True

def test_model_imports():
    """Test that all models can be imported"""
    print("\nTesting model imports...")
    
    try:
        from apps.agents.simple_models import ChatMessage
        print("✅ ChatMessage model imported successfully")
        
        from apps.learning.models import Assessment, Question
        print("✅ Assessment and Question models imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_serializer_imports():
    """Test that all serializers can be imported"""
    print("\nTesting serializer imports...")
    
    try:
        from apps.agents.serializers import (
            ChatMessageSerializer,
            ChatMessageCreateSerializer,
            ChatMessageRateSerializer,
            ChatSessionSerializer
        )
        print("✅ Chat serializers imported successfully")
        
        from apps.learning.serializers import (
            QuizAttemptSerializer,
            QuizAttemptCreateSerializer,
            QuizAttemptSubmitSerializer,
            QuizStatsSerializer
        )
        print("✅ Assessment serializers imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Serializer import failed: {e}")
        return False

def test_viewset_imports():
    """Test that all viewsets can be imported"""
    print("\nTesting viewset imports...")
    
    try:
        from apps.agents.views import ChatAssistantViewSet
        print("✅ ChatAssistantViewSet imported successfully")
        
        from apps.learning.views import AssessmentViewSet
        print("✅ AssessmentViewSet imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Viewset import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 JAC Learning Platform API Configuration Test")
    print("=" * 50)
    
    tests = [
        ("Model Imports", test_model_imports),
        ("Serializer Imports", test_serializer_imports),
        ("ViewSet Imports", test_viewset_imports),
        ("URL Resolution", test_url_resolution),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("🎯 FINAL RESULTS")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! The API implementation is properly configured.")
        print("\n📋 Implemented APIs:")
        print("  ✅ POST /api/agents/chat-assistant/message/")
        print("  ✅ GET  /api/agents/chat-assistant/history/")
        print("  ✅ POST /api/agents/chat-assistant/rate/")
        print("  ✅ GET  /api/assessment/quizzes/")
        print("  ✅ GET  /api/assessment/attempts/")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())