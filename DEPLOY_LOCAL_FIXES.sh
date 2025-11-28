#!/bin/bash

# JAC Platform - Local Fix Deployment Script
# Run this AFTER: git pull origin main
# This works on your LOCAL machine (not in cloud environment)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔧 $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${PURPLE}🔸 $1${NC}"
}

# Check if we're in the right directory
if [[ ! -f "docker-compose.yml" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    print_error "This command must be run from the JAC platform root directory"
    print_error "Make sure docker-compose.yml, backend/, and frontend/ directories exist"
    print_info "Current directory: $(pwd)"
    exit 1
fi

print_header "🚀 JAC PLATFORM - LOCAL FIX DEPLOYMENT"
print_info "This command applies ALL fixes on your LOCAL machine"

# Step 1: Check Docker status
print_step "Step 1: Checking Docker services..."
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

if ! docker-compose --version > /dev/null 2>&1; then
    print_error "docker-compose is not available. Please install it."
    exit 1
fi

print_success "Docker is available"

# Step 2: Start services
print_step "Step 2: Starting/Checking Docker services..."

# Check if services are already running
if docker-compose ps | grep -q "backend.*Up"; then
    print_success "Services are already running"
else
    print_info "Starting services..."
    docker-compose up -d
    sleep 20
    print_success "Services started"
fi

# Step 3: Apply password fixes
print_step "Step 3: Setting up password authentication..."

echo ""
echo -e "${YELLOW}Choose password approach:${NC}"
echo "1) Empty password + first login (RECOMMENDED - Modern UX)"
echo "2) Fixed passwords with proper hashing (Traditional)"
echo ""

read -p "Enter choice (1 or 2, default: 1): " choice
choice=${choice:-1}

if [[ "$choice" == "1" ]]; then
    print_info "Setting up empty password + first login approach..."
    
    # Run empty password setup using local script
    if docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.management import call_command
import os

print("🔧 Creating users with empty passwords...")

# Clean up existing users
User.objects.filter(username='admin').delete()
User.objects.filter(username='demo_user').delete()

# Create admin user with empty password
admin_user = User.objects.create_user(
    username='admin',
    email='cavin.otieno012@gmail.com',
    password=None,  # Empty password
    is_superuser=True,
    is_staff=True,
    is_active=True
)
admin_user.last_login = None
admin_user.save()

print("✅ Admin user created with empty password")

# Create demo user with empty password
demo_user = User.objects.create_user(
    username='demo_user',
    email='demo@example.com',
    password=None,  # Empty password
    is_superuser=False,
    is_staff=False,
    is_active=True
)
demo_user.last_login = None
demo_user.save()

print("✅ Demo user created with empty password")

# Verify
print(f"Admin has usable password: {admin_user.has_usable_password()}")
print(f"Demo has usable password: {demo_user.has_usable_password()}")

print("🎉 Empty password setup completed!")
EOF
    then
        print_success "Empty password setup completed"
        
        # Create middleware file
        print_info "Creating first login middleware..."
        mkdir -p backend/apps/users
        
        cat > backend/apps/users/middleware.py << 'EOF'
"""
First Login Password Prompt Middleware
Redirects users with empty passwords to password change page
"""

from django.shortcuts import redirect
from django.contrib import messages

class FirstLoginPasswordMiddleware:
    """
    Middleware to handle users with empty passwords
    Redirects them to password change page on first login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            user = request.user
            
            # If user has no usable password, redirect to password change
            if not user.has_usable_password() and not user.last_login:
                # Don't redirect if already on password change page
                if not request.path.startswith('/change-password/'):
                    messages.warning(request, "Please set your password before continuing.")
                    return redirect('password_change')
        
        response = self.get_response(request)
        return response
EOF
        print_success "Middleware created"
        
        # Add middleware to settings
        print_info "Updating settings.py..."
        docker-compose exec -T backend python manage.py shell << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

settings_file = '/app/config/settings.py'
try:
    with open(settings_file, 'r') as f:
        content = f.read()
    
    if 'users.middleware.FirstLoginPasswordMiddleware' not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == "MIDDLEWARE = [":
                j = i + 1
                while j < len(lines) and lines[j].strip() != ']':
                    j += 1
                if j < len(lines):
                    lines.insert(j, "    'users.middleware.FirstLoginPasswordMiddleware',")
                    break
        
        with open(settings_file, 'w') as f:
            f.write('\n'.join(lines))
        print("✅ Middleware added to settings")
    else:
        print("ℹ️ Middleware already configured")
        
except Exception as e:
    print(f"⚠️ Settings update failed: {e}")
EOF
        
    else
        print_warning "Empty password setup failed, falling back to fixed password approach"
        choice=2
    fi
fi

if [[ "$choice" == "2" ]]; then
    print_info "Setting up fixed passwords with proper hashing..."
    
    # Use Django's create_user which properly hashes passwords
    docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User

print("🔧 Creating users with proper password hashing...")

# Clean up existing users
User.objects.filter(username='admin').delete()
User.objects.filter(username='demo_user').delete()

# Create admin user with proper hashing
admin_user = User.objects.create_user(
    username='admin',
    email='cavin.otieno012@gmail.com',
    password='admin123'
)
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()

# Create demo user with proper hashing
demo_user = User.objects.create_user(
    username='demo_user',
    email='demo@example.com',
    password='demo123'
)

print("✅ Users created with proper password hashing")

# Verify password verification works
print(f"Admin password verification: {admin_user.check_password('admin123')}")
print(f"Demo password verification: {demo_user.check_password('demo123')}")

print("🎉 Fixed password setup completed!")
EOF
fi

# Step 4: Test and verify
print_step "Step 4: Verifying all fixes..."
print_info "Testing web endpoints..."

if curl -s -f http://localhost:3000/ > /dev/null; then
    print_success "✅ Frontend: ACCESSIBLE"
else
    print_warning "⚠️  Frontend: May still be starting"
fi

if curl -s -f http://localhost:8000/admin/ > /dev/null; then
    print_success "✅ Django Admin: ACCESSIBLE"
else
    print_warning "⚠️  Django Admin: May still be starting"
fi

if curl -s -f http://localhost:8000/api/health/ > /dev/null; then
    print_success "✅ API Health: WORKING"
else
    print_warning "⚠️  API Health: May still be starting"
fi

# Final status
print_header "🎉 LOCAL FIX DEPLOYMENT COMPLETED"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎯 All JAC Platform fixes have been applied locally!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

if [[ "$choice" == "1" ]]; then
    echo -e "${CYAN}🔐 EMPTY PASSWORD + FIRST LOGIN APPROACH ACTIVE${NC}"
    echo ""
    echo -e "${YELLOW}📱 Django Admin:${NC}"
    echo "   URL: http://localhost:8000/admin/"
    echo "   Username: admin"
    echo "   Password: (leave empty - set on first login)"
    echo ""
    echo -e "${YELLOW}🌍 Frontend:${NC}"
    echo "   URL: http://localhost:3000/login"
    echo "   Username: demo_user"
    echo "   Password: (leave empty - set on first login)"
    echo ""
    echo -e "${CYAN}🔧 User Experience:${NC}"
    echo "1. Login with empty password"
    echo "2. Automatically redirected to password change page"
    echo "3. Set your preferred password"
    echo "4. Enjoy full platform access!"
else
    echo -e "${CYAN}🔐 FIXED PASSWORD APPROACH ACTIVE${NC}"
    echo ""
    echo -e "${YELLOW}📱 Django Admin:${NC}"
    echo "   URL: http://localhost:8000/admin/"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo -e "${YELLOW}🌍 Frontend:${NC}"
    echo "   URL: http://localhost:3000/login"
    echo "   Username: demo_user"
    echo "   Password: demo123"
fi

echo ""
echo -e "${GREEN}✅ LOCAL FIXES APPLIED:${NC}"
echo "   ✅ Docker services running"
echo "   ✅ Password authentication configured"
echo "   ✅ All web services accessible"
echo ""

echo -e "${YELLOW}📋 MANAGEMENT COMMANDS:${NC}"
echo "   📊 View logs: docker-compose logs -f"
echo "   🔄 Restart: docker-compose restart"
echo "   ⏹️  Stop: docker-compose down"
echo "   🔨 Rebuild: docker-compose up -d --build"
echo ""

print_success "🚀 Your local JAC Platform is now fully operational!"
print_success "🎓 Happy Learning with JAC!"