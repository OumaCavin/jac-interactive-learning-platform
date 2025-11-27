#!/bin/bash
echo "=== Quick Fix Test ==="

# Rebuild backend container with fixed settings
echo "1. Rebuilding backend container..."
docker-compose up -d --build backend

# Wait for backend to start
echo "2. Waiting 15 seconds for backend to connect..."
sleep 15

# Check if backend is running properly
echo -e "\n3. Backend container status:"
docker-compose ps backend

# Check logs for PostgreSQL connection success
echo -e "\n4. Recent backend logs (looking for PostgreSQL connection):"
docker-compose logs backend | grep -E "(PostgreSQL|database|connection|ERROR)" | tail -10

# Test database connection
echo -e "\n5. Database connection test:"
docker-compose exec backend python manage.py check --database default

# If successful, run migrations
echo -e "\n6. Running migrations:"
docker-compose exec backend python manage.py migrate

echo -e "\n=== Test Complete ==="