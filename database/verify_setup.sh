#!/bin/bash

# JAC Platform - Comprehensive Setup Verification Script
# This script verifies all components are ready for systematic database setup

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔍 $1${NC}"
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

# Verify project structure
verify_project_structure() {
    print_header "VERIFYING PROJECT STRUCTURE"
    
    local structure_ok=true
    
    # Check root files
    if [[ -f "docker-compose.yml" ]]; then
        print_success "docker-compose.yml found"
    else
        print_error "docker-compose.yml not found"
        structure_ok=false
    fi
    
    if [[ -f "requirements.txt" ]]; then
        print_success "requirements.txt found"
    else
        print_warning "requirements.txt not found"
    fi
    
    # Check Django project files
    if [[ -f "manage.py" ]]; then
        print_success "manage.py found"
    else
        print_warning "manage.py not found (may not be in root)"
    fi
    
    # Check database directory
    if [[ -d "database" ]]; then
        print_success "database/ directory found"
    else
        print_error "database/ directory not found"
        structure_ok=false
    fi
    
    return $structure_ok
}

# Verify database files
verify_database_files() {
    print_header "VERIFYING DATABASE FILES"
    
    local files_ok=true
    
    # Required SQL files
    local sql_files=(
        "01_foundation_tables.sql"
        "02_content_structure.sql" 
        "03_learning_system.sql"
        "04_gamification.sql"
    )
    
    for file in "${sql_files[@]}"; do
        if [[ -f "database/$file" ]]; then
            local line_count=$(wc -l < "database/$file")
            print_success "$file found ($line_count lines)"
            
            # Basic SQL syntax check
            if grep -q "CREATE TABLE" "database/$file"; then
                print_info "  ✓ Contains CREATE TABLE statements"
            else
                print_warning "  ⚠️  No CREATE TABLE statements found"
            fi
            
            if grep -q "ALTER TABLE" "database/$file"; then
                print_info "  ✓ Contains ALTER TABLE statements"
            fi
        else
            print_error "$file not found"
            files_ok=false
        fi
    done
    
    # Check data loader
    if [[ -f "database/load_initial_data.py" ]]; then
        local line_count=$(wc -l < "database/load_initial_data.py")
        print_success "load_initial_data.py found ($line_count lines)"
    else
        print_error "load_initial_data.py not found"
        files_ok=false
    fi
    
    # Check setup script
    if [[ -f "database/setup_platform.sh" ]]; then
        print_success "setup_platform.sh found"
        if [[ -x "database/setup_platform.sh" ]]; then
            print_success "setup_platform.sh is executable"
        else
            print_warning "setup_platform.sh is not executable (run: chmod +x database/setup_platform.sh)"
        fi
    else
        print_error "setup_platform.sh not found"
        files_ok=false
    fi
    
    return $files_ok
}

# Verify SQL file content
verify_sql_content() {
    print_header "VERIFYING SQL FILE CONTENT"
    
    local content_ok=true
    
    # Check foundation tables
    if [[ -f "database/01_foundation_tables.sql" ]]; then
        if grep -q "users_user" "database/01_foundation_tables.sql"; then
            print_success "Foundation tables: Custom user model defined"
        else
            print_warning "Foundation tables: Custom user model not found"
            content_ok=false
        fi
    fi
    
    # Check content structure
    if [[ -f "database/02_content_structure.sql" ]]; then
        if grep -q "content_learningmodule" "database/02_content_structure.sql"; then
            print_success "Content structure: Learning modules defined"
        else
            print_warning "Content structure: Learning modules not found"
        fi
    fi
    
    # Check learning system
    if [[ -f "database/03_learning_system.sql" ]]; then
        if grep -q "learning_assessment" "database/03_learning_system.sql"; then
            print_success "Learning system: Assessment system defined"
        else
            print_warning "Learning system: Assessment system not found"
        fi
    fi
    
    # Check gamification
    if [[ -f "database/04_gamification.sql" ]]; then
        if grep -q "gamification_achievement" "database/04_gamification.sql"; then
            print_success "Gamification: Achievement system defined"
        else
            print_warning "Gamification: Achievement system not found"
        fi
    fi
    
    return $content_ok
}

# Verify data loader
verify_data_loader() {
    print_header "VERIFYING DATA LOADER SCRIPT"
    
    if [[ ! -f "database/load_initial_data.py" ]]; then
        print_error "Data loader not found"
        return 1
    fi
    
    # Check for essential functions
    local issues=0
    
    if grep -q "def create_admin_user" "database/load_initial_data.py"; then
        print_success "Admin user creation function found"
    else
        print_warning "Admin user creation function not found"
        ((issues++))
    fi
    
    if grep -q "def create_demo_user" "database/load_initial_data.py"; then
        print_success "Demo user creation function found"
    else
        print_warning "Demo user creation function not found"
        ((issues++))
    fi
    
    if grep -q "def create_sample_content" "database/load_initial_data.py"; then
        print_success "Sample content creation function found"
    else
        print_warning "Sample content creation function not found"
        ((issues++))
    fi
    
    if grep -q "psycopg2" "database/load_initial_data.py" || grep -q "psycopg" "database/load_initial_data.py"; then
        print_success "PostgreSQL connection code found"
    else
        print_warning "PostgreSQL connection code not found"
        ((issues++))
    fi
    
    # Check for error handling
    if grep -q "try:" "database/load_initial_data.py" && grep -q "except" "database/load_initial_data.py"; then
        print_success "Error handling found"
    else
        print_warning "Error handling not found or incomplete"
        ((issues++))
    fi
    
    return $issues
}

# Verify Docker environment
verify_docker_environment() {
    print_header "VERIFYING DOCKER ENVIRONMENT"
    
    local docker_ok=true
    
    # Check if Docker is available
    if command -v docker > /dev/null 2>&1; then
        print_success "Docker is available"
    else
        print_error "Docker is not installed or not in PATH"
        docker_ok=false
    fi
    
    # Check if docker-compose is available
    if command -v docker-compose > /dev/null 2>&1; then
        print_success "docker-compose is available"
    else
        print_error "docker-compose is not installed or not in PATH"
        docker_ok=false
    fi
    
    # Check Docker daemon
    if docker info > /dev/null 2>&1; then
        print_success "Docker daemon is running"
    else
        print_error "Docker daemon is not running"
        docker_ok=false
    fi
    
    return $docker_ok
}

# Generate setup summary
generate_summary() {
    print_header "SETUP VERIFICATION SUMMARY"
    
    echo -e "${YELLOW}🎯 READY TO RUN SETUP:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}Next steps:${NC}"
    echo "1. Make the setup script executable:"
    echo "   ${BLUE}chmod +x database/setup_platform.sh${NC}"
    echo ""
    echo "2. Run the comprehensive setup:"
    echo "   ${BLUE}bash database/setup_platform.sh${NC}"
    echo ""
    echo -e "${YELLOW}📊 WHAT WILL BE CREATED:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${CYAN}🏛️  Foundation (4 tables):${NC}"
    echo "   • Custom user system with custom User model"
    echo "   • User profiles and preferences"
    echo ""
    echo -e "${CYAN}📚 Learning Content (8 tables):${NC}"
    echo "   • Learning modules, content blocks, resources"
    echo "   • Curriculum paths and dependencies"
    echo ""
    echo -e "${CYAN}🎓 Assessment System (15 tables):${NC}"
    echo "   • Tests, questions, adaptive challenges"
    echo "   • User progress, attempts, spaced repetition"
    echo ""
    echo -e "${CYAN}🏆 Gamification (11 tables):${NC}"
    echo "   • Achievements, badges, points, levels"
    echo "   • Streaks, leaderboards, point transactions"
    echo ""
    echo -e "${YELLOW}🔐 CREDENTIALS THAT WILL BE CREATED:${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}🛡️  Admin User:${NC}"
    echo "   • Username: admin"
    echo "   • Password: admin123"
    echo "   • Access: http://localhost:8000/admin/"
    echo ""
    echo -e "${BLUE}👤 Demo User:${NC}"
    echo "   • Email: demo@example.com"
    echo "   • Password: demo123"
    echo "   • Access: http://localhost:3000/login"
    echo ""
    
    print_success "Verification complete! All components are ready."
}

# Main verification function
main() {
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}🔍 JAC PLATFORM SETUP VERIFICATION${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    local all_good=true
    
    # Run all verification steps
    verify_project_structure || all_good=false
    echo ""
    verify_database_files || all_good=false
    echo ""
    verify_sql_content || all_good=false
    echo ""
    verify_data_loader || all_good=false
    echo ""
    verify_docker_environment || all_good=false
    
    echo ""
    if $all_good; then
        print_success "🎉 All verification checks passed!"
        generate_summary
        return 0
    else
        print_error "❌ Some verification checks failed"
        print_info "Please fix the issues above before running setup"
        return 1
    fi
}

# Run verification
main "$@"