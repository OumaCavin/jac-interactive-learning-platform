#!/usr/bin/env python
import os
import sys
import subprocess

# Set environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'jac_platform.settings'
os.environ['PYTHONPATH'] = '/workspace/backend:/tmp/.venv/lib/python3.12/site-packages'

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')

try:
    # Import and run the command
    import django
    django.setup()
    
    from django.core.management import call_command
    
    print("Running curriculum population...")
    call_command('populate_jac_curriculum')
    print("Curriculum population completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()