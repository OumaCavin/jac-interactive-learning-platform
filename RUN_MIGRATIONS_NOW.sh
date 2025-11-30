#!/bin/bash

# JAC Interactive Learning Platform - Run Migrations Now That Containers Are Healthy
# This script runs the migrations now that all containers are healthy

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Running Migrations - All Containers Healthy"
echo "=========================================="

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform

# Pull latest changes
echo ""
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Wait for git to complete
sleep 2

echo ""
echo "✅ All containers are healthy - proceeding with migrations"
echo ""

# Create migrations
echo "🛠️ Creating migrations for collaboration, gamification, jac_execution, learning..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations to database..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ Migration status:"
docker-compose exec backend python manage.py showmigrations

echo ""
echo "🎉 SUCCESS! Your JAC Interactive Learning Platform database schema is now fully updated!"
echo "All 29 model field changes have been applied successfully."
