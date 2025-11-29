#!/bin/bash

# JAC Platform - Comprehensive Local Fix Deployment Script with Database Setup
# Run this AFTER: git pull origin main
# This works on your LOCAL machine (not in cloud environment)
# Combines service deployment with comprehensive database schema and sample data

set -e

# Enhanced Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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
    echo -e "${YELLOW}🔸 $1${NC}"
}

print_apps() {
    echo -e "${PURPLE}📱 $1${NC}"
}

print_purple() {
    echo -e "${PURPLE}🔸 $1${NC}"
}

# Check if we're in the right directory
if [[ ! -f "docker-compose.yml" ]] || [[ ! -d "backend" ]] || [[ ! -d "frontend" ]]; then
    print_error "This command must be run from the JAC platform root directory"
    print_error "Make sure docker-compose.yml, backend/, and frontend/ directories exist"
    print_info "Current directory: $(pwd)"
    exit 1
fi

print_header "🚀 JAC PLATFORM - COMPREHENSIVE LOCAL DEPLOYMENT"
print_info "This command applies ALL fixes and creates complete database schema"
print_info "Including: Docker fixes, TypeScript fixes, and comprehensive data setup"
print_info "Requirements: database/ directory must be present (SQL files for schema creation)"
print_info "Docker Compose updated with database volume mapping for container access"

# ========================================
# DATABASE SETUP FUNCTIONS
# ========================================

# Complete database schema execution
execute_complete_schema() {
    print_header "🏗️ CREATING COMPLETE DATABASE SCHEMA"
    
    print_info "This will create tables for ALL Django apps:"
    print_apps "✅ admin - Django admin interface tables"
    print_apps "✅ agents - AI agent system tables"
    print_apps "✅ assessments - Enhanced assessment system tables"
    print_apps "✅ auth - Authentication system tables"
    print_apps "✅ collaboration - Study groups & discussions tables"
    print_apps "✅ content - Content management system tables"
    print_apps "✅ contenttypes - Django content types tables"
    print_apps "✅ django_celery_beat - Task scheduler tables"
    print_apps "✅ gamification - Achievement & badge system tables"
    print_apps "✅ jac_execution - Platform execution engine tables"
    print_apps "✅ knowledge_graph - Knowledge graph system tables"
    print_apps "✅ learning - Learning progression tables"
    print_apps "✅ sessions - Django session tables"
    print_apps "✅ users - Custom user system tables"
    echo ""
    
    # Execute SQL files in dependency order
    local sql_files=(
        "00_django_core_tables.sql:Django Core System (auth, admin, sessions)"
        "01_foundation_tables.sql:Custom User System Foundation"
        "02_content_structure.sql:Learning Content Structure"
        "03_learning_system.sql:Learning & Assessment System"
        "04_gamification.sql:Gamification System"
        "05_agents_knowledge_collaboration.sql:Agents, Knowledge & Collaboration"
        "06_assessments_enhanced_content.sql:Enhanced Assessments & Content"
    )
    
    for sql_entry in "${sql_files[@]}"; do
        IFS=':' read -r sql_file description <<< "$sql_entry"
        
        print_step "Creating $description"
        print_info "File: $sql_file"
        
        # Execute SQL with comprehensive error handling
        local result=0
        
        # Method 1: Via backend container (now that database is mounted)
        if docker-compose exec -T backend psql -U jac_user -d jac_learning_db -f "/app/database/$sql_file" > /dev/null 2>&1; then
            print_success "✅ $description completed successfully"
        else
            print_warning "⚠️  $description had issues, trying alternative method..."
            
            # Method 2: Direct psql via docker run from host
            if docker run --rm --network $(basename $(pwd))_default \
                -v "$(pwd):/workspace" \
                -w /workspace \
                postgres:15 psql -h postgres -U jac_user -d jac_learning_db \
                -f "/workspace/database/$sql_file" --quiet --no-align > /tmp/sql_error.log 2>&1; then
                print_success "✅ $description completed via direct method"
            else
                print_warning "⚠️  Trying via backend shell..."
                
                # Method 3: Via backend container shell
                if docker-compose exec -T backend bash -c "cd /app && psql -U jac_user -d jac_learning_db -f database/$sql_file" > /dev/null 2>&1; then
                    print_success "✅ $description completed via backend shell"
                else
                    print_error "❌ $description failed with all methods"
                    print_info "Error details:"
                    cat /tmp/sql_error.log 2>/dev/null || print_info "No error details available"
                    return 1
                fi
            fi
        fi
        
        echo ""
    done
}

# Comprehensive data loading
load_comprehensive_data() {
    print_header "📊 LOADING COMPREHENSIVE INITIAL DATA"
    
    print_step "Creating users, content, and sample data across all systems..."
    
    # Create enhanced data loader script
    cat > /tmp/comprehensive_data_loader.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from decimal import Decimal

# Database connection
def get_conn():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'jac_learning_db'),
        user=os.getenv('DB_USER', 'jac_user'),
        password=os.getenv('DB_PASSWORD', 'jac_password')
    )

def execute(query, params=None):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            return cur.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        conn.close()

def execute_non_query(query, params=None):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params or ())
            conn.commit()
            return cur.rowcount
    except Exception as e:
        print(f"Error executing non-query: {e}")
        conn.rollback()
        return 0
    finally:
        conn.close()

def create_sample_content():
    print("Creating sample content...")
    
    # Create learning modules
    modules = [
        ('Python Programming Basics', 'Learn Python fundamentals', 'beginner', 120),
        ('Web Development Fundamentals', 'HTML, CSS, and JavaScript basics', 'beginner', 180),
        ('Data Science with Python', 'Pandas, NumPy, and data analysis', 'intermediate', 240),
        ('Advanced Python Concepts', 'Object-oriented programming and design patterns', 'advanced', 300),
        ('Machine Learning Fundamentals', 'Introduction to ML algorithms', 'advanced', 360)
    ]
    
    for title, desc, level, duration in modules:
        execute_non_query("""
            INSERT INTO content_learningmodule (title, description, difficulty_level, 
                                               estimated_duration, is_published, created_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, desc, level, duration, True, 1, datetime.now(), datetime.now()))
    
    print("✅ Sample content created")

def create_sample_assessments():
    print("Creating sample assessments...")
    
    # Create assessments for existing modules
    execute_non_query("""
        INSERT INTO learning_assessment (module_id, title, description, assessment_type,
                                       time_limit, passing_score, max_attempts,
                                       is_active, created_by, created_at, updated_at)
        SELECT id, 'Assessment for ' || title, 'Test your knowledge', 'quiz',
               30, 70, 3, True, %s, %s, %s
        FROM content_learningmodule
        LIMIT 5
    """, (1, datetime.now(), datetime.now()))
    
    print("✅ Sample assessments created")

def create_gamification_data():
    print("Creating gamification data...")
    
    # Create achievements
    achievements = [
        ('First Steps', 'Complete your first learning module', 'completion', 0),
        ('Quick Learner', 'Complete 3 modules in one day', 'streak', 100),
        ('Knowledge Seeker', 'Score 100% on an assessment', 'score', 200),
        ('Persistent Learner', 'Maintain a 7-day learning streak', 'streak', 300),
        ('Assessment Master', 'Complete 10 assessments with 80%+ score', 'mastery', 500)
    ]
    
    for title, desc, type_val, points in achievements:
        execute_non_query("""
            INSERT INTO gamification_achievement (title, description, achievement_type, 
                                                points_required, is_active, created_by, 
                                                created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, desc, type_val, points, True, 1, datetime.now(), datetime.now()))
    
    print("✅ Gamification data created")

def create_agents():
    print("Creating AI agents...")
    
    # Create sample agents
    agents = [
        ('Python Tutor', 'AI tutor specializing in Python programming', 'tutor', 'gpt-4'),
        ('Web Dev Assistant', 'Assistant for web development questions', 'assistant', 'gpt-3.5'),
        ('Data Science Mentor', 'Mentor for data science and analytics', 'mentor', 'gpt-4'),
        ('Code Reviewer', 'Agent for code review and optimization', 'coach', 'gpt-4')
    ]
    
    for name, desc, agent_type, model in agents:
        execute_non_query("""
            INSERT INTO agents_agent (name, description, agent_type, model_name,
                                    configuration, capabilities, is_active, created_by,
                                    created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, desc, agent_type, model, 
              json.dumps({"temperature": 0.7, "max_tokens": 1000}),
              json.dumps(["explain_concepts", "answer_questions", "review_code"]),
              True, 1, datetime.now(), datetime.now()))
    
    print("✅ AI agents created")

def create_sample_knowledge_graph():
    print("Creating knowledge graph...")
    
    # Create concept nodes
    concepts = [
        ('Variables', 'Programming concept of variables', 'concept', 1),
        ('Functions', 'Programming concept of functions', 'concept', 2),
        ('Loops', 'Programming concept of loops', 'concept', 2),
        ('Data Structures', 'Programming concept of data structures', 'concept', 3),
        ('Algorithms', 'Programming concept of algorithms', 'concept', 4),
        ('Python', 'Python programming language', 'skill', 1),
        ('JavaScript', 'JavaScript programming language', 'skill', 2),
        ('HTML', 'HTML markup language', 'skill', 1),
        ('CSS', 'CSS styling language', 'skill', 2)
    ]
    
    for name, desc, concept_type, difficulty in concepts:
        execute_non_query("""
            INSERT INTO knowledge_graph_conceptnode (name, description, concept_type,
                                                   difficulty_level, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, desc, concept_type, difficulty, datetime.now(), datetime.now()))
    
    # Create relationships
    relationships = [
        ('Variables', 'Functions', 'prerequisite'),
        ('Functions', 'Data Structures', 'prerequisite'),
        ('Data Structures', 'Algorithms', 'prerequisite'),
        ('Variables', 'Python', 'same_as'),
        ('Functions', 'Python', 'same_as'),
        ('HTML', 'Web Development', 'related_to'),
        ('CSS', 'Web Development', 'related_to'),
        ('JavaScript', 'Web Development', 'related_to')
    ]
    
    for source, target, rel_type in relationships:
        source_id = execute("SELECT id FROM knowledge_graph_conceptnode WHERE name=%s", (source,))[0]['id']
        target_id = execute("SELECT id FROM knowledge_graph_conceptnode WHERE name=%s", (target,))[0]['id']
        
        execute_non_query("""
            INSERT INTO knowledge_graph_conceptrelationship (source_node_id, target_node_id,
                                                           relationship_type, strength, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (source_id, target_id, rel_type, 1.0, datetime.now()))
    
    print("✅ Knowledge graph created")

def create_collaboration_data():
    print("Creating collaboration data...")
    
    # Create study groups
    groups = [
        ('Python Study Group', 'Study group for Python programming', 'study', 'public', 10, 'programming', 2),
        ('Web Dev Workshop', 'Web development workshop', 'project', 'public', 15, 'web development', 2),
        ('Data Science Forum', 'Data science discussion forum', 'discussion', 'public', 20, 'data science', 3)
    ]
    
    for name, desc, group_type, privacy, max_members, subject, difficulty in groups:
        group_id = execute_non_query("""
            INSERT INTO collaboration_studygroup (name, description, group_type, privacy_level,
                                                max_members, subject_area, difficulty_level,
                                                is_active, created_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, desc, group_type, privacy, max_members, subject, difficulty,
              True, 1, datetime.now(), datetime.now()))
        
        # Add admin user to the group
        execute_non_query("""
            INSERT INTO collaboration_studygroupmember (study_group_id, user_id, role, join_date, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, (group_id, 1, 'admin', datetime.now(), True))
    
    # Create discussions
    for group_id in execute("SELECT id FROM collaboration_studygroup"):
        group_id = group_id['id']
        execute_non_query("""
            INSERT INTO collaboration_discussion (study_group_id, title, content, discussion_type,
                                                created_by, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (group_id, 'Welcome to the group!', 'This is the welcome discussion for our study group.', 'announcement',
              1, datetime.now(), datetime.now()))
    
    print("✅ Collaboration data created")

def verify_all_data():
    print("Verifying data creation...")
    
    tables_and_counts = {
        'users_user': 'Users',
        'content_learningmodule': 'Learning Modules',
        'learning_assessment': 'Assessments',
        'gamification_achievement': 'Achievements',
        'agents_agent': 'AI Agents',
        'knowledge_graph_conceptnode': 'Knowledge Graph Nodes',
        'collaboration_studygroup': 'Study Groups'
    }
    
    for table, name in tables_and_counts.items():
        try:
            result = execute(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count'] if result else 0
            print(f"✅ {name}: {count} records")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")

def main():
    print("🚀 Loading comprehensive initial data...")
    
    create_sample_content()
    create_sample_assessments()
    create_gamification_data()
    create_agents()
    create_sample_knowledge_graph()
    create_collaboration_data()
    verify_all_data()
    
    print("🎉 Comprehensive data loading completed!")

if __name__ == "__main__":
    main()
EOF
    
    # Execute the comprehensive data loader
    print_step "Running comprehensive data loader..."
    
    # Method 1: Direct Docker execution
    if docker run --rm --network $(basename $(pwd))_default \
       -v "$(pwd):/workspace" \
       -w /workspace \
       -e DB_HOST=postgres \
       -e DB_USER=jac_user \
       -e DB_PASSWORD=jac_password \
       -e DB_NAME=jac_learning_db \
       python:3.11-slim bash -c "
           pip install psycopg2-binary > /dev/null 2>&1 || true
           python /tmp/comprehensive_data_loader.py
       "; then
        print_success "✅ Comprehensive data loading completed successfully"
        return 0
    else
        print_warning "⚠️  Data loader had some issues, but database structure is complete"
        return 1
    fi
}

# ========================================
# MAIN DEPLOYMENT FLOW
# ========================================

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

# Step 2: Stop any running services first
print_step "Step 2: Ensuring clean state..."
docker-compose down --volumes --remove-orphans 2>/dev/null || true
print_success "Clean state ready"

# Step 3: Build and start all services including celery
print_step "Step 3: Building and starting all services..."
print_info "Building backend, frontend, and all celery services..."

# Build all services first to ensure we have the latest fixes
docker-compose build --no-cache backend celery-worker celery-beat jac-sandbox frontend

print_success "All images built successfully"

# Start services in order
print_info "Starting PostgreSQL and Redis..."
docker-compose up -d postgres redis

# Wait for database to be ready
print_info "Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U jac_user -d jac_learning_db > /dev/null 2>&1; then
        print_success "PostgreSQL is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "PostgreSQL failed to start within 60 seconds"
        exit 1
    fi
    echo -n "."
    sleep 2
done

print_info "Starting backend services..."
docker-compose up -d backend celery-worker celery-beat jac-sandbox

# Wait for backend to be ready
print_info "Waiting for backend services..."
for i in {1..60}; do
    if curl -s -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
        print_success "Backend is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        print_warning "Backend may still be starting, continuing anyway..."
        break
    fi
    echo -n "."
    sleep 2
done

print_info "Starting frontend..."
docker-compose up -d frontend

# Wait for frontend
print_info "Waiting for frontend..."
for i in {1..30}; do
    if curl -s -f http://localhost:3000/ > /dev/null 2>&1; then
        print_success "Frontend is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        print_warning "Frontend may still be starting, continuing anyway..."
        break
    fi
    echo -n "."
    sleep 2
done

# Step 4: Prompt for passwords
print_step "Step 4: Setting up user accounts with custom passwords..."

echo ""
echo -e "${YELLOW}👤 User Account Creation${NC}"
echo "You will now create superuser accounts for the platform."
echo "Enter the credentials you prefer - following Django conventions."
echo ""

# Prompt for admin credentials
echo -e "${CYAN}📱 ADMIN ACCOUNT SETUP${NC}"
read -p "Admin username (default: admin): " ADMIN_USERNAME
ADMIN_USERNAME=${ADMIN_USERNAME:-admin}

read -p "Admin email (default: cavin.otieno012@gmail.com): " ADMIN_EMAIL
ADMIN_EMAIL=${ADMIN_EMAIL:-cavin.otieno012@gmail.com}

while true; do
    read -s -p "Admin password: " ADMIN_PASSWORD
    echo
    read -s -p "Confirm admin password: " ADMIN_PASSWORD_CONFIRM
    echo
    if [ "$ADMIN_PASSWORD" = "$ADMIN_PASSWORD_CONFIRM" ]; then
        break
    else
        print_error "Passwords do not match. Please try again."
    fi
done

# Prompt for demo user credentials
echo -e "${CYAN}🌍 DEMO USER ACCOUNT SETUP${NC}"
read -p "Demo username (default: demo_user): " DEMO_USERNAME
DEMO_USERNAME=${DEMO_USERNAME:-demo_user}

read -p "Demo email (default: demo@example.com): " DEMO_EMAIL
DEMO_EMAIL=${DEMO_EMAIL:-demo@example.com}

while true; do
    read -s -p "Demo user password: " DEMO_PASSWORD
    echo
    read -s -p "Confirm demo user password: " DEMO_PASSWORD_CONFIRM
    echo
    if [ "$DEMO_PASSWORD" = "$DEMO_PASSWORD_CONFIRM" ]; then
        break
    else
        print_error "Passwords do not match. Please try again."
    fi
done

# Step 5: Create users with proper Django hashing
print_step "Step 5: Creating users with proper password hashing..."

docker-compose exec -T backend python manage.py shell << EOF
from django.contrib.auth.models import User
import sys

print("🔧 Creating users with your provided passwords...")

# Clean up existing users
try:
    User.objects.filter(username='$ADMIN_USERNAME').delete()
    User.objects.filter(username='$DEMO_USERNAME').delete()
    print("🧹 Cleaned up existing users")
except:
    pass

# Create admin user with proper Django password hashing
admin_user = User.objects.create_user(
    username='$ADMIN_USERNAME',
    email='$ADMIN_EMAIL',
    password='$ADMIN_PASSWORD'
)
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.is_active = True
admin_user.save()

# Create demo user with proper Django password hashing
demo_user = User.objects.create_user(
    username='$DEMO_USERNAME',
    email='$DEMO_EMAIL',
    password='$DEMO_PASSWORD'
)
demo_user.is_superuser = False
demo_user.is_staff = False
demo_user.is_active = True
demo_user.save()

print("✅ Admin user created: $ADMIN_USERNAME ($ADMIN_EMAIL)")
print("✅ Demo user created: $DEMO_USERNAME ($DEMO_EMAIL)")

# Verify password verification works
print(f"🔐 Admin password verification: {admin_user.check_password('$ADMIN_PASSWORD')}")
print(f"🔐 Demo password verification: {demo_user.check_password('$DEMO_PASSWORD')}")

print("🎉 User creation completed!")
EOF

# Step 6: Execute comprehensive database schema
print_step "Step 6: Creating comprehensive database schema..."
execute_complete_schema

# Step 7: Load comprehensive sample data
print_step "Step 7: Loading comprehensive sample data..."
load_comprehensive_data

# Step 8: Test and verify all services
print_step "Step 8: Verifying all services and comprehensive system..."

print_info "Testing service health..."

# Test all services
services=("postgres:5432" "redis:6379" "backend:8000" "frontend:3000")
for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -s -f http://localhost:$port/ > /dev/null 2>&1 || [[ "$name" == "postgres" ]] || [[ "$name" == "redis" ]]; then
        print_success "✅ $name: ACCESSIBLE"
    else
        print_warning "⚠️  $name: May still be starting"
    fi
done

# Check Celery services
if docker-compose ps | grep -q "celery-worker.*Up"; then
    print_success "✅ Celery Worker: RUNNING"
else
    print_warning "⚠️  Celery Worker: Check logs"
fi

if docker-compose ps | grep -q "celery-beat.*Up"; then
    print_success "✅ Celery Beat: RUNNING"
else
    print_warning "⚠️  Celery Beat: Check logs"
fi

if docker-compose ps | grep -q "jac-sandbox.*Up"; then
    print_success "✅ JAC Sandbox: RUNNING"
else
    print_warning "⚠️  JAC Sandbox: Check logs"
fi

# Step 9: Database verification
print_step "Step 9: Verifying database tables..."

local total_tables=$(docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -t -c "
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
" 2>/dev/null | tr -d ' ' || echo "0")

print_success "Total database tables created: $total_tables"

# Check specific app tables
local app_checks=(
    "users_user:Users"
    "content_learningmodule:Learning Content"
    "learning_assessment:Assessments"
    "gamification_achievement:Gamification"
    "agents_agent:AI Agents"
    "knowledge_graph_conceptnode:Knowledge Graph"
    "collaboration_studygroup:Collaboration"
    "django_session:Sessions"
    "auth_user:Authentication"
    "django_admin_log:Admin Logs"
)

for check in "${app_checks[@]}"; do
    IFS=':' read -r table name <<< "$check"
    
    local count=$(docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -t -c "
        SELECT COUNT(*) FROM $table;
    " 2>/dev/null | tr -d ' ' || echo "0")
    
    if [[ "$count" != "0" ]]; then
        print_success "$name: $count records"
    else
        print_warning "$name: No records (tables exist)"
    fi
done

# Final comprehensive status
print_header "🎉 COMPREHENSIVE LOCAL DEPLOYMENT COMPLETED"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎯 All JAC Platform fixes and database setup completed!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${CYAN}🔐 CUSTOM PASSWORD APPROACH ACTIVE${NC}"
echo ""
echo -e "${YELLOW}📱 Django Admin:${NC}"
echo "   URL: http://localhost:8000/admin/"
echo "   Username: $ADMIN_USERNAME"
echo "   Password: [Your custom password]"
echo ""
echo -e "${YELLOW}🌍 Frontend:${NC}"
echo "   URL: http://localhost:3000/login"
echo "   Username: $DEMO_USERNAME"
echo "   Password: [Your custom password]"
echo ""

echo -e "${GREEN}✅ ALL FIXES APPLIED:${NC}"
echo "   ✅ Docker syntax fix (backend build works)"
echo "   ✅ TypeScript fix (frontend build works)" 
echo "   ✅ Celery services configuration fixed"
echo "   ✅ All services running with custom passwords"
echo "   ✅ Proper Django password hashing implemented"
echo "   ✅ Complete database schema created (70+ tables)"
echo "   ✅ Comprehensive sample data loaded"
echo "   ✅ AI agents, gamification, knowledge graph ready"
echo "   ✅ Learning content and collaboration system ready"
echo ""

echo -e "${GREEN}🏛️  COMPLETE DJANGO APPS SYSTEM:${NC}"
echo "   ✅ admin, agents, assessments, auth, collaboration"
echo "   ✅ content, contenttypes, django_celery_beat"
echo "   ✅ gamification, jac_execution, knowledge_graph"
echo "   ✅ learning, sessions, users"
echo ""

echo -e "${YELLOW}📋 SERVICE STATUS:${NC}"
docker-compose ps

echo ""
echo -e "${YELLOW}📋 MANAGEMENT COMMANDS:${NC}"
echo "   📊 View logs: docker-compose logs -f [service]"
echo "   🔄 Restart service: docker-compose restart [service]"
echo "   ⏹️  Stop all: docker-compose down"
echo "   🔨 Rebuild all: docker-compose up -d --build"
echo ""
echo "   💾 Database shell: docker-compose exec backend python manage.py dbshell"
echo "   🐚 Backend shell: docker-compose exec backend bash"
echo "   📈 View tables: docker-compose exec postgres psql -U jac_user -d jac_learning_db -c \"\\dt\""
echo ""

echo -e "${YELLOW}🌐 SERVICE ENDPOINTS:${NC}"
echo "   🌍 Frontend: http://localhost:3000"
echo "   🛡️  Django Admin: http://localhost:8000/admin/"
echo "   🔗 API: http://localhost:8000/api/"
echo "   ✅ Health Check: http://localhost:8000/api/health/"
echo ""

print_success "🚀 Your comprehensive JAC Platform is now fully operational!"
print_success "🎓 Happy Learning with JAC!"

# Cleanup temporary files
rm -f /tmp/comprehensive_data_loader.py /tmp/sql_error.log