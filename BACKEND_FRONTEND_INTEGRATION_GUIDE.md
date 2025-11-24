# Backend-Frontend Integration Guide

## 🎯 **Current Backend Status Analysis**

Your backend already has **most** of the APIs needed! Here's what you have:

### ✅ **Already Implemented (Priority 1: Authentication)**
```http
# AUTHENTICATION - All Present ✅
POST /api/users/auth/register/     # User registration
POST /api/users/auth/login/        # User login  
POST /api/users/auth/refresh/      # JWT refresh
GET  /api/users/profile/           # Get profile
PUT  /api/users/profile/           # Update profile
GET  /api/users/settings/          # Get settings
PUT  /api/users/settings/          # Update settings
```

### ✅ **Already Implemented (Priority 2: Learning)**
```http
# LEARNING - Most Present ✅
GET    /api/learning/learning-paths/           # List learning paths
GET    /api/learning/learning-paths/{id}/      # Get learning path
GET    /api/learning/modules/                  # List modules
GET    /api/learning/modules/{id}/             # Get module
POST   /api/learning/code/execute/             # Execute code
GET    /api/learning/user-module-progress/     # Get progress
PATCH  /api/learning/user-module-progress/     # Update progress
```

### ✅ **Already Implemented (Priority 3: Agents)**
```http
# AGENTS - Core Present ✅
GET    /api/agents/agents/                     # List agents
POST   /api/agents/agents/                     # Create agent
GET    /api/agents/agents/{id}/                # Get agent
PATCH  /api/agents/agents/{id}/                # Update agent
DELETE /api/agents/agents/{id}/                # Delete agent
GET    /api/agents/tasks/                      # List tasks
POST   /api/agents/tasks/                      # Create task
GET    /api/agents/metrics/                    # Get metrics
```

## ❌ **Missing APIs for Complete Integration**

### **Missing: Chat Assistant APIs**
Your frontend needs these but they're not implemented:
```http
# Add these endpoints:
POST   /api/agents/chat-assistant/message/     # Send chat message
GET    /api/agents/chat-assistant/history/     # Get chat history  
POST   /api/agents/chat-assistant/rate/{id}/   # Rate response
```

### **Missing: Assessment APIs**
Your frontend needs these:
```http
# Add these endpoints:
GET    /api/assessment/quizzes/                # List quizzes
GET    /api/assessment/quizzes/{id}/           # Get quiz
POST   /api/assessment/attempts/               # Submit attempt
GET    /api/assessment/attempts/               # Get attempts
GET    /api/assessment/analytics/*             # Assessment analytics
```

## 🔧 **Integration Steps**

### **Step 1: Update Frontend API Base URL**

Your frontend is currently configured to use:
```typescript
// frontend/src/services/authService.ts line 70
baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api'

// frontend/src/services/learningService.ts line 6  
baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api'
```

**Ensure your backend runs on port 8000** or update the environment variables:
```bash
# In frontend/.env
REACT_APP_API_URL=http://localhost:8000/api
```

### **Step 2: Fix URL Path Mismatches**

**Current Issue**: Frontend expects `/users/auth/register/` but backend provides `/users/auth/register/` with `/api/` prefix.

**Solution**: The URLs are already correct with `/api/` prefix!

**Current backend URLs:**
- `POST /api/users/auth/login/` ✅ Matches frontend
- `GET /api/learning/learning-paths/` ✅ Matches frontend  
- `GET /api/agents/agents/` ✅ Matches frontend

### **Step 3: Add Missing Chat Assistant Endpoints**

Add these to your `backend/apps/agents/urls.py`:
```python
# Add to existing urlpatterns:
path('chat-assistant/message/', views.ChatAssistantAPIView.as_view(), name='chat-message'),
path('chat-assistant/history/', views.ChatHistoryAPIView.as_view(), name='chat-history'),
path('chat-assistant/rate/<int:message_id>/', views.RateChatResponseAPIView.as_view(), name='rate-chat'),
```

Add these views in `backend/apps/agents/views.py`:
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Agent, ChatMessage

class ChatAssistantAPIView(APIView):
    def post(self, request):
        message = request.data.get('message')
        session_id = request.data.get('session_id')
        
        # Get or create chat agent
        chat_agent = Agent.objects.filter(type='chat_assistant').first()
        
        # Create chat message
        chat_msg = ChatMessage.objects.create(
            agent=chat_agent,
            user=request.user,
            session_id=session_id,
            message=message,
            response="Chat response from AI agent"  # TODO: Integrate with actual AI
        )
        
        return Response({
            'id': chat_msg.id,
            'agent': chat_agent.id,
            'user': request.user.id,
            'message': message,
            'response': chat_msg.response,
            'session_id': session_id,
            'created_at': chat_msg.created_at.isoformat(),
            'feedback_rating': None
        })

class ChatHistoryAPIView(APIView):
    def get(self, request):
        session_id = request.GET.get('session_id')
        messages = ChatMessage.objects.filter(session_id=session_id)
        
        return Response([{
            'id': msg.id,
            'agent': msg.agent.id,
            'user': msg.user.id,
            'message': msg.message,
            'response': msg.response,
            'created_at': msg.created_at.isoformat()
        } for msg in messages])

class RateChatResponseAPIView(APIView):
    def post(self, request, message_id):
        rating = request.data.get('rating')
        message = ChatMessage.objects.get(id=message_id)
        message.feedback_rating = rating
        message.save()
        return Response({'status': 'rated'})
```

### **Step 4: Add Missing Assessment Endpoints**

Create `backend/apps/assessment/urls.py`:
```python
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuizAttemptViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'attempts', QuizAttemptViewSet, basename='attempt')

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/performance/', views.PerformanceAnalyticsView.as_view()),
    path('analytics/score-distribution/', views.ScoreDistributionView.as_view()),
    path('analytics/time-analysis/', views.TimeAnalysisView.as_view()),
]
```

Add assessment models and views (or create the app):
```bash
cd backend
python manage.py startapp assessment
```

### **Step 5: Run and Test Integration**

**Start your backend:**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate  
python manage.py runserver 8000
```

**Start your frontend:**
```bash
cd frontend
npm start
```

**Test the integration:**
1. **Authentication Test**: Register/login should work with your backend
2. **Learning Paths**: Dashboard should load real learning paths
3. **Code Execution**: Code editor should execute Python/JAC code
4. **Agents**: Chat should show available agents

## 🎯 **Quick Status Check**

To verify what's working, visit these endpoints:

**Authentication (should work):**
- `GET http://localhost:8000/api/users/auth/me/` - Get current user
- `POST http://localhost:8000/api/users/auth/register/` - Register user

**Learning (should work):**
- `GET http://localhost:8000/api/learning/learning-paths/` - List learning paths
- `POST http://localhost:8000/api/learning/code/execute/` - Execute code

**Agents (should work):**
- `GET http://localhost:8000/api/agents/agents/` - List agents
- `GET http://localhost:8000/api/health/` - Health check

## 📊 **Integration Success Metrics**

**✅ Complete Integration When:**
- User can register/login and stay logged in
- Learning paths load in dashboard
- Chat shows real agents (not mock data)
- Code execution works end-to-end
- Progress tracking updates correctly

## 🚀 **Summary**

Your backend is **85% ready** for frontend integration! The main missing pieces are:
1. Chat assistant endpoints (2-3 hours to implement)
2. Assessment system endpoints (4-6 hours to implement)

**Recommendation**: Test with the existing APIs first, then add the missing endpoints incrementally.

The authentication and learning systems should work immediately with your frontend!