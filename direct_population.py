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

print("🚀 Attempting direct curriculum population...")

try:
    from django.core.management import call_command
    
    # Try to populate the curriculum directly
    print("🎓 Running curriculum population command...")
    call_command('populate_jac_curriculum', verbosity=2)
    print("✅ SUCCESS! Curriculum populated successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Try alternative approach - manually create the content
    print("\n🔄 Trying alternative approach...")
    
    try:
        # Import models
        from apps.learning.models import LearningPath, Module, Lesson, Assessment, Question
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        
        print("📋 Creating curriculum content manually...")
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@jaclang.org',
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("✅ Created admin user")
        
        # Create learning path
        learning_path, created = LearningPath.objects.get_or_create(
            name="Complete JAC Programming Language Course",
            defaults={
                'description': 'Comprehensive course covering JAC programming from fundamentals to production applications.',
                'difficulty_level': 'beginner',
                'estimated_duration': 80,
                'prerequisites': [],
                'tags': ['programming', 'jac', 'osp'],
                'is_published': True,
                'is_featured': True,
                'created_by': admin_user,
            }
        )
        if created:
            print(f"✅ Created learning path: {learning_path.name}")
        
        # Create first module
        module, created = Module.objects.get_or_create(
            learning_path=learning_path,
            order=1,
            defaults={
                'title': 'JAC Fundamentals (Week 1-2)',
                'description': 'Master JAC syntax, variables, data types, functions, and control flow.',
                'content': '# Module 1: JAC Fundamentals\n\nWelcome to JAC programming!',
                'content_type': 'markdown',
                'duration_minutes': 960,
                'difficulty_rating': 2,
                'jac_concepts': ['variables', 'types', 'functions'],
                'code_examples': [],
                'has_quiz': True,
                'has_coding_exercise': True,
                'is_published': True,
            }
        )
        if created:
            print(f"✅ Created module: {module.title}")
        
        # Create first lesson
        lesson, created = Lesson.objects.get_or_create(
            module=module,
            order=1,
            defaults={
                'title': 'Introduction to JAC',
                'lesson_type': 'text',
                'content': '# Welcome to JAC Programming!\n\nJAC is a modern programming language.',
                'code_example': 'withentry {\n    print("Hello, JAC World!");\n}',
                'estimated_duration': 30,
                'is_published': True,
            }
        )
        if created:
            print(f"✅ Created lesson: {lesson.title}")
        
        # Create first assessment
        assessment, created = Assessment.objects.get_or_create(
            module=module,
            title='JAC Fundamentals Quiz',
            defaults={
                'description': 'Test your understanding of JAC basics.',
                'assessment_type': 'quiz',
                'difficulty_level': 'beginner',
                'passing_score': 70.0,
                'is_published': True,
            }
        )
        if created:
            print(f"✅ Created assessment: {assessment.title}")
        
        print("\n🎉 Manual curriculum creation completed!")
        
    except Exception as e2:
        print(f"❌ Manual approach failed: {e2}")
        import traceback
        traceback.print_exc()

# Check final results
print("\n📊 Checking final results...")

try:
    from apps.learning.models import LearningPath, Module, Lesson, Assessment
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Count records
    lp_count = LearningPath.objects.count()
    mod_count = Module.objects.count()
    les_count = Lesson.objects.count()
    ass_count = Assessment.objects.count()
    admin_count = User.objects.filter(is_superuser=True).count()
    
    print(f"📚 Learning Paths: {lp_count}")
    print(f"📖 Modules: {mod_count}")
    print(f"📝 Lessons: {les_count}")
    print(f"🎯 Assessments: {ass_count}")
    print(f"👤 Admin Users: {admin_count}")
    
    if lp_count > 0:
        print("\n🎉 SUCCESS! JAC Learning Platform content has been created!")
        print("\n📋 Content Summary:")
        print(f"   • {lp_count} learning path(s)")
        print(f"   • {mod_count} module(s)")
        print(f"   • {les_count} lesson(s)")
        print(f"   • {ass_count} assessment(s)")
        
        # Show details
        learning_path = LearningPath.objects.first()
        if learning_path:
            print(f"\n📖 Main Learning Path: '{learning_path.name}'")
            print(f"   Description: {learning_path.description}")
            
            modules = Module.objects.filter(learning_path=learning_path)
            if modules.exists():
                print(f"   Modules: {', '.join([m.title for m in modules])}")
        
        print("\n🔐 Admin Access:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   URL: http://localhost:8000/admin/")
        
    else:
        print("\n⚠️  No curriculum content found.")
    
except Exception as e:
    print(f"❌ Error checking results: {e}")

print("\n🏁 JAC Learning Platform setup process completed!")