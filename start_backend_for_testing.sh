#!/bin/bash

# Django Backend Startup Script for Real Authentication Testing

echo "🚀 Starting JAC Learning Platform with Django Backend..."
echo "================================================"

# 1. Check if Docker is running
echo "📋 Step 1: Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi
echo "✅ Docker is running"

# 2. Check current git status and ensure latest changes
echo "📋 Step 2: Ensuring latest code..."
git status
git pull origin main --allow-unrelated-histories

# 3. Clean build and start services
echo "📋 Step 3: Cleaning and starting services..."
docker-compose down --remove-orphans
docker system prune -f

# 4. Build and start all services
echo "📋 Step 4: Building and starting containers..."
docker-compose up --build -d

# 5. Wait for services to be healthy
echo "📋 Step 5: Waiting for services to be ready..."
echo "   This may take 2-3 minutes on first run..."

# Wait for postgres
echo "   🗄️  Waiting for PostgreSQL..."
timeout 60 docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db
if [ $? -eq 0 ]; then
    echo "   ✅ PostgreSQL is ready"
else
    echo "   ❌ PostgreSQL failed to start"
    exit 1
fi

# Wait for backend
echo "   🔧 Waiting for Django backend..."
for i in {1..30}; do
    if docker-compose exec -T backend python -c "
import sys
sys.path.append('/app')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth.models import User
users = User.objects.filter(is_staff=True).count()
print(f'Django ready with {users} admin users')
" 2>/dev/null; then
        echo "   ✅ Django backend is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "   ❌ Django backend failed to start"
        docker-compose logs backend | tail -20
        exit 1
    fi
    echo "   ⏳ Waiting... ($i/30)"
    sleep 10
done

# 6. Run migrations if needed
echo "📋 Step 6: Ensuring database migrations..."
docker-compose exec -T backend python manage.py migrate --check || \
docker-compose exec -T backend python manage.py migrate

# 7. Create superuser if needed
echo "📋 Step 7: Ensuring admin user exists..."
docker-compose exec -T backend python -c "
import sys
sys.path.append('/app')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'otienocavin@gmail.com', 'admin123')
    print('✅ Admin user created')
else:
    print('✅ Admin user already exists')
"

# 8. Test backend API
echo "📋 Step 8: Testing backend API..."
curl -f -s http://localhost:8000/api/health/ > /dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Backend API is responding"
else
    echo "   ❌ Backend API is not responding"
    echo "   🔍 Checking backend logs..."
    docker-compose logs backend | tail -10
fi

# 9. Show service status
echo "📋 Step 9: Service Status"
docker-compose ps

echo ""
echo "✨ JAC Learning Platform is ready!"
echo "================================"
echo "🔧 Django Backend:  http://localhost:8000"
echo "🎨 Frontend:        http://localhost:3000"
echo "🗄️  Database:        localhost:5432 (jac_user/jac_password)"
echo ""
echo "👤 Admin Credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo "   Email:    otienocavin@gmail.com"
echo ""
echo "🧪 Authentication Testing:"
echo "   1. Test with mock credentials (no backend needed):"
echo "      - demo@example.com / demo123"
echo "      - admin@jac.com / admin123"
echo ""
echo "   2. Test with real backend:"
echo "      - Register new users at /register"
echo "      - Login with any existing credentials"
echo ""