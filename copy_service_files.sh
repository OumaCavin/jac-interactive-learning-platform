#!/bin/bash

# Script to copy service files from workspace to local directory
# This resolves the ModuleNotFoundError: No module named 'apps.services'

echo "🔧 Copying service files to resolve import error..."

# Create the services directory structure
mkdir -p apps/progress/services

# Copy all service files from workspace to local
echo "📁 Creating service files..."

# Copy the __init__.py file (this should already be there from git pull)
cp backend/apps/progress/services/__init__.py apps/progress/services/

# Copy all the service files
cp backend/apps/progress/services/predictive_analytics_service.py apps/progress/services/
cp backend/apps/progress/services/analytics_service.py apps/progress/services/
cp backend/apps/progress/services/progress_service.py apps/progress/services/
cp backend/apps/progress/services/realtime_monitoring_service.py apps/progress/services/
cp backend/apps/progress/services/advanced_analytics_service.py apps/progress/services/
cp backend/apps/progress/services/notification_service.py apps/progress/services/

echo "✅ Service files copied successfully!"

# Verify the files exist
echo ""
echo "📋 Verifying files:"
ls -la apps/progress/services/

echo ""
echo "🚀 Service files are ready! Restart Docker to test:"
echo "   docker-compose restart backend celery-beat celery-worker"
echo "   docker-compose logs backend"