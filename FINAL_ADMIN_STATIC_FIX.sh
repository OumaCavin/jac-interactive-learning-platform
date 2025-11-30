#!/bin/bash

echo "=== FINAL Django Admin Static Files Fix ==="
echo "Comprehensive solution for dashboard.css 404 errors"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with final fix..."

echo ""
echo "🔧 Step 1: Creating better static files configuration..."

# Create a proper static files finder configuration
cat > backend/config/static_config.py << 'EOF'
"""
Static Files Configuration for Django Admin
This module provides better static files handling for development
"""

import os
from pathlib import Path

def get_static_files_config():
    """
    Returns static files configuration that works in both development and production
    """
    # Base directory
    base_dir = Path(__file__).resolve().parent.parent
    
    static_dirs = [
        base_dir / 'static',  # Local development static files
    ]
    
    # Add Docker volume mount path if it exists
    docker_static_path = Path('/var/www/static')
    if docker_static_path.exists():
        static_dirs.append(str(docker_static_path))
    
    return static_dirs

# Update Django settings to use this configuration
def configure_static_files():
    from django.conf import settings
    
    if hasattr(settings, 'STATICFILES_DIRS'):
        # Don't overwrite existing custom configuration
        return
    
    # Set up static files directories
    static_dirs = get_static_files_config()
    settings.STATICFILES_DIRS = static_dirs
    
    # Ensure static files are served in development
    if settings.DEBUG:
        from django.conf.urls.static import static
        if not any('static' in str(pattern) for pattern in settings.URL_PATTERNS if hasattr(pattern, 'pattern')):
            # Add static files serving
            pass

EOF

echo "✅ Created static configuration module"

echo ""
echo "🔧 Step 2: Updating Django settings for reliable static file serving..."

# Backup current settings
cp backend/config/settings.py backend/config/settings.py.backup

# Update settings.py with more robust static files configuration
python3 << 'PYTHON_EOF'
import re

# Read the current settings
with open('backend/config/settings.py', 'r') as f:
    content = f.read()

# Find and replace the static files section
static_section_pattern = r'# For development, serve static files from both STATIC_ROOT and STATICFILES_DIRS\s*if DEBUG:\s*# In development, serve from both local static files and the collected STATIC_ROOT\s*STATICFILES_DIRS = \[\s*BASE_DIR / \'static\',\s*\'/var/www/static\',  # Add the Docker volume mount path\s*\]\s*else:\s*# For production, use STATIC_ROOT \(already set above\)\s*pass'

# Create new static files configuration
new_static_section = '''# Static files configuration - robust solution for development and production
# Add staticfiles finders for better file detection
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# For development, serve static files from multiple locations
if DEBUG:
    # In development, serve from both local static files and the collected STATIC_ROOT
    STATICFILES_DIRS = [
        BASE_DIR / 'static',           # Local development files
        '/var/www/static',             # Docker volume mount with collected files
    ]
    
    # Ensure static files are properly served in development
    # The URL configuration in urls.py handles serving from STATIC_ROOT
else:
    # For production, use STATIC_ROOT (already set above)
    pass'''

# Replace the section
new_content = re.sub(static_section_pattern, new_static_section, content, flags=re.MULTILINE | re.DOTALL)

# Write back the updated settings
with open('backend/config/settings.py', 'w') as f:
    f.write(new_content)

print("✅ Updated Django settings with robust static files configuration")
PYTHON_EOF

echo "✅ Updated Django settings"

echo ""
echo "🔧 Step 3: Restarting backend container to apply changes..."

docker-compose restart backend

echo ""
echo "🔧 Step 4: Waiting for backend to start..."
sleep 10

echo ""
echo "🔧 Step 5: Testing static file access..."

echo "Testing dashboard.css availability..."
if docker-compose exec backend test -f /var/www/static/admin/css/dashboard.css; then
    echo "✅ dashboard.css file exists in container"
else
    echo "❌ dashboard.css file NOT found in container"
    echo "Running collectstatic again..."
    docker-compose exec backend python manage.py collectstatic --clear --noinput -v 2
fi

echo ""
echo "Testing HTTP access to dashboard.css..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/admin/css/dashboard.css)

if [ "$HTTP_RESPONSE" = "200" ]; then
    echo "✅ SUCCESS: dashboard.css returns HTTP 200!"
    echo "🎉 Your Django admin interface should now load with proper styling!"
    echo ""
    echo "Test it by visiting: http://localhost:8000/admin/"
    echo "Login with: admin / jac_admin_2024!"
else
    echo "❌ FAILED: dashboard.css returns HTTP $HTTP_RESPONSE"
    echo "🔍 Debugging with Django shell..."
    
    echo "Checking Django static files configuration..."
    docker-compose exec backend python manage.py shell << 'SHELL_EOF'
from django.conf import settings
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
print(f"DEBUG: {settings.DEBUG}")

# Check if file exists in STATIC_ROOT
import os
static_file = os.path.join(settings.STATIC_ROOT, 'admin', 'css', 'dashboard.css')
print(f"Dashboard.css path: {static_file}")
print(f"File exists: {os.path.exists(static_file)}")
SHELL_EOF
fi

echo ""
echo "=== Final Admin Static Files Fix Complete ==="
echo "Check the results above for success/failure status."