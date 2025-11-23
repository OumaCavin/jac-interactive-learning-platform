#!/bin/bash
set -e

echo "🚀 Starting JAC Learning Platform..."

# Wait for database to be ready
echo "📡 Waiting for database..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "✅ Database is ready!"

# Run migrations and initialize platform
echo "📦 Running platform initialization..."
python manage.py migrate || echo "Migrations already applied"
python manage.py initialize_platform --username=admin --email=admin@jacplatform.com --password=admin123 || echo "Initialization skipped (already done)"

# Start the server
echo "🌐 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000