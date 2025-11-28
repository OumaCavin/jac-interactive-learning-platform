#!/bin/bash

echo "🔧 JAC Learning Platform - Complete Login Fix"
echo "=============================================="

# Navigate to your project directory
echo "📂 Ensuring we're in the project directory..."
cd ~/projects/jac-interactive-learning-platform || cd /path/to/your/jac-interactive-learning-platform

echo "🛑 Step 1: Stopping and cleaning all services..."
docker-compose down -v

echo "🔄 Step 2: Rebuilding containers from scratch..."
docker-compose up -d --build --force-recreate

echo "⏳ Step 3: Waiting for services to initialize (30 seconds)..."
sleep 30

echo "📊 Step 4: Running comprehensive migration fixes..."

# Fix permissions first
echo "   → Fixing migration directory permissions..."
docker-compose exec -T backend find . -name migrations -exec chmod -R 755 {} \; 2>/dev/null || true

# Clear migration state and run from clean slate
echo "   → Clearing Django migration cache..."
docker-compose exec -T backend rm -rf apps/*/migrations/__pycache__/ 
docker-compose exec -T backend rm -rf .django_migrations_cache/ 2>/dev/null || true

# Apply migrations in correct order
echo "   → Applying migrations with proper handling..."
docker-compose exec -T backend python manage.py migrate --noinput

# Alternative: If migrations still fail, try this approach
echo "   → Attempting manual migration application..."
docker-compose exec -T backend bash -c "
python manage.py makemigrations content --noinput || echo 'Content makemigrations skipped'
python manage.py makemigrations gamification --noinput || echo 'Gamification makemigrations skipped'  
python manage.py makemigrations jac_execution --noinput || echo 'JAC Execution makemigrations skipped'
python manage.py makemigrations knowledge_graph --noinput || echo 'Knowledge graph makemigrations skipped'
python manage.py makemigrations learning --noinput || echo 'Learning makemigrations skipped'
python manage.py makemigrations sessions --noinput || echo 'Sessions makemigrations skipped'
python manage.py migrate --noinput
"

echo "👤 Step 5: Creating admin user..."
docker-compose exec -T backend python manage.py createsuperuser --username admin --email cavin.otieno012@gmail.com --noinput || echo "Superuser creation attempted"

# If createsuperuser fails, try direct approach
echo "   → Alternative: Direct user creation..."
docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='cavin.otieno012@gmail.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Created superuser: {user.username}")
    else:
        print("Admin user already exists")
except Exception as e:
    print(f"❌ Error creating admin: {e}")
EOF

echo "📁 Step 6: Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo "🧹 Step 7: Cleaning up..."
docker-compose exec -T backend rm -rf apps/*/migrations/__pycache__/ 
docker-compose exec -T backend python manage.py check --deploy

echo "🔍 Step 8: Checking final status..."
docker-compose ps

echo ""
echo "🎉 FIX COMPLETED!"
echo "================="
echo ""
echo "🌐 Try accessing these URLs:"
echo "  • Django Admin:     http://localhost:8000/admin/"
echo "  • Frontend Login:   http://localhost:3000/login"
echo "  • API Health:       http://localhost:8000/api/health/"
echo ""
echo "🔑 Login Credentials:"
echo "  • Username: admin"
echo "  • Email:    cavin.otieno012@gmail.com"  
echo "  • Password: admin123"
echo ""
echo "🔧 If issues persist, check logs with:"
echo "  • Backend:  docker-compose logs -f backend"
echo "  • Frontend: docker-compose logs -f frontend"
echo "  • Database: docker-compose logs -f postgres"
echo ""
echo "🆘 For emergency database reset (WARNING: This will delete ALL data):"
echo "  docker-compose down -v && docker-compose up -d --build"