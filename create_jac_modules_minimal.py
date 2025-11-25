#!/usr/bin/env python3
"""
Minimal JAC Module Creation Script
Creates just the 5 JAC learning modules
"""

import os
import sys

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
    from apps.learning.models import LearningPath, Module
    
    return {
        'User': User,
        'LearningPath': LearningPath,
        'Module': Module
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
        
        print("\\n" + "=" * 50)
        print("🎉 JAC Learning Modules Created Successfully!")
        print("=" * 50)
        print(f"📚 Learning Path: {jac_path.name}")
        print(f"📖 Modules Created: {len(created_modules)}")
        print(f"⏱️ Total Duration: {jac_path.estimated_duration} hours")
        print(f"🎯 Difficulty: {jac_path.get_difficulty_level_display()}")
        
        # List all modules
        print("\\n📋 JAC Curriculum Modules:")
        for module in created_modules:
            print(f"   {module.order}. {module.title} ({module.duration_minutes} minutes)")
        
        print("\\n✨ JAC Learning Platform now has full curriculum!")
        print("\\n🌟 The modules cover:")
        print("   - JAC Fundamentals and Python compatibility")
        print("   - Object-Spatial Programming paradigm")
        print("   - AI Integration and advanced features")
        print("   - Cloud Development and deployment")
        print("   - Production Applications and best practices")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)