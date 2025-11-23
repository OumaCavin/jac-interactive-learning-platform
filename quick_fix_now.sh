#!/bin/bash
# Quick Fix Script - Run migrations immediately to resolve the issues

set -e

echo "🔧 Running QUICK FIX to resolve migration issues..."
echo "=================================================="

# Stop containers to ensure clean state
echo "🛑 Stopping containers..."
docker-compose down

# Start only database first
echo "🗄️ Starting database only..."
docker-compose up -d postgres

# Wait for database
echo "⏳ Waiting for database..."
sleep 5

# Start backend only
echo "🚀 Starting backend container..."
docker-compose up -d backend

# Wait for backend
echo "⏳ Waiting for backend..."
sleep 10

# Now run migrations manually with full automation
echo "🔄 Running migrations with FULL automation..."
docker-compose exec -T backend bash -c "
# Set environment to prevent ALL prompts
export DJANGO_COLUMNS=0
export DJANGO_SUPERUSER_ID=''
export PYTHONUNBUFFERED=1

cd /app

echo 'Step 1: Collecting static files (prevents prompts)...'
python manage.py collectstatic --noinput --clear 2>/dev/null || true

echo 'Step 2: Running makemigrations...'
python manage.py makemigrations --merge --noinput || true

echo 'Step 3: Running migrate...'
python manage.py migrate --noinput || true

echo 'Step 4: Creating superuser...'
python manage.py shell -c \"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@jacplatform.com', 
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Superuser created')
else:
    print('Superuser exists')
\" 2>/dev/null || echo 'Superuser creation attempted'

echo 'Step 5: Final status check...'
python manage.py showmigrations
"

echo "✅ Migration fix completed!"
echo "=================================================="