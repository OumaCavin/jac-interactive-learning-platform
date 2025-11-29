#!/usr/bin/env python3
"""
JAC Interactive Learning Platform - Data Loader
Systematically loads initial data in the correct order to avoid dependency issues.
"""

import os
import sys
import django
from django.conf import settings
from django.contrib.auth import get_user_model

# Configure Django settings
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import json

def print_step(step_num, description):
    """Print step header"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print('='*60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def create_admin_user():
    """Step 1: Create admin user - PRODUCTION VERSION
    
    NOTE: Hardcoded user creation has been removed for production security.
    Admin users should be created through Django admin interface or 
    management commands with secure credentials.
    """
    print_step(1, "Admin User Setup")
    
    User = get_user_model()
    
    print_success("Admin user creation disabled for production security.")
    print("To create admin user:")
    print("  1. Run: python manage.py createsuperuser")
    print("  2. Or use Django admin at http://localhost:8000/admin/")
    print("  3. Or use initialize_platform command with --username, --email, --password")
    
    # Check if any superuser exists
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        print_success(f"Found {superusers.count()} superuser(s) in database")
        for admin in superusers:
            print(f"  - {admin.username} ({admin.email})")
        return superusers.first()
    else:
        print("⚠️  No superuser found. Please create one using the methods above.")
        return None

def create_demo_user():
    """Step 2: Demo user creation - PRODUCTION VERSION
    
    NOTE: Hardcoded demo user creation has been removed for production security.
    Demo users should be created through the registration endpoint or Django admin.
    """
    print_step(2, "Demo User Setup")
    
    print_success("Demo user creation disabled for production security.")
    print("To create test/demo users:")
    print("  1. Use frontend registration at http://localhost:3000/register")
    print("  2. Use Django admin at http://localhost:8000/admin/")
    print("  3. Use API endpoint /users/auth/register/")
    
    # Check if demo users exist
    demo_users = User.objects.filter(username__in=['demo', 'test', 'demo_user'])
    if demo_users.exists():
        print_success(f"Found {demo_users.count()} demo/test user(s)")
        for user in demo_users:
            print(f"  - {user.username} ({user.email})")
        return demo_users.first()
    else:
        print("⚠️  No demo users found. Create test users through registration or admin.")
        return None

def create_sample_content(admin_user):
    """Step 3: Create sample learning content"""
    print_step(3, "Creating Sample Learning Content")
    
    from apps.content.models import LearningModule, ContentBlock, ContentResource
    from apps.learning.models import AdaptiveChallenge, Assessment, AssessmentQuestion
    
    # Create sample learning modules
    modules = [
        {
            'title': 'Introduction to Programming',
            'description': 'Learn the basics of programming and problem-solving',
            'module_type': 'tutorial',
            'difficulty_level': 'beginner',
            'estimated_time': 60,
            'learning_objectives': 'Understand variables, data types, and basic programming concepts',
            'content_order': 1
        },
        {
            'title': 'Variables and Data Types',
            'description': 'Master different data types and variable declarations',
            'module_type': 'tutorial',
            'difficulty_level': 'beginner',
            'estimated_time': 45,
            'learning_objectives': 'Work with integers, strings, booleans, and arrays',
            'content_order': 2
        },
        {
            'title': 'Control Structures',
            'description': 'Learn about conditionals and loops',
            'module_type': 'tutorial',
            'difficulty_level': 'intermediate',
            'estimated_time': 90,
            'learning_objectives': 'Implement if statements, for loops, and while loops',
            'content_order': 3
        }
    ]
    
    created_modules = []
    for module_data in modules:
        module_data['created_by'] = admin_user
        module = LearningModule.objects.create(**module_data)
        created_modules.append(module)
        print_success(f"Created learning module: {module.title}")
        
        # Create content blocks for each module
        content_blocks = [
            {
                'title': f'{module.title} - Introduction',
                'content_type': 'text',
                'content_data': {'content': f'Welcome to {module.title}! This module covers fundamental concepts.'},
                'order_index': 1,
                'module': module
            },
            {
                'title': f'{module.title} - Examples',
                'content_type': 'interactive',
                'content_data': {'examples': ['Example 1', 'Example 2'], 'interactive_elements': ['code_editor']},
                'order_index': 2,
                'module': module
            },
            {
                'title': f'{module.title} - Practice',
                'content_type': 'exercise',
                'content_data': {'exercises': ['Exercise 1', 'Exercise 2'], 'submission_type': 'code'},
                'order_index': 3,
                'module': module
            }
        ]
        
        for block_data in content_blocks:
            block = ContentBlock.objects.create(**block_data)
            print_success(f"  Created content block: {block.title}")
    
    # Create sample challenges
    challenges = [
        {
            'title': 'Hello World Challenge',
            'description': 'Write your first program that prints "Hello, World!"',
            'challenge_type': 'coding',
            'difficulty_level': 'beginner',
            'content': 'Create a program that prints "Hello, World!" to the console.',
            'estimated_time': 10,
            'created_by': admin_user
        },
        {
            'title': 'Number Calculator',
            'description': 'Build a simple calculator that can add, subtract, multiply, and divide',
            'challenge_type': 'coding',
            'difficulty_level': 'intermediate',
            'content': 'Implement basic arithmetic operations: addition, subtraction, multiplication, division.',
            'estimated_time': 30,
            'created_by': admin_user
        },
        {
            'title': 'Array Sum Challenge',
            'description': 'Calculate the sum of all elements in an array',
            'challenge_type': 'coding',
            'difficulty_level': 'beginner',
            'content': 'Given an array of numbers, return the sum of all elements.',
            'estimated_time': 15,
            'created_by': admin_user
        }
    ]
    
    for challenge_data in challenges:
        challenge = AdaptiveChallenge.objects.create(**challenge_data)
        print_success(f"Created challenge: {challenge.title}")
    
    # Create sample assessments
    assessment = Assessment.objects.create(
        title='Programming Fundamentals Quiz',
        description='Test your understanding of basic programming concepts',
        assessment_type='quiz',
        time_limit=30,
        max_attempts=3,
        passing_score=70.0,
        instructions='Answer all questions to the best of your ability',
        created_by=admin_user
    )
    print_success(f"Created assessment: {assessment.title}")
    
    # Create sample questions
    questions = [
        {
            'assessment': assessment,
            'question_text': 'What is a variable?',
            'question_type': 'multiple_choice',
            'points': 1.0,
            'order_index': 1,
            'explanation': 'A variable is a named storage location for data.'
        },
        {
            'assessment': assessment,
            'question_text': 'Which data type is used for true/false values?',
            'question_type': 'multiple_choice',
            'points': 1.0,
            'order_index': 2,
            'explanation': 'Boolean data type is used for true/false values.'
        },
        {
            'assessment': assessment,
            'question_text': 'What is the purpose of a loop?',
            'question_type': 'multiple_choice',
            'points': 1.0,
            'order_index': 3,
            'explanation': 'Loops allow you to repeat code multiple times.'
        }
    ]
    
    for question_data in questions:
        question = AssessmentQuestion.objects.create(**question_data)
        print_success(f"  Created question: {question.question_text[:50]}...")
    
    return created_modules

def create_gamification_data(admin_user):
    """Step 4: Create gamification content"""
    print_step(4, "Creating Gamification Content")
    
    from apps.gamification.models import Achievement, Badge, LevelRequirement
    
    # Create achievements
    achievements = [
        {
            'title': 'First Steps',
            'description': 'Complete your first challenge',
            'category': 'beginner',
            'difficulty': 'easy',
            'points_reward': 50,
            'unlock_order': 1,
            'requirements': {'challenges_completed': 1}
        },
        {
            'title': 'Code Warrior',
            'description': 'Solve 10 coding challenges',
            'category': 'coding',
            'difficulty': 'medium',
            'points_reward': 200,
            'unlock_order': 2,
            'requirements': {'challenges_completed': 10}
        },
        {
            'title': 'Speed Demon',
            'description': 'Complete a challenge in under 5 minutes',
            'category': 'speed',
            'difficulty': 'hard',
            'points_reward': 150,
            'unlock_order': 3,
            'requirements': {'fastest_challenge_time': 300}
        },
        {
            'title': 'Consistent Learner',
            'description': 'Maintain a 7-day learning streak',
            'category': 'consistency',
            'difficulty': 'medium',
            'points_reward': 100,
            'unlock_order': 4,
            'requirements': {'learning_streak': 7}
        },
        {
            'title': 'Perfect Score',
            'description': 'Achieve 100% on any assessment',
            'category': 'assessment',
            'difficulty': 'medium',
            'points_reward': 75,
            'unlock_order': 5,
            'requirements': {'assessment_score': 100}
        }
    ]
    
    created_achievements = []
    for achievement_data in achievements:
        achievement = Achievement.objects.create(**achievement_data)
        created_achievements.append(achievement)
        print_success(f"Created achievement: {achievement.title}")
    
    # Create badges
    badges = [
        {
            'title': 'Novice Programmer',
            'description': 'New to programming',
            'category': 'beginner',
            'difficulty': 'easy',
            'rarity': 'common',
            'requirements': {'profile_created': True}
        },
        {
            'title': 'Problem Solver',
            'description': 'Solved 5 challenges',
            'category': 'coding',
            'difficulty': 'medium',
            'rarity': 'uncommon',
            'requirements': {'challenges_solved': 5}
        },
        {
            'title': 'Expert Coder',
            'description': 'Solved 50+ challenges',
            'category': 'coding',
            'difficulty': 'hard',
            'rarity': 'legendary',
            'requirements': {'challenges_solved': 50}
        },
        {
            'title': 'Quick Learner',
            'description': 'Completed 10 challenges in one week',
            'category': 'speed',
            'difficulty': 'hard',
            'rarity': 'rare',
            'requirements': {'challenges_per_week': 10}
        },
        {
            'title': 'Mentor',
            'description': 'Helped 3 other students',
            'category': 'collaboration',
            'difficulty': 'medium',
            'rarity': 'uncommon',
            'requirements': {'students_helped': 3}
        }
    ]
    
    for badge_data in badges:
        badge = Badge.objects.create(**badge_data)
        print_success(f"Created badge: {badge.title}")
    
    # Create level requirements
    level_requirements = [
        {'level': 1, 'requirement_type': 'points', 'requirement_value': 0, 'description': 'Starting level'},
        {'level': 2, 'requirement_type': 'points', 'requirement_value': 100, 'description': 'Reach 100 total points'},
        {'level': 3, 'requirement_type': 'points', 'requirement_value': 250, 'description': 'Reach 250 total points'},
        {'level': 4, 'requirement_type': 'points', 'requirement_value': 500, 'description': 'Reach 500 total points'},
        {'level': 5, 'requirement_type': 'points', 'requirement_value': 1000, 'description': 'Reach 1000 total points'},
        {'level': 6, 'requirement_type': 'challenges_completed', 'requirement_value': 5, 'description': 'Complete 5 challenges'},
        {'level': 7, 'requirement_type': 'challenges_completed', 'requirement_value': 15, 'description': 'Complete 15 challenges'},
        {'level': 8, 'requirement_type': 'challenges_completed', 'requirement_value': 30, 'description': 'Complete 30 challenges'},
        {'level': 9, 'requirement_type': 'challenges_completed', 'requirement_value': 50, 'description': 'Complete 50 challenges'},
        {'level': 10, 'requirement_type': 'challenges_completed', 'requirement_value': 100, 'description': 'Complete 100 challenges'}
    ]
    
    for req_data in level_requirements:
        req = LevelRequirement.objects.create(**req_data)
        print_success(f"Created level requirement: Level {req.level} - {req.requirement_type}")
    
    return created_achievements

def create_collaboration_data(admin_user):
    """Step 5: Create collaboration content"""
    print_step(5, "Creating Collaboration Content")
    
    from apps.collaboration.models import StudyGroup, DiscussionTopic, StudyGroupMembership
    
    # Create study groups
    study_groups = [
        {
            'name': 'Beginner Programmers',
            'description': 'A friendly group for those just starting their programming journey',
            'group_type': 'learning',
            'max_members': 20,
            'created_by': admin_user
        },
        {
            'name': 'Advanced Algorithms',
            'description': 'For experienced programmers looking to master complex algorithms',
            'group_type': 'advanced',
            'max_members': 15,
            'created_by': admin_user
        },
        {
            'name': 'Project Collaboration',
            'description': 'Find teammates for programming projects and hackathons',
            'group_type': 'projects',
            'max_members': 10,
            'created_by': admin_user
        }
    ]
    
    created_groups = []
    for group_data in study_groups:
        group = StudyGroup.objects.create(**group_data)
        created_groups.append(group)
        print_success(f"Created study group: {group.name}")
        
        # Add admin as member
        membership = StudyGroupMembership.objects.create(
            group=group,
            user=admin_user,
            role='admin',
            status='active'
        )
        print_success(f"  Added admin as admin to {group.name}")
    
    # Create discussion topics
    topics = [
        {
            'title': 'Getting Started with Python',
            'description': 'Share resources and tips for learning Python programming',
            'forum': 'help',
            'category': 'Python',
            'created_by': admin_user
        },
        {
            'title': 'Algorithm Discussion: Binary Search',
            'description': 'Deep dive into binary search algorithm implementation',
            'forum': 'algorithms',
            'category': 'Algorithms',
            'created_by': admin_user
        },
        {
            'title': 'Best Practices for Code Reviews',
            'description': 'How to give and receive effective code feedback',
            'forum': 'best_practices',
            'category': 'Best Practices',
            'created_by': admin_user
        },
        {
            'title': 'Upcoming Hackathon Projects',
            'description': 'Find team members for upcoming hackathons',
            'forum': 'events',
            'category': 'Events',
            'created_by': admin_user
        }
    ]
    
    for topic_data in topics:
        topic = DiscussionTopic.objects.create(**topic_data)
        print_success(f"Created discussion topic: {topic.title}")
    
    return created_groups

def create_user_profiles(users):
    """Step 6: Create user profiles and gamification records"""
    print_step(6, "Creating User Profiles and Gamification")
    
    from apps.users.models import UserProfile, UserPreferences
    from apps.gamification.models import UserPoints, UserLevel, LearningStreak
    
    for user in users:
        # Create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'education_level': 'beginner',
                'interests': 'Programming, Algorithms, Web Development',
                'notification_preferences': {'email': True, 'push': False}
            }
        )
        print_success(f"Created profile for {user.username}" if created else f"Profile exists for {user.username}")
        
        # Create user preferences
        preferences, created = UserPreferences.objects.get_or_create(
            user=user,
            defaults={
                'theme_preference': 'light',
                'language_preference': 'en',
                'difficulty_preference': 'medium',
                'learning_style': 'visual'
            }
        )
        print_success(f"Created preferences for {user.username}" if created else f"Preferences exist for {user.username}")
        
        # Create gamification records
        points, created = UserPoints.objects.get_or_create(
            user=user,
            defaults={'total_points': 0, 'available_points': 0, 'lifetime_points': 0}
        )
        print_success(f"Created points record for {user.username}" if created else f"Points exist for {user.username}")
        
        level, created = UserLevel.objects.get_or_create(
            user=user,
            defaults={'current_level': 1, 'total_xp': 0, 'xp_to_next_level': 100}
        )
        print_success(f"Created level record for {user.username}" if created else f"Level exists for {user.username}")
        
        streak, created = LearningStreak.objects.get_or_create(
            user=user,
            defaults={'current_streak': 0, 'longest_streak': 0}
        )
        print_success(f"Created streak record for {user.username}" if created else f"Streak exists for {user.username}")
        
        # Create difficulty profile
        from apps.learning.models import UserDifficultyProfile
        difficulty, created = UserDifficultyProfile.objects.get_or_create(
            user=user,
            defaults={
                'current_difficulty': 'beginner',
                'coding_skill_level': 1,
                'problem_solving_level': 1,
                'jac_knowledge_level': 1,
                'learning_speed': 1
            }
        )
        print_success(f"Created difficulty profile for {user.username}" if created else f"Difficulty profile exists for {user.username}")

def main():
    """Main function to run all data loading steps - PRODUCTION VERSION"""
    print("🚀 JAC Interactive Learning Platform - Data Loader (Production Mode)")
    print("=" * 60)
    
    try:
        # Step 1: Check admin users (no creation)
        admin_user = create_admin_user()
        
        # Step 2: Check demo users (no creation)
        demo_user = create_demo_user()
        
        # Only proceed with content creation if we have at least one admin user
        if not admin_user:
            print_error("No admin user found. Cannot create content without admin user.")
            print("Please create an admin user first using:")
            print("  python manage.py createsuperuser")
            return False
            
        users = [admin_user] + ([demo_user] if demo_user else [])
        
        # Step 3: Create sample content
        modules = create_sample_content(admin_user)
        
        # Step 4: Create gamification content
        achievements = create_gamification_data(admin_user)
        
        # Step 5: Create collaboration data
        groups = create_collaboration_data(admin_user)
        
        # Step 6: Create user profiles
        create_user_profiles(users)
        
        # Final summary
        print_step("COMPLETE", "Data Loading Complete!")
        if admin_user:
            print_success(f"✅ Admin user available: {admin_user.username} (ID: {admin_user.id})")
        if demo_user:
            print_success(f"✅ Demo user available: {demo_user.username} (ID: {demo_user.id})")
        print_success(f"✅ Learning modules created: {len(modules)}")
        print_success(f"✅ Achievements created: {len(achievements)}")
        print_success(f"✅ Study groups created: {len(groups)}")
        print_success(f"✅ All user profiles and gamification records created")
        
        print("\n🎯 PRODUCTION LOGIN:")
        print("=" * 30)
        print("Django Admin:")
        print("  URL: http://localhost:8000/admin/")
        print("  Create users through admin interface or registration")
        print("\nFrontend Registration:")
        print("  URL: http://localhost:3000/register")
        print("  Create new accounts for testing")
        
        print("\n✅ All data loaded successfully!")
        return True
        
    except Exception as e:
        print_error(f"Error during data loading: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)