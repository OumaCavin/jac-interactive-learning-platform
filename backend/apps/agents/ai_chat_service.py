# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
AI Chat Service for JAC Learning Platform
Provides intelligent responses for different agent types based on JAC language content
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from django.contrib.auth.models import User


class JACAIContentProvider:
    """Provides JAC language-specific content and knowledge"""
    
    # JAC Basic Concepts
    BASIC_CONCEPTS = {
        'jac': 'JAC (Jaseci) is a programming language that extends Python with Object-Spatial Programming (OSP) paradigm for handling graph-based data structures naturally.',
        'python': 'JAC is a Python superset, meaning all valid Python code is valid JAC code, but JAC adds additional features for graph operations.',
        'node': 'Nodes are the fundamental entities in JAC graphs. They hold data and can be connected via edges. Think of nodes as objects in a graph structure.',
        'edge': 'Edges connect nodes in JAC, representing relationships. They can be generic (++) or typed (:EdgeType:) with properties.',
        'walker': 'Walkers are autonomous agents that traverse graphs, performing computations. They move from node to node using graph connections.',
        'abilities': 'Abilities are methods defined in nodes or walkers that get triggered during interactions. They can be callable or visit-dependent.',
        'graph': 'A graph is a collection of nodes connected by edges. JAC makes graphs first-class citizens in its type system.',
        'osp': 'Object-Spatial Programming (OSP) shifts from bringing data to computation (traditional OOP) to sending computation to data (traversing graphs).',
        'entry': 'The `with entry` block is like the main() function in C/C++, where code execution begins.',
        'spawn': 'The `spawn` keyword creates and launches walkers onto the graph.',
        'visit': 'Walkers use `visit` to navigate through graph connections and move between nodes.',
        'report': 'Walkers use `report` to send results back while continuing their traversal, unlike return statements.'
    }
    
    # JAC Syntax Patterns
    SYNTAX_EXAMPLES = {
        'variable_declaration': """
        # JAC requires explicit type declarations (strong typing)
        name: str = "Alice"
        age: int = 25
        gpa: float = 3.8
        is_student: bool = True
        """,
        
        'node_definition': """
        # Define a node (like a class with graph capabilities)
        node Person {
            has name: str;
            has age: int;
            has email: str;
            
            def greet -> str {
                return f"Hello, I'm {self.name}!";
            }
        }
        """,
        
        'edge_definition': """
        # Define a typed edge (relationship with properties)
        edge Friend {
            has since: int;  # Year they became friends
            has closeness: int = 5;  # 1-10 scale
            
            def is_close_friend -> bool {
                return self.closeness >= 7;
            }
        }
        """,
        
        'graph_creation': """
        # Create nodes and connect them
        alice = Person(name="Alice", age=25)
        bob = Person(name="Bob", age=30)
        
        # Create typed connections (edges)
        alice +>:Friend(since=2015, closeness=9):+> bob;
        """,
        
        'walker_definition': """
        # Define a walker for graph traversal
        walker GreetFriends {
            has greeting_count: int = 0;
            
            can greet with Person entry {
                print(f"Hello, {here.name}!");
                self.greeting_count += 1;
                visit [-->];  # Visit connected nodes
            }
        }
        """,
        
        'walker_execution': """
        # Launch walker to traverse graph
        with entry {
            # Set up graph
            alice = Person(name="Alice")
            bob = Person(name="Bob") 
            charlie = Person(name="Charlie")
            
            # Connect them
            alice ++> bob ++> charlie;
            
            # Spawn walker to greet everyone
            root spawn GreetFriends();
        }
        """
    }
    
    # Common JAC Questions and Answers
    QNA = {
        'what is jac': 'JAC is a programming language that extends Python with Object-Spatial Programming (OSP) capabilities. It excels at handling graph-based data structures like social networks, knowledge graphs, and AI workflows.',
        'why use jac': 'Use JAC when you need to work with connected data naturally. It simplifies graph operations, provides automatic data persistence, supports multi-user architectures, and scales from single machines to distributed systems.',
        'what is osp': 'Object-Spatial Programming (OSP) is JAC\'s core paradigm where computation moves through spatial relationships in data, rather than bringing data to computation. This is ideal for graph traversal and relationship-heavy applications.',
        'how to define nodes': 'Nodes are defined using the `node` keyword with properties using `has`. For example: `node Person { has name: str; has age: int; }`',
        'how to connect nodes': 'Use spatial operators: `++>` (forward), `<++` (backward), `<++>` (bidirectional). For typed edges: `alice +>:Friend:strength=8:+> bob;`',
        'what are walkers': 'Walkers are autonomous agents that traverse graphs. They carry state and perform actions at nodes they visit. Think of them as "workers" that move through your graph data.',
        'jac vs python': 'JAC is a Python superset - all Python code works in JAC, but JAC adds graph operations, typed edges, walkers, and OSP features. JAC requires explicit type declarations.',
        'getting started': 'Start with: 1) Install Jac with `pip install jac` 2) Learn basic syntax and nodes/edges 3) Practice with simple graphs 4) Try walkers for traversal 5) Build real applications'
    }
    
    # Learning Path Content
    LEARNING_MODULES = {
        'module1': {
            'title': 'JAC Fundamentals',
            'description': 'Basic concepts, syntax, and getting started',
            'topics': ['Installation', 'Basic syntax', 'Variables and types', 'Functions', 'Control flow']
        },
        'module2': {
            'title': 'Object-Spatial Programming',
            'description': 'Understanding OSP paradigm and spatial relationships',
            'topics': ['Nodes and edges', 'Graph creation', 'Spatial operators', 'Relationships', 'Querying graphs']
        },
        'module3': {
            'title': 'Advanced JAC Concepts',
            'description': 'Walkers, abilities, and advanced graph operations',
            'topics': ['Walker classes', 'Graph traversals', 'State management', 'Abilities', 'API endpoints']
        },
        'module4': {
            'title': 'AI Integration',
            'description': 'AI-specific features and integrations',
            'topics': ['AI functions', 'Decorators', 'LLM integration', 'Custom models', 'Agent patterns']
        },
        'module5': {
            'title': 'Production Applications',
            'description': 'Building real-world applications',
            'topics': ['Multi-user systems', 'Cloud deployment', 'Performance optimization', 'Testing', 'Best practices']
        }
    }


class JACAIService:
    """Main AI service for JAC Learning Platform"""
    
    def __init__(self):
        self.content_provider = JACAIContentProvider()
        self.conversation_history = {}  # session_id -> list of exchanges
        
    def process_message(self, message: str, agent_type: str, session_id: str) -> Dict[str, Any]:
        """
        Process user message and generate AI response based on agent type
        """
        # Add to conversation history
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            'type': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat(),
            'agent_type': agent_type
        })
        
        # Generate response based on agent type
        if agent_type == 'content_curator':
            response = self._generate_content_response(message, session_id)
        elif agent_type == 'quiz_master':
            response = self._generate_quiz_response(message, session_id)
        elif agent_type == 'evaluator':
            response = self._generate_evaluation_response(message, session_id)
        elif agent_type == 'progress_tracker':
            response = self._generate_progress_response(message, session_id)
        elif agent_type == 'motivator':
            response = self._generate_motivation_response(message, session_id)
        else:  # system_orchestrator
            response = self._generate_general_response(message, session_id)
        
        # Add AI response to history
        self.conversation_history[session_id].append({
            'type': 'agent',
            'content': response['message'],
            'timestamp': datetime.now().isoformat(),
            'agent_type': agent_type
        })
        
        return {
            'response': response['message'],
            'agent_type': agent_type,
            'suggestions': response.get('suggestions', []),
            'code_examples': response.get('code_examples', []),
            'related_topics': response.get('related_topics', []),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_content_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Content Curator Agent - helps with learning content and resources"""
        message_lower = message.lower()
        
        # Check for concept explanations
        for concept, explanation in self.content_provider.BASIC_CONCEPTS.items():
            if concept in message_lower:
                return {
                    'message': f"**{concept.title()}**: {explanation}\n\nWould you like me to show you some code examples or explain a related concept?",
                    'suggestions': [f"What is {concept}?", f"Show me {concept} code", f"More about {concept}"],
                    'related_topics': [k for k in self.content_provider.BASIC_CONCEPTS.keys() if k != concept][:3]
                }
        
        # Check for syntax examples
        for syntax_type, code in self.content_provider.SYNTAX_EXAMPLES.items():
            if syntax_type.replace('_', ' ') in message_lower or any(word in message_lower for word in syntax_type.split('_')):
                return {
                    'message': f"Here's how to work with **{syntax_type.replace('_', ' ').title()}** in JAC:\n\n```jac\n{code}\n```\n\nThis shows the basic pattern. Would you like me to explain any part in detail or show variations?",
                    'suggestions': [f"Explain {syntax_type}", f"More {syntax_type} examples", f"Practice {syntax_type}"],
                    'code_examples': [code]
                }
        
        # Check for learning path questions
        if 'module' in message_lower or 'lesson' in message_lower or 'curriculum' in message_lower:
            modules_info = "\n".join([
                f"**{key}**: {info['title']} - {info['description']}"
                for key, info in self.content_provider.LEARNING_MODULES.items()
            ])
            return {
                'message': f"Here's the recommended learning path for JAC:\n\n{modules_info}\n\nWould you like me to recommend which module to start with based on your experience?",
                'suggestions': ['What should I start with?', 'How long does each module take?', 'Show module 1 content'],
                'related_topics': list(self.content_provider.LEARNING_MODULES.keys())[:3]
            }
        
        # General learning assistance
        return {
            'message': "I'm your content curator! I can help you with:\n\n• **JAC Concepts**: Ask me about nodes, edges, walkers, OSP, etc.\n• **Code Examples**: Request syntax examples for any topic\n• **Learning Path**: Get recommendations for what to learn next\n• **Resources**: Find the best tutorials and documentation\n\nWhat would you like to explore?",
            'suggestions': ['What is JAC?', 'Show me a code example', 'What should I learn first?'],
            'related_topics': ['jac', 'nodes', 'walkers', 'osp']
        }
    
    def _generate_quiz_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Quiz Master Agent - generates quizzes and assessments"""
        message_lower = message.lower()
        
        # Generate topic-based quiz
        if 'quiz' in message_lower or 'question' in message_lower:
            if 'basic' in message_lower or 'beginner' in message_lower:
                quiz = {
                    'title': 'JAC Fundamentals Quiz',
                    'questions': [
                        {
                            'question': 'What does OSP stand for in JAC?',
                            'options': ['Object-Spatial Programming', 'Object-Structure Processing', 'Optimized Spatial Programming', 'Ordered String Processing'],
                            'correct': 0
                        },
                        {
                            'question': 'Which operator creates a bidirectional edge in JAC?',
                            'options': ['++>', '<++', '<++>', '-->'],
                            'correct': 2
                        },
                        {
                            'question': 'What is a walker in JAC?',
                            'options': ['A type of node', 'An autonomous agent that traverses graphs', 'A function definition', 'A variable type'],
                            'correct': 1
                        }
                    ]
                }
                return {
                    'message': f"Here's a **{quiz['title']}** to test your knowledge:\n\n",
                    'quiz': quiz,
                    'suggestions': ['Give me another quiz', 'Explain the answers', 'More advanced questions'],
                    'related_topics': ['jac', 'walkers', 'nodes', 'edges']
                }
        
        # Generate concept-specific questions
        if 'walker' in message_lower:
            return {
                'message': 'Great topic! Walkers are one of JAC\'s most powerful features. Here\'s a quick assessment:\n\n**Quick Walker Check:**\n1. What do walkers carry while traversing?\n2. How do you start a walker?\n3. What keyword do walkers use to move between nodes?\n\nWould you like me to generate a full quiz on walkers?',
                'suggestions': ['Generate walker quiz', 'Show walker examples', 'Walker vs functions'],
                'related_topics': ['walkers', 'traversal', 'graph', 'navigation']
            }
        
        # General quiz assistance
        return {
            'message': "I'm your quiz master! I can create quizzes on any JAC topic:\n\n• **Concept Quizzes**: Test understanding of nodes, edges, walkers, OSP\n• **Syntax Quizzes**: Practice JAC code patterns and syntax\n• **Practical Quizzes**: Solve real-world problems with JAC\n• **Difficulty Levels**: Beginner, intermediate, or advanced\n\nWhat topic would you like to be quizzed on?",
            'suggestions': ['Quiz on walkers', 'Syntax practice', 'OSP concepts', 'Node and edge operations'],
            'related_topics': ['jac', 'quiz', 'assessment', 'practice']
        }
    
    def _generate_evaluation_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Evaluator Agent - provides code feedback and evaluation"""
        message_lower = message.lower()
        
        # Detect code snippets
        if any(keyword in message_lower for keyword in ['code', 'example', 'syntax', 'does this work']):
            # Extract potential code from message (simplified)
            if 'node' in message_lower:
                feedback = {
                    'status': 'syntax_check',
                    'message': "I can help evaluate your JAC code! I notice you're asking about node-related code. Here's what to check:\n\n**Node Definition Checklist:**\n• Use `node` keyword\n• Define properties with `has`\n• Specify types (str, int, bool, etc.)\n• Close with `}`\n\nWould you like me to review a specific code snippet?",
                    'suggestions': ['Show me proper syntax', 'Check my code', 'Common mistakes'],
                    'related_topics': ['nodes', 'syntax', 'definition']
                }
            else:
                feedback = {
                    'status': 'general_check',
                    'message': "I'd be happy to evaluate your JAC code! Please share your code snippet and I'll check:\n\n• **Syntax**: Correct JAC syntax and structure\n• **Logic**: Proper use of JAC features\n• **Best Practices**: Following JAC conventions\n• **Performance**: Efficient implementation\n\nPaste your code and let me know what specific concerns you have!",
                    'suggestions': ['Check syntax', 'Review logic', 'Performance tips', 'Best practices'],
                    'related_topics': ['syntax', 'best practices', 'code review']
                }
            
            return feedback
        
        # General evaluation assistance
        return {
            'message': "I'm your code evaluator! I can help with:\n\n• **Code Review**: Check your JAC syntax and logic\n• **Debugging**: Find and fix issues in your code\n• **Optimization**: Improve performance and efficiency\n• **Best Practices**: Ensure you're following JAC conventions\n\n**How to get help:**\n1. Share your code snippet\n2. Tell me what you want to achieve\n3. Mention any specific concerns\n\nWhat code would you like me to review?",
            'suggestions': ['Review my code', 'Debug help', 'Optimization tips', 'Best practices'],
            'related_topics': ['code review', 'debugging', 'optimization', 'best practices']
        }
    
    def _generate_progress_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Progress Tracker Agent - monitors learning progress and analytics"""
        message_lower = message.lower()
        
        if 'progress' in message_lower or 'tracking' in message_lower:
            return {
                'message': "I'm tracking your learning progress! Here's what I can help you monitor:\n\n**Progress Metrics:**\n• Modules completed and current position\n• Quiz scores and improvement trends\n• Time spent learning and consistency\n• Code examples practiced and mastered\n• Concepts understood vs. needs review\n\n**Analysis I can provide:**\n• Learning velocity and pace\n• Strengths and areas for improvement\n• Recommended study schedule\n• Goal tracking and milestone achievement\n\nWould you like a detailed progress report or recommendations for next steps?",
                'suggestions': ['Show my progress', 'Learning recommendations', 'Set new goals', 'Time analysis'],
                'related_topics': ['progress', 'analytics', 'goals', 'recommendations']
            }
        
        if 'analytics' in message_lower:
            return {
                'message': "Based on your learning patterns, here's what I observe:\n\n**Learning Analytics:**\n• You ask detailed questions - great for deep understanding!\n• You seem to prefer conceptual explanations with code examples\n• Your progress is steady but could be accelerated with practice\n\n**Recommendations:**\n• Spend 70% time on concepts, 30% on hands-on coding\n• Try the interactive exercises after each lesson\n• Review previous modules if concepts feel unclear\n\nWould you like specific recommendations for your learning style?",
                'suggestions': ['Detailed analytics', 'Learning style analysis', 'Study recommendations', 'Time optimization'],
                'related_topics': ['analytics', 'learning style', 'study tips', 'optimization']
            }
        
        return {
            'message': "I'm your progress tracker! I monitor your learning journey and can provide:\n\n• **Progress Reports**: Detailed analytics of your advancement\n• **Learning Patterns**: Understanding how you learn best\n• **Recommendations**: Personalized study suggestions\n• **Goal Tracking**: Monitor milestones and achievements\n• **Time Analysis**: Optimal study schedules and pacing\n\nWhat aspect of your learning progress interests you most?",
            'suggestions': ['Show my progress', 'Learning recommendations', 'Goal tracking', 'Time analysis'],
            'related_topics': ['progress', 'analytics', 'goals', 'learning patterns']
        }
    
    def _generate_motivation_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """Motivator Agent - provides encouragement and gamification"""
        message_lower = message.lower()
        
        # Detect frustration or difficulty
        if any(word in message_lower for word in ['hard', 'difficult', 'confusing', 'stuck', 'frustrated']):
            return {
                'message': "🌟 I understand that learning a new programming paradigm like OSP can be challenging! That's completely normal and you're doing great.\n\n**Remember:**\n• JAC's graph concepts are different from traditional programming\n• Every expert was once a beginner\n• Small, consistent steps lead to big breakthroughs\n• You're building valuable skills for AI and graph applications\n\n**Try this:**\n1. Focus on one concept at a time (start with nodes)\n2. Draw simple graphs on paper\n3. Practice with small, simple examples\n4. Celebrate small wins!\n\nYou've got this! What's one small step you'd like to try next? 💪",
                'suggestions': ['Explain concepts more simply', 'Give me practice exercises', 'Share success tips', 'Show me what others accomplished'],
                'related_topics': ['encouragement', 'practice', 'concepts', 'progress']
            }
        
        # Detect excitement or progress
        if any(word in message_lower for word in ['awesome', 'great', 'amazing', 'love', 'finally', 'understood']):
            return {
                'message': "🎉 That's fantastic! I love seeing that 'aha!' moment when concepts click!\n\n**You're doing great because:**\n• You're asking the right questions\n• You're taking time to understand, not just memorize\n• You're building a strong foundation for advanced topics\n\n**Keep the momentum going:**\n• Try the next concept while it's fresh\n• Practice with a coding exercise\n• Share what you've learned (teaching reinforces understanding)\n\n**Next milestone opportunities:**\n• Complete your first graph creation\n• Build your first walker\n• Try a mini-project\n\nWhat exciting JAC adventure will you tackle next? 🚀",
                'suggestions': ['More challenges', 'Next topic recommendation', 'Practice projects', 'Share achievement'],
                'related_topics': ['momentum', 'practice', 'projects', 'next steps']
            }
        
        return {
            'message': "Hey there, future JAC expert! 🌟 I'm here to keep you motivated on your learning journey!\n\n**Remember why you're learning JAC:**\n• You're mastering a cutting-edge programming paradigm\n• Graph programming is crucial for AI applications\n• JAC skills open doors to exciting tech opportunities\n• You're part of the Jaseci community!\n\n**Daily motivation:**\n• Every line of code you write builds expertise\n• Consistency beats intensity every time\n• You're already ahead by starting this journey\n• Questions and challenges mean you're growing!\n\n**Let's keep going strong!** What's your learning goal for today? 💪",
            'suggestions': ['Share my progress', 'Set learning goals', 'Get encouragement', 'Find study partners'],
            'related_topics': ['motivation', 'goals', 'progress', 'community']
        }
    
    def _generate_general_response(self, message: str, session_id: str) -> Dict[str, Any]:
        """System Orchestrator Agent - provides general assistance and coordinates other agents"""
        message_lower = message.lower()
        
        # Check for specific questions
        for question, answer in self.content_provider.QNA.items():
            if question in message_lower:
                return {
                    'message': f"**{question.title()}**: {answer}\n\nI'm here to help coordinate your learning journey! Would you like me to connect you with specific agents for deeper assistance?",
                    'suggestions': [q.title() for q in list(self.content_provider.QNA.keys())[:3]],
                    'related_topics': [k for k, v in self.content_provider.BASIC_CONCEPTS.items()][:3]
                }
        
        # Check for help requests
        if 'help' in message_lower or 'what can you do' in message_lower:
            return {
                'message': "Hello! I'm your JAC learning assistant. I can help you with:\n\n**Content Curator**: Concept explanations, code examples, learning resources\n**Quiz Master**: Interactive quizzes and knowledge assessments  \n**Code Evaluator**: Code review, debugging, and best practices\n**Progress Tracker**: Learning analytics and personalized recommendations\n**Motivator**: Encouragement and keeping you engaged\n\n**What can I help you with today?**\n• Learn JAC concepts and syntax\n• Practice with quizzes and exercises  \n• Get code feedback and guidance\n• Track your learning progress\n• Stay motivated and inspired\n\nJust tell me what you need!",
                'suggestions': ['Explain JAC concepts', 'Create a quiz', 'Review my code', 'Track progress', 'Motivate me'],
                'related_topics': ['jac', 'learning', 'help', 'tutorial']
            }
        
        return {
            'message': "Hi! I'm your JAC learning assistant. I can see you're interested in learning about JAC!\n\n**Quick Start Questions:**\n• What is JAC and why should I learn it?\n• How is JAC different from Python?\n• What is Object-Spatial Programming?\n• How do I get started with JAC?\n\n**Or try:**\n• 'What is a node?'\n• 'Show me code examples'\n• 'Create a quiz for me'\n• 'Help me understand walkers'\n\nWhat would you like to explore? I'm here to make your JAC learning journey exciting and successful! 🎯",
            'suggestions': ['What is JAC?', 'Show me examples', 'Get started guide', 'Learning path'],
            'related_topics': ['jac', 'getting started', 'examples', 'tutorial']
        }
    
    def get_agent_capabilities(self, agent_type: str) -> Dict[str, List[str]]:
        """Get capabilities and features for each agent type"""
        capabilities = {
            'content_curator': [
                'Explains JAC concepts and syntax',
                'Provides code examples and tutorials',
                'Recommends learning resources',
                'Curates personalized content',
                'Maintains concept relationships'
            ],
            'quiz_master': [
                'Generates topic-specific quizzes',
                'Adapts difficulty to user level',
                'Provides detailed explanations',
                'Tracks knowledge gaps',
                'Creates interactive assessments'
            ],
            'evaluator': [
                'Reviews JAC code syntax and logic',
                'Provides debugging assistance',
                'Suggests optimizations',
                'Enforces best practices',
                'Validates graph operations'
            ],
            'progress_tracker': [
                'Monitors learning progress',
                'Analyzes learning patterns',
                'Provides personalized recommendations',
                'Tracks completion rates',
                'Suggests study schedules'
            ],
            'motivator': [
                'Provides encouragement and support',
                'Maintains learning streaks',
                'Celebrates achievements',
                'Keeps users engaged',
                'Offers motivational insights'
            ],
            'system_orchestrator': [
                'Coordinates between all agents',
                'Provides system overview',
                'Handles complex queries',
                'Routes to appropriate specialists',
                'Ensures coherent experience'
            ]
        }
        
        return {
            'agent_type': agent_type,
            'capabilities': capabilities.get(agent_type, []),
            'specializations': capabilities.get(agent_type, [])
        }


# Global AI service instance
ai_service = JACAIService()
