# Backend Implementation Priority Guide

## 🎯 **Minimum Viable Backend (MVP)**

To get the frontend working with real backend APIs, you need to implement these **core endpoints** first:

### **Phase 1: Authentication (Days 1-2)**
**Most Critical** - Everything depends on authentication working

```bash
# Required Endpoints:
POST /users/auth/register/
POST /users/auth/login/
POST /users/auth/refresh/
GET  /users/profile/
PUT  /users/profile/
GET  /users/settings/
PUT  /users/settings/
```

**Key Features Needed:**
- JWT token generation and validation
- User registration and login
- Password hashing and validation
- Profile management
- Settings persistence

### **Phase 2: Learning Core (Days 2-3)**
**Essential for core functionality**

```bash
# Required Endpoints:
GET  /learning/learning-paths/
GET  /learning/learning-paths/{id}/
GET  /learning/modules/?learning_path={id}
GET  /learning/modules/{id}/
POST /learning/code/execute/
```

**Key Features Needed:**
- Learning path and module data management
- Code execution service (Python/JAC)
- User progress tracking

### **Phase 3: Agent Chat (Days 3-4)**
**Essential for chat functionality**

```bash
# Required Endpoints:
GET  /agents/
POST /agents/chat-assistant/message/
GET  /agents/chat-assistant/history/
```

**Key Features Needed:**
- Agent status management
- Chat message handling
- Session management

---

## 🚀 **Quick Start Implementation**

### **1. Authentication Setup**

**User Model (Database):**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_staff BOOLEAN DEFAULT false,
    -- Profile fields
    bio TEXT,
    profile_image VARCHAR(500),
    learning_style VARCHAR(20),
    preferred_difficulty VARCHAR(20),
    learning_pace VARCHAR(20),
    -- Statistics
    total_modules_completed INTEGER DEFAULT 0,
    total_time_spent VARCHAR(20) DEFAULT '0 minutes',
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    experience_level INTEGER DEFAULT 0,
    next_level_points INTEGER DEFAULT 100,
    -- Settings
    current_goal VARCHAR(500),
    goal_deadline DATE,
    agent_interaction_level VARCHAR(20) DEFAULT 'moderate',
    preferred_feedback_style VARCHAR(20) DEFAULT 'detailed',
    dark_mode BOOLEAN DEFAULT false,
    notifications_enabled BOOLEAN DEFAULT true,
    email_notifications BOOLEAN DEFAULT true,
    push_notifications BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

**JWT Configuration:**
```python
# Install: pip install pyjwt
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

### **2. Learning Path Setup**

**Database Models:**
```sql
CREATE TABLE learning_paths (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    estimated_duration INTEGER, -- in minutes
    modules_count INTEGER DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    learning_path_id INTEGER REFERENCES learning_paths(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT,
    order_index INTEGER,
    estimated_duration INTEGER,
    module_type VARCHAR(20) CHECK (module_type IN ('lesson', 'exercise', 'assessment')),
    prerequisites INTEGER[], -- Array of module IDs
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### **3. Agent Service Setup**

**Database Models:**
```sql
CREATE TABLE agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('code_evaluator', 'learning_coordinator', 'content_generator', 'progress_tracker', 'chat_assistant', 'knowledge_graph')),
    status VARCHAR(20) DEFAULT 'idle' CHECK (status IN ('idle', 'busy', 'error')),
    current_task TEXT,
    capabilities TEXT[], -- Array of capability strings
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(id),
    user_id UUID REFERENCES users(id),
    session_id VARCHAR(100),
    message TEXT NOT NULL,
    response TEXT,
    feedback_rating INTEGER CHECK (feedback_rating BETWEEN -1 AND 1),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📊 **Database Schema Summary**

**Tables Needed:**
1. `users` - User authentication and profiles
2. `learning_paths` - Learning paths/courses
3. `modules` - Individual learning modules
4. `agents` - AI agents
5. `chat_messages` - Chat history
6. `user_module_progress` - User progress tracking
7. `code_submissions` - Code execution results
8. `quizzes` - Assessment data
9. `quiz_attempts` - User quiz attempts

---

## 🧪 **Testing Strategy**

### **Authentication Testing:**
```bash
# Test Registration
curl -X POST http://localhost:8000/api/users/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123"
  }'

# Test Login
curl -X POST http://localhost:8000/api/users/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123"
  }'
```

### **Learning Path Testing:**
```bash
# Get Learning Paths
curl -X GET http://localhost:8000/api/learning/learning-paths/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Execute Code
curl -X POST http://localhost:8000/api/learning/code/execute/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello World\")",
    "language": "python"
  }'
```

---

## 🔧 **Recommended Tech Stack**

**Backend Framework:**
- **Django + DRF** (Python) - Fastest development
- **Express.js** (Node.js) - If you prefer JavaScript
- **FastAPI** (Python) - Modern, high performance

**Database:**
- **PostgreSQL** - Recommended for production
- **SQLite** - Good for development/testing

**Authentication:**
- **Django REST Framework JWT** or **PyJWT**
- **Passlib** for password hashing

**Code Execution:**
- **Docker containers** for isolated code execution
- **Judge0 API** or custom solution
- **Time and memory limits**

---

## ⚠️ **Important Notes**

### **Security Requirements:**
1. **Password Hashing**: Use `bcrypt` or `argon2`
2. **JWT Secret**: Use environment variables, never hardcode
3. **Rate Limiting**: Implement on auth endpoints
4. **Input Validation**: Validate all user inputs
5. **CORS Configuration**: Proper CORS settings for frontend

### **Performance Considerations:**
1. **Database Indexing**: Index frequently queried fields
2. **Caching**: Redis for session/token caching
3. **Code Execution**: Use worker queues (Celery/RQ)
4. **Pagination**: Implement for list endpoints

### **Development Workflow:**
1. **Start with authentication** - Everything depends on it
2. **Use migrations** - Track database changes
3. **Environment variables** - Never hardcode secrets
4. **API documentation** - Swagger/OpenAPI
5. **Testing** - Unit tests for all endpoints

---

## 🎯 **Success Metrics**

**Phase 1 Success Criteria:**
- ✅ User can register and login
- ✅ JWT tokens work correctly
- ✅ Profile and settings save/load
- ✅ Frontend authentication redirects work

**Phase 2 Success Criteria:**
- ✅ Learning paths load in frontend
- ✅ Modules display correctly
- ✅ Code execution works end-to-end
- ✅ Progress tracking updates

**Phase 3 Success Criteria:**
- ✅ Chat interface connects to real agents
- ✅ Messages save and load correctly
- ✅ Agent status updates in real-time

---

## 📞 **Next Steps**

1. **Choose your backend framework** (Django/Express/FastAPI)
2. **Set up the database** with the schema above
3. **Implement Phase 1** (authentication) first
4. **Test with frontend** - replace mock data gradually
5. **Deploy and scale** as needed

The frontend is **95% complete** and ready - it just needs these backend APIs to become fully functional!