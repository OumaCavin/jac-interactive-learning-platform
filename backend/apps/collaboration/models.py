"""
Collaboration Models - JAC Learning Platform

Models for study groups, discussions, peer sharing, and mentorship.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
import uuid

User = get_user_model()

class StudyGroup(models.Model):
    """Study groups for collaborative learning"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    subject_area = models.CharField(max_length=100, db_index=True)
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ])
    
    # Group settings
    max_members = models.PositiveIntegerField(default=10)
    is_public = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_study_groups')
    
    class Meta:
        db_table = 'collaboration_study_group'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} ({self.subject_area})"

class StudyGroupMembership(models.Model):
    """Membership in study groups"""
    
    class MembershipRole(models.TextChoices):
        MEMBER = 'member', 'Member'
        MODERATOR = 'moderator', 'Moderator'
        LEADER = 'leader', 'Leader'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_group_memberships')
    role = models.CharField(max_length=20, choices=MembershipRole.choices, default=MembershipRole.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'collaboration_study_group_membership'
        unique_together = ['study_group', 'user']
        ordering = ['joined_at']
        
    def __str__(self):
        return f"{self.user.username} -> {self.study_group.name}"

class DiscussionForum(models.Model):
    """Discussion forums for each study group"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    study_group = models.OneToOneField(StudyGroup, on_delete=models.CASCADE, related_name='forum')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'collaboration_discussion_forum'
        
    def __str__(self):
        return f"Forum: {self.study_group.name}"

class DiscussionTopic(models.Model):
    """Topics within discussion forums"""
    
    class TopicStatus(models.TextChoices):
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        PINNED = 'pinned', 'Pinned'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    forum = models.ForeignKey(DiscussionForum, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_topics')
    status = models.CharField(max_length=20, choices=TopicStatus.choices, default=TopicStatus.OPEN)
    is_pinned = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_discussion_topic'
        ordering = ['-is_pinned', '-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.forum.study_group.name}"

class DiscussionPost(models.Model):
    """Posts within discussion topics"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_posts')
    content = models.TextField()
    parent_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_solution = models.BooleanField(default=False, help_text="Marked as solution by topic author")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_discussion_post'
        ordering = ['created_at']
        
    def __str__(self):
        return f"Post by {self.author.username} in {self.topic.title}"

class PeerCodeShare(models.Model):
    """Code sharing between peers"""
    
    class ShareType(models.TextChoices):
        SNIPPET = 'snippet', 'Code Snippet'
        PROJECT = 'project', 'Full Project'
        SOLUTION = 'solution', 'Problem Solution'
        TUTORIAL = 'tutorial', 'Tutorial'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    code_content = models.TextField(help_text="Actual code content")
    language = models.CharField(max_length=50, db_index=True)
    file_name = models.CharField(max_length=200, blank=True)
    tags = models.JSONField(default=list, help_text="List of tags for categorization")
    share_type = models.CharField(max_length=20, choices=ShareType.choices)
    is_public = models.BooleanField(default=True)
    is_tutorial = models.BooleanField(default=False)
    
    # Statistics
    likes_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_codes')
    topic = models.ForeignKey(DiscussionTopic, on_delete=models.CASCADE, null=True, blank=True, related_name='shared_codes')
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='shared_codes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_peer_code_share'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} by {self.author.username}"

class CodeLike(models.Model):
    """Likes for shared code"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_share = models.ForeignKey(PeerCodeShare, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'collaboration_code_like'
        unique_together = ['code_share', 'user']
        
    def __str__(self):
        return f"{self.user.username} liked {self.code_share.title}"

class GroupChallenge(models.Model):
    """Challenges for study groups"""
    
    class ChallengeType(models.TextChoices):
        CODING = 'coding', 'Coding Challenge'
        PROBLEM_SOLVING = 'problem_solving', 'Problem Solving'
        RESEARCH = 'research', 'Research Project'
        PRESENTATION = 'presentation', 'Presentation'
        
    class ChallengeStatus(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    challenge_type = models.CharField(max_length=30, choices=ChallengeType.choices)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('expert', 'Expert')
    ])
    
    # Challenge details
    problem_statement = models.TextField()
    requirements = models.JSONField(default=list)
    test_cases = models.JSONField(default=list)
    solution_template = models.TextField(blank=True)
    
    # Timing
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    estimated_duration = models.PositiveIntegerField(help_text="Estimated time in hours")
    
    # Status and settings
    status = models.CharField(max_length=20, choices=ChallengeStatus.choices, default=ChallengeStatus.DRAFT)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    allow_team_participation = models.BooleanField(default=True)
    
    # Relationships
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_group_challenges')
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='challenges')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_group_challenge'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.study_group.name}"

class ChallengeParticipation(models.Model):
    """Participation in group challenges"""
    
    class ParticipationStatus(models.TextChoices):
        REGISTERED = 'registered', 'Registered'
        IN_PROGRESS = 'in_progress', 'In Progress'
        SUBMITTED = 'submitted', 'Submitted'
        COMPLETED = 'completed', 'Completed'
        ABANDONED = 'abandoned', 'Abandoned'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    challenge = models.ForeignKey(GroupChallenge, on_delete=models.CASCADE, related_name='participations')
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_participations')
    team_name = models.CharField(max_length=200, blank=True)
    team_members = models.JSONField(default=list, help_text="List of team member usernames")
    
    # Progress tracking
    status = models.CharField(max_length=20, choices=ParticipationStatus.choices, default=ParticipationStatus.REGISTERED)
    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Submission details
    submission_content = models.TextField(blank=True)
    code_files = models.JSONField(default=list, help_text="List of submitted code files")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_challenge_participation'
        unique_together = ['challenge', 'participant']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.participant.username} - {self.challenge.title}"

class MentorshipRelationship(models.Model):
    """Mentorship relationships"""
    
    class RelationshipStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentoring_relationships')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_relationships')
    
    # Relationship details
    subject_areas = models.JSONField(default=list, help_text="Areas of expertise/interest")
    goals = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=RelationshipStatus.choices, default=RelationshipStatus.PENDING)
    
    # Meeting settings
    meeting_frequency = models.CharField(max_length=50, blank=True, help_text="e.g., weekly, bi-weekly")
    session_duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    
    # Timestamps
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_mentorship_relationship'
        unique_together = ['mentor', 'mentee']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.mentor.username} -> {self.mentee.username}"

class MentorshipSession(models.Model):
    """Individual mentorship sessions"""
    
    class SessionStatus(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        NO_SHOW = 'no_show', 'No Show'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    relationship = models.ForeignKey(MentorshipRelationship, on_delete=models.CASCADE, related_name='sessions')
    
    # Session details
    title = models.CharField(max_length=200)
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    action_items = models.JSONField(default=list)
    
    # Scheduling
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=SessionStatus.choices, default=SessionStatus.SCHEDULED)
    session_type = models.CharField(max_length=50, choices=[
        ('one_on_one', 'One-on-One'),
        ('group', 'Group Session'),
        ('code_review', 'Code Review'),
        ('project_discussion', 'Project Discussion')
    ], default='one_on_one')
    
    # Feedback
    mentor_feedback = models.TextField(blank=True)
    mentee_feedback = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True, help_text="1-5 rating")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaboration_mentorship_session'
        ordering = ['-scheduled_start']
        
    def __str__(self):
        return f"{self.title} - {self.relationship}"