#!/bin/bash

echo "🔧 Fix Admin Static Files & URL Conflicts"
echo "========================================="
echo ""
echo "📋 Diagnosing the real admin issues..."

cd ~/projects/jac-interactive-learning-platform

echo "Step 1: Check URL configurations..."
docker-compose exec backend python manage.py shell -c "
from django.urls import get_resolver
from django.conf import settings

print('📊 URL Pattern Analysis:')
print('=' * 40)

# Get all URL patterns
resolver = get_resolver()
admin_urls = []
for pattern in resolver.url_patterns:
    if hasattr(pattern, 'urlconf_name'):
        try:
            for p in pattern.urlconf_name:
                if 'admin' in str(p.pattern):
                    admin_urls.append(str(p.pattern))
        except:
            pass
    
# Check for admin patterns
admin_patterns = [p for p in resolver.url_patterns if 'admin' in str(p.pattern)]
print(f'Admin URL patterns found: {len(admin_patterns)}')

for i, pattern in enumerate(admin_patterns[:10], 1):  # Show first 10
    print(f'  {i}. {pattern.pattern}')

print('')
print('📁 Static files configuration:')
print(f'  STATIC_URL: {settings.STATIC_URL}')
print(f'  STATIC_ROOT: {getattr(settings, \"STATIC_ROOT\", \"Not set\")}')
print(f'  DEBUG: {settings.DEBUG}')
print(f'  Static files enabled: {hasattr(settings, \"STATIC_URL\")}')
"

echo ""
echo "Step 2: Check static file serving..."
docker-compose exec backend python manage.py shell -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.staticfiles import views

print('🔍 Static files diagnostic:')
print(f'  STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'  STATICFILES_DIRS: {getattr(settings, \"STATICFILES_DIRS\", [])}')
print(f'  Static URL pattern in URLs: {\"static\" in str(settings.ROOT_URLCONF)}')

# Check if static files are collected
static_root = settings.STATIC_ROOT
if static_root:
    print(f'  Static root exists: {os.path.exists(static_root)}')
    if os.path.exists(static_root):
        admin_css = os.path.join(static_root, 'admin', 'css', 'dashboard.css')
        print(f'  dashboard.css exists: {os.path.exists(admin_css)}')
"

echo ""
echo "Step 3: Check for conflicting URL patterns..."
docker-compose exec backend python manage.py shell -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from django.urls import path, include

print('🔍 Checking URL configuration for conflicts:')

# Check main urls.py
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    
    print('Current URL patterns:')
    for url_pattern in resolver.url_patterns:
        pattern_str = str(url_pattern.pattern)
        if 'admin' in pattern_str.lower():
            print(f'  📍 {pattern_str} -> {url_pattern._func_str if hasattr(url_pattern, \"_func_str\") else url_pattern.name}')
        
except Exception as e:
    print(f'❌ URL check error: {e}')
"

echo ""
echo "Step 4: Test static file access directly..."
docker-compose exec backend python manage.py runserver 0.0.0.0:8001 &
sleep 2

echo "Testing static file serving..."
docker-compose exec backend curl -I http://localhost:8001/static/admin/css/dashboard.css

# Kill the test server
pkill -f "runserver 0.0.0.0:8001"

echo ""
echo "Step 5: Fix static files collection..."
docker-compose exec backend python manage.py collectstatic --noinput --clear

echo ""
echo "Step 6: Check for admin URL conflicts..."
docker-compose exec backend python manage.py shell -c "
from django.conf import settings
print('Admin URL configuration:')
print(f'  ADMIN_URL: {getattr(settings, \"ADMIN_URL\", \"default (admin/)\")}')

# Check if custom admin is configured
if hasattr(settings, 'ADMIN_URL'):
    print('  Custom admin URL detected')
else:
    print('  Using default admin URL (admin/)')
"

echo ""
echo "Step 7: Restart backend to apply changes..."
docker-compose restart backend

echo ""
echo "Step 8: Verify fix..."
sleep 5
curl -I http://localhost:8000/static/admin/css/dashboard.css

echo ""
echo "=========================================="
echo "🎯 ADMIN STATIC FILES FIX COMPLETE"
echo "=========================================="
echo ""
echo "🔗 Now try:"
echo "1. Clear browser cache completely"
echo "2. Refresh admin page: http://localhost:8000/admin/"
echo "3. Check browser console - CSS should load properly"
echo ""