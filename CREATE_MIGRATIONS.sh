#!/bin/bash

# JAC Interactive Learning Platform - Create Migrations Script
# This script will pull latest changes and create migrations for all fixed models

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Creating Migrations for Fixed Models"
echo "=========================================="

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform

# Pull latest changes
echo ""
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

# Wait for git to complete
sleep 3

# Ensure Docker containers are running
echo ""
echo "🐳 Checking Docker containers..."
docker-compose ps

# Check if containers are healthy
echo ""
echo "🛠️ Creating migrations for collaboration, gamification, jac_execution, learning..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "📊 Applying migrations to database..."
docker-compose exec backend python manage.py migrate

echo ""
echo "✅ Migration status:"
docker-compose exec backend python manage.py showmigrations

echo ""
echo "🎉 Migrations completed successfully!"
echo "Your JAC Interactive Learning Platform database schema is now up-to-date."
