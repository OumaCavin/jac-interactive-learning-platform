#!/bin/bash
# Quick fix for database migration issues

echo "🔧 Running database migrations to fix 'jac_user' table issue..."

# Stop containers
docker-compose down

# Start only database and backend
docker-compose up -d postgres redis

# Wait for database
echo "⏳ Waiting for database..."
until docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db; do
    echo "Database not ready yet, waiting..."
    sleep 2
done

# Run migrations
echo "🔄 Running Django migrations..."
docker-compose exec -T backend python manage.py makemigrations
docker-compose exec -T backend python manage.py migrate --noinput
docker-compose exec -T backend python manage.py collectstatic --noinput

echo "✅ Migrations completed!"

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d --build

echo "✅ Fix complete! Check: docker-compose logs --tail=20 backend"