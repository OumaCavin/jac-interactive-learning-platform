#!/bin/bash
# Post Git Pull Setup Script for JAC Learning Platform

echo "🚀 Setting up JAC Learning Platform after git pull..."

# 1. Navigate to backend directory
cd backend

# 2. Kill any existing Django processes
echo "🔄 Stopping existing Django processes..."
pkill -f "python manage.py runserver" 2>/dev/null || true
sleep 2

# 3. Install/update dependencies
echo "📦 Installing/updating dependencies..."
uv pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found, skipping..."

# 4. Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# 5. Collect static files (if needed)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || echo "Static files already up to date"

# 6. Start the server
echo "🌐 Starting Django server on port 8001..."
python manage.py runserver 0.0.0.0:8001

echo "✅ Setup complete! Visit http://localhost:8001/admin/ for the admin interface"