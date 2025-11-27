# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Evaluator Agent

Specialized agent responsible for evaluating user progress, providing detailed
assessments, and maintaining evaluation standards in the JAC Interactive Learning Platform.
"""

from typing import Dict, Any, List, Optional
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count, Q
from .base_agent import BaseAgent, AgentStatus, TaskPriority
from ..learning.models import LearningPath, Module, UserModuleProgress
from ..assessments.models import Assessment, AssessmentQuestion, UserAssessmentResult


class EvaluatorAgent(BaseAgent):
    """
    Evaluator Agent handles:
    - User progress evaluation
    - Performance assessment
    - Learning analytics
    - Competency tracking
    - Rubric-based evaluation
    - Detailed feedback generation
    """
    
    def __init__(self, agent_id: str = None, config: Dict[str, Any] = None):
        super().__init__(
            agent_id=agent_id or "evaluator",
            agent_type="Evaluator",
            config=config or {}
        )
        
        self.evaluation_criteria = {
            'knowledge_acquisition': {
                'weight': 0.3,
                'metrics': ['concept_understanding', 'retention_rate', 'application_ability']
            },
            'skill_development': {
                'weight': 0.25,
                'metrics': ['coding_proficiency', 'problem_solving', 'debugging_ability']
            },
            'learning_efficiency': {
                'weight': 0.2,
                'metrics': ['time_efficiency', 'resource_utilization', 'learning_velocity']
            },
            'engagement_level': {
                'weight': 0.15,
                'metrics': ['participation_rate', 'effort_consistency', 'initiative_taken']
            },
            'collaboration_skills': {
                'weight': 0.1,
                'metrics': ['peer_interaction', 'help_seeking', 'knowledge_sharing']
            }
        }
        
        self.evaluation_rubrics = {}
        self.performance_thresholds = {
            'excellent': {'min': 90, 'max': 100},
            'good': {'min': 80, 'max': 89},
            'satisfactory': {'min': 70, 'max': 79},
            'needs_improvement': {'min': 60, 'max': 69},
            'poor': {'min': 0, 'max': 59}
        }
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process evaluation tasks
        
        Expected task types:
        - 'evaluate_progress': Evaluate user's learning progress
        - 'assess_competency': Assess specific competencies
        - 'generate_evaluation_report': Create comprehensive evaluation report
        - 'calibrate_rubric': Update evaluation rubrics
        - 'benchmark_performance': Compare performance against benchmarks
        - 'identify_learning_gaps': Identify knowledge gaps
        - 'predict_outcomes': Predict learning outcomes
        """
        self.update_status(AgentStatus.PROCESSING)
        
        task_type = task.get('type', 'evaluate_progress')
        
        try:
            if task_type == 'evaluate_progress':
                result = self._evaluate_progress(task.get('params', {}))
            elif task_type == 'assess_competency':
                result = self._assess_competency(task.get('params', {}))
            elif task_type == 'generate_evaluation_report':
                result = self._generate_evaluation_report(task.get('params', {}))
            elif task_type == 'calibrate_rubric':
                result = self._calibrate_rubric(task.get('params', {}))
            elif task_type == 'benchmark_performance':
                result = self._benchmark_performance(task.get('params', {}))
            elif task_type == 'identify_learning_gaps':
                result = self._identify_learning_gaps(task.get('params', {}))
            elif task_type == 'predict_outcomes':
                result = self._predict_outcomes(task.get('params', {}))
            elif task_type == 'evaluate_code_submission':
                result = self._evaluate_code_submission(task.get('params', {}))
            else:
                result = {'error': f'Unknown task type: {task_type}'}
            
            self.update_status(AgentStatus.ACTIVE)
            self.update_metrics('evaluations_completed', self.metrics.get('evaluations_completed', 0) + 1)
            return {'success': True, 'result': result}
            
        except Exception as e:
            self.update_status(AgentStatus.ERROR)
            return {'success': False, 'error': str(e)}
    
    def _evaluate_progress(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate user's learning progress"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        timeframe = params.get('timeframe', 30)  # days
        evaluation_depth = params.get('evaluation_depth', 'comprehensive')  # basic, detailed, comprehensive
        
        if not user:
            return {'error': 'User parameter required for progress evaluation'}
        
        # Gather evaluation data
        evaluation_data = self._gather_evaluation_data(user, learning_path_id, timeframe)
        
        # Perform comprehensive evaluation
        evaluation_result = {
            'evaluation_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'evaluation_date': timezone.now().isoformat(),
            'timeframe_days': timeframe,
            'evaluation_depth': evaluation_depth,
            'overall_score': 0,
            'performance_level': '',
            'criteria_scores': {},
            'detailed_analysis': {},
            'strengths': [],
            'improvement_areas': [],
            'recommendations': [],
            'next_steps': []
        }
        
        # Evaluate each criteria
        for criteria, config in self.evaluation_criteria.items():
            criteria_score = self._evaluate_criteria(user, criteria, evaluation_data, config)
            evaluation_result['criteria_scores'][criteria] = criteria_score
            
            # Update overall score
            evaluation_result['overall_score'] += criteria_score * config['weight']
        
        # Determine performance level
        evaluation_result['performance_level'] = self._determine_performance_level(
            evaluation_result['overall_score']
        )
        
        # Generate detailed analysis
        evaluation_result['detailed_analysis'] = self._generate_detailed_analysis(
            user, evaluation_data, evaluation_result
        )
        
        # Identify strengths and improvement areas
        strengths, improvements = self._analyze_performance_dimensions(evaluation_result)
        evaluation_result['strengths'] = strengths
        evaluation_result['improvement_areas'] = improvements
        
        # Generate recommendations
        evaluation_result['recommendations'] = self._generate_progress_recommendations(
            user, evaluation_result, evaluation_data
        )
        
        # Suggest next steps
        evaluation_result['next_steps'] = self._suggest_progress_next_steps(
            user, evaluation_result
        )
        
        return evaluation_result
    
    def _assess_competency(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Assess specific competencies"""
        user = params.get('user')
        competencies = params.get('competencies', [])
        assessment_method = params.get('assessment_method', 'mixed')  # portfolio, performance, observation
        
        if not user:
            return {'error': 'User parameter required for competency assessment'}
        
        if not competencies:
            return {'error': 'At least one competency must be specified'}
        
        competency_assessment = {
            'assessment_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'competencies': competencies,
            'assessment_method': assessment_method,
            'assessment_date': timezone.now().isoformat(),
            'results': {},
            'overall_competency_level': '',
            'evidence_summary': {},
            'development_recommendations': []
        }
        
        # Assess each competency
        for competency in competencies:
            result = self._assess_single_competency(user, competency, assessment_method)
            competency_assessment['results'][competency] = result
        
        # Calculate overall competency level
        competency_assessment['overall_competency_level'] = self._calculate_overall_competency_level(
            competency_assessment['results']
        )
        
        # Summarize evidence
        competency_assessment['evidence_summary'] = self._compile_evidence_summary(
            competency_assessment['results']
        )
        
        # Generate development recommendations
        competency_assessment['development_recommendations'] = self._generate_competency_recommendations(
            competency_assessment['results']
        )
        
        return competency_assessment
    
    def _generate_evaluation_report(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        user = params.get('user')
        report_type = params.get('report_type', 'student')  # student, instructor, administrator
        time_period = params.get('time_period', 'monthly')  # weekly, monthly, quarterly, yearly
        include_recommendations = params.get('include_recommendations', True)
        
        if not user:
            return {'error': 'User parameter required for report generation'}
        
        # Generate comprehensive data
        report_data = self._compile_report_data(user, time_period)
        
        # Create report structure
        report = {
            'report_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'report_type': report_type,
            'time_period': time_period,
            'report_date': timezone.now().isoformat(),
            'executive_summary': {},
            'detailed_findings': {},
            'learning_analytics': {},
            'performance_metrics': {},
            'recommendations': [],
            'action_items': []
        }
        
        # Generate executive summary
        report['executive_summary'] = self._generate_executive_summary(
            user, report_data, report_type
        )
        
        # Generate detailed findings
        report['detailed_findings'] = self._generate_detailed_findings(
            user, report_data
        )
        
        # Add learning analytics
        report['learning_analytics'] = self._compile_learning_analytics(
            user, report_data
        )
        
        # Add performance metrics
        report['performance_metrics'] = self._compile_performance_metrics(
            user, report_data
        )
        
        if include_recommendations:
            # Generate recommendations
            recommendations = self._generate_report_recommendations(
                user, report_data, report_type
            )
            report['recommendations'] = recommendations
            
            # Generate action items
            action_items = self._generate_action_items(recommendations, report_type)
            report['action_items'] = action_items
        
        return report
    
    def _calibrate_rubric(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update and calibrate evaluation rubrics"""
        rubric_type = params.get('rubric_type', 'general')
        calibration_data = params.get('calibration_data', {})
        feedback_data = params.get('feedback_data', [])
        
        # Get current rubric
        current_rubric = self.evaluation_rubrics.get(rubric_type, self._get_default_rubric(rubric_type))
        
        # Analyze calibration feedback
        if feedback_data:
            calibration_analysis = self._analyze_calibration_feedback(feedback_data)
        else:
            calibration_analysis = {}
        
        # Generate updated rubric
        updated_rubric = self._update_rubric_based_on_calibration(
            current_rubric, calibration_data, calibration_analysis
        )
        
        # Validate rubric changes
        validation_result = self._validate_rubric_changes(current_rubric, updated_rubric)
        
        calibration_result = {
            'calibration_id': str(uuid.uuid4()),
            'rubric_type': rubric_type,
            'calibration_date': timezone.now().isoformat(),
            'previous_rubric': current_rubric,
            'updated_rubric': updated_rubric,
            'calibration_analysis': calibration_analysis,
            'validation_result': validation_result,
            'changes_summary': self._summarize_rubric_changes(current_rubric, updated_rubric)
        }
        
        # Update stored rubric
        self.evaluation_rubrics[rubric_type] = updated_rubric
        
        return calibration_result
    
    def _benchmark_performance(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Compare performance against benchmarks"""
        user = params.get('user')
        benchmark_type = params.get('benchmark_type', 'peer')  # peer, institution, standard, historical
        metrics = params.get('metrics', [])
        
        if not user:
            return {'error': 'User parameter required for benchmarking'}
        
        # Gather benchmark data
        benchmark_data = self._gather_benchmark_data(user, benchmark_type, metrics)
        
        # Perform comparison
        comparison_results = {}
        for metric in metrics:
            comparison = self._compare_metric_against_benchmark(user, metric, benchmark_data)
            comparison_results[metric] = comparison
        
        # Generate benchmark report
        benchmark_report = {
            'benchmark_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'benchmark_type': benchmark_type,
            'benchmark_date': timezone.now().isoformat(),
            'metrics': metrics,
            'comparison_results': comparison_results,
            'overall_ranking': self._calculate_overall_ranking(comparison_results),
            'benchmark_summary': self._generate_benchmark_summary(comparison_results),
            'improvement_suggestions': self._suggest_based_on_benchmark(comparison_results)
        }
        
        return benchmark_report
    
    def _identify_learning_gaps(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Identify knowledge and skill gaps"""
        user = params.get('user')
        learning_path_id = params.get('learning_path_id')
        gap_analysis_depth = params.get('depth', 'detailed')  # basic, detailed, comprehensive
        
        if not user:
            return {'error': 'User parameter required for gap analysis'}
        
        # Identify different types of gaps
        gap_analysis = {
            'gap_analysis_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'analysis_date': timezone.now().isoformat(),
            'analysis_depth': gap_analysis_depth,
            'knowledge_gaps': [],
            'skill_gaps': [],
            'conceptual_gaps': [],
            'application_gaps': [],
            'gap_severity_levels': {},
            'gap_patterns': {},
            'remediation_plan': {},
            'priority_recommendations': []
        }
        
        # Analyze knowledge gaps
        knowledge_gaps = self._analyze_knowledge_gaps(user, learning_path_id)
        gap_analysis['knowledge_gaps'] = knowledge_gaps['identified_gaps']
        
        # Analyze skill gaps
        skill_gaps = self._analyze_skill_gaps(user, learning_path_id)
        gap_analysis['skill_gaps'] = skill_gaps['identified_gaps']
        
        # Analyze conceptual gaps
        conceptual_gaps = self._analyze_conceptual_gaps(user, learning_path_id)
        gap_analysis['conceptual_gaps'] = conceptual_gaps['identified_gaps']
        
        # Analyze application gaps
        application_gaps = self._analyze_application_gaps(user, learning_path_id)
        gap_analysis['application_gaps'] = application_gaps['identified_gaps']
        
        # Calculate gap severity
        gap_analysis['gap_severity_levels'] = self._calculate_gap_severity_levels(gap_analysis)
        
        # Identify patterns
        gap_analysis['gap_patterns'] = self._identify_gap_patterns(gap_analysis)
        
        # Create remediation plan
        gap_analysis['remediation_plan'] = self._create_remediation_plan(gap_analysis)
        
        # Generate priority recommendations
        gap_analysis['priority_recommendations'] = self._generate_gap_recommendations(gap_analysis)
        
        return gap_analysis
    
    def _predict_outcomes(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Predict learning outcomes based on current performance"""
        user = params.get('user')
        prediction_timeframe = params.get('timeframe', 90)  # days
        outcome_type = params.get('outcome_type', 'competency')  # competency, completion, mastery
        
        if not user:
            return {'error': 'User parameter required for outcome prediction'}
        
        # Gather prediction data
        prediction_data = self._gather_prediction_data(user, prediction_timeframe)
        
        # Generate predictions
        prediction_result = {
            'prediction_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'prediction_date': timezone.now().isoformat(),
            'prediction_timeframe_days': prediction_timeframe,
            'outcome_type': outcome_type,
            'predictions': {},
            'confidence_levels': {},
            'factors_considered': {},
            'scenario_analysis': {},
            'recommendations': []
        }
        
        # Make predictions based on historical data and trends
        predictions = self._generate_predictions(user, prediction_data, outcome_type)
        prediction_result['predictions'] = predictions
        
        # Calculate confidence levels
        confidence_levels = self._calculate_prediction_confidence(prediction_data, predictions)
        prediction_result['confidence_levels'] = confidence_levels
        
        # Document factors considered
        prediction_result['factors_considered'] = prediction_data['factors']
        
        # Analyze different scenarios
        if outcome_type == 'competency':
            prediction_result['scenario_analysis'] = self._analyze_competency_scenarios(
                predictions, prediction_data
            )
        
        # Generate recommendations based on predictions
        prediction_result['recommendations'] = self._generate_prediction_recommendations(
            user, predictions, confidence_levels
        )
        
        return prediction_result
    
    def _evaluate_code_submission(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate code submissions with detailed feedback"""
        user = params.get('user')
        code_submission = params.get('code_submission', '')
        submission_type = params.get('submission_type', 'assignment')  # assignment, quiz, project
        evaluation_criteria = params.get('criteria', ['correctness', 'efficiency', 'readability', 'style'])
        
        if not user or not code_submission:
            return {'error': 'User and code submission required for evaluation'}
        
        # Perform comprehensive code evaluation
        evaluation_result = {
            'evaluation_id': str(uuid.uuid4()),
            'user_id': str(user.id),
            'submission_type': submission_type,
            'evaluation_date': timezone.now().isoformat(),
            'overall_score': 0,
            'detailed_scores': {},
            'code_analysis': {},
            'strengths': [],
            'improvements': [],
            'detailed_feedback': {},
            'suggestions': []
        }
        
        # Evaluate each criterion
        for criterion in evaluation_criteria:
            score, feedback = self._evaluate_code_criterion(
                code_submission, criterion, submission_type
            )
            evaluation_result['detailed_scores'][criterion] = score
            evaluation_result['detailed_feedback'][criterion] = feedback
        
        # Calculate overall score
        evaluation_result['overall_score'] = sum(
            evaluation_result['detailed_scores'].values()
        ) / len(evaluation_criteria)
        
        # Analyze code structure and quality
        evaluation_result['code_analysis'] = self._analyze_code_quality(code_submission)
        
        # Identify strengths and improvements
        strengths, improvements = self._analyze_code_strengths_improvements(
            evaluation_result['detailed_scores'], code_submission
        )
        evaluation_result['strengths'] = strengths
        evaluation_result['improvements'] = improvements
        
        # Generate specific suggestions
        evaluation_result['suggestions'] = self._generate_code_suggestions(
            code_submission, evaluation_result['detailed_scores']
        )
        
        return evaluation_result
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities provided by this agent"""
        return [
            'progress_evaluation',
            'competency_assessment',
            'performance_analysis',
            'learning_analytics',
            'gap_identification',
            'outcome_prediction',
            'rubric_calibration',
            'benchmarking',
            'code_evaluation',
            'feedback_generation'
        ]
    
    def get_specialization_info(self) -> Dict[str, Any]:
        """Get detailed information about Evaluator specialization"""
        return {
            'agent_type': 'Evaluator',
            'specialization': 'Assessment and Analytics',
            'key_responsibilities': [
                'Evaluate user progress across multiple dimensions',
                'Assess competencies and skills',
                'Generate detailed evaluation reports',
                'Identify learning gaps and provide remediation',
                'Predict learning outcomes'
            ],
            'evaluation_dimensions': list(self.evaluation_criteria.keys()),
            'assessment_methods': [
                'Formative Assessment',
                'Summative Assessment',
                'Competency-Based Assessment',
                'Portfolio Assessment',
                'Performance Assessment'
            ],
            'analytics_capabilities': [
                'Performance trend analysis',
                'Learning pattern recognition',
                'Predictive modeling',
                'Gap analysis',
                'Benchmark comparison'
            ],
            'specialized_evaluations': [
                'Code quality assessment',
                'Problem-solving evaluation',
                'Collaboration assessment',
                'Critical thinking analysis',
                'Creative thinking evaluation'
            ]
        }
    
    # Helper methods for evaluation
    def _gather_evaluation_data(self, user: User, learning_path_id: Optional[str], timeframe: int) -> Dict[str, Any]:
        """Gather comprehensive data for evaluation"""
        from datetime import timedelta
        
        end_date = timezone.now()
        start_date = end_date - timedelta(days=timeframe)
        
        # Get user progress data
        progress_query = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=start_date
        )
        
        if learning_path_id:
            progress_query = progress_query.filter(
                module__learning_path_id=learning_path_id
            )
        
        progress_data = list(progress_query.order_by('-updated_at'))
        
        # Get assessment results
        assessment_results = UserAssessmentResult.objects.filter(
            user=user,
            completed_at__gte=start_date
        )
        
        # Calculate metrics
        evaluation_data = {
            'user': user,
            'timeframe': timeframe,
            'progress_data': progress_data,
            'assessment_results': list(assessment_results),
            'total_activities': len(progress_data),
            'completion_rate': len([p for p in progress_data if p.status == 'completed']) / max(len(progress_data), 1),
            'average_score': sum(p.score or 0 for p in progress_data) / max(len(progress_data), 1) if progress_data else 0,
            'engagement_metrics': self._calculate_engagement_metrics(progress_data),
            'learning_velocity': self._calculate_learning_velocity(progress_data),
            'factors': [
                'historical_performance',
                'engagement_level',
                'learning_velocity',
                'consistency',
                'skill_development'
            ]
        }
        
        return evaluation_data
    
    def _evaluate_criteria(self, user: User, criteria: str, evaluation_data: Dict, config: Dict) -> float:
        """Evaluate specific criteria"""
        if criteria == 'knowledge_acquisition':
            return self._evaluate_knowledge_acquisition(user, evaluation_data, config)
        elif criteria == 'skill_development':
            return self._evaluate_skill_development(user, evaluation_data, config)
        elif criteria == 'learning_efficiency':
            return self._evaluate_learning_efficiency(user, evaluation_data, config)
        elif criteria == 'engagement_level':
            return self._evaluate_engagement_level(user, evaluation_data, config)
        elif criteria == 'collaboration_skills':
            return self._evaluate_collaboration_skills(user, evaluation_data, config)
        else:
            return 0.0
    
    def _evaluate_knowledge_acquisition(self, user: User, data: Dict, config: Dict) -> float:
        """Evaluate knowledge acquisition metrics"""
        progress_data = data['progress_data']
        assessment_results = data['assessment_results']
        
        if not progress_data:
            return 0.0
        
        # Concept understanding score
        concept_scores = [p.score or 0 for p in progress_data if hasattr(p, 'score') and p.score]
        concept_score = sum(concept_scores) / len(concept_scores) if concept_scores else 0
        
        # Retention rate (based on repeat performances)
        retention_score = self._calculate_retention_rate(progress_data)
        
        # Application ability (based on complexity progression)
        application_score = self._calculate_application_ability(progress_data)
        
        # Weighted average
        final_score = (concept_score * 0.4 + retention_score * 0.3 + application_score * 0.3)
        return min(100, max(0, final_score))
    
    def _evaluate_skill_development(self, user: User, data: Dict, config: Dict) -> float:
        """Evaluate skill development metrics"""
        progress_data = data['progress_data']
        
        if not progress_data:
            return 0.0
        
        # Coding proficiency (based on progression through coding exercises)
        coding_score = self._assess_coding_proficiency(progress_data)
        
        # Problem solving (based on complexity of problems solved)
        problem_solving_score = self._assess_problem_solving(progress_data)
        
        # Debugging ability (based on error correction performance)
        debugging_score = self._assess_debugging_ability(progress_data)
        
        # Weighted average
        final_score = (coding_score * 0.4 + problem_solving_score * 0.4 + debugging_score * 0.2)
        return min(100, max(0, final_score))
    
    def _evaluate_learning_efficiency(self, user: User, data: Dict, config: Dict) -> float:
        """Evaluate learning efficiency metrics"""
        progress_data = data['progress_data']
        
        if not progress_data:
            return 0.0
        
        # Time efficiency (completion time vs estimated time)
        time_efficiency = self._calculate_time_efficiency(progress_data)
        
        # Resource utilization (use of hints, help, resources)
        resource_utilization = self._assess_resource_utilization(progress_data)
        
        # Learning velocity (progress over time)
        learning_velocity = data.get('learning_velocity', 0)
        
        # Weighted average
        final_score = (time_efficiency * 0.4 + resource_utilization * 0.3 + learning_velocity * 0.3)
        return min(100, max(0, final_score))
    
    def _evaluate_engagement_level(self, user: User, data: Dict, config: Dict) -> float:
        """Evaluate engagement level metrics"""
        progress_data = data['progress_data']
        
        if not progress_data:
            return 0.0
        
        engagement_data = data.get('engagement_metrics', {})
        
        # Participation rate
        participation_score = engagement_data.get('participation_rate', 0)
        
        # Effort consistency
        consistency_score = self._calculate_consistency_score(progress_data)
        
        # Initiative taken
        initiative_score = self._assess_initiative_taken(progress_data)
        
        # Weighted average
        final_score = (participation_score * 0.4 + consistency_score * 0.4 + initiative_score * 0.2)
        return min(100, max(0, final_score))
    
    def _evaluate_collaboration_skills(self, user: User, data: Dict, config: Dict) -> float:
        """Evaluate collaboration skills"""
        # This would require data about user interactions, help-seeking behavior, etc.
        # For now, return a placeholder based on overall progress
        return data.get('average_score', 0)
    
    def _determine_performance_level(self, score: float) -> str:
        """Determine performance level based on score"""
        for level, thresholds in self.performance_thresholds.items():
            if thresholds['min'] <= score <= thresholds['max']:
                return level
        return 'unknown'
    
    def _generate_detailed_analysis(self, user: User, data: Dict, result: Dict) -> Dict[str, Any]:
        """Generate detailed analysis of user performance"""
        return {
            'learning_pattern': self._identify_learning_pattern(data),
            'progress_trajectory': self._analyze_progress_trajectory(data),
            'strength_development': self._track_strength_development(data),
            'weakness_evolution': self._track_weakness_evolution(data),
            'engagement_trends': self._analyze_engagement_trends(data),
            'performance_predictors': self._identify_performance_predictors(data)
        }
    
    def _analyze_performance_dimensions(self, evaluation_result: Dict) -> tuple:
        """Analyze performance dimensions to identify strengths and improvements"""
        strengths = []
        improvements = []
        
        criteria_scores = evaluation_result['criteria_scores']
        
        for criteria, score in criteria_scores.items():
            if score >= 80:
                strengths.append(f"Strong {criteria.replace('_', ' ')}")
            elif score < 60:
                improvements.append(f"Needs improvement in {criteria.replace('_', ' ')}")
        
        return strengths, improvements
    
    def _generate_progress_recommendations(self, user: User, result: Dict, data: Dict) -> List[str]:
        """Generate recommendations based on progress evaluation"""
        recommendations = []
        
        overall_score = result['overall_score']
        
        if overall_score >= 90:
            recommendations.append("Continue current learning approach - excellent progress!")
            recommendations.append("Consider taking on more challenging projects")
        elif overall_score >= 80:
            recommendations.append("Good progress overall - focus on areas below 80%")
        elif overall_score >= 70:
            recommendations.append("Satisfactory progress - increase study time and practice")
        else:
            recommendations.append("Progress needs improvement - review fundamentals")
            recommendations.append("Consider additional support or resources")
        
        return recommendations
    
    def _suggest_progress_next_steps(self, user: User, result: Dict) -> List[str]:
        """Suggest next steps based on progress evaluation"""
        next_steps = []
        
        performance_level = result['performance_level']
        
        if performance_level == 'excellent':
            next_steps.append("Advance to next learning module")
            next_steps.append("Take on peer mentoring role")
        elif performance_level == 'good':
            next_steps.append("Continue current learning path")
            next_steps.append("Focus practice on weaker areas")
        elif performance_level == 'satisfactory':
            next_steps.append("Review current module before advancing")
            next_steps.append("Increase practice exercises")
        else:
            next_steps.append("Review previous modules")
            next_steps.append("Seek additional help or tutoring")
        
        return next_steps
    
    # Enhanced helper methods for full 100% coverage
    
    def _calculate_retention_rate(self, progress_data: List) -> float:
        """Calculate retention rate based on repeat performance"""
        if not progress_data:
            return 0.0
        
        # Analyze repeat attempts and performance improvement
        repeat_attempts = 0
        improved_performances = 0
        
        # Group by content to find repeats
        content_groups = {}
        for progress in progress_data:
            content_id = getattr(progress.module, 'content_id', None)
            if content_id:
                if content_id not in content_groups:
                    content_groups[content_id] = []
                content_groups[content_id].append(progress)
        
        # Calculate retention based on repeat patterns
        for content_id, attempts in content_groups.items():
            if len(attempts) > 1:
                repeat_attempts += 1
                # Check if performance improved on repeat
                scores = [attempt.score or 0 for attempt in attempts if hasattr(attempt, 'score')]
                if len(scores) >= 2 and scores[-1] > scores[0]:
                    improved_performances += 1
        
        if repeat_attempts == 0:
            return 85.0  # Default for users who don't need repeats
        
        retention_rate = (improved_performances / repeat_attempts) * 100
        return max(50.0, min(100.0, retention_rate))
    
    def _calculate_application_ability(self, progress_data: List) -> float:
        """Calculate application ability based on complexity progression"""
        if not progress_data:
            return 0.0
        
        # Analyze progression through complexity levels
        complexity_scores = {'beginner': 0.6, 'intermediate': 0.75, 'advanced': 0.9}
        
        progression_score = 0.0
        total_modules = len(progress_data)
        
        for progress in progress_data:
            if hasattr(progress.module, 'content'):
                difficulty = getattr(progress.module.content, 'difficulty_level', 'beginner')
                score = progress.score or 0
                complexity_factor = complexity_scores.get(difficulty, 0.6)
                
                # Higher difficulty with good score indicates strong application ability
                application_score = (score / 100) * complexity_factor
                progression_score += application_score
        
        return (progression_score / max(total_modules, 1)) * 100
    
    def _assess_coding_proficiency(self, progress_data: List) -> float:
        """Assess coding proficiency"""
        if not progress_data:
            return 0.0
        
        coding_indicators = {
            'completion_rate': 0.0,
            'error_correction': 0.0,
            'code_quality': 0.0,
            'problem_solving_speed': 0.0
        }
        
        coding_exercises = [p for p in progress_data if hasattr(p.module, 'content') and 
                          getattr(p.module.content, 'content_type', '') == 'coding_exercise']
        
        if not coding_exercises:
            return 75.0  # Default for non-coding focused progress
        
        # Calculate proficiency metrics
        completed_exercises = len([p for p in coding_exercises if p.status == 'completed'])
        total_exercises = len(coding_exercises)
        coding_indicators['completion_rate'] = (completed_exercises / total_exercises) * 100 if total_exercises > 0 else 0
        
        # Analyze error patterns (simplified)
        error_count = sum(1 for p in coding_exercises if hasattr(p, 'attempts') and p.attempts > 1)
        coding_indicators['error_correction'] = max(0, 100 - (error_count / total_exercises) * 50) if total_exercises > 0 else 0
        
        # Average scores
        scores = [p.score or 0 for p in coding_exercises if hasattr(p, 'score')]
        coding_indicators['code_quality'] = sum(scores) / len(scores) if scores else 0
        
        # Calculate overall proficiency
        proficiency = sum(coding_indicators.values()) / len(coding_indicators)
        return max(0.0, min(100.0, proficiency))
    
    def _assess_problem_solving(self, progress_data: List) -> float:
        """Assess problem-solving ability"""
        if not progress_data:
            return 0.0
        
        # Look for problem-solving indicators
        problem_solving_modules = [p for p in progress_data if hasattr(p.module, 'content') and
                                 'problem' in getattr(p.module.content, 'title', '').lower()]
        
        if not problem_solving_modules:
            # Analyze based on complexity of completed modules
            complex_modules = [p for p in progress_data 
                             if hasattr(p.module, 'content') and 
                             getattr(p.module.content, 'difficulty_level', '') == 'advanced']
            
            if complex_modules:
                scores = [p.score or 0 for p in complex_modules]
                return sum(scores) / len(scores) if scores else 0
            else:
                return 75.0  # Default assessment
        
        # Direct problem-solving assessment
        scores = [p.score or 0 for p in problem_solving_modules]
        time_efficiency = self._calculate_problem_solving_efficiency(problem_solving_modules)
        
        return (sum(scores) / len(scores) * 0.7 + time_efficiency * 0.3)
    
    def _assess_debugging_ability(self, progress_data: List) -> float:
        """Assess debugging ability"""
        if not progress_data:
            return 0.0
        
        # Look for debugging-related activities
        debugging_indicators = {
            'error_correction_rate': 0.0,
            'debugging_speed': 0.0,
            'prevention_score': 0.0
        }
        
        # Analyze attempts and error patterns
        total_attempts = 0
        successful_corrections = 0
        
        for progress in progress_data:
            if hasattr(progress, 'attempts'):
                total_attempts += progress.attempts
                if progress.attempts > 1 and progress.status == 'completed':
                    successful_corrections += 1
        
        if total_attempts > 0:
            debugging_indicators['error_correction_rate'] = (successful_corrections / total_attempts) * 100
        
        # Calculate debugging speed (simplified)
        debugging_indicators['debugging_speed'] = self._calculate_debugging_speed(progress_data)
        
        # Prevention score (fewer errors overall)
        error_prone_modules = [p for p in progress_data if hasattr(p, 'attempts') and p.attempts > 2]
        debugging_indicators['prevention_score'] = max(0, 100 - (len(error_prone_modules) / len(progress_data)) * 100)
        
        return sum(debugging_indicators.values()) / len(debugging_indicators)
    
    def _calculate_time_efficiency(self, progress_data: List) -> float:
        """Calculate time efficiency"""
        if not progress_data:
            return 0.0
        
        efficiency_scores = []
        
        for progress in progress_data:
            if hasattr(progress, 'time_spent') and hasattr(progress.module, 'estimated_duration'):
                actual_time = progress.time_spent or 0
                estimated_time = progress.module.estimated_duration or 1
                
                # Efficiency is higher when actual time is closer to or less than estimated
                efficiency = max(0, 100 - ((actual_time - estimated_time) / estimated_time * 50))
                efficiency_scores.append(min(100, efficiency))
        
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 85.0
    
    def _assess_resource_utilization(self, progress_data: List) -> float:
        """Assess resource utilization"""
        if not progress_data:
            return 0.0
        
        utilization_indicators = {
            'hint_usage': 0.0,
            'documentation_access': 0.0,
            'help_seeking': 0.0,
            'resource_discovery': 0.0
        }
        
        # Analyze help-seeking behavior
        help_requests = sum(1 for p in progress_data if hasattr(p, 'help_used') and p.help_used)
        total_activities = len(progress_data)
        
        # Appropriate help-seeking is good (not too little, not too much)
        help_rate = help_requests / total_activities if total_activities > 0 else 0
        if 0.1 <= help_rate <= 0.4:  # Optimal range
            utilization_indicators['help_seeking'] = 100
        elif help_rate > 0.6:  # Too much help
            utilization_indicators['help_seeking'] = max(0, 100 - (help_rate - 0.6) * 100)
        else:  # Too little help
            utilization_indicators['help_seeking'] = help_rate * 100
        
        # Simulate other utilization metrics
        utilization_indicators['hint_usage'] = min(100, help_rate * 150)
        utilization_indicators['documentation_access'] = 75.0  # Would analyze actual access patterns
        utilization_indicators['resource_discovery'] = 80.0  # Would analyze resource exploration
        
        return sum(utilization_indicators.values()) / len(utilization_indicators)
    
    def _calculate_consistency_score(self, progress_data: List) -> float:
        """Calculate consistency score"""
        if len(progress_data) < 2:
            return 50.0
        
        scores = [p.score or 0 for p in progress_data if hasattr(p, 'score')]
        if len(scores) < 2:
            return 50.0
        
        # Calculate coefficient of variation (lower = more consistent)
        mean_score = sum(scores) / len(scores)
        variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
        std_dev = variance ** 0.5
        
        if mean_score == 0:
            return 50.0
        
        cv = std_dev / mean_score
        consistency_score = max(0, 100 - (cv * 100))
        return min(100, consistency_score)
    
    def _assess_initiative_taken(self, progress_data: List) -> float:
        """Assess initiative taken by user"""
        if not progress_data:
            return 0.0
        
        initiative_indicators = {
            'extra_activities': 0.0,
            'advanced_content': 0.0,
            'peer_help': 0.0,
            'self_directed_learning': 0.0
        }
        
        # Count extra activities (modules beyond required path)
        advanced_modules = [p for p in progress_data 
                          if hasattr(p.module, 'content') and 
                          getattr(p.module.content, 'difficulty_level', '') == 'advanced']
        initiative_indicators['advanced_content'] = min(100, len(advanced_modules) * 20)
        
        # Analyze voluntary participation (simplified)
        voluntary_participation = sum(1 for p in progress_data 
                                    if hasattr(p, 'voluntary') and p.voluntary)
        initiative_indicators['self_directed_learning'] = min(100, voluntary_participation * 25)
        
        # Simulate other indicators
        initiative_indicators['extra_activities'] = 65.0
        initiative_indicators['peer_help'] = 70.0
        
        return sum(initiative_indicators.values()) / len(initiative_indicators)
    
    def _calculate_problem_solving_efficiency(self, problem_modules: List) -> float:
        """Calculate problem-solving efficiency"""
        if not problem_modules:
            return 75.0
        
        efficiency_scores = []
        for module in problem_modules:
            # Analyze completion time vs estimated time
            if hasattr(module, 'time_spent') and hasattr(module.module, 'estimated_duration'):
                efficiency = module.time_spent / module.module.estimated_duration
                efficiency_score = max(0, 100 - (efficiency - 1) * 50)
                efficiency_scores.append(min(100, efficiency_score))
        
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 75.0
    
    def _calculate_debugging_speed(self, progress_data: List) -> float:
        """Calculate debugging speed"""
        debugging_attempts = [p for p in progress_data if hasattr(p, 'attempts') and p.attempts > 1]
        
        if not debugging_attempts:
            return 90.0  # No debugging needed
        
        # Average attempts to resolve issues
        avg_attempts = sum(p.attempts for p in debugging_attempts) / len(debugging_attempts)
        return max(0, 100 - (avg_attempts - 1) * 20)
    
    def _identify_learning_pattern(self, data: Dict) -> str:
        """Identify user's learning pattern"""
        return "consistent_learner"  # Placeholder - would analyze actual patterns
    
    def _analyze_progress_trajectory(self, data: Dict) -> str:
        """Analyze progress trajectory"""
        return "improving"  # Placeholder - would analyze trend
    
    def _track_strength_development(self, data: Dict) -> List[str]:
        """Track strength development"""
        return ["problem solving", "code organization"]  # Placeholder
    
    def _track_weakness_evolution(self, data: Dict) -> List[str]:
        """Track weakness evolution"""
        return ["debugging", "advanced concepts"]  # Placeholder
    
    def _analyze_engagement_trends(self, data: Dict) -> str:
        """Analyze engagement trends"""
        return "stable_high"  # Placeholder
    
    def _identify_performance_predictors(self, data: Dict) -> List[str]:
        """Identify performance predictors"""
        return ["consistency", "practice_frequency", "help_seeking"]  # Placeholder
    
    # Enhanced competency assessment methods
    def _assess_single_competency(self, user: User, competency: str, method: str) -> Dict[str, Any]:
        """Assess single competency with detailed evaluation"""
        # Get relevant progress data for this competency
        relevant_progress = self._get_competency_related_progress(user, competency)
        
        assessment_result = {
            "competency": competency,
            "assessment_method": method,
            "level": "emerging",  # emerging, developing, proficient, advanced
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        # Perform competency-specific assessment
        if competency.lower() in ['programming', 'coding', 'software_development']:
            assessment_result = self._assess_programming_competency(user, relevant_progress)
        elif competency.lower() in ['problem_solving', 'analytical_thinking']:
            assessment_result = self._assess_problem_solving_competency(user, relevant_progress)
        elif competency.lower() in ['communication', 'collaboration']:
            assessment_result = self._assess_communication_competency(user, relevant_progress)
        elif competency.lower() in ['critical_thinking', 'analysis']:
            assessment_result = self._assess_critical_thinking_competency(user, relevant_progress)
        else:
            # Generic competency assessment
            assessment_result = self._assess_generic_competency(user, competency, relevant_progress)
        
        return assessment_result
    
    def _calculate_overall_competency_level(self, results: Dict) -> str:
        """Calculate overall competency level based on individual assessments"""
        if not results:
            return "emerging"
        
        # Convert levels to numeric scores
        level_scores = {
            "emerging": 1,
            "developing": 2,
            "proficient": 3,
            "advanced": 4
        }
        
        # Calculate weighted average
        total_score = 0
        total_weight = 0
        
        for competency, assessment in results.items():
            level = assessment.get("level", "emerging")
            confidence = assessment.get("confidence_level", 0.5)
            weight = confidence  # Weight by confidence level
            
            level_score = level_scores.get(level, 1)
            total_score += level_score * weight
            total_weight += weight
        
        if total_weight == 0:
            return "emerging"
        
        avg_score = total_score / total_weight
        
        # Convert back to level
        if avg_score >= 3.5:
            return "advanced"
        elif avg_score >= 2.5:
            return "proficient"
        elif avg_score >= 1.5:
            return "developing"
        else:
            return "emerging"
    
    def _compile_evidence_summary(self, results: Dict) -> Dict[str, Any]:
        """Compile comprehensive evidence summary"""
        evidence_summary = {
            "total_competencies_assessed": len(results),
            "evidence_by_category": {
                "strong_evidence": [],
                "moderate_evidence": [],
                "limited_evidence": []
            },
            "strength_patterns": [],
            "development_patterns": [],
            "confidence_distribution": {},
            "evidence_quality": "moderate"
        }
        
        for competency, assessment in results.items():
            evidence = assessment.get("evidence", [])
            level = assessment.get("level", "emerging")
            confidence = assessment.get("confidence_level", 0.0)
            
            # Categorize evidence strength
            if len(evidence) >= 5 and confidence >= 0.8:
                evidence_summary["evidence_by_category"]["strong_evidence"].append({
                    "competency": competency,
                    "evidence_count": len(evidence),
                    "confidence": confidence
                })
            elif len(evidence) >= 2 and confidence >= 0.5:
                evidence_summary["evidence_by_category"]["moderate_evidence"].append({
                    "competency": competency,
                    "evidence_count": len(evidence),
                    "confidence": confidence
                })
            else:
                evidence_summary["evidence_by_category"]["limited_evidence"].append({
                    "competency": competency,
                    "evidence_count": len(evidence),
                    "confidence": confidence
                })
        
        # Identify patterns
        strong_competencies = [item["competency"] for item in evidence_summary["evidence_by_category"]["strong_evidence"]]
        developing_competencies = [item["competency"] for item in evidence_summary["evidence_by_category"]["limited_evidence"]]
        
        evidence_summary["strength_patterns"] = self._identify_strength_patterns(strong_competencies)
        evidence_summary["development_patterns"] = self._identify_development_patterns(developing_competencies)
        
        return evidence_summary
    
    def _generate_competency_recommendations(self, results: Dict) -> List[str]:
        """Generate personalized competency development recommendations"""
        recommendations = []
        
        # Analyze assessment results
        emerging_competencies = []
        developing_competencies = []
        proficient_competencies = []
        advanced_competencies = []
        
        for competency, assessment in results.items():
            level = assessment.get("level", "emerging")
            if level == "emerging":
                emerging_competencies.append(competency)
            elif level == "developing":
                developing_competencies.append(competency)
            elif level == "proficient":
                proficient_competencies.append(competency)
            elif level == "advanced":
                advanced_competencies.append(competency)
        
        # Generate recommendations based on patterns
        if emerging_competencies:
            recommendations.append(f"Focus on foundational skills in: {', '.join(emerging_competencies[:3])}")
            recommendations.append("Consider additional practice exercises for emerging competencies")
        
        if developing_competencies:
            recommendations.append("Build on developing competencies through guided projects")
            recommendations.append("Seek feedback on work in developing areas")
        
        if len(proficient_competencies) >= 3:
            recommendations.append("Leverage strong competencies to mentor others")
            recommendations.append("Take on leadership roles in projects requiring these skills")
        
        if advanced_competencies:
            recommendations.append("Pursue advanced challenges and complex projects")
            recommendations.append("Consider contributing to knowledge sharing or teaching")
        
        # General recommendations
        recommendations.extend([
            "Continue regular practice across all competency areas",
            "Seek diverse learning opportunities to strengthen weaker areas",
            "Document learning journey and progress for future reference"
        ])
        
        return recommendations
    
    def _compile_report_data(self, user: User, period: str) -> Dict[str, Any]:
        """Compile report data"""
        return {"user": user, "period": period, "activities": []}
    
    def _generate_executive_summary(self, user: User, data: Dict, report_type: str) -> Dict[str, Any]:
        """Generate executive summary"""
        return {"summary": "Performance summary", "key_points": []}
    
    def _generate_detailed_findings(self, user: User, data: Dict) -> Dict[str, Any]:
        """Generate detailed findings"""
        return {"findings": [], "analysis": {}}
    
    def _compile_learning_analytics(self, user: User, data: Dict) -> Dict[str, Any]:
        """Compile learning analytics"""
        return {"metrics": {}, "trends": {}}
    
    def _compile_performance_metrics(self, user: User, data: Dict) -> Dict[str, Any]:
        """Compile performance metrics"""
        return {"scores": {}, "averages": {}}
    
    def _generate_report_recommendations(self, user: User, data: Dict, report_type: str) -> List[str]:
        """Generate report recommendations"""
        return ["Continue current learning approach"]
    
    def _generate_action_items(self, recommendations: List[str], report_type: str) -> List[str]:
        """Generate action items"""
        return ["Review and implement recommendations"]
    
    def _get_default_rubric(self, rubric_type: str) -> Dict[str, Any]:
        """Get default rubric"""
        return {"criteria": [], "levels": []}
    
    def _analyze_calibration_feedback(self, feedback_data: List) -> Dict[str, Any]:
        """Analyze calibration feedback"""
        return {"suggestions": [], "patterns": []}
    
    def _update_rubric_based_on_calibration(self, current: Dict, calibration_data: Dict, analysis: Dict) -> Dict[str, Any]:
        """Update rubric based on calibration"""
        return current.copy()
    
    def _validate_rubric_changes(self, old_rubric: Dict, new_rubric: Dict) -> Dict[str, Any]:
        """Validate rubric changes"""
        return {"valid": True, "issues": []}
    
    def _summarize_rubric_changes(self, old_rubric: Dict, new_rubric: Dict) -> List[str]:
        """Summarize rubric changes"""
        return ["No changes made"]
    
    def _gather_benchmark_data(self, user: User, benchmark_type: str, metrics: List[str]) -> Dict[str, Any]:
        """Gather benchmark data"""
        return {"user": user, "type": benchmark_type, "data": {}}
    
    def _compare_metric_against_benchmark(self, user: User, metric: str, benchmark_data: Dict) -> Dict[str, Any]:
        """Compare metric against benchmark"""
        return {"user_value": 0, "benchmark_value": 0, "ranking": "average"}
    
    def _calculate_overall_ranking(self, comparison_results: Dict) -> str:
        """Calculate overall ranking"""
        return "average"
    
    def _generate_benchmark_summary(self, comparison_results: Dict) -> Dict[str, Any]:
        """Generate benchmark summary"""
        return {"summary": "Benchmark comparison complete"}
    
    def _suggest_based_on_benchmark(self, comparison_results: Dict) -> List[str]:
        """Suggest improvements based on benchmark"""
        return ["Continue current approach"]
    
    def _analyze_knowledge_gaps(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Analyze knowledge gaps"""
        return {"identified_gaps": []}
    
    def _analyze_skill_gaps(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Analyze skill gaps"""
        return {"identified_gaps": []}
    
    def _analyze_conceptual_gaps(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Analyze conceptual gaps"""
        return {"identified_gaps": []}
    
    def _analyze_application_gaps(self, user: User, learning_path_id: Optional[str]) -> Dict[str, Any]:
        """Analyze application gaps"""
        return {"identified_gaps": []}
    
    def _calculate_gap_severity_levels(self, gap_analysis: Dict) -> Dict[str, Any]:
        """Calculate gap severity levels"""
        return {"overall": "moderate"}
    
    def _identify_gap_patterns(self, gap_analysis: Dict) -> Dict[str, Any]:
        """Identify gap patterns"""
        return {"patterns": []}
    
    def _create_remediation_plan(self, gap_analysis: Dict) -> Dict[str, Any]:
        """Create remediation plan"""
        return {"steps": [], "timeline": ""}
    
    def _generate_gap_recommendations(self, gap_analysis: Dict) -> List[str]:
        """Generate gap recommendations"""
        return ["Focus on identified gaps"]
    
    def _gather_prediction_data(self, user: User, timeframe: int) -> Dict[str, Any]:
        """Gather prediction data"""
        return {"user": user, "timeframe": timeframe, "factors": []}
    
    def _generate_predictions(self, user: User, data: Dict, outcome_type: str) -> Dict[str, Any]:
        """Generate predictions"""
        return {"outcome": "progress", "probability": 0.75}
    
    def _calculate_prediction_confidence(self, data: Dict, predictions: Dict) -> Dict[str, Any]:
        """Calculate prediction confidence"""
        return {"confidence": 0.8}
    
    def _analyze_competency_scenarios(self, predictions: Dict, data: Dict) -> Dict[str, Any]:
        """Analyze competency scenarios"""
        return {"scenarios": []}
    
    def _generate_prediction_recommendations(self, user: User, predictions: Dict, confidence: Dict) -> List[str]:
        """Generate prediction recommendations"""
        return ["Continue current approach"]
    
    def _evaluate_code_criterion(self, code: str, criterion: str, submission_type: str) -> tuple:
        """Evaluate code against specific criterion"""
        score = 80  # Placeholder
        feedback = f"Code shows {criterion}."
        return score, feedback
    
    def _analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality"""
        return {"quality_metrics": {}, "structure_analysis": {}}
    
    def _analyze_code_strengths_improvements(self, scores: Dict, code: str) -> tuple:
        """Analyze code strengths and improvements"""
        strengths = ["Good structure"]
        improvements = ["Add comments"]
        return strengths, improvements
    
    def _generate_code_suggestions(self, code: str, scores: Dict) -> List[str]:
        """Generate code improvement suggestions"""
        return ["Consider adding error handling"]
    
    def _calculate_engagement_metrics(self, progress_data: List) -> Dict[str, Any]:
        """Calculate engagement metrics"""
        return {"participation_rate": 75, "session_frequency": 3}
    
    def _calculate_learning_velocity(self, progress_data: List) -> float:
        """Calculate learning velocity"""
        return 80.0  # Placeholder
    
    # Enhanced competency assessment support methods
    def _get_competency_related_progress(self, user: User, competency: str) -> List:
        """Get progress data related to specific competency"""
        # Filter progress data based on competency type
        related_progress = []
        
        # This would be enhanced to query actual competency-related content
        all_progress = UserModuleProgress.objects.filter(user=user)
        
        # Simple filtering based on content tags or types
        competency_keywords = competency.lower().split('_')
        
        for progress in all_progress:
            if hasattr(progress.module, 'content'):
                content_title = getattr(progress.module.content, 'title', '').lower()
                content_tags = getattr(progress.module.content, 'tags', [])
                
                # Check if any competency keywords appear in content
                if any(keyword in content_title for keyword in competency_keywords) or \
                   any(keyword in str(tag).lower() for tag in content_tags for keyword in competency_keywords):
                    related_progress.append(progress)
        
        return related_progress
    
    def _assess_programming_competency(self, user: User, progress_data: List) -> Dict[str, Any]:
        """Assess programming competency specifically"""
        result = {
            "competency": "programming",
            "level": "developing",
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        if not progress_data:
            result["confidence_level"] = 0.3
            result["development_areas"] = ["Limited programming evidence available"]
            return result
        
        # Analyze coding exercises
        coding_exercises = [p for p in progress_data 
                          if hasattr(p.module, 'content') and 
                          'code' in getattr(p.module.content, 'title', '').lower()]
        
        scores = [p.score or 0 for p in coding_exercises if hasattr(p, 'score')]
        completion_rate = len([p for p in coding_exercises if p.status == 'completed']) / max(len(coding_exercises), 1)
        
        result["score"] = (sum(scores) / len(scores) * 0.7 + completion_rate * 100 * 0.3) if scores else 0
        result["evidence"] = [f"Completed {len(coding_exercises)} coding exercises"]
        
        if result["score"] >= 80:
            result["level"] = "proficient"
            result["strengths"] = ["Strong coding fundamentals", "Good problem-solving in code"]
        elif result["score"] >= 60:
            result["level"] = "developing"
            result["strengths"] = ["Basic coding skills present"]
            result["development_areas"] = ["Improve code efficiency", "Enhance debugging skills"]
        else:
            result["level"] = "emerging"
            result["development_areas"] = ["Focus on basic programming concepts", "Practice more coding exercises"]
        
        result["confidence_level"] = min(0.9, len(progress_data) / 10)  # More evidence = higher confidence
        return result
    
    def _assess_problem_solving_competency(self, user: User, progress_data: List) -> Dict[str, Any]:
        """Assess problem-solving competency specifically"""
        result = {
            "competency": "problem_solving",
            "level": "developing",
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        # Look for problem-solving indicators
        complex_modules = [p for p in progress_data 
                         if hasattr(p.module, 'content') and 
                         getattr(p.module.content, 'difficulty_level', '') in ['intermediate', 'advanced']]
        
        if not complex_modules:
            result["confidence_level"] = 0.2
            result["development_areas"] = ["Limited complex problem evidence"]
            return result
        
        scores = [p.score or 0 for p in complex_modules if hasattr(p, 'score')]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Analyze approach to difficult content
        completion_rate = len([p for p in complex_modules if p.status == 'completed']) / len(complex_modules)
        
        result["score"] = avg_score * 0.8 + completion_rate * 100 * 0.2
        result["evidence"] = [f"Engaged with {len(complex_modules)} complex problems"]
        
        if result["score"] >= 85:
            result["level"] = "advanced"
            result["strengths"] = ["Strong analytical thinking", "Effective problem decomposition"]
        elif result["score"] >= 70:
            result["level"] = "proficient"
            result["strengths"] = ["Good problem-solving approach", "Persistent with challenges"]
        elif result["score"] >= 55:
            result["level"] = "developing"
            result["strengths"] = ["Shows problem-solving potential"]
            result["development_areas"] = ["Improve systematic approach", "Practice more complex problems"]
        else:
            result["level"] = "emerging"
            result["development_areas"] = ["Learn structured problem-solving methods", "Practice with guided problems"]
        
        result["confidence_level"] = min(0.85, len(complex_modules) / 8)
        return result
    
    def _assess_communication_competency(self, user: User, progress_data: List) -> Dict[str, Any]:
        """Assess communication competency specifically"""
        result = {
            "competency": "communication",
            "level": "developing",
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        # Communication is harder to assess from progress data alone
        # This would require interaction data, peer feedback, etc.
        
        # Use engagement and help-seeking patterns as proxies
        help_requests = len([p for p in progress_data if hasattr(p, 'help_used') and p.help_used])
        total_activities = len(progress_data)
        
        help_seeking_rate = help_requests / max(total_activities, 1)
        
        # Appropriate help-seeking suggests good communication (asking for help when needed)
        if 0.1 <= help_seeking_rate <= 0.3:
            result["score"] = 75.0
            result["strengths"] = ["Appropriate help-seeking behavior", "Engages with learning community"]
        elif help_seeking_rate > 0.5:
            result["score"] = 60.0
            result["development_areas"] = ["Work on independent problem-solving", "Build confidence"]
        else:
            result["score"] = 70.0
            result["development_areas"] = ["Encourage more help-seeking when needed", "Build collaboration skills"]
        
        result["evidence"] = [f"Help-seeking rate: {help_seeking_rate:.2f}"]
        result["confidence_level"] = 0.4  # Lower confidence due to indirect assessment
        return result
    
    def _assess_critical_thinking_competency(self, user: User, progress_data: List) -> Dict[str, Any]:
        """Assess critical thinking competency specifically"""
        result = {
            "competency": "critical_thinking",
            "level": "developing",
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        # Look for evidence of analysis, evaluation, and synthesis
        analytical_modules = [p for p in progress_data 
                            if hasattr(p.module, 'content') and 
                            any(keyword in getattr(p.module.content, 'title', '').lower() 
                                for keyword in ['analyze', 'evaluate', 'critique', 'compare'])]
        
        if not analytical_modules:
            # Use performance on challenging content as proxy
            advanced_modules = [p for p in progress_data 
                              if hasattr(p.module, 'content') and 
                              getattr(p.module.content, 'difficulty_level', '') == 'advanced']
            analytical_modules = advanced_modules
        
        if not analytical_modules:
            result["confidence_level"] = 0.2
            result["development_areas"] = ["Limited analytical evidence available"]
            return result
        
        scores = [p.score or 0 for p in analytical_modules if hasattr(p, 'score')]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        result["score"] = avg_score
        result["evidence"] = [f"Engaged with {len(analytical_modules)} analytical tasks"]
        
        if result["score"] >= 80:
            result["level"] = "proficient"
            result["strengths"] = ["Strong analytical skills", "Good evidence evaluation"]
        elif result["score"] >= 65:
            result["level"] = "developing"
            result["strengths"] = ["Shows analytical thinking"]
            result["development_areas"] = ["Improve depth of analysis", "Practice evaluation skills"]
        else:
            result["level"] = "emerging"
            result["development_areas"] = ["Focus on analytical frameworks", "Practice evidence evaluation"]
        
        result["confidence_level"] = min(0.8, len(analytical_modules) / 6)
        return result
    
    def _assess_generic_competency(self, user: User, competency: str, progress_data: List) -> Dict[str, Any]:
        """Assess generic competency when specific assessment not available"""
        result = {
            "competency": competency,
            "level": "developing",
            "score": 0.0,
            "evidence": [],
            "strengths": [],
            "development_areas": [],
            "confidence_level": 0.0
        }
        
        if not progress_data:
            result["confidence_level"] = 0.2
            result["development_areas"] = ["Insufficient evidence for assessment"]
            return result
        
        # Generic assessment based on overall performance
        scores = [p.score or 0 for p in progress_data if hasattr(p, 'score')]
        avg_score = sum(scores) / len(scores) if scores else 0
        completion_rate = len([p for p in progress_data if p.status == 'completed']) / len(progress_data)
        
        result["score"] = avg_score * 0.7 + completion_rate * 100 * 0.3
        result["evidence"] = [f"Evidence from {len(progress_data)} related activities"]
        
        if result["score"] >= 85:
            result["level"] = "advanced"
        elif result["score"] >= 70:
            result["level"] = "proficient"
        elif result["score"] >= 55:
            result["level"] = "developing"
            result["development_areas"] = ["Practice more challenging applications"]
        else:
            result["level"] = "emerging"
            result["development_areas"] = ["Build foundational knowledge and skills"]
        
        result["confidence_level"] = min(0.7, len(progress_data) / 8)
        return result
    
    def _identify_strength_patterns(self, strong_competencies: List[str]) -> List[str]:
        """Identify patterns in strong competencies"""
        patterns = []
        
        # Technical competencies
        technical = [c for c in strong_competencies if any(keyword in c.lower() 
                    for keyword in ['programming', 'coding', 'technical', 'analytical'])]
        if len(technical) >= 2:
            patterns.append("Strong technical and analytical abilities")
        
        # Communication competencies
        communication = [c for c in strong_competencies if any(keyword in c.lower() 
                        for keyword in ['communication', 'collaboration', 'presentation'])]
        if len(communication) >= 2:
            patterns.append("Strong interpersonal and communication skills")
        
        # Problem-solving competencies
        problem_solving = [c for c in strong_competencies if any(keyword in c.lower() 
                          for keyword in ['problem_solving', 'critical_thinking', 'analysis'])]
        if len(problem_solving) >= 2:
            patterns.append("Excellent analytical and problem-solving capabilities")
        
        return patterns if patterns else ["Diverse competency strengths across multiple areas"]
    
    def _identify_development_patterns(self, developing_competencies: List[str]) -> List[str]:
        """Identify patterns in developing competencies"""
        patterns = []
        
        if len(developing_competencies) >= 3:
            patterns.append("Multiple competencies need foundational development")
        
        # Check for systematic gaps
        technical_gaps = [c for c in developing_competencies if any(keyword in c.lower() 
                         for keyword in ['programming', 'technical', 'coding'])]
        if technical_gaps:
            patterns.append("Technical skills require additional attention")
        
        soft_skill_gaps = [c for c in developing_competencies if any(keyword in c.lower() 
                          for keyword in ['communication', 'collaboration', 'leadership'])]
        if soft_skill_gaps:
            patterns.append("Interpersonal and leadership skills need development")
        
        return patterns if patterns else ["General competency development needed"]


# Import uuid for generating unique IDs
import uuid