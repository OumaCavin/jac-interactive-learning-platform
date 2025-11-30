#!/bin/bash

# Jeseci Learning Platform Setup Script
# Automated setup for development environment

set -e  # Exit on any error

echo "🚀 Setting up Jeseci Learning Platform..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

# Install Jaseci CLI
echo "📦 Installing Jaseci CLI..."
pip3 install jaseci jaseci-serv

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Set up Django backend
echo "⚙️ Setting up Django backend..."
cd django-backend

# Run database migrations
echo "🗄️ Setting up database..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
read -p "Do you want to create a superuser? (y/n): " create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python3 manage.py createsuperuser
fi

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

cd ..

# Create logs directory
mkdir -p logs

# Verify Jac installation
echo "✅ Verifying Jac installation..."
if jaseci --version; then
    echo "✅ Jac CLI installed successfully"
else
    echo "⚠️ Jac CLI verification failed - please check installation"
fi

# Verify project structure
echo "🔍 Verifying project structure..."
required_files=(
    "main.jac"
    "jac-core/user_management.jac"
    "jac-core/lesson_system.jac"
    "jac-core/quiz_engine.jac"
    "osp-graph/mastery_graph.jac"
    "byllm-agents/content_generator.jac"
    "jac-client/index.html"
    "jac-client/index.js"
    "jac-client/styles.css"
    "django-backend/api/views.py"
    "django-backend/api/urls.py"
    "django-backend/settings.py"
    "django-backend/urls.py"
    "PROJECT_DOCUMENTATION.md"
    "requirements.txt"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All required files are present"
else
    echo "⚠️ Missing files:"
    printf '%s\n' "${missing_files[@]}"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Start the Django server: cd django-backend && python3 manage.py runserver"
echo "2. Open your browser to: http://localhost:8000"
echo "3. The Jac-Client frontend will load automatically"
echo ""
echo "📚 For more information, see PROJECT_DOCUMENTATION.md"
echo ""
echo "🔧 Development commands:"
echo "- Run tests: cd django-backend && python3 manage.py test"
echo "- Check code style: flake8 django-backend/"
echo "- Format code: black django-backend/"
echo ""
echo "Happy learning with Jeseci! 🎯"