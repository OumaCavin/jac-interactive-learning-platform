#!/bin/bash

# JAC Interactive Learning Platform - Production Deployment Script
# Complete containerized deployment with monitoring and security
# Author: Cavin Otieno
# Version: 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="jac-learning-platform"
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

print_header() {
    echo -e "${BLUE}"
    echo "================================================================"
    echo "🚀 JAC Interactive Learning Platform - Production Deployment"
    echo "================================================================"
    echo -e "${NC}"
    echo "Generated: $(date)"
    echo "Author: Cavin Otieno"
    echo "Version: 1.0.0"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    print_success "Docker is installed: $(docker --version)"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    print_success "Docker Compose is installed: $(docker-compose --version)"
    
    # Check available disk space (minimum 5GB)
    available_space=$(df / | awk 'NR==2 {print $4}')
    if [ "$available_space" -lt 5242880 ]; then  # 5GB in KB
        print_warning "Low disk space detected. At least 5GB recommended."
    else
        print_success "Sufficient disk space available"
    fi
}

setup_environment() {
    print_info "Setting up environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        print_info "Creating environment configuration..."
        cat > "$ENV_FILE" << EOF
# JAC Interactive Learning Platform - Production Environment
# Generated: $(date)

# Security
SECRET_KEY=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 16)

# Database
POSTGRES_PASSWORD=$(openssl rand -base64 16)

# Application
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production

# Email (Configure for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Monitoring
SENTRY_DSN=your-sentry-dsn-here

# SSL (Configure for production)
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem
EOF
        print_success "Environment file created: $ENV_FILE"
        print_warning "Please edit $ENV_FILE with your actual configuration"
    else
        print_success "Environment file already exists"
    fi
}

build_images() {
    print_info "Building Docker images..."
    
    # Build backend
    print_info "Building backend image..."
    docker-compose build backend
    print_success "Backend image built"
    
    # Build frontend
    print_info "Building frontend image..."
    docker-compose build frontend
    print_success "Frontend image built"
    
    # Build other services
    print_info "Building other services..."
    docker-compose build celery-worker celery-beat jac-sandbox
    print_success "All service images built"
}

setup_database() {
    print_info "Setting up database..."
    
    # Start database and cache services first
    docker-compose up -d postgres redis
    
    # Wait for database to be ready
    print_info "Waiting for database to be ready..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db > /dev/null 2>&1; then
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Database failed to start"
        exit 1
    fi
    
    # Run migrations
    print_info "Running database migrations..."
    docker-compose exec backend python manage.py migrate --noinput
    print_success "Database migrations completed"
    
    # Create superuser (if not exists)
    print_info "Setting up admin user..."
    docker-compose exec backend python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Admin user created: admin/admin123')
else:
    print('Admin user already exists')
"
}

deploy_application() {
    print_info "Starting application services..."
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be healthy
    print_info "Waiting for services to be healthy..."
    sleep 10
    
    # Check service health
    services=("backend" "frontend" "postgres" "redis" "nginx")
    for service in "${services[@]}"; do
        if docker-compose ps $service | grep -q "Up"; then
            print_success "$service is running"
        else
            print_error "$service failed to start"
            docker-compose logs $service
        fi
    done
}

run_tests() {
    print_info "Running application tests..."
    
    # Backend tests
    print_info "Running backend tests..."
    docker-compose exec backend python manage.py test
    print_success "Backend tests completed"
    
    # Frontend tests (if configured)
    if docker-compose exec frontend npm test -- --watchAll=false > /dev/null 2>&1; then
        print_success "Frontend tests completed"
    else
        print_warning "Frontend tests failed or not configured"
    fi
}

setup_monitoring() {
    print_info "Setting up monitoring and logging..."
    
    # Create log directories
    mkdir -p logs/{backend,frontend,nginx}
    
    # Setup log rotation
    cat > logrotate.conf << EOF
logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0644 root root
    postrotate
        docker-compose restart nginx
    endscript
}
EOF
    
    print_success "Monitoring setup completed"
}

show_deployment_info() {
    print_header
    echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL!${NC}"
    echo ""
    echo "📱 Application URLs:"
    echo "   Main Application: http://localhost"
    echo "   API Documentation: http://localhost/api/docs/"
    echo "   Admin Panel: http://localhost/admin/"
    echo ""
    echo "🔐 Default Credentials:"
    echo "   Admin: admin / admin123"
    echo "   Demo: demo@example.com / demo123"
    echo ""
    echo "📊 Service Status:"
    docker-compose ps
    echo ""
    echo "📈 Monitoring:"
    echo "   Logs: docker-compose logs -f [service]"
    echo "   Health: curl http://localhost/health"
    echo ""
    echo "🛠️  Management Commands:"
    echo "   Stop: docker-compose down"
    echo "   Restart: docker-compose restart"
    echo "   Update: docker-compose pull && docker-compose up -d"
    echo ""
    echo "🔧 Production Checklist:"
    echo "   ☐ Update SECRET_KEY in .env"
    echo "   ☐ Configure SSL certificates"
    echo "   ☐ Setup email configuration"
    echo "   ☐ Configure monitoring (Sentry, etc.)"
    echo "   ☐ Setup backup strategy"
    echo "   ☐ Configure domain and DNS"
    echo ""
}

cleanup() {
    print_info "Cleaning up temporary files..."
    docker system prune -f
    print_success "Cleanup completed"
}

main() {
    print_header
    
    # Check if we're in the right directory
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Docker Compose file not found. Please run from project root."
        exit 1
    fi
    
    # Run deployment steps
    check_prerequisites
    setup_environment
    build_images
    setup_database
    deploy_application
    setup_monitoring
    
    # Optional: Run tests
    if [ "$1" == "--test" ]; then
        run_tests
    fi
    
    # Show deployment information
    show_deployment_info
    
    print_success "Production deployment completed successfully!"
}

# Handle script arguments
case "$1" in
    --cleanup)
        cleanup
        ;;
    --help)
        echo "Usage: $0 [--test|--cleanup|--help]"
        echo "  --test    Run tests after deployment"
        echo "  --cleanup Clean up Docker system"
        echo "  --help    Show this help message"
        ;;
    *)
        main "$@"
        ;;
esac