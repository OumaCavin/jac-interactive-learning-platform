#!/bin/bash

echo "=== Django Admin Static Files Diagnostic ==="
echo "This script will help identify the root cause of static file 404 errors"
echo

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the jac-interactive-learning-platform directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

echo "✅ Found docker-compose.yml - running diagnostics..."
echo

# 1. Check Django static configuration
echo "🔍 1. Checking Django static files configuration..."
echo "----------------------------------------"
docker-compose exec backend python manage.py shell -c "
from django.conf import settings
print('STATIC_URL:', settings.STATIC_URL)
print('STATIC_ROOT:', settings.STATIC_ROOT)
print('STATIC_ROOT exists:', settings.STATIC_ROOT and __import__('os').path.exists(settings.STATIC_ROOT))
"
echo

# 2. Check static directory structure
echo "🔍 2. Checking static directory structure..."
echo "----------------------------------------"
echo "Static root directory:"
docker-compose exec backend ls -la /app/static/ 2>/dev/null || echo "❌ /app/static/ directory does not exist"

echo
echo "Admin static directory:"
docker-compose exec backend ls -la /app/static/admin/ 2>/dev/null || echo "❌ /app/static/admin/ directory does not exist"

echo
echo "Admin CSS directory:"
docker-compose exec backend ls -la /app/static/admin/css/ 2>/dev/null || echo "❌ /app/static/admin/css/ directory does not exist"
echo

# 3. Check what static files are available
echo "🔍 3. Checking installed Django apps and their static files..."
echo "----------------------------------------"
docker-compose exec backend python manage.py collectstatic --dry-run --verbosity=1
echo

# 4. Test static file serving
echo "🔍 4. Testing static file URLs..."
echo "----------------------------------------"
echo "Testing main static URL:"
curl -I http://localhost:8000/static/ 2>/dev/null || echo "❌ Static root URL not accessible"

echo
echo "Testing admin CSS URL:"
curl -I http://localhost:8000/static/admin/css/dashboard.css 2>/dev/null || echo "❌ Admin CSS URL not accessible"

# 5. Check backend logs for static file errors
echo
echo "🔍 5. Recent backend logs (last 10 lines)..."
echo "----------------------------------------"
docker-compose logs --tail=10 backend
echo

echo "=== Diagnostic Complete ==="
echo
echo "Based on the output above, common issues and solutions:"
echo
echo "❌ If STATIC_ROOT does not exist:"
echo "   → Run: docker-compose exec backend python manage.py collectstatic --noinput"
echo
echo "❌ If /app/static/admin/css/ is missing:"
echo "   → Run: docker-compose exec backend mkdir -p /app/static/admin/css"
echo "   → Then run collectstatic again"
echo
echo "❌ If dashboard.css returns 404:"
echo "   → Run: docker-compose restart backend"
echo "   → Wait 10 seconds, then test again"
echo
echo "❌ If custom admin site issues:"
echo "   → Check that backend/config/urls.py uses custom_admin_site.urls"
echo "   → Verify INSTALLED_APPS includes 'django.contrib.admin'"