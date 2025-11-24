#!/usr/bin/env python
"""Check Django admin registration"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')
django.setup()

from django.contrib.admin import site
from django.apps import apps

print('=== DJANGO ADMIN VERIFICATION ===')
print(f'Admin site header: {site.site_header}')
print(f'Admin site title: {site.site_title}')

print('\n=== REGISTERED MODELS ===')
registered = list(site._registry.keys())
print(f'Total registered models: {len(registered)}')

for model in sorted(registered, key=lambda x: x._meta.label):
    admin_class = site._registry[model]
    print(f'  {model._meta.app_label}.{model.__name__} -> {admin_class.__class__.__name__}')

print('\n=== APPS WITH ADMIN.PY ===')
for app_config in apps.get_app_configs():
    admin_file = os.path.join(app_config.path, 'admin.py')
    if os.path.exists(admin_file):
        size = os.path.getsize(admin_file)
        print(f'  {app_config.label}: admin.py ({size} bytes)')

print('\n=== ADMIN IMPORT TEST ===')
for app_config in apps.get_app_configs():
    admin_file = os.path.join(app_config.path, 'admin.py')
    if os.path.exists(admin_file):
        try:
            module_name = f'{app_config.module.__name__}.admin'
            __import__(module_name)
            print(f'  {app_config.label}: SUCCESS')
        except Exception as e:
            print(f'  {app_config.label}: FAILED - {str(e)[:50]}')