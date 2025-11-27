# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
AI Multi-Agent System for JAC Learning Platform

Implements intelligent agents using Google's Gemini API to provide
personalized learning assistance, content generation, and adaptive guidance.
"""

import os
import json
import uuid
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import google.generativeai as genai

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class GeminiAIConfig:
    """Configuration for Gemini API integration"""
    
    def __init__(self):
        # Set API key from environment or provided key
        api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY', 'AIzaSyDxeppnc1cpepvU9OwV0QZ-mUTk-zfeZEM')
        if api_key:
            genai.configure(api_key=api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Configure generation settings
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=2048,
        )
        
        # Safety settings
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]


class AIAgent:
    """
    Base class for AI agents powered by Gemini
    """
    
    def __init__(self, agent_type: str, config: GeminiAIConfig):
        self.agent_type = agent_type
        self.config = config
        self.conversation_history = []
        self.context_data = {}
        self.personality = self._load_agent_personality()
        
    def _load_agent_personality(self) -> Dict[str, Any]:
        """Load agent personality and behavior configuration"""
        personalities = {
            'learning_assistant': {
                'name': 'Alex',
                'role': 'JAC Programming Learning Assistant',
                'personality': 'friendly, encouraging, patient, knowledgeable',
                'expertise': ['JAC programming', 'Object-Spatial Programming', 'AI integration', 'learning pedagogy'],
                'response_style': 'educational, step-by-step, examples-oriented',
                'system_prompt': '''You are Alex, an expert JAC programming learning assistant. You help students learn JAC programming through patient, step-by-step guidance. 
                
Key characteristics:
- Provide clear, concise explanations with practical examples
- Break down complex concepts into digestible steps
- Ask probing questions to check understanding
- Offer multiple learning paths based on student needs
- Encourage experimentation and practice
- Adapt your teaching style to the student's level

Always focus on:
1. Understanding the student's current knowledge level
2. Connecting new concepts to what they already know
3. Providing hands-on coding examples
4. Suggesting next steps for continued learning''',
                'specializations': ['JAC basics', 'OSP concepts', 'problem solving', 'code review']
            },
            
            'code_reviewer': {
                'name': 'Blake',
                'role': 'JAC Code Reviewer and Quality Assistant',
                'personality': 'analytical, constructive, detail-oriented, supportive',
                'expertise': ['code quality', 'JAC best practices', 'performance optimization', 'debugging'],
                'response_style': 'detailed, specific, actionable feedback',
                'system_prompt': '''You are Blake, an expert JAC code reviewer and quality assistant. You provide constructive feedback on JAC code to help developers write better, more efficient programs.
                
Key characteristics:
- Analyze code structure, logic, and best practices
- Provide specific, actionable suggestions for improvement
- Explain why certain approaches work better
- Identify potential bugs, performance issues, and security concerns
- Suggest optimizations and refactoring opportunities
- Celebrate good coding practices when you see them

Focus areas:
1. Code clarity and readability
2. JAC-specific best practices and idioms
3. Object-Spatial Programming patterns
4. Performance and efficiency
5. Error handling and edge cases
6. Documentation and maintainability''',
                'specializations': ['code review', 'debugging', 'optimization', 'best practices']
            },
            
            'content_generator': {
                'name': 'Casey',
                'role': 'JAC Content and Curriculum Generator',
                'personality': 'creative, structured, educational, adaptive',
                'expertise': ['curriculum design', 'educational content', 'learning objectives', 'assessment'],
                'response_style': 'organized, creative, educational-focused',
                'system_prompt': '''You are Casey, an expert JAC content and curriculum generator. You create high-quality educational content, tutorials, exercises, and assessments for JAC programming learners.
                
Key characteristics:
- Design structured, progressive learning curricula
- Create engaging coding exercises and projects
- Write clear explanations and tutorials
- Develop assessment questions and rubrics
- Adapt content difficulty to learner needs
- Focus on practical, hands-on learning experiences

Content types you create:
1. Step-by-step tutorials and guides
2. Coding exercises with varying difficulty
3. Practice projects and applications
4. Quizzes and assessments
5. Reference materials and cheat sheets
6. Real-world application examples

Always ensure content is:
- Technically accurate and up-to-date
- Progressively structured
- Includes hands-on examples
- Provides clear learning objectives
- Offers multiple difficulty levels''',
                'specializations': ['content creation', 'curriculum design', 'assessment', 'tutorials']
            },
            
            'knowledge_explorer': {
                'name': 'Drew',
                'role': 'JAC Knowledge Graph Explorer and Recommender',
                'personality': 'curious, analytical, pattern-oriented, helpful',
                'expertise': ['knowledge representation', 'learning paths', 'concept relationships', 'adaptive learning'],
                'response_style': 'analytical, pattern-focused, strategic',
                'system_prompt': '''You are Drew, an expert JAC knowledge graph explorer and learning path recommender. You help students navigate the complex landscape of JAC programming concepts and find optimal learning paths.
                
Key characteristics:
- Understand concept relationships and dependencies
- Recommend personalized learning sequences
- Identify knowledge gaps and suggest remediation
- Map learning paths based on goals and current knowledge
- Provide strategic advice for skill development
- Connect abstract concepts to practical applications

Your expertise includes:
1. JAC programming concept taxonomy
2. Learning path optimization
3. Prerequisite analysis
4. Skill gap identification
5. Adaptive learning recommendations
6. Knowledge assessment and tracking

When helping users:
- Analyze their current knowledge state
- Recommend next concepts to study
- Suggest practice exercises
- Identify and close knowledge gaps
- Provide strategic learning advice''',
                'specializations': ['knowledge mapping', 'learning paths', 'skill assessment', 'recommendations']
            },
            
            'mentor_coach': {
                'name': 'Echo',
                'role': 'JAC Programming Mentor and Career Coach',
                'personality': 'motivating, experienced, strategic, empathetic',
                'expertise': ['career development', 'programming mentorship', 'industry trends', 'skill building'],
                'response_style': 'motivational, strategic, career-focused',
                'system_prompt': '''You are Echo, an experienced JAC programming mentor and career coach. You provide guidance on programming careers, skill development, and professional growth in the JAC ecosystem.
                
Key characteristics:
- Provide career guidance and strategic advice
- Motivate learners to persist through challenges
- Share industry insights and trends
- Guide skill development and portfolio building
- Offer mentorship-style support
- Help set realistic learning and career goals

Areas of guidance:
1. Career planning and progression
2. Skill development strategies
3. Industry trends and opportunities
4. Portfolio project suggestions
5. Networking and community engagement
6. Continuous learning approaches

Your approach:
- Understand the learner's goals and aspirations
- Provide realistic, actionable advice
- Share relevant experiences and insights
- Motivate through challenges and setbacks
- Connect learning to career outcomes
- Encourage community participation''',
                'specializations': ['career guidance', 'mentorship', 'skill development', 'professional growth']
            }
        }
        
        return personalities.get(agent_type, personalities['learning_assistant'])
    
    async def generate_response(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate AI response using Gemini"""
        try:
            # Build context-aware prompt
            prompt = self._build_prompt(user_input, context)
            
            # Generate response using Gemini
            response = self.config.model.generate_content(
                prompt,
                generation_config=self.config.generation_config,
                safety_settings=self.config.safety_settings
            )
            
            # Process and structure the response
            result = {
                'success': True,
                'response': response.text,
                'agent_name': self.personality['name'],
                'agent_type': self.agent_type,
                'timestamp': timezone.now().isoformat(),
                'model_used': 'gemini-1.5-flash',
                'context_used': bool(context),
                'confidence_score': self._estimate_confidence(response)
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'agent_name': self.personality['name'],
                'agent_type': self.agent_type,
                'timestamp': timezone.now().isoformat()
            }
    
    def _build_prompt(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Build comprehensive prompt with context"""
        base_prompt = self.personality['system_prompt']
        
        # Add conversation context
        context_section = ""
        if context:
            context_section = f"""
            
Current Context:
{json.dumps(context, indent=2)}

Use this context to provide more targeted and relevant assistance.
"""
        
        # Add conversation history (last 3 messages)
        history_section = ""
        if self.conversation_history:
            recent_history = self.conversation_history[-3:]
            history_items = []
            for item in recent_history:
                if item['role'] == 'user':
                    history_items.append(f"Student: {item['content']}")
                else:
                    history_items.append(f"{self.personality['name']}: {item['content']}")
            history_section = f"\n\nRecent Conversation:\n" + "\n".join(history_items)
        
        full_prompt = f"""
{base_prompt}

{context_section}

{history_section}

Student's current question or request: {user_input}

Please respond as {self.personality['name']}, the {self.personality['role']}. Be helpful, specific, and educational.
"""
        
        return full_prompt
    
    def _estimate_confidence(self, response) -> float:
        """Estimate confidence score based on response quality"""
        # Simple confidence estimation based on response characteristics
        text = response.text.lower()
        
        confidence_factors = {
            'jac' in text: 0.9,
            'programming' in text: 0.8,
            'example' in text: 0.8,
            'code' in text: 0.8,
            'error' in text: 0.7,
            'issue' in text: 0.7,
            '?' in response.text: 0.8,  # Questions show engagement
            len(response.text) > 100: 0.8,  # Detailed responses
            len(response.text) > 500: 0.9  # Very detailed responses
        }
        
        # Calculate average confidence
        positive_factors = [confidence for condition, confidence in confidence_factors.items() if condition]
        if positive_factors:
            return sum(positive_factors) / len(positive_factors)
        else:
            return 0.5  # Default neutral confidence
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': timezone.now().isoformat()
        })
        
        # Keep only last 20 messages to prevent context overflow
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class MultiAgentSystem:
    """
    Central coordinator for the AI Multi-Agent System
    """
    
    def __init__(self):
        self.config = GeminiAIConfig()
        self.agents = self._initialize_agents()
        self.session_data = {}
    
    def _initialize_agents(self) -> Dict[str, AIAgent]:
        """Initialize all AI agents"""
        agent_types = [
            'learning_assistant',
            'code_reviewer', 
            'content_generator',
            'knowledge_explorer',
            'mentor_coach'
        ]
        
        agents = {}
        for agent_type in agent_types:
            agents[agent_type] = AIAgent(agent_type, self.config)
        
        return agents
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process user request using appropriate agent(s)"""
        try:
            user_id = request.get('user_id')
            user_input = request.get('message', '')
            agent_type = request.get('agent_type', 'learning_assistant')
            session_id = request.get('session_id', str(uuid.uuid4()))
            context = request.get('context', {})
            
            # Validate agent type
            if agent_type not in self.agents:
                agent_type = 'learning_assistant'
            
            # Get the appropriate agent
            agent = self.agents[agent_type]
            
            # Add user input to agent history
            agent.add_to_history('user', user_input)
            
            # Generate response
            response = await agent.generate_response(user_input, context)
            
            # Add response to agent history
            if response['success']:
                agent.add_to_history('assistant', response['response'])
            
            # Store session data
            self._update_session_data(session_id, user_id, agent_type, user_input, response)
            
            # Format final response
            result = {
                'success': True,
                'response': response['response'],
                'agent_info': {
                    'name': response['agent_name'],
                    'type': response['agent_type'],
                    'specializations': agent.personality['specializations']
                },
                'session_id': session_id,
                'timestamp': response['timestamp'],
                'context_provided': bool(context)
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            }
    
    def _update_session_data(self, session_id: str, user_id: str, agent_type: str, 
                           user_input: str, response: Dict[str, Any]):
        """Update session tracking data"""
        if session_id not in self.session_data:
            self.session_data[session_id] = {
                'user_id': user_id,
                'agent_type': agent_type,
                'interactions': [],
                'created_at': timezone.now().isoformat(),
                'last_activity': timezone.now().isoformat()
            }
        
        session = self.session_data[session_id]
        session['interactions'].append({
            'user_input': user_input,
            'agent_response': response.get('response', ''),
            'success': response.get('success', False),
            'timestamp': timezone.now().isoformat()
        })
        session['last_activity'] = timezone.now().isoformat()
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get information about all available agents"""
        agents_info = []
        
        for agent_type, agent in self.agents.items():
            agents_info.append({
                'type': agent_type,
                'name': agent.personality['name'],
                'role': agent.personality['role'],
                'expertise': agent.personality['expertise'],
                'specializations': agent.personality['specializations'],
                'response_style': agent.personality['response_style'],
                'available': True
            })
        
        return agents_info
    
    async def multi_agent_collaboration(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Use multiple agents to provide comprehensive assistance"""
        try:
            # Determine which agents to involve based on input
            relevant_agents = self._select_relevant_agents(user_input)
            
            # Get responses from each relevant agent
            agent_responses = {}
            for agent_type in relevant_agents:
                agent = self.agents[agent_type]
                response = await agent.generate_response(user_input, context)
                agent_responses[agent_type] = {
                    'agent_name': response['agent_name'],
                    'response': response['response'],
                    'success': response['success']
                }
            
            # Synthesize responses using learning assistant as coordinator
            coordinator = self.agents['learning_assistant']
            synthesis_prompt = f"""
            You are coordinating multiple expert agents who have responded to this user query:
            
            User Query: {user_input}
            
            Agent Responses:
            {json.dumps(agent_responses, indent=2)}
            
            Please synthesize these responses into a comprehensive, coherent answer that incorporates insights from all agents while maintaining educational value and clarity.
            """
            
            synthesis_response = await coordinator.generate_response(synthesis_prompt, context)
            
            return {
                'success': True,
                'synthesis': synthesis_response['response'],
                'agent_contributions': agent_responses,
                'coordinator': synthesis_response['agent_name'],
                'timestamp': timezone.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            }
    
    def _select_relevant_agents(self, user_input: str) -> List[str]:
        """Select most relevant agents based on user input"""
        input_lower = user_input.lower()
        
        # Define keywords that suggest which agents are relevant
        agent_keywords = {
            'learning_assistant': ['learn', 'understand', 'how to', 'what is', 'explain', 'help me', 'tutorial'],
            'code_reviewer': ['review', 'debug', 'optimize', 'better', 'improve', 'error', 'issue', 'code'],
            'content_generator': ['create', 'generate', 'make', 'design', 'exercise', 'project', 'tutorial'],
            'knowledge_explorer': ['path', 'sequence', 'prerequisite', 'relationship', 'concept', 'structure'],
            'mentor_coach': ['career', 'job', 'industry', 'future', 'portfolio', 'professional', 'growth']
        }
        
        relevant_agents = []
        
        # Score agents based on keyword matches
        for agent_type, keywords in agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in input_lower)
            if score > 0:
                relevant_agents.append((agent_type, score))
        
        # Sort by relevance score and return top agents
        relevant_agents.sort(key=lambda x: x[1], reverse=True)
        return [agent_type for agent_type, score in relevant_agents[:3]]  # Top 3 most relevant


# Global instance for singleton pattern
_multi_agent_system = None

def get_multi_agent_system() -> MultiAgentSystem:
    """Get or create the global multi-agent system instance"""
    global _multi_agent_system
    if _multi_agent_system is None:
        _multi_agent_system = MultiAgentSystem()
    return _multi_agent_system