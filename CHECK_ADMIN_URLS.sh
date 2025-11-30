#!/bin/bash

echo "🔍 Check for Admin URL Conflicts"
echo "================================="

cd ~/projects/jac-interactive-learning-platform

echo "📋 Checking current URL configurations..."

echo ""
echo "1️⃣ Main URLs configuration:"
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import path, include
from django.conf import settings

# Show main URLs.py content
print('Main urls.py patterns:')
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        print(f'  {pattern.pattern} -> {getattr(pattern, \"_func_str\", \"func\")}')
except Exception as e:
    print(f'Error reading URLs: {e}')
"

echo ""
echo "2️⃣ Looking for admin URL patterns:"
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver, path
from django.contrib import admin

# Check for admin patterns
resolver = get_resolver()
admin_patterns = []

for pattern in resolver.url_patterns:
    pattern_str = str(pattern.pattern)
    if 'admin' in pattern_str.lower():
        admin_patterns.append((pattern_str, pattern))

print(f'Found {len(admin_patterns)} admin-related patterns:')
for pattern_str, pattern in admin_patterns:
    print(f'  🔍 {pattern_str}')
    if hasattr(pattern, '_func_str'):
        print(f'     -> {pattern._func_str}')
    elif hasattr(pattern, 'namespace'):
        print(f'     -> namespace: {pattern.namespace}')
"

echo ""
echo "3️⃣ Checking for custom admin URL:"
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

# Check if custom admin URL is configured
admin_url = getattr(settings, 'ADMIN_URL', None)
print(f'ADMIN_URL setting: {admin_url}')

# Check for admin site customization
try:
    from django.contrib.admin.sites import AdminSite
    site = AdminSite()
    print(f'Default admin site name: {site.name}')
except:
    pass

# Look for custom admin configuration
import importlib
try:
    config_module = importlib.import_module('config.admin')
    print('Custom admin configuration found in config.admin')
except ImportError:
    print('No custom admin configuration found')
"

echo ""
echo "4️⃣ Checking for duplicate patterns:"
docker-compose exec backend python manage.py shell -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver
from collections import Counter

resolver = get_resolver()
all_patterns = [str(p.pattern) for p in resolver.url_patterns]

# Count patterns
pattern_counts = Counter(all_patterns)
duplicates = {pattern: count for pattern, count in pattern_counts.items() if count > 1}

if duplicates:
    print('⚠️  DUPLICATE URL PATTERNS FOUND:')
    for pattern, count in duplicates.items():
        print(f'    {pattern}: {count} times')
else:
    print('✅ No duplicate URL patterns found')
"

echo ""
echo "5️⃣ Recommended fixes:"
echo "If duplicates found, you may need to:"
echo "  - Remove duplicate admin URL patterns from main urls.py"
echo "  - Ensure only one admin.site.urls pattern exists"
echo "  - Use proper namespace for custom admin routes"
echo ""
echo "Standard fix pattern:"
echo "  path('admin/', admin.site.urls),"
echo "  path('custom-admin/', admin.site.urls),  # If needed"