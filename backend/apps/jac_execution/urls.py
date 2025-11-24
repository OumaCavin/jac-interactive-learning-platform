"""
URL Configuration for JAC Code Execution API

This module defines the URL patterns for all code execution endpoints,
including execution views, templates, sessions, and security settings.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CodeExecutionViewSet,
    ExecutionTemplateViewSet,
    CodeExecutionSessionViewSet,
    SecuritySettingsViewSet,
    QuickExecutionView,
    ExecutionStatusView,
    LanguageSupportView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'executions', CodeExecutionViewSet, basename='execution')
router.register(r'templates', ExecutionTemplateViewSet, basename='template')
router.register(r'sessions', CodeExecutionSessionViewSet, basename='session')
router.register(r'security', SecuritySettingsViewSet, basename='security')

app_name = 'jac_execution'

urlpatterns = [
    # Main API routes
    path('api/', include(router.urls)),
    
    # Standalone views
    path('api/quick-execute/', QuickExecutionView.as_view(), name='quick-execute'),
    path('api/execution/<uuid:execution_id>/', ExecutionStatusView.as_view(), name='execution-status'),
    path('api/languages/', LanguageSupportView.as_view(), name='language-support'),
]