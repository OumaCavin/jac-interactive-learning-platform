#!/bin/bash

echo "=== Quick Restart Fix for Django Admin ==="
echo "This will restart the backend to apply settings changes"

# Restart backend container
docker-compose restart backend

# Wait for startup
echo "Waiting for backend to start..."
sleep 10

# Test dashboard.css access
echo "Testing dashboard.css access..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ SUCCESS: dashboard.css returns HTTP 200!"
    echo "🎉 Your Django admin interface should now work!"
    echo ""
    echo "Visit: http://localhost:8000/admin/"
    echo "Login: admin / jac_admin_2024!"
else
    echo "❌ FAILED: dashboard.css returns HTTP $HTTP_CODE"
    echo "You may need to pull from GitHub and run the full fix script."
fi