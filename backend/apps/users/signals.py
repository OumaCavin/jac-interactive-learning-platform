# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Signal handlers for the Users app.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import UserProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    """Handle user creation signals."""
    if created:
        # Award welcome achievement
        welcome_achievement = {
            'name': 'Welcome to JAC Learning!',
            'description': 'Successfully registered and started the JAC learning journey',
            'timestamp': timezone.now().isoformat(),
            'points_earned': 10,
            'category': 'onboarding'
        }
        
        if welcome_achievement not in instance.achievements:
            instance.achievements.append(welcome_achievement)
            instance.total_points += 10
            instance.save(update_fields=['achievements', 'total_points'])
        
        # Create initial learning profile
        # This could be extended to create default learning preferences
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def user_updated(sender, instance, **kwargs):
    """Handle user update signals."""
    # Update last activity timestamp
    instance.last_activity_at = timezone.now()
    
    # Auto-save the timestamp
    UserModel.objects.filter(id=instance.id).update(last_activity_at=instance.last_activity_at)


@receiver(post_delete, sender=UserModel)
def user_deleted(sender, instance, **kwargs):
    """Handle user deletion signals."""
    # Clean up related data if needed
    # This would depend on your related models structure
    pass


@receiver(post_save, sender=UserModel)
def check_achievements(sender, instance, **kwargs):
    """Check and award achievements based on user progress."""
    # Level achievements
    level_achievements = {
        5: {'name': 'Rising Star', 'description': 'Reached Level 5', 'points': 50},
        10: {'name': 'Dedicated Learner', 'description': 'Reached Level 10', 'points': 100},
        25: {'name': 'JAC Expert', 'description': 'Reached Level 25', 'points': 250},
        50: {'name': 'Master Programmer', 'description': 'Reached Level 50', 'points': 500},
    }
    
    if instance.level in level_achievements:
        achievement_data = level_achievements[instance.level]
        
        # Check if achievement already exists
        existing_achievements = [a.get('name') for a in instance.achievements]
        
        if achievement_data['name'] not in existing_achievements:
            new_achievement = {
                'name': achievement_data['name'],
                'description': achievement_data['description'],
                'timestamp': timezone.now().isoformat(),
                'points_earned': achievement_data['points'],
                'category': 'progress'
            }
            
            instance.achievements.append(new_achievement)
            instance.total_points += achievement_data['points']
            instance.save(update_fields=['achievements', 'total_points'])
    
    # Streak achievements
    streak_achievements = {
        7: {'name': 'Week Warrior', 'description': '7-day learning streak', 'points': 25},
        30: {'name': 'Monthly Master', 'description': '30-day learning streak', 'points': 100},
        100: {'name': 'Century Scholar', 'description': '100-day learning streak', 'points': 500},
    }
    
    if instance.current_streak in streak_achievements:
        achievement_data = streak_achievements[instance.current_streak]
        
        # Check if achievement already exists
        existing_achievements = [a.get('name') for a in instance.achievements]
        
        if achievement_data['name'] not in existing_achievements:
            new_achievement = {
                'name': achievement_data['name'],
                'description': achievement_data['description'],
                'timestamp': timezone.now().isoformat(),
                'points_earned': achievement_data['points'],
                'category': 'consistency'
            }
            
            instance.achievements.append(new_achievement)
            instance.total_points += achievement_data['points']
            instance.save(update_fields=['achievements', 'total_points'])


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the UserProfile instance whenever the User is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=UserModel)
def ensure_admin_permissions(sender, instance, **kwargs):
    """
    Ensure superuser permissions are properly maintained.
    This handles edge cases where superuser permissions might not be set correctly.
    """
    # If user is supposed to be a superuser, ensure all admin flags are set
    if instance.is_superuser:
        if not instance.is_staff:
            instance.is_staff = True
            instance.save(update_fields=['is_staff'])
        if not instance.is_active:
            instance.is_active = True
            instance.save(update_fields=['is_active'])