# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Collaboration Views - JAC Learning Platform

Django REST Framework viewsets for collaboration features.

Author: Cavin Otieno
Created: 2025-11-26
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import (
    StudyGroup, StudyGroupMembership, DiscussionForum, DiscussionTopic,
    DiscussionPost, PeerCodeShare, CodeLike, GroupChallenge,
    ChallengeParticipation, MentorshipRelationship, MentorshipSession
)
from .serializers import (
    StudyGroupSerializer, StudyGroupMembershipSerializer, DiscussionTopicSerializer,
    DiscussionPostSerializer, PeerCodeShareSerializer, CodeLikeSerializer,
    GroupChallengeSerializer, ChallengeParticipationSerializer,
    MentorshipRelationshipSerializer, MentorshipSessionSerializer,
    CollaborationOverviewSerializer, StudyGroupListSerializer, UserListSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only owners to edit their objects"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', obj.user) == request.user

class StudyGroupViewSet(viewsets.ModelViewSet):
    """ViewSet for StudyGroup model"""
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'description', 'subject_area']
    filterset_fields = ['subject_area', 'level', 'is_public']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return study groups based on user permissions"""
        user = self.request.user
        if user.is_authenticated:
            # Include groups user is a member of, plus public groups
            return StudyGroup.objects.filter(
                Q(memberships__user=user) | Q(is_public=True)
            ).distinct().prefetch_related('memberships')
        return StudyGroup.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        """Set the creator when creating a study group"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        """Join a study group"""
        study_group = self.get_object()
        user = request.user
        
        # Check if already a member
        if study_group.memberships.filter(user=user).exists():
            return Response(
                {'error': 'Already a member of this study group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if group is full
        if study_group.memberships.count() >= study_group.max_members:
            return Response(
                {'error': 'Study group is full'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        membership = StudyGroupMembership.objects.create(
            study_group=study_group,
            user=user,
            role='member'
        )
        
        # Create discussion forum if it doesn't exist
        DiscussionForum.objects.get_or_create(study_group=study_group)
        
        return Response(
            {'message': 'Successfully joined study group'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        """Leave a study group"""
        study_group = self.get_object()
        user = request.user
        
        membership = study_group.memberships.filter(user=user).first()
        if not membership:
            return Response(
                {'error': 'Not a member of this study group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent group creator from leaving (or require special handling)
        if study_group.created_by == user:
            return Response(
                {'error': 'Group creator cannot leave the group'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.delete()
        return Response(
            {'message': 'Successfully left study group'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get study group members"""
        study_group = self.get_object()
        memberships = study_group.memberships.select_related('user').all()
        serializer = StudyGroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

class DiscussionTopicViewSet(viewsets.ModelViewSet):
    """ViewSet for DiscussionTopic model"""
    queryset = DiscussionTopic.objects.all()
    serializer_class = DiscussionTopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['status', 'is_pinned']
    ordering_fields = ['created_at', 'title']
    ordering = ['-is_pinned', '-created_at']
    
    def get_queryset(self):
        """Return topics based on user's study group memberships"""
        user = self.request.user
        if user.is_authenticated:
            return DiscussionTopic.objects.filter(
                forum__study_group__memberships__user=user
            ).select_related('forum', 'forum__study_group', 'author')
        return DiscussionTopic.objects.none()
    
    def perform_create(self, serializer):
        """Set the author when creating a topic"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pin(self, request, pk=None):
        """Pin/unpin a topic"""
        topic = self.get_object()
        topic.is_pinned = not topic.is_pinned
        topic.save()
        return Response(
            {'message': f'Topic {"pinned" if topic.is_pinned else "unpinned"}'},
            status=status.HTTP_200_OK
        )

class DiscussionPostViewSet(viewsets.ModelViewSet):
    """ViewSet for DiscussionPost model"""
    queryset = DiscussionPost.objects.all()
    serializer_class = DiscussionPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['content']
    
    def get_queryset(self):
        """Return posts based on user's study group memberships"""
        user = self.request.user
        if user.is_authenticated:
            return DiscussionPost.objects.filter(
                topic__forum__study_group__memberships__user=user
            ).select_related('topic', 'topic__forum', 'topic__forum__study_group', 'author')
        return DiscussionPost.objects.none()
    
    def perform_create(self, serializer):
        """Set the author when creating a post"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_solution(self, request, pk=None):
        """Mark post as solution (only topic author can do this)"""
        post = self.get_object()
        
        if post.topic.author != request.user:
            return Response(
                {'error': 'Only the topic author can mark solutions'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Remove solution mark from other posts in the topic
        post.topic.posts.filter(is_solution=True).update(is_solution=False)
        
        # Mark this post as solution
        post.is_solution = True
        post.save()
        
        return Response(
            {'message': 'Post marked as solution'},
            status=status.HTTP_200_OK
        )

class PeerCodeShareViewSet(viewsets.ModelViewSet):
    """ViewSet for PeerCodeShare model"""
    queryset = PeerCodeShare.objects.all()
    serializer_class = PeerCodeShareSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description', 'tags']
    filterset_fields = ['language', 'share_type', 'is_public', 'is_tutorial']
    ordering_fields = ['created_at', 'title', 'likes_count', 'views_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return code shares based on user's study group memberships or public visibility"""
        user = self.request.user
        if user.is_authenticated:
            return PeerCodeShare.objects.filter(
                Q(is_public=True) | Q(study_group__memberships__user=user) | Q(author=user)
            ).distinct().select_related('author').prefetch_related('likes')
        return PeerCodeShare.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        """Set the author when creating a code share"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like/unlike a code share"""
        code_share = self.get_object()
        user = request.user
        
        like, created = CodeLike.objects.get_or_create(
            code_share=code_share,
            user=user
        )
        
        if not created:
            like.delete()
            code_share.likes_count = max(0, code_share.likes_count - 1)
            message = 'Unliked'
        else:
            code_share.likes_count += 1
            message = 'Liked'
        
        code_share.save()
        
        return Response(
            {'message': message, 'likes_count': code_share.likes_count},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Increment download count"""
        code_share = self.get_object()
        code_share.downloads_count += 1
        code_share.save()
        
        return Response(
            {'downloads_count': code_share.downloads_count},
            status=status.HTTP_200_OK
        )

class GroupChallengeViewSet(viewsets.ModelViewSet):
    """ViewSet for GroupChallenge model"""
    queryset = GroupChallenge.objects.all()
    serializer_class = GroupChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['challenge_type', 'difficulty_level', 'status']
    ordering_fields = ['start_date', 'title']
    ordering = ['-start_date']
    
    def get_queryset(self):
        """Return challenges based on user's study group memberships"""
        user = self.request.user
        if user.is_authenticated:
            return GroupChallenge.objects.filter(
                study_group__memberships__user=user
            ).select_related('study_group', 'created_by')
        return GroupChallenge.objects.none()
    
    def perform_create(self, serializer):
        """Set the creator when creating a challenge"""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def participate(self, request, pk=None):
        """Participate in a challenge"""
        challenge = self.get_object()
        user = request.user
        
        # Check if already participating
        if challenge.participations.filter(participant=user).exists():
            return Response(
                {'error': 'Already participating in this challenge'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if challenge is full
        if challenge.max_participants:
            current_participants = challenge.participations.count()
            if current_participants >= challenge.max_participants:
                return Response(
                    {'error': 'Challenge is full'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create participation
        participation = ChallengeParticipation.objects.create(
            challenge=challenge,
            participant=user,
            status='registered'
        )
        
        return Response(
            {'message': 'Successfully registered for challenge'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get challenge participants"""
        challenge = self.get_object()
        participations = challenge.participations.select_related('participant').all()
        serializer = ChallengeParticipationSerializer(participations, many=True)
        return Response(serializer.data)

class ChallengeParticipationViewSet(viewsets.ModelViewSet):
    """ViewSet for ChallengeParticipation model"""
    queryset = ChallengeParticipation.objects.all()
    serializer_class = ChallengeParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return participations for authenticated user"""
        return ChallengeParticipation.objects.filter(
            participant=self.request.user
        ).select_related('challenge', 'challenge__study_group')
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit challenge solution"""
        participation = self.get_object()
        
        submission_content = request.data.get('submission_content', '')
        code_files = request.data.get('code_files', [])
        
        participation.submission_content = submission_content
        participation.code_files = code_files
        participation.status = 'submitted'
        participation.submitted_at = timezone.now()
        participation.save()
        
        return Response(
            {'message': 'Challenge submission successful'},
            status=status.HTTP_200_OK
        )

class MentorshipRelationshipViewSet(viewsets.ModelViewSet):
    """ViewSet for MentorshipRelationship model"""
    queryset = MentorshipRelationship.objects.all()
    serializer_class = MentorshipRelationshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        """Return relationships where user is mentor or mentee"""
        return MentorshipRelationship.objects.filter(
            Q(mentor=self.request.user) | Q(mentee=self.request.user)
        ).select_related('mentor', 'mentee')
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a mentorship relationship (for mentees)"""
        relationship = self.get_object()
        
        if relationship.mentee != request.user:
            return Response(
                {'error': 'Only the mentee can accept this relationship'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        relationship.status = 'active'
        relationship.started_at = timezone.now()
        relationship.save()
        
        return Response(
            {'message': 'Mentorship relationship activated'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a mentorship relationship"""
        relationship = self.get_object()
        
        if request.user not in [relationship.mentor, relationship.mentee]:
            return Response(
                {'error': 'Only participants can complete this relationship'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        relationship.status = 'completed'
        relationship.ended_at = timezone.now()
        relationship.save()
        
        return Response(
            {'message': 'Mentorship relationship completed'},
            status=status.HTTP_200_OK
        )

class MentorshipSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for MentorshipSession model"""
    queryset = MentorshipSession.objects.all()
    serializer_class = MentorshipSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'session_type']
    ordering_fields = ['scheduled_start']
    ordering = ['-scheduled_start']
    
    def get_queryset(self):
        """Return sessions for user's mentorship relationships"""
        return MentorshipSession.objects.filter(
            relationship__mentor=self.request.user
        ).union(
            MentorshipSession.objects.filter(
                relationship__mentee=self.request.user
            )
        ).select_related('relationship', 'relationship__mentor', 'relationship__mentee')
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a mentorship session"""
        session = self.get_object()
        
        if request.user not in [session.relationship.mentor, session.relationship.mentee]:
            return Response(
                {'error': 'Only relationship participants can start this session'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        session.actual_start = timezone.now()
        session.status = 'in_progress'
        session.save()
        
        return Response(
            {'message': 'Session started'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a mentorship session"""
        session = self.get_object()
        
        if request.user not in [session.relationship.mentor, session.relationship.mentee]:
            return Response(
                {'error': 'Only relationship participants can complete this session'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        session.actual_end = timezone.now()
        session.status = 'completed'
        session.notes = request.data.get('notes', session.notes)
        session.action_items = request.data.get('action_items', session.action_items)
        session.save()
        
        return Response(
            {'message': 'Session completed'},
            status=status.HTTP_200_OK
        )

# Dashboard/Overview endpoint
class CollaborationOverviewViewSet(viewsets.ViewSet):
    """ViewSet for collaboration overview/dashboard"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get collaboration overview statistics"""
        user = request.user
        
        # Get user's study groups
        user_study_groups = StudyGroup.objects.filter(memberships__user=user)
        
        # Get collaboration statistics
        stats = {
            'total_study_groups': StudyGroup.objects.count(),
            'active_discussions': DiscussionTopic.objects.filter(
                forum__study_group__memberships__user=user
            ).count(),
            'code_shares': PeerCodeShare.objects.filter(
                Q(is_public=True) | Q(study_group__memberships__user=user)
            ).count(),
            'active_challenges': GroupChallenge.objects.filter(
                study_group__memberships__user=user,
                status='active'
            ).count(),
            'active_mentorships': MentorshipRelationship.objects.filter(
                Q(mentor=user) | Q(mentee=user),
                status='active'
            ).count(),
            'my_study_groups': user_study_groups.count(),
            'my_posts': DiscussionPost.objects.filter(
                author=user
            ).count(),
            'my_code_shares': PeerCodeShare.objects.filter(author=user).count(),
        }
        
        serializer = CollaborationOverviewSerializer(stats)
        return Response(serializer.data)