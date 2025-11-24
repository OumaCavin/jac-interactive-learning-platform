"""
Content Curator Agent

Specialized agent responsible for curating, organizing, and managing learning content
in the JAC Interactive Learning Platform.
"""

from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from .base_agent import BaseAgent, AgentStatus, TaskPriority
from ..learning.models import LearningPath, Module, Lesson
from ..content.models import Content, ContentRecommendation, ContentAnalytics


class ContentCuratorAgent(BaseAgent):
    """
    Content Curator Agent handles:
    - Content curation and organization
    - Learning path optimization
    - Content recommendation
    - Module structure management
    - Learning material validation
    """
    
    def __init__(self, agent_id: str = None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id=agent_id or "content_curator",
            agent_type="Content Curator",
            config=config or {}
        )
        
        self.content_database = {}
        self.learning_paths = {}
        self.recommendation_weights = {
            'difficulty': 0.3,
            'relevance': 0.4,
            'user_preference': 0.2,
            'completion_rate': 0.1
        }
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process content curation tasks
        
        Expected task types:
        - 'curate_content': Organize and categorize learning content
        - 'recommend_content': Generate personalized content recommendations
        - 'optimize_learning_path': Optimize learning path structure
        - 'validate_content': Validate content quality and structure
        - 'generate_content_outline': Create structured content outlines
        """
        self.update_status(AgentStatus.PROCESSING)
        
        task_type = task.get('type', 'curate_content')
        
        try:
            if task_type == 'curate_content':
                result = self._curate_content(task.get('params', {}))
            elif task_type == 'recommend_content':
                result = self._recommend_content(task.get('params', {}))
            elif task_type == 'optimize_learning_path':
                result = self._optimize_learning_path(task.get('params', {}))
            elif task_type == 'validate_content':
                result = self._validate_content(task.get('params', {}))
            elif task_type == 'generate_content_outline':
                result = self._generate_content_outline(task.get('params', {}))
            else:
                result = {'error': f'Unknown task type: {task_type}'}
            
            self.update_status(AgentStatus.ACTIVE)
            self.update_metrics('tasks_completed', self.metrics.get('tasks_completed', 0) + 1)
            return {'success': True, 'result': result}
            
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return {'success': False, 'error': str(e)}
    
    def _curate_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Curate and organize learning content"""
        topic = params.get('topic', '')
        difficulty_level = params.get('difficulty', 'beginner')
        content_type = params.get('content_type', 'lesson')
        
        # Simulate content curation process
        curated_items = []
        
        # Filter and organize content based on criteria
        content_items = Content.objects.filter(
            topic__icontains=topic,
            difficulty_level=difficulty_level,
            content_type=content_type,
            is_published=True
        ).order_by('-created_at')[:10]
        
        for item in content_items:
            curated_items.append({
                'id': str(item.id),
                'title': item.title,
                'description': item.description,
                'difficulty': item.difficulty_level,
                'estimated_time': item.estimated_duration,
                'tags': item.tags,
                'relevance_score': self._calculate_relevance(item, topic),
                'quality_score': item.quality_rating or 0
            })
        
        return {
            'curated_content': curated_items,
            'total_items': len(curated_items),
            'topic': topic,
            'difficulty': difficulty_level,
            'curated_at': timezone.now().isoformat()
        }
    
    def _recommend_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized content recommendations"""
        user = params.get('user')
        current_module = params.get('current_module')
        learning_style = params.get('learning_style', 'visual')
        
        if not user:
            return {'error': 'User parameter required for recommendations'}
        
        recommendations = []
        
        # Get user's learning history and preferences
        user_progress = Content.objects.filter(
            learning_path__user=user,
            status='completed'
        ).order_by('-updated_at')[:5]
        
        # Analyze learning patterns
        preferred_difficulty = self._analyze_preferred_difficulty(user_progress)
        preferred_topics = self._extract_preferred_topics(user_progress)
        
        # Generate recommendations based on patterns
        candidate_content = Content.objects.filter(
            is_published=True,
            difficulty_level=preferred_difficulty
        ).exclude(
            id__in=Content.objects.filter(
                learning_path__user=user
            ).values_list('content_id', flat=True)
        )[:20]
        
        for content in candidate_content:
            score = self._calculate_recommendation_score(
                content, user, current_module, learning_style
            )
            recommendations.append({
                'content_id': str(content.id),
                'title': content.title,
                'description': content.description,
                'difficulty': content.difficulty_level,
                'estimated_time': content.estimated_duration,
                'match_score': score,
                'reason': self._generate_recommendation_reason(content, user)
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        return {
            'recommendations': recommendations[:10],
            'learning_style': learning_style,
            'preferred_difficulty': preferred_difficulty,
            'generated_at': timezone.now().isoformat()
        }
    
    def _optimize_learning_path(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize learning path structure and progression"""
        learning_path_id = params.get('learning_path_id')
        
        if not learning_path_id:
            return {'error': 'Learning path ID required'}
        
        try:
            learning_path = LearningPath.objects.get(id=learning_path_id)
        except LearningPath.DoesNotExist:
            return {'error': 'Learning path not found'}
        
        # Analyze current path structure
        modules = Content.objects.filter(learning_path=learning_path).order_by('order')
        
        optimization_suggestions = []
        
        # Check for dependency issues
        dependency_issues = self._analyze_dependencies(modules)
        if dependency_issues:
            optimization_suggestions.extend(dependency_issues)
        
        # Check for pacing issues
        pacing_issues = self._analyze_pacing(modules)
        if pacing_issues:
            optimization_suggestions.extend(pacing_issues)
        
        # Check for difficulty progression
        difficulty_progression = self._analyze_difficulty_progression(modules)
        if difficulty_progression:
            optimization_suggestions.append(difficulty_progression)
        
        # Generate optimized path structure
        optimized_modules = self._generate_optimized_sequence(modules)
        
        return {
            'current_modules_count': modules.count(),
            'optimization_suggestions': optimization_suggestions,
            'optimized_sequence': [
                {
                    'module_id': str(m.id),
                    'title': m.title,
                    'order': idx + 1,
                    'estimated_duration': m.estimated_duration
                }
                for idx, m in enumerate(optimized_modules)
            ],
            'optimization_score': self._calculate_optimization_score(modules, optimized_modules)
        }
    
    def _validate_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content quality and structure"""
        content_id = params.get('content_id')
        
        if not content_id:
            return {'error': 'Content ID required for validation'}
        
        try:
            content = Content.objects.get(content_id=content_id)
        except Module.DoesNotExist:
            return {'error': 'Content not found'}
        
        validation_results = {
            'content_id': content_id,
            'title': content.title,
            'validation_score': 0,
            'issues': [],
            'recommendations': [],
            'structure_valid': True,
            'quality_metrics': {}
        }
        
        # Validate title
        if not content.title or len(content.title.strip()) < 5:
            validation_results['issues'].append('Title too short or missing')
        
        # Validate description
        if not content.description or len(content.description.strip()) < 50:
            validation_results['issues'].append('Description too short or missing')
        
        # Validate difficulty level
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if content.difficulty_level not in valid_difficulties:
            validation_results['issues'].append('Invalid difficulty level')
        
        # Calculate quality metrics
        quality_score = self._calculate_content_quality(content)
        validation_results['quality_metrics'] = quality_score
        validation_results['validation_score'] = quality_score['overall_score']
        
        # Generate recommendations
        recommendations = self._generate_content_recommendations(content)
        validation_results['recommendations'] = recommendations
        
        return validation_results
    
    def _generate_content_outline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured content outlines"""
        topic = params.get('topic', '')
        target_audience = params.get('target_audience', 'beginner')
        duration = params.get('duration', 60)  # minutes
        learning_objectives = params.get('learning_objectives', [])
        
        outline = {
            'topic': topic,
            'target_audience': target_audience,
            'estimated_duration': duration,
            'learning_objectives': learning_objectives,
            'sections': [],
            'total_sections': 0,
            'generated_at': timezone.now().isoformat()
        }
        
        # Generate outline sections based on topic and duration
        sections_count = max(3, min(8, duration // 10))  # 10 minutes per section
        
        for i in range(sections_count):
            section = {
                'section_number': i + 1,
                'title': self._generate_section_title(topic, i),
                'estimated_duration': duration // sections_count,
                'subsections': self._generate_subsections(topic, target_audience),
                'learning_activities': self._suggest_learning_activities(topic, i),
                'assessment_points': self._suggest_assessment_points(topic, i)
            }
            outline['sections'].append(section)
        
        outline['total_sections'] = len(outline['sections'])
        
        return outline
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities provided by this agent"""
        return [
            'content_curation',
            'content_recommendation',
            'learning_path_optimization',
            'content_validation',
            'content_outline_generation',
            'quality_assessment',
            'dependency_analysis',
            'pacing_optimization'
        ]
    
    def get_specialization_info(self) -> Dict[str, Any]:
        """Get detailed information about Content Curator specialization"""
        return {
            'agent_type': 'Content Curator',
            'specialization': 'Content Management and Curation',
            'key_responsibilities': [
                'Curate and organize learning content',
                'Generate personalized recommendations',
                'Optimize learning path structures',
                'Validate content quality',
                'Create structured content outlines'
            ],
            'expertise_areas': [
                'Learning design',
                'Content strategy',
                'Educational psychology',
                'Curriculum development',
                'Learning analytics'
            ],
            'supported_formats': ['lesson', 'exercise', 'quiz', 'project', 'case_study'],
            'optimization_algorithms': [
                'Difficulty progression analysis',
                'Dependency mapping',
                'Pacing optimization',
                'Learning style matching'
            ]
        }
    
    # Helper methods for content processing
    def _calculate_relevance(self, content: Module, topic: str) -> float:
        """Calculate content relevance score"""
        if not topic:
            return 0.5
        
        # Simple relevance calculation based on title and description
        topic_words = topic.lower().split()
        content_text = f"{content.title} {content.description}".lower()
        
        matches = sum(1 for word in topic_words if word in content_text)
        return min(1.0, matches / max(len(topic_words), 1))
    
    def _analyze_preferred_difficulty(self, user_progress) -> str:
        """Analyze user's preferred difficulty level"""
        if not user_progress:
            return 'beginner'
        
        completed_difficulties = [m.content.difficulty_level for m in user_progress if m.content]
        if not completed_difficulties:
            return 'beginner'
        
        # Return the most common difficulty level
        from collections import Counter
        difficulty_counts = Counter(completed_difficulties)
        return difficulty_counts.most_common(1)[0][0]
    
    def _extract_preferred_topics(self, user_progress) -> List[str]:
        """Extract preferred topics from user progress"""
        topics = []
        for module in user_progress:
            if module.content and module.content.tags:
                topics.extend(module.content.tags)
        return list(set(topics))
    
    def _calculate_recommendation_score(self, content, user, current_module, learning_style) -> float:
        """Calculate recommendation score for content"""
        score = 0.0
        
        # Difficulty matching
        if hasattr(user, 'learningprofile'):
            target_difficulty = user.learningprofile.preferred_difficulty
            if content.difficulty_level == target_difficulty:
                score += 0.3
        
        # Learning style matching
        if content.content_type == learning_style:
            score += 0.2
        
        # Topic relevance
        if current_module and hasattr(current_module, 'content'):
            if content.topic == current_module.content.topic:
                score += 0.4
        
        # Content quality
        if content.quality_rating:
            score += (content.quality_rating / 5.0) * 0.1
        
        return min(1.0, score)
    
    def _generate_recommendation_reason(self, content, user) -> str:
        """Generate human-readable recommendation reason"""
        reasons = []
        
        if content.difficulty_level == 'beginner':
            reasons.append("recommended for beginners")
        
        if content.estimated_duration <= 30:
            reasons.append("short duration for quick learning")
        
        if content.quality_rating and content.quality_rating >= 4:
            reasons.append("highly rated content")
        
        return "; ".join(reasons) if reasons else "matches your learning profile"
    
    def _analyze_dependencies(self, modules) -> List[Dict[str, Any]]:
        """Analyze dependency issues in learning path"""
        issues = []
        module_dict = {m.id: m for m in modules}
        
        for module in modules:
            # Check for circular dependencies
            if self._has_circular_dependency(module, module_dict):
                issues.append({
                    'type': 'circular_dependency',
                    'module': module.title,
                    'severity': 'high',
                    'description': f"Module '{module.title}' has circular dependencies"
                })
        
        return issues
    
    def _has_circular_dependency(self, module, module_dict) -> bool:
        """Check if module has circular dependencies"""
        visited = set()
        path = set()
        
        def dfs(current_id):
            if current_id in path:
                return True
            if current_id in visited:
                return False
            
            visited.add(current_id)
            path.add(current_id)
            
            current_module = module_dict.get(current_id)
            if current_module and hasattr(current_module, 'dependencies'):
                for dep_id in current_module.dependencies:
                    if dfs(dep_id):
                        return True
            
            path.remove(current_id)
            return False
        
        return dfs(module.id)
    
    def _analyze_pacing(self, modules) -> List[Dict[str, Any]]:
        """Analyze pacing issues in learning path"""
        issues = []
        total_duration = sum(m.estimated_duration or 0 for m in modules)
        
        if total_duration > 480:  # 8 hours
            issues.append({
                'type': 'pacing',
                'issue': 'too_long',
                'severity': 'medium',
                'description': f"Learning path is too long ({total_duration} minutes)",
                'recommendation': "Consider breaking into multiple paths"
            })
        
        # Check for uneven pacing
        durations = [m.estimated_duration or 0 for m in modules if m.estimated_duration]
        if len(durations) > 2:
            avg_duration = sum(durations) / len(durations)
            long_modules = [d for d in durations if d > avg_duration * 2]
            if long_modules:
                issues.append({
                    'type': 'pacing',
                    'issue': 'uneven_pacing',
                    'severity': 'low',
                    'description': f"Some modules are significantly longer than others",
                    'recommendation': "Consider breaking long modules into smaller chunks"
                })
        
        return issues
    
    def _analyze_difficulty_progression(self, modules) -> Optional[Dict[str, Any]]:
        """Analyze difficulty progression in learning path"""
        difficulties = [m.difficulty_level for m in modules if m.difficulty_level]
        if len(difficulties) < 2:
            return None
        
        difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        progression = [difficulty_order.get(d, 0) for d in difficulties]
        
        # Check for too steep progression
        steep_increases = 0
        for i in range(1, len(progression)):
            if progression[i] - progression[i-1] > 1:
                steep_increases += 1
        
        if steep_increases > len(progression) * 0.3:
            return {
                'type': 'difficulty_progression',
                'issue': 'too_steep',
                'severity': 'medium',
                'description': "Difficulty progression may be too steep",
                'recommendation': "Consider adding intermediate-level modules"
            }
        
        return None
    
    def _generate_optimized_sequence(self, modules) -> List:
        """Generate optimized module sequence"""
        # Simple optimization - sort by difficulty and estimated duration
        return sorted(modules, key=lambda m: (
            {'beginner': 0, 'intermediate': 1, 'advanced': 2}.get(m.difficulty_level, 1),
            m.estimated_duration or 0
        ))
    
    def _calculate_optimization_score(self, original_modules, optimized_modules) -> float:
        """Calculate optimization improvement score"""
        # Simplified scoring based on difficulty progression
        original_scores = self._get_difficulty_progression_score(original_modules)
        optimized_scores = self._get_difficulty_progression_score(optimized_modules)
        
        if original_scores == 0:
            return 1.0  # If no progression, any optimization is good
        
        improvement = (optimized_scores - original_scores) / original_scores
        return max(0.0, min(1.0, 0.5 + improvement))
    
    def _get_difficulty_progression_score(self, modules) -> float:
        """Calculate difficulty progression score"""
        difficulties = [m.difficulty_level for m in modules if m.difficulty_level]
        if len(difficulties) < 2:
            return 0
        
        difficulty_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        progression = [difficulty_order.get(d, 0) for d in difficulties]
        
        # Score based on smooth progression
        smooth_progressions = 0
        for i in range(1, len(progression)):
            diff = progression[i] - progression[i-1]
            if diff >= 0 and diff <= 1:  # Gradual or no increase
                smooth_progressions += 1
        
        return smooth_progressions / (len(progression) - 1)
    
    def _calculate_content_quality(self, content) -> Dict[str, Any]:
        """Calculate content quality metrics"""
        metrics = {
            'completeness_score': 0,
            'clarity_score': 0,
            'engagement_score': 0,
            'accuracy_score': 0,
            'overall_score': 0
        }
        
        # Completeness (presence of required fields)
        required_fields = ['title', 'description', 'difficulty_level']
        complete_fields = sum(1 for field in required_fields if getattr(content, field))
        metrics['completeness_score'] = complete_fields / len(required_fields)
        
        # Clarity (length and structure indicators)
        description_length = len(content.description or "")
        metrics['clarity_score'] = min(1.0, description_length / 200)  # Assume 200 chars is good
        
        # Engagement (tags and content type)
        has_tags = bool(content.tags)
        metrics['engagement_score'] = 0.8 if has_tags else 0.3
        
        # Quality rating
        metrics['accuracy_score'] = (content.quality_rating or 3) / 5.0
        
        # Overall score
        metrics['overall_score'] = sum(metrics.values()) / 4
        
        return metrics
    
    def _generate_content_recommendations(self, content) -> List[str]:
        """Generate recommendations for content improvement"""
        recommendations = []
        
        if len(content.title or "") < 10:
            recommendations.append("Consider making the title more descriptive")
        
        if len(content.description or "") < 100:
            recommendations.append("Expand the description to provide more context")
        
        if not content.tags:
            recommendations.append("Add relevant tags to improve discoverability")
        
        if content.quality_rating and content.quality_rating < 3:
            recommendations.append("Consider reviewing and improving content quality")
        
        return recommendations
    
    def _generate_section_title(self, topic: str, section_num: int) -> str:
        """Generate a section title for content outline"""
        section_templates = [
            f"Introduction to {topic}",
            f"Fundamental Concepts of {topic}",
            f"Advanced {topic} Techniques",
            f"Practical Applications of {topic}",
            f"Best Practices in {topic}",
            f"Real-world Examples",
            f"Case Studies",
            f"Summary and Next Steps"
        ]
        
        if section_num < len(section_templates):
            return section_templates[section_num]
        else:
            return f"{topic} - Part {section_num + 1}"
    
    def _generate_subsections(self, topic: str, target_audience: str) -> List[str]:
        """Generate subsections for a content section"""
        base_subsections = [
            "Learning Objectives",
            "Key Concepts",
            "Practical Examples",
            "Exercises",
            "Summary"
        ]
        return [f"{subsection}" for subsection in base_subsections]
    
    def _suggest_learning_activities(self, topic: str, section_num: int) -> List[str]:
        """Suggest learning activities for a section"""
        activities = [
            "Interactive coding exercises",
            "Problem-solving challenges",
            "Group discussions",
            "Peer review activities",
            "Real-world projects"
        ]
        
        # Rotate activities based on section
        return activities[section_num % len(activities):] + activities[:section_num % len(activities)]
    
    def _suggest_assessment_points(self, topic: str, section_num: int) -> List[str]:
        """Suggest assessment points for a section"""
        assessments = [
            "Knowledge check quiz",
            "Practical application task",
            "Peer assessment",
            "Self-reflection exercise",
            "Project milestone review"
        ]
        
        return assessments[section_num % len(assessments):] + assessments[:section_num % len(assessments)]