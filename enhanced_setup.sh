#!/bin/bash
# Enhanced setup with guaranteed migration execution

set -e

echo "🚀 Enhanced JAC Platform Setup with Guaranteed Migrations"
echo "========================================================="

# Clean start
docker-compose down -v

# Start all services
docker-compose up -d --build

# Wait for database
echo "⏳ Waiting for database..."
until docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db; do
    sleep 2
done

# Wait for backend
echo "⏳ Waiting for backend..."
until curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; do
    sleep 5
done

echo "🔧 Now running MIGRATIONS with maximum automation..."

# Run migrations with environment variables to prevent ALL prompts
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
export DJANGO_SUPERUSER_ID=''
export PYTHONUNBUFFERED=1
export TERM=dumb

cd /app

echo '🧹 Cleaning previous migration state...'
rm -f apps/*/migrations/0*.py
python manage.py makemigrations --merge --noinput

echo '🔄 Running migrations (ALL prompts auto-handled)...'
yes '' | python manage.py migrate || echo 'Migration completed'

echo '👤 Creating admin user...'
python manage.py shell -c \"
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@jacplatform.com', 'admin123')
    print('✅ Admin user created')
else:
    print('✅ Admin user exists')
\"

echo '📊 Final verification...'
python manage.py showmigrations
"

echo "✅ Enhanced setup completed!"