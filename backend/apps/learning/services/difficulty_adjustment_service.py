# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Difficulty Adjustment Service

Provides real-time difficulty adjustment based on user performance analytics
and learning patterns for optimal challenge progression.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q, F
from collections import defaultdict

from ..models import (
    UserDifficultyProfile, UserChallengeAttempt, UserModuleProgress, 
    AdaptiveChallenge, SpacedRepetitionSession
)

User = get_user_model()


class DifficultyAdjustmentService:
    """
    Service for dynamically adjusting user difficulty levels based on performance analytics.
    """
    
    def __init__(self):
        pass
        
    def analyze_user_performance(self, user_id: str, time_window_days: int = 30) -> Dict[str, Any]:
        """
        Comprehensive performance analysis for difficulty adjustment.
        """
        try:
            user = User.objects.get(id=user_id)
            
            # Get performance data
            performance_data = self._get_performance_data(user, time_window_days)
            
            # Calculate difficulty metrics
            difficulty_metrics = self._calculate_difficulty_metrics(performance_data)
            
            # Analyze learning patterns
            learning_patterns = self._analyze_learning_patterns(user, time_window_days)
            
            # Generate recommendations
            recommendations = self._generate_difficulty_recommendations(
                difficulty_metrics, learning_patterns, user
            )
            
            return {
                'success': True,
                'user_id': str(user.id),
                'analysis_period': f'{time_window_days} days',
                'performance_data': performance_data,
                'difficulty_metrics': difficulty_metrics,
                'learning_patterns': learning_patterns,
                'recommendations': recommendations,
                'generated_at': timezone.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_performance_data(self, user: User, time_window_days: int) -> Dict[str, Any]:
        """
        Get comprehensive performance data for a user.
        """
        cutoff_date = timezone.now() - timedelta(days=time_window_days)
        
        # Get challenge attempts
        challenge_attempts = UserChallengeAttempt.objects.filter(
            user=user,
            started_at__gte=cutoff_date
        ).select_related('challenge')
        
        # Get module progress
        module_progress = UserModuleProgress.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        ).select_related('module')
        
        # Get spaced repetition sessions
        repetition_sessions = SpacedRepetitionSession.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        ).select_related('challenge')
        
        # Aggregate challenge performance
        challenge_performance = []
        for attempt in challenge_attempts:
            challenge_performance.append({
                'attempt_id': str(attempt.id),
                'challenge_type': attempt.challenge.challenge_type,
                'difficulty_level': attempt.challenge.difficulty_level,
                'score': attempt.score or 0,
                'time_spent': attempt.time_spent,
                'date': attempt.started_at.date(),
                'status': attempt.status
            })
        
        # Aggregate module performance
        module_performance = []
        for progress in module_progress:
            module_performance.append({
                'module_id': str(progress.module.id),
                'module_title': progress.module.title,
                'difficulty_rating': progress.module.difficulty_rating,
                'status': progress.status,
                'progress_percentage': progress.progress_percentage,
                'quiz_score': progress.quiz_score,
                'coding_score': progress.coding_score,
                'overall_score': progress.overall_score,
                'time_spent': progress.time_spent.total_seconds() / 60 if progress.time_spent else 0,
                'date': progress.created_at.date()
            })
        
        # Aggregate spaced repetition performance
        repetition_performance = []
        for session in repetition_sessions:
            repetition_performance.append({
                'session_id': str(session.id),
                'challenge_id': str(session.challenge.id),
                'challenge_title': session.challenge.title,
                'review_stage': session.review_stage,
                'quality_rating': session.quality_rating,
                'ease_factor': session.ease_factor,
                'completion_rate': 1.0 if session.completed_at else 0.0,
                'date': session.created_at.date()
            })
        
        return {
            'challenge_attempts': challenge_performance,
            'module_progress': module_performance,
            'repetition_sessions': repetition_performance,
            'total_challenges': len(challenge_performance),
            'total_modules': len(module_performance),
            'total_reviews': len(repetition_performance),
            'date_range': {
                'start': cutoff_date.date().isoformat(),
                'end': timezone.now().date().isoformat()
            }
        }
    
    def _calculate_difficulty_metrics(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate key metrics for difficulty adjustment decisions.
        """
        challenge_attempts = performance_data['challenge_attempts']
        module_progress = performance_data['module_progress']
        repetition_sessions = performance_data['repetition_sessions']
        
        # Challenge success metrics
        challenge_success_rate = self._calculate_success_rate(challenge_attempts)
        avg_challenge_score = self._calculate_average_score(challenge_attempts)
        
        # Module completion metrics
        module_completion_rate = self._calculate_module_completion_rate(module_progress)
        avg_module_score = self._calculate_average_module_score(module_progress)
        
        # Time-based metrics
        avg_completion_time = self._calculate_average_completion_time(challenge_attempts)
        learning_velocity = self._calculate_learning_velocity(performance_data)
        
        # Consistency metrics
        performance_consistency = self._calculate_performance_consistency(challenge_attempts)
        engagement_level = self._calculate_engagement_level(performance_data)
        
        # Spaced repetition metrics
        repetition_success_rate = self._calculate_repetition_success_rate(repetition_sessions)
        retention_rate = self._calculate_retention_rate(repetition_sessions)
        
        # Trend analysis
        performance_trend = self._analyze_performance_trend(challenge_attempts)
        
        return {
            'challenge_success_rate': challenge_success_rate,
            'average_challenge_score': avg_challenge_score,
            'module_completion_rate': module_completion_rate,
            'average_module_score': avg_module_score,
            'average_completion_time': avg_completion_time,
            'learning_velocity': learning_velocity,
            'performance_consistency': performance_consistency,
            'engagement_level': engagement_level,
            'repetition_success_rate': repetition_success_rate,
            'retention_rate': retention_rate,
            'performance_trend': performance_trend,
            'difficulty_recommendation': self._determine_difficulty_recommendation({
                'success_rate': challenge_success_rate,
                'avg_score': avg_challenge_score,
                'completion_rate': module_completion_rate,
                'consistency': performance_consistency,
                'trend': performance_trend
            })
        }
    
    def _calculate_success_rate(self, attempts: List[Dict[str, Any]]) -> float:
        """Calculate success rate from challenge attempts."""
        if not attempts:
            return 0.0
        
        successful_attempts = sum(1 for attempt in attempts if attempt['score'] >= 0.6)
        return successful_attempts / len(attempts)
    
    def _calculate_average_score(self, attempts: List[Dict[str, Any]]) -> float:
        """Calculate average score from attempts."""
        if not attempts:
            return 0.0
        
        valid_scores = [attempt['score'] for attempt in attempts if attempt['score'] is not None]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
    
    def _calculate_module_completion_rate(self, progress: List[Dict[str, Any]]) -> float:
        """Calculate module completion rate."""
        if not progress:
            return 0.0
        
        completed_modules = sum(1 for p in progress if p['status'] == 'completed')
        return completed_modules / len(progress)
    
    def _calculate_average_module_score(self, progress: List[Dict[str, Any]]) -> float:
        """Calculate average score from module progress."""
        if not progress:
            return 0.0
        
        valid_scores = [p['overall_score'] for p in progress if p['overall_score'] is not None]
        return sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
    
    def _calculate_average_completion_time(self, attempts: List[Dict[str, Any]]) -> float:
        """Calculate average completion time in minutes."""
        if not attempts:
            return 0.0
        
        valid_times = [attempt['time_spent'] for attempt in attempts if attempt['time_spent'] > 0]
        return sum(valid_times) / len(valid_times) if valid_times else 0.0
    
    def _calculate_learning_velocity(self, performance_data: Dict[str, Any]) -> float:
        """Calculate how quickly user is progressing through content."""
        total_activities = (
            len(performance_data['challenge_attempts']) +
            len(performance_data['module_progress']) +
            len(performance_data['repetition_sessions'])
        )
        
        time_window = 30  # days
        return total_activities / time_window
    
    def _calculate_performance_consistency(self, attempts: List[Dict[str, Any]]) -> float:
        """Calculate consistency of performance over time."""
        if len(attempts) < 3:
            return 0.5  # Neutral score for insufficient data
        
        # Calculate coefficient of variation for scores
        scores = [attempt['score'] for attempt in attempts if attempt['score'] is not None]
        if len(scores) < 3:
            return 0.5
        
        mean_score = np.mean(scores)
        std_score = np.std(scores)
        
        if mean_score == 0:
            return 0.5
        
        # Convert to consistency score (lower variation = higher consistency)
        cv = std_score / mean_score
        consistency_score = max(0, 1 - cv)
        
        return consistency_score
    
    def _calculate_engagement_level(self, performance_data: Dict[str, Any]) -> float:
        """Calculate user engagement level based on activity frequency."""
        # Factors that indicate engagement
        factors = {
            'recent_activity': 0,  # Activity in last 7 days
            'session_frequency': 0,  # Regular learning sessions
            'challenge_variety': 0,  # Trying different challenge types
            'review_completion': 0  # Completing spaced repetition reviews
        }
        
        cutoff_7_days = timezone.now() - timedelta(days=7)
        
        # Recent activity
        recent_challenges = sum(1 for attempt in performance_data['challenge_attempts'] 
                              if attempt['date'] >= cutoff_7_days.date())
        recent_modules = sum(1 for progress in performance_data['module_progress'] 
                           if progress['date'] >= cutoff_7_days.date())
        factors['recent_activity'] = min(1.0, (recent_challenges + recent_modules) / 10)
        
        # Session frequency (assumes regular sessions indicate engagement)
        total_sessions = performance_data['total_challenges'] + performance_data['total_modules']
        factors['session_frequency'] = min(1.0, total_sessions / 20)
        
        # Challenge variety
        challenge_types = set(attempt['challenge_type'] for attempt in performance_data['challenge_attempts'])
        factors['challenge_variety'] = min(1.0, len(challenge_types) / 3)
        
        # Review completion
        completed_reviews = sum(1 for session in performance_data['repetition_sessions'] 
                              if session['completion_rate'] == 1.0)
        total_reviews = performance_data['total_reviews']
        factors['review_completion'] = completed_reviews / total_reviews if total_reviews > 0 else 0
        
        # Weighted average
        weights = {'recent_activity': 0.4, 'session_frequency': 0.3, 'challenge_variety': 0.2, 'review_completion': 0.1}
        engagement_score = sum(factors[factor] * weights[factor] for factor in factors)
        
        return engagement_score
    
    def _calculate_repetition_success_rate(self, sessions: List[Dict[str, Any]]) -> float:
        """Calculate success rate for spaced repetition sessions."""
        if not sessions:
            return 0.0
        
        successful_sessions = sum(1 for session in sessions 
                                if session['completion_rate'] == 1.0 and session['quality_rating'] >= 3)
        return successful_sessions / len(sessions)
    
    def _calculate_retention_rate(self, sessions: List[Dict[str, Any]]) -> float:
        """Calculate retention rate from spaced repetition data."""
        if not sessions:
            return 0.0
        
        # Higher review stages indicate better retention
        total_stages = sum(session['review_stage'] for session in sessions)
        max_possible_stages = len(sessions) * 10  # Assuming max stage of 10
        
        return total_stages / max_possible_stages if max_possible_stages > 0 else 0.0
    
    def _analyze_performance_trend(self, attempts: List[Dict[str, Any]]) -> str:
        """Analyze whether performance is improving, declining, or stable."""
        if len(attempts) < 5:
            return 'insufficient_data'
        
        # Sort attempts by date
        sorted_attempts = sorted(attempts, key=lambda x: x['date'])
        
        # Calculate trend using linear regression
        scores = [attempt['score'] for attempt in sorted_attempts if attempt['score'] is not None]
        if len(scores) < 3:
            return 'insufficient_data'
        
        # Simple trend analysis
        early_scores = scores[:len(scores)//2]
        late_scores = scores[len(scores)//2:]
        
        early_avg = sum(early_scores) / len(early_scores)
        late_avg = sum(late_scores) / len(late_scores)
        
        difference = late_avg - early_avg
        
        if difference > 0.1:
            return 'improving'
        elif difference < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _analyze_learning_patterns(self, user: User, time_window_days: int) -> Dict[str, Any]:
        """
        Analyze user learning patterns for personalized difficulty adjustment.
        """
        cutoff_date = timezone.now() - timedelta(days=time_window_days)
        
        # Learning pace patterns
        attempts = UserChallengeAttempt.objects.filter(
            user=user,
            started_at__gte=cutoff_date
        ).order_by('started_at')
        
        # Time between attempts (engagement frequency)
        attempt_intervals = []
        previous_date = None
        for attempt in attempts:
            if previous_date:
                interval = (attempt.started_at - previous_date).total_seconds() / 3600  # hours
                attempt_intervals.append(interval)
            previous_date = attempt.started_at
        
        # Difficulty progression patterns
        difficulty_levels = [attempt.challenge.difficulty_level for attempt in attempts]
        difficulty_progression = self._analyze_difficulty_progression(difficulty_levels)
        
        # Success patterns by challenge type
        success_by_type = self._analyze_success_by_challenge_type(attempts)
        
        # Time management patterns
        time_patterns = self._analyze_time_patterns(attempts)
        
        return {
            'learning_frequency': {
                'average_interval_hours': np.mean(attempt_intervals) if attempt_intervals else 24,
                'consistency_score': 1.0 - (np.std(attempt_intervals) / np.mean(attempt_intervals)) if attempt_intervals and np.mean(attempt_intervals) > 0 else 0.5
            },
            'difficulty_progression': difficulty_progression,
            'success_by_challenge_type': success_by_type,
            'time_management': time_patterns,
            'optimal_challenge_count': self._determine_optimal_challenge_count(attempts)
        }
    
    def _analyze_difficulty_progression(self, difficulty_levels: List[str]) -> Dict[str, Any]:
        """Analyze how user progresses through difficulty levels."""
        if not difficulty_levels:
            return {'pattern': 'no_data'}
        
        # Count occurrences of each difficulty
        difficulty_counts = defaultdict(int)
        for level in difficulty_levels:
            difficulty_counts[level] += 1
        
        # Determine pattern
        unique_difficulties = list(set(difficulty_levels))
        if len(unique_difficulties) == 1:
            pattern = 'consistent'
        elif len(unique_difficulties) <= 2:
            pattern = 'gradual'
        else:
            pattern = 'varied'
        
        return {
            'pattern': pattern,
            'difficulty_distribution': dict(difficulty_counts),
            'preferred_difficulty': max(difficulty_counts.items(), key=lambda x: x[1])[0] if difficulty_counts else 'beginner'
        }
    
    def _analyze_success_by_challenge_type(self, attempts) -> Dict[str, Any]:
        """Analyze success rates by challenge type."""
        success_by_type = defaultdict(lambda: {'total': 0, 'successful': 0})
        
        for attempt in attempts:
            challenge_type = attempt.challenge.challenge_type
            success_by_type[challenge_type]['total'] += 1
            
            if attempt.score and attempt.score >= 0.6:
                success_by_type[challenge_type]['successful'] += 1
        
        # Calculate success rates
        success_rates = {}
        for challenge_type, stats in success_by_type.items():
            success_rates[challenge_type] = stats['successful'] / stats['total']
        
        return success_rates
    
    def _analyze_time_patterns(self, attempts) -> Dict[str, Any]:
        """Analyze time management patterns."""
        completion_times = [attempt.time_spent for attempt in attempts if attempt.time_spent > 0]
        
        if not completion_times:
            return {'pattern': 'no_data'}
        
        return {
            'average_time': np.mean(completion_times),
            'time_variability': np.std(completion_times) / np.mean(completion_times) if np.mean(completion_times) > 0 else 0,
            'time_consistency': 1.0 - (np.std(completion_times) / np.mean(completion_times)) if np.mean(completion_times) > 0 else 0.5
        }
    
    def _determine_optimal_challenge_count(self, attempts) -> Dict[str, Any]:
        """Determine optimal number of challenges for this user."""
        # Analyze performance vs challenge frequency
        user_attempts = list(attempts)
        
        if len(user_attempts) < 5:
            return {'recommended_daily': 1, 'reasoning': 'building habit'}
        
        # Calculate performance over time periods
        performance_by_day = defaultdict(list)
        for attempt in user_attempts:
            day = attempt.started_at.date()
            if attempt.score is not None:
                performance_by_day[day].append(attempt.score)
        
        # Find optimal frequency
        daily_performance = {}
        for day, scores in performance_by_day.items():
            if len(scores) >= 2:  # At least 2 challenges per day
                daily_performance[day] = np.mean(scores)
        
        if not daily_performance:
            return {'recommended_daily': 1, 'reasoning': 'insufficient data'}
        
        # Determine if more or fewer challenges per day improves performance
        avg_performance = np.mean(list(daily_performance.values()))
        
        if avg_performance > 0.8:
            return {'recommended_daily': 3, 'reasoning': 'high performance indicates readiness for more challenges'}
        elif avg_performance > 0.6:
            return {'recommended_daily': 2, 'reasoning': 'good performance with current frequency'}
        else:
            return {'recommended_daily': 1, 'reasoning': 'focus on quality over quantity'}
    
    def _generate_difficulty_recommendations(self, difficulty_metrics: Dict[str, Any], 
                                           learning_patterns: Dict[str, Any], 
                                           user: User) -> Dict[str, Any]:
        """
        Generate specific difficulty adjustment recommendations.
        """
        recommendations = []
        adjustments = []
        
        # Success rate based recommendations
        success_rate = difficulty_metrics['challenge_success_rate']
        if success_rate >= 0.8 and difficulty_metrics['performance_consistency'] >= 0.7:
            recommendations.append({
                'type': 'increase_difficulty',
                'reason': 'High success rate and consistent performance',
                'confidence': 0.9,
                'priority': 'high'
            })
            adjustments.append({
                'difficulty': 'increase',
                'new_level': self._calculate_next_difficulty(user.difficulty_profile.current_difficulty, 'increase'),
                'rationale': 'User demonstrates mastery at current level'
            })
        elif success_rate < 0.4 or difficulty_metrics['performance_trend'] == 'declining':
            recommendations.append({
                'type': 'decrease_difficulty',
                'reason': 'Low success rate or declining performance trend',
                'confidence': 0.8,
                'priority': 'high'
            })
            adjustments.append({
                'difficulty': 'decrease',
                'new_level': self._calculate_next_difficulty(user.difficulty_profile.current_difficulty, 'decrease'),
                'rationale': 'User needs reinforcement at current level'
            })
        
        # Engagement based recommendations
        engagement = difficulty_metrics['engagement_level']
        if engagement < 0.3:
            recommendations.append({
                'type': 'reduce_challenge_count',
                'reason': 'Low engagement suggests overwhelming challenge load',
                'confidence': 0.7,
                'priority': 'medium'
            })
        elif engagement > 0.8:
            recommendations.append({
                'type': 'increase_challenge_count',
                'reason': 'High engagement indicates readiness for more challenges',
                'confidence': 0.6,
                'priority': 'low'
            })
        
        # Learning velocity recommendations
        velocity = difficulty_metrics['learning_velocity']
        if velocity > 2.0:  # More than 2 activities per day on average
            recommendations.append({
                'type': 'maintain_or_increase_difficulty',
                'reason': 'High learning velocity suggests user can handle more challenge',
                'confidence': 0.6,
                'priority': 'medium'
            })
        elif velocity < 0.5:  # Less than 0.5 activities per day
            recommendations.append({
                'type': 'suggest_motivation_strategies',
                'reason': 'Low learning velocity may indicate motivation issues',
                'confidence': 0.7,
                'priority': 'medium'
            })
        
        # Spaced repetition based recommendations
        retention_rate = difficulty_metrics['retention_rate']
        if retention_rate < 0.3:
            recommendations.append({
                'type': 'increase_review_frequency',
                'reason': 'Low retention rate suggests need for more spaced repetition',
                'confidence': 0.8,
                'priority': 'high'
            })
        
        return {
            'recommendations': recommendations,
            'proposed_adjustments': adjustments,
            'confidence_score': self._calculate_overall_confidence(difficulty_metrics, learning_patterns),
            'implementation_priority': self._prioritize_adjustments(recommendations)
        }
    
    def _calculate_next_difficulty(self, current_difficulty: str, direction: str) -> str:
        """Calculate next difficulty level in given direction."""
        difficulty_order = ['very_beginner', 'beginner', 'intermediate', 'advanced', 'expert']
        current_index = difficulty_order.index(current_difficulty)
        
        if direction == 'increase':
            next_index = min(current_index + 1, len(difficulty_order) - 1)
        else:  # decrease
            next_index = max(current_index - 1, 0)
        
        return difficulty_order[next_index]
    
    def _calculate_overall_confidence(self, difficulty_metrics: Dict[str, Any], 
                                    learning_patterns: Dict[str, Any]) -> float:
        """Calculate overall confidence in difficulty recommendations."""
        confidence_factors = []
        
        # Data sufficiency
        if difficulty_metrics['challenge_success_rate'] > 0:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.3)
        
        # Consistency
        confidence_factors.append(difficulty_metrics['performance_consistency'])
        
        # Engagement
        confidence_factors.append(difficulty_metrics['engagement_level'])
        
        # Learning velocity
        if 0.5 <= difficulty_metrics['learning_velocity'] <= 3.0:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.4)
        
        return np.mean(confidence_factors)
    
    def _prioritize_adjustments(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize difficulty adjustments by priority and confidence."""
        priority_weights = {'high': 3, 'medium': 2, 'low': 1}
        
        # Sort by priority weight and confidence
        sorted_recommendations = sorted(
            recommendations,
            key=lambda x: (priority_weights.get(x['priority'], 1), x['confidence']),
            reverse=True
        )
        
        return sorted_recommendations[:3]  # Return top 3 recommendations
    
    def apply_difficulty_adjustment(self, user_id: str, adjustment_type: str) -> Dict[str, Any]:
        """
        Apply difficulty adjustment based on analysis and recommendations.
        """
        try:
            user = User.objects.get(id=user_id)
            difficulty_profile = user.difficulty_profile
            
            if adjustment_type == 'increase':
                old_difficulty = difficulty_profile.current_difficulty
                difficulty_profile._increase_difficulty()
                new_difficulty = difficulty_profile.current_difficulty
                
                adjustment_made = old_difficulty != new_difficulty
                
            elif adjustment_type == 'decrease':
                old_difficulty = difficulty_profile.current_difficulty
                difficulty_profile._decrease_difficulty()
                new_difficulty = difficulty_profile.current_difficulty
                
                adjustment_made = old_difficulty != new_difficulty
                
            else:
                return {
                    'success': False,
                    'error': 'Invalid adjustment type'
                }
            
            # Update timestamp
            difficulty_profile.last_difficulty_change = timezone.now()
            difficulty_profile.save()
            
            return {
                'success': True,
                'adjustment_applied': adjustment_made,
                'old_difficulty': old_difficulty if adjustment_type in ['increase', 'decrease'] else None,
                'new_difficulty': new_difficulty if adjustment_type in ['increase', 'decrease'] else None,
                'adjustment_date': difficulty_profile.last_difficulty_change.isoformat(),
                'message': f'Difficulty adjusted to {new_difficulty}' if adjustment_made else 'No adjustment needed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_difficulty_history(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's difficulty adjustment history.
        """
        try:
            user = User.objects.get(id=user_id)
            profile = user.difficulty_profile
            
            # Get recent performance to infer history
            recent_attempts = UserChallengeAttempt.objects.filter(
                user=user
            ).order_by('-started_at')[:50].select_related('challenge')
            
            # Analyze difficulty progression
            difficulty_progression = []
            current_difficulty = profile.current_difficulty
            
            # Group attempts by difficulty
            attempts_by_difficulty = defaultdict(list)
            for attempt in recent_attempts:
                attempts_by_difficulty[attempt.challenge.difficulty_level].append(attempt)
            
            # Calculate metrics for each difficulty level
            for difficulty, attempts in attempts_by_difficulty.items():
                if attempts:
                    scores = [a.score for a in attempts if a.score is not None]
                    avg_score = np.mean(scores) if scores else 0
                    success_rate = sum(1 for a in attempts if a.score and a.score >= 0.6) / len(attempts)
                    
                    difficulty_progression.append({
                        'difficulty_level': difficulty,
                        'attempt_count': len(attempts),
                        'average_score': avg_score,
                        'success_rate': success_rate,
                        'is_current': difficulty == current_difficulty
                    })
            
            # Sort by date (most recent first)
            difficulty_progression.sort(key=lambda x: x['is_current'], reverse=True)
            
            return {
                'success': True,
                'current_difficulty': current_difficulty,
                'difficulty_progression': difficulty_progression,
                'total_attempts_analyzed': len(recent_attempts),
                'last_adjustment': profile.last_difficulty_change.isoformat() if profile.last_difficulty_change else None,
                'profile_metrics': {
                    'jac_knowledge_level': profile.jac_knowledge_level,
                    'problem_solving_level': profile.problem_solving_level,
                    'coding_skill_level': profile.coding_skill_level,
                    'recent_accuracy': profile.recent_accuracy,
                    'success_streak': profile.success_streak
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
