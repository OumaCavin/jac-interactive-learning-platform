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
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from apps.agents import views as agents_views

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Health Check  
    path('api/health/', agents_views.system_health_check, name='health_check'),  # Direct health endpoint
    
    # Super simple health check (no Django dependencies)
    path('api/health/static/', lambda request: JsonResponse({
        'status': 'healthy',
        'message': 'Backend service is active',
        'service': 'jac-interactive-learning-platform',
        'timestamp': timezone.now().isoformat()
    }, content_type='application/json'), name='static_health_check'),
    
    # Fallback simple health check
    path('api/health/simple/', lambda request: JsonResponse({
        'status': 'healthy',
        'message': 'Backend is running',
        'service': 'jac-interactive-learning-platform'
    }), name='simple_health_check'),
    
    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/learning/', include('apps.learning.urls')),
    path('api/agents/', include('apps.agents.urls')),
    
    # Include router URLs (if any app registers viewsets)
    path('api/', include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)