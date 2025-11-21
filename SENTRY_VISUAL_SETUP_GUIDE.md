# 🎯 How to Get Sentry DSNs - Visual Guide

## 🔄 **Complete Workflow Diagram**

```
sentry.io Registration 
        ↓
Create Account (GitHub/Google)
        ↓
┌─────────────────────────────────────────────┐
│           Create Projects                    │
├─────────────────────────────────────────────┤
│  Option A: Separate Projects               │
│  ┌─────────────┐    ┌─────────────┐        │
│  │   Backend   │    │  Frontend   │        │
│  │  Python/    │    │ JavaScript/ │        │
│  │   Django    │    │   React     │        │
│  └─────────────┘    └─────────────┘        │
├─────────────────────────────────────────────┤
│  Option B: Single Project                  │
│  ┌─────────────────────────────────────────┐│
│  │        JavaScript Universal             ││
│  │     (Handles Python + JS)              ││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│        Get DSN URLs                         │
├─────────────────────────────────────────────┤
│  1. Click "Settings" (gear icon)           │
│  2. Click "Client Keys (DSN)"              │
│  3. Copy the DSN URL                       │
│  4. Format: https://xxx@sentry.io/yyy     │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│      Configure .env File                   │
├─────────────────────────────────────────────┤
│  SENTRY_DSN_BACKEND=your-backend-dsn       │
│  REACT_APP_SENTRY_DSN=your-frontend-dsn    │
│                                             │
│  Replace placeholders with real DSNs!     │
└─────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────┐
│        Start Monitoring                     │
├─────────────────────────────────────────────┤
│  docker-compose up -d                      │
│                                             │
│  ✅ Check sentry.io dashboard              │
│  ✅ Verify test events appear             │
│  ✅ Monitor all platform errors!          │
└─────────────────────────────────────────────┘
```

## 📋 **Step-by-Step Commands**

### **1. Registration & Project Creation**
```bash
# Go to sentry.io in browser
# Click "Start Free"
# Sign up with GitHub/Google
# Verify email address
```

### **2. Backend Project Setup**
```
Platform: Python
Framework: Django  
Project Name: jac-learning-platform-backend
```

### **3. Frontend Project Setup**
```
Platform: JavaScript
Framework: React
Project Name: jac-learning-platform-frontend
```

### **4. Copy DSNs**
```bash
# Backend DSN location:
# Backend Project → Settings → Client Keys (DSN) → Copy
SENTRY_DSN_BACKEND=https://123456789@sentry.io/123456

# Frontend DSN location:
# Frontend Project → Settings → Client Keys (DSN) → Copy  
REACT_APP_SENTRY_DSN=https://987654321@sentry.io/987654
```

### **5. Environment Configuration**
```bash
# Edit your .env file
cp .env.example .env
nano .env  # or use any editor

# Add your DSNs:
SENTRY_DSN_BACKEND=https://your-actual-backend-dsn@sentry.io/project-id
REACT_APP_SENTRY_DSN=https://your-actual-frontend-dsn@sentry.io/project-id
```

### **6. Start & Test**
```bash
# Launch platform
docker-compose up -d

# Check Sentry dashboard
# Visit: https://sentry.io

# Test by triggering errors:
# - Visit non-existent URLs
# - Submit invalid forms
# - Test code execution features
```

## 🎯 **DSN Format Examples**

### **What Real DSNs Look Like:**
```bash
# Real DSN examples:
SENTRY_DSN_BACKEND=https://1234567890123456@sentry.io/1234567
REACT_APP_SENTRY_DSN=https://9876543210987654@sentry.io/9876543

# Components breakdown:
https://[PUBLIC_KEY]@o[ORG_ID].ingest.sentry.io/[PROJECT_ID]
     │               │        │         │
     │               │        │         └── Project ID
     │               │        └────────────────── Organization ID  
     │               └────────────────────────── Public Key
     └──────────────────────────────────────── Protocol & Base URL
```

### **Where to Find Them:**
```
sentry.io Dashboard
    ↓
Projects (Tab)
    ↓
Your Project Name
    ↓
Settings (⚙️ icon)
    ↓
Client Keys (DSN)
    ↓
Copy the URL that starts with https://
```

## 🚀 **Expected Output**

### **Before Setup:**
```bash
# No error monitoring
❌ Errors go untracked
❌ No performance insights
❌ No user experience data
```

### **After Setup:**
```bash
# Complete error monitoring
✅ All errors tracked in real-time
✅ Performance issues detected
✅ User experience monitored
✅ Agent system failures captured
✅ JAC execution errors logged
```

## 🔧 **Alternative: Single Command Setup**

If you have your DSNs ready:

```bash
# Quick setup
echo "SENTRY_DSN_BACKEND=your-dsn-here" >> .env
echo "REACT_APP_SENTRY_DSN=your-dsn-here" >> .env
docker-compose up -d

# That's it! Start monitoring immediately.
```

## 📊 **Monitoring Coverage**

```
JAC Learning Platform
├── Frontend (React)
│   ├── UI Component Errors ✅
│   ├── JavaScript Exceptions ✅
│   └── API Integration Issues ✅
│
├── Backend (Django)
│   ├── REST API Errors ✅
│   ├── Database Issues ✅
│   └── Agent Coordination ✅
│
├── Workers (Celery)
│   ├── Background Task Failures ✅
│   ├── Code Execution Errors ✅
│   └── Processing Timeouts ✅
│
└── Infrastructure
    ├── Container Health ✅
    ├── Request Routing ✅
    └── SSL/TLS Issues ✅
```

## 🎯 **Summary Answer**

**How to get Sentry DSNs:**

1. **Register** at sentry.io (2 minutes)
2. **Create** backend + frontend projects (1 minute)  
3. **Copy** DSN URLs from Settings → Client Keys (1 minute)
4. **Configure** .env file with your DSNs (1 minute)
5. **Start** monitoring with `docker-compose up -d`

**Total Time**: ~5 minutes to complete setup!

**Result**: Full error monitoring across your entire JAC Learning Platform ecosystem. 🚀