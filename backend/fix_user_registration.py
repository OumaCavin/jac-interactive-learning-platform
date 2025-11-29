#!/usr/bin/env python
"""
Manual fix to ensure User model is registered with custom admin site
"""
import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_user_registration():
    """Manually register User with custom admin site"""
    print("🔧 Fixing User model registration with custom admin site...")
    
    from django.contrib.admin import site as default_site
    from django.contrib.auth import get_user_model
    from config.custom_admin import custom_admin_site
    
    # Import and register User model
    from apps.users.admin import UserAdmin
    from apps.users.models import User
    
    # Unregister from default site if registered
    if User in default_site._registry:
        default_site.unregister(User)
        print("ℹ️  Unregistered User from default site")
    
    # Register with custom site
    if User not in custom_admin_site._registry:
        custom_admin_site.register(User, UserAdmin)
        print("✅ Registered User with custom admin site")
    else:
        print("ℹ️  User already registered with custom admin site")
    
    # Verify registration
    user_admin = custom_admin_site._registry.get(User)
    if user_admin:
        print(f"✅ User model successfully registered with custom admin site")
        print(f"   Admin class: {user_admin.__class__.__name__}")
    else:
        print("❌ Failed to register User model")
        
    print("\n🎯 User model registration fixed!")

if __name__ == "__main__":
    fix_user_registration()