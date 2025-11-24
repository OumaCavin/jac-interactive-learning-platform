#!/usr/bin/env python3
"""
Script to create migrations with automatic 'yes' responses.
"""
import os
import sys
import subprocess
import django

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Set up Django
django.setup()

# Create the migrations command with automatic yes responses
env = os.environ.copy()
env['PYTHONPATH'] = '/tmp/.venv/lib/python3.12/site-packages:/workspace/backend'

try:
    # Use subprocess to run the command with automatic 'y' responses
    cmd = [
        '/tmp/.venv/bin/python', 
        '/workspace/backend/manage.py', 
        'makemigrations', 
        'users'
    ]
    
    print("Creating migrations for users app...")
    
    # Run with input to automatically answer 'y' to prompts
    result = subprocess.run(
        cmd,
        input='y\n',  # Automatically answer 'y' to field rename prompts
        env=env,
        cwd='/workspace/backend',
        text=True,
        capture_output=True,
        timeout=60
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Return code: {result.returncode}")
    
    if result.returncode == 0:
        print("\\n✅ Migrations created successfully!")
        
        # List migration files
        migrations_dir = '/workspace/backend/apps/users/migrations'
        if os.path.exists(migrations_dir):
            migration_files = [f for f in os.listdir(migrations_dir) if f.endswith('.py') and f != '__init__.py']
            print(f"\\nMigration files created:")
            for f in sorted(migration_files):
                print(f"  - {f}")
    else:
        print("\\n❌ Migration creation failed")

except subprocess.TimeoutExpired:
    print("Migration creation timed out")
except Exception as e:
    print(f"Error running migration script: {e}")
    import traceback
    traceback.print_exc()