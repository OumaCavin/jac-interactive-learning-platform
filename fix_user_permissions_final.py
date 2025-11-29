#!/usr/bin/env python3
"""Fix user permissions for the JAC Platform custom User model"""

import os
import sys
import django

# Setup Django with the correct settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def fix_user_permissions():
    print("🔧 Fixing admin permissions for the JAC Platform User model")
    print("=" * 60)
    
    try:
        # Get the user - using the custom User model from apps.users
        user = User.objects.get(username='Ouma')
        
        print(f"✅ Found user: {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Current is_superuser: {user.is_superuser}")
        print(f"   Current is_staff: {user.is_staff}")
        print(f"   Current is_active: {user.is_active}")
        
        # Fix the permissions
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        
        print("\n🔧 Fixed permissions:")
        print("   - is_superuser: True ✅")
        print("   - is_staff: True ✅")
        print("   - is_active: True ✅")
        
        # Verify the fix
        user.refresh_from_db()
        print(f"\n🔍 Verification after save:")
        print(f"   - is_superuser: {user.is_superuser}")
        print(f"   - is_staff: {user.is_staff}")
        print(f"   - is_active: {user.is_active}")
        
        print(f"\n🎉 Success! User '{user.username}' now has admin permissions")
        print(f"   You can now login to http://localhost:8000/admin/")
        
    except User.DoesNotExist:
        print("❌ User 'Ouma' does not exist in the database")
        print("\n📋 Available users:")
        for u in User.objects.all():
            print(f"   - {u.username} ({u.email})")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_user_permissions()