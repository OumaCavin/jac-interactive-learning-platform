#!/bin/bash
# Check the final status of all Docker containers

echo "=== Docker containers status ==="
docker-compose ps

echo "=== Waiting for backend to fully start ==="
sleep 10

echo "=== Backend container logs (last 10 lines) ==="
docker-compose logs backend --tail=10

echo "=== Testing backend endpoint ==="
curl -s http://localhost:8000/ | head -20 || echo "Backend endpoint not available yet"