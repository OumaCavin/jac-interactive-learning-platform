#!/usr/bin/env python
"""
Script to check Django admin site registration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')
django.setup()

from django.contrib.admin import site
from django.apps import apps

print('=== ADMIN SITE REGISTRATION ===')
print(f'Custom admin site: {hasattr(site, \"site_header\")}')
print(f'Custom admin header: {site.site_header if hasattr(site, \"site_header\") else \"Default\"}')

print('\n=== REGISTERED MODELS ===')
# Get all registered admin classes
registered_models = []
for model_admin in site._registry:
    model = site._registry[model_admin].model
    admin_class = site._registry[model_admin]
    registered_models.append({
        'model': model.__name__,
        'app': model._meta.app_label,
        'admin_class': admin_class.__class__.__name__
    })

if registered_models:
    print(f'Total registered models: {len(registered_models)}')
    for item in sorted(registered_models, key=lambda x: (x['app'], x['model'])):
        print(f'  {item[\"app\"]}.{item[\"model\"]} -> {item[\"admin_class\"]}')
else:
    print('No models registered in admin')

print('\n=== APPS WITH ADMIN.PY ===')
for app_config in apps.get_app_configs():
    admin_file = os.path.join(app_config.path, 'admin.py')
    if os.path.exists(admin_file):
        print(f'  {app_config.label} - admin.py exists ({os.path.getsize(admin_file)} bytes)')

print('\n=== CHECKING IMPORT ERRORS ===')
# Try to import each admin module
for app_config in apps.get_app_configs():
    admin_file = os.path.join(app_config.path, 'admin.py')
    if os.path.exists(admin_file):
        try:
            module_name = f'{app_config.module.__name__}.admin'
            __import__(module_name)
            print(f'  {app_config.label}: ✓ Admin imported successfully')
        except Exception as e:
            print(f'  {app_config.label}: ✗ Admin import failed - {str(e)[:100]}...')