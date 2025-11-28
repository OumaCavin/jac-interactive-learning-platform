#!/bin/bash

echo "🔧 JAC Learning Platform - Login Issues Fix Script"
echo "================================================"

# Stop all containers
echo "🛑 Step 1: Stopping all services..."
docker-compose down

# Clean database completely 
echo "🗑️  Step 2: Cleaning database..."
docker-compose down -v

# Rebuild containers
echo "🏗️  Step 3: Rebuilding containers..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Step 4: Waiting for services to initialize..."
sleep 15

# Apply migrations with proper handling
echo "📊 Step 5: Applying migrations..."
docker-compose exec -T backend python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "👤 Step 6: Creating superuser..."
docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from apps.users.models import User as CustomUser

User = get_user_model()

# Check if admin exists
try:
    admin = User.objects.get(username='admin')
    print("Admin user already exists")
except User.DoesNotExist:
    # Create superuser with custom user model
    admin = CustomUser.objects.create_superuser(
        username='admin',
        email='cavin.otieno012@gmail.com', 
        password='admin123'
    )
    print(f"Created superuser: {admin.username}")
except Exception as e:
    print(f"Error creating admin: {e}")
EOF

# Collect static files
echo "📁 Step 7: Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

# Verify services
echo "✅ Step 8: Verifying service status..."
docker-compose ps

echo ""
echo "🎉 Fix completed! Try accessing:"
echo "  • Django Admin: http://localhost:8000/admin/"
echo "  • Frontend Login: http://localhost:3000/login"
echo ""
echo "🔑 Login Credentials:"
echo "  • Username: admin"
echo "  • Email: cavin.otieno012@gmail.com"  
echo "  • Password: admin123"
echo ""
echo "🔍 Check logs with: docker-compose logs -f backend"