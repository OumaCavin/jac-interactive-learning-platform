#!/usr/bin/env python
import sqlite3
import subprocess
import os

print("🔧 Direct SQL fix for JAC curriculum...")

try:
    # Connect to SQLite database directly
    db_path = '/workspace/backend/db.sqlite3'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("📋 Checking current users_user table structure...")
    
    # Get current columns
    cursor.execute("PRAGMA table_info(users_user)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Current columns: {columns}")
    
    # Required columns
    required_columns = [
        ('preferred_learning_style', 'VARCHAR(20) DEFAULT "visual"'),
        ('learning_level', 'VARCHAR(20) DEFAULT "beginner"'),
        ('total_study_time', 'BIGINT DEFAULT 0'),
        ('last_activity', 'DATETIME NULL'),
        ('streak_days', 'INTEGER DEFAULT 0'),
        ('notifications_enabled', 'BOOLEAN DEFAULT 1'),
        ('email_verified', 'BOOLEAN DEFAULT 0')
    ]
    
    # Add missing columns
    missing_columns = []
    for column_name, column_def in required_columns:
        if column_name not in columns:
            try:
                print(f"➕ Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE users_user ADD COLUMN {column_name} {column_def}")
                print(f"✅ Added {column_name}")
                missing_columns.append(column_name)
            except Exception as e:
                print(f"❌ Failed to add {column_name}: {e}")
        else:
            print(f"✅ {column_name} already exists")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n📊 Summary: Added {len(missing_columns)} columns")
    if missing_columns:
        print(f"Added: {', '.join(missing_columns)}")
    
    # Now try to run the curriculum command
    print("\n🎓 Attempting curriculum population...")
    
    result = subprocess.run([
        'python', 'manage.py', 'populate_jac_curriculum'
    ], cwd='/workspace/backend', capture_output=True, text=True, timeout=120)
    
    print(f"Return code: {result.returncode}")
    
    if result.stdout:
        print("\n📝 Output:")
        print(result.stdout)
    
    if result.stderr:
        print("\n⚠️  Errors/Warnings:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("\n🎉 SUCCESS! JAC curriculum has been populated!")
    else:
        print("\n⚠️  Curriculum population returned non-zero exit code")
        
    # Check what was created
    print("\n📊 Verifying results...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check learning tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'learning_%'")
    learning_tables = [row[0] for row in cursor.fetchall()]
    
    if learning_tables:
        print(f"📚 Learning tables found: {learning_tables}")
        
        # Count records
        for table in learning_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} records")
    else:
        print("⚠️  No learning tables found")
    
    # Check admin user
    cursor.execute("SELECT username FROM users_user WHERE is_superuser = 1 LIMIT 1")
    admin_user = cursor.fetchone()
    if admin_user:
        print(f"👤 Admin user: {admin_user[0]}")
    else:
        print("⚠️  No admin user found")
    
    conn.close()
    
    print("\n🏁 Process completed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()