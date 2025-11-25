#!/usr/bin/env python3
"""
Adaptive Learning Implementation Status Check

This script comprehensively analyzes the current implementation status of 
adaptive learning features in the JAC Learning Platform.

Author: Cavin Otieno
Date: 2025-11-26
"""

import os
import sys
import django
from pathlib import Path

# Add the backend path to the Python path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import json
from django.apps import apps
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

class AdaptiveLearningChecker:
    """Analyze adaptive learning implementation status"""
    
    def __init__(self):
        self.results = {
            'implementation_status': {},
            'missing_features': [],
            'partially_implemented': [],
            'fully_implemented': [],
            'technical_requirements': {},
            'recommendations': []
        }
    
    def analyze_adaptive_learning_features(self):
        """Analyze all adaptive learning features"""
        print("🔍 Analyzing Adaptive Learning Implementation...")
        
        # Check specific features
        self.check_difficulty_adjustment()
        self.check_content_personalization()
        self.check_spaced_repetition()
        self.check_challenge_generation()
        self.check_performance_tracking()
        self.check_learning_algorithms()
        self.check_ai_integration()
        
        return self.results
    
    def check_difficulty_adjustment(self):
        """Check difficulty adjustment based on progress"""
        print("   📊 Checking Difficulty Adjustment System...")
        
        # Check models for difficulty tracking
        models_to_check = [
            'apps.learning.models.Module',
            'apps.learning.models.UserModuleProgress',
            'apps.assessment.models.Assessment',
            'apps.progress.models.UserLearningProfile'
        ]
        
        difficulty_features = {
            'difficulty_rating': 'Module difficulty rating (1-5 scale)',
            'user_performance_history': 'Track user performance across difficulty levels',
            'adaptive_difficulty_algorithm': 'AI algorithm to adjust difficulty',
            'difficulty_progression_tracking': 'Track how users progress through difficulty levels',
            'personalized_difficulty_curves': 'Individual difficulty progression curves'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check if models exist and have difficulty-related fields
        try:
            from apps.learning.models import Module, UserModuleProgress
            from apps.assessment.models import Assessment
            
            # Check Module model
            module_fields = [field.name for field in Module._meta.fields]
            if 'difficulty_rating' in module_fields:
                implemented_features.append('difficulty_rating')
            else:
                missing_features.append('difficulty_rating')
            
            # Check UserModuleProgress
            progress_fields = [field.name for field in UserModuleProgress._meta.fields]
            difficulty_related = [f for f in progress_fields if 'difficulty' in f.lower()]
            if not difficulty_related:
                missing_features.extend(['user_difficulty_performance', 'difficulty_adjustment_history'])
            
            # Check Assessment model
            if hasattr(Assessment, '_meta'):
                assessment_fields = [field.name for field in Assessment._meta.fields]
                if 'difficulty_level' in assessment_fields:
                    implemented_features.append('assessment_difficulty_level')
            
        except ImportError as e:
            missing_features.append(f'Model access error: {str(e)}')
        
        # Check for adaptive difficulty services
        try:
            # Look for difficulty adjustment services
            service_files = [
                'backend/apps/agents/progress_tracker.py',
                'backend/apps/learning/services/adaptive_learning_service.py',
                'backend/apps/ai/services/difficulty_adjustment.py'
            ]
            
            adaptive_found = False
            for service_file in service_files:
                if os.path.exists(service_file):
                    with open(service_file, 'r') as f:
                        content = f.read()
                        if 'difficulty' in content.lower() and 'adjust' in content.lower():
                            adaptive_found = True
                            break
            
            if adaptive_found:
                implemented_features.append('adaptive_difficulty_service')
            else:
                missing_features.append('adaptive_difficulty_service')
                
        except Exception as e:
            missing_features.append(f'Service check error: {str(e)}')
        
        self.results['implementation_status']['difficulty_adjustment'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'System to adjust content difficulty based on user performance'
        }
    
    def check_content_personalization(self):
        """Check content personalization engine"""
        print("   🎯 Checking Content Personalization Engine...")
        
        personalization_features = {
            'user_learning_profile': 'User learning preferences and style',
            'content_recommendation_system': 'AI-powered content recommendations',
            'personalized_learning_paths': 'Adaptive learning path generation',
            'content_adaptation_algorithm': 'Real-time content adaptation',
            'learning_style_detection': 'Automatic detection of learning styles',
            'personalization_dashboard': 'User interface for personalization settings'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check for personalization models
        try:
            # Look for user profile or personalization models
            from django.apps import apps
            learning_app = apps.get_model('learning', 'UserLearningPath')
            progress_app = apps.get_model('progress', 'UserLearningProfile')
            
            # Check if we have learning recommendations
            if hasattr(learning_app, 'LearningRecommendation'):
                implemented_features.append('learning_recommendations')
            
            # Check user progress tracking
            progress_fields = [field.name for field in progress_app._meta.fields] if progress_app else []
            personalization_fields = [f for f in progress_fields if any(term in f.lower() for term in ['style', 'preference', 'personal', 'custom'])]
            
            if personalization_fields:
                implemented_features.extend(personalization_fields)
            else:
                missing_features.extend(['learning_style_profile', 'preference_tracking'])
                
        except Exception as e:
            missing_features.append(f'Personalization model error: {str(e)}')
        
        # Check for personalization services
        try:
            service_files = [
                'backend/apps/agents/ai_multi_agent_system.py',
                'backend/apps/agents/motivator.py',
                'backend/apps/learning/services/personalization_service.py'
            ]
            
            ai_found = False
            for service_file in service_files:
                if os.path.exists(service_file):
                    with open(service_file, 'r') as f:
                        content = f.read()
                        if any(term in content.lower() for term in ['personalize', 'recommend', 'adapt']):
                            ai_found = True
                            break
            
            if ai_found:
                implemented_features.append('ai_personalization')
            else:
                missing_features.append('ai_personalization_service')
                
        except Exception as e:
            missing_features.append(f'Personalization service error: {str(e)}')
        
        self.results['implementation_status']['content_personalization'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'Engine to personalize content based on user behavior and preferences'
        }
    
    def check_spaced_repetition(self):
        """Check spaced repetition system"""
        print("   🔄 Checking Spaced Repetition System...")
        
        spaced_repetition_features = {
            'spaced_repetition_algorithm': 'Algorithm to schedule review sessions',
            'forgetting_curve_tracking': 'Track user forgetting curves',
            'review_schedule_generation': 'Generate optimal review schedules',
            'knowledge_retention_tracking': 'Monitor retention over time',
            'adaptive_review_intervals': 'Adjust intervals based on performance'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check for spaced repetition models
        try:
            # Look for models that might track repetition/scheduling
            from apps.learning.models import UserModuleProgress
            from apps.assessment.models import AssessmentAttempt
            
            # Check if models have timing/scheduling fields
            progress_fields = [field.name for field in UserModuleProgress._meta.fields]
            scheduling_fields = [f for f in progress_fields if any(term in f.lower() for term in ['schedule', 'interval', 'repeat', 'review'])]
            
            if scheduling_fields:
                implemented_features.extend(scheduling_fields)
            else:
                missing_features.extend(['review_schedule', 'next_review_date', 'repetition_count'])
            
        except Exception as e:
            missing_features.append(f'Spaced repetition model error: {str(e)}')
        
        # Check for spaced repetition services
        try:
            service_files = [
                'backend/apps/progress/services/analytics_service.py',
                'backend/apps/learning/services/spaced_repetition_service.py'
            ]
            
            repetition_found = False
            for service_file in service_files:
                if os.path.exists(service_file):
                    with open(service_file, 'r') as f:
                        content = f.read()
                        if any(term in content.lower() for term in ['spaced', 'repetition', 'forgetting', 'retention']):
                            repetition_found = True
                            break
            
            if repetition_found:
                implemented_features.append('spaced_repetition_service')
            else:
                missing_features.append('spaced_repetition_service')
                
        except Exception as e:
            missing_features.append(f'Spaced repetition service error: {str(e)}')
        
        self.results['implementation_status']['spaced_repetition'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'System to schedule and manage spaced repetition for optimal learning'
        }
    
    def check_challenge_generation(self):
        """Check challenge generation AI"""
        print("   🎮 Checking Challenge Generation AI...")
        
        challenge_features = {
            'ai_challenge_generator': 'AI system to generate coding challenges',
            'difficulty_matched_challenges': 'Challenges that match user skill level',
            'adaptive_problem_solving': 'Problems that adapt based on user responses',
            'creative_challenge_variation': 'Generate variations of existing challenges',
            'performance_based_challenges': 'Challenges based on user performance data'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check for challenge generation in AI agents
        try:
            ai_files = [
                'backend/apps/agents/ai_multi_agent_system.py',
                'backend/apps/agents/quiz_master.py',
                'backend/apps/agents/motivator.py'
            ]
            
            challenge_found = False
            for ai_file in ai_files:
                if os.path.exists(ai_file):
                    with open(ai_file, 'r') as f:
                        content = f.read()
                        if any(term in content.lower() for term in ['challenge', 'generate', 'problem', 'exercise']):
                            challenge_found = True
                            break
            
            if challenge_found:
                implemented_features.append('ai_challenge_generation')
            else:
                missing_features.append('ai_challenge_generator')
            
            # Check for assessment/quiz models that might support challenge generation
            try:
                from apps.learning.models import Assessment, Question
                if hasattr(Assessment, 'questions'):
                    implemented_features.append('assessment_system')
            except:
                missing_features.append('assessment_challenge_system')
                
        except Exception as e:
            missing_features.append(f'Challenge generation error: {str(e)}')
        
        self.results['implementation_status']['challenge_generation'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'AI system to generate adaptive challenges and problems'
        }
    
    def check_performance_tracking(self):
        """Check performance analysis tracking"""
        print("   📈 Checking Performance Analysis Tracking...")
        
        performance_features = {
            'detailed_performance_metrics': 'Comprehensive performance tracking',
            'real_time_analytics': 'Live performance analytics',
            'learning_velocity_tracking': 'Track learning speed and efficiency',
            'competency_mapping': 'Map skills to competencies',
            'predictive_analytics': 'Predict future performance',
            'performance_insights': 'Generate actionable performance insights'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check analytics service
        try:
            analytics_file = 'backend/apps/progress/services/analytics_service.py'
            if os.path.exists(analytics_file):
                with open(analytics_file, 'r') as f:
                    content = f.read()
                    analytics_terms = ['analytics', 'performance', 'tracking', 'metrics', 'velocity']
                    if any(term in content.lower() for term in analytics_terms):
                        implemented_features.append('analytics_service')
                        
                        # Check for specific methods
                        if 'generate_user_analytics' in content:
                            implemented_features.append('user_analytics')
                        if 'learning_velocity' in content:
                            implemented_features.append('learning_velocity')
                        if 'performance_trend' in content:
                            implemented_features.append('performance_trends')
            else:
                missing_features.append('analytics_service')
                
        except Exception as e:
            missing_features.append(f'Analytics service error: {str(e)}')
        
        # Check progress tracker agent
        try:
            progress_file = 'backend/apps/agents/progress_tracker.py'
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    content = f.read()
                    if 'ProgressTrackerAgent' in content:
                        implemented_features.append('progress_tracker_agent')
                        
                        # Check for specific capabilities
                        if 'generate_analytics' in content:
                            implemented_features.append('analytics_generation')
                        if 'analyze_trends' in content:
                            implemented_features.append('trend_analysis')
            else:
                missing_features.append('progress_tracker_agent')
                
        except Exception as e:
            missing_features.append(f'Progress tracker error: {str(e)}')
        
        self.results['implementation_status']['performance_tracking'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'Comprehensive performance analysis and tracking system'
        }
    
    def check_learning_algorithms(self):
        """Check adaptive learning algorithms"""
        print("   🧠 Checking Adaptive Learning Algorithms...")
        
        algorithm_features = {
            'machine_learning_models': 'ML models for learning predictions',
            'recommendation_algorithms': 'Content and path recommendation algorithms',
            'optimization_algorithms': 'Learning path optimization',
            'pattern_recognition': 'Identify learning patterns',
            'adaptive_pacing': 'Adjust learning pace dynamically'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check for AI/ML integration
        try:
            ai_files = [
                'backend/apps/agents/ai_multi_agent_system.py',
                'backend/config/settings.py'
            ]
            
            ai_found = False
            gemini_found = False
            for ai_file in ai_files:
                if os.path.exists(ai_file):
                    with open(ai_file, 'r') as f:
                        content = f.read()
                        if 'gemini' in content.lower() or 'generativeai' in content.lower():
                            gemini_found = True
                        if any(term in content.lower() for term in ['algorithm', 'model', 'recommend', 'predict']):
                            ai_found = True
            
            if gemini_found:
                implemented_features.append('gemini_ai_integration')
            if ai_found:
                implemented_features.append('ai_algorithms')
            
            # Check for specific algorithm implementations
            algorithm_files = [
                'backend/apps/learning/services/adaptive_learning.py',
                'backend/apps/ai/services/learning_algorithms.py'
            ]
            
            for algo_file in algorithm_files:
                if os.path.exists(algo_file):
                    implemented_features.append('adaptive_algorithm_file')
                    break
            else:
                missing_features.append('adaptive_learning_algorithms')
                
        except Exception as e:
            missing_features.append(f'Algorithm check error: {str(e)}')
        
        self.results['implementation_status']['learning_algorithms'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'AI and ML algorithms for adaptive learning'
        }
    
    def check_ai_integration(self):
        """Check AI integration for adaptive features"""
        print("   🤖 Checking AI Integration...")
        
        ai_features = {
            'gemini_api_integration': 'Google Gemini API for AI capabilities',
            'multi_agent_system': 'Multi-agent AI system',
            'natural_language_processing': 'NLP for content analysis',
            'intelligent_feedback': 'AI-powered feedback system',
            'learning_assistant_agents': 'AI agents for learning assistance'
        }
        
        implemented_features = []
        missing_features = []
        
        # Check AI integration
        try:
            ai_system_file = 'backend/apps/agents/ai_multi_agent_system.py'
            if os.path.exists(ai_system_file):
                with open(ai_system_file, 'r') as f:
                    content = f.read()
                    
                    if 'gemini' in content.lower():
                        implemented_features.append('gemini_integration')
                    if 'AIAgent' in content:
                        implemented_features.append('ai_agent_system')
                    if 'GenerativeModel' in content:
                        implemented_features.append('generative_ai')
            else:
                missing_features.append('ai_multi_agent_system')
                
            # Check settings for API keys
            settings_file = 'backend/config/settings.py'
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    content = f.read()
                    if 'GEMINI_API_KEY' in content:
                        implemented_features.append('api_configuration')
                    else:
                        missing_features.append('api_configuration')
                        
        except Exception as e:
            missing_features.append(f'AI integration check error: {str(e)}')
        
        # Check AI agents
        agent_files = [
            'backend/apps/agents/quiz_master.py',
            'backend/apps/agents/motivator.py',
            'backend/apps/agents/progress_tracker.py'
        ]
        
        agent_count = 0
        for agent_file in agent_files:
            if os.path.exists(agent_file):
                agent_count += 1
        
        if agent_count >= 2:
            implemented_features.append('multiple_ai_agents')
        else:
            missing_features.append('ai_agent_implementation')
        
        self.results['implementation_status']['ai_integration'] = {
            'status': 'partial' if implemented_features else 'missing',
            'implemented_features': implemented_features,
            'missing_features': missing_features,
            'description': 'AI integration for adaptive learning features'
        }
    
    def generate_recommendations(self):
        """Generate implementation recommendations"""
        print("   💡 Generating Recommendations...")
        
        recommendations = []
        
        # Based on implementation status
        for feature, status in self.results['implementation_status'].items():
            if status['status'] == 'missing':
                recommendations.append({
                    'priority': 'high',
                    'feature': feature,
                    'recommendation': f"Implement {feature} system - currently missing",
                    'technical_approach': self.get_technical_approach(feature),
                    'estimated_effort': self.get_effort_estimate(feature)
                })
            elif status['status'] == 'partial':
                recommendations.append({
                    'priority': 'medium',
                    'feature': feature,
                    'recommendation': f"Complete {feature} implementation",
                    'missing_components': status.get('missing_features', []),
                    'technical_approach': self.get_technical_approach(feature),
                    'estimated_effort': self.get_effort_estimate(feature)
                })
        
        self.results['recommendations'] = recommendations
    
    def get_technical_approach(self, feature):
        """Get technical approach for implementing a feature"""
        approaches = {
            'difficulty_adjustment': 'Implement dynamic difficulty adjustment using performance data and ML algorithms',
            'content_personalization': 'Build personalization engine using user behavior analytics and AI recommendations',
            'spaced_repetition': 'Implement spaced repetition algorithm (SM-2 or similar) with review scheduling',
            'challenge_generation': 'Use AI (Gemini) to generate adaptive challenges based on user skill level',
            'performance_tracking': 'Enhance existing analytics with real-time performance monitoring',
            'learning_algorithms': 'Implement ML models for learning pattern recognition and prediction',
            'ai_integration': 'Expand AI agent capabilities for adaptive learning features'
        }
        return approaches.get(feature, 'Standard implementation approach needed')
    
    def get_effort_estimate(self, feature):
        """Get effort estimate for implementing a feature"""
        estimates = {
            'difficulty_adjustment': '2-3 weeks',
            'content_personalization': '3-4 weeks',
            'spaced_repetition': '2-3 weeks',
            'challenge_generation': '1-2 weeks',
            'performance_tracking': '1-2 weeks',
            'learning_algorithms': '4-5 weeks',
            'ai_integration': '2-3 weeks'
        }
        return estimates.get(feature, '1-2 weeks')
    
    def print_results(self):
        """Print comprehensive results"""
        print("\n" + "="*80)
        print("🎯 ADAPTIVE LEARNING IMPLEMENTATION STATUS REPORT")
        print("="*80)
        
        # Implementation status
        print("\n📊 IMPLEMENTATION STATUS:")
        for feature, status in self.results['implementation_status'].items():
            status_emoji = {'complete': '✅', 'partial': '⚠️', 'missing': '❌'}.get(status['status'], '❓')
            print(f"   {status_emoji} {feature.replace('_', ' ').title()}: {status['status'].upper()}")
        
        # Summary statistics
        complete_count = sum(1 for s in self.results['implementation_status'].values() if s['status'] == 'complete')
        partial_count = sum(1 for s in self.results['implementation_status'].values() if s['status'] == 'partial')
        missing_count = sum(1 for s in self.results['implementation_status'].values() if s['status'] == 'missing')
        total_features = len(self.results['implementation_status'])
        
        print(f"\n📈 SUMMARY:")
        print(f"   Total Features Analyzed: {total_features}")
        print(f"   Complete: {complete_count} ({complete_count/total_features*100:.1f}%)")
        print(f"   Partial: {partial_count} ({partial_count/total_features*100:.1f}%)")
        print(f"   Missing: {missing_count} ({missing_count/total_features*100:.1f}%)")
        
        # Recommendations
        if self.results['recommendations']:
            print(f"\n💡 TOP RECOMMENDATIONS:")
            sorted_recommendations = sorted(self.results['recommendations'], key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['priority']], reverse=True)
            for i, rec in enumerate(sorted_recommendations[:5], 1):
                print(f"   {i}. {rec['feature'].replace('_', ' ').title()} ({rec['priority'].upper()})")
                print(f"      Effort: {rec['estimated_effort']}")
        
        # Technical requirements
        print(f"\n🔧 TECHNICAL REQUIREMENTS:")
        print(f"   ✅ Django framework foundation")
        print(f"   ✅ Google Gemini AI API integration")
        print(f"   ✅ PostgreSQL/SQLite database")
        print(f"   ✅ Django REST Framework")
        print(f"   ✅ Multi-agent AI system")
        print(f"   ⚠️  Additional ML/AI libraries needed for adaptive features")
        
        return self.results

def main():
    """Main function to run the analysis"""
    print("🚀 Starting Adaptive Learning Implementation Analysis...")
    
    checker = AdaptiveLearningChecker()
    results = checker.analyze_adaptive_learning_features()
    checker.generate_recommendations()
    final_results = checker.print_results()
    
    # Save results to JSON
    output_file = 'adaptive_learning_status_report.json'
    with open(output_file, 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    
    return final_results

if __name__ == '__main__':
    main()