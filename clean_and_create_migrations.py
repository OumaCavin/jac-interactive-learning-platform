#!/usr/bin/env python3
"""
Script to clean up migration tracking and create fresh migrations.
"""
import os
import sys
import sqlite3
import django

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

# Connect to the database
db_path = '/workspace/backend/db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Remove users app migration records
    print("Removing users app migration records...")
    cursor.execute("DELETE FROM django_migrations WHERE app = 'users'")
    deleted_count = cursor.rowcount
    print(f"Deleted {deleted_count} migration records for users app")
    
    # Also remove references to users tables that might cause issues
    print("Checking for any other references to users in migration tracking...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%user%'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"Found table: {table[0]}")
    
    conn.commit()
    print("\\n✅ Migration tracking cleaned up!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()

# Now create fresh migrations
print("\\n=== Creating fresh migrations ===")
from django.core.management import call_command

try:
    call_command('makemigrations', 'users', verbosity=2)
    print("\\n✅ Fresh migrations created successfully!")
    
except Exception as e:
    print(f"❌ Error creating migrations: {e}")
    import traceback
    traceback.print_exc()