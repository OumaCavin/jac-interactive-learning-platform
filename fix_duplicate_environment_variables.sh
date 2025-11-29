#!/bin/bash

# Fix environment variables in duplicate directory
# This script applies all the environment variable fixes to the jac-interactive-learning-platform duplicate

echo "🔧 Applying environment variable fixes to duplicate directory..."

# Fix initialize_platform.py
echo "📝 Fixing initialize_platform.py..."
sed -i 's|self.style.SUCCESS(f'"'"'Admin URL: http://localhost:8000/admin/'"'"')|# Get environment variables for URLs\n        import os\n        backend_host = os.environ.get('"'"'BACKEND_HOST'"'"', '"'"'localhost'"'"')\n        backend_port = os.environ.get('"'"'BACKEND_PORT'"'"', '"'"'8000'"'"')\n        protocol = '"'"'https'"'"' if os.environ.get('"'"'USE_HTTPS'"'"', '"'"'false'"'"').lower() == '"'"'true'"'"' else '"'"'http'"'"'\n        \n        admin_url = f"{protocol}://{backend_host}:{backend_port}/admin/"\n        api_url = f"{protocol}://{backend_host}:{backend_port}/api/"\n        \n        self.stdout.write(\n            self.style.SUCCESS(f'"'"'Admin URL: {admin_url}'"'"')\n        )|g' /workspace/jac-interactive-learning-platform/backend/apps/management/commands/initialize_platform.py

sed -i 's|self.style.SUCCESS(f'"'"'API URL: http://localhost:8000/api/'"'"')|            self.style.SUCCESS(f'"'"'API URL: {api_url}'"'"')\n        )|g' /workspace/jac-interactive-learning-platform/backend/apps/management/commands/initialize_platform.py

# Fix populate_jac_curriculum.py
echo "📝 Fixing populate_jac_curriculum.py..."
sed -i "s|'  Or use Django admin at http://localhost:8000/admin/'|f'  Or use Django admin at {backend_url}/admin/'|g" /workspace/jac-interactive-learning-platform/backend/apps/learning/management/commands/populate_jac_curriculum.py
sed -i 's|print("See: http://localhost:8000/admin/ or http://localhost:3000/register");|# Get environment variables for URLs\n    import os\n    backend_host = os.environ.get('"'"'BACKEND_HOST'"'"', '"'"'localhost'"'"')\n    backend_port = os.environ.get('"'"'BACKEND_PORT'"'"', '"'"'8000'"'"')\n    frontend_host = os.environ.get('"'"'FRONTEND_HOST'"'"', '"'"'localhost'"'"')\n    frontend_port = os.environ.get('"'"'FRONTEND_PORT'"'"', '"'"'3000'"'"')\n    protocol = '"'"'https'"'"' if os.environ.get('"'"'USE_HTTPS'"'"', '"'"'false'"'"').lower() == '"'"'true'"'"' else '"'"'http'"'"'\n    \n    backend_url = f"{protocol}://{backend_host}:{backend_port}"\n    frontend_url = f"{protocol}://{frontend_host}:{frontend_port}"\n    \n    print(f"See: {backend_url}/admin/ or {frontend_url}/register");|g' /workspace/jac-interactive-learning-platform/backend/apps/learning/management/commands/populate_jac_curriculum.py

# Fix backend settings
echo "📝 Fixing backend config settings..."
sed -i 's|CORS_ALLOWED_ORIGINS = \[|"CORS_ALLOWED_ORIGINS = config(\n    '"'"'CORS_ALLOWED_ORIGINS'"'"', \n    default='"'"'http://localhost:3000,http://127.0.0.1:3000'"'"',\n    cast=lambda v: [s.strip() for s in v.split('"'"','"'"')]\n)|g' /workspace/jac-interactive-learning-platform/backend/config/settings.py
sed -i '/CORS_ALLOW_ALL_ORIGINS/,/CORS_ALLOWED_ORIGINS/c\\n# CORS Configuration\nCORS_ALLOW_ALL_ORIGINS = config('"'"'CORS_ALLOW_ALL_ORIGINS'"'"', default=True, cast=bool)\nCORS_ALLOWED_ORIGINS = config(\n    '"'"'CORS_ALLOWED_ORIGINS'"'"', \n    default='"'"'http://localhost:3000,http://127.0.0.1:3000'"'"',\n    cast=lambda v: [s.strip() for s in v.split('"'"','"'"')]\n)' /workspace/jac-interactive-learning-platform/backend/config/settings.py

sed -i '/CORS_ALLOW_ALL_ORIGINS/,/CORS_ALLOWED_ORIGINS/c\\n# CORS Configuration\nCORS_ALLOW_ALL_ORIGINS = config('"'"'CORS_ALLOW_ALL_ORIGINS'"'"', default=True, cast=bool)\nCORS_ALLOWED_ORIGINS = config(\n    '"'"'CORS_ALLOWED_ORIGINS'"'"', \n    default='"'"'http://localhost:3000,http://127.0.0.1:3000'"'"',\n    cast=lambda v: [s.strip() for s in v.split('"'"','"'"')]\n)' /workspace/jac-interactive-learning-platform/backend/config/settings_minimal.py

# Fix test_predictive_analytics.py
echo "📝 Fixing test_predictive_analytics.py..."
sed -i 's|base_url = "http://localhost:8000"|base_url = os.environ.get('"'"'TEST_API_URL'"'"', '"'"'http://localhost:8000'"'"')|g' /workspace/jac-interactive-learning-platform/backend/test_predictive_analytics.py
sed -i 's|print("4. Check API endpoints at http://localhost:8000/api/v1/predict/")|print(f"4. Check API endpoints at {base_url}/api/v1/predict/")|g' /workspace/jac-interactive-learning-platform/backend/test_predictive_analytics.py

# Fix documentation
echo "📝 Fixing documentation..."
sed -i 's|const ws = new WebSocket('"'"'ws://localhost:8000/ws/dashboard/'"'"');|const ws = new WebSocket(`ws://${window.location.host}/ws/dashboard/`);|g' /workspace/jac-interactive-learning-platform/backend/docs/REAL_TIME_MONITORING_GUIDE.md

# Remove hardcoded proxy from package.json
echo "📝 Fixing package.json proxy..."
sed -i '/"proxy": "http:\/\/localhost:8000"/d' /workspace/jac-interactive-learning-platform/frontend/package.json

echo "✅ Environment variable fixes applied to duplicate directory!"
echo ""
echo "🔍 Summary of changes:"
echo "  - Backend management commands now use environment variables for URLs"
echo "  - CORS configuration now environment-driven"
echo "  - Test files use environment variables"
echo "  - Documentation uses dynamic URLs"
echo "  - Frontend proxy configuration updated"
echo ""
echo "📋 New environment variables available:"
echo "  - BACKEND_HOST, BACKEND_PORT"
echo "  - FRONTEND_HOST, FRONTEND_PORT"
echo "  - USE_HTTPS"
echo "  - TEST_API_URL"
echo "  - REACT_APP_API_URL"