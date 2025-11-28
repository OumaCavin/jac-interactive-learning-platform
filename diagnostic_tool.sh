#!/bin/bash

echo "🔍 JAC PLATFORM DIAGNOSTIC TOOL"
echo "==============================="

cd ~/projects/jac-interactive-learning-platform 2>/dev/null || echo "❌ Project directory not found"

echo "📊 Container Status:"
docker-compose ps

echo ""
echo "🔧 Service Health Check:"
echo "  Backend:  $(curl -s http://localhost:8000/api/health/ | grep -o '"status":"[^"]*"' | head -1 || echo 'OFFLINE')"
echo "  Frontend: $(curl -s -I http://localhost:3000/login | head -1 | grep -o '200\|OK' || echo 'OFFLINE')"

echo ""
echo "🗄️  Database Tables Check:"
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -c "\dt" | grep -E "(user_points|UserPoints|django_celery)" || echo "⚠️  Critical tables missing"

echo ""
echo "🔄 Migration Status:"
docker-compose exec -T backend python manage.py showmigrations | grep -E "\[X\]|\[ \]" | head -20

echo ""
echo "👤 Admin User Check:"
docker-compose exec -T backend python manage.py shell -c "
from django.contrib.auth.models import User
try:
    admin = User.objects.get(username='admin')
    print(f'✅ Admin exists: {admin.username}, Email: {admin.email}, Active: {admin.is_active}')
except User.DoesNotExist:
    print('❌ Admin user does not exist')
except Exception as e:
    print(f'❌ Error checking admin: {e}')
"

echo ""
echo "🔍 Recent Backend Errors:"
docker-compose logs --tail=20 backend | grep -i error | tail -5

echo ""
echo "🛠️  QUICK FIX COMMANDS:"
echo "======================="
echo ""
echo "🚨 If containers are down:"
echo "  docker-compose up -d --build"
echo ""
echo "🔄 If migrations are broken:"
echo "  docker-compose down -v && docker-compose up -d --build"
echo ""
echo "🧹 If you need clean start:"
echo "  ./final_login_fix.sh"
echo ""
echo "📋 If admin user missing:"
echo "  docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "🔍 Debug specific issues:"
echo "  docker-compose logs backend"
echo "  docker-compose exec backend python manage.py check"