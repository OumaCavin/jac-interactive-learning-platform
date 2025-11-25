"""
Progress Tracker Agent

Specialized agent responsible for tracking user progress, providing analytics,
and generating insights about learning journey in the JAC Interactive Learning Platform.
"""

from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count, Q, Sum, F
from datetime import datetime, timedelta
import uuid
import numpy as np
import statistics
from collections import defaultdict, Counter
from .base_agent import BaseAgent, AgentStatus, TaskPriority
from ..learning.models import LearningPath, Module, UserModuleProgress, UserLearningPath, AssessmentAttempt


class ProgressTrackerAgent(BaseAgent):
    """
    Progress Tracker Agent handles:
    - User progress tracking
    - Learning analytics
    - Progress visualization
    - Achievement tracking
    - Learning pathway optimization
    - Performance trend analysis
    """
    
    def __init__(self, agent_id: str = None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id=agent_id or "progress_tracker",
            agent_type="Progress Tracker",
            config=config or {}
        )
        
        self.progress_metrics = {
            'completion_rate': {
                'weight': 0.25,
                'description': 'Percentage of modules completed'
            },
            'accuracy_rate': {
                'weight': 0.25,
                'description': 'Accuracy in assessments and exercises'
            },
            'time_efficiency': {
                'weight': 0.20,
                'description': 'Time taken vs estimated time'
            },
            'engagement_level': {
                'weight': 0.15,
                'description': 'Frequency and consistency of learning'
            },
            'skill_development': {
                'weight': 0.15,
                'description': 'Progression in skill complexity'
            }
        }
        
        self.achievement_categories = {
            'completion_achievements': ['first_module', 'path_completer', 'perfect_score'],
            'effort_achievements': ['consistent_learner', 'early_bird', 'night_owl'],
            'skill_achievements': ['debugger', 'problem_solver', 'code_master'],
            'collaboration_achievements': ['helper', 'mentor', 'peer_learner'],
            'milestone_achievements': ['week_warrior', 'month_master', 'streak_legend']
        }
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process progress tracking tasks
        
        Expected task types:
        - 'track_progress': Track user progress in learning path
        - 'generate_analytics': Generate learning analytics
        - 'create_progress_report': Create detailed progress report
        - 'analyze_trends': Analyze learning trends
        - 'track_achievements': Track and award achievements
        - 'optimize_path': Optimize learning path based on progress
        - 'predict_completion': Predict learning path completion
        - 'generate_insights': Generate learning insights
        """
        self.update_status(AgentStatus.PROCESSING)
        
        task_type = task.get('type', 'track_progress')
        
        try:
            if task_type == 'track_progress':
                result = self._track_progress(task.get('params', {}))
            elif task_type == 'generate_analytics':
                result = self._generate_analytics(task.get('params', {}))
            elif task_type == 'create_progress_report':
                result = self._create_progress_report(task.get('params', {}))
            elif task_type == 'analyze_trends':
                result = self._analyze_trends(task.get('params', {}))
            elif task_type == 'track_achievements':
                result = self._track_achievements(task.get('params', {}))
            elif task_type == 'optimize_path':
                result = self._optimize_learning_path(task.get('params', {}))
            elif task_type == 'predict_completion':
                result = self._predict_completion(task.get('params', {}))
            elif task_type == 'generate_insights':
                result = self._generate_insights(task.get('params', {}))
            elif task_type == 'create_visualization_data':
                result = self._create_visualization_data(task.get('params', {}))
            else:
                result = {'error': f'Unknown task type: {task_type}'}
            
            self.update_status(AgentStatus.ACTIVE)
            self.update_metrics('tracking_operations', self.metrics.get('tracking_operations', 0) + 1)
            return {'success': True, 'result': result}
            
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return {'success': False, 'error': str(e)}
    
    def _track_progress(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Track user's progress in learning path"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        tracking_scope = params.get('scope', 'comprehensive')  # basic, detailed, comprehensive
        
        if not user:
            return {'error': 'User parameter required for progress tracking'}
        
        # Get current progress data
        progress_data = self._collect_progress_data(user, learning_path_id)
        
        # Calculate progress metrics
        progress_metrics = self._calculate_progress_metrics(progress_data)
        
        # Generate progress summary
        progress_summary = {
            'tracking_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'tracking_date': timezone.now().isoformat(),
            'tracking_scope': tracking_scope,
            'overall_progress': 0,
            'completion_percentage': 0,
            'current_level': '',
            'next_milestone': '',
            'estimated_completion': None,
            'progress_metrics': progress_metrics,
            'detailed_breakdown': {},
            'recent_activities': [],
            'performance_summary': {},
            'recommendations': []
        }
        
        # Calculate overall progress
        progress_summary['overall_progress'] = self._calculate_overall_progress(progress_metrics)
        progress_summary['completion_percentage'] = progress_summary['overall_progress']['completion_rate']
        
        # Determine current level
        progress_summary['current_level'] = self._determine_learning_level(
            progress_summary['overall_progress']
        )
        
        # Identify next milestone
        progress_summary['next_milestone'] = self._identify_next_milestone(
            progress_data, progress_summary['overall_progress']
        )
        
        # Predict completion
        progress_summary['estimated_completion'] = self._estimate_completion_date(
            progress_data, progress_summary['overall_progress']
        )
        
        # Generate detailed breakdown
        progress_summary['detailed_breakdown'] = self._generate_detailed_breakdown(
            progress_data, progress_metrics
        )
        
        # Add recent activities
        progress_summary['recent_activities'] = self._get_recent_activities(
            user, learning_path_id, days=7
        )
        
        # Performance summary
        progress_summary['performance_summary'] = self._generate_performance_summary(
            progress_data
        )
        
        # Generate recommendations
        progress_summary['recommendations'] = self._generate_progress_recommendations(
            progress_data, progress_summary
        )
        
        return progress_summary
    
    def _generate_analytics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive learning analytics"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        time_period = params.get('time_period', 30)  # days
        analytics_type = params.get('analytics_type', 'comprehensive')  # basic, performance, engagement
        
        if not user:
            return {'error': 'User parameter required for analytics generation'}
        
        # Collect analytics data
        analytics_data = self._collect_analytics_data(user, learning_path_id, time_period)
        
        analytics_report = {
            'analytics_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'time_period_days': time_period,
            'analytics_type': analytics_type,
            'generation_date': timezone.now().isoformat(),
            'summary_metrics': {},
            'performance_analytics': {},
            'engagement_analytics': {},
            'learning_analytics': {},
            'comparative_analysis': {},
            'trends': {},
            'insights': [],
            'alerts': []
        }
        
        # Generate summary metrics
        analytics_report['summary_metrics'] = self._generate_summary_metrics(analytics_data)
        
        if analytics_type in ['performance', 'comprehensive']:
            # Performance analytics
            analytics_report['performance_analytics'] = self._generate_performance_analytics(
                analytics_data
            )
        
        if analytics_type in ['engagement', 'comprehensive']:
            # Engagement analytics
            analytics_report['engagement_analytics'] = self._generate_engagement_analytics(
                analytics_data
            )
        
        if analytics_type in ['learning', 'comprehensive']:
            # Learning analytics
            analytics_report['learning_analytics'] = self._generate_learning_analytics(
                analytics_data
            )
        
        # Comparative analysis
        analytics_report['comparative_analysis'] = self._generate_comparative_analysis(
            analytics_data, user
        )
        
        # Identify trends
        analytics_report['trends'] = self._identify_learning_trends(analytics_data)
        
        # Generate insights
        analytics_report['insights'] = self._generate_analytics_insights(analytics_report)
        
        # Generate alerts
        analytics_report['alerts'] = self._generate_analytics_alerts(analytics_report)
        
        return analytics_report
    
    def _create_progress_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed progress report"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        report_format = params.get('format', 'student')  # student, instructor, parent
        include_recommendations = params.get('include_recommendations', True)
        
        if not user:
            return {'error': 'User parameter required for progress report'}
        
        # Gather comprehensive report data
        report_data = self._gather_report_data(user, learning_path_id)
        
        # Create report structure
        progress_report = {
            'report_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'report_format': report_format,
            'report_date': timezone.now().isoformat(),
            'report_period': self._determine_report_period(report_data),
            'executive_summary': {},
            'progress_overview': {},
            'detailed_analysis': {},
            'performance_metrics': {},
            'achievements': {},
            'challenges': [],
            'recommendations': [],
            'next_steps': []
        }
        
        # Generate executive summary based on report format
        progress_report['executive_summary'] = self._generate_executive_summary(
            report_data, report_format
        )
        
        # Progress overview
        progress_report['progress_overview'] = self._create_progress_overview(report_data)
        
        # Detailed analysis
        progress_report['detailed_analysis'] = self._create_detailed_analysis(report_data)
        
        # Performance metrics
        progress_report['performance_metrics'] = self._compile_performance_metrics(report_data)
        
        # Achievements section
        progress_report['achievements'] = self._compile_achievements(report_data, report_format)
        
        # Challenges identification
        progress_report['challenges'] = self._identify_challenges(report_data)
        
        if include_recommendations:
            # Recommendations
            progress_report['recommendations'] = self._generate_report_recommendations(
                report_data, report_format
            )
            
            # Next steps
            progress_report['next_steps'] = self._suggest_next_steps(
                report_data, progress_report
            )
        
        return progress_report
    
    def _analyze_trends(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze learning trends and patterns"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        trend_period = params.get('period', 60)  # days
        trend_types = params.get('trend_types', ['performance', 'engagement', 'completion'])
        
        if not user:
            return {'error': 'User parameter required for trend analysis'}
        
        # Collect trend data
        trend_data = self._collect_trend_data(user, learning_path_id, trend_period)
        
        trend_analysis = {
            'analysis_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'analysis_date': timezone.now().isoformat(),
            'trend_period_days': trend_period,
            'analyzed_trends': trend_types,
            'trend_results': {},
            'pattern_analysis': {},
            'predictions': {},
            'recommendations': []
        }
        
        # Analyze each trend type
        for trend_type in trend_types:
            trend_result = self._analyze_specific_trend(
                trend_data, trend_type
            )
            trend_analysis['trend_results'][trend_type] = trend_result
        
        # Pattern analysis
        trend_analysis['pattern_analysis'] = self._analyze_learning_patterns(trend_data)
        
        # Generate predictions
        trend_analysis['predictions'] = self._generate_trend_predictions(trend_data, trend_analysis)
        
        # Recommendations based on trends
        trend_analysis['recommendations'] = self._generate_trend_recommendations(
            trend_analysis
        )
        
        return trend_analysis
    
    def _track_achievements(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Track and award achievements"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        achievement_types = params.get('types', 'all')  # all, specific category
        
        if not user:
            return {'error': 'User parameter required for achievement tracking'}
        
        # Get user's current achievements
        current_achievements = self._get_user_achievements(user, learning_path_id)
        
        # Check for new achievements
        new_achievements = self._check_new_achievements(
            user, learning_path_id, current_achievements
        )
        
        achievement_summary = {
            'tracking_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'tracking_date': timezone.now().isoformat(),
            'previous_achievements': current_achievements,
            'new_achievements': new_achievements,
            'total_achievements': len(current_achievements) + len(new_achievements),
            'achievement_breakdown': {},
            'recent_milestones': [],
            'next_potential_achievements': [],
            'achievement_recommendations': []
        }
        
        # Achievement breakdown by category
        achievement_summary['achievement_breakdown'] = self._categorize_achievements(
            achievement_summary['total_achievements']
        )
        
        # Recent milestones
        achievement_summary['recent_milestones'] = self._identify_recent_milestones(
            user, learning_path_id
        )
        
        # Next potential achievements
        achievement_summary['next_potential_achievements'] = self._suggest_next_achievements(
            user, learning_path_id, achievement_summary
        )
        
        # Achievement recommendations
        achievement_summary['achievement_recommendations'] = self._generate_achievement_recommendations(
            achievement_summary
        )
        
        return achievement_summary
    
    def _optimize_learning_path(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize learning path based on progress data"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        optimization_goals = params.get('goals', ['efficiency', 'engagement'])  # efficiency, engagement, mastery
        
        if not user or not learning_path_id:
            return {'error': 'User and learning path ID required for optimization'}
        
        # Analyze current path performance
        current_performance = self._analyze_path_performance(user, learning_path_id)
        
        # Generate optimization recommendations
        optimization_result = {
            'optimization_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'optimization_date': timezone.now().isoformat(),
            'optimization_goals': optimization_goals,
            'current_performance': current_performance,
            'optimization_suggestions': [],
            'path_modifications': [],
            'estimated_improvements': {},
            'implementation_plan': {},
            'success_metrics': {}
        }
        
        # Generate optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(
            current_performance, optimization_goals
        )
        optimization_result['optimization_suggestions'] = optimization_suggestions
        
        # Suggest path modifications
        path_modifications = self._suggest_path_modifications(
            user, learning_path_id, current_performance, optimization_goals
        )
        optimization_result['path_modifications'] = path_modifications
        
        # Estimate improvements
        optimization_result['estimated_improvements'] = self._estimate_optimization_improvements(
            current_performance, optimization_suggestions
        )
        
        # Create implementation plan
        optimization_result['implementation_plan'] = self._create_implementation_plan(
            path_modifications, optimization_suggestions
        )
        
        # Define success metrics
        optimization_result['success_metrics'] = self._define_success_metrics(
            optimization_goals
        )
        
        return optimization_result
    
    def _predict_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Predict learning path completion"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        prediction_horizon = params.get('horizon', 90)  # days
        
        if not user or not learning_path_id:
            return {'error': 'User and learning path ID required for completion prediction'}
        
        # Analyze current progress and learning patterns
        progress_data = self._collect_progress_data(user, learning_path_id)
        
        # Generate completion prediction
        completion_prediction = {
            'prediction_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'prediction_date': timezone.now().isoformat(),
            'prediction_horizon_days': prediction_horizon,
            'completion_probability': 0,
            'estimated_completion_date': None,
            'confidence_level': 0,
            'completion_timeline': {},
            'risk_factors': [],
            'accelerating_factors': [],
            'scenario_analysis': {},
            'recommendations': []
        }
        
        # Calculate completion probability
        completion_prediction['completion_probability'] = self._calculate_completion_probability(
            progress_data, prediction_horizon
        )
        
        # Estimate completion date
        completion_prediction['estimated_completion_date'] = self._estimate_completion_date(
            progress_data, prediction_horizon
        )
        
        # Calculate confidence level
        completion_prediction['confidence_level'] = self._calculate_prediction_confidence(
            progress_data
        )
        
        # Detailed completion timeline
        completion_prediction['completion_timeline'] = self._create_completion_timeline(
            progress_data, prediction_horizon
        )
        
        # Risk factors
        completion_prediction['risk_factors'] = self._identify_risk_factors(
            progress_data
        )
        
        # Accelerating factors
        completion_prediction['accelerating_factors'] = self._identify_accelerating_factors(
            progress_data
        )
        
        # Scenario analysis
        completion_prediction['scenario_analysis'] = self._analyze_completion_scenarios(
            progress_data, prediction_horizon
        )
        
        # Recommendations
        completion_prediction['recommendations'] = self._generate_completion_recommendations(
            completion_prediction
        )
        
        return completion_prediction
    
    def _generate_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning insights based on progress data"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        insight_types = params.get('types', ['performance', 'learning_patterns', 'behavioral'])
        
        if not user:
            return {'error': 'User parameter required for insight generation'}
        
        # Collect comprehensive data for insights
        insight_data = self._collect_insight_data(user, learning_path_id)
        
        insights = {
            'insight_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'generation_date': timezone.now().isoformat(),
            'insight_types': insight_types,
            'key_insights': [],
            'behavioral_insights': {},
            'performance_insights': {},
            'learning_patterns': {},
            'recommendations': [],
            'actionable_items': []
        }
        
        # Generate insights for each type
        if 'performance' in insight_types:
            insights['performance_insights'] = self._generate_performance_insights(insight_data)
        
        if 'learning_patterns' in insight_types:
            insights['learning_patterns'] = self._generate_learning_pattern_insights(insight_data)
        
        if 'behavioral' in insight_types:
            insights['behavioral_insights'] = self._generate_behavioral_insights(insight_data)
        
        # Key insights summary
        insights['key_insights'] = self._extract_key_insights(insight_data, insights)
        
        # Recommendations based on insights
        insights['recommendations'] = self._generate_insight_based_recommendations(insights)
        
        # Actionable items
        insights['actionable_items'] = self._create_actionable_items(insights)
        
        return insights
    
    def _create_visualization_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create data for progress visualizations"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        visualization_type = params.get('type', 'progress_chart')  # progress_chart, timeline, comparison
        data_points = params.get('points', 30)  # number of data points
        
        if not user:
            return {'error': 'User parameter required for visualization data'}
        
        # Collect visualization data
        viz_data = self._collect_visualization_data(user, learning_path_id, data_points)
        
        visualization_data = {
            'viz_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'learning_path_id': learning_path_id,
            'visualization_type': visualization_type,
            'data_points': data_points,
            'creation_date': timezone.now().isoformat(),
            'chart_data': {},
            'metadata': {},
            'interactive_elements': []
        }
        
        # Generate chart data based on type
        if visualization_type == 'progress_chart':
            visualization_data['chart_data'] = self._create_progress_chart_data(viz_data)
        elif visualization_type == 'timeline':
            visualization_data['chart_data'] = self._create_timeline_data(viz_data)
        elif visualization_type == 'comparison':
            visualization_data['chart_data'] = self._create_comparison_data(viz_data)
        
        # Add metadata
        visualization_data['metadata'] = {
            'chart_title': self._generate_chart_title(visualization_type),
            'data_range': self._get_data_range(viz_data),
            'summary_stats': self._calculate_summary_stats(viz_data)
        }
        
        # Interactive elements
        visualization_data['interactive_elements'] = self._define_interactive_elements(
            visualization_type
        )
        
        return visualization_data
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities provided by this agent"""
        return [
            'progress_tracking',
            'learning_analytics',
            'trend_analysis',
            'achievement_tracking',
            'performance_prediction',
            'path_optimization',
            'insight_generation',
            'data_visualization',
            'completion_prediction',
            'milestone_tracking'
        ]
    
    def get_specialization_info(self) -> Dict[str, Any]:
        """Get detailed information about Progress Tracker specialization"""
        return {
            'agent_type': 'Progress Tracker',
            'specialization': 'Progress Analytics and Tracking',
            'key_responsibilities': [
                'Track comprehensive learning progress',
                'Generate detailed analytics and reports',
                'Identify learning trends and patterns',
                'Track achievements and milestones',
                'Predict completion timelines'
            ],
            'tracking_dimensions': list(self.progress_metrics.keys()),
            'achievement_categories': list(self.achievement_categories.keys()),
            'analytics_capabilities': [
                'Performance trend analysis',
                'Engagement pattern recognition',
                'Learning velocity tracking',
                'Completion probability modeling',
                'Comparative performance analysis'
            ],
            'visualization_types': [
                'Progress charts',
                'Timeline views',
                'Performance comparisons',
                'Achievement galleries',
                'Trend analysis graphs'
            ],
            'prediction_models': [
                'Completion time prediction',
                'Performance trend forecasting',
                'Engagement level prediction',
                'Risk assessment models'
            ]
        }
    
    # Helper methods for data collection and analysis
    def _collect_progress_data(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Collect comprehensive progress data"""
        from datetime import timedelta
        
        # Time range for analysis
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)  # Last 90 days
        
        # Query progress data
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date
        ).order_by('-updated_at')
        
        if learning_path_id:
            progress_query = progress_query.filter(
                module__learning_path_id=learning_path_id
            )
        
        progress_data = list(progress_query)
        
        # Query assessment results
        assessment_query = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=start_date
        ).order_by('-completed_at')
        
        if learning_path_id:
            assessment_query = assessment_query.filter(
                assessment__learning_path_id=learning_path_id
            )
        
        assessment_data = list(assessment_query)
        
        return {
            'user': user,
            'learning_path_id': learning_path_id,
            'progress_data': progress_data,
            'assessment_data': assessment_data,
            'time_range': {'start': start_date, 'end': end_date},
            'total_activities': len(progress_data),
            'total_assessments': len(assessment_data)
        }
    
    def _calculate_progress_metrics(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate progress metrics"""
        progress_activities = progress_data['progress_data']
        assessment_activities = progress_data['assessment_data']
        
        metrics = {}
        
        # Completion rate
        completed_activities = len([p for p in progress_activities if p.status == 'completed'])
        total_activities = len(progress_activities)
        metrics['completion_rate'] = (completed_activities / max(total_activities, 1)) * 100
        
        # Accuracy rate
        assessment_scores = [a.score for a in assessment_activities if a.score]
        metrics['accuracy_rate'] = sum(assessment_scores) / max(len(assessment_scores), 1)
        
        # Time efficiency
        metrics['time_efficiency'] = self._calculate_time_efficiency(progress_activities)
        
        # Engagement level
        metrics['engagement_level'] = self._calculate_engagement_level(progress_data)
        
        # Skill development
        metrics['skill_development'] = self._assess_skill_development(progress_data)
        
        return metrics
    
    def _calculate_overall_progress(self, progress_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall progress score"""
        overall_score = 0
        for metric, value in progress_metrics.items():
            if metric in self.progress_metrics:
                weight = self.progress_metrics[metric]['weight']
                overall_score += value * weight
        
        return {
            'overall_score': overall_score,
            'completion_rate': progress_metrics.get('completion_rate', 0),
            'accuracy_rate': progress_metrics.get('accuracy_rate', 0),
            'time_efficiency': progress_metrics.get('time_efficiency', 0),
            'engagement_level': progress_metrics.get('engagement_level', 0),
            'skill_development': progress_metrics.get('skill_development', 0)
        }
    
    def _determine_learning_level(self, progress: Dict[str, Any]) -> str:
        """Determine current learning level"""
        overall_score = progress['overall_score']
        
        if overall_score >= 90:
            return 'Expert'
        elif overall_score >= 80:
            return 'Advanced'
        elif overall_score >= 70:
            return 'Intermediate'
        elif overall_score >= 60:
            return 'Developing'
        else:
            return 'Beginner'
    
    def _identify_next_milestone(self, progress_data: Dict, overall_progress: Dict) -> str:
        """Identify next learning milestone"""
        completion_rate = overall_progress['completion_rate']
        
        if completion_rate < 25:
            return "Complete your first module"
        elif completion_rate < 50:
            return "Reach 50% completion"
        elif completion_rate < 75:
            return "Complete 3/4 of the learning path"
        elif completion_rate < 100:
            return "Complete the learning path"
        else:
            return "Master advanced concepts"
    
    def _estimate_completion_date(self, progress_data: Dict, overall_progress: Dict) -> Optional[str]:
        """Estimate learning path completion date"""
        completion_rate = overall_progress['completion_rate']
        
        if completion_rate >= 100:
            return None  # Already completed
        
        # Simple estimation based on current velocity
        remaining_percentage = 100 - completion_rate
        daily_progress = completion_rate / 30  # Assume 30 days of progress
        
        if daily_progress > 0:
            days_to_completion = remaining_percentage / daily_progress
            completion_date = timezone.now() + timedelta(days=days_to_completion)
            return completion_date.isoformat()
        
        return None
    
    def _generate_detailed_breakdown(self, progress_data: Dict, progress_metrics: Dict) -> Dict[str, Any]:
        """Generate detailed progress breakdown"""
        return {
            'by_topic': self._breakdown_by_topic(progress_data),
            'by_difficulty': self._breakdown_by_difficulty(progress_data),
            'by_activity_type': self._breakdown_by_activity_type(progress_data),
            'weekly_summary': self._generate_weekly_summary(progress_data),
            'performance_trends': self._analyze_performance_trends(progress_data)
        }
    
    def _get_recent_activities(self, user: User, learning_path_id: Optional[str], days: int = 7) -> List[Dict[str, Any]]:
        """Get recent learning activities"""
        from datetime import timedelta
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        ).order_by('-updated_at')[:10]
        
        activities = []
        for progress in recent_progress:
            activities.append({
                'activity_id': str(progress.id),
                'type': 'module_completion',
                'description': f"Completed: {progress.module.title}",
                'timestamp': progress.updated_at.isoformat(),
                'score': progress.score,
                'duration': progress.time_spent
            })
        
        return activities
    
    def _generate_performance_summary(self, progress_data: Dict) -> Dict[str, Any]:
        """Generate performance summary"""
        return {
            'average_score': 85.0,  # Placeholder
            'best_performance': 95.0,  # Placeholder
            'improvement_rate': 5.0,  # Placeholder
            'consistency_rating': 'high'  # Placeholder
        }
    
    def _generate_progress_recommendations(self, progress_data: Dict, summary: Dict) -> List[str]:
        """Generate progress-based recommendations"""
        recommendations = []
        
        completion_rate = summary['overall_progress']['completion_rate']
        
        if completion_rate < 50:
            recommendations.append("Increase study frequency to maintain momentum")
            recommendations.append("Consider breaking larger modules into smaller tasks")
        elif completion_rate > 80:
            recommendations.append("Great progress! Consider taking on additional challenges")
            recommendations.append("You're ready to help other learners")
        else:
            recommendations.append("Good steady progress - maintain current pace")
            recommendations.append("Focus on mastering the current concepts before advancing")
        
        return recommendations
    
    # Placeholder implementations for other methods
    def _collect_analytics_data(self, user: User, learning_path_id: Optional[str], time_period: int) -> Dict[str, Any]:
        """Collect comprehensive analytics data"""
        start_date = timezone.now() - timedelta(days=time_period)
        end_date = timezone.now()
        
        # Query progress data
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date,
            updated_at__lte=end_date
        ).order_by('-updated_at')
        
        if learning_path_id:
            progress_query = progress_query.filter(
                module__learning_path_id=learning_path_id
            )
        
        progress_data = list(progress_query)
        
        # Query assessment results
        assessment_query = AssessmentAttempt.objects.filter(
            user=user,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        ).order_by('-completed_at')
        
        if learning_path_id:
            assessment_query = assessment_query.filter(
                assessment__learning_path_id=learning_path_id
            )
        
        assessment_data = list(assessment_query)
        
        # Calculate detailed metrics
        completion_stats = self._calculate_completion_statistics(progress_data)
        performance_stats = self._calculate_performance_statistics(assessment_data)
        engagement_stats = self._calculate_engagement_statistics(progress_data)
        velocity_stats = self._calculate_velocity_statistics(progress_data, assessment_data)
        
        return {
            'user': user,
            'learning_path_id': learning_path_id,
            'progress_data': progress_data,
            'assessment_data': assessment_data,
            'time_range': {'start': start_date, 'end': end_date},
            'total_activities': len(progress_data),
            'total_assessments': len(assessment_data),
            'completion_statistics': completion_stats,
            'performance_statistics': performance_stats,
            'engagement_statistics': engagement_stats,
            'velocity_statistics': velocity_stats
        }
    
    def _calculate_completion_statistics(self, progress_data: List) -> Dict[str, Any]:
        """Calculate detailed completion statistics"""
        if not progress_data:
            return {'completion_rate': 0, 'total_modules': 0, 'completed_modules': 0}
        
        total_modules = len(progress_data)
        completed_modules = len([p for p in progress_data if p.status == 'completed'])
        in_progress_modules = len([p for p in progress_data if p.status == 'in_progress'])
        
        # Calculate time-based completion trends
        completion_dates = [p.updated_at for p in progress_data if p.status == 'completed']
        if completion_dates:
            avg_time_to_completion = np.mean([
                (p.updated_at - (p.created_at or p.updated_at)).days 
                for p in progress_data 
                if p.status == 'completed' and hasattr(p, 'created_at')
            ])
        else:
            avg_time_to_completion = 0
        
        return {
            'completion_rate': (completed_modules / total_modules) * 100,
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'in_progress_modules': in_progress_modules,
            'avg_time_to_completion_days': round(avg_time_to_completion, 2)
        }
    
    def _calculate_performance_statistics(self, assessment_data: List) -> Dict[str, Any]:
        """Calculate detailed performance statistics"""
        if not assessment_data:
            return {'average_score': 0, 'score_variance': 0, 'improvement_trend': 'stable'}
        
        scores = [a.score for a in assessment_data if a.score is not None]
        if not scores:
            return {'average_score': 0, 'score_variance': 0, 'improvement_trend': 'stable'}
        
        # Calculate trend using linear regression
        sorted_assessments = sorted(assessment_data, key=lambda x: x.completed_at or x.started_at)
        valid_scores = [(i, a.score) for i, a in enumerate(sorted_assessments) if a.score is not None]
        
        if len(valid_scores) < 3:
            trend = 'stable'
        else:
            x_vals = [x[0] for x in valid_scores]
            y_vals = [x[1] for x in valid_scores]
            
            # Calculate slope
            n = len(valid_scores)
            x_mean = np.mean(x_vals)
            y_mean = np.mean(y_vals)
            
            numerator = sum((x_vals[i] - x_mean) * (y_vals[i] - y_mean) for i in range(n))
            denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))
            
            if denominator > 0:
                slope = numerator / denominator
                if slope > 2:
                    trend = 'improving'
                elif slope < -2:
                    trend = 'declining'
                else:
                    trend = 'stable'
            else:
                trend = 'stable'
        
        return {
            'average_score': round(np.mean(scores), 2),
            'best_score': max(scores),
            'score_variance': round(np.var(scores), 2),
            'improvement_trend': trend,
            'total_assessments': len(assessment_data)
        }
    
    def _calculate_engagement_statistics(self, progress_data: List) -> Dict[str, Any]:
        """Calculate detailed engagement statistics"""
        if not progress_data:
            return {'engagement_level': 0, 'consistency_score': 0, 'active_days': 0}
        
        # Calculate daily activity patterns
        daily_activities = defaultdict(int)
        for progress in progress_data:
            daily_activities[progress.updated_at.date()] += 1
        
        # Calculate consistency score
        activity_counts = list(daily_activities.values())
        if len(activity_counts) > 1:
            consistency_score = max(0, 100 - (np.std(activity_counts) * 20))
        else:
            consistency_score = 100
        
        # Calculate engagement level based on frequency and patterns
        total_days = (max(progress.updated_at for progress in progress_data) - 
                     min(progress.updated_at for progress in progress_data)).days + 1
        
        active_days = len(daily_activities)
        engagement_level = (active_days / max(total_days, 1)) * 100
        
        return {
            'engagement_level': round(engagement_level, 2),
            'consistency_score': round(consistency_score, 2),
            'active_days': active_days,
            'total_days': total_days,
            'avg_activities_per_active_day': round(sum(activity_counts) / max(len(activity_counts), 1), 2)
        }
    
    def _calculate_velocity_statistics(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Calculate learning velocity statistics"""
        # Daily velocity (activities per day)
        if not progress_data:
            return {'daily_velocity': 0, 'weekly_velocity': 0}
        
        total_days = max(1, (max(p.updated_at for p in progress_data) - 
                            min(p.updated_at for p in progress_data)).days)
        
        daily_velocity = len(progress_data) / total_days
        weekly_velocity = daily_velocity * 7
        
        # Weighted recent velocity (more recent activities have higher weight)
        recent_activities = [p for p in progress_data if p.updated_at >= timezone.now() - timedelta(days=7)]
        if recent_activities:
            weighted_velocity = len(recent_activities) / 7.0
        else:
            weighted_velocity = 0
        
        return {
            'daily_velocity': round(daily_velocity, 3),
            'weekly_velocity': round(weekly_velocity, 2),
            'weighted_recent_velocity': round(weighted_velocity, 3),
            'total_activities': len(progress_data)
        }
    
    def _generate_summary_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive summary metrics"""
        progress_data = data.get('progress_data', [])
        assessment_data = data.get('assessment_data', [])
        completion_stats = data.get('completion_statistics', {})
        performance_stats = data.get('performance_statistics', {})
        engagement_stats = data.get('engagement_statistics', {})
        
        # Calculate overall progress score
        completion_rate = completion_stats.get('completion_rate', 0)
        accuracy_rate = performance_stats.get('average_score', 0)
        engagement_level = engagement_stats.get('engagement_level', 0)
        
        # Weighted overall score
        overall_score = (
            completion_rate * 0.4 +
            accuracy_rate * 0.3 +
            engagement_level * 0.3
        )
        
        # Calculate learning velocity
        total_activities = len(progress_data)
        total_days = max(1, (timezone.now() - min(p.updated_at for p in progress_data)).days) if progress_data else 1
        learning_velocity = total_activities / total_days
        
        # Determine learning level based on scores
        if overall_score >= 90:
            learning_level = 'Expert'
        elif overall_score >= 80:
            learning_level = 'Advanced'
        elif overall_score >= 70:
            learning_level = 'Intermediate'
        elif overall_score >= 60:
            learning_level = 'Developing'
        else:
            learning_level = 'Beginner'
        
        return {
            'total_activities': total_activities,
            'total_assessments': len(assessment_data),
            'completion_rate': round(completion_rate, 2),
            'average_score': round(accuracy_rate, 2),
            'engagement_level': round(engagement_level, 2),
            'learning_velocity': round(learning_velocity, 3),
            'overall_score': round(overall_score, 2),
            'learning_level': learning_level,
            'active_days': engagement_stats.get('active_days', 0),
            'consistency_score': round(engagement_stats.get('consistency_score', 0), 2),
            'improvement_trend': performance_stats.get('improvement_trend', 'stable')
        }
    
    def _generate_performance_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed performance analytics"""
        assessment_data = data.get('assessment_data', [])
        if not assessment_data:
            return {'performance_score': 0, 'areas_of_strength': [], 'areas_for_improvement': []}
        
        # Analyze performance by assessment type/category
        performance_by_type = self._analyze_performance_by_type(assessment_data)
        
        # Analyze performance trends
        performance_trends = self._analyze_performance_trends(assessment_data)
        
        # Identify strength and improvement areas
        areas_of_strength, areas_for_improvement = self._identify_performance_areas(assessment_data)
        
        # Calculate performance consistency
        consistency_metrics = self._calculate_performance_consistency(assessment_data)
        
        # Generate predictive insights
        predictive_insights = self._generate_performance_predictions(assessment_data)
        
        return {
            'performance_score': self._calculate_overall_performance_score(assessment_data),
            'performance_by_type': performance_by_type,
            'performance_trends': performance_trends,
            'areas_of_strength': areas_of_strength,
            'areas_for_improvement': areas_for_improvement,
            'consistency_metrics': consistency_metrics,
            'predictive_insights': predictive_insights,
            'recommendations': self._generate_performance_recommendations(assessment_data)
        }
    
    def _analyze_performance_by_type(self, assessment_data: List) -> Dict[str, Any]:
        """Analyze performance by assessment type"""
        type_performance = defaultdict(list)
        
        for assessment in assessment_data:
            if assessment.score is not None:
                assessment_type = getattr(assessment.assessment, 'assessment_type', 'general')
                type_performance[assessment_type].append(assessment.score)
        
        performance_summary = {}
        for assessment_type, scores in type_performance.items():
            performance_summary[assessment_type] = {
                'average_score': round(np.mean(scores), 2),
                'best_score': max(scores),
                'score_variance': round(np.var(scores), 2),
                'attempt_count': len(scores)
            }
        
        return performance_summary
    
    def _analyze_performance_trends(self, assessment_data: List) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(assessment_data) < 3:
            return {'trend_direction': 'stable', 'trend_strength': 'weak'}
        
        # Sort by completion date
        sorted_assessments = sorted([a for a in assessment_data if a.completed_at], 
                                   key=lambda x: x.completed_at)
        
        scores = [a.score for a in sorted_assessments if a.score is not None]
        
        if len(scores) < 3:
            return {'trend_direction': 'stable', 'trend_strength': 'weak'}
        
        # Calculate trend using linear regression
        x_values = list(range(len(scores)))
        
        x_mean = np.mean(x_values)
        y_mean = np.mean(scores)
        
        numerator = sum((x_values[i] - x_mean) * (scores[i] - y_mean) for i in range(len(scores)))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(len(scores)))
        
        if denominator == 0:
            return {'trend_direction': 'stable', 'trend_strength': 'weak'}
        
        slope = numerator / denominator
        
        # Determine trend direction and strength
        if slope > 1:
            direction = 'improving'
            strength = 'strong' if slope > 3 else 'moderate'
        elif slope < -1:
            direction = 'declining'
            strength = 'strong' if slope < -3 else 'moderate'
        else:
            direction = 'stable'
            strength = 'weak'
        
        return {
            'trend_direction': direction,
            'trend_strength': strength,
            'slope': round(slope, 3),
            'correlation_coefficient': self._calculate_correlation_coefficient(x_values, scores)
        }
    
    def _calculate_correlation_coefficient(self, x_values: List[float], y_values: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
        
        n = len(x_values)
        x_mean = np.mean(x_values)
        y_mean = np.mean(y_values)
        
        numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
        
        x_variance = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        y_variance = sum((y_values[i] - y_mean) ** 2 for i in range(n))
        
        denominator = (x_variance * y_variance) ** 0.5
        
        if denominator == 0:
            return 0.0
        
        return round(numerator / denominator, 3)
    
    def _identify_performance_areas(self, assessment_data: List) -> tuple:
        """Identify strength and improvement areas"""
        scores_by_topic = defaultdict(list)
        
        for assessment in assessment_data:
            if assessment.score is not None:
                # Group by assessment topic/category
                topic = getattr(assessment.assessment, 'module', {}).get('title', 'General')
                scores_by_topic[topic].append(assessment.score)
        
        # Calculate average score for each topic
        topic_averages = {}
        for topic, scores in scores_by_topic.items():
            topic_averages[topic] = round(np.mean(scores), 2)
        
        # Sort topics by performance
        sorted_topics = sorted(topic_averages.items(), key=lambda x: x[1], reverse=True)
        
        # Areas of strength (top 25% of topics)
        num_topics = len(sorted_topics)
        strength_threshold = max(0, num_topics // 4)
        
        areas_of_strength = [topic for topic, score in sorted_topics[:max(1, strength_threshold)]]
        areas_for_improvement = [topic for topic, score in sorted_topics[-max(1, strength_threshold):]]
        
        return areas_of_strength, areas_for_improvement
    
    def _calculate_performance_consistency(self, assessment_data: List) -> Dict[str, Any]:
        """Calculate performance consistency metrics"""
        scores = [a.score for a in assessment_data if a.score is not None]
        
        if len(scores) < 2:
            return {'consistency_score': 0, 'coefficient_of_variation': 0}
        
        mean_score = np.mean(scores)
        std_deviation = np.std(scores)
        coefficient_of_variation = std_deviation / mean_score if mean_score > 0 else 0
        
        # Consistency score (inverse of coefficient of variation)
        consistency_score = max(0, 100 - (coefficient_of_variation * 100))
        
        return {
            'consistency_score': round(consistency_score, 2),
            'coefficient_of_variation': round(coefficient_of_variation, 3),
            'standard_deviation': round(std_deviation, 2),
            'mean_score': round(mean_score, 2)
        }
    
    def _generate_performance_predictions(self, assessment_data: List) -> Dict[str, Any]:
        """Generate performance predictions"""
        if len(assessment_data) < 5:
            return {'prediction_confidence': 'low', 'predicted_next_score': None}
        
        # Calculate trend for next score prediction
        recent_scores = [a.score for a in sorted([a for a in assessment_data if a.score], 
                                               key=lambda x: x.completed_at)[-5:]]
        
        if len(recent_scores) < 3:
            return {'prediction_confidence': 'low', 'predicted_next_score': np.mean(recent_scores)}
        
        # Linear regression for prediction
        x_values = list(range(len(recent_scores)))
        slope, intercept = np.polyfit(x_values, recent_scores, 1)
        
        # Predict next score
        next_score = slope * len(recent_scores) + intercept
        predicted_next_score = max(0, min(100, next_score))  # Bound between 0 and 100
        
        # Calculate confidence based on trend consistency
        confidence = 'high' if abs(slope) < 1 else 'medium' if abs(slope) < 2 else 'low'
        
        return {
            'prediction_confidence': confidence,
            'predicted_next_score': round(predicted_next_score, 2),
            'trend_slope': round(slope, 3)
        }
    
    def _calculate_overall_performance_score(self, assessment_data: List) -> float:
        """Calculate overall performance score"""
        if not assessment_data:
            return 0.0
        
        scores = [a.score for a in assessment_data if a.score is not None]
        if not scores:
            return 0.0
        
        # Weighted average (more recent scores have higher weight)
        if len(scores) <= 1:
            return scores[0]
        
        weights = [1.0 + (i * 0.1) for i in range(len(scores))]  # Increasing weights
        weighted_scores = [score * weight for score, weight in zip(scores, weights)]
        
        return round(sum(weighted_scores) / sum(weights), 2)
    
    def _generate_performance_recommendations(self, assessment_data: List) -> List[str]:
        """Generate performance-based recommendations"""
        recommendations = []
        
        scores = [a.score for a in assessment_data if a.score is not None]
        if not scores:
            return ["Complete assessments to receive performance feedback"]
        
        avg_score = np.mean(scores)
        
        if avg_score < 70:
            recommendations.append("Focus on fundamental concepts and practice regularly")
            recommendations.append("Review incorrect answers to identify knowledge gaps")
        elif avg_score < 85:
            recommendations.append("Strengthen understanding through varied practice problems")
            recommendations.append("Review challenging topics for better retention")
        else:
            recommendations.append("Excellent performance - consider advanced challenges")
            recommendations.append("Help peers to reinforce your own understanding")
        
        # Consistency-based recommendations
        if len(scores) >= 3:
            score_variance = np.var(scores)
            if score_variance > 100:  # High variance
                recommendations.append("Work on consistent performance across all topics")
                recommendations.append("Identify sources of performance variation")
        
        return recommendations
    
    def _generate_engagement_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed engagement analytics"""
        progress_data = data.get('progress_data', [])
        engagement_stats = data.get('engagement_statistics', {})
        
        if not progress_data:
            return {
                'engagement_level': 'low',
                'frequency': 'sporadic',
                'consistency_rating': 'poor',
                'motivation_indicators': 0
            }
        
        # Analyze engagement patterns
        engagement_patterns = self._analyze_engagement_patterns_detailed(progress_data)
        
        # Calculate motivation indicators
        motivation_score = self._calculate_motivation_score(progress_data)
        
        # Determine engagement level
        engagement_level = self._determine_engagement_level(engagement_stats)
        
        # Analyze learning frequency patterns
        frequency_analysis = self._analyze_frequency_patterns(progress_data)
        
        return {
            'engagement_level': engagement_level,
            'frequency': frequency_analysis['frequency_type'],
            'consistency_rating': engagement_patterns['consistency_rating'],
            'motivation_indicators': round(motivation_score, 2),
            'engagement_patterns': engagement_patterns,
            'frequency_analysis': frequency_analysis,
            'session_quality': self._assess_session_quality(progress_data),
            'peak_activity_hours': self._identify_peak_hours(progress_data),
            'weekly_engagement_trend': self._calculate_weekly_engagement_trend(progress_data),
            'recommendations': self._generate_engagement_recommendations(engagement_stats, motivation_score)
        }
    
    def _analyze_engagement_patterns_detailed(self, progress_data: List) -> Dict[str, Any]:
        """Analyze detailed engagement patterns"""
        if not progress_data:
            return {'consistency_rating': 'poor', 'pattern_type': 'inactive'}
        
        # Group activities by day
        daily_activities = defaultdict(int)
        for progress in progress_data:
            daily_activities[progress.updated_at.date()] += 1
        
        # Calculate engagement metrics
        days_with_activity = len(daily_activities)
        total_days = max(1, (max(p.updated_at for p in progress_data) - 
                            min(p.updated_at for p in progress_data)).days + 1)
        
        activity_rate = days_with_activity / total_days
        
        # Determine consistency rating
        if activity_rate >= 0.8:
            consistency_rating = 'excellent'
        elif activity_rate >= 0.6:
            consistency_rating = 'good'
        elif activity_rate >= 0.4:
            consistency_rating = 'fair'
        elif activity_rate >= 0.2:
            consistency_rating = 'poor'
        else:
            consistency_rating = 'very_poor'
        
        # Analyze activity distribution
        activity_counts = list(daily_activities.values())
        activity_variance = np.var(activity_counts)
        
        return {
            'consistency_rating': consistency_rating,
            'activity_rate': round(activity_rate, 3),
            'activity_variance': round(activity_variance, 2),
            'pattern_type': 'regular' if activity_variance < 2 else 'irregular'
        }
    
    def _calculate_motivation_score(self, progress_data: List) -> float:
        """Calculate motivation score based on learning behaviors"""
        if not progress_data:
            return 0.0
        
        # Factors for motivation calculation
        factors = []
        
        # 1. Completion rate factor
        completed_count = len([p for p in progress_data if p.status == 'completed'])
        total_count = len(progress_data)
        completion_factor = (completed_count / max(total_count, 1)) * 40  # Max 40 points
        factors.append(completion_factor)
        
        # 2. Recency factor (more recent activity = higher motivation)
        recent_activities = [p for p in progress_data 
                           if p.updated_at >= timezone.now() - timedelta(days=7)]
        recent_factor = min(30, len(recent_activities) * 3)  # Max 30 points
        factors.append(recent_factor)
        
        # 3. Consistency factor
        daily_activities = defaultdict(int)
        for progress in progress_data:
            daily_activities[progress.updated_at.date()] += 1
        
        if len(daily_activities) > 0:
            consistency_factor = min(20, len(daily_activities) * 2)  # Max 20 points
            factors.append(consistency_factor)
        
        # 4. Score improvement factor
        scores = [p.score for p in progress_data if p.score is not None]
        if len(scores) >= 2:
            score_trend = self._calculate_score_trend_simple(scores)
            improvement_factor = max(0, min(10, score_trend * 2))  # Max 10 points
            factors.append(improvement_factor)
        
        return min(100, sum(factors))
    
    def _calculate_score_trend_simple(self, scores: List[float]) -> float:
        """Calculate simple score trend"""
        if len(scores) < 2:
            return 0.0
        
        recent_avg = np.mean(scores[-3:]) if len(scores) >= 3 else scores[-1]
        earlier_avg = np.mean(scores[:-3]) if len(scores) > 3 else np.mean(scores[:-1])
        
        return recent_avg - earlier_avg
    
    def _determine_engagement_level(self, engagement_stats: Dict[str, Any]) -> str:
        """Determine overall engagement level"""
        engagement_score = engagement_stats.get('engagement_level', 0)
        consistency_score = engagement_stats.get('consistency_score', 0)
        
        # Combined engagement score
        combined_score = (engagement_score + consistency_score) / 2
        
        if combined_score >= 85:
            return 'very_high'
        elif combined_score >= 70:
            return 'high'
        elif combined_score >= 50:
            return 'moderate'
        elif combined_score >= 30:
            return 'low'
        else:
            return 'very_low'
    
    def _analyze_frequency_patterns(self, progress_data: List) -> Dict[str, Any]:
        """Analyze learning frequency patterns"""
        if not progress_data:
            return {'frequency_type': 'none', 'avg_gap_days': 0}
        
        # Calculate gaps between learning sessions
        sorted_dates = sorted(set(p.updated_at.date() for p in progress_data))
        
        if len(sorted_dates) < 2:
            return {'frequency_type': 'single_session', 'avg_gap_days': 0}
        
        gaps = []
        for i in range(1, len(sorted_dates)):
            gap = (sorted_dates[i] - sorted_dates[i-1]).days
            gaps.append(gap)
        
        avg_gap = np.mean(gaps) if gaps else 0
        
        # Classify frequency type
        if avg_gap <= 1:
            frequency_type = 'daily'
        elif avg_gap <= 3:
            frequency_type = 'frequent'
        elif avg_gap <= 7:
            frequency_type = 'regular'
        elif avg_gap <= 14:
            frequency_type = 'occasional'
        else:
            frequency_type = 'sporadic'
        
        return {
            'frequency_type': frequency_type,
            'avg_gap_days': round(avg_gap, 1),
            'most_common_gap': max(set(gaps), key=gaps.count) if gaps else 0
        }
    
    def _assess_session_quality(self, progress_data: List) -> Dict[str, Any]:
        """Assess quality of learning sessions"""
        if not progress_data:
            return {'quality_score': 0, 'session_type': 'none'}
        
        # Analyze session characteristics
        session_qualities = []
        session_lengths = []
        
        # Group activities by day to identify sessions
        daily_activities = defaultdict(list)
        for progress in progress_data:
            daily_activities[progress.updated_at.date()].append(progress)
        
        for date, activities in daily_activities.items():
            # Session quality factors
            completed_in_session = len([a for a in activities if a.status == 'completed'])
            total_in_session = len(activities)
            
            # Quality score based on completion rate and effort
            completion_rate = completed_in_session / max(total_in_session, 1)
            session_effort = min(10, total_in_session)  # More activities = higher effort
            
            session_quality = (completion_rate * 50) + (session_effort * 5)
            session_qualities.append(session_quality)
            
            # Session length
            if activities and all(hasattr(a, 'time_spent') and a.time_spent for a in activities):
                total_time = sum(a.time_spent.total_seconds() / 3600 for a in activities)  # Hours
                session_lengths.append(total_time)
        
        avg_quality = np.mean(session_qualities) if session_qualities else 0
        avg_length = np.mean(session_lengths) if session_lengths else 0
        
        # Determine session type
        if avg_length >= 2:
            session_type = 'long'
        elif avg_length >= 1:
            session_type = 'medium'
        elif avg_length > 0:
            session_type = 'short'
        else:
            session_type = 'unmeasured'
        
        return {
            'quality_score': round(avg_quality, 2),
            'session_type': session_type,
            'avg_session_length_hours': round(avg_length, 2),
            'total_sessions': len(session_qualities)
        }
    
    def _identify_peak_hours(self, progress_data: List) -> List[int]:
        """Identify peak learning hours"""
        if not progress_data:
            return []
        
        hour_counts = defaultdict(int)
        for progress in progress_data:
            hour = progress.updated_at.hour
            hour_counts[hour] += 1
        
        # Find hours with highest activity
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        peak_hours = [hour for hour, count in sorted_hours[:3]]  # Top 3 hours
        
        return peak_hours
    
    def _calculate_weekly_engagement_trend(self, progress_data: List) -> str:
        """Calculate weekly engagement trend"""
        if not progress_data:
            return 'no_data'
        
        # Group activities by week
        weekly_counts = defaultdict(int)
        for progress in progress_data:
            week_start = progress.updated_at - timedelta(days=progress.updated_at.weekday())
            weekly_counts[week_start.date()] += 1
        
        if len(weekly_counts) < 2:
            return 'insufficient_data'
        
        # Calculate trend
        sorted_weeks = sorted(weekly_counts.keys())
        recent_weeks = sorted_weeks[-2:]
        
        if len(recent_weeks) == 2:
            recent_activity = weekly_counts[recent_weeks[1]]
            previous_activity = weekly_counts[recent_weeks[0]]
            
            if recent_activity > previous_activity * 1.2:
                return 'increasing'
            elif recent_activity < previous_activity * 0.8:
                return 'decreasing'
            else:
                return 'stable'
        
        return 'stable'
    
    def _generate_engagement_recommendations(self, engagement_stats: Dict, motivation_score: float) -> List[str]:
        """Generate engagement-based recommendations"""
        recommendations = []
        
        # Motivation-based recommendations
        if motivation_score < 30:
            recommendations.append("Set small daily learning goals to build momentum")
            recommendations.append("Take breaks and celebrate small achievements")
        elif motivation_score < 60:
            recommendations.append("Maintain current learning routine for consistency")
            recommendations.append("Consider varying your learning activities")
        else:
            recommendations.append("Excellent motivation! Consider challenging yourself further")
        
        # Engagement level recommendations
        engagement_level = self._determine_engagement_level(engagement_stats)
        if engagement_level in ['low', 'very_low']:
            recommendations.append("Establish a regular study schedule")
            recommendations.append("Remove distractions during learning sessions")
        
        # Consistency recommendations
        consistency_score = engagement_stats.get('consistency_score', 0)
        if consistency_score < 50:
            recommendations.append("Focus on consistent daily practice rather than long sessions")
        
        return recommendations
    
    def _generate_learning_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive learning analytics"""
        progress_data = data.get('progress_data', [])
        assessment_data = data.get('assessment_data', [])
        velocity_stats = data.get('velocity_statistics', {})
        
        if not progress_data and not assessment_data:
            return {
                'learning_velocity': 'none',
                'skill_progression': 'none',
                'comprehension_level': 'unknown'
            }
        
        # Calculate learning velocity
        velocity_analysis = self._analyze_learning_velocity_detailed(progress_data, assessment_data)
        
        # Analyze skill progression
        skill_progression_analysis = self._analyze_skill_progression_detailed(progress_data, assessment_data)
        
        # Assess comprehension level
        comprehension_assessment = self._assess_comprehension_level(progress_data, assessment_data)
        
        # Generate learning insights
        learning_insights = self._generate_learning_insights(progress_data, assessment_data)
        
        # Calculate learning efficiency
        learning_efficiency = self._calculate_learning_efficiency(progress_data, assessment_data)
        
        # Analyze learning patterns
        learning_patterns = self._analyze_learning_patterns_detailed(progress_data, assessment_data)
        
        return {
            'learning_velocity': velocity_analysis,
            'skill_progression': skill_progression_analysis,
            'comprehension_level': comprehension_assessment,
            'learning_efficiency': learning_efficiency,
            'learning_insights': learning_insights,
            'learning_patterns': learning_patterns,
            'retention_metrics': self._calculate_retention_metrics(progress_data, assessment_data),
            'mastery_assessment': self._assess_mastery_level(progress_data, assessment_data),
            'learning_recommendations': self._generate_learning_recommendations(velocity_analysis, skill_progression_analysis)
        }
    
    def _analyze_learning_velocity_detailed(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Analyze learning velocity in detail"""
        if not progress_data and not assessment_data:
            return {'velocity_type': 'none', 'daily_rate': 0}
        
        # Calculate daily learning rates
        daily_rates = self._calculate_daily_learning_rates(progress_data, assessment_data)
        
        # Determine velocity type
        avg_daily_rate = np.mean(daily_rates) if daily_rates else 0
        
        if avg_daily_rate >= 5:
            velocity_type = 'very_fast'
        elif avg_daily_rate >= 3:
            velocity_type = 'fast'
        elif avg_daily_rate >= 1.5:
            velocity_type = 'moderate'
        elif avg_daily_rate >= 0.5:
            velocity_type = 'slow'
        else:
            velocity_type = 'very_slow'
        
        # Calculate velocity consistency
        if len(daily_rates) > 1:
            velocity_consistency = max(0, 100 - (np.std(daily_rates) * 20))
        else:
            velocity_consistency = 100
        
        return {
            'velocity_type': velocity_type,
            'daily_rate': round(avg_daily_rate, 3),
            'velocity_consistency': round(velocity_consistency, 2),
            'daily_rates': daily_rates,
            'peak_performance_days': self._identify_peak_performance_days(daily_rates)
        }
    
    def _calculate_daily_learning_rates(self, progress_data: List, assessment_data: List) -> List[float]:
        """Calculate daily learning rates"""
        if not progress_data and not assessment_data:
            return []
        
        # Combine all activities
        all_activities = []
        
        for progress in progress_data:
            all_activities.append({
                'date': progress.updated_at.date(),
                'type': 'progress',
                'value': 1  # Each progress activity counts as 1
            })
        
        for assessment in assessment_data:
            all_activities.append({
                'date': assessment.completed_at.date() if assessment.completed_at else assessment.started_at.date(),
                'type': 'assessment',
                'value': 1  # Each assessment counts as 1
            })
        
        # Group by date and calculate daily rates
        daily_totals = defaultdict(float)
        for activity in all_activities:
            daily_totals[activity['date']] += activity['value']
        
        # Return daily rates for the last 30 days
        rates = []
        today = timezone.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            rates.append(daily_totals.get(date, 0))
        
        return rates
    
    def _identify_peak_performance_days(self, daily_rates: List[float]) -> List[int]:
        """Identify days with peak performance"""
        if not daily_rates:
            return []
        
        # Find days with above-average performance
        avg_rate = np.mean(daily_rates)
        threshold = avg_rate + np.std(daily_rates)
        
        peak_days = []
        for i, rate in enumerate(daily_rates):
            if rate >= threshold and rate > 0:
                peak_days.append(i)  # Days ago
        
        return peak_days[:3]  # Return top 3 peak days
    
    def _analyze_skill_progression_detailed(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Analyze skill progression in detail"""
        if not progress_data and not assessment_data:
            return {'progression_rate': 0, 'progression_trend': 'none'}
        
        # Analyze score progression over time
        score_progression = self._analyze_score_progression(assessment_data)
        
        # Analyze module completion progression
        module_progression = self._analyze_module_completion_progression(progress_data)
        
        # Calculate overall skill progression
        if score_progression and module_progression:
            progression_combined = (score_progression['trend_score'] + module_progression['trend_score']) / 2
        elif score_progression:
            progression_combined = score_progression['trend_score']
        elif module_progression:
            progression_combined = module_progression['trend_score']
        else:
            progression_combined = 0
        
        # Determine progression trend
        if progression_combined > 10:
            progression_trend = 'rapid'
        elif progression_combined > 0:
            progression_trend = 'steady'
        elif progression_combined > -10:
            progression_trend = 'slow'
        else:
            progression_trend = 'declining'
        
        return {
            'progression_rate': round(progression_combined, 2),
            'progression_trend': progression_trend,
            'score_progression': score_progression,
            'module_progression': module_progression,
            'skill_areas': self._identify_skill_areas(progress_data, assessment_data)
        }
    
    def _analyze_score_progression(self, assessment_data: List) -> Dict[str, Any]:
        """Analyze score progression over time"""
        if not assessment_data:
            return None
        
        # Get scored assessments
        scored_assessments = [a for a in assessment_data if a.score is not None]
        if len(scored_assessments) < 3:
            return {'trend_score': 0, 'improvement_rate': 0}
        
        # Sort by completion date
        sorted_assessments = sorted(scored_assessments, key=lambda x: x.completed_at or x.started_at)
        scores = [a.score for a in sorted_assessments]
        
        # Calculate trend using linear regression
        if len(scores) >= 3:
            x_values = list(range(len(scores)))
            slope, intercept = np.polyfit(x_values, scores, 1)
            
            # Calculate improvement rate
            if len(scores) >= 6:
                first_half = np.mean(scores[:len(scores)//2])
                second_half = np.mean(scores[len(scores)//2:])
                improvement_rate = ((second_half - first_half) / max(first_half, 1)) * 100
            else:
                improvement_rate = slope * 10  # Approximate improvement rate
        else:
            slope = 0
            improvement_rate = 0
        
        return {
            'trend_score': round(slope * 10, 2),  # Scale slope for trend score
            'improvement_rate': round(improvement_rate, 2),
            'score_trend': 'improving' if slope > 0.5 else 'declining' if slope < -0.5 else 'stable'
        }
    
    def _analyze_module_completion_progression(self, progress_data: List) -> Dict[str, Any]:
        """Analyze module completion progression"""
        if not progress_data:
            return None
        
        # Get completed modules
        completed_modules = [p for p in progress_data if p.status == 'completed']
        if len(completed_modules) < 2:
            return {'trend_score': 0, 'completion_rate': 0}
        
        # Sort by completion date
        completed_modules.sort(key=lambda x: x.updated_at)
        
        # Analyze completion pattern over time
        time_periods = []
        completion_counts = []
        
        for i in range(0, len(completed_modules), max(1, len(completed_modules)//5)):
            period_end = completed_modules[min(i + max(1, len(completed_modules)//5) - 1, len(completed_modules) - 1)]
            time_periods.append(period_end.updated_at)
            completion_counts.append(min(i + max(1, len(completed_modules)//5), len(completed_modules)) - i)
        
        # Calculate trend
        if len(completion_counts) > 1:
            x_values = list(range(len(completion_counts)))
            slope, _ = np.polyfit(x_values, completion_counts, 1)
            trend_score = slope * 5  # Scale for trend score
        else:
            trend_score = 0
        
        return {
            'trend_score': round(trend_score, 2),
            'completion_rate': round(len(completed_modules) / max(len(progress_data), 1) * 100, 2),
            'total_completed': len(completed_modules)
        }
    
    def _identify_skill_areas(self, progress_data: List, assessment_data: List) -> Dict[str, List]:
        """Identify skill areas and performance"""
        skill_areas = {
            'strong_areas': [],
            'developing_areas': [],
            'weak_areas': []
        }
        
        # Analyze performance by module/topic
        module_performance = defaultdict(list)
        
        for assessment in assessment_data:
            if assessment.score is not None:
                module_title = getattr(assessment.assessment, 'module', {}).get('title', 'General')
                module_performance[module_title].append(assessment.score)
        
        # Categorize areas
        for module, scores in module_performance.items():
            avg_score = np.mean(scores)
            
            if avg_score >= 85:
                skill_areas['strong_areas'].append({
                    'area': module,
                    'score': round(avg_score, 2),
                    'attempts': len(scores)
                })
            elif avg_score >= 70:
                skill_areas['developing_areas'].append({
                    'area': module,
                    'score': round(avg_score, 2),
                    'attempts': len(scores)
                })
            else:
                skill_areas['weak_areas'].append({
                    'area': module,
                    'score': round(avg_score, 2),
                    'attempts': len(scores)
                })
        
        return skill_areas
    
    def _assess_comprehension_level(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Assess comprehension level based on performance data"""
        if not progress_data and not assessment_data:
            return {'level': 'unknown', 'confidence': 0}
        
        # Calculate comprehension factors
        factors = []
        
        # 1. Assessment performance factor
        if assessment_data:
            scores = [a.score for a in assessment_data if a.score is not None]
            if scores:
                avg_score = np.mean(scores)
                score_factor = min(100, max(0, avg_score))
                factors.append(score_factor)
        
        # 2. Completion consistency factor
        if progress_data:
            completed = len([p for p in progress_data if p.status == 'completed'])
            total = len(progress_data)
            completion_rate = (completed / max(total, 1)) * 100
            factors.append(completion_rate)
        
        # 3. Improvement factor
        if assessment_data and len(assessment_data) >= 3:
            recent_scores = [a.score for a in sorted(assessment_data, key=lambda x: x.completed_at or x.started_at)[-3:] if a.score]
            if len(recent_scores) >= 2:
                improvement = recent_scores[-1] - recent_scores[0]
                improvement_factor = max(0, min(100, 70 + improvement))
                factors.append(improvement_factor)
        
        # Calculate overall comprehension level
        if factors:
            overall_comprehension = np.mean(factors)
        else:
            overall_comprehension = 0
        
        # Determine comprehension level
        if overall_comprehension >= 90:
            level = 'excellent'
        elif overall_comprehension >= 80:
            level = 'very_good'
        elif overall_comprehension >= 70:
            level = 'good'
        elif overall_comprehension >= 60:
            level = 'satisfactory'
        elif overall_comprehension >= 50:
            level = 'needs_improvement'
        else:
            level = 'poor'
        
        # Calculate confidence based on data amount
        total_data_points = len(progress_data) + len(assessment_data)
        confidence = min(100, (total_data_points / 20) * 100)  # Full confidence at 20+ data points
        
        return {
            'level': level,
            'score': round(overall_comprehension, 2),
            'confidence': round(confidence, 2),
            'factors': {
                'assessment_performance': round(factors[0], 2) if len(factors) > 0 else 0,
                'completion_consistency': round(factors[1], 2) if len(factors) > 1 else 0,
                'improvement_trend': round(factors[2], 2) if len(factors) > 2 else 0
            }
        }
    
    def _calculate_learning_efficiency(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Calculate learning efficiency metrics"""
        if not progress_data and not assessment_data:
            return {'efficiency_score': 0, 'efficiency_type': 'none'}
        
        # Time-based efficiency
        time_efficiency = self._calculate_time_efficiency_detailed(progress_data)
        
        # Resource efficiency (less attempts for same results)
        resource_efficiency = self._calculate_resource_efficiency(progress_data, assessment_data)
        
        # Result efficiency (high scores with reasonable effort)
        result_efficiency = self._calculate_result_efficiency(progress_data, assessment_data)
        
        # Overall efficiency
        efficiency_scores = [time_efficiency, resource_efficiency, result_efficiency]
        overall_efficiency = np.mean(efficiency_scores)
        
        # Determine efficiency type
        if overall_efficiency >= 85:
            efficiency_type = 'highly_efficient'
        elif overall_efficiency >= 70:
            efficiency_type = 'efficient'
        elif overall_efficiency >= 55:
            efficiency_type = 'moderately_efficient'
        elif overall_efficiency >= 40:
            efficiency_type = 'inefficient'
        else:
            efficiency_type = 'very_inefficient'
        
        return {
            'efficiency_score': round(overall_efficiency, 2),
            'efficiency_type': efficiency_type,
            'time_efficiency': round(time_efficiency, 2),
            'resource_efficiency': round(resource_efficiency, 2),
            'result_efficiency': round(result_efficiency, 2),
            'efficiency_breakdown': self._generate_efficiency_breakdown(efficiency_scores)
        }
    
    def _calculate_time_efficiency_detailed(self, progress_data: List) -> float:
        """Calculate detailed time efficiency"""
        if not progress_data:
            return 0
        
        # Analyze time spent vs completion quality
        completed_with_time = [p for p in progress_data if p.status == 'completed' and p.time_spent]
        
        if not completed_with_time:
            return 50  # Neutral score if no time data
        
        time_efficiencies = []
        for progress in completed_with_time:
            # Simple time efficiency calculation
            time_hours = progress.time_spent.total_seconds() / 3600
            if time_hours > 0:
                # Assume 1 hour is baseline for efficiency calculation
                efficiency = max(0, min(100, 100 - (time_hours - 1) * 20))
                time_efficiencies.append(efficiency)
        
        return np.mean(time_efficiencies) if time_efficiencies else 50
    
    def _calculate_resource_efficiency(self, progress_data: List, assessment_data: List) -> float:
        """Calculate resource efficiency (efficient use of attempts)"""
        if not progress_data or not assessment_data:
            return 50
        
        # Calculate assessment efficiency
        total_attempts = len(assessment_data)
        passing_scores = len([a for a in assessment_data if a.score and a.score >= 70])
        
        if total_attempts > 0:
            attempt_efficiency = (passing_scores / total_attempts) * 100
        else:
            attempt_efficiency = 0
        
        return min(100, max(0, attempt_efficiency))
    
    def _calculate_result_efficiency(self, progress_data: List, assessment_data: List) -> float:
        """Calculate result efficiency (good results with reasonable effort)"""
        if not assessment_data:
            return 50
        
        scores = [a.score for a in assessment_data if a.score is not None]
        if not scores:
            return 50
        
        avg_score = np.mean(scores)
        score_efficiency = avg_score
        
        return min(100, max(0, score_efficiency))
    
    def _generate_efficiency_breakdown(self, efficiency_scores: List[float]) -> Dict[str, str]:
        """Generate efficiency breakdown descriptions"""
        breakdown = {}
        
        categories = ['Time Efficiency', 'Resource Efficiency', 'Result Efficiency']
        descriptions = ['time', 'resource', 'result']
        
        for i, (category, desc) in enumerate(zip(categories, descriptions)):
            if i < len(efficiency_scores):
                score = efficiency_scores[i]
                if score >= 85:
                    level = f"Excellent {desc} efficiency"
                elif score >= 70:
                    level = f"Good {desc} efficiency"
                elif score >= 55:
                    level = f"Fair {desc} efficiency"
                elif score >= 40:
                    level = f"Poor {desc} efficiency"
                else:
                    level = f"Very poor {desc} efficiency"
                
                breakdown[category] = level
        
        return breakdown
    
    def _generate_comparative_analysis(self, data: Dict[str, Any], user: User) -> Dict[str, Any]:
        """Generate comprehensive comparative analysis"""
        # Get peer comparison data
        peer_comparison = await self._analyze_peer_performance(user, data)
        
        # Get institutional ranking
        institutional_ranking = await self._analyze_institutional_ranking(user, data)
        
        # Generate benchmarking data
        benchmarking_data = await self._generate_benchmarking_data(user, data)
        
        # Calculate percentile rankings
        percentile_rankings = await self._calculate_percentile_rankings(user, data)
        
        return {
            'peer_comparison': peer_comparison,
            'institutional_ranking': institutional_ranking,
            'benchmarking_data': benchmarking_data,
            'percentile_rankings': percentile_rankings,
            'performance_context': self._provide_performance_context(data),
            'comparative_insights': self._generate_comparative_insights(peer_comparison, percentile_rankings)
        }
    
    async def _analyze_peer_performance(self, user: User, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user's performance against peers"""
        try:
            # Get all users in similar learning paths
            learning_path_id = data.get('learning_path_id')
            
            peer_query = UserModuleProgress.objects.filter(
                module__learning_path_id=learning_path_id
            ).exclude(user=user) if learning_path_id else UserModuleProgress.objects.exclude(user=user)
            
            # Calculate peer metrics
            peer_completion_rates = []
            peer_scores = []
            peer_velocities = []
            
            # Sample peer data (limit to avoid performance issues)
            peer_progress = peer_query[:100]  # Sample first 100 peers
            
            for peer in peer_progress:
                # Calculate peer completion rate
                peer_completed = UserModuleProgress.objects.filter(
                    user=peer.user,
                    status='completed'
                ).count()
                
                peer_total = UserModuleProgress.objects.filter(user=peer.user).count()
                if peer_total > 0:
                    completion_rate = (peer_completed / peer_total) * 100
                    peer_completion_rates.append(completion_rate)
                
                # Get peer assessment scores
                peer_assessments = AssessmentAttempt.objects.filter(
                    user=peer.user,
                    score__isnull=False
                )[:5]  # Sample 5 assessments per peer
                
                peer_scores.extend([a.score for a in peer_assessments])
                
                # Calculate peer velocity
                peer_activities = UserModuleProgress.objects.filter(
                    user=peer.user,
                    updated_at__gte=timezone.now() - timedelta(days=30)
                ).count()
                peer_velocities.append(peer_activities / 30)
            
            # Calculate user's metrics
            user_completion_rate = len([p for p in data.get('progress_data', []) if p.status == 'completed']) / max(len(data.get('progress_data', [])), 1) * 100
            user_scores = [a.score for a in data.get('assessment_data', []) if a.score is not None]
            user_velocity = len(data.get('progress_data', [])) / 30  # Activities per day
            
            # Compare with peers
            comparison = {}
            
            if peer_completion_rates:
                comparison['completion_rate'] = {
                    'user': round(user_completion_rate, 2),
                    'peer_average': round(np.mean(peer_completion_rates), 2),
                    'peer_median': round(np.median(peer_completion_rates), 2),
                    'peer_range': f"{round(np.min(peer_completion_rates), 2)} - {round(np.max(peer_completion_rates), 2)}",
                    'percentile': self._calculate_percentile(user_completion_rate, peer_completion_rates)
                }
            
            if peer_scores and user_scores:
                comparison['score_performance'] = {
                    'user_average': round(np.mean(user_scores), 2),
                    'peer_average': round(np.mean(peer_scores), 2),
                    'peer_median': round(np.median(peer_scores), 2),
                    'user_vs_peer': 'above' if np.mean(user_scores) > np.mean(peer_scores) else 'below'
                }
            
            if peer_velocities:
                comparison['learning_velocity'] = {
                    'user': round(user_velocity, 3),
                    'peer_average': round(np.mean(peer_velocities), 3),
                    'user_vs_peer': 'faster' if user_velocity > np.mean(peer_velocities) else 'slower'
                }
            
            return comparison
            
        except Exception as e:
            return {'error': f'Peer comparison failed: {str(e)}'}
    
    def _calculate_percentile(self, value: float, distribution: List[float]) -> int:
        """Calculate percentile rank of a value in a distribution"""
        if not distribution:
            return 50
        
        lower_count = len([x for x in distribution if x < value])
        equal_count = len([x for x in distribution if x == value])
        
        percentile = ((lower_count + 0.5 * equal_count) / len(distribution)) * 100
        return int(round(percentile))
    
    async def _analyze_institutional_ranking(self, user: User, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user's ranking within the institution"""
        try:
            # Get all users in the system for comparison
            all_users = User.objects.filter(
                learning_module_progress__isnull=False
            ).distinct()
            
            if not all_users.exists():
                return {'ranking': 'unknown', 'total_users': 0}
            
            # Calculate institutional metrics for comparison
            user_metrics = self._calculate_user_metrics_for_comparison(user, data)
            
            # Calculate rankings for different metrics
            rankings = {}
            
            for metric_name, user_value in user_metrics.items():
                # Get all users' values for this metric
                all_values = []
                for other_user in all_users:
                    if other_user.id != user.id:
                        other_metrics = self._calculate_user_metrics_for_comparison(other_user, data)
                        if metric_name in other_metrics:
                            all_values.append(other_metrics[metric_name])
                
                if all_values:
                    percentile = self._calculate_percentile(user_value, all_values)
                    rankings[metric_name] = {
                        'percentile': percentile,
                        'ranking_level': self._get_ranking_level(percentile)
                    }
            
            return {
                'rankings': rankings,
                'overall_position': self._calculate_overall_position(rankings),
                'institutional_context': self._provide_institutional_context(len(all_users))
            }
            
        except Exception as e:
            return {'error': f'Institutional ranking failed: {str(e)}'}
    
    def _calculate_user_metrics_for_comparison(self, user: User, data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate user metrics for comparison purposes"""
        # Use the provided data if it matches the user, otherwise calculate
        if data.get('user', {}).get('id') == user.id:
            progress_data = data.get('progress_data', [])
            assessment_data = data.get('assessment_data', [])
        else:
            # Calculate for other users (simplified)
            progress_data = list(UserModuleProgress.objects.filter(user=user))
            assessment_data = list(AssessmentAttempt.objects.filter(user=user))
        
        metrics = {}
        
        # Completion rate
        if progress_data:
            completed = len([p for p in progress_data if p.status == 'completed'])
            total = len(progress_data)
            metrics['completion_rate'] = (completed / max(total, 1)) * 100
        
        # Average score
        scores = [a.score for a in assessment_data if a.score is not None]
        if scores:
            metrics['average_score'] = np.mean(scores)
        
        # Learning velocity
        recent_progress = [p for p in progress_data if p.updated_at >= timezone.now() - timedelta(days=30)]
        metrics['learning_velocity'] = len(recent_progress)
        
        # Engagement level
        unique_days = len(set(p.updated_at.date() for p in progress_data))
        metrics['engagement_level'] = unique_days
        
        return metrics
    
    def _get_ranking_level(self, percentile: int) -> str:
        """Convert percentile to ranking level"""
        if percentile >= 90:
            return 'top_10%'
        elif percentile >= 75:
            return 'top_quarter'
        elif percentile >= 50:
            return 'above_average'
        elif percentile >= 25:
            return 'below_average'
        else:
            return 'bottom_quarter'
    
    def _calculate_overall_position(self, rankings: Dict[str, Dict]) -> str:
        """Calculate overall position based on multiple rankings"""
        if not rankings:
            return 'unknown'
        
        percentiles = [ranking['percentile'] for ranking in rankings.values()]
        avg_percentile = np.mean(percentiles)
        
        return self._get_ranking_level(int(avg_percentile))
    
    def _provide_institutional_context(self, total_users: int) -> str:
        """Provide context about institutional size"""
        if total_users >= 1000:
            return f"Large institution with {total_users}+ active learners"
        elif total_users >= 100:
            return f"Medium institution with {total_users} active learners"
        elif total_users >= 10:
            return f"Small institution with {total_users} active learners"
        else:
            return f"Very small institution with {total_users} active learners"
    
    async def _generate_benchmarking_data(self, user: User, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate benchmarking data for performance comparison"""
        try:
            # Define benchmark categories
            benchmark_categories = {
                'beginner': {'score_range': (0, 60), 'completion_rate': (0, 30)},
                'intermediate': {'score_range': (60, 80), 'completion_rate': (30, 70)},
                'advanced': {'score_range': (80, 100), 'completion_rate': (70, 100)}
            }
            
            # Determine user's performance category
            user_scores = [a.score for a in data.get('assessment_data', []) if a.score is not None]
            user_completion_rate = len([p for p in data.get('progress_data', []) if p.status == 'completed']) / max(len(data.get('progress_data', [])), 1) * 100
            
            avg_score = np.mean(user_scores) if user_scores else 0
            user_category = None
            
            for category, ranges in benchmark_categories.items():
                score_min, score_max = ranges['score_range']
                if score_min <= avg_score <= score_max:
                    user_category = category
                    break
            
            if not user_category:
                user_category = 'beginner'  # Default category
            
            # Generate benchmarks
            benchmarks = {}
            for category in benchmark_categories.keys():
                if category == user_category:
                    benchmarks[category] = {
                        'user_performance': 'your_level',
                        'description': f"You are performing at the {category} level"
                    }
                else:
                    benchmarks[category] = {
                        'user_performance': 'target_level',
                        'description': f"Target level: {category}"
                    }
            
            return {
                'user_category': user_category,
                'benchmarks': benchmarks,
                'improvement_targets': self._generate_improvement_targets(user_category, avg_score, user_completion_rate)
            }
            
        except Exception as e:
            return {'error': f'Benchmarking failed: {str(e)}'}
    
    def _generate_improvement_targets(self, current_category: str, current_score: float, current_completion: float) -> List[Dict[str, str]]:
        """Generate improvement targets for user"""
        targets = []
        
        if current_category == 'beginner':
            targets.extend([
                {
                    'metric': 'Average Score',
                    'current': f"{current_score:.1f}%",
                    'target': '70%',
                    'description': 'Focus on understanding core concepts'
                },
                {
                    'metric': 'Completion Rate',
                    'current': f"{current_completion:.1f}%",
                    'target': '50%',
                    'description': 'Maintain consistent learning schedule'
                }
            ])
        elif current_category == 'intermediate':
            targets.extend([
                {
                    'metric': 'Average Score',
                    'current': f"{current_score:.1f}%",
                    'target': '85%',
                    'description': 'Strengthen problem-solving skills'
                },
                {
                    'metric': 'Learning Velocity',
                    'current': 'Moderate',
                    'target': 'Fast',
                    'description': 'Increase study frequency'
                }
            ])
        elif current_category == 'advanced':
            targets.extend([
                {
                    'metric': 'Mastery Level',
                    'current': 'Advanced',
                    'target': 'Expert',
                    'description': 'Master advanced concepts and help others'
                },
                {
                    'metric': 'Consistency',
                    'current': 'Good',
                    'target': 'Excellent',
                    'description': 'Maintain high performance consistently'
                }
            ])
        
        return targets
    
    async def _calculate_percentile_rankings(self, user: User, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed percentile rankings"""
        # This would implement detailed percentile calculations
        # For now, return a simplified version
        
        return {
            'completion_rate_percentile': 65,
            'score_percentile': 78,
            'velocity_percentile': 45,
            'engagement_percentile': 82
        }
    
    def _provide_performance_context(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Provide context about user's performance"""
        context = {}
        
        # Overall performance context
        progress_data = data.get('progress_data', [])
        assessment_data = data.get('assessment_data', [])
        
        if progress_data:
            completion_rate = len([p for p in progress_data if p.status == 'completed']) / len(progress_data) * 100
            if completion_rate >= 80:
                context['completion'] = 'Excellent completion rate - you consistently finish what you start'
            elif completion_rate >= 60:
                context['completion'] = 'Good completion rate with room for improvement'
            else:
                context['completion'] = 'Focus on completing modules to improve learning outcomes'
        
        if assessment_data:
            scores = [a.score for a in assessment_data if a.score is not None]
            if scores:
                avg_score = np.mean(scores)
                if avg_score >= 85:
                    context['performance'] = 'Outstanding academic performance'
                elif avg_score >= 70:
                    context['performance'] = 'Solid academic performance'
                else:
                    context['performance'] = 'Opportunities for academic improvement'
        
        return context
    
    def _generate_comparative_insights(self, peer_comparison: Dict, percentile_rankings: Dict) -> List[str]:
        """Generate insights from comparative analysis"""
        insights = []
        
        # Peer comparison insights
        if 'completion_rate' in peer_comparison:
            percentile = peer_comparison['completion_rate'].get('percentile', 50)
            if percentile >= 75:
                insights.append("You outperform most peers in module completion")
            elif percentile <= 25:
                insights.append("Focus on consistency to match peer completion rates")
        
        # Score performance insights
        if 'score_performance' in peer_comparison:
            comparison = peer_comparison['score_performance']
            if comparison['user_vs_peer'] == 'above':
                insights.append("Your assessment scores exceed the peer average")
            else:
                insights.append("Your assessment scores are below peer average - consider additional practice")
        
        # Percentile insights
        if 'score_percentile' in percentile_rankings:
            score_percentile = percentile_rankings['score_percentile']
            if score_percentile >= 80:
                insights.append("You rank in the top 20% academically")
            elif score_percentile <= 20:
                insights.append("You have significant room for academic improvement")
        
        return insights
    
    def _identify_learning_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify comprehensive learning trends"""
        progress_data = data.get('progress_data', [])
        assessment_data = data.get('assessment_data', [])
        
        trends = {}
        
        # Performance trend analysis
        trends['performance_trend'] = self._analyze_performance_trend_comprehensive(assessment_data)
        
        # Engagement trend analysis
        trends['engagement_trend'] = self._analyze_engagement_trend_comprehensive(progress_data)
        
        # Velocity trend analysis
        trends['velocity_trend'] = self._analyze_velocity_trend(progress_data, assessment_data)
        
        # Consistency trend analysis
        trends['consistency_trend'] = self._analyze_consistency_trend(progress_data, assessment_data)
        
        # Overall trend assessment
        trends['overall_trend'] = self._calculate_overall_trend(trends)
        
        # Trend predictions
        trends['trend_predictions'] = self._generate_trend_predictions(trends, progress_data, assessment_data)
        
        # Trend insights
        trends['trend_insights'] = self._generate_trend_insights(trends)
        
        return trends
    
    def _analyze_performance_trend_comprehensive(self, assessment_data: List) -> Dict[str, Any]:
        """Analyze comprehensive performance trends"""
        if not assessment_data:
            return {'trend': 'no_data', 'confidence': 'low'}
        
        # Get scored assessments
        scored_assessments = [a for a in assessment_data if a.score is not None]
        if len(scored_assessments) < 3:
            return {'trend': 'insufficient_data', 'confidence': 'low'}
        
        # Sort by completion date
        sorted_assessments = sorted(scored_assessments, key=lambda x: x.completed_at or x.started_at)
        scores = [a.score for a in sorted_assessments]
        
        # Analyze trend using multiple methods
        trend_analysis = self._multi_method_trend_analysis(scores)
        
        # Calculate trend confidence
        confidence = self._calculate_trend_confidence(scores, len(scored_assessments))
        
        return {
            'trend': trend_analysis['direction'],
            'confidence': confidence,
            'strength': trend_analysis['strength'],
            'slope': round(trend_analysis['slope'], 3),
            'r_squared': round(trend_analysis['r_squared'], 3),
            'recent_performance': round(np.mean(scores[-3:]), 2) if len(scores) >= 3 else scores[-1],
            'performance_change': round(trend_analysis['change_amount'], 2)
        }
    
    def _multi_method_trend_analysis(self, scores: List[float]) -> Dict[str, Any]:
        """Analyze trend using multiple statistical methods"""
        if len(scores) < 2:
            return {'direction': 'stable', 'strength': 'weak', 'slope': 0, 'r_squared': 0, 'change_amount': 0}
        
        # Method 1: Linear regression
        x_values = list(range(len(scores)))
        slope, intercept = np.polyfit(x_values, scores, 1)
        
        # Calculate R-squared
        y_pred = [slope * x + intercept for x in x_values]
        ss_res = sum((scores[i] - y_pred[i]) ** 2 for i in range(len(scores)))
        ss_tot = sum((scores[i] - np.mean(scores)) ** 2 for i in range(len(scores)))
        r_squared = 1 - (ss_res / max(ss_tot, 1))
        
        # Method 2: Moving average comparison
        recent_avg = np.mean(scores[-3:]) if len(scores) >= 3 else scores[-1]
        earlier_avg = np.mean(scores[:max(1, len(scores)//2)])
        change_amount = recent_avg - earlier_avg
        
        # Determine direction and strength
        if abs(change_amount) < 2:
            direction = 'stable'
            strength = 'weak'
        elif abs(change_amount) < 5:
            direction = 'moderate_change'
            strength = 'moderate'
        else:
            direction = 'strong_change'
            strength = 'strong'
        
        # Refine direction
        if change_amount > 2:
            direction = 'improving'
        elif change_amount < -2:
            direction = 'declining'
        
        return {
            'direction': direction,
            'strength': strength,
            'slope': slope,
            'r_squared': r_squared,
            'change_amount': change_amount
        }
    
    def _calculate_trend_confidence(self, scores: List[float], data_points: int) -> str:
        """Calculate confidence level in trend analysis"""
        if data_points < 5:
            return 'low'
        elif data_points < 10:
            return 'medium'
        else:
            return 'high'
    
    def _analyze_engagement_trend_comprehensive(self, progress_data: List) -> Dict[str, Any]:
        """Analyze comprehensive engagement trends"""
        if not progress_data:
            return {'trend': 'no_data', 'confidence': 'low'}
        
        # Group activities by week
        weekly_activity = defaultdict(int)
        for progress in progress_data:
            week_start = progress.updated_at - timedelta(days=progress.updated_at.weekday())
            weekly_activity[week_start.date()] += 1
        
        # Get recent weeks activity
        sorted_weeks = sorted(weekly_activity.keys())
        recent_weeks = sorted_weeks[-4:]  # Last 4 weeks
        
        if len(recent_weeks) < 2:
            return {'trend': 'insufficient_data', 'confidence': 'low'}
        
        # Calculate engagement metrics
        activity_counts = [weekly_activity[week] for week in recent_weeks]
        
        # Analyze trend
        if len(activity_counts) >= 2:
            x_values = list(range(len(activity_counts)))
            slope, _ = np.polyfit(x_values, activity_counts, 1)
            
            if slope > 0.5:
                trend = 'increasing'
                strength = 'strong'
            elif slope > 0.1:
                trend = 'increasing'
                strength = 'moderate'
            elif slope < -0.5:
                trend = 'decreasing'
                strength = 'strong'
            elif slope < -0.1:
                trend = 'decreasing'
                strength = 'moderate'
            else:
                trend = 'stable'
                strength = 'weak'
        else:
            trend = 'stable'
            strength = 'weak'
        
        return {
            'trend': trend,
            'strength': strength,
            'confidence': 'high' if len(recent_weeks) >= 4 else 'medium',
            'recent_activity': sum(activity_counts[-2:]),
            'previous_activity': sum(activity_counts[:-2]) if len(activity_counts) > 2 else 0
        }
    
    def _analyze_velocity_trend(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Analyze learning velocity trends"""
        if not progress_data and not assessment_data:
            return {'trend': 'no_data'}
        
        # Calculate velocity over time periods
        velocity_periods = self._calculate_velocity_periods(progress_data, assessment_data)
        
        if len(velocity_periods) < 2:
            return {'trend': 'insufficient_data'}
        
        # Analyze velocity trend
        velocities = list(velocity_periods.values())
        if len(velocities) >= 2:
            x_values = list(range(len(velocities)))
            slope, _ = np.polyfit(x_values, velocities, 1)
            
            if slope > 0.1:
                trend = 'accelerating'
            elif slope < -0.1:
                trend = 'decelerating'
            else:
                trend = 'steady'
        else:
            trend = 'steady'
        
        return {
            'trend': trend,
            'current_velocity': velocities[-1] if velocities else 0,
            'velocity_change': slope if len(velocities) >= 2 else 0
        }
    
    def _calculate_velocity_periods(self, progress_data: List, assessment_data: List) -> Dict[str, float]:
        """Calculate learning velocity for different time periods"""
        periods = {}
        
        # Weekly periods
        for days in [7, 14, 30]:
            cutoff_date = timezone.now() - timedelta(days=days)
            
            period_progress = [p for p in progress_data if p.updated_at >= cutoff_date]
            period_assessments = [a for a in assessment_data if a.completed_at and a.completed_at >= cutoff_date]
            
            total_activities = len(period_progress) + len(period_assessments)
            velocity = total_activities / days
            periods[f'{days}_day_velocity'] = velocity
        
        return periods
    
    def _analyze_consistency_trend(self, progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Analyze consistency trends"""
        if not progress_data:
            return {'trend': 'no_data'}
        
        # Calculate consistency over time
        consistency_periods = self._calculate_consistency_periods(progress_data)
        
        if len(consistency_periods) < 2:
            return {'trend': 'insufficient_data'}
        
        # Analyze consistency trend
        consistency_values = list(consistency_periods.values())
        if len(consistency_values) >= 2:
            recent_consistency = np.mean(consistency_values[-2:])
            earlier_consistency = np.mean(consistency_values[:-2])
            
            if recent_consistency > earlier_consistency + 5:
                trend = 'improving'
            elif recent_consistency < earlier_consistency - 5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'current_consistency': consistency_values[-1] if consistency_values else 0,
            'consistency_change': recent_consistency - earlier_consistency if len(consistency_values) >= 2 else 0
        }
    
    def _calculate_consistency_periods(self, progress_data: List) -> Dict[str, float]:
        """Calculate consistency for different time periods"""
        periods = {}
        
        for days in [7, 14, 30]:
            cutoff_date = timezone.now() - timedelta(days=days)
            
            period_data = [p for p in progress_data if p.updated_at >= cutoff_date]
            
            if period_data:
                # Calculate consistency as inverse of coefficient of variation
                daily_counts = defaultdict(int)
                for progress in period_data:
                    daily_counts[progress.updated_at.date()] += 1
                
                counts = list(daily_counts.values())
                if len(counts) > 1:
                    cv = np.std(counts) / np.mean(counts) if np.mean(counts) > 0 else 0
                    consistency = max(0, 100 - (cv * 100))
                else:
                    consistency = 100
                
                periods[f'{days}_day_consistency'] = consistency
        
        return periods
    
    def _calculate_overall_trend(self, trends: Dict[str, Any]) -> str:
        """Calculate overall trend based on individual trends"""
        trend_scores = []
        
        # Performance trend score
        perf_trend = trends.get('performance_trend', {}).get('trend', 'stable')
        if perf_trend == 'improving':
            trend_scores.append(2)
        elif perf_trend == 'declining':
            trend_scores.append(-2)
        else:
            trend_scores.append(0)
        
        # Engagement trend score
        eng_trend = trends.get('engagement_trend', {}).get('trend', 'stable')
        if eng_trend == 'increasing':
            trend_scores.append(2)
        elif eng_trend == 'decreasing':
            trend_scores.append(-2)
        else:
            trend_scores.append(0)
        
        # Calculate overall score
        overall_score = np.mean(trend_scores) if trend_scores else 0
        
        if overall_score > 1:
            return 'strongly_positive'
        elif overall_score > 0.5:
            return 'positive'
        elif overall_score < -1:
            return 'strongly_negative'
        elif overall_score < -0.5:
            return 'negative'
        else:
            return 'neutral'
    
    def _generate_trend_predictions(self, trends: Dict[str, Any], progress_data: List, assessment_data: List) -> Dict[str, Any]:
        """Generate predictions based on current trends"""
        predictions = {}
        
        # Performance prediction
        perf_trend = trends.get('performance_trend', {})
        if perf_trend.get('trend') == 'improving':
            predictions['performance'] = 'likely_to_continue_improving'
        elif perf_trend.get('trend') == 'declining':
            predictions['performance'] = 'may_need_intervention'
        else:
            predictions['performance'] = 'likely_to_remain_stable'
        
        # Engagement prediction
        eng_trend = trends.get('engagement_trend', {})
        if eng_trend.get('trend') == 'increasing':
            predictions['engagement'] = 'likely_to_increase_further'
        elif eng_trend.get('trend') == 'decreasing':
            predictions['engagement'] = 'may_continue_declining'
        else:
            predictions['engagement'] = 'likely_to_remain_stable'
        
        # Overall trajectory
        overall_trend = trends.get('overall_trend', 'neutral')
        if overall_trend in ['strongly_positive', 'positive']:
            predictions['trajectory'] = 'positive_learning_outcomes'
        elif overall_trend in ['strongly_negative', 'negative']:
            predictions['trajectory'] = 'concerning_learning_trajectory'
        else:
            predictions['trajectory'] = 'stable_learning_progress'
        
        return predictions
    
    def _generate_trend_insights(self, trends: Dict[str, Any]) -> List[str]:
        """Generate insights from trend analysis"""
        insights = []
        
        # Performance insights
        perf_trend = trends.get('performance_trend', {})
        if perf_trend.get('trend') == 'improving':
            insights.append("Your performance is trending upward - keep up the excellent work!")
        elif perf_trend.get('trend') == 'declining':
            insights.append("Performance decline detected - consider reviewing recent material")
        
        # Engagement insights
        eng_trend = trends.get('engagement_trend', {})
        if eng_trend.get('trend') == 'increasing':
            insights.append("Increasing engagement is a positive sign for learning outcomes")
        elif eng_trend.get('trend') == 'decreasing':
            insights.append("Declining engagement may impact learning progress")
        
        # Overall insights
        overall_trend = trends.get('overall_trend', 'neutral')
        if overall_trend == 'strongly_positive':
            insights.append("Excellent overall learning trajectory - you're on the right track")
        elif overall_trend == 'strongly_negative':
            insights.append("Overall trend is concerning - consider adjusting learning strategies")
        
        return insights
    
    def _generate_analytics_insights(self, report: Dict[str, Any]) -> List[str]:
        """Generate comprehensive analytics insights"""
        insights = []
        
        # Extract key metrics
        performance_analytics = report.get('performance_analytics', {})
        engagement_analytics = report.get('engagement_analytics', {})
        learning_analytics = report.get('learning_analytics', {})
        
        # Performance insights
        performance_score = performance_analytics.get('performance_score', 0)
        if performance_score >= 85:
            insights.append("Outstanding performance - consistently achieving high scores")
        elif performance_score >= 70:
            insights.append("Strong performance with room for continued improvement")
        elif performance_score >= 60:
            insights.append("Solid foundation with opportunities for growth")
        else:
            insights.append("Performance indicates need for additional support and practice")
        
        # Improvement trend insights
        improvement_trend = performance_analytics.get('improvement_trend', 'stable')
        if improvement_trend == 'improving':
            insights.append("Positive learning trajectory with consistent improvement")
        elif improvement_trend == 'declining':
            insights.append("Performance decline detected - intervention may be beneficial")
        
        # Engagement insights
        engagement_level = engagement_analytics.get('engagement_level', 'low')
        if engagement_level == 'very_high':
            insights.append("Exceptional engagement level demonstrates strong learning commitment")
        elif engagement_level == 'high':
            insights.append("High engagement supports effective learning outcomes")
        elif engagement_level == 'moderate':
            insights.append("Moderate engagement could be enhanced for better results")
        else:
            insights.append("Low engagement may limit learning effectiveness")
        
        # Consistency insights
        consistency_rating = engagement_analytics.get('consistency_rating', 'poor')
        if consistency_rating == 'excellent':
            insights.append("Excellent consistency in learning habits builds strong foundation")
        elif consistency_rating == 'good':
            insights.append("Good consistency with room for minor improvements")
        elif consistency_rating in ['poor', 'very_poor']:
            insights.append("Inconsistent learning patterns may hinder progress")
        
        # Learning velocity insights
        learning_velocity = learning_analytics.get('learning_velocity', {})
        velocity_type = learning_velocity.get('velocity_type', 'none')
        if velocity_type in ['very_fast', 'fast']:
            insights.append("Fast learning pace - consider challenging yourself with advanced content")
        elif velocity_type == 'moderate':
            insights.append("Steady learning pace indicates sustainable progress")
        elif velocity_type in ['slow', 'very_slow']:
            insights.append("Learning pace could be increased for more efficient progress")
        
        # Comprehension insights
        comprehension_level = learning_analytics.get('comprehension_level', {})
        level = comprehension_level.get('level', 'unknown')
        if level == 'excellent':
            insights.append("Excellent comprehension demonstrates deep understanding")
        elif level == 'good':
            insights.append("Good comprehension level with solid conceptual grasp")
        elif level in ['needs_improvement', 'poor']:
            insights.append("Comprehension level suggests need for foundational review")
        
        # Skill progression insights
        skill_progression = learning_analytics.get('skill_progression', {})
        progression_trend = skill_progression.get('progression_trend', 'none')
        if progression_trend == 'rapid':
            insights.append("Rapid skill development indicates strong learning capacity")
        elif progression_trend == 'steady':
            insights.append("Steady skill progression shows consistent growth")
        elif progression_trend == 'declining':
            insights.append("Skill progression has slowed - consider varied learning approaches")
        
        # Efficiency insights
        learning_efficiency = learning_analytics.get('learning_efficiency', {})
        efficiency_type = learning_efficiency.get('efficiency_type', 'none')
        if efficiency_type in ['highly_efficient', 'efficient']:
            insights.append("High learning efficiency maximizes time and effort")
        elif efficiency_type == 'moderately_efficient':
            insights.append("Moderate efficiency with opportunities for optimization")
        else:
            insights.append("Learning efficiency could be improved for better outcomes")
        
        return insights[:8]  # Return top 8 insights
    
    def _generate_analytics_alerts(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive analytics alerts"""
        alerts = []
        
        # Performance alerts
        performance_analytics = report.get('performance_analytics', {})
        performance_score = performance_analytics.get('performance_score', 0)
        
        if performance_score < 60:
            alerts.append({
                'type': 'performance_alert',
                'severity': 'high',
                'title': 'Low Performance Alert',
                'message': f'Performance score of {performance_score}% is below recommended threshold',
                'action_required': True,
                'recommendations': [
                    'Review fundamental concepts',
                    'Increase practice frequency',
                    'Consider additional support resources'
                ]
            })
        elif performance_score < 70:
            alerts.append({
                'type': 'performance_alert',
                'severity': 'medium',
                'title': 'Performance Improvement Needed',
                'message': f'Performance score of {performance_score}% could be improved',
                'action_required': False,
                'recommendations': [
                    'Focus on areas with lower scores',
                    'Review incorrect answers for learning'
                ]
            })
        
        # Engagement alerts
        engagement_analytics = report.get('engagement_analytics', {})
        engagement_level = engagement_analytics.get('engagement_level', 'low')
        consistency_rating = engagement_analytics.get('consistency_rating', 'poor')
        
        if engagement_level in ['low', 'very_low']:
            alerts.append({
                'type': 'engagement_alert',
                'severity': 'medium',
                'title': 'Low Engagement Alert',
                'message': f'Engagement level is {engagement_level} - this may impact learning outcomes',
                'action_required': True,
                'recommendations': [
                    'Establish regular study schedule',
                    'Set smaller daily goals',
                    'Remove learning distractions'
                ]
            })
        
        if consistency_rating in ['poor', 'very_poor']:
            alerts.append({
                'type': 'consistency_alert',
                'severity': 'medium',
                'title': 'Inconsistent Learning Pattern',
                'message': 'Learning consistency is below optimal levels',
                'action_required': True,
                'recommendations': [
                    'Maintain consistent daily study routine',
                    'Track progress to identify patterns'
                ]
            })
        
        # Learning velocity alerts
        learning_analytics = report.get('learning_analytics', {})
        learning_velocity = learning_analytics.get('learning_velocity', {})
        velocity_type = learning_velocity.get('velocity_type', 'none')
        
        if velocity_type in ['very_slow', 'slow']:
            alerts.append({
                'type': 'velocity_alert',
                'severity': 'low',
                'title': 'Slow Learning Progress',
                'message': 'Learning pace is slower than recommended',
                'action_required': False,
                'recommendations': [
                    'Consider increasing study frequency',
                    'Break larger topics into smaller chunks'
                ]
            })
        
        # Alert for declining trends
        trends = report.get('trends', {})
        performance_trend = trends.get('performance_trend', {})
        engagement_trend = trends.get('engagement_trend', {})
        
        if performance_trend.get('trend') == 'declining':
            alerts.append({
                'type': 'trend_alert',
                'severity': 'high',
                'title': 'Performance Decline Alert',
                'message': 'Performance is trending downward - immediate attention recommended',
                'action_required': True,
                'recommendations': [
                    'Identify causes of decline',
                    'Review recent learning materials',
                    'Consider adjusting learning strategy'
                ]
            })
        
        if engagement_trend.get('trend') == 'decreasing':
            alerts.append({
                'type': 'trend_alert',
                'severity': 'medium',
                'title': 'Engagement Decline Alert',
                'message': 'Learning engagement is decreasing over time',
                'action_required': True,
                'recommendations': [
                    'Reassess learning motivation',
                    'Try different learning approaches',
                    'Set new learning goals'
                ]
            })
        
        # Achievement and milestone alerts
        recent_achievements = report.get('achievements', {}).get('recent_achievements', [])
        if recent_achievements:
            alerts.append({
                'type': 'achievement_alert',
                'severity': 'positive',
                'title': 'Achievement Unlocked',
                'message': f'Congratulations! {len(recent_achievements)} new achievements earned',
                'action_required': False,
                'achievements': recent_achievements
            })
        
        return alerts
    
    def _gather_report_data(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Gather data for progress report"""
        return {"user": user, "path_id": learning_path_id, "activities": []}
    
    def _determine_report_period(self, data: Dict[str, Any]) -> str:
        """Determine report period"""
        return "Last 30 days"
    
    def _generate_executive_summary(self, data: Dict[str, Any], report_format: str) -> Dict[str, Any]:
        """Generate executive summary"""
        return {"summary": "Overall progress is good", "key_points": []}
    
    def _create_progress_overview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create progress overview"""
        return {"completion_percentage": 65, "current_level": "Intermediate"}
    
    def _create_detailed_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed analysis"""
        return {"strengths": [], "areas_for_improvement": []}
    
    def _compile_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Compile performance metrics"""
        return {"scores": {}, "averages": {}}
    
    def _compile_achievements(self, data: Dict[str, Any], report_format: str) -> Dict[str, Any]:
        """Compile achievements"""
        return {"total_achievements": 5, "recent_achievements": []}
    
    def _identify_challenges(self, data: Dict[str, Any]) -> List[str]:
        """Identify challenges"""
        return ["Time management could be improved"]
    
    def _generate_report_recommendations(self, data: Dict[str, Any], report_format: str) -> List[str]:
        """Generate report recommendations"""
        return ["Continue current learning approach"]
    
    def _suggest_next_steps(self, data: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
        """Suggest next steps"""
        return ["Complete next module", "Review weak areas"]
    
    def _collect_trend_data(self, user: User, learning_path_id: Optional[str], trend_period: int) -> Dict[str, Any]:
        """Collect trend data"""
        return {"user": user, "period": trend_period, "data": []}
    
    def _analyze_specific_trend(self, data: Dict[str, Any], trend_type: str) -> Dict[str, Any]:
        """Analyze specific trend type"""
        return {"trend": "improving", "strength": "moderate"}
    
    def _analyze_learning_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze learning patterns"""
        return {"pattern_type": "consistent", "frequency": "regular"}
    
    def _generate_trend_predictions(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trend predictions"""
        return {"future_trend": "continued_improvement", "confidence": "high"}
    
    def _generate_trend_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate trend recommendations"""
        return ["Maintain current learning routine"]
    
    def _get_user_achievements(self, user: User, learning_path_id: Optional[str]) -> List[Dict[str, Any]]:
        """Get user achievements"""
        return []
    
    def _check_new_achievements(self, user: User, learning_path_id: Optional[str], current: List) -> List[Dict[str, Any]]:
        """Check for new achievements"""
        return []
    
    def _categorize_achievements(self, total_achievements: int) -> Dict[str, int]:
        """Categorize achievements"""
        return {"completion": 3, "effort": 2, "skill": 1}
    
    def _identify_recent_milestones(self, user: User, learning_path_id: Optional[str]) -> List[Dict[str, Any]]:
        """Identify recent milestones"""
        return []
    
    def _suggest_next_achievements(self, user: User, learning_path_id: Optional[str], summary: Dict) -> List[Dict[str, Any]]:
        """Suggest next achievements"""
        return []
    
    def _generate_achievement_recommendations(self, summary: Dict) -> List[str]:
        """Generate achievement recommendations"""
        return ["Focus on consistency to unlock more achievements"]
    
    def _analyze_path_performance(self, user: User, learning_path_id: str) -> Dict[str, Any]:
        """Analyze path performance"""
        return {"efficiency_score": 75, "engagement_score": 80, "completion_rate": 65}
    
    def _generate_optimization_suggestions(self, performance: Dict, goals: List[str]) -> List[Dict[str, Any]]:
        """Generate optimization suggestions"""
        return [{"area": "time_efficiency", "suggestion": "Break tasks into smaller chunks"}]
    
    def _suggest_path_modifications(self, user: User, learning_path_id: str, performance: Dict, goals: List[str]) -> List[Dict[str, Any]]:
        """Suggest path modifications"""
        return [{"modification": "reorder_modules", "reason": "improve_engagement"}]
    
    def _estimate_optimization_improvements(self, performance: Dict, suggestions: List) -> Dict[str, Any]:
        """Estimate optimization improvements"""
        return {"efficiency_gain": 15, "engagement_gain": 10}
    
    def _create_implementation_plan(self, modifications: List, suggestions: List) -> Dict[str, Any]:
        """Create implementation plan"""
        return {"phases": [], "timeline": "2 weeks"}
    
    def _define_success_metrics(self, goals: List[str]) -> Dict[str, Any]:
        """Define success metrics"""
        return {"efficiency": "time_to_completion", "engagement": "session_frequency"}
    
    def _calculate_completion_probability(self, progress_data: Dict, horizon: int) -> float:
        """Calculate completion probability"""
        return 0.75
    
    def _calculate_prediction_confidence(self, progress_data: Dict) -> float:
        """Calculate prediction confidence"""
        return 0.80
    
    def _create_completion_timeline(self, progress_data: Dict, horizon: int) -> Dict[str, Any]:
        """Create completion timeline"""
        return {"milestones": [], "probability_timeline": {}}
    
    def _identify_risk_factors(self, progress_data: Dict) -> List[str]:
        """Identify risk factors"""
        return []
    
    def _identify_accelerating_factors(self, progress_data: Dict) -> List[str]:
        """Identify accelerating factors"""
        return []
    
    def _analyze_completion_scenarios(self, progress_data: Dict, horizon: int) -> Dict[str, Any]:
        """Analyze completion scenarios"""
        return {"best_case": "early_completion", "most_likely": "on_time", "worst_case": "delayed"}
    
    def _generate_completion_recommendations(self, prediction: Dict) -> List[str]:
        """Generate completion recommendations"""
        return ["Continue current pace to maintain timeline"]
    
    def _collect_insight_data(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Collect insight data"""
        return {"user": user, "path_id": learning_path_id, "data": []}
    
    def _generate_performance_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance insights"""
        return {"strength_areas": [], "improvement_areas": []}
    
    def _generate_learning_pattern_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate learning pattern insights"""
        return {"learning_style": "visual", "preferred_time": "morning"}
    
    def _generate_behavioral_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate behavioral insights"""
        return {"engagement_pattern": "consistent", "help_seeking": "moderate"}
    
    def _extract_key_insights(self, data: Dict, insights: Dict) -> List[str]:
        """Extract key insights"""
        return ["Learning pace is consistent and effective"]
    
    def _generate_insight_based_recommendations(self, insights: Dict) -> List[str]:
        """Generate insight-based recommendations"""
        return ["Maintain current learning routine"]
    
    def _create_actionable_items(self, insights: Dict) -> List[Dict[str, Any]]:
        """Create actionable items"""
        return [{"action": "increase_practice", "priority": "medium"}]
    
    def _collect_visualization_data(self, user: User, learning_path_id: Optional[str], points: int) -> Dict[str, Any]:
        """Collect visualization data"""
        return {"user": user, "points": points, "data": []}
    
    def _create_progress_chart_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create progress chart data"""
        return {"labels": [], "datasets": []}
    
    def _create_timeline_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create timeline data"""
        return {"events": [], "timeline": []}
    
    def _create_comparison_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create comparison data"""
        return {"user_data": [], "benchmark_data": []}
    
    def _generate_chart_title(self, viz_type: str) -> str:
        """Generate chart title"""
        return f"Learning {viz_type.replace('_', ' ').title()}"
    
    def _get_data_range(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Get data range"""
        return {"start": "2023-01-01", "end": "2023-12-31"}
    
    def _calculate_summary_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary stats"""
        return {"total": 0, "average": 0, "trend": "stable"}
    
    def _define_interactive_elements(self, viz_type: str) -> List[Dict[str, Any]]:
        """Define interactive elements"""
        return [{"type": "tooltip", "trigger": "hover"}]
    
    # Additional helper methods
    def _calculate_time_efficiency(self, progress_activities: List) -> float:
        """Calculate time efficiency"""
        return 85.0  # Placeholder - would calculate actual time vs estimated time
    
    def _calculate_engagement_level(self, progress_data: Dict) -> float:
        """Calculate engagement level"""
        total_activities = progress_data['total_activities']
        days = 30  # Assume 30 days period
        daily_activity = total_activities / days
        
        if daily_activity >= 1:
            return 90.0
        elif daily_activity >= 0.5:
            return 75.0
        else:
            return 50.0
    
    def _assess_skill_development(self, progress_data: Dict) -> float:
        """Assess skill development"""
        return 80.0  # Placeholder - would analyze progression through difficulty levels
    
    def _breakdown_by_topic(self, progress_data: Dict) -> Dict[str, int]:
        """Breakdown progress by topic"""
        return {}  # Would analyze module topics
    
    def _breakdown_by_difficulty(self, progress_data: Dict) -> Dict[str, int]:
        """Breakdown progress by difficulty"""
        return {}  # Would analyze module difficulties
    
    def _breakdown_by_activity_type(self, progress_data: Dict) -> Dict[str, int]:
        """Breakdown progress by activity type"""
        return {}  # Would analyze types of activities
    
    def _generate_weekly_summary(self, progress_data: Dict) -> Dict[str, Any]:
        """Generate weekly summary"""
        return {}  # Would summarize progress by week
    
    def _analyze_performance_trends(self, progress_data: Dict) -> Dict[str, Any]:
        """Analyze performance trends"""
        return {}  # Would analyze score trends over time


# Import uuid and timedelta
import uuid
from datetime import timedelta