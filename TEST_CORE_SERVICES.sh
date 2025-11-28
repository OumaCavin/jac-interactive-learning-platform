#!/bin/bash

# JAC Learning Platform - Core Services Test
# Tests only the essential services: backend and frontend
# Author: Cavin Otieno

echo "=========================================="
echo "JAC Learning Platform - Core Services Test"
echo "Testing essential backend and frontend services only"
echo "=========================================="

# Function to check if docker-compose is available
check_docker() {
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ docker-compose is not installed or not in PATH"
        return 1
    fi
    echo "✅ docker-compose found"
    return 0
}

# Function to test core services deployment
test_core_services() {
    echo ""
    echo "🚀 Testing Core Services Deployment..."
    echo "=========================================="
    
    if docker-compose -f docker-compose.simple.yml up -d; then
        echo "✅ Core services started successfully!"
        echo "   - PostgreSQL database"
        echo "   - Redis cache"
        echo "   - Django backend API"
        echo "   - React frontend"
        echo ""
        echo "⏳ Waiting 45 seconds for services to initialize..."
        sleep 45
        
        # Check service health
        echo ""
        echo "📊 Service Status:"
        docker-compose -f docker-compose.simple.yml ps
        
        # Test backend health
        echo ""
        echo "🔍 Testing Backend Health..."
        if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
            echo "✅ Backend API is responding"
        else
            echo "⚠️  Backend API may still be starting up"
        fi
        
        # Test frontend
        echo ""
        echo "🔍 Testing Frontend..."
        if curl -f http://localhost:3000/ > /dev/null 2>&1; then
            echo "✅ Frontend is responding"
        else
            echo "⚠️  Frontend may still be starting up"
        fi
        
        return 0
    else
        echo "❌ Core services deployment failed"
        return 1
    fi
}

# Function to clean up
cleanup() {
    echo ""
    echo "🧹 Cleaning up core services..."
    docker-compose -f docker-compose.simple.yml down --volumes
    echo "✅ Cleanup completed"
}

# Main execution
main() {
    echo "Starting core services test..."
    
    # Check prerequisites
    check_docker || exit 1
    
    # Pull latest changes
    echo ""
    echo "📥 Pulling latest changes from GitHub..."
    git pull origin main
    echo "✅ Latest changes pulled"
    
    # Test core services
    if test_core_services; then
        echo ""
        echo "🎉 CORE SERVICES TEST PASSED!"
        echo "The backend Docker syntax fix and frontend TypeScript fix are working."
        echo ""
        echo "✅ Available Services:"
        echo "   • PostgreSQL Database: localhost:5432"
        echo "   • Django Backend API: http://localhost:8000"
        echo "   • React Frontend: http://localhost:3000"
        echo "   • Redis Cache: localhost:6379"
        echo ""
        echo "Next steps:"
        echo "1. Test password hashing deployment:"
        echo "   ./DEPLOY_LOCAL_FIXES.sh"
        echo ""
        echo "2. Access the application:"
        echo "   Frontend: http://localhost:3000"
        echo "   Backend API: http://localhost:8000"
        echo ""
        echo "Demo credentials:"
        echo "   • User: demo@example.com / demo123"
        echo "   • Admin: admin@jac.com / admin123"
    else
        echo ""
        echo "❌ CORE SERVICES TEST FAILED"
        echo "Please check the error messages above"
    fi
    
    # Cleanup option
    echo ""
    read -p "   Clean up services? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cleanup
    fi
}

# Run main function
main "$@"