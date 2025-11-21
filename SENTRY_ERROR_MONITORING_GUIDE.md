# Sentry DSN Error Monitoring Configuration

## 🎯 **Platform Coverage for Sentry DSN**

### **1. Django Backend Application (Primary)**
```python
# backend/config/settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_BACKEND'),
    integrations=[
        DjangoIntegration(auto_enabling=True),
        CeleryIntegration(monitor_beat_tasks=True),
        RedisIntegration(),
    ],
    traces_sample_rate=0.1,  # Performance monitoring
    send_default_pii=False,   # Privacy protection
    environment=os.getenv('ENVIRONMENT', 'development'),
)
```

**Monitored Areas:**
- ✅ API endpoint errors (500, 502, 504)
- ✅ Database connection issues
- ✅ Agent coordination failures
- ✅ JAC code execution errors
- ✅ User authentication issues
- ✅ Learning path processing errors
- ✅ Assessment generation failures

### **2. React Frontend Application**
```javascript
// frontend/src/index.tsx
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN_FRONTEND,
  integrations: [
    new BrowserTracing({
      tracingOrigins: ["localhost", /^https:\/\/.*\.yourdomain\.com/],
    }),
  ],
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV,
});
```

**Monitored Areas:**
- ✅ React component rendering errors
- ✅ JavaScript runtime exceptions
- ✅ API call failures
- ✅ Monaco Editor integration errors
- ✅ Code execution UI failures
- ✅ User interaction errors
- ✅ Form submission issues

### **3. Celery Worker Processes**
```python
# backend/config/celery.py
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN_CELERY'),
    integrations=[CeleryIntegration(monitor_beat_tasks=True)],
    traces_sample_rate=0.1,
    environment=os.getenv('ENVIRONMENT', 'development'),
)
```

**Monitored Areas:**
- ✅ Agent task execution failures
- ✅ Code execution worker errors
- ✅ Background processing timeouts
- ✅ Queue processing issues
- ✅ Agent communication breakdowns
- ✅ Batch assessment generation errors

### **4. Docker Container Monitoring**
```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - SENTRY_DSN_BACKEND=${SENTRY_DSN_BACKEND}
      - ENVIRONMENT=${ENVIRONMENT:-production}
    
  celery-worker:
    environment:
      - SENTRY_DSN_CELERY=${SENTRY_DSN_CELERY}
      - ENVIRONMENT=${ENVIRONMENT:-production}
    
  frontend:
    environment:
      - REACT_APP_SENTRY_DSN_FRONTEND=${REACT_APP_SENTRY_DSN_FRONTEND}
      - NODE_ENV=${NODE_ENV:-production}
```

## 🔍 **Sentry Configuration Types**

### **Development Environment**
```bash
# .env file
SENTRY_DSN_BACKEND=https://xxx@sentry.io/project-id
SENTRY_DSN_FRONTEND=https://yyy@sentry.io/project-id  
SENTRY_DSN_CELERY=https://zzz@sentry.io/project-id
ENVIRONMENT=development
```

### **Production Environment**
```bash
# .env.production
SENTRY_DSN_BACKEND=https://prod-backend@sentry.io/project-id
SENTRY_DSN_FRONTEND=https://prod-frontend@sentry.io/project-id
SENTRY_DSN_CELERY=https://prod-celery@sentry.io/project-id
ENVIRONMENT=production
NODE_ENV=production
```

## 📊 **Error Monitoring Scope**

### **Backend Python Application**
- **API Errors**: HTTP 500, 502, 504 responses
- **Database Issues**: Connection errors, query timeouts
- **Agent System**: Coordination failures, task processing errors
- **JAC Execution**: Code sandbox failures, timeout errors
- **Authentication**: Login failures, JWT token issues
- **Learning System**: Path generation errors, progress tracking failures

### **Frontend React Application**
- **JavaScript Errors**: Runtime exceptions, undefined references
- **React Errors**: Component rendering failures, state issues
- **API Integration**: Failed API calls, network timeouts
- **Code Editor**: Monaco Editor initialization errors
- **User Interface**: Form validation, navigation failures

### **Celery Background Tasks**
- **Task Execution**: Agent task failures, processing errors
- **Queue Management**: Redis connection issues, task timeouts
- **Agent Coordination**: Inter-agent communication failures
- **Code Processing**: JAC execution in worker context

## 🚨 **Critical Error Types to Monitor**

### **High Priority Errors**
1. **JAC Code Execution Failures** - Core platform functionality
2. **Agent System Breakdown** - Multi-agent coordination failures
3. **Database Connection Issues** - Data persistence problems
4. **Authentication System Failures** - User access problems
5. **API Endpoint Failures** - Service availability issues

### **Medium Priority Errors**
1. **UI Component Failures** - User experience issues
2. **Performance Degradation** - Slow response times
3. **Memory Leaks** - Resource consumption problems
4. **Cache Failures** - Redis connection issues

### **Low Priority Warnings**
1. **Minor UI Glitches** - Non-blocking visual issues
2. **Logging Warnings** - Non-critical system messages
3. **Development Errors** - Only in non-production

## 🔧 **Sentry Configuration Best Practices**

### **1. Environment Separation**
```python
# Separate DSNs for each environment
ENVIRONMENT_SENTRY_MAPPING = {
    'development': 'https://dev@sentry.io/project',
    'staging': 'https://staging@sentry.io/project', 
    'production': 'https://prod@sentry.io/project'
}
```

### **2. Performance Monitoring**
```python
# Enable performance tracing
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    traces_sample_rate=0.1,  # Sample 10% of transactions
    profiles_sample_rate=0.1,  # Profile 10% of transactions
)
```

### **3. Error Filtering**
```python
# Ignore specific errors in Python
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    before_send=lambda event, hint: filter_event(event, hint)
)

def filter_event(event, hint):
    # Ignore health check errors
    if event.get('request', {}).get('url', '').endswith('/health/'):
        return None
    return event
```

### **4. User Context (Anonymized)**
```python
# Add user context (without PII)
sentry_sdk.set_user({
    "id": user.id,  # Only user ID, no email/name
    "username": user.username,  # Safe username
})
```

## 📈 **Sentry Dashboard Organization**

### **Projects Structure**
```
JAC Learning Platform/
├── Backend API (Python/Django)
├── Frontend App (React/TypeScript)
├── Celery Workers (Python tasks)
├── Knowledge Graph (NetworkX)
├── Agent System (Multi-agent coordination)
└── Code Execution Engine
```

### **Alert Rules**
1. **Critical**: JAC execution failures affecting >10 users
2. **High**: Agent system coordination breakdown
3. **Medium**: API response time >5 seconds
4. **Low**: UI component rendering issues

## 🔒 **Security Considerations**

### **DSN Protection**
- Use environment variables for all DSNs
- Never commit DSNs to version control
- Use different projects for dev/staging/production
- Enable DSN security features in Sentry dashboard

### **Data Privacy**
- Enable `send_default_pii=False`
- Filter out sensitive user data
- Use IP anonymization
- Enable enhanced privacy features

### **Access Control**
- Restrict Sentry project access to development team
- Use Sentry organization with proper team permissions
- Regular security review of Sentry configurations

---

**Summary**: Sentry DSN error monitoring covers all critical applications in the JAC platform - Django backend, React frontend, Celery workers, and the complete containerized ecosystem. Each service gets its own DSN for proper environment separation and targeted monitoring.