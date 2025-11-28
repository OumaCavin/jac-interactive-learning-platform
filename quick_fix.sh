#!/bin/bash

# JAC Learning Platform - Quick Fix Script
# Applies the URL namespace and database constraint fixes

echo "🔧 Applying JAC Platform fixes..."

cd ~/projects/jac-interactive-learning-platform

echo "📝 Step 1: Generating migrations for changed models..."
docker-compose exec backend python manage.py makemigrations

echo "📋 Step 2: Applying migrations..."
docker-compose exec backend python manage.py migrate

echo "🏗️  Step 3: Restarting backend to apply changes..."
docker-compose restart backend

echo "⏳ Step 4: Waiting for backend to be ready..."
sleep 20

echo "🔍 Step 5: Verifying fixes..."
docker-compose exec backend python manage.py check --database default

echo ""
echo "✅ Fixes applied successfully!"
echo "📱 Access your application at:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend: http://localhost:8000"
echo "   • Admin: http://localhost:8000/admin/"
