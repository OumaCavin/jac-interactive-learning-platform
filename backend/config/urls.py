# JAC Platform Configuration - Settings by Cavin Otieno

"""
Main URL Configuration for JAC Learning Platform

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import admin
from .custom_admin import custom_admin_site
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
# )
from apps.agents import views as agents_views

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    # Django Admin Interface (Custom Styled)
    path('admin/', custom_admin_site.urls),
    
    # API Documentation (Commented out - requires drf_spectacular)
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Health Check  
    path('api/health/', agents_views.system_health_check, name='health_check'),  # Direct health endpoint
    
    # Super simple health check (no Django dependencies) - Optimized to reduce calls
    path('api/health/static/', lambda request: JsonResponse({
        'status': 'healthy',
        'message': 'Backend service is active',
        'service': 'jac-interactive-learning-platform',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    }, content_type='application/json'), name='static_health_check'),
    
    # Fallback simple health check
    path('api/health/simple/', lambda request: JsonResponse({
        'status': 'healthy',
        'message': 'Backend is running',
        'service': 'jac-interactive-learning-platform'
    }), name='simple_health_check'),
    
    # API endpoints with /api/ prefix (primary)
    path('api/users/', include('apps.users.urls')),  # Users app now properly installed
    path('api/learning/', include('apps.learning.urls')),
    path('api/content/', include('apps.content.urls')),
    path('api/agents/', include('apps.agents.urls')),
    path('api/assessments/', include('apps.assessments.urls')),
    # path('api/progress/', include('apps.progress.urls')),  # Progress tracking and analytics (temporarily disabled)
    path('api/gamification/', include('apps.gamification.urls')),  # Gamification system
    path('api/collaboration/', include('apps.collaboration.urls')),  # Collaboration features
    path('api/jac-execution/', include('apps.jac_execution.urls')),  # JAC execution engine
    path('api/knowledge-graph/', include('apps.knowledge_graph.urls')),  # Knowledge Graph API
    # path('api/ai-agents/', include('apps.api_endpoints.ai_agents_urls')),  # AI Multi-Agent System (commented out temporarily)
    
    # Fallback endpoints without /api/ prefix (for frontend compatibility)
    path('users/', include('apps.users.urls')),  # Users app now properly installed
    path('learning/', include('apps.learning.urls')),
    path('assessments/', include('apps.assessments.urls')),
    # path('progress/', include('apps.progress.urls')),  # Progress tracking and analytics (temporarily disabled)
    # Note: jac_execution URLs included only once to avoid namespace conflicts
    # Note: agents endpoints are only available via /api/agents/ to avoid namespace conflicts
    
    # Health check endpoints without /api/ prefix
    path('health/static/', lambda request: JsonResponse({
        'status': 'healthy',
        'message': 'Backend service is active',
        'service': 'jac-interactive-learning-platform',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0'
    }, content_type='application/json'), name='static_health_check_no_prefix'),
    
    # Include router URLs (if any app registers viewsets)
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from the local static directory in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')