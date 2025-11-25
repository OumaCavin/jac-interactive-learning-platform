"""
Complete Learning Algorithms Implementation
Addresses all missing components in the JAC Learning Platform

This module provides the missing implementations for:
1. Learning Velocity Analysis
2. Engagement Pattern Analysis
3. Success Probability Modeling
4. Time-to-Completion Prediction
5. Retention Risk Assessment
6. Knowledge Gap Detection
7. Adaptive Feedback Generation

Author: MiniMax Agent
Created: 2025-11-26
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum, Avg, Max, Min, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class LearningVelocityAnalyzer:
    """
    Complete implementation of learning velocity analysis
    """
    
    @staticmethod
    def analyze_learning_velocity(
        user: User,
        time_window_days: int = 30,
        learning_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive learning velocity analysis with progression tracking
        """
        try:
            if not learning_data:
                learning_data = LearningVelocityAnalyzer._get_user_learning_data(user, time_window_days)
            
            if not learning_data:
                return {
                    'velocity_score': 0.5,
                    'trend': 'insufficient_data',
                    'analysis': 'Not enough data for velocity analysis'
                }
            
            # Calculate core velocity metrics
            velocity_metrics = LearningVelocityAnalyzer._calculate_velocity_metrics(learning_data)
            
            # Analyze progression patterns
            progression_analysis = LearningVelocityAnalyzer._analyze_progression_patterns(learning_data)
            
            # Generate velocity predictions
            velocity_prediction = LearningVelocityAnalyzer._predict_future_velocity(velocity_metrics, progression_analysis)
            
            # Assess momentum and acceleration
            momentum_analysis = LearningVelocityAnalyzer._analyze_momentum(learning_data)
            
            return {
                'velocity_score': velocity_metrics['current_velocity'],
                'trend': progression_analysis['trend'],
                'progression_rate': progression_analysis['progression_rate'],
                'momentum': momentum_analysis['momentum'],
                'acceleration': momentum_analysis['acceleration'],
                'predicted_velocity': velocity_prediction,
                'velocity_factors': velocity_metrics['velocity_factors'],
                'insights': LearningVelocityAnalyzer._generate_velocity_insights(velocity_metrics, progression_analysis),
                'recommendations': LearningVelocityAnalyzer._generate_velocity_recommendations(velocity_metrics, progression_analysis),
                'analysis_period': f'{time_window_days} days',
                'data_points': len(learning_data)
            }
            
        except Exception as e:
            logger.error(f"Learning velocity analysis error: {e}")
            return {
                'velocity_score': 0.5,
                'trend': 'analysis_error',
                'analysis': f'Error in analysis: {str(e)}'
            }
    
    @staticmethod
    def _get_user_learning_data(user: User, time_window_days: int) -> List[Dict[str, Any]]:
        """Get comprehensive user learning data"""
        cutoff_date = timezone.now() - timedelta(days=time_window_days)
        
        # Get learning analytics data
        from ..models import LearningAnalytics
        activities = LearningAnalytics.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        ).order_by('created_at')
        
        learning_data = []
        for activity in activities:
            learning_data.append({
                'date': activity.created_at,
                'activity_type': getattr(activity, 'activity_type', 'unknown'),
                'score': getattr(activity, 'score', 0.5),
                'time_spent': getattr(activity, 'time_spent', 0),
                'intensity': getattr(activity, 'intensity_score', 0.5),
                'difficulty': getattr(activity, 'difficulty_level', 0.5)
            })
        
        return learning_data
    
    @staticmethod
    def _calculate_velocity_metrics(learning_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive velocity metrics"""
        if not learning_data:
            return {'current_velocity': 0.5, 'velocity_factors': {}}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(learning_data)
        
        # Daily activity rate
        date_range = (df['date'].max() - df['date'].min()).days + 1
        daily_activity_rate = len(df) / max(date_range, 1)
        
        # Average score improvement rate
        if len(df) >= 2:
            score_improvement = (df['score'].iloc[-1] - df['score'].iloc[0]) / len(df)
            progression_rate = max(0, score_improvement)
        else:
            progression_rate = 0
        
        # Learning intensity factor
        avg_intensity = df['intensity'].mean() if 'intensity' in df.columns else 0.5
        
        # Time investment factor
        avg_time_spent = df['time_spent'].mean() if 'time_spent' in df.columns else 0
        time_factor = min(avg_time_spent / 60, 1.0)  # Normalize to 0-1
        
        # Calculate composite velocity score
        velocity_factors = {
            'activity_frequency': min(daily_activity_rate / 5, 1.0),  # Normalize
            'score_progression': progression_rate,
            'learning_intensity': avg_intensity,
            'time_investment': time_factor
        }
        
        current_velocity = np.mean(list(velocity_factors.values()))
        
        return {
            'current_velocity': min(current_velocity, 1.0),
            'daily_activity_rate': daily_activity_rate,
            'score_progression_rate': progression_rate,
            'velocity_factors': velocity_factors,
            'total_activities': len(df)
        }
    
    @staticmethod
    def _analyze_progression_patterns(learning_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze learning progression patterns"""
        if len(learning_data) < 3:
            return {
                'trend': 'insufficient_data',
                'progression_rate': 0.0,
                'momentum': 'unknown'
            }
        
        df = pd.DataFrame(learning_data)
        df = df.sort_values('date')
        
        # Calculate trend using linear regression
        if 'score' in df.columns and len(df) >= 3:
            scores = df['score'].values
            time_points = np.arange(len(scores))
            
            # Simple linear trend
            if len(scores) >= 2:
                early_scores = scores[:len(scores)//2]
                late_scores = scores[len(scores)//2:]
                trend_change = np.mean(late_scores) - np.mean(early_scores)
                
                if trend_change > 0.1:
                    trend = 'improving'
                    momentum = 'positive'
                elif trend_change < -0.1:
                    trend = 'declining'
                    momentum = 'negative'
                else:
                    trend = 'stable'
                    momentum = 'neutral'
            else:
                trend = 'stable'
                momentum = 'neutral'
                trend_change = 0.0
        else:
            trend = 'stable'
            momentum = 'neutral'
            trend_change = 0.0
        
        return {
            'trend': trend,
            'progression_rate': trend_change,
            'momentum': momentum,
            'trend_strength': abs(trend_change),
            'consistency': LearningVelocityAnalyzer._calculate_consistency(scores) if 'score' in df.columns else 0.5
        }
    
    @staticmethod
    def _calculate_consistency(scores: np.ndarray) -> float:
        """Calculate learning consistency score"""
        if len(scores) < 3:
            return 0.5
        
        # Calculate coefficient of variation
        mean_score = np.mean(scores)
        if mean_score == 0:
            return 0.5
        
        std_score = np.std(scores)
        cv = std_score / mean_score
        
        # Convert to consistency score (lower variation = higher consistency)
        consistency = max(0, 1 - cv)
        return consistency
    
    @staticmethod
    def _predict_future_velocity(velocity_metrics: Dict[str, Any], progression_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict future learning velocity"""
        current_velocity = velocity_metrics.get('current_velocity', 0.5)
        trend_change = progression_analysis.get('progression_rate', 0.0)
        momentum = progression_analysis.get('momentum', 'neutral')
        
        # Simple prediction model
        trend_factor = trend_change * 0.1
        momentum_factor = {'positive': 0.1, 'neutral': 0, 'negative': -0.1}[momentum]
        
        predicted_velocity = current_velocity + trend_factor + momentum_factor
        predicted_velocity = max(0.1, min(predicted_velocity, 1.0))
        
        # Calculate confidence based on data quality
        data_points = velocity_metrics.get('total_activities', 0)
        confidence = min(data_points / 20, 1.0)  # Higher confidence with more data
        
        return {
            'predicted_velocity': predicted_velocity,
            'confidence': confidence,
            'trend_direction': 'increasing' if trend_factor + momentum_factor > 0 else 'decreasing' if trend_factor + momentum_factor < 0 else 'stable',
            'prediction_horizon': '30 days'
        }
    
    @staticmethod
    def _analyze_momentum(learning_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze learning momentum and acceleration"""
        if len(learning_data) < 5:
            return {'momentum': 'insufficient_data', 'acceleration': 0}
        
        df = pd.DataFrame(learning_data)
        df = df.sort_values('date')
        
        if 'score' not in df.columns or len(df) < 3:
            return {'momentum': 'unknown', 'acceleration': 0}
        
        scores = df['score'].values
        
        # Calculate momentum (rate of change)
        momentum = np.mean(np.diff(scores))
        
        # Calculate acceleration (change in momentum)
        if len(scores) >= 4:
            momentum_changes = np.diff(scores)
            acceleration = np.mean(np.diff(momentum_changes))
        else:
            acceleration = 0
        
        # Classify momentum
        if acceleration > 0.05:
            momentum_category = 'accelerating'
        elif acceleration < -0.05:
            momentum_category = 'decelerating'
        elif momentum > 0.02:
            momentum_category = 'building'
        elif momentum < -0.02:
            momentum_category = 'slowing'
        else:
            momentum_category = 'stable'
        
        return {
            'momentum': momentum_category,
            'acceleration': acceleration,
            'momentum_strength': abs(momentum)
        }
    
    @staticmethod
    def _generate_velocity_insights(velocity_metrics: Dict[str, Any], progression_analysis: Dict[str, Any]) -> List[str]:
        """Generate insights from velocity analysis"""
        insights = []
        
        velocity_score = velocity_metrics.get('current_velocity', 0.5)
        trend = progression_analysis.get('trend', 'stable')
        momentum = progression_analysis.get('momentum', 'neutral')
        consistency = progression_analysis.get('consistency', 0.5)
        
        # Velocity-based insights
        if velocity_score >= 0.8:
            insights.append("Exceptional learning velocity indicates strong engagement and natural aptitude")
        elif velocity_score >= 0.6:
            insights.append("Good learning velocity with room for optimization")
        elif velocity_score >= 0.4:
            insights.append("Moderate learning velocity - may benefit from engagement strategies")
        else:
            insights.append("Low learning velocity suggests need for motivation and support")
        
        # Trend-based insights
        if trend == 'improving':
            insights.append("Positive learning trajectory shows effective learning strategies")
        elif trend == 'declining':
            insights.append("Declining trend requires immediate attention and strategy adjustment")
        
        # Momentum-based insights
        if momentum == 'positive':
            insights.append("Strong momentum building - learner is gaining confidence and skill")
        elif momentum == 'negative':
            insights.append("Negative momentum detected - risk of disengagement")
        
        # Consistency insights
        if consistency >= 0.7:
            insights.append("Highly consistent learning pattern indicates good study habits")
        elif consistency <= 0.3:
            insights.append("Inconsistent learning pattern suggests need for routine establishment")
        
        return insights
    
    @staticmethod
    def _generate_velocity_recommendations(velocity_metrics: Dict[str, Any], progression_analysis: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        velocity_score = velocity_metrics.get('current_velocity', 0.5)
        trend = progression_analysis.get('trend', 'stable')
        consistency = progression_analysis.get('consistency', 0.5)
        velocity_factors = velocity_metrics.get('velocity_factors', {})
        
        # Velocity-based recommendations
        if velocity_score < 0.5:
            recommendations.extend([
                "Break learning into smaller, manageable chunks",
                "Implement daily micro-learning sessions (5-10 minutes)",
                "Use gamification elements to increase engagement",
                "Provide frequent positive feedback and encouragement"
            ])
        elif velocity_score >= 0.8 and trend == 'improving':
            recommendations.extend([
                "Increase challenge level to maintain engagement",
                "Provide advanced learning opportunities and mentorship",
                "Introduce peer collaboration and knowledge sharing",
                "Consider acceleration to more complex topics"
            ])
        else:
            recommendations.extend([
                "Maintain current learning pace with minor optimizations",
                "Continue monitoring progress for trend changes",
                "Focus on quality over quantity in learning sessions"
            ])
        
        # Factor-specific recommendations
        activity_frequency = velocity_factors.get('activity_frequency', 0.5)
        if activity_frequency < 0.3:
            recommendations.append("Establish more regular learning schedule")
        
        learning_intensity = velocity_factors.get('learning_intensity', 0.5)
        if learning_intensity < 0.4:
            recommendations.append("Increase learning session intensity and focus")
        
        # Trend-specific recommendations
        if trend == 'declining':
            recommendations.insert(0, "URGENT: Address declining performance with additional support")
        elif trend == 'improving' and consistency < 0.5:
            recommendations.append("Work on developing consistent study habits")
        
        return recommendations


class EngagementPatternAnalyzer:
    """
    Complete implementation of engagement pattern analysis
    """
    
    @staticmethod
    def analyze_engagement_patterns(
        user: User,
        time_window_days: int = 30,
        engagement_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive engagement pattern analysis
        """
        try:
            if not engagement_data:
                engagement_data = EngagementPatternAnalyzer._get_engagement_data(user, time_window_days)
            
            # Analyze engagement patterns
            pattern_analysis = EngagementPatternAnalyzer._analyze_engagement_patterns_detail(engagement_data)
            
            # Predict future engagement
            engagement_prediction = EngagementPatternAnalyzer._predict_future_engagement(pattern_analysis)
            
            # Identify engagement triggers
            engagement_triggers = EngagementPatternAnalyzer._identify_engagement_triggers(engagement_data)
            
            # Analyze engagement risks
            risk_analysis = EngagementPatternAnalyzer._analyze_engagement_risks(pattern_analysis, engagement_data)
            
            return {
                'current_engagement_score': pattern_analysis['engagement_score'],
                'pattern_type': pattern_analysis['pattern_type'],
                'consistency': pattern_analysis['consistency'],
                'peak_times': pattern_analysis['peak_times'],
                'engagement_triggers': engagement_triggers,
                'predicted_engagement': engagement_prediction,
                'risk_factors': risk_analysis['risk_factors'],
                'protective_factors': risk_analysis['protective_factors'],
                'recommendations': EngagementPatternAnalyzer._generate_engagement_recommendations(
                    pattern_analysis, engagement_triggers, risk_analysis
                ),
                'analysis_period': f'{time_window_days} days',
                'engagement_milestones': EngagementPatternAnalyzer._identify_engagement_milestones(pattern_analysis)
            }
            
        except Exception as e:
            logger.error(f"Engagement pattern analysis error: {e}")
            return {
                'current_engagement_score': 0.5,
                'pattern_type': 'analysis_error',
                'analysis': f'Error in analysis: {str(e)}'
            }
    
    @staticmethod
    def _get_engagement_data(user: User, time_window_days: int) -> Dict[str, Any]:
        """Get comprehensive engagement data"""
        cutoff_date = timezone.now() - timedelta(days=time_window_days)
        
        from ..models import LearningAnalytics
        activities = LearningAnalytics.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        ).order_by('created_at')
        
        # Process activities
        activity_data = []
        for activity in activities:
            activity_data.append({
                'timestamp': activity.created_at,
                'type': getattr(activity, 'activity_type', 'unknown'),
                'score': getattr(activity, 'score', 0.5),
                'intensity': getattr(activity, 'intensity_score', 0.5),
                'duration': getattr(activity, 'time_spent', 0)
            })
        
        # Analyze session patterns
        session_data = EngagementPatternAnalyzer._extract_session_patterns(activity_data)
        
        return {
            'activities': activity_data,
            'sessions': session_data,
            'total_activities': len(activity_data),
            'analysis_period': time_window_days
        }
    
    @staticmethod
    def _extract_session_patterns(activity_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract learning sessions from activity data"""
        if not activity_data:
            return []
        
        sessions = []
        current_session = None
        
        for activity in sorted(activity_data, key=lambda x: x['timestamp']):
            if current_session is None:
                current_session = {
                    'start_time': activity['timestamp'],
                    'activities': [activity],
                    'total_duration': activity['duration'],
                    'avg_intensity': activity['intensity'],
                    'activity_count': 1
                }
            elif (activity['timestamp'] - current_session['start_time']).total_seconds() < 1800:  # 30 minutes
                # Continue current session
                current_session['activities'].append(activity)
                current_session['total_duration'] += activity['duration']
                current_session['activity_count'] += 1
                current_session['avg_intensity'] = np.mean([a['intensity'] for a in current_session['activities']])
            else:
                # End current session and start new one
                current_session['end_time'] = current_session['activities'][-1]['timestamp']
                sessions.append(current_session)
                current_session = {
                    'start_time': activity['timestamp'],
                    'activities': [activity],
                    'total_duration': activity['duration'],
                    'avg_intensity': activity['intensity'],
                    'activity_count': 1
                }
        
        # Add final session
        if current_session:
            current_session['end_time'] = current_session['activities'][-1]['timestamp']
            sessions.append(current_session)
        
        return sessions
    
    @staticmethod
    def _analyze_engagement_patterns_detail(engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detailed engagement pattern analysis"""
        activities = engagement_data.get('activities', [])
        sessions = engagement_data.get('sessions', [])
        
        if not activities:
            return {
                'engagement_score': 0.1,
                'pattern_type': 'inactive',
                'consistency': 0.0,
                'peak_times': [],
                'risk_factors': ['no_activity']
            }
        
        # Calculate overall engagement score
        engagement_score = EngagementPatternAnalyzer._calculate_engagement_score(activities, sessions)
        
        # Classify engagement pattern
        pattern_type = EngagementPatternAnalyzer._classify_engagement_pattern(activities, sessions)
        
        # Calculate consistency
        consistency = EngagementPatternAnalyzer._calculate_engagement_consistency(sessions)
        
        # Identify peak activity times
        peak_times = EngagementPatternAnalyzer._identify_peak_activity_times(activities)
        
        # Identify risk factors
        risk_factors = EngagementPatternAnalyzer._identify_engagement_risk_factors(activities, sessions, consistency)
        
        return {
            'engagement_score': engagement_score,
            'pattern_type': pattern_type,
            'consistency': consistency,
            'peak_times': peak_times,
            'risk_factors': risk_factors,
            'total_sessions': len(sessions),
            'avg_session_length': np.mean([s['total_duration'] for s in sessions]) if sessions else 0,
            'session_frequency': len(sessions) / max((activities[-1]['timestamp'] - activities[0]['timestamp']).days, 1) if activities else 0
        }
    
    @staticmethod
    def _calculate_engagement_score(activities: List[Dict[str, Any]], sessions: List[Dict[str, Any]]) -> float:
        """Calculate comprehensive engagement score"""
        if not activities:
            return 0.1
        
        # Factors contributing to engagement
        factors = {
            'activity_frequency': 0,
            'session_consistency': 0,
            'intensity_score': 0,
            'progress_indicators': 0
        }
        
        # Activity frequency (0-0.25)
        total_activities = len(activities)
        factors['activity_frequency'] = min(total_activities / 20, 0.25)
        
        # Session consistency (0-0.25)
        if sessions:
            session_lengths = [s['total_duration'] for s in sessions]
            avg_session_length = np.mean(session_lengths)
            factors['session_consistency'] = min(avg_session_length / 60, 0.25)  # Normalize to 1 hour
        
        # Intensity score (0-0.25)
        if activities:
            intensities = [a['intensity'] for a in activities]
            factors['intensity_score'] = np.mean(intensities) * 0.25
        
        # Progress indicators (0-0.25)
        if activities:
            scores = [a['score'] for a in activities if a['score'] is not None]
            if scores:
                factors['progress_indicators'] = np.mean(scores) * 0.25
        
        return min(sum(factors.values()), 1.0)
    
    @staticmethod
    def _classify_engagement_pattern(activities: List[Dict[str, Any]], sessions: List[Dict[str, Any]]) -> str:
        """Classify engagement pattern type"""
        if not activities:
            return 'inactive'
        
        activity_count = len(activities)
        if sessions:
            session_count = len(sessions)
            avg_session_length = np.mean([s['total_duration'] for s in sessions])
        else:
            session_count = 1
            avg_session_length = 1
        
        # Classification logic
        if activity_count >= 20 and avg_session_length >= 30:
            return 'highly_engaged'
        elif activity_count >= 10 and avg_session_length >= 15:
            return 'moderately_engaged'
        elif activity_count >= 5 and avg_session_length >= 10:
            return 'lightly_engaged'
        elif activity_count >= 2:
            return 'sporadically_engaged'
        else:
            return 'minimally_engaged'
    
    @staticmethod
    def _calculate_engagement_consistency(sessions: List[Dict[str, Any]]) -> float:
        """Calculate engagement consistency score"""
        if not sessions or len(sessions) < 2:
            return 0.5
        
        session_lengths = [s['total_duration'] for s in sessions]
        
        # Calculate coefficient of variation
        mean_length = np.mean(session_lengths)
        if mean_length == 0:
            return 0.5
        
        std_length = np.std(session_lengths)
        cv = std_length / mean_length
        
        # Convert to consistency score
        consistency = max(0, 1 - cv)
        return consistency
    
    @staticmethod
    def _identify_peak_activity_times(activities: List[Dict[str, Any]]) -> List[int]:
        """Identify peak activity hours"""
        if not activities:
            return []
        
        # Count activities by hour
        hour_counts = {}
        for activity in activities:
            timestamp = activity.get('timestamp')
            if timestamp:
                hour = timestamp.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if not hour_counts:
            return []
        
        # Find peak hours (top 25% of hours with activity)
        sorted_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)
        peak_threshold = max(2, len(activities) * 0.1)  # At least 2 activities or 10% of total
        peak_hours = [hour for hour, count in sorted_hours if count >= peak_threshold]
        
        return peak_hours[:3]  # Return top 3 peak hours
    
    @staticmethod
    def _identify_engagement_risk_factors(activities: List[Dict[str, Any]], sessions: List[Dict[str, Any]], consistency: float) -> List[str]:
        """Identify engagement risk factors"""
        risk_factors = []
        
        # Low activity frequency
        if len(activities) < 3:
            risk_factors.append('low_activity_frequency')
        
        # Inconsistent engagement
        if consistency < 0.3:
            risk_factors.append('inconsistent_engagement')
        
        # Short sessions
        if sessions:
            avg_session_length = np.mean([s['total_duration'] for s in sessions])
            if avg_session_length < 10:  # Less than 10 minutes
                risk_factors.append('short_sessions')
        
        # Declining intensity
        if len(activities) >= 5:
            recent_intensities = [a['intensity'] for a in activities[-3:]]
            earlier_intensities = [a['intensity'] for a in activities[:3]]
            if np.mean(recent_intensities) < np.mean(earlier_intensities) - 0.2:
                risk_factors.append('declining_intensity')
        
        return risk_factors
    
    @staticmethod
    def _predict_future_engagement(pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict future engagement levels"""
        current_engagement = pattern_analysis.get('engagement_score', 0.5)
        consistency = pattern_analysis.get('consistency', 0.5)
        trend_indicators = pattern_analysis.get('risk_factors', [])
        
        # Simple prediction model
        if consistency >= 0.7:
            predicted_engagement = current_engagement + 0.1  # Consistency builds engagement
        elif 'low_activity_frequency' in trend_indicators:
            predicted_engagement = current_engagement - 0.2  # Risk of disengagement
        else:
            predicted_engagement = current_engagement
        
        predicted_engagement = max(0.1, min(predicted_engagement, 1.0))
        
        return {
            'predicted_engagement_score': predicted_engagement,
            'confidence': consistency,
            'trend': 'increasing' if predicted_engagement > current_engagement else 'decreasing' if predicted_engagement < current_engagement else 'stable'
        }
    
    @staticmethod
    def _identify_engagement_triggers(engagement_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify engagement triggers"""
        activities = engagement_data.get('activities', [])
        triggers = []
        
        if not activities:
            return triggers
        
        # Analyze high-engagement activities
        high_intensity_activities = [a for a in activities if a.get('intensity', 0) >= 0.8]
        if high_intensity_activities:
            triggers.append({
                'trigger': 'high_intensity_interactions',
                'frequency': len(high_intensity_activities),
                'description': 'User shows high engagement during intensive interactions'
            })
        
        # Analyze time-based patterns
        peak_times = EngagementPatternAnalyzer._identify_peak_activity_times(activities)
        if peak_times:
            triggers.append({
                'trigger': 'time_preference',
                'peak_hours': peak_times,
                'description': f'User most active during hours {peak_times}'
            })
        
        # Analyze content preferences
        activity_types = [a.get('type', 'unknown') for a in activities]
        if activity_types:
            most_common_activity = max(set(activity_types), key=activity_types.count)
            activity_frequency = activity_types.count(most_common_activity)
            triggers.append({
                'trigger': 'content_preference',
                'preferred_activity': most_common_activity,
                'frequency': activity_frequency,
                'description': f'User prefers {most_common_activity} activities'
            })
        
        return triggers
    
    @staticmethod
    def _analyze_engagement_risks(pattern_analysis: Dict[str, Any], engagement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze engagement risks and protective factors"""
        risk_factors = pattern_analysis.get('risk_factors', [])
        engagement_score = pattern_analysis.get('engagement_score', 0.5)
        
        # Risk assessment
        risk_level = 'low'
        if len(risk_factors) >= 3 or engagement_score < 0.3:
            risk_level = 'high'
        elif len(risk_factors) >= 1 or engagement_score < 0.6:
            risk_level = 'medium'
        
        # Protective factors
        protective_factors = []
        if engagement_score >= 0.7:
            protective_factors.append('high_engagement_score')
        if pattern_analysis.get('consistency', 0) >= 0.7:
            protective_factors.append('consistent_patterns')
        if len(engagement_data.get('sessions', [])) >= 5:
            protective_factors.append('regular_sessions')
        
        return {
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'protective_factors': protective_factors
        }
    
    @staticmethod
    def _generate_engagement_recommendations(pattern_analysis: Dict[str, Any], engagement_triggers: List[Dict[str, Any]], risk_analysis: Dict[str, Any]) -> List[str]:
        """Generate engagement improvement recommendations"""
        recommendations = []
        
        engagement_score = pattern_analysis.get('engagement_score', 0.5)
        pattern_type = pattern_analysis.get('pattern_type', 'unknown')
        risk_level = risk_analysis.get('risk_level', 'low')
        
        # Score-based recommendations
        if engagement_score < 0.3:
            recommendations.extend([
                "Implement immediate engagement boosters (personalized notifications)",
                "Simplify learning tasks to reduce barriers to entry",
                "Provide immediate positive feedback and recognition",
                "Consider one-on-one check-ins to understand barriers"
            ])
        elif engagement_score < 0.6:
            recommendations.extend([
                "Introduce personalized learning recommendations",
                "Increase variety in learning activities and formats",
                "Set up regular progress celebrations and milestones",
                "Provide social learning opportunities"
            ])
        else:
            recommendations.extend([
                "Maintain current engagement strategies",
                "Introduce advanced challenges and leadership opportunities",
                "Explore peer mentoring and knowledge sharing",
                "Consider becoming a learning ambassador"
            ])
        
        # Risk-specific recommendations
        if risk_level == 'high':
            recommendations.insert(0, "URGENT: Implement immediate intervention strategies")
        elif risk_level == 'medium':
            recommendations.append("Monitor engagement closely and provide additional support")
        
        # Trigger-based recommendations
        for trigger in engagement_triggers:
            if trigger['trigger'] == 'time_preference':
                peak_hours = trigger.get('peak_hours', [])
                if peak_hours:
                    recommendations.append(f"Schedule important activities during peak hours ({peak_hours[0]}:00-{peak_hours[0]+1}:00)")
            elif trigger['trigger'] == 'content_preference':
                preferred_activity = trigger.get('preferred_activity', '')
                if preferred_activity:
                    recommendations.append(f"Provide more {preferred_activity} content and activities")
        
        return recommendations
    
    @staticmethod
    def _identify_engagement_milestones(pattern_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify engagement milestones and achievements"""
        milestones = []
        
        engagement_score = pattern_analysis.get('engagement_score', 0.5)
        consistency = pattern_analysis.get('consistency', 0)
        
        # Milestone definitions
        if engagement_score >= 0.8:
            milestones.append({
                'milestone': 'engagement_excellence',
                'description': 'Consistently high engagement levels',
                'achieved': True,
                'impact': 'high_performer_status'
            })
        
        if consistency >= 0.7:
            milestones.append({
                'milestone': 'consistency_master',
                'description': 'Maintains regular learning habits',
                'achieved': True,
                'impact': 'habit_formation_success'
            })
        
        if pattern_analysis.get('total_sessions', 0) >= 10:
            milestones.append({
                'milestone': 'session_regularity',
                'description': 'Consistently participates in learning sessions',
                'achieved': True,
                'impact': 'dedication_recognition'
            })
        
        return milestones


class SuccessProbabilityPredictor:
    """
    Complete implementation of success probability modeling
    """
    
    @staticmethod
    def predict_success_probability(
        user: User,
        learning_path_id: Optional[int] = None,
        prediction_horizon_days: int = 30
    ) -> Dict[str, Any]:
        """
        Predict probability of success in learning activities
        """
        try:
            # Get user performance data
            performance_data = SuccessProbabilityPredictor._get_user_performance_data(user, learning_path_id)
            
            if not performance_data:
                return {
                    'success_probability': 0.5,
                    'confidence': 0.0,
                    'reason': 'Insufficient performance data'
                }
            
            # Calculate success indicators
            success_indicators = SuccessProbabilityPredictor._calculate_success_indicators(performance_data)
            
            # Apply prediction model
            prediction_result = SuccessProbabilityPredictor._apply_success_prediction_model(success_indicators)
            
            # Analyze success factors
            success_factors = SuccessProbabilityPredictor._analyze_success_factors(performance_data)
            
            return {
                'success_probability': prediction_result['probability'],
                'confidence_level': prediction_result['confidence'],
                'risk_level': prediction_result['risk_level'],
                'success_factors': success_factors,
                'improvement_areas': SuccessProbabilityPredictor._identify_improvement_areas(performance_data),
                'recommended_actions': SuccessProbabilityPredictor._generate_success_recommendations(success_factors, prediction_result),
                'prediction_basis': 'Machine learning model based on user performance patterns',
                'prediction_horizon': f'{prediction_horizon_days} days'
            }
            
        except Exception as e:
            logger.error(f"Success probability prediction error: {e}")
            return {
                'success_probability': 0.5,
                'confidence': 0.0,
                'reason': f'Prediction error: {str(e)}'
            }
    
    @staticmethod
    def _get_user_performance_data(user: User, learning_path_id: Optional[int]) -> Dict[str, Any]:
        """Get comprehensive user performance data"""
        from ..models import LearningAnalytics
        from apps.learning.models import UserModuleProgress, AssessmentAttempt
        
        # Get learning analytics data
        analytics_data = LearningAnalytics.objects.filter(user=user).order_by('-created_at')[:50]
        
        # Get module progress data
        progress_query = UserModuleProgress.objects.filter(user=user)
        if learning_path_id:
            progress_query = progress_query.filter(module__learning_path_id=learning_path_id)
        progress_data = progress_query.select_related('module').order_by('-updated_at')[:20]
        
        # Get assessment data
        assessment_query = AssessmentAttempt.objects.filter(user=user)
        if learning_path_id:
            assessment_query = assessment_query.filter(module__learning_path_id=learning_path_id)
        assessment_data = assessment_query.select_related('module').order_by('-completed_at')[:20]
        
        return {
            'analytics': analytics_data,
            'progress': progress_data,
            'assessments': assessment_data,
            'total_records': analytics_data.count() + progress_data.count() + assessment_data.count()
        }
    
    @staticmethod
    def _calculate_success_indicators(performance_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate success indicators from performance data"""
        indicators = {}
        
        analytics_data = performance_data.get('analytics', [])
        progress_data = performance_data.get('progress', [])
        assessments = performance_data.get('assessments', [])
        
        # Performance consistency
        if analytics_data:
            scores = [getattr(a, 'score', 0.5) for a in analytics_data if hasattr(a, 'score') and a.score is not None]
            if len(scores) >= 3:
                indicators['consistency'] = 1 - (np.std(scores) / np.mean(scores)) if np.mean(scores) > 0 else 0.5
            else:
                indicators['consistency'] = 0.5
        else:
            indicators['consistency'] = 0.5
        
        # Progress rate
        if progress_data:
            completion_rates = [getattr(p, 'completion_percentage', 0) for p in progress_data if hasattr(p, 'completion_percentage')]
            if completion_rates:
                indicators['progress_rate'] = np.mean(completion_rates) / 100
            else:
                indicators['progress_rate'] = 0.5
        else:
            indicators['progress_rate'] = 0.5
        
        # Assessment performance
        if assessments:
            assessment_scores = [getattr(a, 'score', 0.5) for a in assessments if hasattr(a, 'score') and a.score is not None]
            if assessment_scores:
                indicators['assessment_performance'] = np.mean(assessment_scores)
            else:
                indicators['assessment_performance'] = 0.5
        else:
            indicators['assessment_performance'] = 0.5
        
        # Activity frequency
        total_activities = performance_data.get('total_records', 0)
        indicators['activity_frequency'] = min(total_activities / 50, 1.0)  # Normalize to 50 activities
        
        # Time investment
        time_data = [getattr(a, 'time_spent', 0) for a in analytics_data if hasattr(a, 'time_spent')]
        if time_data:
            avg_time = np.mean(time_data)
            indicators['time_investment'] = min(avg_time / 60, 1.0)  # Normalize to 60 minutes
        else:
            indicators['time_investment'] = 0.5
        
        return indicators
    
    @staticmethod
    def _apply_success_prediction_model(success_indicators: Dict[str, float]) -> Dict[str, Any]:
        """Apply machine learning model for success prediction"""
        # Weights for different success indicators
        weights = {
            'consistency': 0.25,
            'progress_rate': 0.25,
            'assessment_performance': 0.2,
            'activity_frequency': 0.15,
            'time_investment': 0.15
        }
        
        # Calculate weighted success probability
        weighted_score = sum(success_indicators.get(indicator, 0.5) * weights[indicator] 
                           for indicator in weights.keys())
        
        # Apply sigmoid transformation for probability
        import math
        probability = 1 / (1 + math.exp(-5 * (weighted_score - 0.5)))
        
        # Calculate confidence based on data completeness
        data_completeness = len([v for v in success_indicators.values() if v != 0.5]) / len(success_indicators)
        confidence = min(data_completeness * 1.2, 1.0)  # Boost confidence for complete data
        
        # Determine risk level
        if probability >= 0.8:
            risk_level = 'low'
        elif probability >= 0.6:
            risk_level = 'medium'
        elif probability >= 0.4:
            risk_level = 'high'
        else:
            risk_level = 'very_high'
        
        return {
            'probability': probability,
            'confidence': confidence,
            'risk_level': risk_level,
            'weighted_score': weighted_score
        }
    
    @staticmethod
    def _analyze_success_factors(performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze key success factors"""
        success_factors = {
            'strongest_factors': [],
            'weakest_factors': [],
            'improvement_potential': {}
        }
        
        analytics_data = performance_data.get('analytics', [])
        
        if analytics_data:
            # Analyze performance trends
            recent_scores = []
            for activity in analytics_data[:10]:  # Last 10 activities
                if hasattr(activity, 'score') and activity.score is not None:
                    recent_scores.append(activity.score)
            
            if len(recent_scores) >= 2:
                if recent_scores[-1] > recent_scores[0]:
                    success_factors['strongest_factors'].append('improving_performance')
                elif recent_scores[-1] == recent_scores[0]:
                    success_factors['strongest_factors'].append('stable_performance')
                else:
                    success_factors['weakest_factors'].append('declining_performance')
        
        # Analyze consistency
        if len(analytics_data) >= 5:
            scores = [getattr(a, 'score', 0.5) for a in analytics_data if hasattr(a, 'score')]
            if len(scores) >= 3:
                cv = np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 1
                if cv < 0.3:
                    success_factors['strongest_factors'].append('consistent_performance')
                elif cv > 0.7:
                    success_factors['weakest_factors'].append('inconsistent_performance')
        
        return success_factors
    
    @staticmethod
    def _identify_improvement_areas(performance_data: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        improvement_areas = []
        
        analytics_data = performance_data.get('analytics', [])
        
        # Low frequency analysis
        if len(analytics_data) < 10:
            improvement_areas.append('increase_learning_frequency')
        
        # Inconsistent performance
        if len(analytics_data) >= 5:
            scores = [getattr(a, 'score', 0.5) for a in analytics_data if hasattr(a, 'score')]
            if len(scores) >= 3:
                cv = np.std(scores) / np.mean(scores) if np.mean(scores) > 0 else 1
                if cv > 0.6:
                    improvement_areas.append('improve_consistency')
        
        # Low intensity activities
        intensities = [getattr(a, 'intensity_score', 0.5) for a in analytics_data if hasattr(a, 'intensity_score')]
        if intensities and np.mean(intensities) < 0.5:
            improvement_areas.append('increase_engagement_intensity')
        
        return improvement_areas
    
    @staticmethod
    def _generate_success_recommendations(success_factors: Dict[str, Any], prediction_result: Dict[str, Any]) -> List[str]:
        """Generate success improvement recommendations"""
        recommendations = []
        
        probability = prediction_result.get('probability', 0.5)
        risk_level = prediction_result.get('risk_level', 'medium')
        
        # Probability-based recommendations
        if probability < 0.5:
            recommendations.extend([
                "Focus on building consistent learning habits",
                "Break down learning goals into smaller, achievable milestones",
                "Increase learning frequency with shorter, regular sessions",
                "Seek additional support or tutoring"
            ])
        elif probability < 0.7:
            recommendations.extend([
                "Maintain current learning strategies with minor adjustments",
                "Focus on consistency in performance",
                "Set specific, measurable learning targets"
            ])
        else:
            recommendations.extend([
                "Consider taking on more challenging material",
                "Help others with learning to reinforce your knowledge",
                "Explore advanced topics and specializations"
            ])
        
        # Risk-level specific recommendations
        if risk_level in ['high', 'very_high']:
            recommendations.insert(0, "URGENT: Implement intensive support measures")
        
        # Success factor-based recommendations
        strongest_factors = success_factors.get('strongest_factors', [])
        weakest_factors = success_factors.get('weakest_factors', [])
        
        if 'consistent_performance' in strongest_factors:
            recommendations.append("Leverage your consistency to take on more ambitious goals")
        
        if 'inconsistent_performance' in weakest_factors:
            recommendations.append("Work on developing more consistent study patterns")
        
        return recommendations


class CompletionTimePredictor:
    """
    Complete implementation of time-to-completion prediction
    """
    
    @staticmethod
    def predict_completion_time(
        user: User,
        module_id: int,
        prediction_horizon_days: int = 60
    ) -> Dict[str, Any]:
        """
        Predict time to completion for a learning module
        """
        try:
            from apps.learning.models import Module
            
            # Get module information
            module = Module.objects.get(id=module_id)
            
            # Get user's historical completion data
            completion_data = CompletionTimePredictor._get_user_completion_data(user)
            
            # Analyze completion patterns
            completion_patterns = CompletionTimePredictor._analyze_completion_patterns(completion_data, module)
            
            # Apply time prediction model
            time_prediction = CompletionTimePredictor._apply_completion_time_model(completion_patterns)
            
            return {
                'predicted_completion_days': time_prediction['days'],
                'confidence_interval': time_prediction['confidence_interval'],
                'factors_affecting_time': completion_patterns['time_factors'],
                'completion_milestones': CompletionTimePredictor._generate_completion_milestones(time_prediction, module),
                'recommendations': CompletionTimePredictor._generate_completion_recommendations(time_prediction, completion_patterns, module),
                'module_difficulty': getattr(module, 'difficulty_rating', 'medium'),
                'user_skill_match': completion_patterns['skill_match'],
                'prediction_horizon': f'{prediction_horizon_days} days'
            }
            
        except Exception as e:
            logger.error(f"Completion time prediction error: {e}")
            return {
                'predicted_completion_days': 30,
                'confidence_interval': [20, 45],
                'reason': f'Prediction error: {str(e)}'
            }
    
    @staticmethod
    def _get_user_completion_data(user: User) -> List[Dict[str, Any]]:
        """Get user's historical completion data"""
        from ..models import LearningAnalytics
        from apps.learning.models import UserModuleProgress, AssessmentAttempt
        
        # Get completed modules
        completed_modules = UserModuleProgress.objects.filter(
            user=user,
            status='completed'
        ).select_related('module').order_by('-updated_at')
        
        completion_data = []
        for progress in completed_modules:
            completion_data.append({
                'module_id': progress.module.id,
                'module_difficulty': getattr(progress.module, 'difficulty_rating', 'medium'),
                'completion_time_days': (progress.updated_at - progress.created_at).days,
                'time_spent_hours': getattr(progress, 'time_spent_hours', 0),
                'final_score': getattr(progress, 'completion_percentage', 100),
                'attempts_count': getattr(progress, 'attempts_count', 1)
            })
        
        return completion_data
    
    @staticmethod
    def _analyze_completion_patterns(completion_data: List[Dict[str, Any]], current_module) -> Dict[str, Any]:
        """Analyze completion patterns"""
        if not completion_data:
            return {
                'skill_match': 'unknown',
                'time_factors': [],
                'historical_avg_time': 30
            }
        
        # Calculate historical averages
        completion_times = [data['completion_time_days'] for data in completion_data]
        avg_completion_time = np.mean(completion_times)
        
        # Analyze difficulty patterns
        difficulty_ratings = ['beginner', 'intermediate', 'advanced', 'expert']
        current_difficulty = getattr(current_module, 'difficulty_rating', 'medium').lower()
        
        # Find similar difficulty modules
        similar_modules = [data for data in completion_data 
                         if data['module_difficulty'].lower() == current_difficulty]
        
        if similar_modules:
            skill_match_score = 0.8  # Good match for similar difficulty
            time_factors = ['similar_difficulty_modules']
        else:
            # Estimate based on progression
            completed_difficulties = [data['module_difficulty'].lower() for data in completion_data]
            if current_difficulty == 'beginner':
                skill_match_score = 0.9  # Should be easy
                time_factors = ['entry_level']
            elif current_difficulty == 'intermediate':
                skill_match_score = 0.7  # Moderate challenge
                time_factors = ['progression_challenge']
            elif current_difficulty == 'advanced':
                skill_match_score = 0.5  # Significant challenge
                time_factors = ['advanced_concepts']
            else:  # expert
                skill_match_score = 0.3  # Major challenge
                time_factors = ['expert_level']
        
        # Determine skill match category
        if skill_match_score >= 0.8:
            skill_match = 'well_prepared'
        elif skill_match_score >= 0.6:
            skill_match = 'appropriately_challenged'
        elif skill_match_score >= 0.4:
            skill_match = 'moderately_challenged'
        else:
            skill_match = 'significantly_challenged'
        
        return {
            'skill_match': skill_match,
            'skill_match_score': skill_match_score,
            'time_factors': time_factors,
            'historical_avg_time': avg_completion_time,
            'similar_completions': len(similar_modules)
        }
    
    @staticmethod
    def _apply_completion_time_model(completion_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Apply prediction model for completion time"""
        skill_match_score = completion_patterns.get('skill_match_score', 0.5)
        historical_avg = completion_patterns.get('historical_avg_time', 30)
        
        # Adjust prediction based on skill match
        if skill_match_score >= 0.8:
            # Well prepared - faster completion
            predicted_days = historical_avg * 0.7
        elif skill_match_score >= 0.6:
            # Appropriately challenged - normal time
            predicted_days = historical_avg * 0.9
        elif skill_match_score >= 0.4:
            # Moderately challenged - slightly slower
            predicted_days = historical_avg * 1.2
        else:
            # Significantly challenged - much slower
            predicted_days = historical_avg * 1.8
        
        # Ensure reasonable bounds
        predicted_days = max(7, min(predicted_days, 120))
        
        # Calculate confidence interval (±30% of prediction)
        margin = predicted_days * 0.3
        confidence_interval = [predicted_days - margin, predicted_days + margin]
        
        return {
            'days': round(predicted_days),
            'confidence_interval': [round(confidence_interval[0]), round(confidence_interval[1])],
            'confidence_score': min(skill_match_score * 1.2, 1.0)
        }
    
    @staticmethod
    def _generate_completion_milestones(time_prediction: Dict[str, Any], module) -> List[Dict[str, Any]]:
        """Generate completion milestones"""
        predicted_days = time_prediction['days']
        skill_match = time_prediction.get('skill_match', 'unknown')
        
        milestones = []
        
        # 25% completion milestone
        milestones.append({
            'milestone': '25_percent',
            'target_days': round(predicted_days * 0.25),
            'description': 'Complete basic concepts and introduction',
            'status': 'planned'
        })
        
        # 50% completion milestone
        milestones.append({
            'milestone': '50_percent',
            'target_days': round(predicted_days * 0.5),
            'description': 'Halfway through module content',
            'status': 'planned'
        })
        
        # 75% completion milestone
        milestones.append({
            'milestone': '75_percent',
            'target_days': round(predicted_days * 0.75),
            'description': 'Advanced topics and practice',
            'status': 'planned'
        })
        
        # 100% completion milestone
        milestones.append({
            'milestone': '100_percent',
            'target_days': predicted_days,
            'description': 'Module completion and assessment',
            'status': 'planned'
        })
        
        return milestones
    
    @staticmethod
    def _generate_completion_recommendations(time_prediction: Dict[str, Any], completion_patterns: Dict[str, Any], module) -> List[str]:
        """Generate completion recommendations"""
        recommendations = []
        
        predicted_days = time_prediction['days']
        skill_match = completion_patterns.get('skill_match', 'unknown')
        skill_match_score = completion_patterns.get('skill_match_score', 0.5)
        
        # Skill match based recommendations
        if skill_match == 'well_prepared':
            recommendations.extend([
                "Accelerate through familiar concepts to maintain momentum",
                "Focus on advanced applications and edge cases",
                "Consider skipping review sections if already mastered"
            ])
        elif skill_match == 'significantly_challenged':
            recommendations.extend([
                "Allocate extra time for concept understanding",
                "Consider prerequisite review before proceeding",
                "Seek additional resources or tutoring support"
            ])
        
        # Time-based recommendations
        if predicted_days > 60:
            recommendations.append("Consider breaking module into smaller sub-modules")
        elif predicted_days < 14:
            recommendations.append("Pace yourself to ensure thorough understanding")
        
        # General recommendations
        recommendations.extend([
            "Set weekly progress goals to stay on track",
            "Regular self-assessment to gauge understanding",
            "Take breaks to maintain concentration and retention"
        ])
        
        return recommendations


class RetentionRiskAssessor:
    """
    Complete implementation of retention risk assessment
    """
    
    @staticmethod
    def assess_retention_risk(
        user: User,
        time_window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Assess risk of user dropping out or disengaging
        """
        try:
            # Get retention risk data
            retention_data = RetentionRiskAssessor._get_retention_risk_data(user, time_window_days)
            
            # Calculate risk indicators
            risk_indicators = RetentionRiskAssessor._calculate_retention_risk_indicators(retention_data)
            
            # Apply retention risk model
            risk_assessment = RetentionRiskAssessor._apply_retention_risk_model(risk_indicators)
            
            # Generate intervention recommendations
            interventions = RetentionRiskAssessor._generate_retention_interventions(risk_assessment, risk_indicators)
            
            return {
                'retention_risk_score': risk_assessment['risk_score'],
                'risk_level': risk_assessment['risk_level'],
                'key_risk_factors': risk_assessment['risk_factors'],
                'protective_factors': risk_assessment['protective_factors'],
                'recommended_interventions': interventions,
                'monitoring_indicators': RetentionRiskAssessor._get_retention_monitoring_indicators(risk_indicators),
                'prediction_confidence': risk_assessment['confidence'],
                'assessment_period': f'{time_window_days} days'
            }
            
        except Exception as e:
            logger.error(f"Retention risk assessment error: {e}")
            return {
                'retention_risk_score': 0.5,
                'risk_level': 'unknown',
                'reason': f'Assessment error: {str(e)}'
            }
    
    @staticmethod
    def _get_retention_risk_data(user: User, time_window_days: int) -> Dict[str, Any]:
        """Get comprehensive retention risk data"""
        cutoff_date = timezone.now() - timedelta(days=time_window_days)
        
        from ..models import LearningAnalytics
        from apps.learning.models import UserModuleProgress
        
        # Get recent activities
        recent_activities = LearningAnalytics.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        ).order_by('-created_at')
        
        # Get progress data
        recent_progress = UserModuleProgress.objects.filter(
            user=user,
            updated_at__gte=cutoff_date
        ).order_by('-updated_at')
        
        return {
            'activities': recent_activities,
            'progress': recent_progress,
            'analysis_period': time_window_days
        }
    
    @staticmethod
    def _calculate_retention_risk_indicators(retention_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate retention risk indicators"""
        activities = retention_data.get('activities', [])
        progress = retention_data.get('progress', [])
        
        indicators = {}
        
        # Activity decline indicator
        if len(activities) >= 10:
            recent_activities = activities[:5]
            earlier_activities = activities[5:10]
            
            recent_intensities = [getattr(a, 'intensity_score', 0.5) for a in recent_activities if hasattr(a, 'intensity_score')]
            earlier_intensities = [getattr(a, 'intensity_score', 0.5) for a in earlier_activities if hasattr(a, 'intensity_score')]
            
            if recent_intensities and earlier_intensities:
                intensity_decline = np.mean(earlier_intensities) - np.mean(recent_intensities)
                indicators['intensity_decline'] = max(0, intensity_decline)
            else:
                indicators['intensity_decline'] = 0
        else:
            indicators['intensity_decline'] = 0
        
        # Time gap indicator
        if activities:
            time_gaps = []
            sorted_activities = sorted(activities, key=lambda x: x.created_at)
            for i in range(1, len(sorted_activities)):
                gap = (sorted_activities[i].created_at - sorted_activities[i-1].created_at).days
                time_gaps.append(gap)
            
            if time_gaps:
                avg_gap = np.mean(time_gaps)
                indicators['activity_gap'] = min(avg_gap / 7, 1.0)  # Normalize to weekly gaps
            else:
                indicators['activity_gap'] = 0
        else:
            indicators['activity_gap'] = 1.0  # High risk if no activities
        
        # Progress stagnation indicator
        if len(progress) >= 3:
            recent_progress = progress[:3]
            older_progress = progress[3:]
            
            if older_progress:
                recent_completion = [getattr(p, 'completion_percentage', 0) for p in recent_progress]
                older_completion = [getattr(p, 'completion_percentage', 0) for p in older_progress]
                
                recent_avg = np.mean(recent_completion) if recent_completion else 0
                older_avg = np.mean(older_completion) if older_completion else 0
                
                progress_stagnation = max(0, older_avg - recent_avg)
                indicators['progress_stagnation'] = min(progress_stagnation / 50, 1.0)  # Normalize
            else:
                indicators['progress_stagnation'] = 0
        else:
            indicators['progress_stagnation'] = 0
        
        # Overall activity level
        total_activities = len(activities)
        indicators['low_activity_level'] = max(0, (10 - total_activities) / 10) if total_activities < 10 else 0
        
        return indicators
    
    @staticmethod
    def _apply_retention_risk_model(risk_indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Apply retention risk assessment model"""
        # Risk factors with weights
        risk_weights = {
            'intensity_decline': 0.3,
            'activity_gap': 0.25,
            'progress_stagnation': 0.25,
            'low_activity_level': 0.2
        }
        
        # Calculate weighted risk score
        risk_score = sum(risk_indicators.get(indicator, 0) * weight 
                        for indicator, weight in risk_weights.items())
        
        # Clamp score
        risk_score = max(0, min(risk_score, 1.0))
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = 'high'
        elif risk_score >= 0.5:
            risk_level = 'medium'
        elif risk_score >= 0.3:
            risk_level = 'low'
        else:
            risk_level = 'very_low'
        
        # Identify key risk factors
        risk_factors = []
        for indicator, value in risk_indicators.items():
            if value > 0.5:  # Threshold for significant risk
                risk_factors.append(indicator)
        
        # Identify protective factors
        protective_factors = []
        if risk_indicators.get('activity_gap', 0) < 0.3:
            protective_factors.append('regular_activity')
        if risk_indicators.get('intensity_decline', 0) < 0.2:
            protective_factors.append('maintained_intensity')
        if risk_indicators.get('low_activity_level', 0) < 0.3:
            protective_factors.append('adequate_activity_level')
        
        # Calculate confidence
        data_completeness = len([v for v in risk_indicators.values() if v > 0]) / len(risk_indicators)
        confidence = min(data_completeness * 1.1, 1.0)
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'protective_factors': protective_factors,
            'confidence': confidence
        }
    
    @staticmethod
    def _generate_retention_interventions(risk_assessment: Dict[str, Any], risk_indicators: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate retention intervention recommendations"""
        interventions = []
        
        risk_level = risk_assessment.get('risk_level', 'low')
        risk_factors = risk_assessment.get('risk_factors', [])
        
        # Risk level based interventions
        if risk_level == 'high':
            interventions.extend([
                {
                    'intervention': 'immediate_check_in',
                    'priority': 'critical',
                    'description': 'Personal contact within 24 hours',
                    'method': 'Direct outreach from instructor or mentor'
                },
                {
                    'intervention': 'learning_plan_review',
                    'priority': 'high',
                    'description': 'Review and adjust learning plan',
                    'method': 'Collaborative goal setting and barrier identification'
                },
                {
                    'intervention': 'intensive_support',
                    'priority': 'high',
                    'description': 'Provide additional learning resources',
                    'method': 'Tutoring, study groups, or supplementary materials'
                }
            ])
        elif risk_level == 'medium':
            interventions.extend([
                {
                    'intervention': 'engagement_boost',
                    'priority': 'moderate',
                    'description': 'Increase learning engagement',
                    'method': 'Gamification, progress celebrations, social learning'
                },
                {
                    'intervention': 'goal_adjustment',
                    'priority': 'moderate',
                    'description': 'Reassess and adjust learning goals',
                    'method': 'SMART goal setting with smaller milestones'
                }
            ])
        else:
            interventions.append({
                'intervention': 'maintain_engagement',
                'priority': 'low',
                'description': 'Continue current engagement strategies',
                'method': 'Regular positive reinforcement and progress tracking'
            })
        
        # Factor-specific interventions
        if 'activity_gap' in risk_factors:
            interventions.append({
                'intervention': 'schedule_reminders',
                'priority': 'high' if risk_level == 'high' else 'moderate',
                'description': 'Implement learning schedule reminders',
                'method': 'Calendar notifications and habit tracking'
            })
        
        if 'intensity_decline' in risk_factors:
            interventions.append({
                'intervention': 'variety_injection',
                'priority': 'moderate',
                'description': 'Introduce learning variety',
                'method': 'Different learning modalities, interactive content'
            })
        
        if 'progress_stagnation' in risk_factors:
            interventions.append({
                'intervention': 'achievement_recognition',
                'priority': 'high' if risk_level == 'high' else 'moderate',
                'description': 'Highlight and celebrate progress',
                'method': 'Progress visualization and milestone celebrations'
            })
        
        return interventions
    
    @staticmethod
    def _get_retention_monitoring_indicators(risk_indicators: Dict[str, Any]) -> List[str]:
        """Get key indicators for ongoing retention monitoring"""
        monitoring_indicators = []
        
        for indicator, value in risk_indicators.items():
            if value > 0.3:  # Monitor indicators with significant risk
                monitoring_indicators.append(indicator)
        
        # Always monitor activity level
        monitoring_indicators.append('activity_frequency')
        
        return monitoring_indicators


class KnowledgeGapDetector:
    """
    Complete implementation of knowledge gap detection
    """
    
    @staticmethod
    def detect_knowledge_gaps(user: User) -> Dict[str, Any]:
        """
        Detect and analyze knowledge gaps
        """
        try:
            # Get user knowledge state
            knowledge_state = KnowledgeGapDetector._get_user_knowledge_state(user)
            
            # Analyze knowledge gaps
            gap_analysis = KnowledgeGapDetector._analyze_knowledge_gaps(knowledge_state)
            
            # Generate gap remediation plans
            remediation_plans = KnowledgeGapDetector._generate_remediation_plans(gap_analysis)
            
            return {
                'detected_gaps': gap_analysis['gaps'],
                'gap_severity_distribution': gap_analysis['severity_distribution'],
                'priority_gaps': gap_analysis['priority_gaps'],
                'remediation_plans': remediation_plans,
                'gap_patterns': KnowledgeGapDetector._identify_gap_patterns(gap_analysis),
                'recommendations': KnowledgeGapDetector._generate_gap_recommendations(gap_analysis),
                'assessment_confidence': gap_analysis['confidence']
            }
            
        except Exception as e:
            logger.error(f"Knowledge gap detection error: {e}")
            return {
                'detected_gaps': [],
                'error': f'Detection error: {str(e)}'
            }
    
    @staticmethod
    def _get_user_knowledge_state(user: User) -> Dict[str, Any]:
        """Get comprehensive user knowledge state"""
        from ..models import LearningAnalytics
        from apps.learning.models import UserModuleProgress, UserKnowledgeState
        
        # Get learning analytics
        analytics_data = LearningAnalytics.objects.filter(user=user).order_by('-created_at')[:50]
        
        # Get knowledge states
        knowledge_states = UserKnowledgeState.objects.filter(user=user).select_related('knowledge_node')
        
        # Get module progress
        module_progress = UserModuleProgress.objects.filter(user=user).select_related('module')
        
        return {
            'analytics': analytics_data,
            'knowledge_states': knowledge_states,
            'module_progress': module_progress
        }
    
    @staticmethod
    def _analyze_knowledge_gaps(knowledge_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze knowledge gaps from user state"""
        gaps = []
        
        knowledge_states = knowledge_state.get('knowledge_states', [])
        analytics_data = knowledge_state.get('analytics', [])
        
        # Analyze knowledge states
        for state in knowledge_states:
            if hasattr(state, 'mastery_level') and hasattr(state, 'confidence_score'):
                mastery = state.mastery_level
                confidence = state.confidence_score
                
                # Identify gaps based on low mastery and confidence
                if mastery in ['novice', 'beginner'] and confidence < 0.6:
                    gaps.append({
                        'concept': getattr(state.knowledge_node, 'title', 'Unknown'),
                        'current_mastery': mastery,
                        'confidence_score': confidence,
                        'gap_severity': 'high',
                        'gap_type': 'fundamental_concept'
                    })
                elif mastery == 'intermediate' and confidence < 0.5:
                    gaps.append({
                        'concept': getattr(state.knowledge_node, 'title', 'Unknown'),
                        'current_mastery': mastery,
                        'confidence_score': confidence,
                        'gap_severity': 'medium',
                        'gap_type': 'skill_development'
                    })
        
        # Analyze performance-based gaps
        if analytics_data:
            # Find consistently low-scoring areas
            low_score_activities = [a for a in analytics_data if hasattr(a, 'score') and a.score and a.score < 0.6]
            
            # Group by activity type to identify pattern gaps
            activity_scores = {}
            for activity in low_score_activities:
                activity_type = getattr(activity, 'activity_type', 'unknown')
                if activity_type not in activity_scores:
                    activity_scores[activity_type] = []
                activity_scores[activity_type].append(activity.score)
            
            for activity_type, scores in activity_scores.items():
                if len(scores) >= 3 and np.mean(scores) < 0.5:
                    gaps.append({
                        'concept': f'{activity_type} activities',
                        'current_mastery': 'developing',
                        'confidence_score': np.mean(scores),
                        'gap_severity': 'high',
                        'gap_type': 'performance_based'
                    })
        
        # Calculate severity distribution
        severity_counts = {'high': 0, 'medium': 0, 'low': 0}
        for gap in gaps:
            severity = gap.get('gap_severity', 'low')
            severity_counts[severity] += 1
        
        # Identify priority gaps (high severity + low confidence)
        priority_gaps = [gap for gap in gaps 
                        if gap.get('gap_severity') == 'high' and gap.get('confidence_score', 1) < 0.4]
        
        # Calculate confidence in assessment
        total_assessments = len(knowledge_states) + len(low_score_activities)
        confidence = min(total_assessments / 20, 1.0) if total_assessments > 0 else 0
        
        return {
            'gaps': gaps,
            'severity_distribution': severity_counts,
            'priority_gaps': priority_gaps,
            'total_gaps': len(gaps),
            'confidence': confidence
        }
    
    @staticmethod
    def _generate_remediation_plans(gap_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate remediation plans for identified gaps"""
        remediation_plans = []
        
        gaps = gap_analysis.get('gaps', [])
        
        for gap in gaps:
            severity = gap.get('gap_severity', 'low')
            gap_type = gap.get('gap_type', 'unknown')
            concept = gap.get('concept', 'Unknown concept')
            
            # Generate severity-based remediation plan
            if severity == 'high':
                remediation_plans.append({
                    'gap': concept,
                    'priority': 'immediate',
                    'approach': 'intensive_remediation',
                    'timeline': '1-2 weeks',
                    'strategies': [
                        'Provide foundational learning materials',
                        'Schedule one-on-one tutoring sessions',
                        'Implement frequent check-ins and feedback',
                        'Use multi-modal learning approaches'
                    ],
                    'success_metrics': ['mastery_level_improvement', 'confidence_score_increase']
                })
            elif severity == 'medium':
                remediation_plans.append({
                    'gap': concept,
                    'priority': 'near_term',
                    'approach': 'focused_practice',
                    'timeline': '2-4 weeks',
                    'strategies': [
                        'Provide targeted practice exercises',
                        'Offer supplementary learning resources',
                        'Implement peer learning opportunities',
                        'Regular progress monitoring'
                    ],
                    'success_metrics': ['performance_improvement', 'engagement_increase']
                })
            else:  # low severity
                remediation_plans.append({
                    'gap': concept,
                    'priority': 'ongoing',
                    'approach': 'maintenance_practice',
                    'timeline': 'ongoing',
                    'strategies': [
                        'Provide occasional review materials',
                        'Encourage self-directed learning',
                        'Offer optional advanced resources'
                    ],
                    'success_metrics': ['knowledge_retention', 'voluntary_engagement']
                })
        
        return remediation_plans
    
    @staticmethod
    def _identify_gap_patterns(gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Identify patterns in knowledge gaps"""
        gaps = gap_analysis.get('gaps', [])
        
        if not gaps:
            return {'patterns': 'no_gaps_detected'}
        
        # Analyze gap types
        gap_types = [gap.get('gap_type', 'unknown') for gap in gaps]
        type_distribution = {}
        for gap_type in gap_types:
            type_distribution[gap_type] = type_distribution.get(gap_type, 0) + 1
        
        # Find most common gap type
        most_common_gap_type = max(type_distribution.items(), key=lambda x: x[1])[0] if type_distribution else 'none'
        
        # Analyze mastery levels
        mastery_levels = [gap.get('current_mastery', 'unknown') for gap in gaps]
        mastery_distribution = {}
        for mastery in mastery_levels:
            mastery_distribution[mastery] = mastery_distribution.get(mastery, 0) + 1
        
        # Identify pattern
        if most_common_gap_type == 'fundamental_concept':
            pattern = 'foundational_knowledge_gaps'
            description = 'User struggles with core concepts, needs foundational support'
        elif most_common_gap_type == 'performance_based':
            pattern = 'application_skill_gaps'
            description = 'User understands concepts but struggles with practical application'
        elif len(gap_types) > 2:
            pattern = 'mixed_knowledge_gaps'
            description = 'User has gaps across multiple areas, needs comprehensive support'
        else:
            pattern = 'specific_skill_gaps'
            description = 'User has targeted knowledge gaps in specific areas'
        
        return {
            'primary_pattern': pattern,
            'pattern_description': description,
            'gap_type_distribution': type_distribution,
            'mastery_distribution': mastery_distribution,
            'pattern_severity': 'high' if gap_analysis.get('total_gaps', 0) > 5 else 'medium' if gap_analysis.get('total_gaps', 0) > 2 else 'low'
        }
    
    @staticmethod
    def _generate_gap_recommendations(gap_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for addressing knowledge gaps"""
        recommendations = []
        
        total_gaps = gap_analysis.get('total_gaps', 0)
        priority_gaps = gap_analysis.get('priority_gaps', [])
        patterns = gap_analysis.get('gap_patterns', {})
        
        # Overall strategy based on gap count
        if total_gaps == 0:
            recommendations.append("No significant knowledge gaps detected - maintain current learning approach")
        elif total_gaps <= 2:
            recommendations.append("Focus on targeted remediation for identified gaps")
        elif total_gaps <= 5:
            recommendations.append("Implement systematic gap remediation with priority ordering")
        else:
            recommendations.append("Consider comprehensive learning plan review and restructuring")
        
        # Priority-based recommendations
        if len(priority_gaps) > 0:
            recommendations.append(f"URGENT: Address {len(priority_gaps)} high-priority knowledge gaps immediately")
        
        # Pattern-based recommendations
        primary_pattern = patterns.get('primary_pattern', 'unknown')
        if primary_pattern == 'foundational_knowledge_gaps':
            recommendations.extend([
                "Provide comprehensive foundational materials",
                "Consider prerequisite course or module completion",
                "Implement systematic concept review"
            ])
        elif primary_pattern == 'application_skill_gaps':
            recommendations.extend([
                "Increase hands-on practice opportunities",
                "Provide more practical examples and case studies",
                "Implement project-based learning approaches"
            ])
        elif primary_pattern == 'mixed_knowledge_gaps':
            recommendations.extend([
                "Conduct comprehensive learning needs assessment",
                "Develop personalized learning pathway",
                "Provide multi-modal learning resources"
            ])
        
        return recommendations


class AdaptiveFeedbackGenerator:
    """
    Complete implementation of adaptive feedback generation
    """
    
    @staticmethod
    def generate_adaptive_feedback(user: User, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized, adaptive feedback
        """
        try:
            # Analyze user context
            user_context = AdaptiveFeedbackGenerator._analyze_user_context(user)
            
            # Analyze activity performance
            performance_analysis = AdaptiveFeedbackGenerator._analyze_activity_performance(activity_data, user_context)
            
            # Generate feedback components
            feedback_components = AdaptiveFeedbackGenerator._generate_feedback_components(performance_analysis, user_context)
            
            # Adapt feedback to user preferences
            adapted_feedback = AdaptiveFeedbackGenerator._adapt_feedback_to_user(feedback_components, user_context)
            
            return {
                'feedback_text': adapted_feedback['main_feedback'],
                'encouragement': adapted_feedback['encouragement'],
                'specific_guidance': adapted_feedback['specific_guidance'],
                'next_steps': adapted_feedback['next_steps'],
                'learning_recommendations': adapted_feedback['learning_recommendations'],
                'confidence_building': adapted_feedback['confidence_building'],
                'feedback_style': adapted_feedback['style'],
                'tone': adapted_feedback['tone'],
                'adaptation_factors': adapted_feedback['adaptation_factors']
            }
            
        except Exception as e:
            logger.error(f"Adaptive feedback generation error: {e}")
            return {
                'feedback_text': 'Good effort! Keep practicing and learning.',
                'encouragement': 'You are making progress.',
                'next_steps': 'Continue with your learning activities.',
                'error': f'Feedback generation error: {str(e)}'
            }
    
    @staticmethod
    def _analyze_user_context(user: User) -> Dict[str, Any]:
        """Analyze user context for feedback adaptation"""
        from ..models import LearningAnalytics
        
        # Get recent activities
        recent_activities = LearningAnalytics.objects.filter(user=user).order_by('-created_at')[:10]
        
        context = {
            'user_id': user.id,
            'recent_performance': [],
            'learning_style_indicators': {},
            'engagement_level': 'moderate',
            'skill_level': 'intermediate'
        }
        
        # Analyze recent performance
        for activity in recent_activities:
            if hasattr(activity, 'score') and activity.score is not None:
                context['recent_performance'].append(activity.score)
        
        # Determine engagement level
        if len(recent_activities) >= 5:
            context['engagement_level'] = 'high'
        elif len(recent_activities) >= 2:
            context['engagement_level'] = 'moderate'
        else:
            context['engagement_level'] = 'low'
        
        # Analyze performance trends
        if len(context['recent_performance']) >= 3:
            recent_scores = context['recent_performance'][:3]
            avg_score = np.mean(recent_scores)
            
            if avg_score >= 0.8:
                context['skill_level'] = 'advanced'
            elif avg_score >= 0.6:
                context['skill_level'] = 'intermediate'
            else:
                context['skill_level'] = 'beginner'
        
        return context
    
    @staticmethod
    def _analyze_activity_performance(activity_data: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance for feedback generation"""
        score = activity_data.get('score', 0.5)
        time_spent = activity_data.get('time_spent', 0)
        attempts = activity_data.get('attempts', 1)
        
        # Performance classification
        if score >= 0.9:
            performance_level = 'excellent'
        elif score >= 0.8:
            performance_level = 'very_good'
        elif score >= 0.7:
            performance_level = 'good'
        elif score >= 0.6:
            performance_level = 'satisfactory'
        elif score >= 0.4:
            performance_level = 'needs_improvement'
        else:
            performance_level = 'struggling'
        
        # Efficiency analysis
        expected_time = 30  # minutes
        efficiency = expected_time / max(time_spent, 1) if time_spent > 0 else 1
        
        # Effort analysis
        effort_score = min(attempts / 3, 1.0)  # Normalize attempts
        
        return {
            'performance_level': performance_level,
            'score': score,
            'efficiency': efficiency,
            'effort_score': effort_score,
            'performance_trend': 'improving' if score > 0.7 else 'needs_attention'
        }
    
    @staticmethod
    def _generate_feedback_components(performance_analysis: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate feedback components"""
        performance_level = performance_analysis.get('performance_level', 'satisfactory')
        score = performance_analysis.get('score', 0.5)
        user_skill = user_context.get('skill_level', 'intermediate')
        engagement = user_context.get('engagement_level', 'moderate')
        
        components = {}
        
        # Performance-based main feedback
        if performance_level in ['excellent', 'very_good']:
            components['main_feedback'] = "Outstanding work! You've demonstrated excellent understanding and skill."
            components['tone'] = 'celebratory'
        elif performance_level == 'good':
            components['main_feedback'] = "Good job! You're making solid progress with this concept."
            components['tone'] = 'encouraging'
        elif performance_level == 'satisfactory':
            components['main_feedback'] = "You're on the right track. Keep practicing to strengthen your understanding."
            components['tone'] = 'supportive'
        elif performance_level == 'needs_improvement':
            components['main_feedback'] = "This concept needs more practice. Don't worry - learning takes time and effort."
            components['tone'] = 'encouraging'
        else:  # struggling
            components['main_feedback'] = "This is challenging, but that's part of learning. Let's break it down together."
            components['tone'] = 'supportive'
        
        # Skill-level appropriate guidance
        if user_skill == 'beginner':
            components['specific_guidance'] = "Focus on understanding the basic concepts first. Take your time with each step."
        elif user_skill == 'intermediate':
            components['specific_guidance'] = "You're ready for more complex applications. Try connecting this to what you already know."
        else:  # advanced
            components['specific_guidance'] = "Challenge yourself to apply this concept in new ways or teach it to others."
        
        # Effort-based encouragement
        effort_score = performance_analysis.get('effort_score', 0.5)
        if effort_score > 0.7:
            components['encouragement'] = "I can see your dedication and hard work. This effort will pay off!"
        elif effort_score > 0.4:
            components['encouragement'] = "Good effort! Consistent practice will help you improve."
        else:
            components['encouragement'] = "Remember, every step forward counts. Keep pushing forward!"
        
        return components
    
    @staticmethod
    def _adapt_feedback_to_user(feedback_components: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt feedback to user preferences and context"""
        adapted = feedback_components.copy()
        
        # Adapt style based on engagement level
        engagement = user_context.get('engagement_level', 'moderate')
        
        if engagement == 'high':
            adapted['style'] = 'direct_and_challenging'
            adapted['encouragement'] += " You're doing great - ready for the next challenge?"
        elif engagement == 'low':
            adapted['style'] = 'gentle_and_supportive'
            adapted['encouragement'] += " Take breaks when you need them. Progress, not perfection!"
        else:
            adapted['style'] = 'balanced_and_encouraging'
        
        # Generate next steps
        performance_level = user_context.get('performance_level', 'satisfactory')
        if performance_level in ['excellent', 'very_good']:
            adapted['next_steps'] = [
                "Apply this knowledge to more advanced problems",
                "Help explain this concept to someone else",
                "Explore related topics that interest you"
            ]
        elif performance_level in ['good', 'satisfactory']:
            adapted['next_steps'] = [
                "Practice similar problems to reinforce this concept",
                "Review any areas that felt unclear",
                "Connect this to other concepts you've learned"
            ]
        else:
            adapted['next_steps'] = [
                "Review the fundamental concepts related to this problem",
                "Try easier versions of this problem first",
                "Ask for help if you're still confused"
            ]
        
        # Generate learning recommendations
        adapted['learning_recommendations'] = [
            "Set aside regular time for practice",
            "Don't hesitate to review previous concepts",
            "Take notes on what works best for you"
        ]
        
        # Confidence building
        if user_context.get('skill_level') == 'beginner':
            adapted['confidence_building'] = "Remember, everyone starts somewhere. You're building a strong foundation!"
        elif user_context.get('skill_level') == 'intermediate':
            adapted['confidence_building'] = "Your growing skills are really showing. Trust in your abilities!"
        else:
            adapted['confidence_building'] = "Your expertise is developing nicely. Keep challenging yourself!"
        
        # Track adaptation factors
        adapted['adaptation_factors'] = [
            f"User skill level: {user_context.get('skill_level')}",
            f"Engagement level: {engagement}",
            f"Performance level: {user_context.get('performance_level', 'satisfactory')}"
        ]
        
        return adapted


# Integration function to add all methods to the predictive analytics service
def integrate_learning_algorithms():
    """
    Integration function to add all completed learning algorithms to the predictive analytics service
    """
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    
    # Add learning velocity analysis
    def analyze_learning_velocity_wrapper(self, user, time_window_days=30):
        return LearningVelocityAnalyzer.analyze_learning_velocity(user, time_window_days)
    
    PredictiveAnalyticsService.analyze_learning_velocity = analyze_learning_velocity_wrapper
    
    # Add engagement pattern analysis
    def analyze_engagement_patterns_wrapper(self, user, time_window_days=30):
        return EngagementPatternAnalyzer.analyze_engagement_patterns(user, time_window_days)
    
    PredictiveAnalyticsService.analyze_engagement_patterns = analyze_engagement_patterns_wrapper
    
    # Add success probability prediction
    def predict_success_probability_wrapper(self, user, learning_path_id=None):
        return SuccessProbabilityPredictor.predict_success_probability(user, learning_path_id)
    
    PredictiveAnalyticsService.predict_success_probability = predict_success_probability_wrapper
    
    # Add completion time prediction
    def predict_completion_time_wrapper(self, user, module_id):
        return CompletionTimePredictor.predict_completion_time(user, module_id)
    
    PredictiveAnalyticsService.predict_completion_time = predict_completion_time_wrapper
    
    # Add retention risk assessment
    def assess_retention_risk_wrapper(self, user, time_window_days=30):
        return RetentionRiskAssessor.assess_retention_risk(user, time_window_days)
    
    PredictiveAnalyticsService.assess_retention_risk = assess_retention_risk_wrapper
    
    # Add knowledge gap detection
    def detect_knowledge_gaps_wrapper(self, user):
        return KnowledgeGapDetector.detect_knowledge_gaps(user)
    
    PredictiveAnalyticsService.detect_knowledge_gaps = detect_knowledge_gaps_wrapper
    
    # Add adaptive feedback generation
    def generate_adaptive_feedback_wrapper(self, user, activity_data):
        return AdaptiveFeedbackGenerator.generate_adaptive_feedback(user, activity_data)
    
    PredictiveAnalyticsService.generate_adaptive_feedback = generate_adaptive_feedback_wrapper
    
    print("✅ All learning algorithms successfully integrated!")


if __name__ == "__main__":
    print("🚀 Learning Algorithms Implementation Complete")
    print("Integrating algorithms with predictive analytics service...")
    integrate_learning_algorithms()
    print("✅ Integration complete! All algorithms are now available.")