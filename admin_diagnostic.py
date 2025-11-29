#!/usr/bin/env python
"""
Admin Diagnostic Script
Check custom admin site configuration and user registration
"""

import sys
import os
import django

# Add the backend directory to the path
sys.path.insert(0, '/workspace/jac-interactive-learning-platform/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_admin_setup():
    """Comprehensive admin setup check"""
    print("🔍 JAC Platform Admin Diagnostic")
    print("=" * 50)
    
    # Import Django modules
    from django.contrib.admin import site as default_site
    from django.contrib.auth import get_user_model
    from config.custom_admin import custom_admin_site
    from django.apps import apps
    
    # Check user model
    User = get_user_model()
    print(f"\n👤 User Model: {User.__name__}")
    print(f"   Model path: {User.__module__}")
    
    # Check user permissions
    try:
        user = User.objects.get(username='Ouma')
        print(f"\n🔑 User Details:")
        print(f"   Username: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   is_superuser: {user.is_superuser}")
        print(f"   is_staff: {user.is_staff}")
        print(f"   is_active: {user.is_active}")
    except User.DoesNotExist:
        print("❌ User 'Ouma' does not exist!")
        return
    
    # Check custom admin site
    print(f"\n🏢 Custom Admin Site:")
    print(f"   Site name: {custom_admin_site.name}")
    print(f"   Site header: {custom_admin_site.site_header}")
    
    # Check User registration with custom site
    print(f"\n📋 Admin Site Registration:")
    try:
        user_admin = custom_admin_site._registry.get(User)
        if user_admin:
            print(f"   ✅ User model registered with custom admin site")
            print(f"   Admin class: {user_admin.__class__.__name__}")
        else:
            print(f"   ❌ User model NOT registered with custom admin site")
    except Exception as e:
        print(f"   ❌ Error checking registration: {e}")
    
    # Check default site registration for comparison
    try:
        default_user_admin = default_site._registry.get(User)
        if default_user_admin:
            print(f"   ℹ️  User model registered with default admin site")
            print(f"   Default admin class: {default_user_admin.__class__.__name__}")
        else:
            print(f"   ℹ️  User model NOT registered with default admin site")
    except Exception as e:
        print(f"   ℹ️  Error checking default site: {e}")
    
    # List all registered models
    print(f"\n📦 Custom Admin Site Models:")
    registered_models = list(custom_admin_site._registry.keys())
    for model in sorted(registered_models, key=lambda x: x.__name__):
        admin_class = custom_admin_site._registry[model]
        print(f"   ✅ {model.__name__} → {admin_class.__class__.__name__}")
    
    print(f"\n📊 Summary:")
    print(f"   Registered models: {len(registered_models)}")
    
    # Final diagnosis
    print(f"\n🎯 Diagnosis:")
    if user.is_superuser and user.is_staff and user.is_active:
        print(f"   ✅ User permissions are correct")
    else:
        print(f"   ❌ User permissions issue")
        
    if custom_admin_site._registry.get(User):
        print(f"   ✅ User registered with custom admin site")
        print(f"   💡 Admin should work! Try accessing /admin/")
    else:
        print(f"   ❌ User NOT registered with custom admin site")
        print(f"   💡 This is likely the issue!")

if __name__ == "__main__":
    check_admin_setup()