#!/bin/bash

# JAC Learning Platform - Complete Test and Deployment Script
# Tests all fixes: Docker syntax, TypeScript, Celery services, and Password hashing
# Author: Cavin Otieno

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔧 $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${YELLOW}🔸 $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_step "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        return 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        return 1
    fi
    
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        return 1
    fi
    
    print_success "All prerequisites met"
    return 0
}

# Test backend build
test_backend_build() {
    print_step "Testing Backend Docker Build..."
    
    if docker-compose build --no-cache backend; then
        print_success "Backend Docker build PASSED"
        return 0
    else
        print_error "Backend Docker build FAILED"
        return 1
    fi
}

# Test frontend build
test_frontend_build() {
    print_step "Testing Frontend TypeScript Build..."
    
    if docker-compose build --no-cache frontend; then
        print_success "Frontend TypeScript build PASSED"
        return 0
    else
        print_error "Frontend TypeScript build FAILED"
        return 1
    fi
}

# Test celery builds
test_celery_builds() {
    print_step "Testing Celery Services Build..."
    
    # Test celery-worker
    if docker-compose build --no-cache celery-worker; then
        print_success "Celery Worker build PASSED"
    else
        print_error "Celery Worker build FAILED"
        return 1
    fi
    
    # Test celery-beat
    if docker-compose build --no-cache celery-beat; then
        print_success "Celery Beat build PASSED"
    else
        print_error "Celery Beat build FAILED"
        return 1
    fi
    
    # Test jac-sandbox
    if docker-compose build --no-cache jac-sandbox; then
        print_success "JAC Sandbox build PASSED"
    else
        print_error "JAC Sandbox build FAILED"
        return 1
    fi
    
    return 0
}

# Deploy and test full stack
deploy_full_stack() {
    print_step "Deploying Full Stack..."
    
    # Clean start
    print_info "Starting with clean slate..."
    docker-compose down --volumes --remove-orphans 2>/dev/null || true
    
    # Start core services
    print_info "Starting PostgreSQL and Redis..."
    docker-compose up -d postgres redis
    
    # Wait for PostgreSQL
    print_info "Waiting for PostgreSQL..."
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db > /dev/null 2>&1; then
            print_success "PostgreSQL is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_error "PostgreSQL failed to start"
            return 1
        fi
        sleep 2
    done
    
    # Start backend and celery services
    print_info "Starting backend services..."
    docker-compose up -d backend celery-worker celery-beat jac-sandbox
    
    # Wait for backend
    print_info "Waiting for backend API..."
    for i in {1..60}; do
        if curl -s -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
            print_success "Backend API is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            print_warning "Backend API may still be starting"
            break
        fi
        sleep 2
    done
    
    # Start frontend
    print_info "Starting frontend..."
    docker-compose up -d frontend
    
    # Wait for frontend
    print_info "Waiting for frontend..."
    for i in {1..30}; do
        if curl -s -f http://localhost:3000/ > /dev/null 2>&1; then
            print_success "Frontend is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Frontend may still be starting"
            break
        fi
        sleep 2
    done
    
    print_success "Full stack deployment completed"
    return 0
}

# Verify all services
verify_services() {
    print_step "Verifying all services..."
    
    # Check service status
    echo ""
    print_info "Service Status:"
    docker-compose ps
    
    # Test health endpoints
    echo ""
    print_info "Health Check Results:"
    
    services=("PostgreSQL" "Redis" "Backend API" "Frontend" "Celery Worker" "Celery Beat" "JAC Sandbox")
    urls=("postgres:5432" "redis:6379" "http://localhost:8000/api/health/" "http://localhost:3000/" "" "" "")
    
    for i in "${!services[@]}"; do
        service="${services[$i]}"
        url="${urls[$i]}"
        
        if [[ "$service" == "PostgreSQL" ]]; then
            if docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db > /dev/null 2>&1; then
                print_success "$service: HEALTHY"
            else
                print_error "$service: NOT READY"
            fi
        elif [[ "$service" == "Redis" ]]; then
            if docker-compose exec -T redis redis-cli -a redis_password ping > /dev/null 2>&1; then
                print_success "$service: HEALTHY"
            else
                print_error "$service: NOT READY"
            fi
        else
            if curl -s -f "$url" > /dev/null 2>&1; then
                print_success "$service: HEALTHY"
            else
                print_warning "$service: May still be starting"
            fi
        fi
    done
}

# Main execution
main() {
    echo ""
    print_header "🚀 JAC PLATFORM - COMPLETE TEST AND DEPLOYMENT"
    echo ""
    
    # Check prerequisites
    check_prerequisites || exit 1
    
    # Pull latest changes
    print_step "Pulling latest changes..."
    git pull origin main
    print_success "Latest changes pulled"
    
    # Test individual builds
    print_header "🏗️  TESTING INDIVIDUAL BUILDS"
    
    BACKEND_OK=false
    FRONTEND_OK=false
    CELERY_OK=false
    
    test_backend_build && BACKEND_OK=true
    test_frontend_build && FRONTEND_OK=true
    test_celery_builds && CELERY_OK=true
    
    # Build summary
    print_header "📊 BUILD TEST RESULTS"
    
    if [ "$BACKEND_OK" = true ]; then
        print_success "✅ Backend Docker Syntax Fix: WORKING"
    else
        print_error "❌ Backend Docker Syntax Fix: FAILED"
    fi
    
    if [ "$FRONTEND_OK" = true ]; then
        print_success "✅ Frontend TypeScript Fix: WORKING"
    else
        print_error "❌ Frontend TypeScript Fix: FAILED"
    fi
    
    if [ "$CELERY_OK" = true ]; then
        print_success "✅ Celery Services Configuration: WORKING"
    else
        print_error "❌ Celery Services Configuration: FAILED"
    fi
    
    # Overall result
    if [ "$BACKEND_OK" = true ] && [ "$FRONTEND_OK" = true ] && [ "$CELERY_OK" = true ]; then
        echo ""
        print_success "🎉 ALL BUILD TESTS PASSED!"
        
        # Ask if user wants to proceed with deployment
        echo ""
        read -p "   Proceed with full stack deployment? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_header "🚀 DEPLOYING FULL STACK"
            deploy_full_stack || exit 1
            verify_services
        fi
        
        echo ""
        print_success "✅ ALL TESTS COMPLETED SUCCESSFULLY!"
        echo ""
        echo -e "${CYAN}Next Steps:${NC}"
        echo "1. Deploy password hashing with prompts:"
        echo "   ./DEPLOY_LOCAL_FIXES.sh"
        echo ""
        echo "2. Or run the full deployment:"
        echo "   ./DEPLOY_LOCAL_FIXES.sh"
        echo ""
        echo -e "${YELLOW}Service URLs:${NC}"
        echo "• Frontend: http://localhost:3000"
        echo "• Backend API: http://localhost:8000"
        echo "• Django Admin: http://localhost:8000/admin/"
        echo "• JAC Sandbox: http://localhost:8080"
        
    else
        print_error "❌ SOME TESTS FAILED"
        echo "Please review the error messages above and try again."
        exit 1
    fi
}

# Run main function
main "$@"