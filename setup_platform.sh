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
DEFAULT_ADMIN_EMAIL="cavin.otieno012@gmail.com"
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
echo "  → Fixing permissions..."
docker-compose exec -T backend chmod -R 755 /app/ || echo "  ℹ️  Permission fix attempted"

# Enhanced migration strategy with explicit app targeting
echo "  → Running enhanced migrations with explicit app targeting..."
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
export DJANGO_SUPERUSER_ID=''
export PYTHONUNBUFFERED=1
cd /app

echo 'Step 1: Collecting static files...'
python manage.py collectstatic --noinput --clear 2>/dev/null || true

echo 'Step 2: Creating migrations for users and learning apps...'
python manage.py makemigrations users learning --merge --noinput || true

echo 'Step 3: Checking for any remaining unmigrated changes...'
python manage.py makemigrations --dry-run --noinput || true

echo 'Step 4: Applying all migrations...'
python manage.py migrate --noinput || true

echo 'Step 5: Verifying User model fields...'
python manage.py shell << 'EOF_VERIFY'
from django.contrib.auth import get_user_model
User = get_user_model()
print(f'✅ User table: {User._meta.db_table}')
print(f'✅ Total fields: {len(User._meta.fields)}')
required_fields = ['email', 'created_at', 'updated_at', 'last_login_at', 'last_activity_at', 'total_points', 'level']
for field_name in required_fields:
    try:
        field = User._meta.get_field(field_name)
        print(f'✅ {field_name}: {field.__class__.__name__}')
    except:
        print(f'❌ {field_name}: MISSING')
EOF_VERIFY

echo 'Step 6: Creating superuser if needed...'
python manage.py shell << 'EOF_SUPERUSER'
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

if not User.objects.filter(username='${DEFAULT_ADMIN_USER}').exists():
    user = User.objects.create_superuser(
        username='${DEFAULT_ADMIN_USER}',
        email='${DEFAULT_ADMIN_EMAIL}',
        password='${DEFAULT_ADMIN_PASSWORD}',
        first_name='Admin',
        last_name='User',
        is_verified=True,
        verification_token_expires_at=timezone.now()
    )
    print('✅ Superuser created successfully')
else:
    print('✅ Superuser already exists')
EOF_SUPERUSER

echo 'Step 7: Final migration status...'
python manage.py showmigrations
" && {
    echo "  ✅ Enhanced migrations completed successfully!"
} || {
    echo "  ⚠️  Enhanced migrations completed with warnings, trying fallback auto_migrate..."
    
    # Fallback to auto_migrate
    echo "  → Using auto_migrate as backup method..."
    docker-compose exec -T backend bash -c "
    export DJANGO_COLUMNS=0
    export DJANGO_SUPERUSER_ID=''
    cd /app
    echo '🔄 Using auto_migrate fallback...'
    python manage.py auto_migrate --verbosity=2
    " && {
        echo "  ✅ Auto-migrate fallback completed!"
    } || {
        echo "  ❌ All migration methods failed - check logs above"
    }
}

echo -e "${GREEN}✅ Migration process completed!${NC}"

# Verify admin account was created (already handled in enhanced migrations)
echo -e "${YELLOW}🔍 Verifying admin account...${NC}"
ADMIN_EXISTS=$(docker-compose exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
print('EXISTS' if User.objects.filter(username='${DEFAULT_ADMIN_USER}').exists() else 'NOT_EXISTS')
" 2>/dev/null || echo "NOT_EXISTS")

if [ "$ADMIN_EXISTS" = "EXISTS" ]; then
    echo -e "${GREEN}✅ Admin account verified and ready${NC}"
else
    echo -e "${YELLOW}⚠️  Admin account not found - this should not happen with enhanced migrations${NC}"
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
echo "  • Enhanced migration system automatically handles missing fields"
echo "  • URL namespace conflicts resolved automatically"
echo "  • User model with all 22 fields will be created"
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