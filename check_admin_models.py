#!/usr/bin/env python
"""
Script to check registered Django admin models
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')
django.setup()

from django.apps import apps

print('=== REGISTERED ADMIN MODELS ===')
for app_config in apps.get_app_configs():
    if hasattr(app_config, 'admin_site'):
        print(f'\nApp: {app_config.label}')
        try:
            models = list(app_config.get_models())
            print(f'Models found: {len(models)}')
            for model in models:
                print(f'  - {model.__name__}')
        except Exception as e:
            print(f'  Error: {e}')

print('\n=== ADMIN SITE INFO ===')
from config.custom_admin import custom_admin_site
print(f'Admin site header: {custom_admin_site.site_header}')
print(f'Admin site title: {custom_admin_site.site_title}')
print(f'Admin index title: {custom_admin_site.index_title}')