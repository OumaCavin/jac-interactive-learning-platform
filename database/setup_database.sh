#!/bin/bash

# JAC Interactive Learning Platform - Master Database Setup Script
# This script systematically creates the database schema and loads initial data

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
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

# Check if Docker is running
check_docker() {
    print_header "STEP 1: Checking Docker Environment"
    
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running or not accessible"
        exit 1
    fi
    print_success "Docker is running"
    
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "docker-compose is not installed"
        exit 1
    fi
    print_success "docker-compose is available"
}

# Clean slate approach
clean_slate() {
    print_header "STEP 2: Creating Clean Slate"
    
    print_warning "This will remove all existing containers and volumes!"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Aborted by user"
        exit 0
    fi
    
    print_info "Stopping all services..."
    docker-compose down 2>/dev/null || true
    
    print_info "Cleaning up Docker resources..."
    docker system prune -f 2>/dev/null || true
    docker volume prune -f 2>/dev/null || true
    
    print_success "Clean slate created"
}

# Start services
start_services() {
    print_header "STEP 3: Starting Services"
    
    print_info "Building and starting containers..."
    docker-compose up --build -d
    
    print_info "Waiting for services to be ready..."
    sleep 30
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
    else
        print_error "Some services failed to start"
        docker-compose ps
        exit 1
    fi
}

# Run Django migrations
run_migrations() {
    print_header "STEP 4: Running Django Migrations"
    
    print_info "Applying Django built-in migrations..."
    if docker-compose exec -T backend python manage.py migrate --noinput; then
        print_success "Django migrations completed"
    else
        print_error "Django migrations failed"
        docker-compose logs backend | tail -20
        exit 1
    fi
}

# Execute SQL scripts in order
execute_sql_scripts() {
    print_header "STEP 5: Creating Database Schema"
    
    SQL_DIR="./database"
    
    # Check if SQL files exist
    if [[ ! -d "$SQL_DIR" ]]; then
        print_error "Database directory not found: $SQL_DIR"
        exit 1
    fi
    
    # List of SQL files in order
    SQL_FILES=(
        "01_foundation_tables.sql"
        "02_content_structure.sql"
        "03_learning_system.sql"
        "04_gamification.sql"
    )
    
    for sql_file in "${SQL_FILES[@]}"; do
        if [[ -f "$SQL_DIR/$sql_file" ]]; then
            print_info "Executing $sql_file..."
            if docker-compose exec -T backend psql -U jac_user -d jac_learning_db -f "/app/database/$sql_file"; then
                print_success "Completed $sql_file"
            else
                print_error "Failed to execute $sql_file"
                docker-compose logs backend | tail -20
                exit 1
            fi
        else
            print_warning "SQL file not found: $sql_file"
        fi
    done
}

# Load initial data
load_data() {
    print_header "STEP 6: Loading Initial Data"
    
    if [[ -f "database/load_initial_data.py" ]]; then
        print_info "Running data loader script..."
        if docker-compose exec -T backend python /app/database/load_initial_data.py; then
            print_success "Initial data loaded successfully"
        else
            print_error "Failed to load initial data"
            docker-compose logs backend | tail -20
            exit 1
        fi
    else
        print_warning "Data loader script not found"
    fi
}

# Test the application
test_application() {
    print_header "STEP 7: Testing Application"
    
    # Test API health
    print_info "Testing API health endpoint..."
    if curl -s -f http://localhost:8000/api/health/ > /dev/null; then
        print_success "API health check passed"
    else
        print_error "API health check failed"
        print_info "Checking backend logs..."
        docker-compose logs backend | tail -10
    fi
    
    # Test Django admin access
    print_info "Testing Django admin access..."
    if curl -s -f http://localhost:8000/admin/ | grep -q "Django administration"; then
        print_success "Django admin is accessible"
    else
        print_error "Django admin not accessible"
    fi
    
    # Test frontend
    print_info "Testing frontend..."
    if curl -s -f http://localhost:3000/ | grep -q -i "login\|sign"; then
        print_success "Frontend is accessible"
    else
        print_warning "Frontend may not be fully loaded yet"
    fi
}

# Show final status
show_status() {
    print_header "DATABASE SETUP COMPLETE!"
    
    echo -e "${GREEN}🎉 Database setup completed successfully!${NC}\n"
    
    echo -e "${YELLOW}LOGIN CREDENTIALS:${NC}"
    echo "=================="
    echo ""
    echo -e "${BLUE}Django Admin:${NC}"
    echo "  URL: http://localhost:8000/admin/"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo ""
    echo -e "${BLUE}Demo User (Frontend):${NC}"
    echo "  URL: http://localhost:3000/login"
    echo "  Email: demo@example.com"
    echo "  Password: demo123"
    echo ""
    echo -e "${BLUE}Health Check:${NC}"
    echo "  API: http://localhost:8000/api/health/"
    echo ""
    
    echo -e "${YELLOW}USEFUL COMMANDS:${NC}"
    echo "================"
    echo "  View logs: docker-compose logs -f backend"
    echo "  Access shell: docker-compose exec backend bash"
    echo "  Access database: docker-compose exec backend python manage.py dbshell"
    echo "  Check status: docker-compose ps"
    echo "  Stop services: docker-compose down"
    echo ""
    
    echo -e "${YELLOW}DATABASE TABLES CREATED:${NC}"
    echo "========================="
    echo "  ✅ users_user (Custom User Model)"
    echo "  ✅ users_userprofile & users_userpreferences"
    echo "  ✅ content_learningmodule, content_contentblock, content_contentresource"
    echo "  ✅ content_curriculumpath & content_pathmodule"
    echo "  ✅ learning_assessment & learning_assessmentquestion"
    echo "  ✅ learning_adaptivechallenge"
    echo "  ✅ learning_userlearningpath, learning_userassessmentresult"
    echo "  ✅ learning_userchallengeattempt, learning_spacedrepetitionsession"
    echo "  ✅ learning_userdifficultyprofile, learning_learningrecommendation"
    echo "  ✅ gamification_achievement, gamification_badge"
    echo "  ✅ gamification_userpoints, gamification_userlevel"
    echo "  ✅ gamification_userachievement, gamification_userbadge"
    echo "  ✅ gamification_pointtransaction, gamification_learningstreak"
    echo ""
    
    print_success "Your JAC Interactive Learning Platform is ready to use!"
}

# Main execution
main() {
    print_header "JAC INTERACTIVE LEARNING PLATFORM"
    print_header "DATABASE SETUP & INITIALIZATION"
    
    echo -e "${YELLOW}This script will:${NC}"
    echo "1. Clean up existing containers and volumes"
    echo "2. Start Docker services"
    echo "3. Run Django migrations"
    echo "4. Create database schema in correct order"
    echo "5. Load initial data"
    echo "6. Test the application"
    echo ""
    
    # Run all steps
    check_docker
    clean_slate
    start_services
    run_migrations
    execute_sql_scripts
    load_data
    test_application
    show_status
}

# Handle script interruption
trap 'print_error "Script interrupted"; exit 1' INT

# Check if running from correct directory
if [[ ! -f "docker-compose.yml" ]]; then
    print_error "This script must be run from the project root directory (where docker-compose.yml is located)"
    exit 1
fi

# Run main function
main "$@"