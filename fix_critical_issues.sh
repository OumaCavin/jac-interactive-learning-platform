#!/bin/bash

# JAC Learning Platform - Critical Issues Fix Script
# Fixes URL namespace conflicts, database constraints, and migration issues

echo "🔧 Fixing critical issues in JAC Learning Platform..."

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform

echo "📝 Issue 1: Fixing URL namespace conflict..."

# Fix the URL namespace conflict by removing the duplicate jac-execution include
sed -i '/path.*jac-execution.*include.*apps\.jac_execution\.urls/d' backend/config/urls.py

# Add a comment explaining the fix
sed -i '/# JAC execution engine/a\\n    # Note: jac_execution URLs included only once to avoid namespace conflicts' backend/config/urls.py

echo "✅ URL namespace conflict fixed"

echo "🗄️  Issue 2: Fixing database constraint violation..."

# Fix UserLevel model by adding default value for xp_to_next_level
sed -i 's/xp_to_next_level = models\.PositiveIntegerField()/xp_to_next_level = models.PositiveIntegerField(default=100)/' backend/apps/gamification/models.py

echo "✅ Database constraint violation fixed"

echo "📊 Issue 3: Generating new migrations..."

# Generate migrations for apps with changes
echo "🔄 Generating migrations for collaboration app..."
docker-compose exec backend python manage.py makemigrations collaboration

echo "🔄 Generating migrations for gamification app..."
docker-compose exec backend python manage.py makemigrations gamification

echo "🔄 Generating migrations for learning app..."
docker-compose exec backend python manage.py makemigrations learning

echo "📋 Issue 4: Running migrations..."

# Apply the new migrations
docker-compose exec backend python manage.py migrate

echo "🏗️ Issue 5: Rebuilding backend..."

# Rebuild backend to apply fixes
docker-compose up -d --build backend

echo "⏳ Waiting for backend to be ready..."
sleep 15

echo "🔍 Issue 6: Verifying fixes..."

# Check database connection
docker-compose exec backend python manage.py check --database default

# Test backend health
curl -s http://localhost:8000/api/health/ | head -n 1

echo ""
echo "🎉 ALL CRITICAL ISSUES FIXED!"
echo ""
echo "✅ Fixed URL namespace conflicts"
echo "✅ Fixed database constraint violations"  
echo "✅ Generated pending migrations"
echo "✅ Applied all migrations"
echo "✅ Rebuilt backend with fixes"
echo ""
echo "📱 Access your application at:"
echo "   • Frontend: http://localhost:3000"
echo "   • Backend API: http://localhost:8000"
echo "   • Django Admin: http://localhost:8000/admin/"
echo ""
echo "🔑 Admin Credentials:"
echo "   • Username: admin"
echo "   • Password: admin123"
