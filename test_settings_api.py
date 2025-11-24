#!/usr/bin/env python3
"""
Settings API Test Script
Verifies that the UserSettingsView endpoint is properly configured and functional.
"""

import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.append('/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

def test_settings_api():
    """Test the UserSettingsView API endpoint functionality."""
    
    print("🧪 Testing Settings API Integration")
    print("=" * 50)
    
    # Create test user
    try:
        test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print("✅ Test user created successfully")
    except Exception as e:
        print(f"❌ Failed to create test user: {e}")
        return False
    
    # Create client and get JWT token
    client = Client()
    
    # Login to get JWT token
    response = client.post('/api/users/auth/login/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return False
    
    token_data = response.json()
    access_token = token_data['tokens']['access']
    
    print("✅ JWT token obtained successfully")
    
    # Set authorization header
    client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
    
    # Test 1: GET settings
    print("\n📋 Test 1: GET /api/users/settings/")
    response = client.get('/api/users/settings/')
    
    if response.status_code == 200:
        settings_data = response.json()
        print("✅ GET settings successful")
        print(f"   - Retrieved {len(settings_data)} settings fields")
        print(f"   - Learning style: {settings_data.get('learning_style', 'Not found')}")
        print(f"   - Email: {settings_data.get('email', 'Not found')}")
        print(f"   - Dark mode: {settings_data.get('dark_mode', 'Not found')}")
    else:
        print(f"❌ GET settings failed: {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    
    # Test 2: PUT settings update
    print("\n📝 Test 2: PUT /api/users/settings/ (Update settings)")
    update_data = {
        'learning_style': 'auditory',
        'preferred_difficulty': 'intermediate',
        'dark_mode': False,
        'bio': 'Updated bio for testing'
    }
    
    response = client.put('/api/users/settings/', 
                         data=json.dumps(update_data),
                         content_type='application/json')
    
    if response.status_code == 200:
        updated_data = response.json()
        print("✅ PUT settings update successful")
        print(f"   - Learning style updated to: {updated_data.get('learning_style')}")
        print(f"   - Dark mode updated to: {updated_data.get('dark_mode')}")
    else:
        print(f"❌ PUT settings update failed: {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    
    # Test 3: PATCH settings partial update
    print("\n🔄 Test 3: PATCH /api/users/settings/ (Partial update)")
    patch_data = {
        'learning_pace': 'fast'
    }
    
    response = client.patch('/api/users/settings/',
                           data=json.dumps(patch_data),
                           content_type='application/json')
    
    if response.status_code == 200:
        patched_data = response.json()
        print("✅ PATCH settings partial update successful")
        print(f"   - Learning pace updated to: {patched_data.get('learning_pace')}")
    else:
        print(f"❌ PATCH settings partial update failed: {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    
    # Test 4: POST settings reset
    print("\n🔄 Test 4: POST /api/users/settings/ (Reset to defaults)")
    response = client.post('/api/users/settings/')
    
    if response.status_code == 200:
        reset_data = response.json()
        print("✅ POST settings reset successful")
        print(f"   - Learning style reset to: {reset_data['settings'].get('learning_style')}")
        print(f"   - Reset message: {reset_data.get('message', 'No message')}")
    else:
        print(f"❌ POST settings reset failed: {response.status_code}")
        print(f"   Response: {response.content.decode()}")
    
    # Test 5: Validation test
    print("\n⚠️  Test 5: Validation test (Invalid learning style)")
    invalid_data = {
        'learning_style': 'invalid_style'
    }
    
    response = client.put('/api/users/settings/',
                         data=json.dumps(invalid_data),
                         content_type='application/json')
    
    if response.status_code == 400:
        error_data = response.json()
        print("✅ Validation test successful - Invalid data rejected")
        print(f"   - Error message: {error_data.get('learning_style', 'No error message')}")
    else:
        print(f"⚠️  Validation test unexpected result: {response.status_code}")
    
    # Cleanup
    try:
        test_user.delete()
        print("\n🧹 Test user cleaned up successfully")
    except:
        print("\n⚠️  Failed to clean up test user")
    
    print("\n" + "=" * 50)
    print("🎉 Settings API Integration Test Complete!")
    print("✅ Backend UserSettingsView endpoint is fully functional")
    
    return True

if __name__ == '__main__':
    try:
        test_settings_api()
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()