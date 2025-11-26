# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Gamification Signals - JAC Learning Platform

Django signals for automatic gamification triggers.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import (
    UserPoints, UserLevel, LearningStreak, UserBadge, UserAchievement,
    Achievement, AchievementProgress
)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_gamification_records(sender, instance, created, **kwargs):
    """Create initial gamification records when user is created"""
    if created:
        # Create UserPoints
        UserPoints.objects.get_or_create(user=instance)
        
        # Create UserLevel
        UserLevel.objects.get_or_create(user=instance)
        
        # Create LearningStreak
        LearningStreak.objects.get_or_create(user=instance)


@receiver(post_save, sender='learning.UserModuleProgress')
def update_gamification_on_module_completion(sender, instance, created, **kwargs):
    """Update gamification when module is completed"""
    if instance.is_completed and not created:  # Only on completion updates
        user = instance.user
        
        # Award points for module completion
        user_points = UserPoints.objects.get_or_create(user=user)[0]
        user_points.add_points(50, 'module_completion', {
            'module_id': str(instance.module.id),
            'module_title': instance.module.title,
            'learning_path_id': str(instance.learning_path.id) if instance.learning_path else None
        })
        
        # Update learning streak
        streak = LearningStreak.objects.get_or_create(user=user)[0]
        streak.record_activity()
        
        # Check for learning-related achievements
        _check_learning_achievements(user, instance.module.learning_path)
        
        # Update module completion achievement
        _update_achievement_progress(user, 'modules_completed', 1)


@receiver(post_save, sender='assessments.AssessmentAttempt')
def update_gamification_on_assessment(sender, instance, created, **kwargs):
    """Update gamification when assessment is completed"""
    if not created:  # Only on updates (when attempt is finalized)
        user = instance.user
        
        # Award points based on score
        if instance.score >= 90:
            points = 100
            source = 'assessment_perfect'
        elif instance.score >= 70:
            points = 75
            source = 'assessment_good'
        elif instance.score >= 50:
            points = 50
            source = 'assessment_passed'
        else:
            points = 25
            source = 'assessment_attempted'
        
        user_points = UserPoints.objects.get_or_create(user=user)[0]
        user_points.add_points(points, source, {
            'assessment_id': str(instance.assessment.id),
            'score': instance.score,
            'attempt_number': instance.attempt_number
        })
        
        # Update streak
        streak = LearningStreak.objects.get_or_create(user=user)[0]
        streak.record_activity()
        
        # Check for assessment-related achievements
        _check_assessment_achievements(user, instance)
        
        # Update assessment achievement
        _update_achievement_progress(user, 'assessments_completed', 1)
        
        if instance.score >= 100:  # Perfect score
            _update_achievement_progress(user, 'perfect_scores', 1)


@receiver(post_save, sender='jac_execution.CodeExecution')
def update_gamification_on_code_execution(sender, instance, created, **kwargs):
    """Update gamification when code is successfully executed"""
    if instance.is_successful:
        user = instance.user
        
        # Award points for code execution
        user_points = UserPoints.objects.get_or_create(user=user)[0]
        user_points.add_points(25, 'code_execution', {
            'code_execution_id': str(instance.id),
            'language': instance.language,
            'execution_time': instance.execution_time.total_seconds() if instance.execution_time else None
        })
        
        # Update coding achievement
        _update_achievement_progress(user, 'code_executions', 1)


# @receiver(post_save, sender='agents.AgentCommunication')  # TEMPORARILY DISABLED
def update_gamification_on_agent_chat(sender, instance, created, **kwargs):
    """Update gamification when user chats with AI agents"""
    if created:
        user = instance.user
        
        # Award points for AI interaction
        user_points = UserPoints.objects.get_or_create(user=user)[0]
        user_points.add_points(10, 'ai_chat', {
            'agent_id': str(instance.agent.id),
            'agent_type': instance.agent.agent_type
        })
        
        # Update AI interaction achievement
        _update_achievement_progress(user, 'ai_conversations', 1)


@receiver(post_save, sender='knowledge_graph.KnowledgeNode')
def update_gamification_on_knowledge_graph(sender, instance, created, **kwargs):
    """Update gamification when user creates or explores knowledge nodes"""
    if created:
        user = instance.created_by
        
        if user and user.is_authenticated:
            # Award points for knowledge graph activity
            user_points = UserPoints.objects.get_or_create(user=user)[0]
            user_points.add_points(15, 'knowledge_graph', {
                'node_id': str(instance.id),
                'node_type': instance.node_type
            })
            
            # Update knowledge graph achievement
            _update_achievement_progress(user, 'knowledge_nodes_created', 1)


def _check_learning_achievements(user, learning_path):
    """Check and unlock learning-related achievements"""
    # Get user's module completion count
    from apps.learning.models import ModuleProgress
    completed_modules = ModuleProgress.objects.filter(
        user=user, 
        is_completed=True
    ).count()
    
    # Check specific achievement thresholds
    achievement_thresholds = [1, 5, 10, 25, 50, 100]
    
    for threshold in achievement_thresholds:
        achievement = Achievement.objects.filter(
            criteria_type='modules_completed',
            criteria_value=threshold,
            is_active=True
        ).first()
        
        if achievement and completed_modules >= threshold:
            _unlock_achievement(user, achievement)


def _check_assessment_achievements(user, assessment_attempt):
    """Check and unlock assessment-related achievements"""
    from apps.assessments.models import AssessmentAttempt
    
    # Perfect scores achievement
    perfect_scores = AssessmentAttempt.objects.filter(
        user=user,
        score=100
    ).count()
    
    achievement = Achievement.objects.filter(
        criteria_type='perfect_scores',
        criteria_value=5,
        is_active=True
    ).first()
    
    if achievement and perfect_scores >= 5:
        _unlock_achievement(user, achievement)


def _update_achievement_progress(user, achievement_type, increment_by=1):
    """Update progress for achievement type"""
    achievements = Achievement.objects.filter(
        criteria_type=achievement_type,
        is_active=True
    )
    
    for achievement in achievements:
        progress, created = AchievementProgress.objects.get_or_create(
            user=user,
            achievement=achievement,
            defaults={'target_count': achievement.criteria_value}
        )
        
        # Update progress
        progress.increment(increment_by)
        
        # Check if achievement should be completed
        if progress.current_count >= progress.target_count:
            _unlock_achievement(user, achievement)


def _unlock_achievement(user, achievement):
    """Unlock an achievement for a user"""
    # Check if already unlocked
    if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
        return
    
    # Create user achievement
    user_achievement = UserAchievement.objects.create(
        user=user,
        achievement=achievement,
        target_progress=achievement.criteria_value,
        current_progress=achievement.criteria_value,
        is_completed=True,
        completed_at=timezone.now(),
        points_earned=achievement.points_reward
    )
    
    # Award points
    user_points = UserPoints.objects.get_or_create(user=user)[0]
    user_points.add_points(achievement.points_reward, 'achievement', {
        'achievement_id': str(achievement.id),
        'achievement_title': achievement.title
    })
    
    # Award badge if associated
    if achievement.badge:
        user_badge = UserBadge.objects.create(
            user=user,
            badge=achievement.badge,
            earned_through='achievement_unlock',
            is_verified=True,
            verified_at=timezone.now()
        )
        user_achievement.badge_earned = user_badge
        user_achievement.save()
    
    # Update user level
    user_level = UserLevel.objects.get_or_create(user=user)[0]
    user_level.add_xp(achievement.points_reward)