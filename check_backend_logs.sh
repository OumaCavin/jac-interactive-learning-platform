#!/bin/bash
echo "=== Backend Logs ==="
docker-compose logs -f backend

echo -e "\n=== Quick Status Check ==="
docker-compose ps

echo -e "\n=== Database Connection Test ==="
docker-compose exec backend python manage.py check --database default