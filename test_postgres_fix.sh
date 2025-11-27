#!/bin/bash
echo "=== Testing PostgreSQL Fix ==="

# 1. Apply the fix (either pull or edit manually)
echo "1. Applying fix..."

# 2. Rebuild backend container with fixed settings
echo "2. Rebuilding backend container..."
docker-compose up -d --build backend

# 3. Wait for backend to start
echo "3. Waiting for backend to connect to PostgreSQL..."
sleep 10

# 4. Check logs for connection success
echo "4. Checking backend logs for PostgreSQL connection..."
docker-compose logs backend | tail -20

# 5. Test database connection
echo -e "\n5. Testing database connection..."
docker-compose exec backend python manage.py check --database default

# 6. Run migrations
echo -e "\n6. Running migrations..."
docker-compose exec backend python manage.py migrate

echo -e "\n=== Test Complete ==="