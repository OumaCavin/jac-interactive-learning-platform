# 🚀 Quick Sentry DSN Setup Checklist

## ⚡ **5-Minute Setup Guide**

### ✅ **Step 1: Create Sentry Account (2 minutes)**
- [ ] Go to [https://sentry.io](https://sentry.io)
- [ ] Click "Start Free" 
- [ ] Sign up with GitHub/Google
- [ ] Verify email

### ✅ **Step 2: Create Projects (1 minute)**
**Option A - Separate Projects:**
- [ ] Backend: Select **Python** → **Django**
- [ ] Frontend: Select **JavaScript** → **React**

**Option B - Single Project:**
- [ ] Universal: Select **JavaScript** (handles both)

### ✅ **Step 3: Copy DSN URLs (1 minute)**
- [ ] Backend Project → Settings → Client Keys (DSN) → Copy
- [ ] Frontend Project → Settings → Client Keys (DSN) → Copy

### ✅ **Step 4: Configure Environment (1 minute)**
```bash
# Edit .env file
nano .env

# Replace placeholder DSNs:
SENTRY_DSN_BACKEND=https://YOUR-BACKEND-DSN@sentry.io/PROJECT-ID
REACT_APP_SENTRY_DSN=https://YOUR-FRONTEND-DSN@sentry.io/PROJECT-ID
```

### ✅ **Step 5: Test & Verify**
```bash
# Start platform
docker-compose up -d

# Check Sentry dashboard for test events
# All errors will now be tracked!
```

## 🎯 **What You'll Get After Setup:**

### **Backend Monitoring:**
- ✅ Django API errors
- ✅ Database connection issues  
- ✅ Agent system failures
- ✅ JAC code execution errors

### **Frontend Monitoring:**
- ✅ React component crashes
- ✅ JavaScript errors
- ✅ API call failures
- ✅ Code editor issues

### **Worker Monitoring:**
- ✅ Celery task failures
- ✅ Background processing errors
- ✅ Agent coordination issues

## 📊 **Expected Results:**

```
Sentry Dashboard →
├── jac-learning-platform-backend
│   ├── Error tracking (0 test events)
│   ├── Performance monitoring  
│   └── Release tracking
└── jac-learning-platform-frontend
    ├── JavaScript errors
    ├── User experience monitoring
    └── Session replay
```

## 🔧 **Quick Commands:**

```bash
# 1. Create account and projects
# 2. Copy these DSN placeholders to .env:
SENTRY_DSN_BACKEND=https://placeholder@sentry.io/123456
REACT_APP_SENTRY_DSN=https://placeholder@sentry.io/789012

# 3. Replace with your actual DSNs from sentry.io
# 4. Start monitoring!
docker-compose up -d
```

## ⚠️ **Important Reminders:**

- **Free Tier**: Up to 5,000 errors/month
- **Separate DSNs**: Use different projects for dev/prod
- **Security**: Never commit .env with real DSNs
- **Testing**: Check Sentry dashboard for test events

---

**Result**: Complete error monitoring for your JAC Learning Platform! 🚀