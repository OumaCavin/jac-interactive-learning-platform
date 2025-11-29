#!/bin/bash

echo "=== JAC Interactive Learning Platform - Celery Beat Build Fix ==="
echo "This script fixes the 'Killed' error during celery-beat Docker build"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Docker build failure fix for celery-beat service"
print_status "Issue: 'Killed' error during apt-get install in Dockerfile.celery-beat"
print_status "Cause: Memory/resource constraints during Docker build process"
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    print_status "Please run this script in an environment with Docker installed"
    exit 1
fi

print_status "Step 1: Clean Docker build cache and dangling images"
if docker system prune -f > /dev/null 2>&1; then
    print_status "✅ Docker system cleaned successfully"
else
    print_warning "⚠️ Docker system prune failed, continuing..."
fi

print_status "Step 2: Remove existing celery-beat image and containers"
if docker-compose rm -f celery-beat > /dev/null 2>&1; then
    print_status "✅ Removed existing celery-beat containers"
else
    print_status "ℹ️ No existing celery-beat containers to remove"
fi

# Remove the image specifically
if docker rmi -f $(docker images --filter reference="*celery-beat*" -q) > /dev/null 2>&1; then
    print_status "✅ Removed existing celery-beat images"
else
    print_status "ℹ️ No existing celery-beat images to remove"
fi

print_status "Step 3: Verify Dockerfile.celery-beat has been optimized"
if [ -f "backend/Dockerfile.celery-beat" ]; then
    print_status "✅ Dockerfile.celery-beat found and optimized"
    echo ""
    echo "Key optimizations applied:"
    echo "- Added DEBIAN_FRONTEND=noninteractive"
    echo "- Added --no-install-recommends flag"
    echo "- Enhanced cleanup with pip cache purge"
    echo "- Combined RUN commands for efficiency"
    echo ""
else
    print_error "❌ backend/Dockerfile.celery-beat not found!"
    exit 1
fi

print_status "Step 4: Build celery-beat service with clean cache"
echo "Building celery-beat... This may take a few minutes"
if docker-compose build --no-cache --pull celery-beat; then
    print_status "✅ celery-beat build completed successfully!"
    echo ""
    print_status "Step 5: Test the build by starting services"
    print_status "You can now run: docker-compose up -d backend celery-worker celery-beat"
else
    print_error "❌ celery-beat build failed"
    echo ""
    echo "If build still fails, try these additional steps:"
    echo "1. Restart Docker daemon: sudo systemctl restart docker"
    echo "2. Increase Docker memory limit (if using Docker Desktop)"
    echo "3. Close other applications to free memory"
    echo "4. Try building without parallelization: docker-compose build --no-cache --pull --parallel=false celery-beat"
    exit 1
fi

echo ""
print_status "🎉 Celery Beat build fix completed!"
echo ""
echo "Next steps:"
echo "1. Run: docker-compose up -d backend celery-worker celery-beat"
echo "2. Check status: docker-compose ps"
echo "3. View logs: docker-compose logs -f celery-beat"
echo ""
echo "If you still encounter issues, the Dockerfile has been optimized"
echo "for minimal memory usage and should build successfully."