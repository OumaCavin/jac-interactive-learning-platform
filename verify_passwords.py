#!/usr/bin/env python3
"""
Quick Password Verification Script
Tests if the password hashing fix worked correctly
"""

import subprocess
import sys

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_admin_login():
    """Test admin user password verification"""
    cmd = """
    docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User
try:
    admin = User.objects.get(username='admin')
    is_valid = admin.check_password('admin123')
    print(f"ADMIN_USER_EXISTS:{admin is not None}")
    print(f"PASSWORD_VALID:{is_valid}")
    print(f"IS_SUPERUSER:{admin.is_superuser}")
    print(f"EMAIL:{admin.email}")
except User.DoesNotExist:
    print("ADMIN_USER_EXISTS:False")
    print("PASSWORD_VALID:False")
    print("IS_SUPERUSER:False")
    print("EMAIL:None")
except Exception as e:
    print(f"ERROR:{str(e)}")
EOF
    """
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("🔍 Admin User Test Results:")
        for line in stdout.strip().split('\n'):
            if line:
                print(f"   {line}")
    else:
        print(f"❌ Admin test failed: {stderr}")
    
    return success

def test_demo_login():
    """Test demo user password verification"""
    cmd = """
    docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User
try:
    demo = User.objects.get(username='demo_user')
    is_valid = demo.check_password('demo123')
    print(f"DEMO_USER_EXISTS:{demo is not None}")
    print(f"PASSWORD_VALID:{is_valid}")
    print(f"EMAIL:{demo.email}")
except User.DoesNotExist:
    print("DEMO_USER_EXISTS:False")
    print("PASSWORD_VALID:False")
    print("EMAIL:None")
except Exception as e:
    print(f"ERROR:{str(e)}")
EOF
    """
    
    success, stdout, stderr = run_command(cmd)
    if success:
        print("\n🔍 Demo User Test Results:")
        for line in stdout.strip().split('\n'):
            if line:
                print(f"   {line}")
    else:
        print(f"❌ Demo test failed: {stderr}")
    
    return success

def test_web_endpoints():
    """Test if web endpoints are accessible"""
    print("\n🌐 Testing Web Endpoints...")
    
    # Test Django admin
    cmd = "curl -s -f http://localhost:8000/admin/ > /dev/null"
    success, _, _ = run_command(cmd)
    if success:
        print("   ✅ Django Admin: ACCESSIBLE")
    else:
        print("   ❌ Django Admin: NOT ACCESSIBLE")
    
    # Test frontend
    cmd = "curl -s -f http://localhost:3000/ > /dev/null"
    success, _, _ = run_command(cmd)
    if success:
        print("   ✅ Frontend: ACCESSIBLE")
    else:
        print("   ❌ Frontend: NOT ACCESSIBLE")
    
    # Test API
    cmd = "curl -s -f http://localhost:8000/api/health/ > /dev/null"
    success, _, _ = run_command(cmd)
    if success:
        print("   ✅ API Health: WORKING")
    else:
        print("   ❌ API Health: NOT RESPONDING")

def main():
    print("🔍 JAC Platform Password & Service Verification")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not subprocess.run("ls docker-compose.yml", shell=True, capture_output=True).returncode == 0:
        print("❌ Please run this from the JAC platform directory")
        sys.exit(1)
    
    admin_ok = test_admin_login()
    demo_ok = test_demo_login()
    test_web_endpoints()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    if admin_ok and demo_ok:
        print("✅ All password verifications PASSED")
        print("\n🎯 YOU CAN NOW LOGIN WITH:")
        print("   Django Admin: http://localhost:8000/admin/")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n   Frontend: http://localhost:3000/login")
        print("   Username: demo_user")
        print("   Password: demo123")
    else:
        print("❌ Password verification FAILED")
        print("\n🔧 RUN THE PASSWORD HASHING FIX:")
        print("   docker-compose exec backend python /tmp/fix_password_hashing.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()