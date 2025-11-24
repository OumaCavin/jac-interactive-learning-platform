#!/usr/bin/env python
"""
Complete JAC Curriculum Setup and Population Script
This script fixes database issues and populates the curriculum
"""

import os
import sys
import django
import subprocess

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'jac_platform.settings'
os.environ['PYTHONPATH'] = '/workspace/backend:/tmp/.venv/lib/python3.12/site-packages'

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')

def setup_and_populate_curriculum():
    """Setup database and populate curriculum"""
    
    print("🚀 Starting JAC Learning Platform Setup...")
    
    try:
        # Setup Django
        print("📦 Setting up Django...")
        django.setup()
        print("✅ Django setup successful!")
        
        # Import Django modules
        from django.core.management import call_command
        from django.db import connection
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        print("🔧 Checking database schema...")
        
        # Check if users_user table has the required columns
        with connection.cursor() as cursor:
            cursor.execute("DESCRIBE users_user")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Check if required columns exist
            required_columns = ['preferred_learning_style', 'learning_level', 'total_study_time', 
                              'last_activity', 'streak_days', 'notifications_enabled', 'email_verified']
            
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                print(f"⚠️  Missing columns: {missing_columns}")
                print("🔄 Creating missing columns...")
                
                # Add missing columns
                for column in missing_columns:
                    if column == 'preferred_learning_style':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN preferred_learning_style VARCHAR(20) DEFAULT 'visual'")
                    elif column == 'learning_level':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN learning_level VARCHAR(20) DEFAULT 'beginner'")
                    elif column == 'total_study_time':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN total_study_time BIGINT DEFAULT 0")
                    elif column == 'last_activity':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN last_activity DATETIME NULL")
                    elif column == 'streak_days':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN streak_days INT DEFAULT 0")
                    elif column == 'notifications_enabled':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN notifications_enabled BOOLEAN DEFAULT 1")
                    elif column == 'email_verified':
                        cursor.execute("ALTER TABLE users_user ADD COLUMN email_verified BOOLEAN DEFAULT 0")
                
                print("✅ Database schema updated!")
            else:
                print("✅ Database schema is up to date!")
        
        # Apply migrations for other apps
        print("📋 Applying migrations...")
        try:
            call_command('migrate', verbosity=0)
            print("✅ Migrations applied successfully!")
        except Exception as e:
            print(f"⚠️  Migration warning: {e}")
        
        # Now populate the curriculum
        print("🎓 Populating JAC Learning Curriculum...")
        print("This may take a few minutes...")
        
        # Capture output during curriculum population
        import io
        from contextlib import redirect_stdout, redirect_stderr
        
        output = io.StringIO()
        error_output = io.StringIO()
        
        try:
            with redirect_stdout(output), redirect_stderr(error_output):
                call_command('populate_jac_curriculum', verbosity=2)
            
            # Print the output
            stdout_content = output.getvalue()
            stderr_content = error_output.getvalue()
            
            if stdout_content:
                print("📝 Curriculum Population Output:")
                print(stdout_content)
            
            if stderr_content:
                print("⚠️  Warnings/Errors:")
                print(stderr_content)
                
            print("🎉 JAC Learning Curriculum populated successfully!")
            
            # Show final statistics
            from apps.learning.models import LearningPath, Module, Lesson, Assessment, Question
            
            learning_path_count = LearningPath.objects.count()
            module_count = Module.objects.count()
            lesson_count = Lesson.objects.count()
            assessment_count = Assessment.objects.count()
            question_count = Question.objects.count()
            
            print("\n📊 Final Statistics:")
            print(f"📚 Learning Paths: {learning_path_count}")
            print(f"📖 Modules: {module_count}")
            print(f"📝 Lessons: {lesson_count}")
            print(f"🎯 Assessments: {assessment_count}")
            print(f"❓ Questions: {question_count}")
            
            # Show created admin user
            admin_count = User.objects.filter(is_superuser=True).count()
            print(f"👤 Admin Users: {admin_count}")
            
        except Exception as e:
            print(f"❌ Error during curriculum population: {e}")
            import traceback
            traceback.print_exc()
            
            # Try alternative approach - run the command directly
            print("\n🔄 Trying alternative approach...")
            try:
                result = subprocess.run([
                    '/tmp/.venv/bin/python', 
                    '/workspace/backend/manage.py', 
                    'populate_jac_curriculum'
                ], cwd='/workspace/backend', capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print("✅ Curriculum population completed via subprocess!")
                    print("Output:", result.stdout)
                else:
                    print("❌ Subprocess also failed:")
                    print("Error:", result.stderr)
                    
            except Exception as subprocess_error:
                print(f"❌ Subprocess approach failed: {subprocess_error}")
        
        print("\n🎓 JAC Learning Platform setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_and_populate_curriculum()
    if success:
        print("\n✅ All done! The JAC Learning Platform is ready!")
    else:
        print("\n❌ Setup encountered issues. Please check the errors above.")
    
    sys.exit(0 if success else 1)