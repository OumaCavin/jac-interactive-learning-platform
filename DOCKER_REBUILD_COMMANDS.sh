#!/bin/bash
# Pull latest changes and rebuild Docker containers

echo "=== Pulling latest changes from GitHub ==="
git pull origin main

echo "=== Stopping Docker containers ==="
docker-compose down

echo "=== Rebuilding and starting containers ==="
docker-compose up -d --build

echo "=== Checking backend logs ==="
sleep 10
docker-compose logs backend --tail=50

echo "=== Docker containers status ==="
docker-compose ps