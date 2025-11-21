# How to Get Sentry DSNs - Complete Guide

## 🚀 **Step-by-Step Process to Obtain Sentry DSNs**

### **Step 1: Create Sentry Account**
1. Go to [https://sentry.io/](https://sentry.io/)
2. Click "Start Free" or "Get Started"
3. Sign up with GitHub, Google, or email
4. Verify your email address

### **Step 2: Create Projects for JAC Platform**

#### **Option A: Separate Projects (Recommended)**

**Backend Project (Python/Django)**
1. Click "Projects" → "Create Project"
2. Select: **Platform: Python** → **Framework: Django**
3. Project Name: `jac-learning-platform-backend`
4. Click "Create Project"

**Frontend Project (React/TypeScript)**  
1. Click "Projects" → "Create Project"
2. Select: **Platform: JavaScript** → **Framework: React**
3. Project Name: `jac-learning-platform-frontend`
4. Click "Create Project"

#### **Option B: Single Multi-Service Project**

**Universal Platform Project**
1. Click "Projects" → "Create Project"  
2. Select: **Platform: JavaScript** (can handle both Python and JS)
3. Project Name: `jac-learning-platform`
4. Click "Create Project"

### **Step 3: Get DSN URLs**

#### **For Backend (Django + Celery)**
1. Go to **jac-learning-platform-backend** project
2. Click **Settings** (gear icon) → **Client Keys (DSN)**
3. Copy the **DSN** URL
4. Should look like: `https://abc123@sentry.io/123456`

#### **For Frontend (React)**
1. Go to **jac-learning-platform-frontend** project  
2. Click **Settings** → **Client Keys (DSN)**
3. Copy the **DSN** URL
4. Should look like: `https://def456@sentry.io/789012`

### **Step 4: Configure Environment Variables**

#### **Create .env file from template:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env and replace placeholder DSNs
nano .env  # or use your preferred editor
```

#### **Add your actual DSNs:**
```bash
# Replace these with your actual Sentry DSNs
SENTRY_DSN_BACKEND=https://your-actual-backend-dsn@sentry.io/project-id
REACT_APP_SENTRY_DSN=https://your-actual-frontend-dsn@sentry.io/project-id
```

### **Step 5: Test Sentry Integration**

#### **Backend Test**
```bash
# Start Django server
cd backend
python manage.py runserver

# Test error reporting by visiting a non-existent URL
curl http://localhost:8000/test-error
```

#### **Frontend Test**
```bash
# Start React app
cd frontend  
npm start

# Open browser and check browser console
# Navigate to pages to trigger potential errors
```

### **Step 6: Verify in Sentry Dashboard**

1. Go to your Sentry projects dashboard
2. Check for test errors and test events
3. Verify data is flowing correctly

## 🔧 **Configuration Examples**

### **Individual Project Setup**

```bash
# For jac-learning-platform-backend
# Project Type: Python/Django
# DSN Format: https://xxx@sentry.io/yyy
SENTRY_DSN_BACKEND=https://1234567890123456@sentry.io/1234567

# For jac-learning-platform-frontend  
# Project Type: JavaScript/React
# DSN Format: https://xxx@sentry.io/yyy
REACT_APP_SENTRY_DSN=https://9876543210987654@sentry.io/9876543
```

### **Single Project Setup**

```bash
# Use same DSN for all services
# Project Type: JavaScript (can handle Python)
SENTRY_DSN_BACKEND=https://abcd1234@sentry.io/abcd123
REACT_APP_SENTRY_DSN=https://abcd1234@sentry.io/abcd123
```

## 🏷️ **Finding Existing DSNs**

### **If You Already Have Projects:**
1. Login to [sentry.io](https://sentry.io/)
2. Go to **Projects** tab
3. Click on your project name
4. Click **Settings** → **Client Keys (DSN)**
5. Copy the DSN URL

### **Environment Variables Location**
```bash
# Check if DSNs are already set
echo $SENTRY_DSN_BACKEND
echo $REACT_APP_SENTRY_DSN

# View your .env file
cat .env | grep SENTRY
```

## 🔐 **Security Notes**

### **Never Do This:**
- ❌ Commit DSNs to Git
- ❌ Share DSNs in public forums
- ❌ Use production DSNs in development
- ❌ Post DSNs in documentation

### **Always Do This:**
- ✅ Use environment variables
- ✅ Separate DSNs for dev/staging/production
- ✅ Rotate DSNs if compromised
- ✅ Use different projects for different environments

## 🎯 **DSN Format Explanation**

```
https://[PUBLIC_KEY]@o[ORG_ID].ingest.sentry.io/[PROJECT_ID]

Example:
https://1234567890123456@o123456.ingest.sentry.io/1234567
     │               │        │         │
     │               │        │         └── Project ID
     │               │        └────────────────── Organization ID
     │               └────────────────────────── Public Key
     └──────────────────────────────────────── Protocol & Base URL
```

## 📊 **Expected DSN Examples**

### **Development DSNs**
```
# Test/Development environments
SENTRY_DSN_BACKEND=https://dev123@sentry.io/dev123
REACT_APP_SENTRY_DSN=https://dev456@sentry.io/dev456
```

### **Production DSNs**
```  
# Live production environments
SENTRY_DSN_BACKEND=https://prod123@sentry.io/prod123
REACT_APP_SENTRY_DSN=https://prod456@sentry.io/prod456
```

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **"DSN not configured" warnings**
```bash
# Check environment variables are set
echo $SENTRY_DSN_BACKEND
echo $REACT_APP_SENTRY_DSN

# Verify DSN format is correct
# Should start with https:// and contain @sentry.io/
```

#### **"No events received"**
```bash
# Check network connectivity
curl -I https://sentry.io/api/0/headless/test/

# Verify DSN is correct and active
# Check Sentry project settings for disabled keys
```

#### **"Rate limit exceeded"**
```bash
# Sentry has rate limits per DSN
# Wait and try again, or upgrade plan
# Reduce sample rates in configuration
```

## 🔄 **Quick Setup Commands**

### **Clone and Configure**
```bash
# 1. Clone the JAC platform
git clone <your-repo-url>
cd jac-learning-platform

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env with your DSNs
# Replace the placeholder DSNs with real ones from sentry.io

# 4. Start the platform
docker-compose up -d
```

### **Alternative: Direct Setup**
```bash
# For manual testing without Docker
cd backend
pip install sentry-sdk[django]
cp .env.example .env
# Edit .env with your DSNs
python manage.py runserver
```

## 🎯 **Summary**

To get Sentry DSNs:

1. **Create account** at sentry.io
2. **Create projects** (Backend + Frontend or Single)
3. **Copy DSN URLs** from Settings → Client Keys
4. **Configure .env** with your DSNs
5. **Test integration** and verify in dashboard

The DSNs will enable comprehensive error monitoring across your entire JAC Learning Platform!