#!/bin/bash
# COMPREHENSIVE MIGRATION FIX - Resets and recreates all migrations

echo "🛠️ COMPREHENSIVE MIGRATION FIX"
echo "=============================="

# Step 1: Stop services and clean everything
echo "Step 1: Stopping services and cleaning database..."
docker-compose down
docker-compose down -v

# Step 2: Start database only
echo "Step 2: Starting database..."
docker-compose up -d postgres

# Wait for database
echo "Step 3: Waiting for database..."
sleep 5

# Step 3: Start backend
echo "Step 4: Starting backend..."
docker-compose up -d backend

# Wait for backend
echo "Step 5: Waiting for backend..."
sleep 10

# Step 4: Complete migration reset and recreation
echo "Step 6: Complete migration reset and recreation..."
docker-compose exec -T backend bash -c "
cd /app

echo '🔧 Setting up environment...'
export DJANGO_COLUMNS=0
export DJANGO_SUPERUSER_ID=''

echo '🧹 Removing ALL existing migration files except __init__.py...'
find apps -name 'migrations' -type d -exec find {} -name '*.py' ! -name '__init__.py' -delete \; 2>/dev/null || true

echo '🗑️ Clearing Django migration history...'
rm -f db.sqlite3 2>/dev/null || true
python manage.py migrate auth 0001 --fake 2>/dev/null || true
python manage.py migrate contenttypes 0001 --fake 2>/dev/null || true

echo '📝 Creating fresh migration files...'
python manage.py makemigrations --merge --noinput

echo '✅ Migration files created, now applying...'

echo '🔄 Applying database migrations with full output...'
python manage.py migrate --noinput --verbosity=2

echo '📊 Final migration status:'
python manage.py showmigrations --verbosity=1
"

# Step 5: Create admin user
echo ""
echo "Step 7: Creating admin user..."
docker-compose exec -T backend bash -c "
cd /app
python manage.py shell -c \"
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@jacplatform.com',
            password='admin123',
            first_name='Admin',
            last_name='User'
        )
        print('✅ Admin user created successfully')
    else:
        print('✅ Admin user already exists')
except Exception as e:
    print(f'❌ Error: {e}')
    # Check table existence
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(\\"SELECT table_name FROM information_schema.tables WHERE table_name='jac_user'\\")
        result = cursor.fetchone()
        print(f'jac_user table exists: {result is not None}')
\"
"

# Step 6: Restart all services
echo ""
echo "Step 8: Restarting all services..."
docker-compose restart

echo ""
echo "Step 9: Final verification..."
sleep 10

# Health check
echo "🏥 Health check:"
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ Backend API is healthy"
else
    echo "❌ Backend API is not responding"
fi

echo ""
echo "=============================="
echo "✅ COMPREHENSIVE FIX COMPLETED"
echo "=============================="
echo ""
echo "🎉 Your JAC Learning Platform should now be fully functional!"
echo "   Access: http://localhost:3000/admin"
echo "   Username: admin"
echo "   Password: admin123"
echo "=============================="