# Docker Deployment Troubleshooting Guide

## Problem: Backend Hangs During Startup

### **Symptom:**
```
✅ Database is ready!
⏳ Waiting for backend to be ready...
Backend not ready yet, waiting...
Backend not ready yet, waiting...
...
```

## **Root Cause Analysis**

The issue was caused by multiple factors:

1. **Complex Health Check Dependencies** - The original health endpoint required Django to be fully loaded, Redis connections, and database checks which could fail during startup
2. **Aggressive Health Check Timing** - Original settings gave insufficient time for Django initialization (40s start period with 30s intervals)
3. **Fragile Startup Sequence** - No fallback mechanisms for failed health checks
4. **Development vs Production Configuration** - Using `runserver` in Docker instead of proper production server

## **Implemented Solutions**

### 1. **Multiple Health Check Endpoints**

Created a hierarchy of health checks with different levels of dependencies:

#### Primary Health Check
- **Endpoint:** `http://localhost:8000/api/health/`
- **Status:** Full health check with database, Redis, and system status
- **Dependencies:** Django fully loaded, database connection, Redis (optional)

#### Fallback Health Checks
- **Simple Endpoint:** `http://localhost:8000/api/health/simple/`
  - Basic Django health check without complex dependencies
  - Graceful degradation for startup issues

- **Static Endpoint:** `http://localhost:8000/api/health/static/`
  - Minimal dependencies, works even if Django isn't fully loaded
  - Last resort health check

### 2. **Improved Docker Health Check Configuration**

**Before:**
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health/').read()"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**After:**
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request, time; 
         for url in ['http://localhost:8000/api/health/simple/', 'http://localhost:8000/api/health/']:
             try: 
                 response = urllib.request.urlopen(url, timeout=5)
                 if response.getcode() == 200: 
                     print('OK'); exit(0)
             except: 
                 continue
         print('FAIL'); exit(1)"]
  interval: 45s
  timeout: 15s
  retries: 5
  start_period: 90s
```

### 3. **Enhanced Startup Script**

**Key Improvements:**
- ✅ Better error handling and graceful degradation
- ✅ 60-second timeout for database migrations
- ✅ More detailed logging for troubleshooting
- ✅ Fallback behavior when dependencies fail

### 4. **Debug Tools**

Created `startup_debug.py` script for troubleshooting:
```bash
cd backend && python startup_debug.py
```

## **Testing the Fix**

### 1. **Clean Deployment**
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Rebuild with new configuration
docker-compose up --build

# Monitor backend startup
docker-compose logs -f backend
```

### 2. **Check Health Endpoints**
```bash
# Test primary health check
curl http://localhost:8000/api/health/

# Test simple health check
curl http://localhost:8000/api/health/simple/

# Test static health check
curl http://localhost:8000/api/health/static/
```

### 3. **Monitor Container Health**
```bash
# Check container health status
docker-compose ps

# View health check logs
docker inspect $(docker-compose ps -q backend) | jq '.[0].State.Health'
```

## **Future Prevention**

### **Health Check Best Practices**

1. **Multiple Levels of Health Checks**
   - Static endpoint (no dependencies)
   - Basic endpoint (minimal dependencies)  
   - Full endpoint (all dependencies)

2. **Reasonable Timeouts**
   - Start period: 90+ seconds for complex applications
   - Interval: 45-60 seconds to avoid overwhelming the service
   - Timeout: 10-15 seconds for health check requests
   - Retries: 3-5 attempts

3. **Graceful Degradation**
   - Health checks should NOT depend on all services being perfect
   - Redis/secondary service failures shouldn't fail the health check
   - Database migrations should not block health checks indefinitely

### **Monitoring Checklist**

- [ ] Database connection tested
- [ ] Redis connection tested (optional)
- [ ] Static file serving working
- [ ] Basic API endpoints responding
- [ ] Django admin accessible
- [ ] Frontend can communicate with backend

## **Common Issues & Solutions**

### **Issue: "Database not ready yet"**
**Solution:** Increase database connection timeout in entrypoint script

### **Issue: "Migration timeout"**
**Solution:** Add `check=False` to migration command and log warnings

### **Issue: "Health check timeout"**
**Solution:** Use multiple health endpoints with fallbacks

### **Issue: "Permission denied"**
**Solution:** Use non-root user in Dockerfile with proper ownership

### **Issue: "Import errors"**
**Solution:** Ensure all dependencies are installed and PYTHONPATH is set

## **Quick Diagnosis Commands**

```bash
# Check if backend is responding
curl -I http://localhost:8000/api/health/

# View backend logs in real-time
docker-compose logs -f backend

# Check backend container status
docker-compose ps backend

# Test database connectivity
docker-compose exec backend python -c "
import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings');
import django; django.setup();
from django.db import connection;
cursor = connection.cursor(); cursor.execute('SELECT 1');
print('Database connection OK')
"

# Run startup debug script
docker-compose exec backend python startup_debug.py
```

## **Performance Monitoring**

```bash
# Monitor container resource usage
docker stats $(docker-compose ps -q backend)

# Check disk space for logs
docker-compose exec backend df -h /app

# Monitor network connectivity
docker-compose exec backend ping postgres
```

---

## **Summary**

The Docker deployment issue has been resolved through:
1. **Multi-level health checks** with graceful fallbacks
2. **Improved timing configurations** for complex application startup
3. **Better error handling** to prevent cascading failures
4. **Enhanced monitoring tools** for troubleshooting

The backend should now start reliably and respond to health checks within 90 seconds, even if some dependencies (Redis, complex Django features) aren't immediately available.

**Next Steps:** The Docker containers will automatically pull these changes when restarted. Monitor the deployment logs to ensure smooth startup.

---

*Last Updated: 2025-11-23*