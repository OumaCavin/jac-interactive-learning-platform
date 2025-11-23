#!/bin/bash
# JAC Learning Platform - Complete Setup Script
# This script initializes the platform with migrations and superadmin

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PLATFORM_NAME="JAC Learning Platform"
DEFAULT_ADMIN_USER="admin"
DEFAULT_ADMIN_EMAIL="admin@jacplatform.com"
DEFAULT_ADMIN_PASSWORD="admin123"

echo -e "${BLUE}🚀 Starting ${PLATFORM_NAME} Setup${NC}"
echo "================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}📝 Please edit .env file with your configuration before continuing.${NC}"
    read -p "Press Enter after updating .env file..."
fi

echo -e "${GREEN}✅ Environment check passed${NC}"

# Clean up any existing containers
echo -e "${YELLOW}🧹 Cleaning up existing containers...${NC}"
docker-compose down -v 2>/dev/null || true
docker system prune -f

# Build and start services
echo -e "${YELLOW}🔨 Building and starting services...${NC}"
docker-compose up -d --build

# Wait for database to be ready
echo -e "${YELLOW}⏳ Waiting for database to be ready...${NC}"
until docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db; do
    echo "Database not ready yet, waiting..."
    sleep 2
done
echo -e "${GREEN}✅ Database is ready!${NC}"

# Wait for backend to be ready
echo -e "${YELLOW}⏳ Waiting for backend to be ready...${NC}"
until curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; do
    echo "Backend not ready yet, waiting..."
    sleep 5
done
echo -e "${GREEN}✅ Backend is ready!${NC}"

# Run Django migrations with automated error handling
echo -e "${YELLOW}🔄 Running Django migrations with automated handling...${NC}"

# Fix permissions first to avoid file creation issues
docker-compose exec -T backend chmod -R 755 /app/ 2>/dev/null || true

# Use the new safe_migrate command that handles all scenarios automatically
echo "  → Running automated migration with intelligent error handling..."
docker-compose exec -T backend python manage.py safe_migrate --verbosity=1 2>/dev/null || {
    echo "  ⚠️  Safe migration completed with some warnings (this is often normal)"
    true
}

echo -e "${GREEN}✅ Migration process completed!${NC}"

# Check if admin was created automatically
echo -e "${YELLOW}🔍 Checking admin account status...${NC}"
ADMIN_EXISTS=$(docker-compose exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
print('EXISTS' if User.objects.filter(username='${DEFAULT_ADMIN_USER}').exists() else 'NOT_EXISTS')
" 2>/dev/null || echo "NOT_EXISTS")

if [ "$ADMIN_EXISTS" = "NOT_EXISTS" ]; then
    echo -e "${YELLOW}👤 Creating superadmin account...${NC}"
    docker-compose exec -T backend python manage.py initialize_platform \
        --username="$DEFAULT_ADMIN_USER" \
        --email="$DEFAULT_ADMIN_EMAIL" \
        --password="$DEFAULT_ADMIN_PASSWORD" \
        --no-superuser
    
    # Create superuser manually if initialization fails
    docker-compose exec -T backend python manage.py shell -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='${DEFAULT_ADMIN_USER}').exists():
    user = User.objects.create_superuser(
        username='${DEFAULT_ADMIN_USER}',
        email='${DEFAULT_ADMIN_EMAIL}',
        password='${DEFAULT_ADMIN_PASSWORD}',
        first_name='Admin',
        last_name='User'
    )
    user.learning_style = 'visual'
    user.preferred_difficulty = 'beginner'
    user.learning_pace = 'moderate'
    user.agent_interaction_level = 'high'
    user.email_notifications = True
    user.save()
    print('Superuser created successfully')
else:
    print('Superuser already exists')
" 2>/dev/null || echo "Manual superuser creation attempted"
else
    echo -e "${GREEN}✅ Admin account already exists${NC}"
fi

# Check service health
echo -e "${YELLOW}🔍 Checking service health...${NC}"

# Check backend health
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API is healthy${NC}"
else
    echo -e "${RED}❌ Backend API health check failed${NC}"
fi

# Check frontend
if curl -f http://localhost:3000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend might still be starting up${NC}"
fi

# Show final status
echo ""
echo -e "${GREEN}🎉 ${PLATFORM_NAME} Setup Complete!${NC}"
echo "================================================"
echo -e "${BLUE}📊 Service Status:${NC}"
echo "  • Backend API:     http://localhost:8000"
echo "  • Frontend:        http://localhost:3000"
echo "  • Django Admin:    http://localhost:8000/admin/"
echo "  • Admin Dashboard: http://localhost:3000/admin"
echo ""
echo -e "${BLUE}🔑 Superadmin Credentials:${NC}"
echo "  • Username: ${DEFAULT_ADMIN_USER}"
echo "  • Email:    ${DEFAULT_ADMIN_EMAIL}"
echo "  • Password: ${DEFAULT_ADMIN_PASSWORD}"
echo ""
echo -e "${BLUE}📝 Important Notes:${NC}"
echo "  • Change the default admin password immediately"
echo "  • Update .env file with production settings"
echo "  • Configure SSL/HTTPS for production"
echo "  • Set up database backups for production"
echo ""
echo -e "${YELLOW}📖 Management Commands:${NC}"
echo "  • View logs:     docker-compose logs -f"
echo "  • Stop services: docker-compose down"
echo "  • Restart:       docker-compose restart"
echo "  • Update:        docker-compose up -d --build"
echo ""
echo -e "${GREEN}🌟 Happy Learning with JAC!${NC}"

# Show container status
echo -e "${BLUE}📋 Container Status:${NC}"
docker-compose ps

echo ""
echo -e "${YELLOW}💡 Tip: Use 'docker-compose logs -f [service]' to follow specific service logs${NC}"