#!/bin/bash
# DATABASE DEBUG SCRIPT - Check current state

echo "🔍 DATABASE DEBUG SCRIPT"
echo "========================"

# Check if containers are running
echo "📋 Container Status:"
docker-compose ps

echo ""
echo "🔧 Database Connection Test:"
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -c "
SELECT 
    table_name, 
    table_type 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
"

echo ""
echo "📊 Migration Status:"
docker-compose exec -T backend python manage.py showmigrations --verbosity=1

echo ""
echo "🔍 User Table Check:"
docker-compose exec -T backend python manage.py shell -c \"
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    # Check if table exists by trying to query it
    count = User.objects.count()
    print(f'User table exists and accessible - {count} users found')
except Exception as e:
    print(f'❌ User table issue: {e}')
    print('This confirms the jac_user table does not exist')
\"

echo ""
echo "⚙️ Django Settings Check:"
docker-compose exec -T backend python manage.py shell -c \"
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.conf import settings
print(f'AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}')
print(f'Database Engine: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
print(f'Database Name: {settings.DATABASES[\"default\"][\"NAME\"]}')
\"

echo ""
echo "========================"
echo "✅ DEBUG COMPLETED"
echo "========================"