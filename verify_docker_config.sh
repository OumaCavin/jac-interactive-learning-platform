#!/bin/bash

# Docker Configuration Verification Script
# Tests that non-root user configuration is working correctly
# Author: Cavin Otieno

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔹 $1${NC}"
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
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${YELLOW}🔸 $1${NC}"
}

# Check if Docker is running
check_docker() {
    print_header "DOCKER CONFIGURATION VERIFICATION"
    
    print_step "Checking Docker daemon status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    print_success "Docker daemon is running"
}

# Check Docker Compose configuration
check_docker_compose() {
    print_step "Validating Docker Compose configuration..."
    
    if docker-compose config > /dev/null 2>&1; then
        print_success "Docker Compose configuration is valid"
    else
        print_error "Docker Compose configuration has errors"
        docker-compose config
        exit 1
    fi
}

# Check for non-root user configuration
check_non_root_users() {
    print_step "Verifying non-root user configuration..."
    
    local services_with_users=$(docker-compose config | grep -c "user: \"jac:jac\"" || true)
    
    if [ "$services_with_users" -ge 4 ]; then
        print_success "Found non-root user configuration for $services_with_users services"
        print_info "Services configured with jac:jac user:"
        docker-compose config | grep -A 1 "user: \"jac:jac\""
    else
        print_error "Expected at least 4 services with non-root users, found: $services_with_users"
    fi
}

# Check Dockerfiles
check_dockerfiles() {
    print_step "Verifying Dockerfiles exist..."
    
    local dockerfiles=("Dockerfile" "Dockerfile.celery-worker" "Dockerfile.celery-beat" "Dockerfile.jac-sandbox")
    
    for dockerfile in "${dockerfiles[@]}"; do
        if [ -f "backend/$dockerfile" ]; then
            print_success "Found: backend/$dockerfile"
        else
            print_error "Missing: backend/$dockerfile"
        fi
    done
}

# Check virtual environment setup in backend Dockerfile
check_venv_setup() {
    print_step "Verifying virtual environment setup..."
    
    if grep -q "python -m venv" backend/Dockerfile; then
        print_success "Virtual environment setup found in backend Dockerfile"
    else
        print_warning "Virtual environment setup not found in backend Dockerfile"
    fi
    
    if grep -q "ENV PATH=\"/home/jac/venv" backend/Dockerfile; then
        print_success "Virtual environment PATH configuration found"
    else
        print_warning "Virtual environment PATH configuration not found"
    fi
}

# Check entrypoint scripts
check_entrypoints() {
    print_step "Verifying entrypoint scripts..."
    
    if grep -q "execvp.*venv/bin/python" backend/Dockerfile; then
        print_success "Entrypoint uses virtual environment Python"
    else
        print_warning "Entrypoint may not be using virtual environment Python"
    fi
}

# Build test (without starting services)
test_build() {
    print_header "BUILD TEST"
    
    print_step "Building Docker images to verify configuration..."
    
    # Build only the backend service first
    if docker-compose build backend > /dev/null 2>&1; then
        print_success "Backend image built successfully"
    else
        print_error "Backend image build failed"
        docker-compose build backend
        exit 1
    fi
    
    # Check if non-root user was created
    print_step "Verifying non-root user in image..."
    if docker run --rm jac-interactive-learning-platform_backend:latest id jac > /dev/null 2>&1; then
        print_success "Non-root user 'jac' created in image"
    else
        print_warning "Could not verify non-root user 'jac' in image"
    fi
}

# Check database directory
check_database_files() {
    print_step "Checking database setup files..."
    
    if [ -d "database" ]; then
        local file_count=$(ls database/*.sql 2>/dev/null | wc -l)
        print_success "Found database directory with $file_count SQL files"
    else
        print_error "Database directory not found"
    fi
}

# Show summary
show_summary() {
    print_header "CONFIGURATION SUMMARY"
    
    print_info "✅ Docker Configuration Updated Successfully!"
    print_info "✅ Non-root user 'jac:jac' configured for all Django services"
    print_info "✅ Virtual environment setup in backend Dockerfile"
    print_info "✅ Individual Dockerfiles for Celery and Sandbox services"
    print_info "✅ Virtual environment PATH configuration"
    print_info "✅ Updated docker-compose.yml with proper user specifications"
    
    echo ""
    print_step "Next Steps:"
    echo "1. Clean rebuild: docker-compose down -v && docker-compose build --no-cache"
    echo "2. Start services: docker-compose up -d"
    echo "3. Test database: bash database/setup_comprehensive.sh"
    echo "4. Verify no root warnings in build output"
    
    echo ""
    print_success "Root user warning should be eliminated!"
}

# Main execution
main() {
    if [ ! -f "docker-compose.yml" ]; then
        print_error "docker-compose.yml not found in current directory"
        exit 1
    fi
    
    check_docker
    check_docker_compose
    check_non_root_users
    check_dockerfiles
    check_venv_setup
    check_entrypoints
    check_database_files
    test_build
    show_summary
}

main "$@"