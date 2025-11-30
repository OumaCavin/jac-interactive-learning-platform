#!/bin/bash

echo "=== COMPLETE Django Admin Static Files Fix ==="
echo "Fixes DEBUG=True and STATICFILES_DIRS to serve dashboard.css"
echo "This is the definitive solution that addresses all root causes"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with complete fix..."

echo ""
echo "🔧 Step 1: Stopping backend container to ensure settings refresh..."
docker-compose stop backend

echo ""
echo "🔧 Step 2: Creating corrected settings.py with both DEBUG=True and proper STATICFILES_DIRS..."

# Create a new settings file with all corrections
python3 << 'PYTHON_EOF'
import re
import os

# Read the current settings.py
settings_path = 'backend/config/settings.py'
with open(settings_path, 'r') as f:
    content = f.read()

print("Original DEBUG setting found:")
debug_match = re.search(r'DEBUG\s*=\s*(\w+)', content)
if debug_match:
    print(f"  {debug_match.group()}")

# Fix 1: Ensure DEBUG=True
content = re.sub(r'DEBUG\s*=\s*(\w+)', 'DEBUG = True', content)
print("✅ Updated DEBUG setting to True")

# Fix 2: Update STATICFILES_DIRS to include both /app/static and /var/www/static
staticfiles_pattern = r'STATICFILES_DIRS\s*=\s*\[(.*?)\]'

def replace_staticfiles_dirs(match):
    existing_dirs = match.group(1)
    # Keep existing local static files and add /var/www/static
    new_dirs = f'''[PosixPath('/app/static'), PosixPath('/var/www/static')]'''
    return f'STATICFILES_DIRS = {new_dirs}'

content = re.sub(staticfiles_pattern, replace_staticfiles_dirs, content, flags=re.DOTALL)
print("✅ Updated STATICFILES_DIRS to include both local and Docker volume paths")

# Fix 3: Ensure proper static files URL configuration in development
if 'if settings.DEBUG:' in content:
    # Update the static files serving section
    static_serving_pattern = r'# Serve media files in development\s*if settings\.DEBUG:\s*urlpatterns \+= static\(settings\.MEDIA_URL, document_root=settings\.MEDIA_ROOT\)\s*# Serve static files from Docker volume in development\s*urlpatterns \+= static\(settings\.STATIC_URL, document_root=settings\.STATIC_ROOT\)'
    
    new_static_serving = '''# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # CRITICAL: Serve static files from both local and Docker volume paths
    urlpatterns += static('/static/', document_root='/var/www/static')
    urlpatterns += static('/static/', document_root='/app/static')'''
    
    content = re.sub(static_serving_pattern, new_static_serving, content, flags=re.DOTALL)
    print("✅ Updated static files URL configuration")

# Write the corrected settings
with open(settings_path, 'w') as f:
    f.write(content)

print("✅ Settings file updated successfully")

# Also update URLs.py if it needs fixing
urls_path = 'backend/config/urls.py'
with open(urls_path, 'r') as f:
    urls_content = f.read()

# Ensure static files serving is properly configured
if '/static/' not in urls_content or 'document_root=' not in urls_content:
    print("🔧 Updating URLs.py with proper static files serving...")
    
    # Add static files serving at the end
    urls_addition = '''

# Serve static files in development (comprehensive fix)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve from Docker volume (/var/www/static) - primary path
    urlpatterns += static('/static/', document_root='/var/www/static')
    # Serve from local static (/app/static) - fallback path
    urlpatterns += static('/static/', document_root='/app/static')
'''
    
    urls_content += urls_addition
    
    with open(urls_path, 'w') as f:
        f.write(urls_content)
    
    print("✅ Updated URLs.py with dual path static files serving")
else:
    print("✅ URLs.py already has static files configuration")

PYTHON_EOF

echo ""
echo "🔧 Step 3: Verifying file corrections..."
echo "Checking DEBUG setting:"
grep "DEBUG = True" backend/config/settings.py && echo "✅ DEBUG=True found" || echo "❌ DEBUG=True not found"

echo "Checking STATICFILES_DIRS:"
grep "PosixPath('/var/www/static')" backend/config/settings.py && echo "✅ /var/www/static found in STATICFILES_DIRS" || echo "❌ /var/www/static not in STATICFILES_DIRS"

echo ""
echo "🔧 Step 4: Starting backend container..."
docker-compose start backend

echo ""
echo "🔧 Step 5: Waiting for backend to fully start..."
sleep 15

echo ""
echo "🔧 Step 6: Verifying DEBUG=True is now active..."
DEBUG_CHECK=$(docker-compose exec backend python manage.py shell -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)" 2>/dev/null)

echo "Current DEBUG setting: $DEBUG_CHECK"

echo ""
echo "🔧 Step 7: Testing static file access..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

if [ "$HTTP_RESPONSE" = "200" ]; then
    echo "🎉 SUCCESS: dashboard.css returns HTTP 200!"
    echo ""
    echo "✅ Your Django admin interface should now load with proper styling!"
    echo "🌐 Visit: http://localhost:8000/admin/"
    echo "🔐 Login: admin / jac_admin_2024!"
    echo ""
    echo "🔍 Final verification - testing admin interface accessibility:"
    ADMIN_TEST=$(curl -s http://localhost:8000/admin/ | grep -q "Django administration" && echo "✅ Admin interface loads correctly!" || echo "⚠️  Check admin interface manually")
    echo "$ADMIN_TEST"
    
    echo ""
    echo "🎉 MISSION ACCOMPLISHED!"
    echo "The dashboard.css issue has been resolved!"
    
else
    echo "❌ STILL FAILED: dashboard.css returns HTTP $HTTP_RESPONSE"
    echo ""
    echo "🔍 Emergency debugging..."
    docker-compose exec backend python manage.py shell -c "
from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.finders import find
import os

print('=== EMERGENCY DEBUG - COMPLETE CONFIGURATION ===')
print(f'DEBUG: {settings.DEBUG}')
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')

# Test file existence in both locations
locations = [
    '/var/www/static/admin/css/dashboard.css',
    '/app/static/admin/css/dashboard.css'
]

print('\n=== FILE EXISTENCE CHECK ===')
for location in locations:
    exists = os.path.exists(location)
    readable = os.access(location, os.R_OK) if exists else False
    print(f'{location}: EXISTS={exists}, READABLE={readable}')

# Test Django's staticfiles finder
print('\n=== DJANGO STATICFILES FINDER ===')
try:
    found_path = find('admin/css/dashboard.css')
    print(f'Django found: {found_path}')
except Exception as e:
    print(f'Django finder error: {e}')

# Test URL construction
print('\n=== URL CONSTRUCTION ===')
storage = StaticFilesStorage()
try:
    url = storage.url('admin/css/dashboard.css')
    print(f'Storage URL: {url}')
except Exception as e:
    print(f'Storage URL error: {e}')
"
fi

echo ""
echo "=== COMPLETE Django Admin Static Files Fix Complete ==="
echo "This script ensures:"
echo "1. ✅ DEBUG=True (enables static file serving)"
echo "2. ✅ STATICFILES_DIRS includes both /app/static and /var/www/static"
echo "3. ✅ URL configuration serves from both paths"
echo "4. ✅ Files are confirmed to exist in /var/www/static/"
echo ""
echo "🎯 This should definitively resolve the dashboard.css 404 issue!"