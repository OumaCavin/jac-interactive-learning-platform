"""
Django management command to populate the complete JAC learning curriculum
with comprehensive content based on official JAC documentation.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.learning.models import (
    LearningPath, Module, Lesson, Assessment, AssessmentQuestion
)
import uuid
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the complete 5-module JAC learning curriculum with comprehensive content'

    def handle(self, *args, **options):
        """Populate the complete JAC curriculum with real content from official docs"""
        
        # Create or get admin user for content creation
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@jaclang.org',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Created admin user'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not create admin user: {e}'))
            return

        # Create the main JAC learning path
        self.stdout.write('Creating JAC Learning Path...')
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
            self.stdout.write(self.style.SUCCESS(f'Created learning path: {learning_path.name}'))
        else:
            self.stdout.write(f'Learning path already exists: {learning_path.name}')

        # Define the complete curriculum structure
        modules_data = [
            {
                'order': 1,
                'title': 'JAC Fundamentals (Week 1-2)',
                'description': 'Master JAC syntax, variables, data types, functions, and control flow. Learn the foundational concepts of this Python superset language.',
                'content': self.get_module1_content(),
                'duration_minutes': 960,  # 16 hours
                'difficulty_rating': 2,
                'jac_concepts': ['variables', 'types', 'functions', 'control_flow', 'operators', 'collections'],
                'code_examples': self.get_module1_code_examples(),
                'has_quiz': True,
                'has_coding_exercise': True,
                'lessons': self.get_module1_lessons(),
                'assessments': self.get_module1_assessments(),
            },
            {
                'order': 2,
                'title': 'Object-Spatial Programming (Week 3-4)',
                'description': 'Learn JAC\'s revolutionary Object-Spatial Programming paradigm. Master nodes, edges, and walkers for graph-based applications.',
                'content': self.get_module2_content(),
                'duration_minutes': 960,  # 16 hours
                'difficulty_rating': 3,
                'jac_concepts': ['nodes', 'edges', 'walkers', 'osp', 'graph_traversal', 'abilities'],
                'code_examples': self.get_module2_code_examples(),
                'has_quiz': True,
                'has_coding_exercise': True,
                'lessons': self.get_module2_lessons(),
                'assessments': self.get_module2_assessments(),
            },
            {
                'order': 3,
                'title': 'Advanced JAC Concepts (Week 5-6)',
                'description': 'Explore advanced OOP, class hierarchies, advanced OSP operations, and walker-based API development.',
                'content': self.get_module3_content(),
                'duration_minutes': 1200,  # 20 hours
                'difficulty_rating': 4,
                'jac_concepts': ['advanced_oop', 'class_hierarchies', 'advanced_osp', 'api_development', 'persistence'],
                'code_examples': self.get_module3_code_examples(),
                'has_quiz': True,
                'has_coding_exercise': True,
                'lessons': self.get_module3_lessons(),
                'assessments': self.get_module3_assessments(),
            },
            {
                'order': 4,
                'title': 'AI Integration (Week 7-8)',
                'description': 'Integrate AI capabilities using JAC\'s byLLM framework. Learn decorators, async programming, and advanced AI operations.',
                'content': self.get_module4_content(),
                'duration_minutes': 1200,  # 20 hours
                'difficulty_rating': 4,
                'jac_concepts': ['ai_functions', 'decorators', 'async_programming', 'byllm', 'multimodal_ai'],
                'code_examples': self.get_module4_code_examples(),
                'has_quiz': True,
                'has_coding_exercise': True,
                'lessons': self.get_module4_lessons(),
                'assessments': self.get_module4_assessments(),
            },
            {
                'order': 5,
                'title': 'Production Applications (Week 9-10)',
                'description': 'Build production-ready applications with multi-user architecture, deployment strategies, and performance optimization.',
                'content': self.get_module5_content(),
                'duration_minutes': 1280,  # 21+ hours
                'difficulty_rating': 5,
                'jac_concepts': ['deployment', 'multi_user', 'performance', 'security', 'cloud_features'],
                'code_examples': self.get_module5_code_examples(),
                'has_quiz': True,
                'has_coding_exercise': True,
                'lessons': self.get_module5_lessons(),
                'assessments': self.get_module5_assessments(),
            }
        ]

        # Create modules and content
        for module_data in modules_data:
            self.stdout.write(f'Creating {module_data["title"]}...')
            
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
                self.stdout.write(self.style.SUCCESS(f'Created module: {module.title}'))
            else:
                self.stdout.write(f'Module already exists: {module.title}')

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
                    self.stdout.write(self.style.SUCCESS(f'  Created lesson: {lesson.title}'))

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
                    self.stdout.write(self.style.SUCCESS(f'  Created assessment: {assessment.title}'))
                    
                    # Create questions for this assessment
                    for i, question_data in enumerate(assessment_data['questions']):
                        question, q_created = AssessmentQuestion.objects.get_or_create(
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
                            self.stdout.write(f'    Created question {i+1}')

        self.stdout.write(self.style.SUCCESS('✅ JAC Learning Curriculum population completed!'))
        self.stdout.write(f'📚 Created {LearningPath.objects.count()} learning path(s)')
        self.stdout.write(f'📖 Created {Module.objects.filter(learning_path=learning_path).count()} module(s)')
        self.stdout.write(f'📝 Created {Lesson.objects.filter(module__learning_path=learning_path).count()} lesson(s)')
        self.stdout.write(f'🎯 Created {Assessment.objects.filter(module__learning_path=learning_path).count()} assessment(s)')
        self.stdout.write(f'❓ Created {AssessmentQuestion.objects.filter(assessment__module__learning_path=learning_path).count()} question(s)')

    # Module 1: JAC Fundamentals Content
    def get_module1_content(self):
        return '''# Module 1: JAC Fundamentals

Welcome to your JAC programming journey! In this foundational module, you'll learn the essential building blocks of JAC, a powerful programming language that extends Python with innovative features.

## What You'll Learn

- **JAC Syntax & Structure**: Master JAC's unique syntax and code organization
- **Variables & Data Types**: Understand strong typing and JAC's data types
- **Functions & Control Flow**: Learn to structure your code with functions and logic
- **Operators & Collections**: Work with data using JAC's operators and data structures
- **Object-Oriented Programming**: Create classes and objects the JAC way

## Why Learn JAC?

JAC is a **native superset of Python**, meaning you can leverage your existing Python knowledge while learning powerful new concepts. JAC introduces **Object-Spatial Programming (OSP)**, a revolutionary paradigm that changes how you think about data and computation.

## Getting Started

JAC uses `withentry` as the program entry point, semicolons to end statements, and curly braces for code blocks. This module will guide you through each concept with practical examples.

## Learning Approach

We'll start with familiar concepts (variables, functions) and gradually introduce JAC-specific features. Each lesson includes:
- **Clear explanations** of new concepts
- **Practical code examples** you can run immediately  
- **Hands-on exercises** to reinforce learning
- **Real-world applications** to show practical use

Let's begin your JAC programming adventure!'''

    def get_module1_code_examples(self):
        return [
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
            },
            {
                'title': 'Functions with Types',
                'code': '''def calculate_grade(score: int) -> str {
    if (score >= 90) {
        return "A";
    } elif (score >= 80) {
        return "B";
    } elif (score >= 70) {
        return "C";
    } elif (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}

withentry {
    test_score: int = 87;
    letter_grade: str = calculate_grade(test_score);
    print(f"Score: {test_score} = Grade: {letter_grade}");
}''',
                'description': 'Functions with type annotations'
            },
            {
                'title': 'Working with Collections',
                'code': '''# Lists in JAC
student_scores: list[int] = [85, 92, 78, 95, 88];
student_names: list[str] = ["Alice", "Bob", "Charlie", "Diana", "Eve"];

# Dictionary for student data
student_data: dict[str, any] = {
    "name": "Alice Johnson",
    "age": 20,
    "major": "Computer Science",
    "gpa": 3.85
};

withentry {
    # Accessing list elements
    print(f"First student: {student_names[0]}");
    print(f"First score: {student_scores[0]}");
    
    # Accessing dictionary values
    print(f"Student name: {student_data["name"]}");
    print(f"Major: {student_data["major"]}");
    
    # List operations
    student_scores.append(90);
    print(f"Updated scores: {student_scores}");
}''',
                'description': 'Working with JAC collections'
            }
        ]

    def get_module1_lessons(self):
        return [
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

## Why JAC?

1. **Learn Once, Apply Everywhere**: Leverage existing Python knowledge
2. **Future-Proof**: Built for AI and modern application development  
3. **Type Safety**: Catch errors early with strong typing
4. **Spatial Thinking**: Model complex relationships naturally
5. **Production Ready**: Used in real-world AI applications

## Getting Ready

In this module, you'll learn:
- JAC syntax and structure
- Variables and data types
- Functions and control flow
- Collections and operators
- Basic object-oriented programming

Let's dive in!''',
                'duration': 30
            },
            {
                'order': 2,
                'title': 'JAC Syntax and Structure',
                'type': 'text',
                'content': '''# JAC Syntax and Structure

JAC maintains Python's readability while adding some important structural differences.

## Program Structure

Every JAC program starts with `withentry` and uses semicolons to end statements:

```jac
withentry {
    print("JAC program starts here");
    
    # Variable declaration
    message: str = "Hello World";
    
    # Function call
    print(message);
    
    # Semicolons are required!
}
```

## Code Blocks

JAC uses curly braces for code blocks instead of Python's indentation:

```jac
if (score > 90) {
    print("Excellent!");
    grade = "A";
} else {
    print("Good effort!");
    grade = "B";
}
```

## Comments

```jac
# Single-line comment
# This explains what the code does

#* 
Multi-line comment
Spans multiple lines
*#

/* Another multi-line comment style */
```

## Statements and Expressions

**Statements** (end with semicolon):
```jac
name: str = "Alice";
print(name);
result: int = 10 + 5;
```

**Expressions** (evaluate to values):
```jac
5 + 3              # Evaluates to 8
"Hello" + " World" # Evaluates to "Hello World"
x > 5              # Evaluates to true or false
```

## Naming Conventions

- **Variables**: `student_name`, `grade_point_average`
- **Functions**: `calculate_grade`, `find_maximum`
- **Constants**: `MAX_SCORE`, `DEFAULT_VALUE`

## Indentation

While JAC doesn't require Python's strict indentation, **consistent indentation makes code readable**:

```jac
def process_student(student_data: dict[str, any]) -> void {
    if (student_data["score"] > 90) {
        print("Honor roll student!");
        student_data["status"] = "honor";
    } else {
        print("Keep studying!");
        student_data["status"] = "regular";
    }
}
```

## Best Practices

1. **Use descriptive names**: `student_grade` not `sg`
2. **Comment complex logic**: Explain the "why", not the "what"
3. **Keep functions small**: One function, one responsibility
4. **Use consistent style**: Pick a style and stick to it
5. **Type everything**: JAC's strength is strong typing

Ready to work with variables? Let's continue!''',
                'duration': 45
            },
            {
                'order': 3,
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
multiline: str = "This is a
multi-line string";
```

### Integer (int)
```jac
student_id: int = 12345;
score: int = -42;
count: int = 0;
```

### Float (float)
```jac
gpa: float = 3.85;
temperature: float = 98.6;
price: float = 19.99;
```

### Boolean (bool)
```jac
is_enrolled: bool = true;
has_passed: bool = false;
is_active: bool = true;
```

## The 'any' Type

The `any` type provides flexibility for dynamic content:

```jac
flexible_value: any = 42;
flexible_value = "Now I'm a string";
flexible_value = [1, 2, 3];
flexible_value = {"key": "value"};
```

## Type Annotations

JAC requires type annotations for all variables:

```jac
# Correct - fully typed
student_score: int = 95;
student_name: str = "Alice";

# Also correct - type inference for constants
PI = 3.14159;  # Type inferred as float
NAME = "JAC";  # Type inferred as str
```

## Collections

### Lists
```jac
student_names: list[str] = ["Alice", "Bob", "Charlie"];
test_scores: list[int] = [85, 92, 78, 95];
mixed_data: list[any] = [1, "hello", true, 3.14];
```

### Dictionaries
```jac
student_record: dict[str, any] = {
    "name": "Alice Johnson",
    "age": 20,
    "major": "Computer Science",
    "gpa": 3.85,
    "courses": ["Math", "Physics", "Programming"]
};
```

### Tuples (Immutable)
```jac
coordinates: tuple[int, int] = (10, 20);
student_info: tuple[str, int, str] = ("Alice", 20, "CS");
```

### Sets (Unique items)
```jac
student_ids: set[int] = {101, 102, 103, 101};  # {101, 102, 103}
unique_names: set[str] = {"Alice", "Bob", "Alice"};  # {"Alice", "Bob"}
```

## Type Checking

JAC can check types at runtime:

```jac
def process_student_data(data: dict[str, any]) -> str {
    if (data["score"] is int) {
        return "Valid integer score";
    } else {
        return "Invalid score type";
    }
}
```

## Global Variables

Use `glob` for variables accessible throughout your program:

```jac
glob school_name: str = "JAC University";
glob passing_grade: int = 60;
glob max_students: int = 100;

def get_school_info() -> str {
    return f"Welcome to {school_name}";
}
```

## Type Conversion

```jac
# Converting between types
score_text: str = "85";
score_number: int = int(score_text);  # "85" -> 85
gpa_text: str = str(3.85);           # 3.85 -> "3.85"

# Checking types
def check_type(value: any) -> str {
    if (value is int) {
        return "integer";
    } elif (value is str) {
        return "string";
    } elif (value is bool) {
        return "boolean";
    } else {
        return "unknown";
    }
}
```

## Best Practices

1. **Always specify types**: Don't rely on type inference
2. **Use descriptive names**: `student_grade` not `sg`
3. **Choose appropriate types**: Use `bool` for true/false, not `int`
4. **Avoid `any` when possible**: Strong typing catches errors
5. **Document complex types**: Comments help understanding

Ready to learn about operators and expressions? Let's continue!''',
                'duration': 60
            },
            {
                'order': 4,
                'title': 'Functions and Control Flow',
                'type': 'text',
                'content': '''# Functions and Control Flow

Functions are the building blocks of organized code in JAC. Control flow allows your programs to make decisions and repeat actions.

## Functions

### Basic Function Syntax

```jac
def greet_student(name: str) -> str {
    return f"Hello, {name}! Welcome to JAC.";
}

withentry {
    message: str = greet_student("Alice");
    print(message);  # Output: Hello, Alice! Welcome to JAC.
}
```

### Function Parameters

```jac
# Single parameter
def calculate_grade(score: int) -> str {
    if (score >= 90) return "A";
    elif (score >= 80) return "B";
    elif (score >= 70) return "C";
    elif (score >= 60) return "D";
    else return "F";
}

# Multiple parameters
def calculate_gpa(grades: list[int]) -> float {
    if (len(grades) == 0) return 0.0;
    
    total: int = 0;
    for grade in grades {
        total += grade;
    }
    return total / len(grades);
}

# Default parameters
def format_student_info(name: str, grade: str = "N/A") -> str {
    return f"Student: {name}, Grade: {grade}";
}
```

### Function Return Types

```jac
# Void function (no return value)
def print_welcome(message: str) -> void {
    print(f"Welcome: {message}");
}

# Returning multiple values
def get_student_stats(scores: list[int]) -> tuple[float, int, int] {
    if (len(scores) == 0) {
        return (0.0, 0, 0);
    }
    
    total: int = 0;
    high_score: int = scores[0];
    low_score: int = scores[0];
    
    for score in scores {
        total += score;
        if (score > high_score) high_score = score;
        if (score < low_score) low_score = score;
    }
    
    average: float = total / len(scores);
    return (average, high_score, low_score);
}
```

## Control Flow Statements

### If-Else Statements

```jac
def determine_grade_level(score: int) -> str {
    if (score >= 95) {
        return "Exceptional";
    } elif (score >= 85) {
        return "Excellent";
    } elif (score >= 75) {
        return "Good";
    } elif (score >= 65) {
        return "Satisfactory";
    } else {
        return "Needs Improvement";
    }
}

# Complex conditionals
def is_eligible_for_honor_roll(gpa: float, attendance: float, behavior_score: int) -> bool {
    return (gpa >= 3.5) and (attendance >= 0.95) and (behavior_score >= 4);
}
```

### While Loops

```jac
def count_to_number(target: int) -> void {
    count: int = 1;
    while (count <= target) {
        print(f"Count: {count}");
        count += 1;
    }
}

def find_first_even(numbers: list[int]) -> int {
    index: int = 0;
    while (index < len(numbers)) {
        if (numbers[index] % 2 == 0) {
            return numbers[index];
        }
        index += 1;
    }
    return -1;  # No even number found
}
```

### For Loops

```jac
# For-in loop (iterating over collections)
def print_student_names(names: list[str]) -> void {
    for name in names {
        print(f"Student: {name}");
    }
}

# For loop with range
def print_numbers(start: int, end: int) -> void {
    for i: int = start; i <= end; i += 1 {
        print(f"Number: {i}");
    }
}

# Enumerate with index
def print_with_index(items: list[str]) -> void {
    for index, item in enumerate(items) {
        print(f"{index}: {item}");
    }
}
```

### Break and Continue

```jac
def find_target_score(target: int, scores: list[int]) -> int {
    for score in scores {
        if (score == target) {
            print(f"Found target score: {target}");
            break;  # Exit loop early
        }
    }
    
    # Process all scores, skip negatives
    for score in scores {
        if (score < 0) {
            continue;  # Skip this iteration
        }
        print(f"Processing score: {score}");
    }
}
```

### Match Statements (Pattern Matching)

```jac
def process_student_type(student_type: str) -> str {
    match student_type {
        case "undergraduate" {
            return "Bachelor's degree program";
        }
        case "graduate" {
            return "Master's or PhD program";
        }
        case "doctoral" {
            return "PhD research program";
        }
        case _ {  # Default case
            return "Unknown student type";
        }
    }
}

def categorize_score(score: int) -> str {
    match score {
        case s if (s >= 90) {
            return "Excellent (A)";
        }
        case s if (s >= 80) {
            return "Good (B)";
        }
        case s if (s >= 70) {
            return "Average (C)";
        }
        case s if (s >= 60) {
            return "Below Average (D)";
        }
        case _ {
            return "Failing (F)";
        }
    }
}
```

## Function Best Practices

1. **Single Responsibility**: Each function should do one thing well
2. **Descriptive Names**: `calculate_grade_average` not `calc_avg`
3. **Type Annotations**: Always specify parameter and return types
4. **Early Returns**: Return early for edge cases
5. **Documentation**: Comment complex logic and algorithms

## Control Flow Best Practices

1. **Keep Conditions Simple**: Complex conditions should be broken down
2. **Use Meaningful Variable Names**: `student_score` not `s`
3. **Avoid Deep Nesting**: More than 3 levels is hard to follow
4. **Choose Right Loop**: for-in for collections, while for conditions
5. **Break Early**: Return or break when condition is met

Ready to work with collections and operators? Let's continue!''',
                'duration': 75
            },
            {
                'order': 5,
                'title': 'Operators and Collections',
                'type': 'text',
                'content': '''# Operators and Collections

Master JAC's operators and learn to work effectively with collections like lists, dictionaries, and sets.

## Arithmetic Operators

```jac
withentry {
    # Basic arithmetic
    a: int = 10;
    b: int = 3;
    
    print(f"Addition: {a} + {b} = {a + b}");        # 13
    print(f"Subtraction: {a} - {b} = {a - b}");    # 7
    print(f"Multiplication: {a} * {b} = {a * b}"); # 30
    print(f"Division: {a} / {b} = {a / b}");      # 3.33...
    print(f"Floor Division: {a} // {b} = {a // b}"); # 3
    print(f"Modulo: {a} % {b} = {a % b}");        # 1
    print(f"Exponent: {a} ** {b} = {a ** b}");    # 1000
}
```

## Assignment Operators

```jac
score: int = 100;

# Compound assignments
score += 5;      # score = score + 5  -> 105
score -= 10;     # score = score - 10 -> 95
score *= 2;      # score = score * 2  -> 190
score /= 5;      # score = score / 5  -> 38.0
score %= 7;      # score = score % 7  -> 3.0

print(f"Final score: {score}");
```

## Comparison Operators

```jac
def compare_scores(student1: int, student2: int) -> dict[str, bool] {
    return {
        "equal": student1 == student2,
        "not_equal": student1 != student2,
        "greater": student1 > student2,
        "less": student1 < student2,
        "greater_equal": student1 >= student2,
        "less_equal": student1 <= student2
    };
}
```

## Logical Operators

```jac
def evaluate_student(score: int, attendance: float, participation: int) -> str {
    # Using logical operators
    excellent: bool = (score >= 90) and (attendance >= 0.95);
    good_enough: bool = (score >= 80) or (participation >= 8);
    not_failing: bool = score >= 60;
    
    if (excellent) {
        return "Honor Roll";
    } elif (good_enough and not_failing) {
        return "Passing";
    } else {
        return "Needs Improvement";
    }
}
```

## Working with Lists

```jac
# Creating and initializing lists
student_names: list[str] = [];
test_scores: list[int] = [85, 92, 78, 95, 88];
mixed_data: list[any] = ["Alice", 20, 3.85, true];

# Adding elements
student_names.append("Alice");
student_names.append("Bob");
student_names.insert(1, "Charlie");  # Insert at index 1

# Accessing elements
first_student: str = student_names[0];      # "Alice"
last_student: str = student_names[-1];      # "Bob"

# Removing elements
removed: str = student_names.pop();         # Remove and return last
student_names.remove("Charlie");            # Remove first occurrence of "Charlie"

# List operations
list_length: int = len(student_names);
is_empty: bool = len(student_names) == 0;
contains_alice: bool = "Alice" in student_names;

# List slicing
first_three: list[str] = student_names[0:3];
last_two: list[str] = student_names[-2:];
all_except_first: list[str] = student_names[1:];
```

## List Methods and Functions

```jac
def analyze_scores(scores: list[int]) -> dict[str, any] {
    if (len(scores) == 0) {
        return {"error": "No scores provided"};
    }
    
    # Built-in functions
    total: int = sum(scores);
    count: int = len(scores);
    average: float = total / count;
    max_score: int = max(scores);
    min_score: int = min(scores);
    
    # Sorting
    sorted_ascending: list[int] = sorted(scores);
    sorted_descending: list[int] = sorted(scores, reverse=true);
    
    return {
        "scores": scores,
        "total": total,
        "count": count,
        "average": average,
        "max": max_score,
        "min": min_score,
        "sorted_asc": sorted_ascending,
        "sorted_desc": sorted_descending
    };
}
```

## Working with Dictionaries

```jac
# Creating dictionaries
student_record: dict[str, any] = {
    "name": "Alice Johnson",
    "age": 20,
    "major": "Computer Science",
    "gpa": 3.85,
    "courses": ["Math", "Physics", "Programming"],
    "active": true
};

# Accessing values
name: str = student_record["name"];  # "Alice Johnson"
age: int = student_record.get("age", 0);  # 20, with default

# Adding/updating values
student_record["year"] = "Junior";
student_record["gpa"] = 3.90;

# Removing values
removed_value: any = student_record.pop("active", false);
del student_record["year"];  # Remove key-value pair

# Dictionary methods
all_keys: list[str] = list(student_record.keys());
all_values: list[any] = list(student_record.values());
key_value_pairs: list[tuple[str, any]] = list(student_record.items());

# Checking membership
has_name: bool = "name" in student_record;
has_email: bool = "email" in student_record;

print(f"Keys: {all_keys}");
print(f"Values: {all_values}");
```

## Dictionary Comprehensions

```jac
# Creating dictionaries from other data
score_dict: dict[str, int] = {
    "Alice": 95,
    "Bob": 87,
    "Charlie": 92,
    "Diana": 89
};

# Filter high performers (90+)
high_performers: dict[str, int] = {
    name: score for name, score in score_dict.items() 
    if score >= 90
};

# Create grade mapping
grade_mapping: dict[str, str] = {
    name: (score >= 90 ? "A" : score >= 80 ? "B" : "C")
    for name, score in score_dict.items()
};

print(f"High performers: {high_performers}");
print(f"Grade mapping: {grade_mapping}");
```

## Working with Sets

```jac
# Creating sets
student_ids: set[int] = {101, 102, 103, 101};  # {101, 102, 103} (duplicates removed)
course_codes: set[str] = {"CS101", "MATH201", "PHY301", "CS101"};

# Set operations
all_students: set[int] = student_ids | {104, 105};        # Union
common_courses: set[str] = course_codes & {"CS101", "MATH201"};  # Intersection
unique_courses: set[str] = course_codes - {"CS101"};      # Difference

# Set methods
course_codes.add("ENG101");
course_codes.remove("PHY301");
has_cs101: bool = "CS101" in course_codes;
is_empty: bool = len(course_codes) == 0;

print(f"Student IDs: {student_ids}");
print(f"Course codes: {course_codes}");
```

## String Operations

```jac
def string_operations_demo() -> void {
    name: str = "Alice Johnson";
    course: str = "Computer Science";
    
    # String length and access
    name_length: int = len(name);
    first_char: str = name[0];        # "A"
    last_char: str = name[-1];        # "n"
    
    # String methods
    uppercase: str = name.upper();              # "ALICE JOHNSON"
    lowercase: str = course.lower();            # "computer science"
    title_case: str = name.title();             # "Alice Johnson"
    split_name: list[str] = name.split(" ");    # ["Alice", "Johnson"]
    joined_name: str = split_name.join(" ");    # "Alice Johnson"
    
    # String formatting
    formatted1: str = f"Student: {name}, Course: {course}";
    formatted2: str = "Student: {}, Course: {}".format(name, course);
    padded: str = name.pad(20);                 # "Alice Johnson       "
    
    # String checking
    starts_with_a: bool = name.startswith("A");
    ends_with_n: bool = name.endswith("n");
    contains_space: bool = " " in name;
    
    print(f"Name: {name}");
    print(f"Length: {name_length}");
    print(f"Uppercase: {uppercase}");
    print(f"Split: {split_name}");
}
```

## Collection Best Practices

1. **Choose the right collection**: Lists for ordered data, sets for unique items, dicts for key-value
2. **Avoid mutations in loops**: Create new collections instead
3. **Use comprehensions**: Cleaner syntax for creating collections
4. **Handle empty collections**: Always check for empty before processing
5. **Type your collections**: `list[int]` not `list`

Ready to learn about Object-Oriented Programming in JAC? Let's continue!''',
                'duration': 60
            }
        ]

    def get_module1_assessments(self):
        return [
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
                        'text': 'Which data type would you use for a student\'s GPA (3.85)?',
                        'type': 'multiple_choice',
                        'difficulty': 'beginner',
                        'points': 1.0,
                        'options': ['int', 'str', 'float', 'bool'],
                        'correct_answer': {'index': 2},
                        'explanation': 'GPA values with decimals require the float data type.'
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
                        'explanation': 'withentry marks the starting point of a JAC program, similar to main() in other languages.'
                    },
                    {
                        'text': 'How do you access the first element of a list named `students`?',
                        'type': 'multiple_choice',
                        'difficulty': 'beginner',
                        'points': 1.0,
                        'options': [
                            'students.first()',
                            'students(0)',
                            'students[0]',
                            'students.get(0)'
                        ],
                        'correct_answer': {'index': 2},
                        'explanation': 'JAC uses square brackets for list indexing, similar to Python: students[0]'
                    },
                    {
                        'text': 'Write a JAC function that takes an integer score and returns "Pass" if score >= 60, otherwise "Fail".',
                        'type': 'code',
                        'difficulty': 'intermediate',
                        'points': 3.0,
                        'code_template': '''def check_pass_fail(score: int) -> str {
    # Your code here
    
}''',
                        'correct_answer': {'code': '''def check_pass_fail(score: int) -> str {
    if (score >= 60) {
        return "Pass";
    } else {
        return "Fail";
    }
}'''},
                        'explanation': 'This function uses an if-else statement to compare the score against the passing threshold.'
                    }
                ]
            },
            {
                'title': 'JAC Functions Coding Exercise',
                'description': 'Practice writing JAC functions with proper type annotations and control flow.',
                'type': 'assignment',
                'difficulty': 'intermediate',
                'time_limit': 45,
                'max_attempts': 2,
                'passing_score': 80.0,
                'questions': [
                    {
                        'text': 'Create a function `calculate_average` that takes a list of integers and returns the average as a float.',
                        'type': 'code',
                        'difficulty': 'intermediate',
                        'points': 5.0,
                        'code_template': '''def calculate_average(scores: list[int]) -> float {
    # Handle empty list
    # Calculate sum
    # Return average
    
}''',
                        'correct_answer': {'code': '''def calculate_average(scores: list[int]) -> float {
    if (len(scores) == 0) {
        return 0.0;
    }
    
    total: int = 0;
    for score in scores {
        total += score;
    }
    
    return total / len(scores);
}'''},
                        'explanation': 'This solution handles edge cases and uses proper type annotations.'
                    },
                    {
                        'text': 'Write a function `find_grade_letter` that converts a numeric score to a letter grade (A: 90+, B: 80-89, C: 70-79, D: 60-69, F: <60).',
                        'type': 'code',
                        'difficulty': 'intermediate',
                        'points': 5.0,
                        'code_template': '''def find_grade_letter(score: int) -> str {
    # Use if-elif-else chain
    
}''',
                        'correct_answer': {'code': '''def find_grade_letter(score: int) -> str {
    if (score >= 90) {
        return "A";
    } elif (score >= 80) {
        return "B";
    } elif (score >= 70) {
        return "C";
    } elif (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}'''},
                        'explanation': 'This uses a cascading if-elif-else structure to assign letter grades based on score ranges.'
                    }
                ]
            }
        ]

    # Module 2: Object-Spatial Programming Content
    def get_module2_content(self):
        return '''# Module 2: Object-Spatial Programming (OSP)

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

Imagine you're organizing a university:
- **Traditional approach**: Gather all student data, process it, return results
- **OSP approach**: Send agents (walkers) to visit student nodes, process them on-site

## Why OSP?

1. **Natural Problem Modeling**: Many real-world problems are spatial/graph-based
2. **Performance**: Computation happens where data lives
3. **Scalability**: Handle distributed and networked data naturally
4. **AI Integration**: Perfect for AI agents and knowledge graphs
5. **Cleaner Code**: Separate data structure from traversal logic

## The OSP Trinity

- **Nodes**: Data locations (like houses in a neighborhood)
- **Edges**: Relationships between nodes (like roads between houses)  
- **Walkers**: Mobile computation (like people walking between houses)

## Learning Approach

Each lesson builds on the previous:
1. **Concept Introduction**: Understand the theory
2. **Practical Examples**: See OSP in action
3. **Hands-on Exercises**: Build your own graph applications
4. **Real-world Applications**: Connect to practical uses

Let's explore this paradigm-shifting approach to programming!'''

    def get_module2_code_examples(self):
        return [
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

edge Teaches {
    has start_date: str;
    has schedule: str;
}

# Create the graph
withentry {
    # Create nodes
    alice: Student = Student(name="Alice Johnson", age=20, major="CS", gpa=3.8);
    bob: Student = Student(name="Bob Smith", age=21, major="Math", gpa=3.6);
    
    cs101: Course = Course(title="Intro to Programming", code="CS101", credits=3);
    math201: Course = Course(title="Calculus II", code="MATH201", credits=4);
    
    # Create connections
    alice +>:EnrolledIn(semester="Fall 2024", grade="A"):+> cs101;
    bob +>:EnrolledIn(semester="Fall 2024", grade="B"):+> math201;
    
    cs101 +>:Teaches(start_date="2024-08-15", schedule="MWF 10:00"):+> alice;
    
    print("Graph created successfully!");
}''',
                'description': 'Basic nodes, edges, and connections'
            },
            {
                'title': 'Walker Traversal',
                'code': '''# Define nodes with abilities
node Student {
    has name: str;
    has gpa: float;
    has status: str = "active";
    
    can greet with visitor entry {
        print(f"Hello {visitor.name}! I'm {self.name} with GPA {self.gpa}");
    }
    
    can calculate_honor_status {
        if (self.gpa >= 3.5) {
            self.status = "honor_student";
        } else {
            self.status = "regular_student";
        }
    }
}

# Define a walker
walker StudentExplorer {
    has visitor_name: str = "Explorer";
    
    can start with `root entry {
        print(f"Starting exploration as {self.visitor_name}");
        visit[-->];  # Visit all connected nodes
        disengage;
    }
    
    can visit_student with Student entry {
        print(f"Found student: {self.context.name}");
        self.context.calculate_honor_status();
        print(f"Status: {self.context.status}");
    }
}

withentry {
    # Create student nodes
    alice: Student = Student(name="Alice", gpa=3.8);
    bob: Student = Student(name="Bob", gpa=3.2);
    charlie: Student = Student(name="Charlie", gpa=3.9);
    
    # Connect them to root
    alice <-: connected_to :-> `root;
    bob <-: connected_to :-> `root;
    charlie <-: connected_to :-> `root;
    
    # Start walker
    StudentExplorer(visitor_name="Data Collector");
}''',
                'description': 'Walkers traversing graph and triggering node abilities'
            },
            {
                'title': 'Graph Queries and Filtering',
                'code': '''# Advanced filtering and querying
node Person {
    has name: str;
    has age: int;
    has occupation: str;
}

edge FriendWith {
    has strength: float = 0.5;  # Friendship strength 0-1
    has since: str;
}

withentry {
    # Create a social network
    alice: Person = Person(name="Alice", age=25, occupation="Engineer");
    bob: Person = Person(name="Bob", age=30, occupation="Designer");
    charlie: Person = Person(name="Charlie", age=28, occupation="Teacher");
    diana: Person = Person(name="Diana", age=26, occupation="Engineer");
    
    # Create friendship edges with different strengths
    alice +>:FriendWith(strength=0.8, since="2020"):+> bob;
    alice +>:FriendWith(strength=0.6, since="2019"):+> charlie;
    bob +>:FriendWith(strength=0.9, since="2018"):+> diana;
    charlie +>:FriendWith(strength=0.7, since="2021"):+> diana;
    
    # Connect all to root
    alice <-: connected_to :-> `root;
    bob <-: connected_to :-> `root;
    charlie <-: connected_to :-> `root;
    diana <-: connected_to :-> `root;
    
    # Query examples
    print("=== All connections from Alice ===");
    # Get all nodes Alice is connected to
    alice_connections = [alice-->];
    for person in alice_connections {
        print(f"Connected to: {person.name}");
    }
    
    print("\\n=== Strong friendships (strength > 0.7) ===");
    # Find strong friendships
    strong_friends = [alice->:FriendWith(strength>0.7:->)];
    for edge in strong_friends {
        print(f"Strong friendship with {edge.dest.name}, strength: {edge.strength}");
    }
    
    print("\\n=== Engineers only ===");
    # Filter by occupation
    engineers = [alice->:FriendWith->:(?Person:occupation=="Engineer")];
    for person in engineers {
        print(f"Engineer friend: {person.name}");
    }
    
    print("\\n=== Young friends (age < 27) ===");
    young_friends = [alice->:FriendWith->:(?Person:age<27)];
    for person in young_friends {
        print(f"Young friend: {person.name}, age: {person.age}");
    }
}''',
                'description': 'Advanced graph queries and filtering techniques'
            },
            {
                'title': 'Walker Inheritance and Composition',
                'code': '''# Advanced walker patterns
node Service {
    has name: str;
    has status: str = "available";
}

node Weather(Service) {
    has temperature: int = 75;
    has condition: str = "sunny";
}

node Time(Service) {
    has hour: int = 12;
    has minute: int = 30;
    has period: str = "PM";
}

# Base walker
walker StateAgent {
    has state: dict[str, any] = {};
    
    can start with `root entry {
        print("Starting state collection...");
    }
    
    can visit_service with Service entry {
        print(f"Visiting service: {self.context.name}");
        self.state[self.context.name] = {
            "status": self.context.status,
            "data": self.context.get_service_data()
        };
    }
}

# Specialized walker for weather only
walker WeatherCollector(StateAgent) {
    can visit_weather with Weather entry {
        print(f"Collecting weather: {self.context.condition}, {self.context.temperature}°F");
        self.state["weather"] = {
            "temperature": self.context.temperature,
            "condition": self.context.condition
        };
    }
}

# Multi-modal data collector
walker DataAggregator {
    has collected_data: dict[str, any] = {};
    
    can aggregate with `root entry {
        visit[-->(?Service)];  # Visit all service nodes
        self.generate_report();
    }
    
    can aggregate with Weather entry {
        self.collected_data["weather"] = self.context.get_weather_report();
    }
    
    can aggregate with Time entry {
        self.collected_data["time"] = self.context.get_time_report();
    }
    
    can generate_report {
        print("\\n=== Data Aggregation Report ===");
        for category, data in self.collected_data.items() {
            print(f"{category}: {data}");
        }
    }
}

# Sample service data methods
node Service {
    can get_service_data -> dict[str, any] {
        return {"name": self.name, "status": self.status};
    }
}

node Weather {
    can get_weather_report -> str {
        return f"{self.condition} weather at {self.temperature}°F";
    }
}

node Time {
    can get_time_report -> str {
        return f"Current time: {self.hour}:{self.minute} {self.period}";
    }
}

withentry {
    # Create service nodes
    weather_node: Weather = Weather(name="Weather Service", temperature=72, condition="cloudy");
    time_node: Time = Time(name="Time Service", hour=2, minute=45, period="PM");
    
    # Connect to root
    weather_node <-: connected_to :-> `root;
    time_node <-: connected_to :-> `root;
    
    print("=== Weather Collector ===");
    WeatherCollector();
    
    print("\\n=== Data Aggregator ===");
    DataAggregator();
}''',
                'description': 'Walker inheritance and specialized data collection'
            }
        ]

    def get_module2_lessons(self):
        return [
            {
                'order': 1,
                'title': 'Introduction to Object-Spatial Programming',
                'type': 'text',
                'content': '''# Introduction to Object-Spatial Programming

Welcome to the paradigm that will change how you think about programming! Object-Spatial Programming (OSP) is JAC's revolutionary approach to organizing and processing data.

## The Traditional Programming Problem

In traditional programming (like Python, Java, C++), we follow this pattern:

```
1. Gather all data into memory
2. Apply computation to the data  
3. Return results
```

**Example**: Processing student records
```python
# Traditional approach
students = get_all_students()  # Get all data
honor_students = []           # Process data
for student in students:
    if student.gpa >= 3.5:
        honor_students.append(student)
return honor_students          # Return results
```

**Problems with this approach:**
- **Memory Intensive**: All data must fit in memory
- **Inefficient**: Moving lots of data around
- **Not Natural**: Many problems are inherently spatial/relational
- **Scalability Issues**: Difficult to handle distributed data

## The OSP Revolution

OSP flips the script: **"Send computation to the data!"**

```
1. Data stays where it is (distributed)
2. Send mobile computation (walkers) to process data
3. Collect results from the computation
```

**Example**: Processing student records with OSP
```jac
# OSP approach - walker goes to each student
walker HonorRollChecker {
    can check_student with Student entry {
        if (self.context.gpa >= 3.5) {
            report self.context;  # Stream result back
        }
    }
}

// Later...
honor_students = HonorRollChecker();  # Results stream back
```

## The OSP Trinity

OSP is built on three fundamental concepts:

### 1. Nodes (Data Locations)
Think of nodes as **houses in a neighborhood**. They hold data and can interact with visitors.

```jac
node Student {
    has name: str;
    has gpa: float;
    has major: str;
    
    // Methods that activate when visited
    can greet with visitor entry {
        print(f"Hello {visitor.name}! I'm {self.name}");
    }
}
```

### 2. Edges (Relationships)  
Edges are **first-class relationships** between nodes. They can have their own properties.

```jac
// Edge type with properties
edge EnrolledIn {
    has semester: str;
    has grade: str;
}

// Creating connections
alice +>:EnrolledIn(semester="Fall 2024", grade="A"):+> cs101;
```

### 3. Walkers (Mobile Computation)
Walkers are **people walking between houses**. They move through the graph, triggering interactions.

```jac
walker StudentExplorer {
    has explorer_name: str;
    
    can start with `root entry {
        print("Starting exploration...");
        visit[-->];  // Visit all connected nodes
    }
    
    can visit_student with Student entry {
        print(f"Found: {self.context.name}");
    }
}
```

## Why OSP Matters

### 1. **Natural Problem Modeling**
Real-world problems often involve relationships:
- Social networks (friendships, follows)
- Transportation systems (routes, connections)
- Knowledge graphs (concepts, relationships)
- Supply chains (suppliers, products, orders)

### 2. **Performance Benefits**
- **Data Locality**: Computation happens where data lives
- **Memory Efficiency**: Don't need to load everything into memory
- **Parallelism**: Multiple walkers can work simultaneously
- **Distributed Computing**: Natural fit for distributed systems

### 3. **AI and Knowledge Graphs**
OSP is perfect for AI applications:
- **Knowledge Representation**: Facts and relationships
- **Reasoning**: Following chains of inference
- **Recommendation Systems**: Finding related items
- **Natural Language Processing**: Parsing relationships in text

### 4. **Cleaner Architecture**
```jac
// Traditional: Mix data and behavior
class Student:
    def process_all_students(self):
        # Complex logic mixed with data

// OSP: Separate concerns
node Student {
    has data;  // Just data
    can greet; // Simple, focused methods
}

walker StudentProcessor {
    has algorithm;  // Separate algorithm
    can visit_student; // Focused behavior
}
```

## JAC's Spatial Thinking

In JAC, you think spatially:

**Instead of**: "Get all students and filter them"
**Think**: "Send a walker to visit all student nodes"

**Instead of**: "Find connected users"
**Think**: "Query the graph for connections"

**Instead of**: "Process this tree recursively"  
**Think**: "Let a walker traverse the tree"

## Key OSP Principles

1. **Data is Spatial**: Organize information in space (graphs)
2. **Computation is Mobile**: Send agents to process data
3. **Relationships are First-Class**: Edges have properties and behavior
4. **Declarative Queries**: Ask "what" not "how"
5. **Streaming Results**: Get results as they're found
6. **Type-Driven Interactions**: Abilities trigger based on node types

## Your OSP Journey

In this module, you'll learn to:
1. **Think Spatially**: See problems as graph navigation
2. **Define Nodes and Edges**: Create your graph structures
3. **Build Walkers**: Write mobile computation agents
4. **Master Abilities**: Create interactive node behaviors
5. **Query Graphs**: Use JAC's powerful graph syntax
6. **Handle Complexity**: Build sophisticated applications

Ready to dive into nodes and edges? Let's start building!''',
                'duration': 45
            },
            {
                'order': 2,
                'title': 'Nodes: The Building Blocks',
                'type': 'text',
                'content': '''# Nodes: The Building Blocks of OSP

Nodes are the fundamental data containers in Object-Spatial Programming. Think of them as **smart data containers** that can hold information and interact with visiting computation.

## What is a Node?

A node represents an **entity or location** in your application's graph. Unlike traditional objects, nodes are:
- **Persistent**: Connected nodes save automatically
- **Interactive**: Can have abilities that trigger during visits
- **Spatial**: Located in a graph with other nodes
- **Type-Safe**: All properties must have explicit types

## Basic Node Definition

```jac
node Student {
    // Properties (data)
    has name: str;
    has age: int;
    has major: str;
    has gpa: float;
    
    // Constructor (automatic)
    // Properties are initialized with provided values
}
```

**Creating a student node:**
```jac
withentry {
    alice: Student = Student(
        name="Alice Johnson",
        age=20,
        major="Computer Science", 
        gpa=3.85
    );
    
    print(f"Created student: {alice.name}");
}
```

## Node Properties

### Required Properties
All properties must be provided during node creation:

```jac
node Book {
    has title: str;          // Required
    has author: str;         // Required
    has pages: int;          // Required
    has isbn: str;           // Required
}

withentry {
    // All properties must be provided
    my_book: Book = Book(
        title="Clean Code",
        author="Robert Martin",
        pages=464,
        isbn="978-0132350884"
    );
}
```

### Default Values
Provide defaults for optional properties:

```jac
node Student {
    has name: str;                    // Required
    has age: int;                     // Required
    has status: str = "active";       // Default value
    has gpa: float = 0.0;            // Default value
    has courses: list[str] = [];      // Default empty list
}

withentry {
    // Can omit properties with defaults
    new_student: Student = Student(
        name="Bob Smith",
        age=19
    );
    
    print(f"Status: {new_student.status}");  // "active"
    print(f"GPA: {new_student.gpa}");        // 0.0
    print(f"Courses: {new_student.courses}"); // []
}
```

## Node Abilities (Methods)

Nodes can have **abilities** - special methods that trigger automatically when specific events occur.

### Entry Abilities
Trigger when a walker visits the node:

```jac
node Student {
    has name: str;
    has gpa: float;
    
    // This ability triggers when any walker visits
    can greet with visitor entry {
        print(f"Hello {visitor.name}! I'm {self.name}.");
    }
    
    // This ability triggers for specific walker types
    can assess with Grader entry {
        if (self.gpa >= 3.5) {
            print(f"{self.name}: Honor student!");
        } else {
            print(f"{self.name}: Keep studying!");
        }
    }
}
```

### Custom Abilities
Methods that can be called explicitly:

```jac
node Student {
    has name: str;
    has gpa: float;
    has credit_hours: int = 0;
    
    // Custom ability
    can calculate_academic_status -> str {
        if (self.gpa >= 3.5) {
            return "Honor Student";
        } elif (self.gpa >= 3.0) {
            return "Good Standing";
        } elif (self.gpa >= 2.0) {
            return "Satisfactory";
        } else {
            return "Academic Warning";
        }
    }
    
    // Ability with parameters
    can update_gpa(new_gpa: float, hours: int) -> void {
        old_points: float = self.gpa * self.credit_hours;
        new_points: float = new_gpa * hours;
        self.credit_hours += hours;
        self.gpa = (old_points + new_points) / self.credit_hours;
    }
}

withentry {
    alice: Student = Student(name="Alice", gpa=3.8, credit_hours=60);
    
    // Call abilities explicitly
    status: str = alice.calculate_academic_status();
    print(f"Academic Status: {status}");
    
    // Update GPA
    alice.update_gpa(3.9, 15);  // New GPA, 15 credit hours
    print(f"Updated GPA: {alice.gpa}");
}
```

## Node Inheritance

Nodes can inherit from other nodes, creating hierarchical relationships:

```jac
// Base node
node Person {
    has name: str;
    has age: int;
    has email: str;
    
    can introduce_self {
        print(f"Hi, I'm {self.name}, {self.age} years old");
    }
}

// Student inherits from Person
node Student(Person) {
    has student_id: str;
    has major: str;
    has gpa: float;
    
    // Can override inherited abilities
    can introduce_self {
        print(f"Hi, I'm {self.name}, a {self.major} student");
    }
    
    // Student-specific ability
    can study_hours -> int {
        return int(self.gpa * 10);  // Simple heuristic
    }
}

// Teacher inherits from Person
node Teacher(Person) {
    has employee_id: str;
    has department: str;
    has salary: float;
    
    can teach_subject(subject: str) -> void {
        print(f"I teach {subject} in the {self.department} department");
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
    
    bob: Teacher = Teacher(
        name="Dr. Smith",
        age=45,
        email="smith@college.edu",
        employee_id="T67890",
        department="Computer Science",
        salary=75000.0
    );
    
    // All have the basic introduce_self ability
    alice.introduce_self();    // "Hi, I'm Alice Johnson, a Computer Science student"
    bob.introduce_self();      // "Hi, I'm Dr. Smith, 45 years old"
    
    // Student-specific ability
    print(f"Alice studies {alice.study_hours()} hours per week");
    
    // Teacher-specific ability
    bob.teach_subject("Data Structures");
}
```

## Node Persistence

**Magical Feature**: Nodes connected to the root node **automatically persist** between program runs!

```jac
// This data will be saved automatically!
withentry {
    // Create and connect nodes to root
    alice: Student = Student(name="Alice", age=20, gpa=3.8);
    bob: Student = Student(name="Bob", age=21, gpa=3.6);
    
    // Connect to root (this enables persistence)
    alice <-: connected_to :-> `root;
    bob <-: connected_to :-> `root;
    
    print("Students saved to database automatically!");
}

// When you run the program again, alice and bob will still exist!
```

## Advanced Node Patterns

### 1. Computed Properties
```jac
node Student {
    has name: str;
    has grades: list[int] = [];
    
    // Computed property (not stored)
    can get_average_grade -> float {
        if (len(self.grades) == 0) {
            return 0.0;
        }
        total: int = 0;
        for grade in self.grades {
            total += grade;
        }
        return total / len(self.grades);
    }
}
```

### 2. Event-Driven Updates
```jac
node Student {
    has name: str;
    has gpa: float;
    has status: str = "active";
    
    can gpa_updated(new_gpa: float) -> void {
        self.gpa = new_gpa;
        
        // Update status based on GPA
        if (new_gpa < 2.0) {
            self.status = "academic_warning";
        } elif (new_gpa >= 3.5) {
            self.status = "honor_roll";
        }
        
        print(f"{self.name} status updated to: {self.status}");
    }
}
```

## Best Practices for Nodes

1. **Keep Properties Simple**: Each property should hold one piece of information
2. **Use Descriptive Names**: `student_email` not `se`
3. **Provide Defaults**: Make optional properties have sensible defaults
4. **Write Focused Abilities**: Each ability should have one clear purpose
5. **Document Complex Logic**: Abilities can be complex, add comments
6. **Use Type Annotations**: All properties and methods need types
7. **Plan for Inheritance**: Design base nodes that can be extended

## Common Node Patterns

### 1. **Data Container Node**
```jac
node Configuration {
    has app_name: str;
    has version: str;
    has debug_mode: bool = false;
}
```

### 2. **Event Emitter Node**
```jac
node EventSource {
    has event_type: str;
    has data: dict[str, any] = {};
    
    can emit_event(event_type: str, event_data: dict[str, any]) -> void {
        self.event_type = event_type;
        self.data = event_data;
        report {"type": event_type, "data": event_data};
    }
}
```

### 3. **State Machine Node**
```jac
node ProcessState {
    has current_state: str = "idle";
    has history: list[str] = [];
    
    can transition_to(new_state: str) -> bool {
        if (self.is_valid_transition(new_state)) {
            self.history.append(self.current_state);
            self.current_state = new_state;
            return true;
        }
        return false;
    }
    
    can is_valid_transition(new_state: str) -> bool {
        valid_transitions: dict[str, list[str]] = {
            "idle": ["running", "paused"],
            "running": ["paused", "completed", "error"],
            "paused": ["running", "cancelled"],
            "completed": [],
            "cancelled": [],
            "error": ["idle"]
        };
        return new_state in valid_transitions.get(self.current_state, []);
    }
}
```

Ready to learn about edges and relationships? Let's continue!''',
                'duration': 75
            }
        ]

    def get_module2_assessments(self):
        return [
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
                    },
                    {
                        'text': 'How do you define a basic node in JAC?',
                        'type': 'multiple_choice',
                        'difficulty': 'beginner',
                        'points': 1.0,
                        'options': [
                            'class Student { has name: str; }',
                            'node Student { has name: str; }',
                            'obj Student { has name: str; }',
                            'struct Student { has name: str; }'
                        ],
                        'correct_answer': {'index': 1},
                        'explanation': 'JAC uses the `node` keyword to define node types with `has` for properties.'
                    },
                    {
                        'text': 'What keyword is used to define a walker?',
                        'type': 'multiple_choice',
                        'difficulty': 'beginner',
                        'points': 1.0,
                        'options': ['class', 'walker', 'agent', 'process'],
                        'correct_answer': {'index': 1},
                        'explanation': 'JAC uses `walker` to define mobile computation units that traverse the graph.'
                    },
                    {
                        'text': 'Write a simple node definition for a Book with title, author, and pages properties.',
                        'type': 'code',
                        'difficulty': 'intermediate',
                        'points': 3.0,
                        'code_template': '''# Define a Book node here

withentry {
    # Create a book instance
    my_book = Book(title="Clean Code", author="Robert Martin", pages=464);
    print(f"Book: {my_book.title} by {my_book.author}");
}''',
                        'correct_answer': {'code': '''node Book {
    has title: str;
    has author: str;
    has pages: int;
}

withentry {
    my_book: Book = Book(title="Clean Code", author="Robert Martin", pages=464);
    print(f"Book: {my_book.title} by {my_book.author}");
}'''},
                        'explanation': 'This defines a Book node with three properties and demonstrates creating an instance.'
                    },
                    {
                        'text': 'What does the `visit[-->]` statement do in a walker?',
                        'type': 'multiple_choice',
                        'difficulty': 'intermediate',
                        'points': 2.0,
                        'options': [
                            'Creates a new node',
                            'Visits all connected child nodes from current position',
                            'Deletes the current node',
                            'Exits the walker immediately'
                        ],
                        'correct_answer': {'index': 1},
                        'explanation': '`visit[-->]` makes the walker traverse to all nodes connected by outgoing edges.'
                    }
                ]
            }
        ]

    # Module 3: Advanced JAC Concepts Content
    def get_module3_content(self):
        return '''# Module 3: Advanced JAC Concepts

Take your JAC skills to the next level! This module covers advanced Object-Spatial Programming, enhanced OOP, and building production-ready applications.

## What You'll Learn

- **Enhanced OOP**: Advanced class hierarchies, multiple inheritance, and design patterns
- **Advanced OSP**: Complex graph operations, filtering, and optimization
- **Walker APIs**: Create RESTful APIs using walkers as endpoints
- **Persistence**: Master JAC's automatic persistence and data management
- **File Operations**: Import systems and external file handling
- **Error Handling**: Robust error management and debugging techniques

## Advanced Paradigms

This module bridges traditional OOP with spatial programming, showing you how to:
- Build scalable graph applications
- Create flexible API architectures
- Handle complex data relationships
- Implement production-grade error handling

## Real-World Applications

You'll build applications that demonstrate:
- Multi-user systems with permission management
- Graph-based recommendation engines
- API-driven web services
- Distributed data processing systems

Ready to become a JAC expert? Let's dive deep!'''

    def get_module3_code_examples(self):
        return [
            {
                'title': 'Enhanced OOP with Multiple Inheritance',
                'code': '''# Advanced class hierarchies and multiple inheritance
node Person {
    has name: str;
    has age: int;
    has email: str;
    
    can get_info -> dict[str, any] {
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email
        };
    }
}

node Loggable {
    has created_at: str;
    has updated_at: str = "";
    
    can log_activity(activity: str) -> void {
        timestamp: str = self.get_current_time();
        print(f"[{timestamp}] {self.name}: {activity}");
    }
    
    can get_current_time -> str {
        return "2024-11-24 15:30:00";
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
        self.update_timestamp();
    }
    
    can update_timestamp -> void {
        self.updated_at = self.get_current_time();
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
    alice.created_at = alice.get_current_time();
    
    alice.add_course("Data Structures");
    alice.add_course("Algorithms");
    
    print("Student Info:", alice.get_info());
}''',
                'description': 'Multiple inheritance and advanced OOP patterns'
            },
            {
                'title': 'Advanced Graph Queries and Filtering',
                'code': '''# Complex graph traversal and filtering patterns
node University {
    has name: str;
    has location: str;
}

node Student {
    has name: str;
    has gpa: float;
}

edge EnrolledIn {
    has semester: str;
}

withentry {
    mit: University = University(name="MIT", location="Cambridge, MA");
    alice: Student = Student(name="Alice Johnson", gpa=3.9);
    bob: Student = Student(name="Bob Smith", gpa=3.7);
    
    # Create enrollment relationships
    alice +>:EnrolledIn(semester="Fall 2024"):+> mit;
    bob +>:EnrolledIn(semester="Fall 2024"):+> mit;
    
    # Connect to root for querying
    alice <-: connected_to :-> `root;
    bob <-: connected_to :-> `root;
    mit <-: connected_to :-> `root;
    
    print("=== Advanced Graph Queries ===");
    
    # Query high-GPA students
    high_performers = [alice->:(?Student:gpa>3.8)];
    print(f"High performers: {len(high_performers)} students");
    
    for student in high_performers {
        print(f"- {student.name} (GPA: {student.gpa})");
    }
}''',
                'description': 'Complex graph structures and advanced querying'
            }
        ]

    def get_module3_lessons(self):
        return [
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

## Design Patterns in JAC

JAC supports various design patterns including Factory, Observer, and Strategy patterns.

Ready to learn about advanced OSP operations? Let's continue!''',
                'duration': 60
            }
        ]

    def get_module3_assessments(self):
        return [
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
                        'explanation': 'JAC supports multiple inheritance by listing parent classes separated by commas: node Child(Parent1, Parent2).'
                    }
                ]
            }
        ]

    # Module 4: AI Integration Content
    def get_module4_content(self):
        return '''# Module 4: AI Integration with JAC

Harness the power of artificial intelligence in your JAC applications! This module covers JAC's advanced AI capabilities.

## What You'll Learn

- **byLLM Framework**: JAC's revolutionary AI integration system
- **AI Functions**: Create AI-powered functions with zero prompt engineering
- **Decorators**: Enhance functions with timing, caching, and error handling
- **Async Programming**: Handle concurrent AI operations efficiently
- **Multimodal AI**: Work with text, images, and audio

## The AI-First Paradigm

JAC is designed for the AI era with type-safe AI integration and automatic prompt optimization.

Ready to build AI-powered applications? Let's dive in!'''

    def get_module4_code_examples(self):
        return [
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
        ]

    def get_module4_lessons(self):
        return [
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
        ]

    def get_module4_assessments(self):
        return [
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
        ]

    # Module 5: Production Applications Content
    def get_module5_content(self):
        return '''# Module 5: Production Applications

Build robust, scalable, production-ready applications with JAC! This final module covers deployment, security, and performance optimization.

## What You'll Learn

- **Multi-User Architecture**: Design systems for multiple users with proper permissions
- **Deployment Strategies**: Deploy JAC applications to various environments
- **Performance Optimization**: Scale your applications for production workloads
- **Security Best Practices**: Implement robust security measures
- **Monitoring and Logging**: Track application health and performance

## Production-Ready Patterns

This module covers enterprise-grade patterns for building scalable systems.

Ready to build production-ready applications? Let's make it happen!'''

    def get_module5_code_examples(self):
        return [
            {
                'title': 'Multi-User Architecture with Permissions',
                'code': '''# Multi-user architecture with role-based permissions
node User {
    has username: str;
    has email: str;
    has role: str = "student";
    has is_active: bool = true;
    
    can has_permission(permission: str) -> bool {
        role_permissions: dict[str, list[str]] = {
            "admin": ["*"],  # All permissions
            "instructor": ["read_courses", "grade_assignments"],
            "student": ["read_courses", "submit_assignments"],
            "guest": ["read_public_content"]
        };
        
        user_permissions: list[str] = role_permissions.get(self.role, []);
        return ("*" in user_permissions) or (permission in user_permissions);
    }
}

withentry {
    print("=== Multi-User Architecture Demo ===");
    
    admin: User = User(username="admin", email="admin@school.edu", role="admin");
    student: User = User(username="alice", email="alice@student.edu", role="student");
    
    print(f"Admin can grade: {admin.has_permission("grade_assignments")}");
    print(f"Student can grade: {student.has_permission("grade_assignments")}");
    
    print("\\n=== Demo Complete ===");
}''',
                'description': 'Multi-user architecture with role-based permissions'
            }
        ]

    def get_module5_lessons(self):
        return [
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
        ]

    def get_module5_assessments(self):
        return [
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
                        'text': 'What are the key components of a secure multi-user architecture?',
                        'type': 'essay',
                        'difficulty': 'advanced',
                        'points': 10.0,
                        'correct_answer': {'response': '''A secure multi-user architecture should include:

1. **User Management**: User nodes with proper authentication and roles
2. **Role-Based Access Control (RBAC)**: Role nodes with permissions
3. **Authentication Service**: Credential validation and session management
4. **Authorization Service**: Permission checking and access control
5. **Input Validation**: Schema validation and sanitization
6. **Session Management**: Secure session creation and validation
7. **Audit Logging**: Comprehensive activity logging
8. **Rate Limiting**: Protection against abuse
9. **Data Protection**: Encryption and secure data handling
10. **Security Headers**: CORS, CSP, and other security headers

These components work together to provide a robust foundation for multi-user applications.'''},
                        'explanation': 'This tests understanding of complete security architecture for production applications.'
                    }
                ]
            }
        ]
