#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, '/workspace/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_platform.settings')

# Setup Django
django.setup()

# Now we can use Django models
from django.core.management import call_command
from apps.users.models import User

print("Django setup successful!")
print(f"User model fields: {[field.name for field in User._meta.fields]}")

# Try to apply migrations
print("Applying migrations...")
try:
    call_command('migrate', verbosity=1)
    print("Migrations applied successfully!")
except Exception as e:
    print(f"Error applying migrations: {e}")

# Now try curriculum population
print("Populating JAC curriculum...")
try:
    call_command('populate_jac_curriculum', verbosity=1)
    print("Curriculum populated successfully!")
except Exception as e:
    print(f"Error populating curriculum: {e}")