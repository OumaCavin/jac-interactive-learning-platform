"""
Quiz Master Agent

Specialized agent responsible for creating quizzes, assessments, and evaluations
in the JAC Interactive Learning Platform.
"""

from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count
from .base_agent import BaseAgent, AgentStatus, TaskPriority
from ..learning.models import LearningPath, Module, UserModuleProgress, UserLearningPath
from ..assessments.models import Assessment, AssessmentQuestion, UserAssessmentResult


class QuizMasterAgent(BaseAgent):
    """
    Quiz Master Agent handles:
    - Quiz and assessment generation
    - Question bank management
    - Adaptive difficulty adjustment
    - Performance analysis
    - Personalized testing
    """
    
    def __init__(self, agent_id: str = None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id=agent_id or "quiz_master",
            agent_type="Quiz Master",
            config=config or {}
        )
        
        self.question_types = {
            'multiple_choice': 'Multiple Choice',
            'true_false': 'True/False',
            'fill_blank': 'Fill in the Blank',
            'code_completion': 'Code Completion',
            'essay': 'Essay',
            'programming': 'Programming Exercise',
            'debugging': 'Debugging Task'
        }
        
        self.difficulty_weights = {
            'easy': 1,
            'medium': 2,
            'hard': 3
        }
        
        self.assessment_templates = {}
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process quiz and assessment tasks
        
        Expected task types:
        - 'generate_quiz': Create a new quiz with questions
        - 'generate_assessment': Create comprehensive assessment
        - 'adaptive_questions': Generate questions based on user performance
        - 'analyze_performance': Analyze quiz performance data
        - 'recommend_difficulty': Recommend appropriate difficulty level
        - 'create_question_bank': Build organized question bank
        """
        self.update_status(AgentStatus.PROCESSING)
        
        task_type = task.get('type', 'generate_quiz')
        
        try:
            if task_type == 'generate_quiz':
                result = self._generate_quiz(task.get('params', {}))
            elif task_type == 'generate_assessment':
                result = self._generate_assessment(task.get('params', {}))
            elif task_type == 'adaptive_questions':
                result = self._generate_adaptive_questions(task.get('params', {}))
            elif task_type == 'analyze_performance':
                result = self._analyze_performance(task.get('params', {}))
            elif task_type == 'recommend_difficulty':
                result = self._recommend_difficulty(task.get('params', {}))
            elif task_type == 'create_question_bank':
                result = self._create_question_bank(task.get('params', {}))
            elif task_type == 'generate_feedback':
                result = self._generate_feedback(task.get('params', {}))
            else:
                result = {'error': f'Unknown task type: {task_type}'}
            
            self.update_status(AgentStatus.ACTIVE)
            self.update_metrics('assessments_created', self.metrics.get('assessments_created', 0) + 1)
            return {'success': True, 'result': result}
            
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return {'success': False, 'error': str(e)}
    
    def _generate_quiz(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new quiz with questions"""
        topic = params.get('topic', '')
        difficulty = params.get('difficulty', 'medium')
        num_questions = params.get('num_questions', 10)
        question_types = params.get('question_types', ['multiple_choice'])
        time_limit = params.get('time_limit', 30)  # minutes
        
        if not topic:
            return {'error': 'Topic is required for quiz generation'}
        
        quiz = {
            'quiz_id': str(uuid.uuid4()),
            'title': f"{topic.title()} Quiz",
            'topic': topic,
            'difficulty': difficulty,
            'total_questions': num_questions,
            'time_limit': time_limit,
            'question_types': question_types,
            'questions': [],
            'scoring_config': {
                'points_per_question': 10,
                'time_bonus': True,
                'penalty_for_wrong_answers': 0
            },
            'generated_at': timezone.now().isoformat()
        }
        
        # Generate questions based on topic and requirements
        questions = self._generate_questions_for_topic(
            topic=topic,
            difficulty=difficulty,
            num_questions=num_questions,
            question_types=question_types
        )
        
        quiz['questions'] = questions
        
        # Calculate difficulty distribution
        difficulty_dist = self._analyze_question_difficulty(questions)
        quiz['difficulty_distribution'] = difficulty_dist
        
        # Add metadata
        quiz['metadata'] = {
            'estimated_completion_time': sum(q['estimated_time'] for q in questions),
            'cognitive_load': self._calculate_cognitive_load(questions),
            'learning_objectives': self._extract_learning_objectives(questions)
        }
        
        return quiz
    
    def _generate_assessment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive assessment"""
        learning_path_id = params.get('learning_path_id')
        assessment_type = params.get('assessment_type', 'formative')  # formative, summative
        include_practical = params.get('include_practical', True)
        
        if not learning_path_id:
            return {'error': 'Learning path ID is required'}
        
        try:
            learning_path = LearningPath.objects.get(id=learning_path_id)
        except LearningPath.DoesNotExist:
            return {'error': 'Learning path not found'}
        
        assessment = {
            'assessment_id': str(uuid.uuid4()),
            'learning_path_id': str(learning_path_id),
            'title': f"{learning_path.title} - {assessment_type.title()} Assessment",
            'type': assessment_type,
            'sections': [],
            'total_questions': 0,
            'time_limit': 0,
            'scoring_config': {
                'passing_score': 70,
                'max_score': 100
            },
            'generated_at': timezone.now().isoformat()
        }
        
        # Get modules from learning path
        modules = Module.objects.filter(
            learning_path=learning_path
        ).order_by('order')
        
        if not modules:
            return {'error': 'No modules found in learning path'}
        
        # Generate assessment sections for each module
        for module in modules:
            section = self._generate_assessment_section(module, assessment_type, include_practical)
            if section:
                assessment['sections'].append(section)
        
        # Calculate totals
        assessment['total_questions'] = sum(len(section['questions']) for section in assessment['sections'])
        assessment['time_limit'] = sum(section.get('time_limit', 30) for section in assessment['sections'])
        
        return assessment
    
    def _generate_adaptive_questions(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate questions based on user performance history"""
        user = params.get('user')
        topic = params.get('topic', '')
        current_performance = params.get('current_performance', {})
        target_difficulty = params.get('target_difficulty', 'medium')
        num_questions = params.get('num_questions', 5)
        
        if not user:
            return {'error': 'User parameter required for adaptive questions'}
        
        # Analyze user's performance history
        performance_analysis = self._analyze_user_performance(user, topic)
        
        # Adjust difficulty based on performance
        adjusted_difficulty = self._adjust_difficulty_for_adaptation(
            performance_analysis, target_difficulty
        )
        
        # Generate personalized questions
        questions = self._generate_questions_for_topic(
            topic=topic,
            difficulty=adjusted_difficulty,
            num_questions=num_questions,
            question_types=['multiple_choice', 'true_false'],
            user_preferences=self._get_user_question_preferences(user)
        )
        
        # Enhance questions with adaptive features
        for question in questions:
            question['adaptive_metadata'] = self._generate_adaptive_metadata(
                question, performance_analysis
            )
        
        return {
            'adaptive_questions': questions,
            'original_difficulty': target_difficulty,
            'adjusted_difficulty': adjusted_difficulty,
            'performance_analysis': performance_analysis,
            'personalization_factors': {
                'strength_areas': performance_analysis.get('strength_areas', []),
                'improvement_areas': performance_analysis.get('improvement_areas', []),
                'learning_velocity': performance_analysis.get('velocity', 'medium')
            }
        }
    
    def _analyze_performance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quiz/assessment performance data"""
        assessment_id = params.get('assessment_id')
        user_id = params.get('user_id')
        timeframe = params.get('timeframe', 30)  # days
        
        analysis = {
            'analysis_id': str(uuid.uuid4()),
            'timeframe_days': timeframe,
            'generated_at': timezone.now().isoformat(),
            'summary': {},
            'detailed_metrics': {},
            'insights': [],
            'recommendations': []
        }
        
        # Get performance data
        if assessment_id:
            # Analyze specific assessment
            performance_data = self._get_assessment_performance_data(assessment_id)
            analysis['assessment_specific'] = performance_data
        elif user_id:
            # Analyze user performance over time
            performance_data = self._get_user_performance_over_time(user_id, timeframe)
            analysis['user_performance'] = performance_data
        else:
            return {'error': 'Either assessment_id or user_id required'}
        
        # Generate insights and recommendations
        insights = self._generate_performance_insights(performance_data)
        recommendations = self._generate_performance_recommendations(performance_data)
        
        analysis['insights'] = insights
        analysis['recommendations'] = recommendations
        analysis['summary'] = self._create_performance_summary(performance_data)
        
        return analysis
    
    def _recommend_difficulty(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend appropriate difficulty level for user"""
        user = params.get('user')
        topic = params.get('topic', '')
        recent_scores = params.get('recent_scores', [])
        
        if not user:
            return {'error': 'User parameter required'}
        
        # Get user's learning history
        user_progress = UserModuleProgress.objects.filter(
            user=user,
            module__content__topic__icontains=topic
        ).order_by('-updated_at')[:10]
        
        # Calculate performance metrics
        avg_score = 0
        score_trend = 'stable'
        
        if recent_scores:
            avg_score = sum(recent_scores) / len(recent_scores)
            if len(recent_scores) > 1:
                if recent_scores[-1] > recent_scores[0] + 10:
                    score_trend = 'improving'
                elif recent_scores[-1] < recent_scores[0] - 10:
                    score_trend = 'declining'
        
        # Determine recommended difficulty
        recommended_difficulty = self._determine_difficulty_level(
            avg_score, score_trend, user_progress
        )
        
        # Confidence score for recommendation
        confidence = self._calculate_difficulty_recommendation_confidence(
            avg_score, len(recent_scores), user_progress.count()
        )
        
        return {
            'recommended_difficulty': recommended_difficulty,
            'confidence_score': confidence,
            'reasoning': {
                'average_score': avg_score,
                'score_trend': score_trend,
                'user_progress_count': user_progress.count()
            },
            'alternative_difficulties': self._get_alternative_difficulties(
                recommended_difficulty, avg_score
            ),
            'adaptation_suggestions': self._suggest_difficulty_adaptations(
                recommended_difficulty, user
            )
        }
    
    def _create_question_bank(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create organized question bank"""
        topic = params.get('topic', '')
        difficulty_levels = params.get('difficulty_levels', ['easy', 'medium', 'hard'])
        question_types = params.get('question_types', list(self.question_types.keys()))
        min_questions_per_type = params.get('min_questions_per_type', 5)
        
        question_bank = {
            'bank_id': str(uuid.uuid4()),
            'topic': topic,
            'difficulty_levels': difficulty_levels,
            'question_types': question_types,
            'questions_by_type': {},
            'questions_by_difficulty': {},
            'statistics': {},
            'created_at': timezone.now().isoformat()
        }
        
        # Generate questions for each type and difficulty combination
        for question_type in question_types:
            questions_for_type = []
            
            for difficulty in difficulty_levels:
                questions = self._generate_questions_for_topic(
                    topic=topic,
                    difficulty=difficulty,
                    num_questions=min_questions_per_type * 2,  # Generate extra for variety
                    question_types=[question_type],
                    bank_mode=True
                )
                questions_for_type.extend(questions)
            
            question_bank['questions_by_type'][question_type] = questions_for_type
            
            # Organize by difficulty as well
            for question in questions_for_type:
                difficulty = question['difficulty']
                if difficulty not in question_bank['questions_by_difficulty']:
                    question_bank['questions_by_difficulty'][difficulty] = []
                question_bank['questions_by_difficulty'][difficulty].append(question)
        
        # Calculate statistics
        question_bank['statistics'] = {
            'total_questions': sum(
                len(questions) for questions in question_bank['questions_by_type'].values()
            ),
            'type_distribution': {
                qtype: len(questions) 
                for qtype, questions in question_bank['questions_by_type'].items()
            },
            'difficulty_distribution': {
                difficulty: len(questions)
                for difficulty, questions in question_bank['questions_by_difficulty'].items()
            },
            'average_question_length': self._calculate_average_question_length(question_bank)
        }
        
        return question_bank
    
    def _generate_feedback(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized feedback for quiz results"""
        user = params.get('user')
        assessment_results = params.get('assessment_results', {})
        questions_answered = params.get('questions_answered', [])
        
        if not user or not assessment_results:
            return {'error': 'User and assessment results required'}
        
        feedback = {
            'feedback_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'overall_score': assessment_results.get('score', 0),
            'performance_level': self._determine_performance_level(assessment_results.get('score', 0)),
            'detailed_feedback': {},
            'strengths': [],
            'improvement_areas': [],
            'learning_recommendations': [],
            'next_steps': [],
            'generated_at': timezone.now().isoformat()
        }
        
        # Analyze performance by topic/area
        area_performance = self._analyze_performance_by_area(questions_answered)
        feedback['detailed_feedback'] = area_performance
        
        # Identify strengths and weaknesses
        strengths = self._identify_strengths(area_performance)
        improvements = self._identify_improvement_areas(area_performance)
        
        feedback['strengths'] = strengths
        feedback['improvement_areas'] = improvements
        
        # Generate recommendations
        recommendations = self._generate_learning_recommendations(
            user, area_performance, assessment_results
        )
        feedback['learning_recommendations'] = recommendations
        
        # Suggest next steps
        next_steps = self._suggest_next_steps(user, assessment_results, area_performance)
        feedback['next_steps'] = next_steps
        
        return feedback
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities provided by this agent"""
        return [
            'quiz_generation',
            'assessment_creation',
            'adaptive_testing',
            'performance_analysis',
            'difficulty_recommendation',
            'question_bank_creation',
            'personalized_feedback',
            'cognitive_load_assessment',
            'learning_objective_mapping'
        ]
    
    def get_specialization_info(self) -> Dict[str, Any]:
        """Get detailed information about Quiz Master specialization"""
        return {
            'agent_type': 'Quiz Master',
            'specialization': 'Assessment and Evaluation',
            'key_responsibilities': [
                'Generate quizzes and assessments',
                'Create adaptive testing scenarios',
                'Analyze performance data',
                'Provide personalized feedback',
                'Build comprehensive question banks'
            ],
            'question_types_supported': list(self.question_types.keys()),
            'assessment_formats': [
                'Formative Assessment',
                'Summative Assessment',
                'Diagnostic Assessment',
                'Adaptive Assessment',
                'Performance-Based Assessment'
            ],
            'analytics_capabilities': [
                'Performance trend analysis',
                'Difficulty calibration',
                'Learning velocity assessment',
                'Knowledge gap identification',
                'Predictive modeling'
            ]
        }
    
    # Helper methods for question generation
    def _generate_questions_for_topic(self, topic: str, difficulty: str, num_questions: int, 
                                    question_types: List[str], user_preferences: Dict = None,
                                    bank_mode: bool = False) -> List[Dict[str, Any]]:
        """Generate questions for a specific topic"""
        questions = []
        
        # JAC/Jaseci specific question templates
        jac_question_templates = {
            'multiple_choice': [
                {
                    'template': f"What is the primary purpose of {topic} in JAC programming?",
                    'options': [
                        f"To define {topic} functionality",
                        f"To manage {topic} execution",
                        f"To optimize {topic} performance",
                        f"All of the above"
                    ],
                    'correct': 3
                },
                {
                    'template': f"Which statement about {topic} is correct?",
                    'options': [
                        f"{topic} is only used in advanced JAC programs",
                        f"{topic} can be imported from other JAC modules",
                        f"{topic} is not supported in current JAC version",
                        f"{topic} requires special syntax"
                    ],
                    'correct': 1
                }
            ],
            'true_false': [
                {
                    'template': f"True or False: {topic} is a fundamental concept in JAC programming.",
                    'correct': True,
                    'explanation': f"{topic} is indeed a core concept that every JAC programmer should understand."
                },
                {
                    'template': f"True or False: {topic} can only be used with specific JAC data types.",
                    'correct': False,
                    'explanation': f"{topic} can be used with various data types in JAC."
                }
            ],
            'fill_blank': [
                {
                    'template': f"Complete the sentence: In JAC, {topic} is used to _______________.",
                    'correct_answers': ['define', 'create', 'establish'],
                    'context': "This tests understanding of the basic purpose of the concept."
                }
            ],
            'code_completion': [
                {
                    'template': f"Complete the following JAC code using {topic}:",
                    'code_snippet': f"// Using {topic}\n{topic} my_{topic.lower()} = ___________;",
                    'correct_completion': f"new {topic}()",
                    'hints': ["Think about JAC object instantiation", "Consider the syntax for creating objects"]
                }
            ]
        }
        
        # Generate questions based on templates
        for i in range(num_questions):
            question_type = question_types[i % len(question_types)]
            
            if question_type in jac_question_templates:
                template = jac_question_templates[question_type][i % len(jac_question_templates[question_type])]
                
                question = self._build_question_from_template(
                    template, question_type, topic, difficulty, bank_mode
                )
                questions.append(question)
            else:
                # Fallback question generation
                question = self._generate_fallback_question(topic, question_type, difficulty)
                questions.append(question)
        
        return questions
    
    def _build_question_from_template(self, template: Dict, question_type: str, topic: str,
                                    difficulty: str, bank_mode: bool = False) -> Dict[str, Any]:
        """Build a question from a template"""
        question = {
            'question_id': str(uuid.uuid4()),
            'type': question_type,
            'topic': topic,
            'difficulty': difficulty,
            'text': template['template'].format(topic=topic),
            'estimated_time': self._estimate_question_time(question_type, difficulty),
            'cognitive_level': self._determine_cognitive_level(difficulty),
            'learning_objectives': [f"Understand {topic}", f"Apply {topic} concepts"],
            'metadata': {}
        }
        
        # Add type-specific content
        if question_type == 'multiple_choice':
            question['options'] = template['options']
            question['correct_answer'] = template['correct']
            question['explanation'] = f"The correct answer is option {template['correct'] + 1} because {topic} serves the primary function described."
        
        elif question_type == 'true_false':
            question['correct_answer'] = template['correct']
            question['explanation'] = template['explanation']
        
        elif question_type == 'fill_blank':
            question['correct_answers'] = template['correct_answers']
            question['context'] = template['context']
        
        elif question_type == 'code_completion':
            question['code_snippet'] = template['code_snippet']
            question['correct_completion'] = template['correct_completion']
            question['hints'] = template['hints']
        
        if not bank_mode:
            # Add interactive metadata for active quizzes
            question['interactive_metadata'] = {
                'allow_skip': True,
                'show_hint_after': 30,  # seconds
                'points': self._calculate_question_points(difficulty),
                'penalty_for_hint': 2
            }
        
        return question
    
    def _generate_fallback_question(self, topic: str, question_type: str, difficulty: str) -> Dict[str, Any]:
        """Generate a fallback question when templates are exhausted"""
        return {
            'question_id': str(uuid.uuid4()),
            'type': question_type,
            'topic': topic,
            'difficulty': difficulty,
            'text': f"What is the most important aspect of {topic} in JAC programming?",
            'options': [
                "Understanding the basic concepts",
                "Knowing when to apply it",
                "Mastering the implementation details",
                "All of the above are important"
            ],
            'correct_answer': 3,
            'explanation': f"All aspects are important when working with {topic} in JAC.",
            'estimated_time': 45,
            'cognitive_level': self._determine_cognitive_level(difficulty)
        }
    
    def _estimate_question_time(self, question_type: str, difficulty: str) -> int:
        """Estimate time to complete question (seconds)"""
        base_times = {
            'multiple_choice': 30,
            'true_false': 20,
            'fill_blank': 45,
            'code_completion': 90,
            'essay': 300,
            'programming': 600,
            'debugging': 300
        }
        
        difficulty_multipliers = {
            'easy': 1.0,
            'medium': 1.3,
            'hard': 1.6
        }
        
        base_time = base_times.get(question_type, 60)
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        
        return int(base_time * multiplier)
    
    def _determine_cognitive_level(self, difficulty: str) -> str:
        """Determine Bloom's taxonomy cognitive level based on difficulty"""
        cognitive_mapping = {
            'easy': 'Remember/Understand',
            'medium': 'Apply/Analyze',
            'hard': 'Analyze/Evaluate/Create'
        }
        return cognitive_mapping.get(difficulty, 'Understand')
    
    def _calculate_question_points(self, difficulty: str) -> int:
        """Calculate points for a question based on difficulty"""
        point_values = {
            'easy': 5,
            'medium': 10,
            'hard': 15
        }
        return point_values.get(difficulty, 10)
    
    def _analyze_question_difficulty(self, questions: List[Dict]) -> Dict[str, Any]:
        """Analyze difficulty distribution in questions"""
        difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
        
        for question in questions:
            difficulty = question.get('difficulty', 'medium')
            difficulty_counts[difficulty] += 1
        
        total = len(questions)
        return {
            'distribution': difficulty_counts,
            'percentages': {
                level: (count / total) * 100 if total > 0 else 0
                for level, count in difficulty_counts.items()
            },
            'average_difficulty': sum(
                {'easy': 1, 'medium': 2, 'hard': 3}.get(q.get('difficulty', 'medium'), 2)
                for q in questions
            ) / len(questions) if questions else 0
        }
    
    def _calculate_cognitive_load(self, questions: List[Dict]) -> str:
        """Calculate overall cognitive load of questions"""
        cognitive_levels = [q.get('cognitive_level', 'Understand') for q in questions]
        
        high_cognitive = sum(1 for level in cognitive_levels if 'Analyze' in level or 'Evaluate' in level)
        percentage = (high_cognitive / len(questions)) * 100 if questions else 0
        
        if percentage > 60:
            return 'high'
        elif percentage > 30:
            return 'medium'
        else:
            return 'low'
    
    def _extract_learning_objectives(self, questions: List[Dict]) -> List[str]:
        """Extract learning objectives from questions"""
        objectives = set()
        for question in questions:
            if 'learning_objectives' in question:
                objectives.update(question['learning_objectives'])
        return list(objectives)
    
    def _generate_assessment_section(self, module, assessment_type: str, include_practical: bool) -> Optional[Dict[str, Any]]:
        """Generate assessment section for a module"""
        section = {
            'section_id': str(uuid.uuid4()),
            'module_id': str(module.id),
            'module_title': module.title,
            'assessment_type': assessment_type,
            'questions': [],
            'time_limit': 30,
            'points': 0
        }
        
        # Generate questions based on module content and assessment type
        num_questions = {
            'formative': 5,
            'summative': 10,
            'diagnostic': 8
        }.get(assessment_type, 5)
        
        difficulty = module.difficulty_level or 'medium'
        
        questions = self._generate_questions_for_topic(
            topic=module.title,
            difficulty=difficulty,
            num_questions=num_questions,
            question_types=['multiple_choice', 'true_false', 'fill_blank']
        )
        
        section['questions'] = questions
        section['points'] = sum(self._calculate_question_points(q['difficulty']) for q in questions)
        
        if include_practical and assessment_type == 'summative':
            # Add practical component
            practical_question = {
                'question_id': str(uuid.uuid4()),
                'type': 'programming',
                'topic': module.title,
                'difficulty': difficulty,
                'text': f"Implement a solution that demonstrates your understanding of {module.title}",
                'points': 20,
                'estimated_time': 300
            }
            section['questions'].append(practical_question)
            section['points'] += 20
        
        return section
    
    def _analyze_user_performance(self, user: User, topic: str) -> Dict[str, Any]:
        """Analyze user's performance history for a topic"""
        # Get user's progress data
        progress_data = UserModuleProgress.objects.filter(
            user=user,
            module__content__topic__icontains=topic
        ).order_by('-updated_at')[:20]
        
        if not progress_data:
            return {
                'average_score': 0,
                'attempts_count': 0,
                'improvement_trend': 'no_data',
                'strength_areas': [],
                'improvement_areas': []
            }
        
        scores = []
        for progress in progress_data:
            if hasattr(progress, 'score') and progress.score:
                scores.append(progress.score)
        
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Analyze trends
        improvement_trend = 'stable'
        if len(scores) > 2:
            recent_avg = sum(scores[:5]) / min(5, len(scores))
            old_avg = sum(scores[-5:]) / min(5, len(scores))
            if recent_avg > old_avg + 10:
                improvement_trend = 'improving'
            elif recent_avg < old_avg - 10:
                improvement_trend = 'declining'
        
        return {
            'average_score': average_score,
            'attempts_count': len(progress_data),
            'scores': scores,
            'improvement_trend': improvement_trend,
            'last_activity': progress_data[0].updated_at.isoformat() if progress_data else None
        }
    
    def _adjust_difficulty_for_adaptation(self, performance_analysis: Dict, target_difficulty: str) -> str:
        """Adjust difficulty based on performance analysis"""
        avg_score = performance_analysis.get('average_score', 50)
        trend = performance_analysis.get('improvement_trend', 'stable')
        
        difficulty_order = {'easy': 1, 'medium': 2, 'hard': 3}
        target_level = difficulty_order.get(target_difficulty, 2)
        
        # Adjust based on performance
        if avg_score > 85 and trend == 'improving':
            # User is doing very well, increase difficulty
            adjusted_level = min(3, target_level + 1)
        elif avg_score < 60 or trend == 'declining':
            # User struggling, decrease difficulty
            adjusted_level = max(1, target_level - 1)
        else:
            # Keep target difficulty
            adjusted_level = target_level
        
        # Convert back to string
        level_map = {1: 'easy', 2: 'medium', 3: 'hard'}
        return level_map.get(adjusted_level, target_difficulty)
    
    def _get_user_question_preferences(self, user: User) -> Dict[str, Any]:
        """Get user's question type preferences"""
        # This would typically come from user profile or learning analytics
        return {
            'preferred_types': ['multiple_choice', 'true_false'],
            'time_per_question_preference': 60,  # seconds
            'hint_usage_pattern': 'moderate',
            'skip_pattern': 'rarely'
        }
    
    def _generate_adaptive_metadata(self, question: Dict, performance_analysis: Dict) -> Dict[str, Any]:
        """Generate adaptive metadata for question"""
        return {
            'adaptive_difficulty': question['difficulty'],
            'confidence_threshold': 0.7,
            'allow_partial_credit': True,
            'show_detailed_feedback': True,
            'personalization_factors': {
                'user_strength_level': 'medium',
                'topic_familiarity': 'developing',
                'optimal_challenge_level': 'medium'
            }
        }
    
    def _get_assessment_performance_data(self, assessment_id: str) -> Dict[str, Any]:
        """Get performance data for specific assessment"""
        # This would query the actual database
        return {
            'assessment_id': assessment_id,
            'total_takers': 0,
            'average_score': 0,
            'pass_rate': 0,
            'difficulty_analysis': {},
            'common_errors': []
        }
    
    def _get_user_performance_over_time(self, user_id: str, timeframe_days: int) -> Dict[str, Any]:
        """Get user's performance data over time period"""
        # This would query the actual database
        return {
            'user_id': user_id,
            'timeframe_days': timeframe_days,
            'performance_trend': 'stable',
            'average_score': 75,
            'total_assessments': 0,
            'improvement_areas': []
        }
    
    def _generate_performance_insights(self, performance_data: Dict) -> List[str]:
        """Generate insights from performance data"""
        insights = []
        
        if 'average_score' in performance_data:
            score = performance_data['average_score']
            if score >= 90:
                insights.append("Exceptional performance across all areas")
            elif score >= 80:
                insights.append("Strong performance with room for minor improvements")
            elif score >= 70:
                insights.append("Good performance, consider focusing on challenging areas")
            else:
                insights.append("Performance needs improvement, recommend additional practice")
        
        return insights
    
    def _generate_performance_recommendations(self, performance_data: Dict) -> List[str]:
        """Generate recommendations based on performance data"""
        recommendations = []
        
        if 'improvement_areas' in performance_data:
            for area in performance_data['improvement_areas']:
                recommendations.append(f"Practice more in {area} to improve overall performance")
        
        recommendations.append("Continue current learning approach while focusing on weak areas")
        return recommendations
    
    def _create_performance_summary(self, performance_data: Dict) -> Dict[str, Any]:
        """Create summary of performance data"""
        return {
            'overall_rating': 'good',
            'key_strengths': [],
            'primary_focus_areas': [],
            'next_recommended_action': 'Continue current learning plan'
        }
    
    def _determine_difficulty_level(self, avg_score: float, score_trend: str, user_progress) -> str:
        """Determine appropriate difficulty level"""
        if avg_score >= 85:
            if score_trend == 'improving':
                return 'hard'
            else:
                return 'medium'
        elif avg_score >= 70:
            return 'medium'
        else:
            return 'easy'
    
    def _calculate_difficulty_recommendation_confidence(self, avg_score: float, 
                                                     num_recent_scores: int, 
                                                     total_attempts: int) -> float:
        """Calculate confidence in difficulty recommendation"""
        confidence_factors = []
        
        # Factor in number of recent scores
        if num_recent_scores >= 5:
            confidence_factors.append(0.4)
        elif num_recent_scores >= 3:
            confidence_factors.append(0.3)
        else:
            confidence_factors.append(0.1)
        
        # Factor in total attempts
        if total_attempts >= 10:
            confidence_factors.append(0.3)
        elif total_attempts >= 5:
            confidence_factors.append(0.2)
        else:
            confidence_factors.append(0.1)
        
        # Factor in score consistency (simplified)
        if avg_score > 0:
            confidence_factors.append(0.3)
        
        return sum(confidence_factors)
    
    def _get_alternative_difficulties(self, recommended: str, avg_score: float) -> List[str]:
        """Get alternative difficulty recommendations"""
        alternatives = []
        
        if recommended == 'medium':
            if avg_score > 85:
                alternatives.append('hard')
            if avg_score < 60:
                alternatives.append('easy')
        elif recommended == 'hard':
            if avg_score < 75:
                alternatives.append('medium')
        elif recommended == 'easy':
            if avg_score > 80:
                alternatives.append('medium')
        
        return alternatives
    
    def _suggest_difficulty_adaptations(self, difficulty: str, user: User) -> List[str]:
        """Suggest ways to adapt difficulty for user"""
        suggestions = {
            'easy': [
                "Focus on building confidence with basic concepts",
                "Gradually increase challenge as comfort level improves"
            ],
            'medium': [
                "Balance practice between familiar and new concepts",
                "Increase difficulty gradually based on performance"
            ],
            'hard': [
                "Ensure solid foundation before advancing",
                "Provide additional support resources when needed"
            ]
        }
        return suggestions.get(difficulty, [])
    
    def _calculate_average_question_length(self, question_bank: Dict) -> float:
        """Calculate average question text length"""
        all_questions = []
        for questions_list in question_bank['questions_by_type'].values():
            all_questions.extend(questions_list)
        
        if not all_questions:
            return 0
        
        total_length = sum(len(q.get('text', '')) for q in all_questions)
        return total_length / len(all_questions)
    
    def _determine_performance_level(self, score: float) -> str:
        """Determine performance level based on score"""
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'good'
        elif score >= 70:
            return 'satisfactory'
        elif score >= 60:
            return 'needs_improvement'
        else:
            return 'poor'
    
    def _analyze_performance_by_area(self, questions_answered: List[Dict]) -> Dict[str, Any]:
        """Analyze performance by topic area"""
        area_performance = {}
        
        for question in questions_answered:
            topic = question.get('topic', 'general')
            is_correct = question.get('is_correct', False)
            
            if topic not in area_performance:
                area_performance[topic] = {'correct': 0, 'total': 0}
            
            area_performance[topic]['total'] += 1
            if is_correct:
                area_performance[topic]['correct'] += 1
        
        # Calculate percentages
        for topic in area_performance:
            total = area_performance[topic]['total']
            correct = area_performance[topic]['correct']
            area_performance[topic]['percentage'] = (correct / total) * 100 if total > 0 else 0
        
        return area_performance
    
    def _identify_strengths(self, area_performance: Dict[str, Any]) -> List[str]:
        """Identify user's strengths based on performance"""
        strengths = []
        
        for topic, data in area_performance.items():
            if data['percentage'] >= 80:
                strengths.append(f"Strong understanding of {topic}")
            elif data['percentage'] >= 70:
                strengths.append(f"Good grasp of {topic}")
        
        return strengths
    
    def _identify_improvement_areas(self, area_performance: Dict[str, Any]) -> List[str]:
        """Identify areas needing improvement"""
        improvements = []
        
        for topic, data in area_performance.items():
            if data['percentage'] < 60:
                improvements.append(f"{topic} needs additional practice")
            elif data['percentage'] < 75:
                improvements.append(f"Improve understanding of {topic}")
        
        return improvements
    
    def _generate_learning_recommendations(self, user: User, area_performance: Dict, 
                                         assessment_results: Dict) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Recommendations based on weak areas
        weak_areas = [topic for topic, data in area_performance.items() 
                     if data['percentage'] < 70]
        
        if weak_areas:
            recommendations.append(f"Focus study time on: {', '.join(weak_areas)}")
        
        # Recommendations based on overall performance
        overall_score = assessment_results.get('score', 0)
        if overall_score < 70:
            recommendations.append("Consider reviewing fundamental concepts before advanced topics")
        elif overall_score > 85:
            recommendations.append("Ready to tackle more challenging material")
        
        return recommendations
    
    def _suggest_next_steps(self, user: User, assessment_results: Dict, 
                          area_performance: Dict) -> List[str]:
        """Suggest next steps based on assessment results"""
        next_steps = []
        
        overall_score = assessment_results.get('score', 0)
        
        if overall_score < 60:
            next_steps.append("Review the learning materials for areas with low scores")
            next_steps.append("Practice with additional exercises in weak areas")
        elif overall_score < 80:
            next_steps.append("Continue with the next module while reviewing weak areas")
        else:
            next_steps.append("Proceed to the next learning module")
            next_steps.append("Consider taking on more challenging practice problems")
        
        return next_steps


# Import uuid for generating unique IDs
import uuid