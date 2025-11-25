"""
Collaboration URLs - JAC Learning Platform

URL routing for collaboration features.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()
router.register(r'study-groups', views.StudyGroupViewSet, basename='studygroup')
router.register(r'discussion-topics', views.DiscussionTopicViewSet, basename='discussiontopic')
router.register(r'discussion-posts', views.DiscussionPostViewSet, basename='discussionpost')
router.register(r'code-shares', views.PeerCodeShareViewSet, basename='peercodeshare')
router.register(r'challenges', views.GroupChallengeViewSet, basename='groupchallenge')
router.register(r'participations', views.ChallengeParticipationViewSet, basename='challengeparticipation')
router.register(r'mentorships', views.MentorshipRelationshipViewSet, basename='mentorshiprelationship')
router.register(r'sessions', views.MentorshipSessionViewSet, basename='mentorshipsession')
router.register(r'overview', views.CollaborationOverviewViewSet, basename='collaborationoverview')

urlpatterns = [
    # API endpoints will be registered via router
    # The router will create URLs like:
    # /api/collaboration/study-groups/
    # /api/collaboration/study-groups/{id}/join/
    # /api/collaboration/overview/overview/
    path('', include(router.urls)),
]