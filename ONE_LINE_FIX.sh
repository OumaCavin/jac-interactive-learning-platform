#!/bin/bash
# Ultra-simple fix for missing static directories

echo "Creating missing static directories and collecting files..."

# Create static directory structure
docker-compose exec backend bash -c "
    mkdir -p /app/static/admin/css &&
    echo '✅ Created static directory structure' &&
    python manage.py collectstatic --noinput &&
    echo '✅ Collected static files' &&
    chown -R jac:jac /app/static/ &&
    echo '✅ Fixed permissions'
"

# Restart backend
echo "Restarting backend..."
docker-compose restart backend

# Wait and test
echo "Waiting for backend to start..."
sleep 10

echo "Testing static files..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css 2>/dev/null)

if [ "$response" = "200" ]; then
    echo "✅ SUCCESS! dashboard.css is now accessible"
    echo "🎯 Admin interface should work now. Try: http://localhost:8000/admin/"
else
    echo "❌ FAILED: dashboard.css returns HTTP $response"
    echo "Run DIAGNOSE_ADMIN_STATIC.sh for detailed diagnostics"
fi