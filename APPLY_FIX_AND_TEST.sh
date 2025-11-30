#!/bin/bash
# Apply the latest fix and test the application

echo "=== Pulling latest fix from GitHub ==="
git pull origin main

echo "=== Restarting backend container ==="
docker-compose restart backend

echo "=== Checking backend logs ==="
sleep 5
docker-compose logs backend --tail=30

echo "=== Docker containers status ==="
docker-compose ps