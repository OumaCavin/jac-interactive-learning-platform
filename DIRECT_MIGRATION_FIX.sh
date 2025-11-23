# DIRECT MIGRATION FIX - Quick solution

echo "🚀 DIRECT MIGRATION FIX"
echo "======================"

# Step 1: Generate migrations
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
cd /app

echo '📝 Creating migration files...'
python manage.py makemigrations users --noinput
echo '✅ Users migration created'

python manage.py makemigrations learning --noinput
echo '✅ Learning migration created'

python manage.py makemigrations --merge --noinput
echo '✅ Merged migrations created'

echo '📊 Migration files status:'
ls -la apps/*/migrations/*.py
"

# Step 2: Apply migrations
docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
cd /app

echo '🔄 Applying migrations...'
python manage.py migrate --noinput --verbosity=2

echo '📊 Final status:'
python manage.py showmigrations
"

# Step 3: Create admin user
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
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@jacplatform.com', 'admin123')
    print('✅ Admin created successfully')
else:
    print('✅ Admin user exists')
\"
"

echo "✅ DIRECT FIX COMPLETED!"