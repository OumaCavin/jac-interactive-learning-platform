#!/usr/bin/env python3
"""
CRITICAL FIX: Proper Django User Creation with Password Hashing
This script creates users using Django's management commands to ensure proper password hashing
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.db import connection
import subprocess
import json

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # Add the backend path to Python path
    backend_path = '/workspace/jac-interactive-learning-platform/backend'
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    django.setup()
    print("✅ Django environment setup complete")

def create_users_with_proper_hashing():
    """Create users using Django management commands for proper password hashing"""
    
    print("\n🔧 Creating users with proper Django password hashing...")
    
    # Remove existing users if they exist
    try:
        User.objects.filter(username='admin').delete()
        User.objects.filter(username='demo_user').delete()
        print("🗑️ Cleaned up existing users")
    except Exception as e:
        print(f"ℹ️ No existing users to clean: {e}")
    
    # Create admin user using Django management
    print("👤 Creating admin user...")
    admin_result = subprocess.run([
        'python', 'manage.py', 'createsuperuser',
        '--username', 'admin',
        '--email', 'cavin.otieno012@gmail.com',
        '--noinput'
    ], input='admin123\nadmin123\n', text=True, capture_output=True, cwd='/workspace/jac-interactive-learning-platform/backend')
    
    if admin_result.returncode == 0:
        print("✅ Admin user created successfully")
        
        # Set the password programmatically to ensure it's hashed
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('admin123')
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()
        print("✅ Admin password set and superuser permissions confirmed")
    else:
        print(f"❌ Admin creation failed: {admin_result.stderr}")
        # Fallback: create user directly
        try:
            admin_user = User.objects.create_user(
                username='admin',
                email='cavin.otieno012@gmail.com',
                password='admin123'
            )
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            print("✅ Admin user created via fallback method")
        except Exception as e:
            print(f"❌ Admin creation failed completely: {e}")
    
    # Create demo user using Django management
    print("👤 Creating demo user...")
    demo_result = subprocess.run([
        'python', 'manage.py', 'createsuperuser',
        '--username', 'demo_user',
        '--email', 'demo@example.com',
        '--noinput'
    ], input='demo123\ndemo123\n', text=True, capture_output=True, cwd='/workspace/jac-interactive-learning-platform/backend')
    
    if demo_result.returncode == 0:
        print("✅ Demo user created successfully")
        
        # Set the password programmatically
        demo_user = User.objects.get(username='demo_user')
        demo_user.set_password('demo123')
        demo_user.save()
        print("✅ Demo password set")
    else:
        print(f"❌ Demo creation failed: {demo_result.stderr}")
        # Fallback: create user directly
        try:
            demo_user = User.objects.create_user(
                username='demo_user',
                email='demo@example.com',
                password='demo123'
            )
            print("✅ Demo user created via fallback method")
        except Exception as e:
            print(f"❌ Demo creation failed completely: {e}")

def verify_users():
    """Verify that users were created with proper hashing"""
    
    print("\n🔍 Verifying user creation and password hashing...")
    
    # Check admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Admin user found:")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Is Superuser: {admin_user.is_superuser}")
        print(f"   Is Staff: {admin_user.is_staff}")
        print(f"   Password Hash: {admin_user.password[:50]}...")
        
        # Test password verification
        if admin_user.check_password('admin123'):
            print("✅ Admin password verification: SUCCESS")
        else:
            print("❌ Admin password verification: FAILED")
            
    except User.DoesNotExist:
        print("❌ Admin user not found")
    except Exception as e:
        print(f"❌ Error checking admin user: {e}")
    
    # Check demo user
    try:
        demo_user = User.objects.get(username='demo_user')
        print(f"\n✅ Demo user found:")
        print(f"   Username: {demo_user.username}")
        print(f"   Email: {demo_user.email}")
        print(f"   Is Superuser: {demo_user.is_superuser}")
        print(f"   Password Hash: {demo_user.password[:50]}...")
        
        # Test password verification
        if demo_user.check_password('demo123'):
            print("✅ Demo password verification: SUCCESS")
        else:
            print("❌ Demo password verification: FAILED")
            
    except User.DoesNotExist:
        print("❌ Demo user not found")
    except Exception as e:
        print(f"❌ Error checking demo user: {e}")

def main():
    print("🚨 JAC Platform Password Hashing Fix")
    print("=" * 50)
    
    try:
        setup_django()
        create_users_with_proper_hashing()
        verify_users()
        
        print("\n🎉 Password hashing fix completed!")
        print("\n📋 CREDENTIALS TO USE:")
        print("Django Admin: http://localhost:8000/admin/")
        print("   Username: admin")
        print("   Password: admin123")
        print("\nFrontend Login: http://localhost:3000/login")
        print("   Username: demo_user")
        print("   Password: demo123")
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())