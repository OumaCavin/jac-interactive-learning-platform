#!/usr/bin/env python3
"""Fix user permissions for custom User model"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_platform.settings.dev')
django.setup()

from users.models import User
from django.contrib.auth import get_user_model

def fix_user_permissions():
    User = get_user_model()  # This gets the custom User model
    
    print("📋 All users in the system:")
    print("=" * 50)
    
    for user in User.objects.all():
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Superuser: {user.is_superuser}")
        print(f"Staff: {user.is_staff}")
        print(f"Active: {user.is_active}")
        print("-" * 30)
    
    print("\n🔧 Fixing permissions for 'Ouma'...")
    
    try:
        user = User.objects.get(username='Ouma')
        print(f"Found user: {user.username}")
        
        # Fix permissions
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        
        print("✅ Fixed permissions for user 'Ouma'")
        print("   - is_superuser: True")
        print("   - is_staff: True")
        print("   - is_active: True")
        
        # Verify the fix
        user.refresh_from_db()
        print(f"\n🔍 Verification:")
        print(f"   - is_superuser: {user.is_superuser}")
        print(f"   - is_staff: {user.is_staff}")
        print(f"   - is_active: {user.is_active}")
        
    except User.DoesNotExist:
        print("❌ User 'Ouma' does not exist")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_user_permissions()