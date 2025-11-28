#!/bin/bash
echo "=== Emergency PostgreSQL Fix (Skip Git) ==="

cd ~/projects/jac-interactive-learning-platform

echo "1. Backup original settings..."
cp backend/config/settings.py backend/config/settings.py.backup.$(date +%Y%m%d_%H%M%S)

echo "2. Fixing PostgreSQL charset issue..."
# Remove the problematic charset line
sed -i '/charset.*utf8/d' backend/config/settings.py

echo "3. Verifying the fix..."
grep -n "charset" backend/config/settings.py
echo "(Should show no results - charset should be removed)"

echo "4. Rebuilding backend with fixed settings..."
docker-compose up -d --build backend

echo "5. Waiting 15 seconds for backend to start..."
sleep 15

echo "6. Testing database connection..."
docker-compose exec backend python manage.py check --database default

echo "7. If successful, running migrations..."
docker-compose exec backend python manage.py migrate

echo "8. Creating admin user..."
echo "Run: docker-compose exec backend python manage.py createsuperuser"

echo -e "\n=== Emergency Fix Complete ==="