# JAC Interactive Learning Platform - Complete Generation Prompt

## 🎯 Project Overview

Create a comprehensive, production-ready **JAC Interactive Learning Platform** - an advanced multi-agent adaptive learning system for the Jaseci programming language using Object-Spatial Programming (OSP) concepts. This platform should integrate modern web technologies with AI-powered learning assistance.

## 🏗️ System Architecture Requirements

### Core Technology Stack
- **Backend**: Django 4.2.7 + Django REST Framework + Python 3.11
- **Frontend**: React 18.2.0 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL 15 with Redis 7 caching
- **Containerization**: Docker with multi-stage builds and docker-compose orchestration
- **Task Queue**: Celery with Redis broker
- **Code Execution**: Secure JAC/Python sandbox with Docker isolation
- **Authentication**: JWT with refresh tokens
- **State Management**: Redux Toolkit + React Query
- **UI Design**: Glassmorphism design system

### Infrastructure Services (8 Docker Containers)
1. **PostgreSQL 15**: Primary database with health checks
2. **Redis 7**: Caching and session store with password protection
3. **Django Backend**: REST API with 25+ endpoints
4. **React Frontend**: Modern SPA with TypeScript
5. **Nginx**: Reverse proxy with SSL/TLS support
6. **Celery Worker**: Background task processing
7. **Celery Beat**: Scheduled task management
8. **Flower**: Celery monitoring and management

## 🧠 Multi-Agent System Requirements

### 6 Specialized AI Agents
1. **ContentCurator Agent**: Curates and organizes learning materials, tracks content quality
2. **QuizMaster Agent**: Generates adaptive quizzes and assessments based on learning progress
3. **Evaluator Agent**: Provides intelligent code evaluation and feedback for JAC programs
4. **ProgressTracker Agent**: Monitors learning progress, generates analytics and insights
5. **Motivator Agent**: Provides encouragement, gamification, and achievement tracking
6. **SystemOrchestrator Agent**: Coordinates all agents, manages workflows and system performance

### Agent Implementation Details
- Each agent should inherit from a BaseAgent class with common interfaces
- Agents should support asynchronous task processing
- Include agent metrics tracking and performance monitoring
- Implement agent communication protocols and workflow coordination
- Support for agent scaling and load balancing

## 📚 Learning Platform Features

### Core Learning Features
1. **Adaptive Learning Paths**: Personalized learning sequences based on user progress and preferences
2. **OSP Knowledge Graph**: Interactive representation of JAC concepts and relationships using NetworkX
3. **Real-time Code Execution**: In-browser JAC/Python code execution with Monaco Editor integration
4. **Interactive Assessments**: Dynamic quizzes with AI-powered feedback and scoring
5. **Progress Tracking**: Detailed analytics dashboard with learning insights
6. **Gamification**: Achievement system, learning streaks, and progress badges
7. **Glassmorphism UI**: Modern, intuitive interface with smooth animations (Framer Motion)

### JAC-Specific Features
1. **JAC Syntax Highlighting**: Custom syntax highlighting for JAC in Monaco Editor
2. **JAC Code Execution**: Secure sandbox for JAC program execution
3. **OSP Visualization**: Interactive graph visualization of Object-Spatial Programming concepts
4. **JAC Built-in Actions**: Integration with Jaseci standard library
5. **Custom Actions Support**: Framework for extending JAC with custom functionality

## 🏭 Phase-by-Phase Implementation

### Phase 1: Multi-Agent System Foundation
**Deliverables:**
- Django project structure with modular apps (agents, learning, users)
- BaseAgent class with common interfaces and capabilities
- 6 specialized agent implementations with unique functionalities
- AgentsManager for coordination and task distribution
- Agent metrics tracking and monitoring
- Database models for agents, tasks, and agent communication

**Key Files:**
- `backend/apps/agents/base_agent.py` - Common agent interface
- `backend/apps/agents/agents_manager.py` - Agent coordination system
- `backend/apps/agents/system_orchestrator.py` - Central orchestrator
- `backend/apps/agents/content_curator.py` - Content curation agent
- `backend/apps/agents/quiz_master.py` - Assessment generation agent
- `backend/apps/agents/evaluator.py` - Code evaluation agent
- `backend/apps/agents/progress_tracker.py` - Progress monitoring agent
- `backend/apps/agents/motivator.py` - Gamification agent

### Phase 2: JAC Code Execution Engine
**Deliverables:**
- Secure code execution sandbox with Docker isolation
- Support for both JAC and Python code execution
- Resource limiting (CPU, memory, execution time)
- Code execution API with result tracking
- Integration with the multi-agent system for automated evaluation
- Security measures including input validation and sandboxing

**Key Files:**
- `backend/apps/learning/jac_code_executor.py` - Core execution engine
- `backend/config/execution_sandbox.py` - Docker container management
- `backend/apps/learning/views.py` - Code execution API endpoints
- `backend/apps/learning/serializers.py` - Execution request/response serialization

### Phase 3: React Frontend Application
**Deliverables:**
- Modern React 18 application with TypeScript
- Glassmorphism design system with Tailwind CSS
- Monaco Editor integration with JAC syntax highlighting
- Redux Toolkit state management and React Query for API calls
- Responsive design with mobile optimization
- Code splitting and lazy loading for performance
- Comprehensive routing and navigation system

**Key Files:**
- `frontend/src/App.tsx` - Main application component with routing
- `frontend/src/store/store.ts` - Redux store configuration
- `frontend/src/components/layout/MainLayout.tsx` - Main application layout
- `frontend/src/pages/Dashboard.tsx` - Learning dashboard
- `frontend/src/pages/CodeEditor.tsx` - Interactive code editor
- `frontend/src/pages/LearningPaths.tsx` - Learning path management
- `frontend/src/services/apiService.ts` - API communication layer
- `frontend/tailwind.config.js` - Glassmorphism design configuration

### Phase 4: Production Deployment
**Deliverables:**
- Complete Docker orchestration with 8 services
- Production-optimized Dockerfiles with multi-stage builds
- Nginx reverse proxy configuration with SSL/TLS
- Database migrations and seeding
- Health checks and monitoring setup
- Automated deployment scripts
- Security hardening and configuration

**Key Files:**
- `docker-compose.yml` - Complete service orchestration
- `backend/Dockerfile` - Production backend container
- `frontend/Dockerfile.prod` - Production frontend container
- `frontend/nginx.conf` - Nginx production configuration
- `deploy.sh` - Automated deployment script
- `PRODUCTION_DEPLOYMENT.md` - Comprehensive deployment guide

## 📋 Detailed Implementation Requirements

### Backend Implementation

#### Django Project Structure
```
backend/
├── config/
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── agents/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── base_agent.py
│   │   ├── agents_manager.py
│   │   ├── system_orchestrator.py
│   │   ├── content_curator.py
│   │   ├── quiz_master.py
│   │   ├── evaluator.py
│   │   ├── progress_tracker.py
│   │   └── motivator.py
│   ├── learning/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── jac_code_executor.py
│   │   └── execution_sandbox.py
│   └── users/
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       └── urls.py
├── requirements.txt
├── manage.py
└── Dockerfile
```

#### API Endpoints Requirements
- **Authentication**: `/api/auth/login`, `/api/auth/register`, `/api/auth/refresh`
- **User Management**: `/api/users/profile`, `/api/users/progress`
- **Learning Paths**: `/api/learning/paths`, `/api/learning/modules`
- **Code Execution**: `/api/execute`, `/api/execute/status/<id>`
- **Agent Operations**: `/api/agents/status`, `/api/agents/tasks`
- **Assessments**: `/api/assessments`, `/api/assessments/submit`
- **Knowledge Graph**: `/api/knowledge/graph`, `/api/knowledge/nodes`

### Frontend Implementation

#### React Application Structure
```
frontend/src/
├── components/
│   ├── layout/
│   │   ├── MainLayout.tsx
│   │   └── AuthLayout.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Modal.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── NotificationProvider.tsx
│   └── code/
│       ├── MonacoEditor.tsx
│       ├── SyntaxHighlighter.tsx
│       └── ExecutionResult.tsx
├── pages/
│   ├── Dashboard.tsx
│   ├── auth/
│   │   ├── LoginPage.tsx
│   │   └── RegisterPage.tsx
│   ├── learning/
│   │   ├── LearningPaths.tsx
│   │   ├── LearningPathDetail.tsx
│   │   └── ModuleContent.tsx
│   ├── CodeEditor.tsx
│   ├── KnowledgeGraph.tsx
│   └── assessments/
│       ├── Assessments.tsx
│       └── AssessmentDetail.tsx
├── services/
│   ├── apiService.ts
│   ├── authService.ts
│   ├── agentService.ts
│   └── executionService.ts
├── store/
│   ├── store.ts
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── learningSlice.ts
│   │   └── agentsSlice.ts
│   └── api/
│       └── apiSlice.ts
├── types/
│   ├── user.ts
│   ├── learning.ts
│   ├── agents.ts
│   └── execution.ts
└── utils/
    ├── constants.ts
    ├── helpers.ts
    └── validation.ts
```

#### UI/UX Requirements
- **Glassmorphism Design**: Glass-like components with backdrop blur effects
- **Color Scheme**: Dark theme with vibrant accent colors
- **Responsive Design**: Mobile-first approach with breakpoint optimization
- **Animations**: Smooth transitions using Framer Motion
- **Typography**: Modern font stack with proper hierarchy
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Code splitting, lazy loading, and optimization

### Code Execution Engine Requirements

#### Security Features
- **Container Isolation**: Docker containers with network isolation
- **Resource Limits**: CPU, memory, and time constraints
- **Input Validation**: Comprehensive code sanitization
- **Sandbox Environment**: Isolated execution with restricted permissions
- **Security Monitoring**: Real-time threat detection and logging

#### Performance Features
- **Async Execution**: Non-blocking code execution
- **Resource Pooling**: Reusable execution containers
- **Caching**: Result caching for repeated executions
- **Load Balancing**: Distribute execution load across workers
- **Monitoring**: Real-time execution metrics and alerting

### Multi-Agent System Requirements

#### Agent Architecture
- **BaseAgent Class**: Common interface with status, priority, and task handling
- **Agent Communication**: Message passing and event-driven coordination
- **Task Distribution**: Intelligent load balancing and task routing
- **State Management**: Agent state persistence and recovery
- **Performance Monitoring**: Metrics collection and analysis

#### Agent Workflows
- **Learning Path Generation**: ContentCurator + QuizMaster coordination
- **Code Evaluation**: Evaluator + SystemOrchestrator workflow
- **Progress Analysis**: ProgressTracker + Motivator interaction
- **Adaptive Assessment**: Multi-agent adaptive assessment generation
- **System Optimization**: Performance monitoring and optimization

## 🚀 Deployment and Production Requirements

### Docker Configuration
- **Multi-stage Builds**: Optimized image sizes with build caching
- **Health Checks**: Container health monitoring with automatic restart
- **Volume Management**: Persistent data storage for databases and cache
- **Network Isolation**: Secure inter-container communication
- **Resource Limits**: Memory and CPU constraints for all services

### Security Configuration
- **Non-root Containers**: All services running as non-root users
- **SSL/TLS**: HTTPS encryption with certificate management
- **Input Validation**: Comprehensive sanitization and validation
- **Rate Limiting**: API rate limiting and DDoS protection
- **CORS Configuration**: Proper cross-origin resource sharing setup

### Monitoring and Logging
- **Application Logs**: Structured logging with log rotation
- **Health Monitoring**: Service health checks and alerting
- **Performance Metrics**: Resource usage and performance tracking
- **Error Tracking**: Centralized error monitoring and alerting
- **User Analytics**: Learning progress and engagement tracking

## 📊 Performance and Scalability

### Performance Targets
- **API Response Time**: < 200ms for 95th percentile
- **Code Execution**: < 10 seconds for complex JAC programs
- **Page Load Time**: < 2 seconds for initial page load
- **Database Queries**: < 100ms for simple queries
- **Agent Response**: < 5 seconds for agent tasks

### Scalability Features
- **Horizontal Scaling**: Support for multiple instances of each service
- **Load Balancing**: Nginx load balancing for backend services
- **Database Optimization**: Query optimization and indexing
- **Caching Strategy**: Multi-level caching (Redis, CDN, application)
- **Auto-scaling**: Kubernetes-ready configuration

## 🔒 Security Requirements

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Granular permission system
- **Session Management**: Secure session handling with Redis
- **Password Security**: Bcrypt hashing with salt rounds
- **API Security**: Authentication middleware and guards

### Code Execution Security
- **Sandboxing**: Isolated execution environment
- **Resource Limits**: Memory, CPU, and time constraints
- **Network Isolation**: No external network access
- **File System Security**: Restricted file system access
- **Input Sanitization**: Comprehensive code validation

## 📝 Documentation Requirements

### Technical Documentation
- **API Documentation**: Swagger/OpenAPI specification
- **Code Comments**: Comprehensive inline documentation
- **Architecture Diagrams**: System and data flow diagrams
- **Deployment Guide**: Step-by-step deployment instructions
- **Developer Guide**: Setup and development workflow

### User Documentation
- **User Manual**: Platform usage instructions
- **JAC Tutorial**: Comprehensive JAC learning guide
- **API Examples**: Code examples for developers
- **Troubleshooting**: Common issues and solutions
- **FAQ**: Frequently asked questions

## ✅ Quality Assurance

### Testing Requirements
- **Unit Tests**: Comprehensive test coverage (>80%)
- **Integration Tests**: API and service integration testing
- **End-to-End Tests**: Complete user workflow testing
- **Performance Tests**: Load testing and optimization
- **Security Tests**: Penetration testing and vulnerability assessment

### Code Quality
- **Linting**: ESLint for JavaScript/TypeScript, Pylint for Python
- **Formatting**: Prettier for JavaScript, Black for Python
- **Type Safety**: TypeScript strict mode, Python type hints
- **Code Review**: Peer review process and guidelines
- **Documentation**: Comprehensive inline and external documentation

## 🎯 Success Criteria

The platform should successfully demonstrate:

1. **Complete Multi-Agent System**: All 6 agents functioning and coordinating
2. **Secure Code Execution**: Safe JAC/Python code execution with sandboxing
3. **Modern UI/UX**: Responsive, glassmorphism design with smooth interactions
4. **Production Deployment**: Fully containerized, scalable, and secure deployment
5. **Comprehensive Documentation**: Complete technical and user documentation
6. **Quality Assurance**: Extensive testing and code quality measures
7. **Performance Targets**: Meeting all specified performance requirements
8. **Security Compliance**: All security requirements implemented and verified

## 🔧 Final Deliverables

1. **Complete Source Code**: Full application with all components
2. **Docker Configuration**: Production-ready containerization
3. **Deployment Scripts**: Automated deployment and management
4. **Documentation Suite**: Technical and user documentation
5. **Testing Suite**: Comprehensive test coverage
6. **Performance Optimization**: Optimized for production use
7. **Security Hardening**: Production security configuration
8. **Monitoring Setup**: Health checks and monitoring configuration

---

**Project Timeline**: Single comprehensive session development
**Expected Code Volume**: 15,000+ lines across all components
**Target Users**: JAC programming learners, educators, and developers
**Deployment Target**: Production-ready for immediate use

This prompt should guide the generation of a complete, production-ready JAC Interactive Learning Platform with all the features, components, and quality standards specified.