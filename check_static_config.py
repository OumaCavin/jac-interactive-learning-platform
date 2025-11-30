#!/usr/bin/env python
"""Check Django static files configuration"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/app')
django.setup()

from django.conf import settings
import os

print("=== Django Static Files Configuration ===")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print()

# Check if STATIC_ROOT exists
static_root = settings.STATIC_ROOT
print(f"STATIC_ROOT exists: {os.path.exists(static_root)}")

if os.path.exists(static_root):
    print(f"Directory contents of {static_root}:")
    try:
        for item in os.listdir(static_root):
            item_path = os.path.join(static_root, item)
            if os.path.isdir(item_path):
                print(f"  📁 {item}/")
                # Show subdirectories for static admin
                if item == "admin":
                    admin_path = os.path.join(static_root, item, "css")
                    if os.path.exists(admin_path):
                        css_files = os.listdir(admin_path)
                        print(f"    📁 css/")
                        for css_file in css_files:
                            print(f"      📄 {css_file}")
                    else:
                        print(f"    ❌ css/ directory missing")
            else:
                print(f"  📄 {item}")
    except Exception as e:
        print(f"  Error listing directory: {e}")
else:
    print(f"❌ STATIC_ROOT directory does not exist")
    print(f"   This explains why static files return 404!")

print("\n=== Static Files Finding ===")
from django.contrib.staticfiles import finders
print("Static files finders result:")
for finder in finders.get_finders():
    print(f"  {finder}")