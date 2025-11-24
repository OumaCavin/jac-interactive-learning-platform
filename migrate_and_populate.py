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
from django.db import connection

print("🚀 Applying Django migrations...")

try:
    # Apply migrations for all apps
    call_command('migrate', verbosity=1)
    print("✅ Migrations applied successfully!")
    
    # Now try to populate the curriculum
    print("\n🎓 Populating JAC Learning Curriculum...")
    call_command('populate_jac_curriculum', verbosity=2)
    print("🎉 Curriculum populated successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Try alternative approach - run the specific migration
    print("\n🔄 Trying alternative approach...")
    
    try:
        # Try applying users migration specifically
        from django.db import migrations
        
        # Apply users migration manually
        call_command('makemigrations', 'users', verbosity=1)
        call_command('migrate', 'users', verbosity=1)
        
        # Apply other migrations
        call_command('migrate', 'jac_execution', verbosity=1)
        call_command('migrate', 'learning', verbosity=1)
        
        # Now try curriculum
        print("\n🎓 Trying curriculum population again...")
        call_command('populate_jac_curriculum', verbosity=2)
        print("🎉 Curriculum populated successfully!")
        
    except Exception as e2:
        print(f"❌ Alternative approach also failed: {e2}")

print("\n📊 Checking final results...")

# Check what was created
try:
    from apps.learning.models import LearningPath, Module, Lesson, Assessment, Question
    
    print(f"📚 Learning Paths: {LearningPath.objects.count()}")
    print(f"📖 Modules: {Module.objects.count()}")
    print(f"📝 Lessons: {Lesson.objects.count()}")
    print(f"🎯 Assessments: {Assessment.objects.count()}")
    print(f"❓ Questions: {Question.objects.count()}")
    
    # Check admin user
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_users = User.objects.filter(is_superuser=True).count()
    print(f"👤 Admin Users: {admin_users}")
    
    if LearningPath.objects.count() > 0:
        print("\n✅ SUCCESS! JAC Learning Curriculum has been populated!")
    else:
        print("\n⚠️  Curriculum population may not have completed successfully")
        
except Exception as e:
    print(f"❌ Error checking results: {e}")

print("\n🏁 Process completed!")