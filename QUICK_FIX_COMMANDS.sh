#!/bin/bash
# Quick manual fix commands - run these line by line if the automated script doesn't work

echo "=== MANUAL FIX COMMANDS ==="
echo "Run these commands one by one:"
echo
echo "# 1. Navigate to project directory"
echo "cd ~/projects/jac-interactive-learning-platform"
echo
echo "# 2. Collect static files"
echo "docker-compose exec backend python manage.py collectstatic --noinput"
echo
echo "# 3. Fix permissions"
echo "docker-compose exec backend chown -R jac:jac /app/static/"
echo
echo "# 4. Restart backend"
echo "docker-compose restart backend"
echo
echo "# 5. Wait for restart (10 seconds)"
echo "sleep 10"
echo
echo "# 6. Test static files"
echo "curl -I http://localhost:8000/static/admin/css/dashboard.css"
echo
echo "# 7. Check logs if issues persist"
echo "docker-compose logs --tail=10 backend"
echo
echo "=== END MANUAL COMMANDS ==="