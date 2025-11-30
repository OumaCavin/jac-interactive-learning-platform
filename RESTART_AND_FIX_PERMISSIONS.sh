#!/bin/bash
# JAC Interactive Learning Platform - Restart to Fix Permissions
# Author: MiniMax Agent
# Created: 2025-11-30

echo "🔄 Restarting containers to fix permission issues..."
echo "================================================"

echo "Step 1: Stopping all containers..."
docker-compose down

echo ""
echo "Step 2: Starting containers fresh..."
docker-compose up -d

echo ""
echo "Step 3: Waiting for backend to be ready..."
sleep 10

echo ""
echo "Step 4: Checking container status..."
docker-compose ps

echo ""
echo "Step 5: Creating migrations with fresh permissions..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "Step 6: Applying migrations..."
docker-compose exec backend python manage.py migrate

echo ""
echo "Step 7: Final verification..."
docker-compose exec backend python manage.py showmigrations | head -20

echo ""
echo "✅ Container restart and migration completion!"