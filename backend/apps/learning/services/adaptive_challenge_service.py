# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Adaptive Challenge Generation Service

Uses AI agents to generate personalized challenges based on user difficulty profiles
and performance history for optimal learning outcomes.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from ..models import (
    UserDifficultyProfile, AdaptiveChallenge, UserChallengeAttempt, 
    SpacedRepetitionSession, UserModuleProgress, Module
)
# Removed Google dependency - using local implementation
# from ...agents.ai_multi_agent_system import get_multi_agent_system

User = get_user_model()


class AdaptiveChallengeService:
    """
    Service for generating and managing adaptive challenges using AI.
    """
    
    def __init__(self):
        # Using local AI service instead of Google dependency
        self.multi_agent_system = None
    
    async def generate_personalized_challenge(self, user_id: str, challenge_type: str = None, 
                                           specific_topic: str = None) -> Dict[str, Any]:
        """
        Generate a personalized challenge for a user based on their difficulty profile.
        """
        try:
            # Get user and difficulty profile
            user = User.objects.get(id=user_id)
            
            # Ensure user has a difficulty profile
            difficulty_profile, created = UserDifficultyProfile.objects.get_or_create(
                user=user,
                defaults={
                    'current_difficulty': 'beginner',
                    'jac_knowledge_level': 1,
                    'problem_solving_level': 1,
                    'coding_skill_level': 1
                }
            )
            
            # Determine challenge parameters
            challenge_params = self._determine_challenge_parameters(difficulty_profile, challenge_type, specific_topic)
            
            # Generate challenge content using AI
            challenge_content = await self._generate_challenge_content(challenge_params)
            
            # Create the challenge record
            challenge = AdaptiveChallenge.objects.create(
                title=challenge_content['title'],
                description=challenge_content['description'],
                challenge_type=challenge_params['challenge_type'],
                content=json.dumps(challenge_content['content']),
                difficulty_level=difficulty_profile.current_difficulty,
                skill_dimensions=challenge_params['skill_dimensions'],
                estimated_time=challenge_content['estimated_time'],
                generated_by_agent='content_generator',
                generation_prompt=challenge_params['generation_prompt'],
                adaptation_rules=challenge_params['adaptation_rules'],
                created_by=user
            )
            
            # Create initial attempt record
            attempt = UserChallengeAttempt.objects.create(
                user=user,
                challenge=challenge,
                status='started'
            )
            
            return {
                'success': True,
                'challenge': {
                    'id': str(challenge.id),
                    'title': challenge.title,
                    'description': challenge.description,
                    'challenge_type': challenge.challenge_type,
                    'difficulty_level': challenge.difficulty_level,
                    'content': challenge_content['content'],
                    'estimated_time': challenge.estimated_time,
                    'skill_dimensions': challenge.skill_dimensions,
                },
                'attempt_id': str(attempt.id),
                'personalization': {
                    'difficulty_level': difficulty_profile.current_difficulty,
                    'skill_levels': {
                        'jac_knowledge': difficulty_profile.jac_knowledge_level,
                        'problem_solving': difficulty_profile.problem_solving_level,
                        'coding_skill': difficulty_profile.coding_skill_level
                    },
                    'recent_accuracy': difficulty_profile.recent_accuracy,
                    'success_streak': difficulty_profile.success_streak
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _determine_challenge_parameters(self, difficulty_profile: UserDifficultyProfile, 
                                      challenge_type: str = None, specific_topic: str = None) -> Dict[str, Any]:
        """
        Determine challenge parameters based on user profile and preferences.
        """
        # Determine challenge type if not specified
        if not challenge_type:
            challenge_type = self._select_challenge_type(difficulty_profile)
        
        # Determine skill dimensions to target
        skill_dimensions = self._determine_skill_dimensions(difficulty_profile)
        
        # Create generation prompt
        generation_prompt = self._build_generation_prompt(
            difficulty_profile, challenge_type, skill_dimensions, specific_topic
        )
        
        # Define adaptation rules
        adaptation_rules = {
            'difficulty_adjustment': {
                'increase_threshold': 0.8,
                'decrease_threshold': 0.4,
                'max_difficulty': 'expert'
            },
            'time_estimation': {
                'base_minutes': 15,
                'difficulty_multiplier': 0.2
            },
            'feedback_requirements': [
                'encouragement',
                'specific_guidance',
                'next_steps'
            ]
        }
        
        return {
            'challenge_type': challenge_type,
            'skill_dimensions': skill_dimensions,
            'generation_prompt': generation_prompt,
            'adaptation_rules': adaptation_rules,
            'user_profile': {
                'difficulty_level': difficulty_profile.current_difficulty,
                'jac_knowledge_level': difficulty_profile.jac_knowledge_level,
                'problem_solving_level': difficulty_profile.problem_solving_level,
                'coding_skill_level': difficulty_profile.coding_skill_level,
                'recent_accuracy': difficulty_profile.recent_accuracy,
                'success_streak': difficulty_profile.success_streak
            }
        }
    
    def _select_challenge_type(self, difficulty_profile: UserDifficultyProfile) -> str:
        """
        Select appropriate challenge type based on user profile.
        """
        # Get recent performance data
        recent_attempts = UserChallengeAttempt.objects.filter(
            user=difficulty_profile.user
        ).order_by('-started_at')[:5]
        
        performance_trends = []
        for attempt in recent_attempts:
            if attempt.score is not None:
                performance_trends.append(attempt.score)
        
        avg_performance = sum(performance_trends) / len(performance_trends) if performance_trends else 0.5
        
        # Select challenge type based on performance and skill levels
        if difficulty_profile.coding_skill_level < 3:
            return 'quiz'  # Focus on conceptual understanding
        elif avg_performance > 0.8:
            return 'coding'  # Ready for coding challenges
        elif avg_performance < 0.4:
            return 'scenario'  # Easier conceptual scenarios
        else:
            return 'debug'  # Debugging challenges for skill building
    
    def _determine_skill_dimensions(self, difficulty_profile: UserDifficultyProfile) -> Dict[str, int]:
        """
        Determine which skill dimensions to target in the challenge.
        """
        # Focus on the weakest areas
        skill_levels = {
            'jac_concepts': difficulty_profile.jac_knowledge_level,
            'problem_solving': difficulty_profile.problem_solving_level,
            'coding_practice': difficulty_profile.coding_skill_level
        }
        
        # Return skill dimensions sorted by weakest first
        return dict(sorted(skill_levels.items(), key=lambda x: x[1]))
    
    def _build_generation_prompt(self, difficulty_profile: UserDifficultyProfile, 
                               challenge_type: str, skill_dimensions: Dict[str, int], 
                               specific_topic: str = None) -> str:
        """
        Build a comprehensive prompt for AI challenge generation.
        """
        prompt = f"""
You are an expert JAC programming educator creating a personalized challenge.

**User Profile:**
- Current difficulty: {difficulty_profile.current_difficulty}
- JAC knowledge level: {difficulty_profile.jac_knowledge_level}/10
- Problem solving level: {difficulty_profile.problem_solving_level}/10
- Coding skill level: {difficulty_profile.coding_skill_level}/10
- Recent accuracy: {difficulty_profile.recent_accuracy:.1%}
- Success streak: {difficulty_profile.success_streak} correct answers

**Challenge Requirements:**
- Type: {challenge_type}
- Target skills: {', '.join(skill_dimensions.keys())}
- {"Specific topic: " + specific_topic if specific_topic else "No specific topic requested"}
- Difficulty should be {difficulty_profile.current_difficulty} level

**Generation Instructions:**
1. Create a {challenge_type} challenge appropriate for {difficulty_profile.current_difficulty} level
2. Focus on the weakest skill areas first
3. Make it challenging but achievable (success rate should be 60-80%)
4. Include clear instructions and examples
5. Provide constructive feedback mechanisms
6. Ensure the challenge is specific to JAC programming concepts

**Output Format:**
Return a JSON object with:
- title: Engaging challenge title
- description: Clear challenge description
- content: The actual challenge content (can include multiple choice questions, coding problems, scenarios, etc.)
- estimated_time: Time in minutes to complete (15-30 minutes)
- learning_objectives: What the student will learn
- hints: Optional helpful hints
- solution_approach: How to approach the challenge

Make this challenge both educational and engaging for JAC programming students.
"""
        return prompt
    
    async def _generate_challenge_content(self, challenge_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate challenge content using the AI multi-agent system.
        """
        try:
            # Use the content generator agent
            request_data = {
                'user_id': 'system',  # System request
                'message': challenge_params['generation_prompt'],
                'agent_type': 'content_generator',
                'context': {
                    'challenge_type': challenge_params['challenge_type'],
                    'difficulty_level': challenge_params['user_profile']['difficulty_level']
                }
            }
            
            # Use local AI service instead of Google
            response = await self._process_local_request(request_data)
            
            if response['success']:
                # Parse the AI response to extract challenge content
                ai_content = response['response']
                return self._parse_ai_response(ai_content, challenge_params)
            else:
                # Fallback to a basic challenge structure
                return self._create_fallback_challenge(challenge_params)
                
        except Exception as e:
            # Fallback to basic challenge on error
            return self._create_fallback_challenge(challenge_params)
    
    def _parse_ai_response(self, ai_response: str, challenge_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse AI response and extract structured challenge content.
        """
        # Try to extract JSON from the response
        try:
            # Look for JSON blocks in the response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                content = json.loads(json_match.group())
            else:
                # If no JSON found, create structured content from the response
                content = self._structure_text_response(ai_response, challenge_params)
            
            # Validate and enhance the content
            return self._validate_and_enhance_content(content, challenge_params)
            
        except Exception as e:
            # Fallback to text-based structure
            return self._structure_text_response(ai_response, challenge_params)
    
    def _structure_text_response(self, text: str, challenge_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure a text response into challenge format.
        """
        # Basic fallback structure
        difficulty = challenge_params['user_profile']['difficulty_level']
        challenge_type = challenge_params['challenge_type']
        
        return {
            'title': f'JAC {difficulty.title()} {challenge_type.title()} Challenge',
            'description': f'A {difficulty} level {challenge_type} challenge focused on JAC programming concepts.',
            'content': {
                'type': challenge_type,
                'instructions': text[:500] + '...' if len(text) > 500 else text,
                'questions': self._generate_basic_questions(challenge_params),
                'requirements': 'Complete all parts of the challenge to demonstrate understanding.'
            },
            'estimated_time': 20,
            'learning_objectives': [
                f'Improve {difficulty} level JAC programming skills',
                'Practice problem-solving techniques',
                'Build coding confidence'
            ],
            'hints': [
                'Take your time to read carefully',
                'Think step by step',
                'Use JAC documentation as reference'
            ],
            'solution_approach': 'Break down the problem into smaller parts and solve each systematically.'
        }
    
    def _validate_and_enhance_content(self, content: Dict[str, Any], challenge_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and enhance challenge content with required fields.
        """
        required_fields = ['title', 'description', 'content', 'estimated_time']
        
        # Ensure all required fields are present
        for field in required_fields:
            if field not in content:
                if field == 'title':
                    content[field] = f"JAC {challenge_params['user_profile']['difficulty_level'].title()} Challenge"
                elif field == 'description':
                    content[field] = f"A {challenge_params['challenge_type']} challenge for JAC programming practice."
                elif field == 'content':
                    content[field] = {'type': challenge_params['challenge_type'], 'instructions': 'Complete this challenge.'}
                elif field == 'estimated_time':
                    content[field] = 20
        
        # Set reasonable defaults for optional fields
        if 'learning_objectives' not in content:
            content['learning_objectives'] = ['Practice JAC programming concepts', 'Improve problem-solving skills']
        
        if 'hints' not in content:
            content['hints'] = ['Read carefully', 'Think systematically', 'Practice regularly']
        
        if 'solution_approach' not in content:
            content['solution_approach'] = 'Analyze the problem, break it down, and solve step by step.'
        
        return content
    
    def _generate_basic_questions(self, challenge_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate basic questions for the challenge.
        """
        difficulty = challenge_params['user_profile']['difficulty_level']
        skill_levels = challenge_params['user_profile']
        
        questions = []
        
        # Generate different question types based on difficulty and skills
        if challenge_params['challenge_type'] == 'quiz':
            questions = [
                {
                    'type': 'multiple_choice',
                    'question': f'Which JAC concept is most important for {difficulty} level programming?',
                    'options': ['Object creation', 'Data manipulation', 'Method execution', 'Memory management'],
                    'correct_answer': 0
                },
                {
                    'type': 'multiple_choice',
                    'question': 'What is the primary benefit of JAC programming?',
                    'options': ['Faster execution', 'Simpler syntax', 'Better organization', 'Lower memory usage'],
                    'correct_answer': 2
                }
            ]
        elif challenge_params['challenge_type'] == 'coding':
            questions = [
                {
                    'type': 'coding',
                    'question': f'Write a simple JAC program that demonstrates {difficulty} level concepts.',
                    'instructions': 'Create a basic program using JAC syntax.',
                    'starter_code': '// Start your JAC code here',
                    'test_cases': ['Program should compile', 'Should demonstrate basic concepts']
                }
            ]
        
        return questions
    
    async def _process_local_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process request using local AI service instead of Google
        """
        try:
            agent_type = request_data.get('agent_type', 'content_generator')
            message = request_data.get('message', '')
            
            # Generate response based on agent type
            if agent_type == 'content_generator':
                return self._generate_challenge_content_locally(message, request_data)
            elif agent_type == 'learning_assistant':
                return self._generate_feedback_locally(message, request_data)
            else:
                # Default content generation
                return {
                    'success': True,
                    'response': self._generate_default_response(message, agent_type)
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_challenge_content_locally(self, message: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate challenge content using local AI logic
        """
        try:
            context = request_data.get('context', {})
            challenge_type = context.get('challenge_type', 'quiz')
            difficulty_level = context.get('difficulty_level', 'beginner')
            
            # Generate content based on type and difficulty
            if challenge_type == 'quiz':
                content = self._generate_quiz_content(difficulty_level)
            elif challenge_type == 'coding':
                content = self._generate_coding_content(difficulty_level)
            elif challenge_type == 'debug':
                content = self._generate_debug_content(difficulty_level)
            else:
                content = self._generate_general_content(difficulty_level)
            
            return {
                'success': True,
                'response': json.dumps(content)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Content generation error: {str(e)}'
            }
    
    def _generate_feedback_locally(self, message: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate feedback using local AI logic
        """
        try:
            context = request_data.get('context', {})
            user_score = context.get('user_score', 0.5)
            difficulty_level = context.get('difficulty_level', 'beginner')
            
            feedback = self._generate_basic_feedback(user_score, difficulty_level)
            
            return {
                'success': True,
                'response': feedback
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Feedback generation error: {str(e)}'
            }
    
    def _generate_default_response(self, message: str, agent_type: str) -> str:
        """
        Generate default response for unknown agent types
        """
        return f"Generated response for {agent_type} based on request: {message[:100]}..."
    
    def _generate_quiz_content(self, difficulty_level: str) -> Dict[str, Any]:
        """
        Generate quiz content locally
        """
        questions = []
        
        if difficulty_level == 'beginner':
            questions = [
                {
                    'type': 'multiple_choice',
                    'question': 'What is the main purpose of JAC programming?',
                    'options': ['Network communication', 'Graph-based programming', 'Database management', 'Web development'],
                    'correct_answer': 1
                },
                {
                    'type': 'multiple_choice',
                    'question': 'Which component is fundamental to JAC programming?',
                    'options': ['Walker', 'Node', 'Edge', 'All of the above'],
                    'correct_answer': 3
                }
            ]
        elif difficulty_level == 'intermediate':
            questions = [
                {
                    'type': 'multiple_choice',
                    'question': 'How do you create a new walker in JAC?',
                    'options': ['walker = new Walker()', 'can walker spawn', 'create walker', 'spawn walker'],
                    'correct_answer': 1
                },
                {
                    'type': 'multiple_choice',
                    'question': 'What does the `can` keyword represent in JAC?',
                    'options': ['Class definition', 'Ability/behavior', 'Variable declaration', 'Function call'],
                    'correct_answer': 1
                }
            ]
        else:  # advanced
            questions = [
                {
                    'type': 'multiple_choice',
                    'question': 'What is the primary advantage of using walkers in JAC?',
                    'options': ['Memory efficiency', 'Parallel processing', 'Code simplicity', 'Debugging capabilities'],
                    'correct_answer': 1
                },
                {
                    'type': 'multiple_choice',
                    'question': 'How does JAC handle graph traversal compared to traditional programming?',
                    'options': ['Recursive functions', 'Built-in walkers', 'Iterative loops', 'Callback functions'],
                    'correct_answer': 1
                }
            ]
        
        return {
            'title': f'JAC {difficulty_level.title()} Quiz Challenge',
            'description': f'Test your JAC {difficulty_level} level programming knowledge.',
            'content': {
                'type': 'quiz',
                'questions': questions,
                'instructions': 'Answer all questions to the best of your ability.'
            },
            'estimated_time': 15,
            'learning_objectives': [
                f'Assess JAC {difficulty_level} programming concepts',
                'Practice problem-solving skills',
                'Build confidence in JAC understanding'
            ]
        }
    
    def _generate_coding_content(self, difficulty_level: str) -> Dict[str, Any]:
        """
        Generate coding challenge content locally
        """
        if difficulty_level == 'beginner':
            challenge = """
            Create a simple JAC program that:
            1. Creates a walker
            2. Has the walker move between two nodes
            3. Prints a message when it reaches the destination
            """
            starter_code = """
            // JAC Beginner Coding Challenge
            node: my_start;
            node: my_destination;
            
            walker my_walker {
                can {
                    // Add your movement logic here
                }
            }
            """
        elif difficulty_level == 'intermediate':
            challenge = """
            Create a JAC program that:
            1. Creates multiple walkers
            2. Implements a simple graph traversal algorithm
            3. Tracks the number of nodes visited
            4. Reports the final count
            """
            starter_code = """
            // JAC Intermediate Coding Challenge
            node: start_node;
            node: mid_node_1;
            node: mid_node_2;
            node: end_node;
            
            edge: start_node -> mid_node_1;
            edge: start_node -> mid_node_2;
            edge: mid_node_1 -> end_node;
            edge: mid_node_2 -> end_node;
            
            walker: my_walker {
                can {
                    // Implement graph traversal with counting
                }
            }
            """
        else:  # advanced
            challenge = """
            Create an advanced JAC program that:
            1. Implements a pathfinding algorithm
            2. Handles dynamic graph modifications
            3. Uses multiple walker types for different tasks
            4. Optimizes for shortest path
            """
            starter_code = """
            // JAC Advanced Coding Challenge
            // Implement pathfinding with multiple walker types
            
            walker: pathfinder {
                can {
                    // Advanced pathfinding logic
                }
            }
            
            walker: explorer {
                can {
                    // Dynamic graph exploration
                }
            }
            """
        
        return {
            'title': f'JAC {difficulty_level.title()} Coding Challenge',
            'description': f'Solve a {difficulty_level} level JAC programming challenge.',
            'content': {
                'type': 'coding',
                'challenge': challenge,
                'starter_code': starter_code,
                'instructions': 'Complete the code to meet the challenge requirements.'
            },
            'estimated_time': 25,
            'learning_objectives': [
                f'Practice JAC {difficulty_level} programming skills',
                'Apply programming concepts practically',
                'Develop problem-solving abilities'
            ]
        }
    
    def _generate_debug_content(self, difficulty_level: str) -> Dict[str, Any]:
        """
        Generate debugging challenge content locally
        """
        if difficulty_level == 'beginner':
            buggy_code = """
            // JAC Beginner Debug Challenge - Find the errors!
            node: start;
            node: finish;
            
            walker: debug_walker {
                can {
                    start -> finish;  // Error: missing edge definition
                    return "Reached destination";
                }
            }
            """
            expected_errors = [
                "Missing edge definition between start and finish nodes",
                "Improper syntax for node traversal"
            ]
        elif difficulty_level == 'intermediate':
            buggy_code = """
            // JAC Intermediate Debug Challenge
            node: A, B, C;
            
            edge: A -> B;
            edge: B -> C;  // Error: edge goes wrong direction
            
            walker: my_walker {
                can {
                    A -> C;  // Error: no direct edge A->C
                    exit;
                }
            }
            """
            expected_errors = [
                "Incorrect edge direction",
                "Attempting to traverse non-existent edge"
            ]
        else:  # advanced
            buggy_code = """
            // JAC Advanced Debug Challenge
            walker: advanced_walker {
                can {
                    // Multiple logical errors in algorithm
                    if (node_exists(target)) {
                        path = shortest_path(current, target);  // Error: function might not exist
                        walker.spawn(path[0]);  // Error: incorrect walker spawning
                        return SUCCESS;
                    }
                }
            }
            """
            expected_errors = [
                "Potential undefined function calls",
                "Incorrect walker spawning syntax",
                "Missing error handling"
            ]
        
        return {
            'title': f'JAC {difficulty_level.title()} Debug Challenge',
            'description': f'Find and fix the bugs in this {difficulty_level} level JAC code.',
            'content': {
                'type': 'debug',
                'buggy_code': buggy_code,
                'expected_errors': expected_errors,
                'instructions': 'Identify the errors and provide corrected code.'
            },
            'estimated_time': 20,
            'learning_objectives': [
                f'Develop debugging skills at {difficulty_level} level',
                'Practice code analysis',
                'Improve error detection abilities'
            ]
        }
    
    def _generate_general_content(self, difficulty_level: str) -> Dict[str, Any]:
        """
        Generate general challenge content
        """
        return {
            'title': f'JAC {difficulty_level.title()} Challenge',
            'description': f'A {difficulty_level} level JAC programming challenge.',
            'content': {
                'type': 'general',
                'instructions': f'Complete this {difficulty_level} level JAC programming challenge.',
                'requirements': 'Demonstrate your understanding of JAC programming concepts.'
            },
            'estimated_time': 20,
            'learning_objectives': [
                f'Practice {difficulty_level} level JAC concepts',
                'Apply programming knowledge',
                'Build confidence'
            ]
        }
    
    def _create_fallback_challenge(self, challenge_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a basic fallback challenge when AI generation fails.
        """
        difficulty = challenge_params['user_profile']['difficulty_level']
        challenge_type = challenge_params['challenge_type']
        
        return {
            'title': f'JAC {difficulty.title()} Practice - {challenge_type.title()}',
            'description': f'A {difficulty} level {challenge_type} challenge for JAC programming practice.',
            'content': {
                'type': challenge_type,
                'instructions': f'Complete this {challenge_type} challenge focusing on JAC programming concepts suitable for {difficulty} level learners.',
                'main_task': 'Demonstrate your understanding of JAC programming through this practical exercise.',
                'questions': self._generate_basic_questions(challenge_params)
            },
            'estimated_time': 20,
            'learning_objectives': [
                'Practice JAC programming syntax',
                'Improve problem-solving skills',
                'Build programming confidence'
            ],
            'hints': [
                'Review JAC documentation',
                'Start with simple concepts',
                'Practice regularly'
            ],
            'solution_approach': 'Break down the challenge into smaller parts and solve each systematically.'
        }
    
    async def submit_challenge_response(self, attempt_id: str, responses: Dict[str, Any], 
                                      feedback: str = None) -> Dict[str, Any]:
        """
        Process user responses to a challenge and provide adaptive feedback.
        """
        try:
            attempt = UserChallengeAttempt.objects.get(id=attempt_id)
            
            # Calculate score based on responses
            score = self._calculate_challenge_score(attempt.challenge, responses)
            
            # Generate AI feedback if not provided
            if not feedback:
                feedback = await self._generate_feedback(attempt, responses, score)
            
            # Complete the attempt
            final_score = attempt.complete_attempt(score, responses, feedback)
            
            # Check if spaced repetition session should be created
            await self._schedule_spaced_repetition(attempt.user, attempt.challenge, final_score)
            
            return {
                'success': True,
                'score': final_score,
                'feedback': feedback,
                'next_steps': self._generate_next_steps(attempt.user, attempt.challenge, final_score),
                'difficulty_adjustment': self._get_difficulty_adjustment_summary(attempt.user)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_challenge_score(self, challenge: AdaptiveChallenge, responses: Dict[str, Any]) -> float:
        """
        Calculate score based on user responses and challenge type.
        """
        if challenge.challenge_type == 'quiz':
            return self._calculate_quiz_score(challenge, responses)
        elif challenge.challenge_type == 'coding':
            return self._calculate_coding_score(challenge, responses)
        elif challenge.challenge_type == 'debug':
            return self._calculate_debug_score(challenge, responses)
        else:
            return self._calculate_general_score(challenge, responses)
    
    def _calculate_quiz_score(self, challenge: AdaptiveChallenge, responses: Dict[str, Any]) -> float:
        """
        Calculate score for quiz-type challenges.
        """
        content = json.loads(challenge.content)
        questions = content.get('questions', [])
        
        if not questions:
            return 0.5  # Default score
        
        correct_answers = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            question_key = f'question_{i}'
            if question_key in responses:
                user_answer = responses[question_key]
                correct_answer = question.get('correct_answer')
                
                if user_answer == correct_answer:
                    correct_answers += 1
        
        return correct_answers / total_questions if total_questions > 0 else 0.5
    
    def _calculate_coding_score(self, challenge: AdaptiveChallenge, responses: Dict[str, Any]) -> float:
        """
        Calculate score for coding challenges.
        """
        # For coding challenges, evaluate based on code quality and completeness
        code = responses.get('code', '')
        
        if not code:
            return 0.0
        
        # Basic scoring criteria
        score = 0.5  # Base score for attempting
        
        # Check for basic JAC syntax elements
        jac_keywords = ['walker', 'node', 'edge', 'graph', 'can', 'spawn']
        found_keywords = sum(1 for keyword in jac_keywords if keyword.lower() in code.lower())
        score += min(found_keywords * 0.1, 0.3)
        
        # Check for comments/documentation
        if '//' in code or '/*' in code:
            score += 0.1
        
        # Check for proper structure
        if '{' in code and '}' in code:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_debug_score(self, challenge: AdaptiveChallenge, responses: Dict[str, Any]) -> float:
        """
        Calculate score for debugging challenges.
        """
        # Similar to coding but with debugging-specific criteria
        return self._calculate_coding_score(challenge, responses) * 0.9  # Slightly lower due to debugging difficulty
    
    def _calculate_general_score(self, challenge: AdaptiveChallenge, responses: Dict[str, Any]) -> float:
        """
        Calculate score for other challenge types.
        """
        # General scoring based on response completeness and quality
        if not responses:
            return 0.0
        
        # Check if responses contain meaningful content
        meaningful_responses = sum(1 for v in responses.values() if v and len(str(v).strip()) > 10)
        total_responses = len(responses)
        
        if total_responses == 0:
            return 0.5
        
        base_score = meaningful_responses / total_responses
        return min(base_score + 0.2, 1.0)  # Bonus for participation
    
    async def _generate_feedback(self, attempt: UserChallengeAttempt, responses: Dict[str, Any], 
                               score: float) -> str:
        """
        Generate personalized feedback using AI.
        """
        try:
            user_profile = attempt.user.difficulty_profile
            
            feedback_prompt = f"""
Generate personalized feedback for a JAC programming challenge completion.

**Challenge Details:**
- Type: {attempt.challenge.challenge_type}
- Difficulty: {attempt.challenge.difficulty_level}
- User Score: {score:.1%}

**User Profile:**
- Current difficulty level: {user_profile.current_difficulty}
- Success streak: {user_profile.success_streak}
- Recent accuracy: {user_profile.recent_accuracy:.1%}

**Performance Analysis:**
- Score: {score:.1%}
- {"Excellent performance!" if score >= 0.8 else "Good effort!" if score >= 0.6 else "Room for improvement" if score >= 0.4 else "Keep practicing"}
- User responses: {json.dumps(responses, indent=2)}

**Feedback Requirements:**
1. Provide encouraging and constructive feedback
2. Highlight strengths in the performance
3. Suggest specific areas for improvement
4. Recommend next steps for learning
5. Match the tone to the user's current skill level
6. Keep feedback concise but meaningful (2-3 paragraphs)

Please generate thoughtful, personalized feedback that motivates continued learning.
"""
            
            request_data = {
                'user_id': 'system',
                'message': feedback_prompt,
                'agent_type': 'learning_assistant',
                'context': {
                    'user_score': score,
                    'difficulty_level': user_profile.current_difficulty
                }
            }
            
            # Use local AI service instead of Google
            response = await self._process_local_request(request_data)
            
            if response['success']:
                return response['response']
            else:
                return self._generate_basic_feedback(score, user_profile.current_difficulty)
                
        except Exception as e:
            return self._generate_basic_feedback(score, 'beginner')
    
    def _generate_basic_feedback(self, score: float, difficulty_level: str) -> str:
        """
        Generate basic feedback when AI generation fails.
        """
        if score >= 0.8:
            feedback = f"Excellent work! You've demonstrated strong understanding at the {difficulty_level} level. "
            feedback += "Your performance shows good grasp of JAC programming concepts. "
            feedback += "Consider taking on more challenging exercises to continue growing your skills."
        elif score >= 0.6:
            feedback = f"Good job! You're making solid progress at the {difficulty_level} level. "
            feedback += "Your understanding of JAC concepts is developing well. "
            feedback += "Keep practicing to strengthen your skills and build confidence."
        elif score >= 0.4:
            feedback = f"Nice effort! You're learning at the {difficulty_level} level. "
            feedback += "Don't worry if some concepts are challenging - that's part of learning. "
            feedback += "Review the material and try again. You're on the right track!"
        else:
            feedback = f"Learning takes time, especially at the {difficulty_level} level. "
            feedback += "Don't be discouraged - every step forward is progress. "
            feedback += "Consider reviewing the basics and trying again with smaller, focused challenges."
        
        return feedback
    
    def _schedule_spaced_repetition(self, user: User, challenge: AdaptiveChallenge, score: float):
        """
        Schedule spaced repetition sessions based on performance.
        """
        # Only schedule for good performances (score >= 0.6)
        if score < 0.6:
            return
        
        # Check if a session already exists for this challenge
        existing_session = SpacedRepetitionSession.objects.filter(
            user=user,
            challenge=challenge
        ).first()
        
        if existing_session:
            # Update existing session
            if score >= 0.8:
                existing_session.mark_as_ready()
            return
        
        # Create new spaced repetition session
        session = SpacedRepetitionSession.objects.create(
            user=user,
            challenge=challenge,
            scheduled_for=timezone.now() + timedelta(days=1),  # First review in 1 day
            status='scheduled'
        )
        
        return session
    
    def _generate_next_steps(self, user: User, challenge: AdaptiveChallenge, score: float) -> List[str]:
        """
        Generate personalized next steps for continued learning.
        """
        steps = []
        
        # Difficulty-based recommendations
        if score >= 0.8:
            steps.append("Challenge yourself with more advanced JAC concepts")
            steps.append("Try complex debugging exercises")
            steps.append("Work on mini-projects to apply your skills")
        elif score >= 0.6:
            steps.append("Continue practicing with similar difficulty challenges")
            steps.append("Review any concepts that felt challenging")
            steps.append("Explore related JAC programming topics")
        else:
            steps.append("Review the basic JAC concepts covered in this challenge")
            steps.append("Try easier challenges to build confidence")
            steps.append("Practice with simpler coding exercises")
        
        # Skill-specific recommendations
        user_profile = user.difficulty_profile
        if user_profile.jac_knowledge_level < 3:
            steps.append("Focus on understanding JAC syntax and basic concepts")
        if user_profile.problem_solving_level < 3:
            steps.append("Practice breaking down problems into smaller steps")
        if user_profile.coding_skill_level < 3:
            steps.append("Work on basic JAC coding exercises")
        
        return steps
    
    def _get_difficulty_adjustment_summary(self, user: User) -> Dict[str, Any]:
        """
        Get summary of any difficulty adjustments made for the user.
        """
        if not hasattr(user, 'difficulty_profile'):
            return {'adjusted': False, 'message': 'No difficulty profile found'}
        
        profile = user.difficulty_profile
        
        # Check if difficulty was recently adjusted
        if profile.last_difficulty_change:
            time_since_change = timezone.now() - profile.last_difficulty_change
            
            if time_since_change.days < 1:  # Adjusted within last day
                return {
                    'adjusted': True,
                    'message': f'Your difficulty level has been adjusted to {profile.current_difficulty}',
                    'new_difficulty': profile.current_difficulty,
                    'reason': 'Based on your recent performance'
                }
        
        return {
            'adjusted': False,
            'message': 'Your difficulty level is appropriate for your current performance',
            'current_difficulty': profile.current_difficulty
        }
    
    async def get_due_reviews(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get challenges due for spaced repetition review.
        """
        try:
            user = User.objects.get(id=user_id)
            due_sessions = SpacedRepetitionSession.objects.filter(
                user=user,
                status='ready',
                scheduled_for__lte=timezone.now()
            ).select_related('challenge')
            
            reviews = []
            for session in due_sessions:
                challenge_content = json.loads(session.challenge.content)
                reviews.append({
                    'session_id': str(session.id),
                    'challenge': {
                        'id': str(session.challenge.id),
                        'title': session.challenge.title,
                        'description': session.challenge.description,
                        'challenge_type': session.challenge.challenge_type,
                        'difficulty_level': session.challenge.difficulty_level,
                        'content': challenge_content
                    },
                    'review_stage': session.review_stage,
                    'ease_factor': session.ease_factor,
                    'scheduled_for': session.scheduled_for.isoformat()
                })
            
            return reviews
            
        except Exception as e:
            return []
    
    async def complete_review(self, session_id: str, quality_rating: int) -> Dict[str, Any]:
        """
        Complete a spaced repetition review session.
        """
        try:
            session = SpacedRepetitionSession.objects.get(id=session_id)
            next_review = session.complete_review(quality_rating)
            
            return {
                'success': True,
                'next_review_date': next_review.isoformat(),
                'new_stage': session.review_stage,
                'new_interval': session.interval_days,
                'quality_rating': quality_rating
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }