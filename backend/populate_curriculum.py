#!/usr/bin/env python
"""
Standalone script to populate the JAC curriculum without Django app registry issues.
"""

import os
import sys
import django

# Add the project root to the path
sys.path.insert(0, '/workspace/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_minimal')
django.setup()

# Now import Django models
from django.contrib.auth import get_user_model
from apps.learning.models import (
    LearningPath, Module, Lesson, Assessment, Question
)
import json

User = get_user_model()

def populate_jac_curriculum():
    """Populate the complete JAC curriculum with comprehensive content"""
    
    print("Starting JAC Curriculum Population...")
    
    # Create or get admin user for content creation
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@jaclang.org',
                password='admin123'
            )
            print('Created admin user')
    except Exception as e:
        print(f'Could not create admin user: {e}')
        return

    # Create the main JAC learning path
    print('Creating JAC Learning Path...')
    learning_path, created = LearningPath.objects.get_or_create(
        name="Complete JAC Programming Language Course",
        defaults={
            'description': 'Comprehensive course covering JAC programming from fundamentals to production applications. Learn both traditional programming and Object-Spatial Programming (OSP) paradigm.',
            'difficulty_level': 'beginner',
            'estimated_duration': 80,  # 80 hours total
            'prerequisites': [],
            'tags': ['programming', 'jac', 'osp', 'ai', 'graph-programming'],
            'is_published': True,
            'is_featured': True,
            'created_by': admin_user,
        }
    )
    
    if created:
        print(f'Created learning path: {learning_path.name}')
    else:
        print(f'Learning path already exists: {learning_path.name}')

    # Define the complete curriculum structure with comprehensive content
    modules_data = [
        {
            'order': 1,
            'title': 'JAC Fundamentals (Week 1-2)',
            'description': 'Master JAC syntax, variables, data types, functions, and control flow. Learn the foundational concepts of this Python superset language.',
            'content': '''# Module 1: JAC Fundamentals

Welcome to your JAC programming journey! In this foundational module, you'll learn the essential building blocks of JAC, a powerful programming language that extends Python with innovative features.

## What You'll Learn

- **JAC Syntax & Structure**: Master JAC's unique syntax and code organization
- **Variables & Data Types**: Understand strong typing and JAC's data types
- **Functions & Control Flow**: Learn to structure your code with functions and logic
- **Operators & Collections**: Work with data using JAC's operators and data structures
- **Object-Oriented Programming**: Create classes and objects the JAC way

## Why Learn JAC?

JAC is a **native superset of Python**, meaning you can leverage your existing Python knowledge while learning powerful new concepts. JAC introduces **Object-Spatial Programming (OSP)**, a revolutionary paradigm that changes how you think about data and computation.''',
            'duration_minutes': 960,  # 16 hours
            'difficulty_rating': 2,
            'jac_concepts': ['variables', 'types', 'functions', 'control_flow', 'operators', 'collections'],
            'code_examples': [
                {
                    'title': 'Hello World in JAC',
                    'code': '''withentry {
    print("Hello, JAC World!");
}''',
                    'description': 'Your first JAC program'
                },
                {
                    'title': 'Variable Declarations',
                    'code': '''# Variable declarations with explicit types
student_name: str = "Alice Johnson";
grade: int = 95;
gpa: float = 3.85;
is_honor_student: bool = true;

print(f"Student: {student_name}");
print(f"Grade: {grade}");
print(f"GPA: {gpa}");
print(f"Honor Student: {is_honor_student}");''',
                    'description': 'Strong typing in JAC'
                }
            ],
            'has_quiz': True,
            'has_coding_exercise': True,
            'lessons': [
                {
                    'order': 1,
                    'title': 'Introduction to JAC',
                    'type': 'text',
                    'content': '''# Welcome to JAC Programming!

## What is JAC?

JAC (Jaseci Application Language) is a modern programming language that extends Python with powerful new features, particularly **Object-Spatial Programming (OSP)**. Think of JAC as Python with superpowers!

## Key Features

- **Native Superset of Python**: All your Python knowledge applies
- **Strong Typing**: Variables must have explicit types (better error catching)
- **Object-Spatial Programming**: Revolutionary paradigm for graph-based applications
- **AI Integration**: Built-in support for AI operations
- **Modern Syntax**: Clean, readable code with semicolons and curly braces

## Your First JAC Program

Here's your "Hello World" in JAC:

```jac
withentry {
    print("Hello, JAC World!");
}
```

**Key differences from Python:**
- Uses `withentry` instead of `if __name__ == "__main__"`
- Statements end with semicolons (`;`)
- Code blocks use curly braces (`{}`) instead of indentation
- Comments start with `#` (same as Python)

Let's dive in!''',
                    'duration': 30
                },
                {
                    'order': 2,
                    'title': 'Variables and Data Types',
                    'type': 'text',
                    'content': '''# Variables and Data Types

JAC uses **strong typing**, meaning every variable must have an explicit type. This catches errors early and makes code more maintainable.

## Variable Declaration

```jac
# Basic syntax: variable_name: type = value;
name: str = "Alice";
age: int = 25;
height: float = 5.6;
is_student: bool = true;
```

## Primitive Data Types

### String (str)
```jac
student_name: str = "Alice Johnson";
message: str = 'Hello, world!';
```

### Integer (int)
```jac
student_id: int = 12345;
score: int = -42;
```

### Float (float)
```jac
gpa: float = 3.85;
temperature: float = 98.6;
```

### Boolean (bool)
```jac
is_enrolled: bool = true;
has_passed: bool = false;
```

Ready to learn about functions and control flow? Let's continue!''',
                    'duration': 60
                }
            ],
            'assessments': [
                {
                    'title': 'JAC Fundamentals Quiz',
                    'description': 'Test your understanding of JAC syntax, variables, and basic programming concepts.',
                    'type': 'quiz',
                    'difficulty': 'beginner',
                    'time_limit': 30,
                    'max_attempts': 3,
                    'passing_score': 70.0,
                    'questions': [
                        {
                            'text': 'What is the correct way to declare a variable in JAC?',
                            'type': 'multiple_choice',
                            'difficulty': 'beginner',
                            'points': 1.0,
                            'options': [
                                'variable_name = value;',
                                'var variable_name: type = value;',
                                'variable_name: type = value;',
                                'type variable_name = value;'
                            ],
                            'correct_answer': {'index': 2},
                            'explanation': 'JAC uses explicit type declarations: variable_name: type = value;'
                        },
                        {
                            'text': 'What does the `withentry` keyword do in JAC?',
                            'type': 'multiple_choice',
                            'difficulty': 'beginner',
                            'points': 1.0,
                            'options': [
                                'Defines a function',
                                'Marks the program entry point',
                                'Creates a class',
                                'Declares a variable'
                            ],
                            'correct_answer': {'index': 1},
                            'explanation': 'withentry marks the starting point of a JAC program.'
                        }
                    ]
                }
            ],
        },
        {
            'order': 2,
            'title': 'Object-Spatial Programming (Week 3-4)',
            'description': 'Learn JAC\'s revolutionary Object-Spatial Programming paradigm. Master nodes, edges, and walkers for graph-based applications.',
            'content': '''# Module 2: Object-Spatial Programming (OSP)

Welcome to the revolutionary world of **Object-Spatial Programming (OSP)**! This module will transform how you think about data and computation.

## What You'll Learn

- **Object-Spatial Programming Paradigm**: Understand OSP's fundamental shift from traditional programming
- **Nodes and Edges**: Master JAC's graph-based data structures
- **Walkers**: Learn mobile computation units that traverse graphs
- **Abilities**: Discover automatic methods that trigger during interactions
- **Graph Navigation**: Explore powerful graph traversal and querying

## What is Object-Spatial Programming?

Traditional programming follows the paradigm: **"Bring data to computation"** (OOP). 
OSP flips this: **"Send computation to data"** (Spatial).

## The OSP Trinity

- **Nodes**: Data locations (like houses in a neighborhood)
- **Edges**: Relationships between nodes (like roads between houses)  
- **Walkers**: Mobile computation (like people walking between houses)

Let's explore this paradigm-shifting approach to programming!''',
            'duration_minutes': 960,
            'difficulty_rating': 3,
            'jac_concepts': ['nodes', 'edges', 'walkers', 'osp', 'graph_traversal', 'abilities'],
            'code_examples': [
                {
                    'title': 'Basic Node and Edge Definition',
                    'code': '''# Define node types
node Student {
    has name: str;
    has age: int;
    has major: str;
    has gpa: float;
}

node Course {
    has title: str;
    has code: str;
    has credits: int;
}

# Define edge types
edge EnrolledIn {
    has semester: str;
    has grade: str;
}

# Create the graph
withentry {
    # Create nodes
    alice: Student = Student(name="Alice Johnson", age=20, major="CS", gpa=3.8);
    cs101: Course = Course(title="Intro to Programming", code="CS101", credits=3);
    
    # Create connections
    alice +>:EnrolledIn(semester="Fall 2024", grade="A"):+> cs101;
    
    print("Graph created successfully!");
}''',
                    'description': 'Basic nodes, edges, and connections'
                }
            ],
            'has_quiz': True,
            'has_coding_exercise': True,
            'lessons': [
                {
                    'order': 1,
                    'title': 'Introduction to Object-Spatial Programming',
                    'type': 'text',
                    'content': '''# Introduction to Object-Spatial Programming

Welcome to the paradigm that will change how you think about programming! Object-Spatial Programming (OSP) is JAC's revolutionary approach to organizing and processing data.

## The Traditional Programming Problem

In traditional programming, we follow this pattern:
```
1. Gather all data into memory
2. Apply computation to the data  
3. Return results
```

## The OSP Revolution

OSP flips the script: **"Send computation to the data!"**

## The OSP Trinity

### 1. Nodes (Data Locations)
Think of nodes as **houses in a neighborhood**. They hold data and can interact with visitors.

### 2. Edges (Relationships)  
Edges are **first-class relationships** between nodes.

### 3. Walkers (Mobile Computation)
Walkers are **people walking between houses**. They move through the graph, triggering interactions.

Ready to dive into nodes and edges? Let's start building!''',
                    'duration': 45
                }
            ],
            'assessments': [
                {
                    'title': 'OSP Fundamentals Assessment',
                    'description': 'Test your understanding of Object-Spatial Programming concepts, nodes, and basic graph structures.',
                    'type': 'quiz',
                    'difficulty': 'beginner',
                    'time_limit': 40,
                    'max_attempts': 3,
                    'passing_score': 75.0,
                    'questions': [
                        {
                            'text': 'What are the three fundamental components of Object-Spatial Programming?',
                            'type': 'multiple_choice',
                            'difficulty': 'beginner',
                            'points': 2.0,
                            'options': [
                                'Objects, Methods, Properties',
                                'Nodes, Edges, Walkers',
                                'Classes, Functions, Variables',
                                'Data, Logic, Control Flow'
                            ],
                            'correct_answer': {'index': 1},
                            'explanation': 'OSP is built on Nodes (data locations), Edges (relationships), and Walkers (mobile computation).'
                        }
                    ]
                }
            ],
        },
        {
            'order': 3,
            'title': 'Advanced JAC Concepts (Week 5-6)',
            'description': 'Explore advanced OOP, class hierarchies, advanced OSP operations, and walker-based API development.',
            'content': '''# Module 3: Advanced JAC Concepts

Take your JAC skills to the next level! This module covers advanced Object-Spatial Programming, enhanced OOP, and building production-ready applications.

## What You'll Learn

- **Enhanced OOP**: Advanced class hierarchies, multiple inheritance, and design patterns
- **Advanced OSP**: Complex graph operations, filtering, and optimization
- **Walker APIs**: Create RESTful APIs using walkers as endpoints
- **Persistence**: Master JAC's automatic persistence and data management
- **Error Handling**: Robust error management and debugging techniques

Ready to become a JAC expert? Let's dive deep!''',
            'duration_minutes': 1200,
            'difficulty_rating': 4,
            'jac_concepts': ['advanced_oop', 'class_hierarchies', 'advanced_osp', 'api_development', 'persistence'],
            'code_examples': [
                {
                    'title': 'Enhanced OOP with Multiple Inheritance',
                    'code': '''# Advanced class hierarchies and multiple inheritance
node Person {
    has name: str;
    has age: int;
    has email: str;
}

node Loggable {
    has created_at: str;
    has updated_at: str = "";
    
    can log_activity(activity: str) -> void {
        print(f"[{self.created_at}] {self.name}: {activity}");
    }
}

# Multiple inheritance
node Student(Person, Loggable) {
    has student_id: str;
    has major: str;
    has gpa: float;
    has courses: list[str] = [];
    
    can add_course(course: str) -> void {
        self.courses.append(course);
        self.log_activity(f"Added course: {course}");
    }
}

withentry {
    alice: Student = Student(
        name="Alice Johnson",
        age=20,
        email="alice@email.com",
        student_id="S12345",
        major="Computer Science",
        gpa=3.85
    );
    alice.created_at = "2024-11-24 15:30:00";
    
    alice.add_course("Data Structures");
    print("Student Info:", alice.courses);
}''',
                    'description': 'Multiple inheritance and advanced OOP patterns'
                }
            ],
            'has_quiz': True,
            'has_coding_exercise': True,
            'lessons': [
                {
                    'order': 1,
                    'title': 'Enhanced Object-Oriented Programming',
                    'type': 'text',
                    'content': '''# Enhanced Object-Oriented Programming in JAC

JAC extends traditional OOP with powerful features like multiple inheritance, interfaces, and design patterns.

## Multiple Inheritance

JAC supports multiple inheritance, allowing nodes to inherit from multiple parent types:

```jac
node Person {
    has name: str;
    has age: int;
}

node Loggable {
    has created_at: str;
    can log_activity(activity: str) {
        print(f"[{self.created_at}] {self.name}: {activity}");
    }
}

// Multiple inheritance
node Student(Person, Loggable) {
    has student_id: str;
    has gpa: float;
}
```

Ready to learn about advanced OSP operations? Let's continue!''',
                    'duration': 60
                }
            ],
            'assessments': [
                {
                    'title': 'Advanced JAC Concepts Quiz',
                    'description': 'Test your understanding of advanced OOP patterns and design patterns in JAC.',
                    'type': 'quiz',
                    'difficulty': 'intermediate',
                    'time_limit': 45,
                    'max_attempts': 3,
                    'passing_score': 75.0,
                    'questions': [
                        {
                            'text': 'How does JAC handle multiple inheritance?',
                            'type': 'multiple_choice',
                            'difficulty': 'intermediate',
                            'points': 2.0,
                            'options': [
                                'JAC does not support multiple inheritance',
                                'JAC supports multiple inheritance using comma separation',
                                'JAC only allows single inheritance',
                                'JAC uses interfaces instead of inheritance'
                            ],
                            'correct_answer': {'index': 1},
                            'explanation': 'JAC supports multiple inheritance by listing parent classes separated by commas.'
                        }
                    ]
                }
            ],
        },
        {
            'order': 4,
            'title': 'AI Integration (Week 7-8)',
            'description': 'Integrate AI capabilities using JAC\'s byLLM framework. Learn decorators, async programming, and advanced AI operations.',
            'content': '''# Module 4: AI Integration with JAC

Harness the power of artificial intelligence in your JAC applications! This module covers JAC's advanced AI capabilities.

## What You'll Learn

- **byLLM Framework**: JAC's revolutionary AI integration system
- **AI Functions**: Create AI-powered functions with zero prompt engineering
- **Decorators**: Enhance functions with timing, caching, and error handling
- **Async Programming**: Handle concurrent AI operations efficiently
- **Multimodal AI**: Work with text, images, and audio

## The AI-First Paradigm

JAC is designed for the AI era with type-safe AI integration and automatic prompt optimization.

Ready to build AI-powered applications? Let's dive in!''',
            'duration_minutes': 1200,
            'difficulty_rating': 4,
            'jac_concepts': ['ai_functions', 'decorators', 'async_programming', 'byllm', 'multimodal_ai'],
            'code_examples': [
                {
                    'title': 'Basic byLLM Integration',
                    'code': '''# Basic byLLM integration with JAC
import from byllm.lib { Model };

# Configure AI model
glob text_model = Model(model_name="gpt-4o-mini");

# Simple AI function with byLLM
def generate_student_feedback(student_name: str, grade: int) -> str byllm() {
    """
    Generate personalized feedback for a student based on their grade.
    The AI will handle the prompt engineering automatically.
    """
}

def explain_concept(concept: str) -> str byllm() {
    """
    Explain a programming concept in simple terms.
    """
}

withentry {
    print("=== JAC AI Integration Demo ===");
    
    # Generate personalized feedback
    feedback: str = generate_student_feedback("Alice Johnson", 92);
    print(f"\\nStudent Feedback: {feedback}");
    
    # Explain a concept
    explanation: str = explain_concept("Object-Spatial Programming");
    print(f"\\nConcept Explanation: {explanation}");
    
    print("\\n=== AI Integration Complete ===");
}''',
                    'description': 'Basic byLLM integration and AI function creation'
                }
            ],
            'has_quiz': True,
            'has_coding_exercise': True,
            'lessons': [
                {
                    'order': 1,
                    'title': 'Introduction to byLLM Framework',
                    'type': 'text',
                    'content': '''# Introduction to byLLM Framework

Welcome to JAC's revolutionary AI integration system! The byLLM framework transforms how you integrate AI into applications.

## What is byLLM?

byLLM is JAC's zero-prompt-engineering AI framework that lets you:
- Define AI functions using normal JAC syntax
- Let AI handle prompt engineering automatically
- Get type-safe AI responses
- Switch between AI models easily

## The Traditional AI Problem

Traditional AI integration requires manual prompt engineering, but byLLM turns this into simple function definitions.

## The byLLM Solution

```jac
def generate_feedback(name: str, grade: int) -> str byllm() {
    // AI handles all prompt engineering automatically!
}
```

Ready to build AI-powered applications? Let's dive in!''',
                    'duration': 75
                }
            ],
            'assessments': [
                {
                    'title': 'AI Integration Assessment',
                    'description': 'Test your understanding of byLLM framework and AI function creation.',
                    'type': 'quiz',
                    'difficulty': 'intermediate',
                    'time_limit': 50,
                    'max_attempts': 3,
                    'passing_score': 80.0,
                    'questions': [
                        {
                            'text': 'What does byLLM stand for?',
                            'type': 'multiple_choice',
                            'difficulty': 'beginner',
                            'points': 2.0,
                            'options': [
                                'Build Your Language Model',
                                'Beautiful Language Model',
                                'Meaning-Typed LLM',
                                'Basic Language Model'
                            ],
                            'correct_answer': {'index': 2},
                            'explanation': 'byLLM stands for "Meaning-Typed LLM" and provides zero prompt engineering with type safety.'
                        }
                    ]
                }
            ],
        },
        {
            'order': 5,
            'title': 'Production Applications (Week 9-10)',
            'description': 'Build production-ready applications with multi-user architecture, deployment strategies, and performance optimization.',
            'content': '''# Module 5: Production Applications

Build robust, scalable, production-ready applications with JAC! This final module covers deployment, security, and performance optimization.

## What You'll Learn

- **Multi-User Architecture**: Design systems for multiple users with proper permissions
- **Deployment Strategies**: Deploy JAC applications to various environments
- **Performance Optimization**: Scale your applications for production workloads
- **Security Best Practices**: Implement robust security measures
- **Monitoring and Logging**: Track application health and performance

## Production-Ready Patterns

This module covers enterprise-grade patterns for building scalable systems.

Ready to build production-ready applications? Let's make it happen!''',
            'duration_minutes': 1280,
            'difficulty_rating': 5,
            'jac_concepts': ['deployment', 'multi_user', 'performance', 'security', 'cloud_features'],
            'code_examples': [
                {
                    'title': 'Multi-User Architecture with Permissions',
                    'code': '''# Multi-user architecture with role-based permissions
node User {
    has username: str;
    has email: str;
    has role: str = "student";
    has is_active: bool = true;
    has created_at: str;
    has last_login: str = "";
    
    can has_permission(permission: str) -> bool {
        role_permissions: dict[str, list[str]] = {
            "admin": ["*"],  # All permissions
            "instructor": ["read_courses", "write_courses", "grade_assignments", "read_students"],
            "student": ["read_courses", "submit_assignments", "read_own_grades"],
            "guest": ["read_public_content"]
        };
        
        user_permissions: list[str] = role_permissions.get(self.role, []);
        return ("*" in user_permissions) or (permission in user_permissions);
    }
}

withentry {
    print("=== Multi-User Architecture Demo ===");
    
    # Create users with different roles
    admin: User = User(
        username="admin",
        email="admin@school.edu",
        role="admin",
        created_at="2024-11-01T00:00:00"
    );
    
    instructor: User = User(
        username="dr_smith",
        email="smith@school.edu", 
        role="instructor",
        created_at="2024-11-01T00:00:00"
    );
    
    student: User = User(
        username="alice_j",
        email="alice@student.edu",
        role="student", 
        created_at="2024-11-01T00:00:00"
    );
    
    print("\\n1. Permission Testing:");
    
    # Test permissions
    print(f"Admin can grade assignments: {admin.has_permission("grade_assignments")}");
    print(f"Instructor can grade assignments: {instructor.has_permission("grade_assignments")}");
    print(f"Student can grade assignments: {student.has_permission("grade_assignments")}");
    
    print("\\n2. Student-specific permissions:");
    print(f"Student can submit assignments: {student.has_permission("submit_assignments")}");
    print(f"Student can read courses: {student.has_permission("read_courses")}");
    
    print("\\n=== Multi-User Architecture Demo Complete ===");
}''',
                    'description': 'Multi-user architecture with role-based permissions and audit trails'
                }
            ],
            'has_quiz': True,
            'has_coding_exercise': True,
            'lessons': [
                {
                    'order': 1,
                    'title': 'Multi-User Architecture and Security',
                    'type': 'text',
                    'content': '''# Multi-User Architecture and Security

Building production-ready applications requires careful consideration of user management, security, and access control.

## User Management Architecture

### Role-Based Access Control (RBAC)

```jac
node User {
    has username: str;
    has role: str;
    
    can has_permission(permission: str) -> bool {
        role_permissions: dict[str, list[str]] = {
            "admin": ["*"],
            "student": ["read_courses", "submit_work"]
        };
        
        user_permissions: list[str] = role_permissions.get(self.role, []);
        return ("*" in user_permissions) or (permission in user_permissions);
    }
}
```

## Security Best Practices

1. **Authentication**: Use proper password hashing
2. **Authorization**: Implement role-based access control
3. **Input Validation**: Sanitize all user inputs
4. **Session Management**: Secure session handling
5. **Audit Logging**: Track user activities

Ready to learn about deployment strategies? Let's continue!''',
                    'duration': 90
                }
            ],
            'assessments': [
                {
                    'title': 'Production Applications Final Assessment',
                    'description': 'Comprehensive assessment covering multi-user architecture and security concepts.',
                    'type': 'exam',
                    'difficulty': 'advanced',
                    'time_limit': 90,
                    'max_attempts': 2,
                    'passing_score': 85.0,
                    'questions': [
                        {
                            'text': 'What are the key components of a secure multi-user architecture in JAC?',
                            'type': 'essay',
                            'difficulty': 'advanced',
                            'points': 10.0,
                            'correct_answer': {'response': '''A secure multi-user architecture in JAC should include:

1. **User Management**: User nodes with proper authentication, roles, and profiles
2. **Role-Based Access Control (RBAC)**: Role nodes with permissions and user-role assignments
3. **Authentication Service**: Credential validation, session management, and token generation
4. **Authorization Service**: Permission checking, resource-level access control
5. **Input Validation**: Schema validation, sanitization, and type checking
6. **Session Management**: Secure session creation, validation, and cleanup
7. **Audit Logging**: Comprehensive activity logging for compliance and security
8. **Rate Limiting**: Protection against abuse and DDoS attacks
9. **Data Protection**: Encryption, anonymization, and secure data handling
10. **Security Headers**: CORS, CSP, and other security headers for web applications

These components work together to provide a robust, scalable, and secure foundation for multi-user applications.'''},
                            'explanation': 'This tests understanding of complete security architecture for production applications.'
                        }
                    ]
                }
            ],
        }
    ]

    # Create modules and content
    for module_data in modules_data:
        print(f'Creating {module_data["title"]}...')
        
        module, created = Module.objects.get_or_create(
            learning_path=learning_path,
            order=module_data['order'],
            defaults={
                'title': module_data['title'],
                'description': module_data['description'],
                'content': module_data['content'],
                'content_type': 'markdown',
                'duration_minutes': module_data['duration_minutes'],
                'difficulty_rating': module_data['difficulty_rating'],
                'jac_concepts': module_data['jac_concepts'],
                'code_examples': module_data['code_examples'],
                'has_quiz': module_data['has_quiz'],
                'has_coding_exercise': module_data['has_coding_exercise'],
                'is_published': True,
            }
        )
        
        if created:
            print(f'Created module: {module.title}')
        else:
            print(f'Module already exists: {module.title}')

        # Create lessons for this module
        for lesson_data in module_data['lessons']:
            lesson, created = Lesson.objects.get_or_create(
                module=module,
                order=lesson_data['order'],
                defaults={
                    'title': lesson_data['title'],
                    'lesson_type': lesson_data['type'],
                    'content': lesson_data['content'],
                    'code_example': lesson_data.get('code_example', ''),
                    'quiz_questions': lesson_data.get('quiz_questions', []),
                    'estimated_duration': lesson_data['duration'],
                    'is_published': True,
                }
            )
            
            if created:
                print(f'  Created lesson: {lesson.title}')

        # Create assessments for this module
        for assessment_data in module_data['assessments']:
            assessment, created = Assessment.objects.get_or_create(
                module=module,
                title=assessment_data['title'],
                defaults={
                    'description': assessment_data['description'],
                    'assessment_type': assessment_data['type'],
                    'difficulty_level': assessment_data['difficulty'],
                    'time_limit': assessment_data.get('time_limit'),
                    'max_attempts': assessment_data.get('max_attempts', 3),
                    'passing_score': assessment_data.get('passing_score', 70.0),
                    'is_published': True,
                }
            )
            
            if created:
                print(f'  Created assessment: {assessment.title}')
                
                # Create questions for this assessment
                for i, question_data in enumerate(assessment_data['questions']):
                    question, q_created = Question.objects.get_or_create(
                        assessment=assessment,
                        question_text=question_data['text'],
                        defaults={
                            'question_type': question_data['type'],
                            'difficulty_level': question_data['difficulty'],
                            'points': question_data['points'],
                            'question_options': question_data.get('options', []),
                            'correct_answer': question_data.get('correct_answer', {}),
                            'code_template': question_data.get('code_template', ''),
                            'explanation': question_data.get('explanation', ''),
                            'hints': question_data.get('hints', []),
                        }
                    )
                    
                    if q_created:
                        print(f'    Created question {i+1}')

    print('✅ JAC Learning Curriculum population completed!')
    print(f'📚 Created {LearningPath.objects.count()} learning path(s)')
    print(f'📖 Created {Module.objects.filter(learning_path=learning_path).count()} module(s)')
    print(f'📝 Created {Lesson.objects.filter(module__learning_path=learning_path).count()} lesson(s)')
    print(f'🎯 Created {Assessment.objects.filter(module__learning_path=learning_path).count()} assessment(s)')
    print(f'❓ Created {Question.objects.filter(assessment__module__learning_path=learning_path).count()} question(s)')

if __name__ == '__main__':
    populate_jac_curriculum()
