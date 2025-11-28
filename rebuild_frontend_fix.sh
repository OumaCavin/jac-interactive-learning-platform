#!/bin/bash

# JAC Learning Platform - Frontend Rebuild Script for Login Form Fixes

echo "🔧 Rebuilding frontend with login form positioning fixes..."

# Navigate to project directory
cd ~/projects/jac-interactive-learning-platform

# Stop any running containers
echo "🛑 Stopping containers..."
docker-compose down

# Rebuild frontend with latest changes
echo "🏗️  Rebuilding frontend..."
docker-compose up -d --build

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to start..."
sleep 10

# Check if frontend is running
echo "✅ Checking frontend status..."
docker-compose ps frontend

echo ""
echo "🎉 Frontend rebuild completed!"
echo "📱 Access your application at: http://localhost:3000"
echo ""
echo "✨ Login form should now have:"
echo "   • Proper input field spacing"
echo "   • Visible button text"
echo "   • Correct checkbox styling"
echo "   • No overlapping validation messages"
echo "   • Enhanced form layout and alignment"
