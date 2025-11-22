# JAC Learning Platform Backend

Django-based backend for the JAC Interactive Learning Platform with multi-agent system integration.

## 🏗️ Architecture

- **Django 5.2.8**: Web framework (Updated 2025-11-22)
- **Django REST Framework**: API development
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **Celery**: Async task processing
- **NetworkX**: Knowledge graph management
- **Jaseci Integration**: JAC code execution engine

## 📁 Structure

```
backend/
├── config/              # Django settings and configuration
├── apps/
│   ├── users/           # User management and authentication
│   ├── learning/        # Core learning management
│   ├── content/         # Learning content and curriculum
│   ├── assessments/     # Quizzes and evaluations
│   ├── progress/        # Learning progress tracking
│   ├── agents/          # Multi-agent system implementation
│   ├── knowledge_graph/ # OSP knowledge graph
│   └── jac_execution/   # JAC code execution engine
├── shared/              # Shared utilities and types
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration
└── manage.py           # Django management
```

## 🚦 Development

### Local Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### API Endpoints
- `/api/users/` - User management
- `/api/learning/` - Learning paths and content
- `/api/assessments/` - Quizzes and evaluations
- `/api/progress/` - Progress tracking
- `/api/agents/` - Multi-agent interactions
- `/api/jac/` - JAC code execution
- `/api/graph/` - Knowledge graph operations

## 🤖 Multi-Agent System

### Agent Endpoints
- `POST /api/agents/content-curator/` - Content curation
- `POST /api/agents/quiz-master/` - Quiz generation
- `POST /api/agents/evaluator/` - Code evaluation
- `POST /api/agents/progress-tracker/` - Progress analysis
- `POST /api/agents/motivator/` - Motivation and gamification
- `POST /api/agents/orchestrator/` - System coordination

## 📊 Database Schema

### Core Models
- **User**: Extended user profile with learning preferences
- **LearningPath**: Personalized learning sequences
- **Module**: Individual learning modules
- **Assessment**: Quizzes and evaluations
- **Progress**: Learning progress tracking
- **KnowledgeNode**: OSP knowledge graph nodes
- **KnowledgeEdge**: OSP knowledge graph edges
- **CodeExecution**: JAC code execution results

## 🔧 Configuration

Environment variables:
- `DEBUG`: Development mode
- `SECRET_KEY`: Django secret key
- `DB_*`: Database configuration
- `REDIS_URL`: Redis connection
- `CELERY_*`: Celery configuration
- `JASECI_*`: Jaseci engine configuration
## ✅ Production Deployment (Verified 2025-11-22)

### Health Check Endpoint
The backend provides a comprehensive health check endpoint:

```bash
curl http://localhost:8000/api/health/
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22 09:33:02.271654+00:00",
  "service": "jac-interactive-learning-platform",
  "version": "1.0.0",
  "environment": "production",
  "database": "healthy",
  "redis": "healthy"
}
```

### Docker Health Check Configuration
```yaml
healthcheck:
  test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000', timeout=10)\""]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Production Verification Status
- ✅ Database connectivity: PostgreSQL operational
- ✅ Cache system: Redis connection healthy
- ✅ API endpoints: All REST endpoints responding
- ✅ Task queue: Celery worker and beat operational
- ✅ Error monitoring: Sentry integration active
- ✅ Docker health checks: Process-based monitoring configured

### Environment Setup for Production
```bash
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://:password@host:6379/0
CORS_ALLOWED_ORIGINS=https://your-domain.com
```