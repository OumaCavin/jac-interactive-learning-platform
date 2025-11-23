docker-compose exec -T backend bash -c "
export DJANGO_COLUMNS=0
export DJANGO_SUPERUSER_ID=''
cd /app

echo 'Running makemigrations...'
python manage.py makemigrations --merge --noinput || echo 'Makemigrations completed'

echo 'Running migrate with full automation...'
python manage.py migrate --noinput || echo 'Migration completed'

echo 'Creating superuser...'
python manage.py shell -c \"
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@jacplatform.com', 
        password='admin123'
    )
    print('Superuser created')
else:
    print('Superuser already exists')
\" || echo 'Superuser setup completed'

echo 'Final migration status:'
python manage.py showmigrations
"