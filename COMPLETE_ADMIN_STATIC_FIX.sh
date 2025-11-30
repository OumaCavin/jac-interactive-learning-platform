#!/bin/bash

echo "🔧 COMPLETE ADMIN STATIC FILES FIX"
echo "=================================="
echo ""
echo "🎯 Fixing static files serving and admin access..."

cd ~/projects/jac-interactive-learning-platform

echo "Step 1: Collect all static files (including admin CSS)..."
docker-compose exec backend python manage.py collectstatic --noinput --clear
echo ""

echo "Step 2: Check static files structure..."
docker-compose exec backend python manage.py shell -c "
import os
from django.conf import settings

print('📁 Static files check:')
print(f'  STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'  STATIC_URL: {settings.STATIC_URL}')

# Check if admin CSS exists
admin_css_path = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'dashboard.css')
print(f'  dashboard.css exists: {os.path.exists(admin_css_path)}')

if os.path.exists(admin_css_path):
    print(f'  File size: {os.path.getsize(admin_css_path)} bytes')
    print('  ✅ Admin CSS file found')
else:
    print('  ❌ Admin CSS file missing')
"

echo ""
echo "Step 3: Verify admin URL configuration..."
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from django.contrib import admin
from config.custom_admin import custom_admin_site

print('🔍 Admin URL analysis:')
resolver = get_resolver()

# Check for admin patterns
admin_patterns = [p for p in resolver.url_patterns if 'admin' in str(p.pattern)]
print(f'  Admin patterns found: {len(admin_patterns)}')

for pattern in admin_patterns:
    print(f'    📍 {pattern.pattern} -> {getattr(pattern, \"_func_str\", \"unknown\")}')

# Check if custom admin is properly configured
print(f'  Custom admin site name: {custom_admin_site.name}')
print(f'  Custom admin URL pattern: admin/')
"

echo ""
echo "Step 4: Test static file URLs directly..."
echo "Testing static file access patterns..."

# Test various static file access patterns
docker-compose exec backend python manage.py runserver 0.0.0.0:8001 &
sleep 3

echo "Testing admin CSS access:"
curl -I http://localhost:8001/static/admin/css/dashboard.css
echo ""

echo "Testing general static access:"
curl -I http://localhost:8001/static/admin/css/base.css
echo ""

# Stop test server
pkill -f "runserver 0.0.0.0:8001"

echo ""
echo "Step 5: Check for DEBUG setting..."
docker-compose exec backend python manage.py shell -c "
from django.conf import settings
print(f'DEBUG setting: {settings.DEBUG}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'Using staticfiles app: {\"django.contrib.staticfiles\" in settings.INSTALLED_APPS}')
"

echo ""
echo "Step 6: Fix static files permissions..."
docker-compose exec backend bash -c '
chown -R jac:jac /app/staticfiles/
chmod -R 755 /app/staticfiles/
chown -R jac:jac /app/backend/staticfiles/
chmod -R 755 /app/backend/staticfiles/
echo "Static files permissions fixed"
'

echo ""
echo "Step 7: Restart all services..."
docker-compose restart backend

echo ""
echo "Step 8: Wait for services to be ready..."
sleep 10

echo ""
echo "Step 9: Final verification..."
echo "Testing live admin page:"
curl -I http://localhost:8000/admin/
echo ""

echo "Testing live admin CSS:"
curl -I http://localhost:8000/static/admin/css/dashboard.css
echo ""

echo ""
echo "Step 10: Check container status..."
docker-compose ps

echo ""
echo "=========================================="
echo "🎯 COMPLETE ADMIN FIX APPLIED"
echo "=========================================="
echo ""
echo "🌐 Browser Instructions:"
echo "1. Clear ALL browser cache and cookies for localhost:8000"
echo "2. Open incognito/private browsing window"
echo "3. Go to: http://localhost:8000/admin/"
echo "4. Login with: admin / jac_admin_2024!"
echo ""
echo "✅ Expected results:"
echo "- CSS should load properly (no console errors)"
echo "- Admin interface should be fully styled"
echo "- All admin models should be accessible"
echo ""
echo "🔧 If still having issues:"
echo "- Check browser network tab for 404s"
echo "- Verify static files are served correctly"
echo "- Try hard refresh (Ctrl+F5)"