#!/usr/bin/env python

import os
import sys

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'jac_platform.settings'
os.environ['PYTHONPATH'] = '/workspace/backend:/tmp/.venv/lib/python3.12/site-packages'

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')

# Import Django
import django
django.setup()

# Import database modules
from django.db import connection

print("🚀 Fixing database schema with direct SQL...")

try:
    with connection.cursor() as cursor:
        print("📋 Checking current table structure...")
        
        # Check if users_user table exists and its structure
        try:
            cursor.execute("DESCRIBE users_user")
            current_columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns: {current_columns}")
        except Exception as e:
            print(f"⚠️  Could not describe users_user table: {e}")
            current_columns = []
        
        # Required columns for the custom User model
        required_columns = {
            'preferred_learning_style': 'VARCHAR(20) DEFAULT "visual"',
            'learning_level': 'VARCHAR(20) DEFAULT "beginner"',
            'total_study_time': 'BIGINT DEFAULT 0',
            'last_activity': 'DATETIME NULL',
            'streak_days': 'INT DEFAULT 0',
            'notifications_enabled': 'BOOLEAN DEFAULT TRUE',
            'email_verified': 'BOOLEAN DEFAULT FALSE'
        }
        
        print("🔧 Adding missing columns...")
        
        added_columns = []
        failed_columns = []
        
        for column_name, column_def in required_columns.items():
            if column_name not in current_columns:
                try:
                    print(f"➕ Adding {column_name}...")
                    cursor.execute(f"ALTER TABLE users_user ADD COLUMN {column_name} {column_def}")
                    print(f"✅ Successfully added {column_name}")
                    added_columns.append(column_name)
                except Exception as e:
                    print(f"❌ Failed to add {column_name}: {e}")
                    failed_columns.append(column_name)
            else:
                print(f"✅ {column_name} already exists")
        
        print(f"\n📊 Summary:")
        print(f"✅ Columns added: {len(added_columns)}")
        print(f"❌ Columns failed: {len(failed_columns)}")
        if added_columns:
            print(f"   Added: {', '.join(added_columns)}")
        if failed_columns:
            print(f"   Failed: {', '.join(failed_columns)}")
        
        # Verify the changes
        print("\n🔍 Verifying changes...")
        cursor.execute("DESCRIBE users_user")
        final_columns = [row[0] for row in cursor.fetchall()]
        
        missing_final = [col for col in required_columns.keys() if col not in final_columns]
        
        if not missing_final:
            print("✅ All required columns are now present!")
            
            # Now try to run the curriculum population
            print("\n🎓 Attempting curriculum population...")
            
            try:
                from django.core.management import call_command
                call_command('populate_jac_curriculum', verbosity=2)
                print("🎉 SUCCESS! Curriculum populated!")
                
            except Exception as e:
                print(f"❌ Curriculum population failed: {e}")
                print("🔄 Trying subprocess approach...")
                
                import subprocess
                try:
                    result = subprocess.run([
                        '/tmp/.venv/bin/python', 
                        '/workspace/backend/manage.py', 
                        'populate_jac_curriculum'
                    ], cwd='/workspace/backend', capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0:
                        print("✅ SUCCESS! Curriculum populated via subprocess!")
                        print("Output:", result.stdout)
                    else:
                        print("❌ Subprocess failed:")
                        print("Error:", result.stderr)
                        
                except Exception as subprocess_error:
                    print(f"❌ Subprocess also failed: {subprocess_error}")
            
        else:
            print(f"❌ Still missing columns: {missing_final}")
            print("Database schema fix incomplete")
    
    # Check final results
    print("\n📊 Checking final results...")
    try:
        from apps.learning.models import LearningPath, Module, Lesson, Assessment, Question
        
        lp_count = LearningPath.objects.count()
        mod_count = Module.objects.count()
        les_count = Lesson.objects.count()
        ass_count = Assessment.objects.count()
        que_count = Question.objects.count()
        
        print(f"📚 Learning Paths: {lp_count}")
        print(f"📖 Modules: {mod_count}")
        print(f"📝 Lessons: {les_count}")
        print(f"🎯 Assessments: {ass_count}")
        print(f"❓ Questions: {que_count}")
        
        if lp_count > 0:
            print("\n🎉 SUCCESS! JAC Learning Platform curriculum has been populated!")
        else:
            print("\n⚠️  No curriculum data found. Population may have failed.")
            
    except Exception as e:
        print(f"❌ Error checking results: {e}")
    
except Exception as e:
    print(f"❌ Database fix failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Process completed!")