#!/bin/bash
# Local Development Setup Script

echo "🚀 Setting up JAC Learning Platform locally..."

# Navigate to project root
cd ~/projects/jac-interactive-learning-platform

# Activate your existing virtual environment
source .venv/bin/activate  # or your jac-int-venv

# Install dependencies using pip (since uv might not be available)
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt 2>/dev/null || echo "No requirements.txt found"

# For Django projects, install common dependencies
pip install django djangorestframework django-cors-headers python-decouple

# Navigate to backend
cd backend

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Create superuser (if not exists)
echo "👤 Create superuser for admin access..."
python manage.py createsuperuser

# Start development server
echo "🌐 Starting Django development server..."
python manage.py runserver 0.0.0.0:8000

echo "✅ Setup complete! Visit http://localhost:8000/admin/ for admin interface"