#!/usr/bin/env python
"""Debug why Django admin CSS files aren't being collected"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/app')
django.setup()

from django.conf import settings
from django.contrib.staticfiles import finders
from django.apps import apps

print("=== Django Admin Static Files Debug ===")
print(f"Django version: {django.get_version()}")
print()

# Check if admin is properly installed
try:
    from django.contrib.admin import site
    print("✅ Django admin is properly imported")
    print(f"Admin site: {site.__class__.__name__}")
except ImportError as e:
    print(f"❌ Django admin import failed: {e}")

print()

# Check installed apps
print("📋 INSTALLED APPS:")
for app in apps.get_app_configs():
    print(f"  - {app.label}: {app.name}")
    # Check specifically for admin static files in each app
    if hasattr(app, 'path'):
        admin_static_path = os.path.join(app.path, 'static', 'admin')
        if os.path.exists(admin_static_path):
            css_files = []
            for root, dirs, files in os.walk(admin_static_path):
                css_files.extend([f for f in files if f.endswith('.css')])
            if css_files:
                print(f"    📁 Admin CSS files found: {css_files}")

print()

# Check static configuration
print("⚙️  STATIC FILES CONFIGURATION:")
print(f"  STATIC_URL: {settings.STATIC_URL}")
print(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print()

# Check static finders
print("🔍 STATIC FILES FINDERS:")
finders_result = list(finders.get_finders())
print(f"Found {len(finders_result)} finders")

for finder in finders_result:
    try:
        print(f"  Finder: {finder.__class__.__name__}")
        # Try to find admin CSS files
        admin_files = list(finder.list(['admin/**/*.css']))
        if admin_files:
            print(f"    📁 Admin CSS files: {[f[0] for f in admin_files[:5]]}")  # Show first 5
        else:
            print(f"    ❌ No admin CSS files found by this finder")
    except Exception as e:
        print(f"    ⚠️  Error: {e}")

print()

# Check current static root contents
print("📁 CURRENT STATIC ROOT CONTENTS:")
static_root = settings.STATIC_ROOT
if os.path.exists(static_root):
    for item in os.listdir(static_root):
        item_path = os.path.join(static_root, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
            if item == "admin":
                admin_path = item_path
                if os.path.exists(admin_path):
                    css_path = os.path.join(admin_path, "css")
                    if os.path.exists(css_path):
                        css_files = os.listdir(css_path)
                        print(f"    📁 css/ -> {css_files}")
                    else:
                        print(f"    ❌ css/ directory missing")
        else:
            print(f"  📄 {item}")
else:
    print(f"❌ STATIC_ROOT does not exist: {static_root}")

print()
print("=== Debug Complete ===")