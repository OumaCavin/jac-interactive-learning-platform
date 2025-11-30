#!/bin/bash

echo "=========================================="
echo "JAC Platform - Fix Admin Permissions"
echo "=========================================="
echo ""
echo "🔧 Fixing admin user permissions for Django admin access..."

cd ~/projects/jac-interactive-learning-platform

echo "Step 1: Verify admin user status..."
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from apps.users.models import User
try:
    admin = User.objects.get(username='admin')
    print(f'✅ Admin user found: {admin.username}')
    print(f'   Email: {admin.email}')
    print(f'   Is superuser: {admin.is_superuser}')
    print(f'   Is staff: {admin.is_staff}')
    print(f'   Is active: {admin.is_active}')
    
    # Fix permissions if needed
    if not admin.is_superuser:
        admin.is_superuser = True
        admin.save()
        print('🔧 Fixed: Added superuser permissions')
    
    if not admin.is_staff:
        admin.is_staff = True
        admin.save()
        print('🔧 Fixed: Added staff permissions')
        
    if not admin.is_active:
        admin.is_active = True
        admin.save()
        print('🔧 Fixed: Activated user')
        
except User.DoesNotExist:
    print('❌ Admin user not found!')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "Step 2: Check Django admin configuration..."
docker-compose exec backend python manage.py shell -c "
from django.contrib import admin
from django.conf import settings

print('Admin configuration check:')
print(f'  INSTALLED_APPS has admin: {\"django.contrib.admin\" in settings.INSTALLED_APPS}')
print(f'  MIDDLEWARE has admin: {\"django.contrib.sessions.middleware.SessionMiddleware\" in settings.MIDDLEWARE}')
print(f'  Templates configured: {hasattr(settings, \"TEMPLATES\")}')

# Check admin site
try:
    from django.contrib.admin.sites import AdminSite
    site = AdminSite()
    print(f'  Admin site available: ✅')
except Exception as e:
    print(f'  Admin site error: ❌ {e}')
"

echo ""
echo "Step 3: Test admin access..."
docker-compose exec backend python manage.py shell -c "
from django.test import Client
from django.contrib.auth import get_user_model
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

User = get_user_model()
client = Client()

try:
    # Login as admin
    admin = User.objects.get(username='admin')
    logged_in = client.login(username='admin', password='jac_admin_2024!')
    print(f'Login test: {\"✅ Success\" if logged_in else \"❌ Failed\"}')
    
    # Test admin page access
    response = client.get('/admin/')
    print(f'Admin index page: {response.status_code}')
    
    if response.status_code == 200:
        print('✅ Admin access working!')
    elif response.status_code == 403:
        print('❌ Access denied - permissions issue')
    else:
        print(f'⚠️ Unexpected status: {response.status_code}')
        
except Exception as e:
    print(f'❌ Admin test error: {e}')
"

echo ""
echo "Step 4: Restart backend if needed..."
docker-compose restart backend

echo ""
echo "Step 5: Verify containers..."
docker-compose ps

echo ""
echo "=========================================="
echo "🎯 ADMIN PERMISSION FIX COMPLETE"
echo "=========================================="
echo ""
echo "🌐 Try accessing: http://localhost:8000/admin/"
echo "   Login: admin / jac_admin_2024!"
echo ""
echo "🔗 If still having issues:"
echo "   1. Clear browser cache and cookies"
echo "   2. Try incognito/private browsing mode"
echo "   3. Check browser console for errors"
echo ""