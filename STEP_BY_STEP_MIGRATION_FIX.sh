#!/bin/bash
# STEP-BY-STEP MIGRATION FIX
# This script will fix the missing migration files and complete the setup

echo "🔧 STEP-BY-STEP MIGRATION FIX"
echo "=============================="

# Step 1: Generate missing migration files
echo "Step 1: Generating missing migration files..."
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
cd /app

echo '🧹 Cleaning existing migration files for users and learning...'
find apps/users/migrations -name '*.py' ! -name '__init__.py' -delete 2>/dev/null || true
find apps/learning/migrations -name '*.py' ! -name '__init__.py' -delete 2>/dev/null || true

echo '📝 Creating fresh migration files...'
python manage.py makemigrations users --noinput
echo '✅ Users app migrations created'

python manage.py makemigrations learning --noinput  
echo '✅ Learning app migrations created'

python manage.py makemigrations --merge --noinput
echo '✅ Merged migrations created'

echo '📊 Current migration status:'
python manage.py showmigrations
"

# Step 2: Apply all migrations
echo ""
echo "Step 2: Applying all migrations..."
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
cd /app

echo '🔄 Applying database migrations...'
python manage.py migrate --noinput

echo '📊 Final migration status:'
python manage.py showmigrations
"

# Step 3: Create admin user
echo ""
echo "Step 3: Creating admin user..."
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
cd /app

echo '👤 Creating admin user...'
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
    print(f'❌ Error creating admin: {e}')
    # Try to verify if jac_user table exists
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(\\"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='jac_user'\\")
        table_exists = cursor.fetchone()
        print(f'jac_user table exists: {table_exists is not None}')
\"
"

echo ""
echo "Step 4: Verifying final status..."
docker-compose exec -T backend python manage.py showmigrations

echo ""
echo "=============================="
echo "✅ STEP-BY-STEP FIX COMPLETED"
echo "=============================="