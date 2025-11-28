#!/bin/bash

# JAC Learning Platform - Build Test Script
# Tests both backend Docker syntax fix and frontend TypeScript fix
# Author: Cavin Otieno

echo "=========================================="
echo "JAC Learning Platform - Build Test Script"
echo "Testing Docker syntax fix and TypeScript compilation fix"
echo "=========================================="

# Function to check if docker-compose is available
check_docker() {
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ docker-compose is not installed or not in PATH"
        echo "Please install Docker Desktop or Docker Compose"
        return 1
    fi
    echo "✅ docker-compose found"
    return 0
}

# Function to check if we're in the project directory
check_project_dir() {
    if [ ! -f "docker-compose.yml" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        echo "❌ Not in project root directory"
        echo "Please run this script from the jac-interactive-learning-platform directory"
        return 1
    fi
    echo "✅ Project directory confirmed"
    return 0
}

# Function to test backend Docker build
test_backend() {
    echo ""
    echo "🔨 Testing Backend Docker Build..."
    echo "=========================================="
    
    if docker-compose build --no-cache backend; then
        echo "✅ Backend Docker build completed successfully!"
        echo "   - Docker COPY syntax fix is working"
        echo "   - No 'COPY failed: stat ||' errors"
        return 0
    else
        echo "❌ Backend Docker build failed"
        echo "   - Check if Docker syntax fix is correctly applied"
        return 1
    fi
}

# Function to test frontend build
test_frontend() {
    echo ""
    echo "🔨 Testing Frontend TypeScript Compilation..."
    echo "=========================================="
    
    if docker-compose build --no-cache frontend; then
        echo "✅ Frontend build completed successfully!"
        echo "   - TypeScript compilation fix is working"
        echo "   - No TS2345 type mismatch errors"
        return 0
    else
        echo "❌ Frontend build failed"
        echo "   - Check if TypeScript authentication fix is correctly applied"
        echo "   - Look for TypeScript compilation errors in the output"
        return 1
    fi
}

# Function to run full stack test
test_full_stack() {
    echo ""
    echo "🚀 Testing Full Stack Deployment..."
    echo "=========================================="
    
    if docker-compose up -d; then
        echo "✅ Full stack deployment completed!"
        echo "   - Waiting 30 seconds for containers to start..."
        sleep 30
        
        # Check container status
        echo ""
        echo "📊 Container Status:"
        docker-compose ps
        
        # Check backend logs
        echo ""
        echo "📋 Backend Logs:"
        docker-compose logs backend | tail -20
        
        # Check frontend logs  
        echo ""
        echo "📋 Frontend Logs:"
        docker-compose logs frontend | tail -20
        
        echo ""
        echo "✅ Full stack test completed successfully!"
        return 0
    else
        echo "❌ Full stack deployment failed"
        return 1
    fi
}

# Function to clean up
cleanup() {
    echo ""
    echo "🧹 Cleaning up containers and volumes..."
    docker-compose down --volumes
    echo "✅ Cleanup completed"
}

# Main execution
main() {
    echo "Starting build tests..."
    
    # Check prerequisites
    check_docker || exit 1
    check_project_dir || exit 1
    
    # Pull latest changes
    echo ""
    echo "📥 Pulling latest changes from GitHub..."
    git pull origin main
    echo "✅ Latest changes pulled"
    
    # Test backend build
    if test_backend; then
        BACKEND_SUCCESS=true
    else
        BACKEND_SUCCESS=false
    fi
    
    # Test frontend build
    if test_frontend; then
        FRONTEND_SUCCESS=true
    else
        FRONTEND_SUCCESS=false
    fi
    
    # Summary
    echo ""
    echo "=========================================="
    echo "BUILD TEST SUMMARY"
    echo "=========================================="
    
    if [ "$BACKEND_SUCCESS" = true ]; then
        echo "✅ Backend Docker Build: PASSED"
    else
        echo "❌ Backend Docker Build: FAILED"
    fi
    
    if [ "$FRONTEND_SUCCESS" = true ]; then
        echo "✅ Frontend TypeScript Build: PASSED"
    else
        echo "❌ Frontend TypeScript Build: FAILED"
    fi
    
    # Overall result
    if [ "$BACKEND_SUCCESS" = true ] && [ "$FRONTEND_SUCCESS" = true ]; then
        echo ""
        echo "🎉 ALL TESTS PASSED!"
        echo "Both the Docker syntax fix and TypeScript fix are working correctly."
        echo ""
        echo "Next steps:"
        echo "1. Run the password hashing deployment script:"
        echo "   ./DEPLOY_LOCAL_FIXES.sh"
        echo ""
        echo "2. Test the full application:"
        read -p "   Start full stack deployment? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            test_full_stack
        fi
    else
        echo ""
        echo "⚠️  SOME TESTS FAILED"
        echo "Please review the error messages above and check:"
        echo "1. Docker syntax fix in backend/Dockerfile"
        echo "2. TypeScript fix in frontend/src/pages/auth/LoginPage.tsx"
    fi
    
    # Cleanup option
    echo ""
    read -p "   Clean up containers and volumes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
    fi
}

# Run main function
main "$@"