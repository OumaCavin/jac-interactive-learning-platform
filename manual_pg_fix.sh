#!/bin/bash
echo "=== Manual PostgreSQL Fix (While Debugging Git) ==="

cd ~/projects/jac-interactive-learning-platform

echo "1. Backup settings file..."
cp backend/config/settings.py backend/config/settings.py.backup.$(date +%Y%m%d_%H%M%S)

echo "2. Apply PostgreSQL charset fix..."
# Remove the invalid charset line that's causing the connection error
sed -i '/charset.*utf8/d' backend/config/settings.py

echo "3. Verify fix applied..."
echo "Checking for any remaining charset references:"
grep -n "charset" backend/config/settings.py || echo "✅ No charset references found (good!)"

echo "4. Show the fixed OPTIONS section (should be lines ~109-111):"
sed -n '105,115p' backend/config/settings.py

echo "5. Rebuild backend container with fixed settings..."
docker-compose up -d --build backend

echo "6. Wait for backend to connect to PostgreSQL..."
sleep 15

echo "7. Test database connection..."
docker-compose exec backend python manage.py check --database default

echo "8. If successful, run migrations..."
docker-compose exec backend python manage.py migrate

echo -e "\n=== Manual Fix Applied ==="
echo "You can now create admin user with: docker-compose exec backend python manage.py createsuperuser"