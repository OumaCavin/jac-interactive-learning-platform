#!/bin/bash
# Docker Debug Commands

echo "=== BACKEND LOGS ==="
docker logs jac-interactive-learning-platform_backend_1 --tail 50

echo -e "\n=== CELERY BEAT LOGS ==="
docker logs jac-interactive-learning-platform_celery-beat --tail 30

echo -e "\n=== CELERY WORKER LOGS ==="
docker logs jac-interactive-learning-platform_celery-worker --tail 30

echo -e "\n=== BACKEND CONTAINER STATUS ==="
docker inspect jac-interactive-learning-platform_backend_1 | jq -r '.[] | .State'

echo -e "\n=== TEST BACKEND HEALTH ==="
curl -f http://localhost:8000/api/health/ || echo "Backend not responding"

echo -e "\n=== CHECK DATABASE CONNECTION ==="
docker-compose exec backend python manage.py dbshell << 'EOF'
SELECT 1;
.quit
EOF