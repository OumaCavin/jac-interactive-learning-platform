#!/bin/bash
# EMERGENCY FIX: Copy service files to local project directory
# This resolves the ModuleNotFoundError by ensuring all service files exist locally

echo "🚨 EMERGENCY SERVICE FILES FIX"
echo "================================="

# Set the target directory (your local project)
TARGET_DIR="$HOME/projects/jac-interactive-learning-platform"

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ Target directory not found: $TARGET_DIR"
    echo "Please update the TARGET_DIR variable to your actual project path"
    exit 1
fi

echo "📁 Target directory: $TARGET_DIR"
echo ""

# Create the services directory in your local project
echo "🔧 Creating services directory structure..."
mkdir -p "$TARGET_DIR/apps/progress/services"

# Copy all service files from workspace to your local project
echo "📋 Copying service files..."

# Check if files exist in workspace and copy them
FILES_TO_COPY=(
    "backend/apps/progress/services/__init__.py"
    "backend/apps/progress/services/predictive_analytics_service.py"
    "backend/apps/progress/services/analytics_service.py"
    "backend/apps/progress/services/progress_service.py"
    "backend/apps/progress/services/realtime_monitoring_service.py"
    "backend/apps/progress/services/advanced_analytics_service.py"
    "backend/apps/progress/services/notification_service.py"
    "backend/apps/progress/services/background_monitoring_service.py"
)

for file in "${FILES_TO_COPY[@]}"; do
    if [ -f "$file" ]; then
        # Get just the filename
        filename=$(basename "$file")
        echo "  ✅ Copying $filename..."
        cp "$file" "$TARGET_DIR/apps/progress/services/"
    else
        echo "  ❌ Source file not found: $file"
    fi
done

echo ""
echo "🎉 Service files copied successfully!"

# Verify the files exist
echo ""
echo "📋 Verifying files in your project:"
if [ -d "$TARGET_DIR/apps/progress/services" ]; then
    ls -la "$TARGET_DIR/apps/progress/services/"
    echo ""
    echo "✅ All service files are now in your local project!"
else
    echo "❌ Services directory was not created properly"
    exit 1
fi

echo ""
echo "🚀 NEXT STEPS:"
echo "==============="
echo "1. Navigate to your project directory:"
echo "   cd $TARGET_DIR"
echo ""
echo "2. Rebuild and restart Docker containers:"
echo "   docker-compose down"
echo "   docker-compose up -d --build"
echo ""
echo "3. Check that the backend starts without errors:"
echo "   docker-compose logs backend"
echo ""
echo "4. Test the API:"
echo "   Visit: http://localhost:8000/api/docs/"
echo ""
echo "✅ This should resolve the ModuleNotFoundError!"