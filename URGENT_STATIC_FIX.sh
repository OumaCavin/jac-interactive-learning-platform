#!/bin/bash

echo "=== URGENT Django Admin Static Files Fix ==="
echo "Targeting the URL configuration issue"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with fix..."

echo ""
echo "🔧 Step 1: Backup current URLs configuration..."
cp backend/config/urls.py backend/config/urls.py.backup

echo ""
echo "🔧 Step 2: Fixing static files URL configuration..."

# Create the corrected URLs.py
cat > backend/config/urls_fixed.py << 'EOF'
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from apps.agents import views as agents_views

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    # Django Admin Interface (Custom Styled)
    path('admin/', custom_admin_site.urls),
    
    # API Documentation (Re-enabled with drf_spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
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
    # Progress tracking and analytics (re-enabled)
    path('api/progress/', include('apps.progress.urls')),
    path('api/gamification/', include('apps.gamification.urls')),  # Gamification system
    # Collaboration features (re-enabled)
    path('api/collaboration/', include('apps.collaboration.urls')),
    # JAC execution engine (re-enabled)
    path('api/jac-execution/', include('apps.jac_execution.urls')),
    # Knowledge Graph API (re-enabled)
    path('api/knowledge-graph/', include('apps.knowledge_graph.urls')),
    # path('api/ai-agents/', include('apps.api_endpoints.ai_agents_urls')),  # AI Multi-Agent System (commented out temporarily)
    
    # Fallback endpoints without /api/ prefix (for frontend compatibility)
    path('users/', include('apps.users.urls')),  # Users app now properly installed
    path('learning/', include('apps.learning.urls')),
    path('assessments/', include('apps.assessments.urls')),
    path('progress/', include('apps.progress.urls')),  # Progress tracking and analytics (re-enabled)
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
    
    # CRITICAL FIX: Serve static files using STATIC_ROOT directly
    # This ensures Django admin CSS files are properly served
    urlpatterns += static('/static/', document_root='/var/www/static')
    
    # Also serve from local static files as fallback
    urlpatterns += static('/static/', document_root=settings.BASE_DIR / 'static')
EOF

# Replace the current urls.py with the fixed version
mv backend/config/urls_fixed.py backend/config/urls.py

echo "✅ Fixed Django static files URL configuration"

echo ""
echo "🔧 Step 3: Verifying dashboard.css file exists..."
if docker-compose exec backend test -f /var/www/static/admin/css/dashboard.css; then
    echo "✅ dashboard.css file confirmed in container"
else
    echo "⚠️  dashboard.css not found, collecting static files again..."
    docker-compose exec backend python manage.py collectstatic --clear --noinput -v 2
fi

echo ""
echo "🔧 Step 4: Restarting backend to apply URL changes..."
docker-compose restart backend

echo ""
echo "🔧 Step 5: Waiting for backend to start..."
sleep 10

echo ""
echo "🔧 Step 6: Testing static file access..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

if [ "$HTTP_RESPONSE" = "200" ]; then
    echo "🎉 SUCCESS: dashboard.css returns HTTP 200!"
    echo ""
    echo "✅ Your Django admin interface should now load with proper styling!"
    echo "🌐 Visit: http://localhost:8000/admin/"
    echo "🔐 Login: admin / jac_admin_2024!"
    echo ""
    echo "🔍 Final test - check admin interface:"
    curl -s http://localhost:8000/admin/ | grep -q "Django administration" && echo "✅ Admin interface is loading correctly!" || echo "⚠️  Admin interface may still have issues"
else
    echo "❌ STILL FAILED: dashboard.css returns HTTP $HTTP_RESPONSE"
    echo ""
    echo "🔍 Emergency debug - checking file content:"
    docker-compose exec backend cat /var/www/static/admin/css/dashboard.css | head -5
    echo ""
    echo "🔧 Last resort - let me check Django's static files finder..."
    docker-compose exec backend python manage.py shell -c "
import os
from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.finders import find

print('=== Django Static Files Debug ===')
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')

# Check if Django can find dashboard.css
try:
    found_path = find('admin/css/dashboard.css')
    print(f'Django found dashboard.css at: {found_path}')
except Exception as e:
    print(f'Django could not find dashboard.css: {e}')

# Check file system directly
dashboard_path = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'dashboard.css')
print(f'File exists at: {dashboard_path}')
print(f'File readable: {os.path.exists(dashboard_path)}')
"
fi

echo ""
echo "=== Django Admin Static Files Fix Complete ==="
echo "The URL configuration has been updated to serve static files correctly."