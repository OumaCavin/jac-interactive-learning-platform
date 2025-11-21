#!/bin/bash

# JAC Interactive Learning Platform - Complete Integration Startup Script
# Author: Cavin Otieno
# Generated: 2025-11-21 21:34:07

echo "🚀 JAC Interactive Learning Platform - Complete Integration Startup"
echo "=================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "/workspace/backend" ] || [ ! -d "/workspace/frontend" ]; then
    print_error "Error: Workspace directory structure not found"
    echo "Expected: /workspace/backend and /workspace/frontend"
    exit 1
fi

print_status "Workspace structure verified"

# Backend Setup
echo ""
echo "🔧 Backend Setup"
echo "----------------"

cd /workspace/backend

# Install backend dependencies
print_info "Installing backend dependencies..."
if pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 djangorestframework-simplejwt==5.3.0 --user > /dev/null 2>&1; then
    print_status "Backend dependencies installed"
else
    print_warning "Some backend dependencies may already be installed"
fi

# Setup database
print_info "Setting up database..."
python manage.py makemigrations > /dev/null 2>&1
python manage.py migrate > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_status "Database setup complete"
else
    print_warning "Database setup encountered issues (may already be setup)"
fi

# Frontend Setup  
echo ""
echo "🎨 Frontend Setup"
echo "-----------------"

cd /workspace/frontend

# Install frontend dependencies
print_info "Installing frontend dependencies..."
if npm install > /dev/null 2>&1; then
    print_status "Frontend dependencies installed"
else
    print_warning "npm install encountered issues - checking if dependencies exist..."
    if [ -d "node_modules" ]; then
        print_status "node_modules directory exists, continuing..."
    else
        print_error "Frontend dependencies not found. Please run 'npm install' manually."
        exit 1
    fi
fi

# Server Startup
echo ""
echo "🚀 Starting Servers"
echo "-------------------"

# Start Django backend in background
print_info "Starting Django backend server..."
cd /workspace/backend
export DJANGO_SETTINGS_MODULE=config.settings.local
nohup python manage.py runserver 0.0.0.0:8000 > /tmp/django.log 2>&1 &
DJANGO_PID=$!
print_status "Django backend started (PID: $DJANGO_PID)"
print_info "Backend will be available at: http://localhost:8000"

# Wait a moment for Django to start
sleep 3

# Start React frontend in background
print_info "Starting React frontend server..."
cd /workspace/frontend
nohup npm start > /tmp/react.log 2>&1 &
REACT_PID=$!
print_status "React frontend started (PID: $REACT_PID)")
print_info "Frontend will be available at: http://localhost:3000"

# Wait for servers to fully start
echo ""
echo "⏳ Waiting for servers to start..."
sleep 5

# Test server availability
echo ""
echo "🔍 Testing Server Availability"
echo "------------------------------"

# Test Django backend
if curl -s http://localhost:8000 > /dev/null; then
    print_status "Django backend is responding"
else
    print_warning "Django backend may still be starting..."
fi

# Test React frontend
if curl -s http://localhost:3000 > /dev/null; then
    print_status "React frontend is responding"
else
    print_warning "React frontend may still be starting..."
fi

# Display server information
echo ""
echo "🎯 Integration Summary"
echo "======================"
echo ""
echo "📱 Application Access:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "🔐 Demo Credentials:"
echo "   Email: demo@example.com"
echo "   Password: demo123"
echo ""
echo "🔗 API Endpoints Available:"
echo "   GET    http://localhost:8000/api/agents/        - List agents"
echo "   POST   http://localhost:8000/api/learning/execute/ - Execute code"
echo "   POST   http://localhost:8000/api/auth/login/     - User login"
echo ""
echo "⚡ Quick Test Commands:"
echo "   # Test backend API"
echo "   curl http://localhost:8000/api/agents/"
echo ""
echo "   # Test frontend"
echo "   open http://localhost:3000"
echo ""
echo "🛑 To stop servers:"
echo "   kill $DJANGO_PID $REACT_PID"
echo ""

# Save PIDs for easy management
echo $DJANGO_PID > /tmp/django.pid
echo $REACT_PID > /tmp/react.pid

print_status "Integration startup complete!"
print_info "Servers running in background. Check /tmp/django.log and /tmp/react.log for detailed output."

echo ""
echo "Ready for end-to-end testing! 🎉"