"""
URL Configuration for Agents App

URL patterns for agent management, workflows, and system orchestration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'agents', views.AgentViewSet, basename='agent')
router.register(r'tasks', views.TaskViewSet, basename='task')
# router.register(r'communications', views.AgentCommunicationViewSet, basename='communication')
router.register(r'metrics', views.AgentMetricsViewSet, basename='metric')
# router.register(r'sessions', views.LearningSessionViewSet, basename='session')

app_name = 'agents'

urlpatterns = [
    # Health check endpoint for Docker health checks
    path('health/', views.system_health_check, name='system_health'),
    
    # API Views
    path('workflow/', views.AgentWorkflowAPIView.as_view(), name='workflow'),
    path('coordinate/', views.AgentCoordinationAPIView.as_view(), name='coordinate'),
    path('monitor/', views.AgentSystemMonitorAPIView.as_view(), name='monitor'),
    path('emergency/', views.AgentEmergencyAPIView.as_view(), name='emergency'),
    path('load-distribution/', views.AgentLoadDistributionAPIView.as_view(), name='load-distribution'),
    path('validate/', views.AgentWorkflowValidationAPIView.as_view(), name='validate'),
    path('lifecycle/', views.AgentLifecycleAPIView.as_view(), name='lifecycle'),
    
    # Chat Assistant Endpoints
    path('chat-assistant/message/', views.ChatAssistantAPIView.as_view(), name='chat-message'),
    path('chat-assistant/history/', views.ChatAssistantAPIView.as_view(), name='chat-history'),
    path('chat-assistant/rate/<uuid:message_id>/', views.RateChatMessageAPIView.as_view(), name='chat-rate'),
    path('chat-assistant/sessions/', views.ChatSessionListAPIView.as_view(), name='chat-sessions'),
    
    # Include router URLs
    path('', include(router.urls)),
]