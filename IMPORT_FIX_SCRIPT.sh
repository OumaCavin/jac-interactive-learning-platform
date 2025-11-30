#!/bin/bash

# JAC Interactive Learning Platform - Import Fix Script
# Fixes ModuleNotFoundError: No module named 'apps.services'
# Author: Cavin Otieno

set -e

echo "🔧 JAC Import Error Fix Script"
echo "=================================="
echo ""

# Navigate to project directory
PROJECT_DIR="$HOME/projects/jac-interactive-learning-platform"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "❌ Error: Project directory not found at $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"
echo "📁 Working directory: $(pwd)"
echo ""

# Pull latest changes from Git
echo "📥 Pulling latest changes from GitHub..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ Git pull successful"
else
    echo "⚠️ Git pull failed, continuing with local files..."
fi

echo ""

# Check if service files exist
echo "🔍 Checking service files..."
SERVICE_DIR="$PROJECT_DIR/backend/apps/progress/services"

if [ ! -d "$SERVICE_DIR" ]; then
    echo "❌ Service directory not found: $SERVICE_DIR"
    exit 1
fi

SERVICE_FILES=("__init__.py" "predictive_analytics_service.py" "analytics_service.py" "progress_service.py" "realtime_monitoring_service.py" "advanced_analytics_service.py" "notification_service.py" "background_monitoring_service.py")

for file in "${SERVICE_FILES[@]}"; do
    if [ -f "$SERVICE_DIR/$file" ]; then
        echo "✅ Found: $file"
    else
        echo "❌ Missing: $file"
    fi
done

echo ""

# Stop Docker containers
echo "🛑 Stopping Docker containers..."
docker-compose down

if [ $? -eq 0 ]; then
    echo "✅ Docker containers stopped"
else
    echo "⚠️ Warning: Some containers may not have stopped properly"
fi

echo ""

# Clear Docker cache and rebuild
echo "🔨 Rebuilding Docker containers (this may take a few minutes)..."
timeout 300 docker-compose up -d --build --force-recreate

if [ $? -eq 0 ]; then
    echo "✅ Docker containers rebuilt and started"
else
    echo "⚠️ Docker build timed out or failed. Trying to start existing containers..."
    docker-compose up -d
fi

echo ""

# Wait for containers to start
echo "⏳ Waiting for containers to stabilize..."
sleep 10

# Check container status
echo "📊 Container Status:"
docker-compose ps

echo ""

# Test the import fix
echo "🧪 Testing import fix..."
docker-compose exec -T backend python -c "
try:
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    from apps.progress.services.analytics_service import AnalyticsService
    from apps.progress.services.progress_service import ProgressService
    print('✅ All service imports successful!')
except Exception as e:
    print(f'❌ Import test failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! The import error has been resolved!"
    echo ""
    echo "📍 Your JAC Interactive Learning Platform is now running:"
    echo "   • Backend API: http://localhost:8000/api/docs/"
    echo "   • Frontend: http://localhost:3000"
    echo "   • Nginx: http://localhost:80"
    echo ""
    echo "📋 What was fixed:"
    echo "   • Corrected import paths from '..services' to '.services'"
    echo "   • Fixed relative imports in views_predictive.py"
    echo "   • Fixed relative imports in views_advanced_analytics.py"
    echo "   • Fixed relative imports in consumers.py"
    echo ""
else
    echo ""
    echo "❌ Import test failed. Please check the logs:"
    echo "   docker-compose logs backend"
    exit 1
fi

# Show useful commands
echo ""
echo "🔧 Useful commands for debugging:"
echo "   • View backend logs: docker-compose logs backend"
echo "   • View all logs: docker-compose logs"
echo "   • Check service files: docker-compose exec backend ls -la /app/apps/progress/services/"
echo "   • Test API: curl http://localhost:8000/api/progress/learning-paths/"
echo ""
echo "✨ JAC Import Fix Complete!"