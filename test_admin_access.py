#!/usr/bin/env python
"""
Simple Admin Test Script
Test if admin access works
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/workspace/jac-interactive-learning-platform/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

def test_admin_access():
    """Test admin access"""
    from django.contrib.auth import get_user_model
    from django.contrib.admin import site as default_site
    from config.custom_admin import custom_admin_site
    
    print("🧪 Admin Access Test")
    print("=" * 25)
    
    User = get_user_model()
    
    # Test 1: Check user exists and has permissions
    try:
        user = User.objects.get(username='Ouma')
        print(f"✅ User 'Ouma' found")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_active: {user.is_active}")
        
        if not (user.is_superuser and user.is_staff and user.is_active):
            print("❌ User permissions issue!")
            return False
            
    except User.DoesNotExist:
        print("❌ User 'Ouma' not found!")
        return False
    
    # Test 2: Check custom admin site registration
    if User in custom_admin_site._registry:
        print("✅ User registered with custom admin site")
    else:
        print("❌ User NOT registered with custom admin site")
        return False
    
    # Test 3: Check default admin site (for comparison)
    if User in default_site._registry:
        print("ℹ️  User also registered with default admin site")
    else:
        print("ℹ️  User not registered with default admin site")
    
    # Test 4: Check admin site properties
    print(f"✅ Custom admin site: {custom_admin_site.name}")
    print(f"✅ Site header: {custom_admin_site.site_header}")
    
    print("\n🎉 Admin configuration looks good!")
    print("Try accessing: http://localhost:8000/admin/")
    return True

if __name__ == "__main__":
    test_admin_access()