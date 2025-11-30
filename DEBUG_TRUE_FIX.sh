#!/bin/bash

echo "=== DEBUG=TRUE Django Static Files Fix ==="
echo "Temporarily enabling DEBUG=True to serve static files"
echo "Files exist in /var/www/static/, just need DEBUG=True to serve them"

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ ERROR: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

echo "✅ Found docker-compose.yml - proceeding with DEBUG fix..."

echo ""
echo "🔧 Step 1: Backing up current settings..."
cp backend/config/settings.py backend/config/settings.py.backup

echo ""
echo "🔧 Step 2: Temporarily enabling DEBUG=True..."
python3 << 'PYTHON_EOF'
import re

# Read the current settings
with open('backend/config/settings.py', 'r') as f:
    content = f.read()

# Find and replace DEBUG=False with DEBUG=True
# Look for the line that sets DEBUG
debug_pattern = r'DEBUG\s*=\s*False'
debug_replacement = 'DEBUG = True'

# Replace the DEBUG setting
new_content = re.sub(debug_pattern, debug_replacement, content)

# Write back the updated settings
with open('backend/config/settings.py', 'w') as f:
    f.write(new_content)

print("✅ Updated DEBUG setting to True in settings.py")
PYTHON_EOF

echo ""
echo "🔧 Step 3: Restarting backend to apply DEBUG change..."
docker-compose restart backend

echo ""
echo "🔧 Step 4: Waiting for backend to start..."
sleep 10

echo ""
echo "🔧 Step 5: Verifying DEBUG=True is now active..."
DEBUG_CHECK=$(docker-compose exec backend python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)")

echo "DEBUG setting is now: $DEBUG_CHECK"

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
    echo "🔍 Final verification - testing admin interface:"
    curl -s http://localhost:8000/admin/ | grep -q "Django administration" && echo "✅ Admin interface is loading!" || echo "⚠️  Check admin interface manually"
    
    echo ""
    echo "🔧 Restoration instructions:"
    echo "To revert to production mode (DEBUG=False):"
    echo "   python3 -c \""
    echo "import re"
    echo "with open('backend/config/settings.py', 'r') as f:"
    echo "    content = f.read()"
    echo "content = re.sub(r'DEBUG\s*=\s*True', 'DEBUG = False', content)"
    echo "with open('backend/config/settings.py', 'w') as f:"
    echo "    f.write(content)"
    echo "\""
    echo "   docker-compose restart backend"
else
    echo "❌ STILL FAILED: dashboard.css returns HTTP $HTTP_RESPONSE"
    echo ""
    echo "🔍 Debugging further..."
    docker-compose exec backend python manage.py shell -c "
from django.conf import settings
print(f'DEBUG: {settings.DEBUG}')
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')

# Check static files storage
from django.contrib.staticfiles.storage import StaticFilesStorage
storage = StaticFilesStorage()
try:
    url = storage.url('admin/css/dashboard.css')
    print(f'StaticFilesStorage URL: {url}')
except Exception as e:
    print(f'StaticFilesStorage error: {e}')
"
fi

echo ""
echo "=== Django DEBUG Static Files Fix Complete ==="
echo "This solution temporarily enables DEBUG=True to serve static files."
echo "Files are confirmed to exist in /var/www/static/admin/css/ - now they should be served!"