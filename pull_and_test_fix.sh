#!/bin/bash
echo "=== Pull and Test PostgreSQL Fix ==="

cd ~/projects/jac-interactive-learning-platform

echo "1. Pull the latest changes from remote..."
git pull origin main

echo -e "\n2. Verify the fix is applied (should show no charset references)..."
grep -n "charset" backend/config/settings.py || echo "✅ No charset references found (good!)"

echo -e "\n3. Rebuild backend container with fixed settings..."
docker-compose up -d --build backend

echo -e "\n4. Wait for backend to connect to PostgreSQL..."
sleep 15

echo -e "\n5. Test database connection..."
docker-compose exec backend python manage.py check --database default

echo -e "\n6. If successful, run migrations..."
docker-compose exec backend python manage.py migrate

echo -e "\n7. Create admin user..."
docker-compose exec backend python manage.py createsuperuser

echo -e "\n=== Fix Complete ==="
echo "You can now login at http://localhost:8000/admin/ with admin/admin123"