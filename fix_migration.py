#!/usr/bin/env python3
import subprocess
import sys
import time

def fix_migration_issue():
    """Fix the migration issue by deleting the conflicting migration and recreating it"""
    
    print("Fixing migration issue...")
    
    # 1. Delete the problematic migration file
    migration_file = "/workspace/backend/apps/learning/migrations/0003_add_adaptive_learning_models.py"
    try:
        import os
        if os.path.exists(migration_file):
            os.remove(migration_file)
            print(f"Deleted problematic migration file: {migration_file}")
        
        # Also delete any __pycache__ files
        cache_dir = "/workspace/backend/apps/learning/migrations/__pycache__"
        if os.path.exists(cache_dir):
            for file in os.listdir(cache_dir):
                if file.endswith('.pyc'):
                    os.remove(os.path.join(cache_dir, file))
            print("Cleaned up migration cache files")
        
    except Exception as e:
        print(f"Error cleaning migration files: {e}")
    
    # 2. Check if database has easiness_factor column
    try:
        import sqlite3
        conn = sqlite3.connect('/workspace/backend/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(learning_spacedrepetitionsession)")
        columns = cursor.fetchall()
        
        has_easiness = False
        has_ease = False
        
        for col in columns:
            if col[1] == 'easiness_factor':
                has_easiness = True
            elif col[1] == 'ease_factor':
                has_ease = True
        
        print(f"Database columns check - has_easiness: {has_easiness}, has_ease: {has_ease}")
        
        if has_easiness and not has_ease:
            # Rename the column in database
            cursor.execute("ALTER TABLE learning_spacedrepetitionsession RENAME COLUMN easiness_factor TO ease_factor")
            print("Renamed easiness_factor column to ease_factor in database")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking/fixing database: {e}")
    
    # 3. Create a new migration with correct field name
    try:
        # First makemigrations
        result = subprocess.run([
            sys.executable, "manage.py", "makemigrations", "learning"
        ], cwd="/workspace/backend", capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("Successfully created new migration file")
            print(result.stdout)
        else:
            print(f"Error creating migration: {result.stderr}")
            
    except Exception as e:
        print(f"Error in makemigrations: {e}")

if __name__ == "__main__":
    fix_migration_issue()