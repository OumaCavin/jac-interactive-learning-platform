#!/usr/bin/env python3
"""
Fix migration history by manually marking learning migrations as applied
"""

import sqlite3
import os

def fix_migration_history():
    os.chdir('/workspace/backend')
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("🔧 Fixing migration history...")
    
    # First, check what migrations exist in the database
    cursor.execute("SELECT app, name FROM django_migrations ORDER BY id")
    applied_migrations = cursor.fetchall()
    print("📊 Currently applied migrations:")
    for app, name in applied_migrations:
        print(f"  {app}: {name}")
    
    # Remove any existing learning migrations to avoid conflicts
    cursor.execute("DELETE FROM django_migrations WHERE app = 'learning'")
    removed_count = cursor.rowcount
    print(f"✅ Removed {removed_count} existing learning migrations")
    
    # Add the learning migrations as if they were applied
    learning_migrations = [
        ('learning', '0001_initial'),
        ('learning', '0002_initial'),
        ('learning', '0003_adaptive_learning_clean')
    ]
    
    for app, name in learning_migrations:
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES (?, ?, ?)
        """, (app, name, '2025-11-26 07:26:00.000000'))
    
    print("✅ Added learning migrations to history")
    
    conn.commit()
    conn.close()
    
    print("🎉 Migration history fixed!")

if __name__ == "__main__":
    fix_migration_history()