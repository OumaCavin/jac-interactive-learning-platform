#!/usr/bin/env python3
"""
Verify curriculum data was populated successfully.
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, '/workspace/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Import models
try:
    from apps.learning.models import LearningPath, Module, Lesson, Assessment
    print("✅ Models imported successfully")
except Exception as e:
    print(f"❌ Model import failed: {e}")
    sys.exit(1)

# Check data counts
def check_curriculum_data():
    try:
        learning_paths = LearningPath.objects.all()
        modules = Module.objects.all()
        lessons = Lesson.objects.all()
        assessments = Assessment.objects.all()

        print("\n📊 Curriculum Data Summary:")
        print("=" * 50)
        print(f"Learning Paths: {learning_paths.count()}")
        print(f"Modules: {modules.count()}")
        print(f"Lessons: {lessons.count()}")
        print(f"Assessments: {assessments.count()}")
        print("=" * 50)

        if learning_paths.count() > 0:
            print("\n🎓 Learning Paths:")
            for lp in learning_paths:
                print(f"  - {lp.title} (ID: {lp.id})")
                
        if modules.count() > 0:
            print(f"\n📚 Modules ({modules.count()} total):")
            for module in modules.order_by('learning_path_id', 'order'):
                print(f"  - {module.title} (Order: {module.order}) - Path: {module.learning_path.title if module.learning_path else 'None'}")
                
        if lessons.count() > 0:
            print(f"\n📝 Sample Lessons (first 10 of {lessons.count()}):")
            for lesson in lessons.order_by('module__order', 'order')[:10]:
                print(f"  - {lesson.title} (Module: {lesson.module.title if lesson.module else 'None'}, Order: {lesson.order})")
                
        if assessments.count() > 0:
            print(f"\n✅ Assessments ({assessments.count()} total):")
            for assessment in assessments.order_by('module__order', 'order'):
                print(f"  - {assessment.title} (Module: {assessment.module.title if assessment.module else 'None'})")

        # Check for specific JAC curriculum
        jac_path = learning_paths.filter(title__icontains='JAC').first()
        if jac_path:
            print(f"\n🎯 JAC Learning Path Found:")
            print(f"  - ID: {jac_path.id}")
            print(f"  - Title: {jac_path.title}")
            print(f"  - Description: {jac_path.description[:100]}...")
            
            jac_modules = modules.filter(learning_path=jac_path)
            print(f"  - JAC Modules: {jac_modules.count()}")
            
            for module in jac_modules.order_by('order'):
                module_lessons = lessons.filter(module=module)
                module_assessments = assessments.filter(module=module)
                print(f"    📖 {module.title}: {module_lessons.count()} lessons, {module_assessments.count()} assessments")
                
        print("\n✅ Curriculum verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error checking curriculum data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_curriculum_data()
    sys.exit(0 if success else 1)