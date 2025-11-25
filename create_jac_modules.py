#!/usr/bin/env python3
"""
Simple JAC Module Population Script
Creates the 5 JAC learning modules with correct field names
"""

import os
import sys
import json

# Add Django to path
sys.path.insert(0, '/workspace/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def setup_django():
    """Setup Django"""
    import django
    django.setup()
    
    # Import models
    from apps.users.models import User
    from apps.learning.models import LearningPath, Module, Lesson
    from apps.assessments.models import Assessment, AssessmentQuestion
    
    return {
        'User': User,
        'LearningPath': LearningPath,
        'Module': Module,
        'Lesson': Lesson,
        'Assessment': Assessment,
        'AssessmentQuestion': AssessmentQuestion
    }

def main():
    """Main function"""
    print("🚀 Creating JAC Learning Modules")
    print("=" * 50)
    
    try:
        # Setup Django
        print("🔧 Setting up Django...")
        models = setup_django()
        print("✅ Django setup complete")
        
        User = models['User']
        LearningPath = models['LearningPath']
        Module = models['Module']
        Lesson = models['Lesson']
        Assessment = models['Assessment']
        AssessmentQuestion = models['AssessmentQuestion']
        
        # Create or get admin user
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@jacplatform.com',
                password='admin123'
            )
        
        # Create JAC Learning Path
        jac_path, _ = LearningPath.objects.get_or_create(
            name="Complete JAC Programming Course",
            defaults={
                'description': "Comprehensive course covering all aspects of JAC programming from basics to production deployment",
                'difficulty_level': 'beginner',
                'estimated_duration': 38,  # 38 hours
                'created_by': admin_user,
                'is_published': True,
                'is_featured': True
            }
        )
        print(f"📚 Learning Path created: {jac_path.name}")
        
        # Create the 5 modules with correct field names
        modules_data = [
            {
                'title': 'Module 1: JAC Fundamentals',
                'description': 'Introduction to Jac and Basic Programming',
                'difficulty_rating': 2,
                'duration_minutes': 360,  # 6 hours
                'order': 1,
                'jac_concepts': ['JAC basics', 'Python compatibility', 'Variable types', 'Basic syntax']
            },
            {
                'title': 'Module 2: Object-Spatial Programming',
                'description': 'Master the OSP paradigm with nodes, edges, and walkers',
                'difficulty_rating': 3,
                'duration_minutes': 480,  # 8 hours
                'order': 2,
                'jac_concepts': ['Object-Spatial Programming', 'Nodes and edges', 'Walkers', 'Graph traversal']
            },
            {
                'title': 'Module 3: AI Integration and Advanced Features',
                'description': 'AI decorators, byLLM, and advanced programming patterns',
                'difficulty_rating': 4,
                'duration_minutes': 600,  # 10 hours
                'order': 3,
                'jac_concepts': ['AI decorators', 'byLLM', 'Async patterns', 'AI integration']
            },
            {
                'title': 'Module 4: Cloud Development and Deployment',
                'description': 'Production deployment and cloud-native features',
                'difficulty_rating': 4,
                'duration_minutes': 480,  # 8 hours
                'order': 4,
                'jac_concepts': ['Cloud deployment', 'Multi-user architecture', 'Cloud features', 'Production optimization']
            },
            {
                'title': 'Module 5: Production Applications',
                'description': 'Real-world projects and best practices',
                'difficulty_rating': 5,
                'duration_minutes': 360,  # 6 hours
                'order': 5,
                'jac_concepts': ['Production apps', 'Testing strategies', 'Debugging', 'Performance optimization']
            }
        ]
        
        created_modules = []
        for i, module_data in enumerate(modules_data, 1):
            module, created = Module.objects.get_or_create(
                learning_path=jac_path,
                order=module_data['order'],
                defaults={
                    'title': module_data['title'],
                    'description': module_data['description'],
                    'content': f"# {module_data['title']}\\n\\n{module_data['description']}\\n\\nThis module covers JAC programming fundamentals and advanced concepts.",
                    'content_type': 'markdown',
                    'duration_minutes': module_data['duration_minutes'],
                    'difficulty_rating': module_data['difficulty_rating'],
                    'jac_concepts': module_data['jac_concepts'],
                    'is_published': True
                }
            )
            if created:
                print(f"✅ Created {module_data['title']}")
            else:
                print(f"📖 Updated {module_data['title']}")
            created_modules.append(module)
            
            # Create a sample lesson for each module
            lesson, _ = Lesson.objects.get_or_create(
                module=module,
                order=1,
                defaults={
                    'title': f"Introduction to {module_data['title']}",
                    'lesson_type': 'text',
                    'content': f"Welcome to {module_data['title']}!\\n\\nThis lesson introduces the key concepts you'll learn in this module.",
                    'code_example': f'# Example code for {module_data["title"]}\\nprint("JAC is awesome!");'
                }
            )
            
            # Create assessment for each module
            assessment, _ = Assessment.objects.get_or_create(
                module=module,
                title=f"{module_data['title']} Assessment",
                defaults={
                    'description': f"Assessment for {module_data['title']}",
                    'assessment_type': 'quiz',
                    'time_limit': 60,
                    'max_attempts': 3,
                    'passing_score': 70.0,
                    'is_published': True
                }
            )
            
            # Add sample question
            question, _ = AssessmentQuestion.objects.get_or_create(
                assessment=assessment,
                defaults={
                    'title': f'Question 1 - {module_data["title"]}',
                    'question_text': f"What is the primary focus of {module_data['title']}?",
                    'question_type': 'multiple_choice',
                    'options': json.dumps([
                        "Basic programming concepts",
                        module_data['jac_concepts'][0] if module_data['jac_concepts'] else "Advanced features",
                        "Cloud development",
                        "AI integration"
                    ]),
                    'correct_answer': module_data['jac_concepts'][0] if module_data['jac_concepts'] else "Basic concepts",
                    'difficulty_level': 'medium',
                    'points': 1.0,
                    'order': 1
                }
            )
        
        print("\\n" + "=" * 50)
        print("🎉 JAC Learning Modules Created Successfully!")
        print("=" * 50)
        print(f"📚 Learning Path: {jac_path.name}")
        print(f"📖 Modules Created: {len(created_modules)}")
        print(f"📝 Assessments Created: {len(created_modules)}")
        print(f"❓ Questions Created: {len(created_modules)}")
        print(f"⏱️ Total Duration: {jac_path.estimated_duration} hours")
        print(f"🎯 Difficulty: {jac_path.get_difficulty_level_display()}")
        print("\\n✨ JAC Learning Platform now has full curriculum!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)