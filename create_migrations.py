#!/usr/bin/env python3
"""
Script to create migrations automatically with 'yes' responses.
"""
import os
import sys
import django

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

from django.core.management import call_command

try:
    print("Creating migrations for users app...")
    
    # Use the migration command with verbosity to see what's happening
    call_command('makemigrations', 'users', verbosity=2)
    
    print("\\n✅ Migrations created successfully!")
    
    # Check what migrations were created
    from django.apps import apps
    users_app = apps.get_app_config('users')
    print(f"\\nMigration files in users app:")
    for migration in users_app.get_migrations().migrations:
        print(f"  - {migration}")
    
except Exception as e:
    print(f"❌ Error creating migrations: {e}")
    import traceback
    traceback.print_exc()