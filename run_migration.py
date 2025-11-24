#!/usr/bin/env python
"""
Simple script to run Django migrations directly.
"""
import os
import sys

# Add the backend directory to Python path
backend_path = '/workspace/backend'
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command

try:
    print("Running makemigrations for users app...")
    call_command('makemigrations', 'users')
    
    print("Running migrate for users app...")
    call_command('migrate', 'users')
    
    print("Checking migration status...")
    call_command('showmigrations')
    
    print("Migration completed successfully!")
    
except Exception as e:
    print(f"Error during migration: {e}")
    import traceback
    traceback.print_exc()