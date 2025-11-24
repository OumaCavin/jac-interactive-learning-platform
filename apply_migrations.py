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

# Import Django modules
from django.core.management import call_command

print("🚀 Applying the newly created migrations...")

try:
    # Apply migrations for users app first
    print("📋 Applying users migrations...")
    call_command('migrate', 'users', verbosity=2)
    print("✅ Users migrations applied!")
    
    # Apply migrations for learning app
    print("\n📋 Applying learning migrations...")
    call_command('migrate', 'learning', verbosity=2)
    print("✅ Learning migrations applied!")
    
    # Apply migrations for jac_execution app if it exists
    print("\n📋 Applying jac_execution migrations...")
    try:
        call_command('migrate', 'jac_execution', verbosity=2)
        print("✅ jac_execution migrations applied!")
    except Exception as e:
        print(f"⚠️  jac_execution migration error (may be expected): {e}")
    
    # Apply all remaining migrations
    print("\n📋 Applying remaining migrations...")
    call_command('migrate', verbosity=1)
    print("✅ All migrations applied!")
    
    # Now populate the curriculum
    print("\n🎓 Populating JAC Learning Curriculum...")
    print("This may take a few minutes...")
    
    call_command('populate_jac_curriculum', verbosity=2)
    print("🎉 Curriculum population completed successfully!")
    
except Exception as e:
    print(f"❌ Error during migration/population: {e}")
    import traceback
    traceback.print_exc()
    
    # Try to at least run the curriculum command
    print("\n🔄 Trying curriculum command directly...")
    try:
        call_command('populate_jac_curriculum', verbosity=1)
        print("✅ Curriculum population worked!")
    except Exception as e2:
        print(f"❌ Curriculum command also failed: {e2}")

# Check final results
print("\n📊 Checking final results...")

try:
    from apps.learning.models import LearningPath, Module, Lesson, Assessment, Question
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Count records
    lp_count = LearningPath.objects.count()
    mod_count = Module.objects.count()
    les_count = Lesson.objects.count()
    ass_count = Assessment.objects.count()
    que_count = Question.objects.count()
    admin_count = User.objects.filter(is_superuser=True).count()
    
    print(f"📚 Learning Paths: {lp_count}")
    print(f"📖 Modules: {mod_count}")
    print(f"📝 Lessons: {les_count}")
    print(f"🎯 Assessments: {ass_count}")
    print(f"❓ Questions: {que_count}")
    print(f"👤 Admin Users: {admin_count}")
    
    if lp_count > 0:
        print("\n🎉 SUCCESS! JAC Learning Platform curriculum has been populated!")
        print("\n📋 Here's what was created:")
        print(f"   • {lp_count} comprehensive learning path(s)")
        print(f"   • {mod_count} detailed module(s) covering JAC fundamentals to production")
        print(f"   • {les_count} interactive lesson(s) with code examples")
        print(f"   • {ass_count} assessment(s) with questions and exercises")
        print(f"   • {que_count} question(s) for testing knowledge")
        
        # Show first learning path details
        learning_path = LearningPath.objects.first()
        if learning_path:
            print(f"\n📖 Learning Path: '{learning_path.name}'")
            print(f"   Description: {learning_path.description}")
            print(f"   Difficulty: {learning_path.difficulty_level}")
            print(f"   Duration: {learning_path.estimated_duration} hours")
        
    else:
        print("\n⚠️  No curriculum data found. Population may have failed.")
    
except Exception as e:
    print(f"❌ Error checking results: {e}")

print("\n🏁 JAC Learning Platform setup process completed!")