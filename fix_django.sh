#!/bin/bash

echo "Starting Django server fix..."

# Kill any existing Django processes
pkill -f "runserver" 2>/dev/null
pkill -f "python.*manage" 2>/dev/null

# Remove users app completely if it exists
if [ -d "/workspace/backend/apps/users" ]; then
    echo "Removing users app..."
    rm -rf /workspace/backend/apps/users
fi

# Clean Python cache
find /workspace/backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find /workspace/backend -name "*.pyc" -delete 2>/dev/null

# Remove duplicate directory
if [ -d "/workspace/jac_learning_platform" ]; then
    echo "Removing duplicate jac_learning_platform directory..."
    rm -rf /workspace/jac_learning_platform
fi

echo "Starting Django server on port 8000..."
cd /workspace/backend
/tmp/.venv/bin/python manage.py runserver 0.0.0.0:8000 --settings=config.settings_minimal &

# Store PID
DJANGO_PID=$!
echo "Django server started with PID: $DJANGO_PID"

# Wait for server to start
sleep 10

# Test health endpoint
echo "Testing Django health endpoint..."
curl -s http://localhost:8000/api/health/static/ && echo "SUCCESS: Django server is running!" || echo "FAILED: Django server not responding"

# Test Chat Assistant API
echo "Testing Chat Assistant API..."
curl -X POST http://localhost:8000/api/agents/chat-assistant/message/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test-session"}' \
  2>/dev/null && echo "SUCCESS: Chat Assistant API working!" || echo "FAILED: Chat Assistant API not responding"

# Test Assessment API
echo "Testing Assessment API..."
curl -s http://localhost:8000/api/assessment/quizzes/ && echo "SUCCESS: Assessment API working!" || echo "FAILED: Assessment API not responding"

echo "Tests completed!"
echo "Django PID: $DJANGO_PID"
echo "Server should be running on http://localhost:8000"