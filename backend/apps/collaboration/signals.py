"""
Collaboration Signals - JAC Learning Platform

Django signals for automatic collaboration features.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    StudyGroup, StudyGroupMembership, DiscussionForum, DiscussionTopic,
    DiscussionPost, PeerCodeShare, GroupChallenge, ChallengeParticipation,
    MentorshipRelationship, MentorshipSession
)

@receiver(post_save, sender=StudyGroup)
def create_discussion_forum(sender, instance, created, **kwargs):
    """Create discussion forum when study group is created"""
    if created:
        DiscussionForum.objects.get_or_create(
            study_group=instance,
            defaults={
                'name': f"{instance.name} Discussion",
                'description': f"Discussion forum for {instance.name}"
            }
        )

@receiver(post_save, sender=StudyGroupMembership)
def notify_membership_change(sender, instance, created, **kwargs):
    """Handle membership changes in study groups"""
    if created:
        # Could send notification email or create activity log
        pass

@receiver(post_save, sender=DiscussionTopic)
def increment_topic_views(sender, instance, created, **kwargs):
    """Update forum statistics when topic is created"""
    if created:
        forum = instance.forum
        # Could update forum statistics
        pass

@receiver(post_save, sender=DiscussionPost)
def update_topic_activity(sender, instance, created, **kwargs):
    """Update topic activity when post is created"""
    if created:
        topic = instance.topic
        topic.updated_at = timezone.now()
        topic.save(update_fields=['updated_at'])

@receiver(post_save, sender=PeerCodeShare)
def track_code_share_stats(sender, instance, created, **kwargs):
    """Track code sharing statistics"""
    if created:
        # Could log creation activity
        pass

@receiver(post_save, sender=GroupChallenge)
def notify_challenge_participants(sender, instance, created, **kwargs):
    """Notify study group members about new challenges"""
    if created:
        # Could send notifications to study group members
        pass

@receiver(post_save, sender=ChallengeParticipation)
def update_challenge_status(sender, instance, created, **kwargs):
    """Update challenge status when participation changes"""
    if created:
        challenge = instance.challenge
        if challenge.status == 'draft':
            challenge.status = 'active'
            challenge.save(update_fields=['status'])

@receiver(post_save, sender=MentorshipRelationship)
def schedule_initial_session(sender, instance, created, **kwargs):
    """Schedule initial session when mentorship relationship is activated"""
    if instance.status == 'active' and not instance.sessions.exists():
        # Could create initial session scheduling
        pass

@receiver(post_save, sender=MentorshipSession)
def update_mentorship_stats(sender, instance, created, **kwargs):
    """Update mentorship relationship when session is completed"""
    if instance.status == 'completed':
        relationship = instance.relationship
        # Could update relationship statistics
        pass

# User profile updates
@receiver(post_save, sender=User)
def create_user_collaboration_preferences(sender, instance, created, **kwargs):
    """Initialize collaboration preferences when user is created"""
    if created:
        # Could create user preferences for collaboration features
        pass