#!/bin/bash
# Pull the latest fix and test the complete application

echo "=== Pulling latest fix from GitHub ==="
git pull origin main

echo "=== Restarting backend container ==="
docker-compose restart backend

echo "=== Checking backend logs ==="
sleep 10
docker-compose logs backend --tail=50

echo "=== Checking all container statuses ==="
docker-compose ps

echo "=== Testing backend health (if available) ==="
curl -s http://localhost:8000/health/ || echo "Backend not yet available at /health/"