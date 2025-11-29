#!/bin/bash

# Test Django Backend and Real Authentication

echo "🧪 Testing Real Authentication with Django Backend"
echo "================================================="

# Test 1: Check if Django is running
echo "📋 Test 1: Django Backend Health Check"
curl -s http://localhost:8000/api/health/ | head -5
echo ""

# Test 2: Test user registration endpoint
echo "📋 Test 2: User Registration Endpoint"
curl -s -X POST http://localhost:8000/api/users/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser123",
    "email": "test@example.com", 
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
  }' | head -5
echo ""

# Test 3: Test login endpoint  
echo "📋 Test 3: User Login Endpoint"
curl -s -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }' | head -5
echo ""

# Test 4: Check frontend accessibility
echo "📋 Test 4: Frontend Accessibility"
curl -s -I http://localhost:3000/ | grep "HTTP\|Status"
echo ""

echo "✅ Backend Testing Complete!"
echo "================================"
echo "🎯 Real Authentication Available:"
echo "   - Register new users: POST /api/users/auth/register/"
echo "   - Login: POST /api/users/auth/login/"
echo "   - User Profile: GET /api/users/profile/"
echo ""
echo "🚀 Ready to test in browser:"
echo "   Frontend: http://localhost:3000/login"
echo "   Admin:    http://localhost:8000/admin/"