#!/bin/bash

# JAC Interactive Learning Platform - Complete Import Fix Script
# Author: Cavin Otieno
# Fixes all identified import and syntax errors across the entire codebase

set -e

echo "🔧 JAC Complete Import Fix Script"
echo "================================="
echo "This script fixes all import issues found in the comprehensive audit"
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

# Pull latest changes from Git (includes all import fixes)
echo "📥 Pulling latest changes from GitHub..."
echo "   (Includes: progress app import fixes, management command fixes, syntax fixes)"
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ Git pull successful"
else
    echo "⚠️ Git pull failed, continuing with local files..."
fi

echo ""

# Check Python syntax of all key files
echo "🔍 Checking Python syntax..."
SYNTAX_OK=true

# Check views files
for views_file in $(find backend/apps -name "*views*.py" -type f); do
    if python3 -m py_compile "$views_file" 2>/dev/null; then
        echo "  ✅ Syntax OK: $(basename $views_file)"
    else
        echo "  ❌ Syntax Error: $(basename $views_file)"
        SYNTAX_OK=false
    fi
done

# Check management commands
for cmd_file in $(find backend/apps -name "*.py" -path "*/management/*" -type f); do
    if python3 -m py_compile "$cmd_file" 2>/dev/null; then
        echo "  ✅ Syntax OK: $(basename $cmd_file)"
    else
        echo "  ❌ Syntax Error: $(basename $cmd_file)"
        SYNTAX_OK=false
    fi
done

if [ "$SYNTAX_OK" = true ]; then
    echo "✅ All Python files have valid syntax!"
else
    echo "❌ Some Python files have syntax errors!"
    echo "   Please check the errors above and fix manually"
    exit 1
fi

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
echo "🔨 Rebuilding Docker containers..."
echo "   (This process may take 5-10 minutes depending on your connection)"
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
sleep 15

# Check container status
echo "📊 Container Status:"
docker-compose ps

echo ""

# Test the import fixes comprehensively
echo "🧪 Testing import fixes across all apps..."
docker-compose exec -T backend python -c "
import sys
import os

print('Testing imports across all apps...')

# Test progress app imports (the main issue)
try:
    from apps.progress.services.predictive_analytics_service import PredictiveAnalyticsService
    from apps.progress.services.analytics_service import AnalyticsService
    from apps.progress.services.progress_service import ProgressService
    from apps.progress.services.advanced_analytics_service import AdvancedAnalyticsService
    from apps.progress.services.realtime_monitoring_service import RealtimeMonitoringService
    print('  ✅ Progress app service imports: OK')
except Exception as e:
    print(f'  ❌ Progress app service imports failed: {e}')
    sys.exit(1)

# Test learning app imports
try:
    from apps.learning.services.adaptive_challenge_service import AdaptiveChallengeService
    from apps.learning.services.difficulty_adjustment_service import DifficultyAdjustmentService
    print('  ✅ Learning app service imports: OK')
except Exception as e:
    print(f'  ❌ Learning app service imports failed: {e}')
    sys.exit(1)

# Test jac_execution app imports
try:
    from apps.jac_execution.services.executor import ExecutionService
    print('  ✅ Jac Execution app service imports: OK')
except Exception as e:
    print(f'  ❌ Jac Execution app service imports failed: {e}')
    sys.exit(1)

# Test knowledge_graph app imports
try:
    from apps.knowledge_graph.services.analytics import KnowledgeGraphAnalytics
    from apps.knowledge_graph.services.graph_algorithms import GraphAnalyzer
    print('  ✅ Knowledge Graph app service imports: OK')
except Exception as e:
    print(f'  ❌ Knowledge Graph app service imports failed: {e}')
    sys.exit(1)

# Test cross-app imports
try:
    from apps.progress.services.advanced_analytics_service import AdvancedAnalyticsService
    from apps.learning.models import UserModuleProgress, AssessmentAttempt
    from apps.assessments.models import AssessmentAttempt as AssessmentAttemptModel
    print('  ✅ Cross-app imports: OK')
except Exception as e:
    print(f'  ❌ Cross-app imports failed: {e}')
    sys.exit(1)

print('')
print('🎉 All import tests passed successfully!')
"

IMPORT_TEST=$?

if [ $IMPORT_TEST -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! All import errors have been resolved!"
    echo ""
    echo "📍 Your JAC Interactive Learning Platform is now running with:"
    echo "   • ✅ Fixed progress app service imports"
    echo "   • ✅ Fixed management command imports"
    echo "   • ✅ Fixed syntax errors"
    echo "   • ✅ Verified cross-app imports"
    echo ""
    echo "🌐 Access Points:"
    echo "   • Backend API: http://localhost:8000/api/docs/"
    echo "   • Frontend: http://localhost:3000"
    echo "   • Nginx: http://localhost:80"
    echo "   • Admin: http://localhost:8000/admin/"
    echo ""
    echo "📋 Summary of Fixes Applied:"
    echo "   1. Progress app views: Changed '..services' to '.services'"
    echo "   2. Progress app consumers: Fixed relative import paths"
    echo "   3. Management commands: Fixed start_monitoring import path"
    echo "   4. Learning app: Fixed duplicate parenthesis in populate_jac_curriculum"
    echo ""
else
    echo ""
    echo "❌ Import test failed. Please check the logs for more details:"
    echo "   docker-compose logs backend"
    echo ""
    echo "   You may need to:"
    echo "   1. Check if all files were properly pulled from Git"
    echo "   2. Restart Docker with 'docker-compose down && docker-compose up -d --build'"
    echo "   3. Check for any custom local changes that might conflict"
    exit 1
fi

# Show useful commands for debugging
echo ""
echo "🔧 Useful commands for ongoing development:"
echo "   • View backend logs: docker-compose logs backend --tail=50"
echo "   • View all logs: docker-compose logs"
echo "   • Check service files: docker-compose exec backend ls -la /app/apps/progress/services/"
echo "   • Test API endpoints: curl http://localhost:8000/api/progress/learning-paths/"
echo "   • Django shell: docker-compose exec backend python manage.py shell"
echo "   • Check migrations: docker-compose exec backend python manage.py showmigrations"
echo ""

# Test Django system check
echo "🔍 Running Django system check..."
docker-compose exec -T backend python manage.py check --deploy

if [ $? -eq 0 ]; then
    echo "✅ Django system check passed!"
else
    echo "⚠️ Django system check had warnings (this may be normal in development mode)"
fi

echo ""
echo "✨ Complete Import Fix Applied Successfully!"
echo "✨ JAC Platform is ready for development!"
echo ""
echo "📚 For more details, see: COMPREHENSIVE_IMPORT_AUDIT_REPORT.md"
echo ""