"""
URL Configuration for AI Multi-Agent System

Routes URLs for AI agent interactions and multi-agent collaboration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .knowledge_graph_api import AIAgentAPIViewSet

# Create router for ViewSets
router = DefaultRouter()
router.register(r'ai-agents', AIAgentAPIViewSet, basename='ai-agents')

app_name = 'ai_agents'

urlpatterns = [
    # Main API routes
    path('api/', include(router.urls)),
]