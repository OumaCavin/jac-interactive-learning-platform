#!/usr/bin/env python
"""
Quick Admin Fix Script
Manually ensure User model is registered with custom admin site
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, '/workspace/jac-interactive-learning-platform/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

def fix_admin_registration():
    """Fix admin registration issues"""
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
    from django.contrib.auth import get_user_model
    from config.custom_admin import custom_admin_site
    from apps.users.models import User
    from apps.users.admin import UserAdmin
    
    print("🔧 Admin Registration Fix")
    print("=" * 30)
    
    # Ensure User model is registered with custom admin site
    try:
        # Unregister if already registered
        try:
            custom_admin_site.unregister(User)
            print("📤 Unregistered User from custom admin site")
        except admin.sites.NotRegistered:
            print("ℹ️  User was not registered with custom admin site")
        
        # Re-register the User model
        custom_admin_site.register(User, UserAdmin)
        print("✅ Registered User with custom admin site")
        
        # Verify registration
        if User in custom_admin_site._registry:
            print("✅ User model is now properly registered!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = fix_admin_registration()
    if success:
        print("\n🎉 Fix completed! Try accessing the admin again.")
        print("   URL: http://localhost:8000/admin/")
    else:
        print("\n❌ Fix failed. Check the errors above.")