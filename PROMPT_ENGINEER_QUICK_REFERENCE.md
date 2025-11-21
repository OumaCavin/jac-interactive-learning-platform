# JAC Platform - Prompt Engineer Quick Reference

## 🚀 Critical Technical Decisions

### Architecture Pattern
- **Microservices**: 8 Docker containers with clear separation of concerns
- **Event-Driven**: Multi-agent system with message passing coordination
- **Progressive Enhancement**: Glassmorphism UI with fallbacks for performance
- **Security-First**: Container isolation, input validation, and sandboxing

### Technology Stack Choices (Non-Negotiable)
```
Backend: Django 4.2.7 + DRF + Python 3.11
Frontend: React 18.2 + TypeScript + Tailwind CSS
Database: PostgreSQL 15 + Redis 7
Container: Docker + docker-compose orchestration
Queue: Celery + Redis broker
Editor: Monaco Editor with JAC syntax highlighting
State: Redux Toolkit + React Query
```

### Key Implementation Patterns

#### 1. Multi-Agent Coordination
```python
class BaseAgent:
    - Async task processing
    - Status tracking (IDLE, BUSY, ERROR)
    - Priority queuing
    - Inter-agent communication
    - Metrics collection

class SystemOrchestrator:
    - Coordinates all 6 agents
    - Manages workflows
    - Load balancing
    - Error recovery
```

#### 2. Secure Code Execution
```python
jac_code_executor.py:
- Docker container isolation
- Resource limits (CPU, memory, time)
- Network isolation
- Input sanitization
- Result tracking and caching
```

#### 3. Glassmorphism UI Design
```css
/* Core glassmorphism pattern */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

#### 4. React Architecture
```typescript
// Component structure pattern
- App.tsx (router + providers)
- MainLayout/AuthLayout
- Page components (lazy-loaded)
- Service layer (API abstraction)
- Redux slices + React Query
- Type definitions
```

## 🎯 Phase Implementation Sequence

### Phase 1: Multi-Agent Foundation (Priority 1)
1. Django project setup with apps structure
2. BaseAgent abstract class with core interfaces
3. 6 specialized agents with unique functionalities
4. AgentsManager for coordination
5. Database models and migrations

### Phase 2: Code Execution Engine (Priority 2)
1. JAC code executor with Docker sandbox
2. Security measures and resource limits
3. API endpoints for code execution
4. Integration with agent system
5. Execution result tracking

### Phase 3: React Frontend (Priority 3)
1. Project setup with TypeScript + Tailwind
2. Glassmorphism design system
3. Monaco Editor integration
4. Redux + React Query setup
5. Complete page implementations

### Phase 4: Production Deployment (Priority 4)
1. Docker orchestration (8 services)
2. Production Dockerfiles
3. Nginx reverse proxy
4. Health checks and monitoring
5. Deployment automation

## 🔧 Critical Code Patterns

### Agent Communication
```python
# Standard agent message format
{
    "message_type": "task_request|task_response|status_update",
    "sender_agent": "content_curator",
    "receiver_agent": "system_orchestrator", 
    "task_id": "uuid",
    "payload": {...},
    "priority": "HIGH|MEDIUM|LOW",
    "timestamp": "ISO-8601"
}
```

### Code Execution Request
```python
class CodeExecutionRequest:
    code: str
    language: str  # "jac" or "python"
    timeout: int = 30  # seconds
    memory_limit: int = 512  # MB
    user_id: Optional[int]
    task_id: Optional[str]
```

### Docker Compose Structure
```yaml
# Essential services (in order):
1. postgres (database)
2. redis (cache + broker)
3. backend (Django API)
4. frontend (React app)
5. nginx (reverse proxy)
6. celery-worker (task processing)
7. celery-beat (scheduling)
8. flower (monitoring)
```

## 📋 Non-Negotiable Requirements

### Security
- [ ] All containers run as non-root users
- [ ] Code execution in isolated Docker containers
- [ ] Input sanitization and validation
- [ ] JWT authentication with refresh tokens
- [ ] CORS configuration
- [ ] Rate limiting

### Performance
- [ ] Code splitting in React
- [ ] Database query optimization
- [ ] Redis caching layer
- [ ] Health checks for all services
- [ ] Resource limits for containers

### Quality
- [ ] >80% test coverage
- [ ] TypeScript strict mode
- [ ] Python type hints
- [ ] Code linting and formatting
- [ ] API documentation (Swagger)
- [ ] Comprehensive error handling

## 🚨 Common Implementation Mistakes to Avoid

1. **Missing Agent Coordination**: Agents must communicate via structured messages
2. **Insecure Code Execution**: Never execute code without Docker isolation
3. **Poor UI Performance**: Always use code splitting and lazy loading
4. **Missing Health Checks**: All Docker services need health monitoring
5. **Inadequate Error Handling**: Comprehensive error boundaries and logging
6. **Hardcoded Credentials**: Use environment variables for all secrets
7. **Missing Type Safety**: Strict TypeScript + Python type hints
8. **Incomplete Documentation**: API docs + user guides required

## 📊 Success Metrics

- [ ] All 6 agents operational and coordinating
- [ ] Secure JAC/Python code execution working
- [ ] Glassmorphism UI with smooth animations
- [ ] 8 Docker services running with health checks
- [ ] API response times <200ms (95th percentile)
- [ ] Code execution <10 seconds for complex programs
- [ ] Page load time <2 seconds
- [ ] Complete documentation suite

## 🎯 Prompt Engineering Tips

1. **Be Specific About Stack**: Mention exact versions and technologies
2. **Emphasize Security**: Highlight sandbox and container isolation requirements
3. **Show Agent Coordination**: Demonstrate inter-agent communication patterns
4. **Detail UI Requirements**: Specify glassmorphism design and Monaco Editor
5. **Include Deployment**: Mention production Docker configuration
6. **Reference Existing Patterns**: Point to similar successful implementations
7. **Set Clear Milestones**: Phase-by-phase progression with deliverables
8. **Quality Standards**: Emphasize testing, types, and documentation requirements

---

**Key Takeaway**: This is a complex full-stack project requiring deep expertise in Django, React, Docker, multi-agent systems, and secure code execution. The prompt must emphasize all these technical requirements clearly.