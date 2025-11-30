#!/bin/bash

echo "=========================================="
echo "🚀 JAC Platform - GitHub Update & Admin Fix"
echo "=========================================="
echo ""
echo "📥 Pulling latest admin fix scripts from GitHub..."

cd ~/projects/jac-interactive-learning-platform

echo "Step 1: Pull latest changes..."
git pull origin main

echo ""
echo "Step 2: Running fast admin fix..."
bash FAST_ADMIN_FIX.sh

echo ""
echo "Step 3: Testing admin access..."
echo "Testing admin page:"
curl -I http://localhost:8000/admin/ | head -1

echo ""
echo "Testing admin CSS:"
curl -I http://localhost:8000/static/admin/css/dashboard.css | head -1

echo ""
echo "=========================================="
echo "🎯 READY FOR BROWSER TESTING"
echo "=========================================="
echo ""
echo "🌐 Now test in browser:"
echo "1. Open: http://localhost:8000/admin/"
echo "2. Login: admin / jac_admin_2024!"
echo "3. Admin interface should load with proper CSS"
echo ""
echo "🧪 If still having issues, run:"
echo "   bash COMPLETE_ADMIN_STATIC_FIX.sh"