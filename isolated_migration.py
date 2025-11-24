import os
import sys
import subprocess
import uuid

# Create a unique temp directory for this script
temp_dir = f"/tmp/migration_{uuid.uuid4()}"
os.makedirs(temp_dir, exist_ok=True)

# Create isolated migration script
migration_script = f"""#!/usr/bin/env python3
import os
import sys
import django
from django.conf import settings

# Minimal Django setup
sys.path.insert(0, '/workspace/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

try:
    django.setup()
    from django.core.management import call_command
    
    print("=== Starting Migration Process ===")
    print("1. Making migrations for users app...")
    call_command('makemigrations', 'users', verbosity=2)
    
    print("\\n2. Applying migrations for users app...")
    call_command('migrate', 'users', verbosity=2)
    
    print("\\n3. Checking migration status...")
    call_command('showmigrations', verbosity=1)
    
    print("\\n✅ Migration completed successfully!")
    
except Exception as e:
    print(f"❌ Error: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""

# Write the script
script_path = f"{temp_dir}/migrate.py"
with open(script_path, 'w') as f:
    f.write(migration_script)

print(f"Created migration script at: {script_path}")

# Run it in a completely isolated environment
env = os.environ.copy()
env['PYTHONPATH'] = '/tmp/.venv/lib/python3.12/site-packages:/workspace/backend'
env['DJANGO_SETTINGS_MODULE'] = 'config.settings'

try:
    result = subprocess.run(
        ['/tmp/.venv/bin/python', script_path],
        env=env,
        cwd='/workspace/backend',
        capture_output=True,
        text=True,
        timeout=60
    )
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
        
    print(f"Return code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("Migration script timed out")
except Exception as e:
    print(f"Error running migration script: {e}")

# Cleanup
import shutil
shutil.rmtree(temp_dir, ignore_errors=True)