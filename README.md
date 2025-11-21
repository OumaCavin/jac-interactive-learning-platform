# JAC Interactive Learning Platform

An advanced multi-agent adaptive learning platform for the Jaseci programming language using Object-Spatial Programming (OSP), byLLM AI integration, and modern web technologies.

## 👨‍💻 Author Information

**Author**: Cavin Otieno  
**GitHub**: [OumaCavin](https://github.com/OumaCavin)  
**LinkedIn**: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)  
**Email**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com)  
**Phone**: +254708101604  
**WhatsApp**: [Contact via WhatsApp](https://wa.me/254708101604)  

## 🚀 Features

- **Adaptive Learning**: Personalized learning paths based on user progress and preferences
- **Multi-Agent System**: 6 specialized AI agents for comprehensive learning support
- **OSP Knowledge Graph**: Interactive representation of JAC concepts and relationships
- **Real-time Code Execution**: In-browser JAC code execution and visualization
- **Interactive Assessments**: Dynamic quizzes and evaluations with AI-powered feedback
- **Progress Tracking**: Detailed analytics and learning insights
- **Gamification**: Achievement system and learning streaks
- **Glassmorphism UI**: Modern, intuitive interface design
- **Monitoring & Observability**: Comprehensive monitoring with Prometheus, Grafana, and centralized logging
- **Security**: Production-ready security with JWT authentication and environment-based secrets

## 🏗️ Architecture

### Multi-Agent System
- **ContentCurator**: Curates and organizes learning materials
- **QuizMaster**: Generates adaptive quizzes and assessments
- **Evaluator**: Provides intelligent code evaluation and feedback
- **ProgressTracker**: Monitors and analyzes learning progress
- **Motivator**: Provides encouragement and gamification
- **SystemOrchestrator**: Coordinates all agents and workflows

### Technology Stack
- **Backend**: Django 4.2.7 + Django REST Framework + Python 3.11
- **Frontend**: React 18.2 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL 15 + Redis 7 (caching)
- **Containerization**: Docker + docker-compose orchestration
- **Task Queue**: Celery + Redis broker
- **Code Execution**: Secure JAC/Python sandbox with Docker isolation
- **Monitoring**: Prometheus + Grafana + ELK Stack
- **Authentication**: JWT with refresh tokens
- **State Management**: Redux Toolkit + React Query

## 📁 Complete Project Structure

```
jac-interactive-learning-platform/
├── backend/                          # Django backend application
│   ├── config/                       # Django configuration
│   │   ├── settings/                 # Environment-specific settings
│   │   │   ├── base.py               # Base settings
│   │   │   ├── development.py        # Development settings
│   │   │   ├── production.py         # Production settings
│   │   │   └── test.py               # Test settings
│   │   ├── urls.py                   # Main URL routing
│   │   ├── wsgi.py                   # WSGI configuration
│   │   └── sentry.py                 # Sentry error monitoring
│   ├── apps/                         # Django applications
│   │   ├── agents/                   # Multi-agent system
│   │   │   ├── models.py             # Agent data models
│   │   │   ├── views.py              # Agent API views
│   │   │   ├── serializers.py        # Agent serialization
│   │   │   ├── base_agent.py         # Base agent class
│   │   │   ├── agents_manager.py     # Agent coordination
│   │   │   ├── system_orchestrator.py
│   │   │   ├── content_curator.py
│   │   │   ├── quiz_master.py
│   │   │   ├── evaluator.py
│   │   │   ├── progress_tracker.py
│   │   │   └── motivator.py
│   │   ├── learning/                 # Learning management
│   │   │   ├── models.py             # Learning data models
│   │   │   ├── views.py              # Learning API views
│   │   │   ├── serializers.py        # Learning serialization
│   │   │   ├── jac_code_executor.py  # JAC code execution engine
│   │   │   └── execution_sandbox.py  # Secure code execution
│   │   └── users/                    # User management
│   ├── requirements.txt              # Python dependencies
│   ├── manage.py                     # Django management script
│   └── Dockerfile                    # Backend container
├── frontend/                         # React frontend application
│   ├── src/                          # Source code
│   │   ├── components/               # React components
│   │   │   ├── layout/               # Layout components
│   │   │   │   ├── MainLayout.tsx    # Main application layout
│   │   │   │   └── AuthLayout.tsx    # Authentication layout
│   │   │   ├── ui/                   # UI components
│   │   │   │   ├── Button.tsx        # Button components
│   │   │   │   ├── Modal.tsx         # Modal components
│   │   │   │   ├── LoadingSpinner.tsx
│   │   │   │   └── NotificationProvider.tsx
│   │   │   └── code/                 # Code editor components
│   │   │       ├── MonacoEditor.tsx  # Monaco code editor
│   │   │       ├── SyntaxHighlighter.tsx
│   │   │       └── ExecutionResult.tsx
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.tsx         # Main dashboard
│   │   │   ├── auth/                 # Authentication pages
│   │   │   │   ├── LoginPage.tsx     # Login page
│   │   │   │   └── RegisterPage.tsx  # Registration page
│   │   │   ├── learning/             # Learning pages
│   │   │   │   ├── LearningPaths.tsx
│   │   │   │   ├── LearningPathDetail.tsx
│   │   │   │   └── ModuleContent.tsx
│   │   │   ├── CodeEditor.tsx        # Code editor page
│   │   │   ├── KnowledgeGraph.tsx    # Knowledge graph visualization
│   │   │   └── assessments/          # Assessment pages
│   │   │       ├── Assessments.tsx
│   │   │       └── AssessmentDetail.tsx
│   │   ├── services/                 # API services
│   │   │   ├── apiService.ts         # Main API service
│   │   │   ├── authService.ts        # Authentication service
│   │   │   ├── agentService.ts       # Agent service
│   │   │   └── executionService.ts   # Code execution service
│   │   ├── store/                    # Redux store
│   │   │   ├── store.ts              # Store configuration
│   │   │   └── slices/               # Redux slices
│   │   │       ├── authSlice.ts      # Authentication state
│   │   │       ├── learningSlice.ts  # Learning state
│   │   │       └── agentsSlice.ts    # Agents state
│   │   ├── types/                    # TypeScript types
│   │   │   ├── user.ts               # User types
│   │   │   ├── learning.ts           # Learning types
│   │   │   ├── agents.ts             # Agent types
│   │   │   └── execution.ts          # Execution types
│   │   ├── utils/                    # Utilities
│   │   │   ├── constants.ts          # Application constants
│   │   │   ├── helpers.ts            # Helper functions
│   │   │   ├── validation.ts         # Validation functions
│   │   │   └── sentry.ts             # Sentry configuration
│   │   ├── App.tsx                   # Main app component
│   │   └── index.tsx                 # App entry point
│   ├── public/                       # Public assets
│   ├── package.json                  # Node dependencies
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── Dockerfile                    # Frontend container
│   └── nginx.conf                    # Nginx configuration
├── monitoring/                       # Monitoring and observability
│   ├── prometheus/                   # Prometheus configuration
│   │   ├── prometheus.yml            # Main config
│   │   └── rules/                    # Alerting rules
│   ├── grafana/                      # Grafana dashboards
│   │   ├── dashboards/               # Dashboard definitions
│   │   └── provisioning/             # Dashboard provisioning
│   ├── loki/                         # Centralized logging
│   │   └── loki-config.yml           # Loki configuration
│   └── jaeger/                       # Distributed tracing
│       └── jaeger-config.yml         # Jaeger configuration
├── docs/                             # Documentation
│   ├── api/                          # API documentation
│   │   └── openapi.yml               # OpenAPI/Swagger spec
│   ├── architecture/                 # Architecture diagrams
│   ├── deployment/                   # Deployment guides
│   │   ├── docker-compose.yml        # Local development
│   │   ├── kubernetes/               # K8s manifests
│   │   └── cloud/                    # Cloud deployment guides
│   └── onboarding/                   # Onboarding guide
├── scripts/                          # Automation scripts
│   ├── deploy.sh                     # Deployment automation
│   ├── backup.sh                     # Database backup
│   ├── monitoring-setup.sh           # Monitoring setup
│   └── health-check.sh               # Health monitoring
├── tests/                            # Test suites
│   ├── backend/                      # Backend tests
│   │   ├── unit/                     # Unit tests
│   │   ├── integration/              # Integration tests
│   │   └── e2e/                      # End-to-end tests
│   └── frontend/                     # Frontend tests
│       ├── unit/                     # Component tests
│       ├── integration/              # Integration tests
│       └── e2e/                      # E2E tests with Cypress
├── jac_models/                       # JAC language models
│   ├── examples/                     # JAC code examples
│   ├── templates/                    # JAC code templates
│   └── reference/                    # JAC reference materials
├── knowledge_graph/                  # OSP knowledge graph
│   ├── graph_models/                 # Graph data models
│   ├── algorithms/                   # Graph algorithms
│   └── visualization/                # Graph visualization utils
├── shared/                           # Shared utilities
│   ├── types/                        # Shared type definitions
│   ├── utils/                        # Common utilities
│   └── constants/                    # Shared constants
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore rules
├── docker-compose.yml                # Main orchestration
├── docker-compose.monitoring.yml     # Monitoring stack
├── README.md                         # This file
└── LICENSE                           # MIT License
```

## 🚦 Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 1. Clone Repository
```bash
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform
```

### 2. Set Up Git Configuration
```bash
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"
git branch -M main
```

### 3. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# Start with monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

### 5. Run Migrations
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser
```

### 6. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs/
- **Grafana Dashboard**: http://localhost:3001
- **Prometheus**: http://localhost:9090
- **Jaeger UI**: http://localhost:16686

## 📚 Learning Modules

1. **JAC Basics**: Introduction to JAC syntax and concepts
2. **Nodes & Edges**: Understanding OSP fundamentals
3. **Walkers**: Navigation and traversal patterns
4. **Built-in Actions**: Standard library functions
5. **Custom Actions**: Extending JAC with custom functionality
6. **Graph Operations**: Advanced graph manipulation
7. **Error Handling**: Debugging and error management
8. **Performance**: Optimization techniques
9. **Real-world Applications**: Practical project examples
10. **Best Practices**: Code organization and patterns
11. **Advanced Patterns**: Complex OSP patterns
12. **Integration**: Working with external systems

## 📊 Monitoring & Observability

### Metrics (Prometheus)
- **Application Metrics**: Request rates, response times, error rates
- **Business Metrics**: Learning progress, agent performance
- **Infrastructure Metrics**: CPU, memory, disk usage
- **Database Metrics**: Query performance, connection pools

### Logging (Loki + ELK Stack)
- **Centralized Logging**: All services log to centralized system
- **Log Aggregation**: Structured logging with correlation IDs
- **Log Retention**: Configurable retention policies
- **Alerting**: Error and warning alerts

### Tracing (Jaeger)
- **Distributed Tracing**: Request flow across services
- **Performance Analysis**: Identify bottlenecks
- **Error Tracking**: Trace errors through the system
- **Service Dependencies**: Visualize service architecture

### Dashboards (Grafana)
- **Real-time Dashboards**: Live system monitoring
- **Business Intelligence**: Learning analytics
- **Performance Metrics**: System performance visualization
- **Custom Alerts**: Configurable alerting rules

## 🔐 Security Features

- **Authentication**: JWT with refresh tokens
- **Authorization**: Role-based access control
- **Code Execution**: Sandboxed environment with resource limits
- **API Security**: Rate limiting, CORS configuration
- **Data Protection**: Input validation, SQL injection prevention
- **Environment Variables**: Secure secret management
- **Container Security**: Non-root containers, security scanning

## 🛠️ Development Workflow

### Git Workflow
```bash
# Clone repository
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform

# Set up git configuration
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"
git branch -M main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat(learning): add new learning module support"

# Push changes
git push origin feature/your-feature-name

# Create pull request and merge to main
```

### Package Management

#### Python Dependencies
```bash
# Development
pip install -r requirements.txt

# Update dependencies
pip install --upgrade package-name
pip freeze > requirements.txt

# Latest versions example
pip install \
  Django \
  djangorestframework \
  celery[redis] \
  gunicorn \
  python-decouple \
  sentry-sdk[django] \
  Pillow \
  django-cors-headers \
  django-extensions \
  pytest-django
```

#### Node.js Dependencies
```bash
# Install dependencies
npm ci

# Add new package
npm install package-name

# Update package
npm update package-name

# Production build
npm run build
```

## 🚀 Deployment Options

### 1. Docker Compose (Development/Staging)
```bash
# Clone repository
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform

# Set up environment
cp .env.example .env
# Configure .env with your settings

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### 2. Kubernetes (Production)
```bash
# Install Helm
curl https://get.helm.sh/helm-v3.11.0-linux-amd64.tar.gz | tar xz
sudo mv linux-amd64/helm /usr/local/bin/helm

# Add Helm repositories
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Deploy to Kubernetes
kubectl create namespace jac-learning
helm install jac-learning ./helm/chart --namespace jac-learning

# Check deployment
kubectl get pods -n jac-learning
```

### 3. Cloud Managed (AWS EKS)
```bash
# Create EKS cluster
eksctl create cluster \
  --name jac-learning-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 10

# Configure kubectl
aws eks update-kubeconfig --region us-west-2 --name jac-learning-cluster

# Deploy application
kubectl apply -f k8s/
```

### 4. PaaS (Heroku/Azure)
```bash
# Heroku deployment
heroku create jac-learning-platform
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
heroku config:set SECRET_KEY=your-secret-key
git subtree push --prefix backend heroku main

# Azure App Service
az webapp create --resource-group jac-learning-rg --plan jac-learning-plan --name jac-learning-platform
az webapp config connection-string set --resource-group jac-learning-rg --name jac-learning-platform --connection-string-type PostgreSQL --settings DefaultConnection=$DATABASE_URL
```

## 📋 Environment Variables

### Required Variables
```bash
# Django Configuration
SECRET_KEY=your-super-secure-secret-key-at-least-50-characters
DEBUG=False
ALLOWED_HOSTS=localhost,your-domain.com

# Database Configuration
DB_NAME=jac_learning_db
DB_USER=jac_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your-redis-password

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=cavin.otieno012@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sentry Error Monitoring
SENTRY_DSN_BACKEND=https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000
REACT_APP_SENTRY_DSN=https://ef79ebd29c8a961b5d5dd6c313ccf7ba@o4510403562307584.ingest.de.sentry.io/4510403631054928

# Google AI API
GOOGLE_API_KEY=AIzaSyB3OhghL8KcNaixdZkM4Wfd07_dAoQvrI0

# GitHub PAT
GITHUB_PAT=your-github-personal-access-token

# WhatsApp Integration
WHATSAPP_NUMBER=+254708101604
WHATSAPP_API_URL=https://wa.me/254708101604
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest
python -m pytest tests/unit/
python -m pytest tests/integration/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:unit
npm run test:integration
npm run test:e2e
```

### Load Testing
```bash
# Install k6
brew install k6  # macOS
apt install k6   # Ubuntu

# Run load tests
k6 run tests/load/api-load-test.js
k6 run tests/load/frontend-load-test.js
```

## 📈 Performance Optimization

- **Code Splitting**: React lazy loading for optimal bundle sizes
- **Database Optimization**: Query optimization and indexing
- **Caching Strategy**: Redis caching for frequently accessed data
- **CDN Integration**: Static asset delivery optimization
- **Container Optimization**: Multi-stage Docker builds
- **Horizontal Scaling**: Kubernetes HPA configuration

## 🔧 Maintenance

### Database Maintenance
```bash
# Backup database
./scripts/backup.sh

# Restore database
psql -U jac_user -d jac_learning_db < backup.sql

# Clean up old logs
find ./logs -name "*.log" -mtime +30 -delete
```

### Monitoring Checks
```bash
# Health check
./scripts/health-check.sh

# Performance check
curl http://localhost:8000/api/health/detailed

# Log analysis
tail -f logs/django.log | grep ERROR
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat(learning): add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Format
```
type(scope): description

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Test additions/updates
- chore: Build/maintenance changes

Examples:
feat(agents): add new evaluator agent functionality
fix(api): resolve JWT token expiration issue
docs(readme): update installation instructions
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Complete Documentation

### Architecture & Design Documentation

Our platform includes comprehensive architecture documentation with visual diagrams:

- **📋 [Documentation Index](docs/README_DOCUMENTATION_INDEX.md)** - Complete index of all documentation and resources
- **🏗️ [System Architecture Overview](docs/architecture_overview.png)** - High-level system architecture diagram
- **🚀 [Deployment Architecture](docs/deployment_architecture.png)** - Production deployment architecture
- **🤖 [Multi-Agent System](docs/multi_agent_system.png)** - 6-agent system architecture
- **📊 [UML Class Diagram](docs/class_diagram.png)** - Complete entity relationships and methods
- **👤 [UML Use Case Diagram](docs/use_case_diagram.png)** - User interactions and system capabilities
- **⚡ [Activity Diagram](docs/activity_diagram.png)** - Learning workflow and user journey
- **🔧 [Component Diagram](docs/component_diagram.png)** - System component architecture

### API & Development Documentation

- **📖 [OpenAPI/Swagger Specification](docs/api_reference.yaml)** - Complete REST API documentation with all endpoints, schemas, and examples
- **👨‍💻 [Complete Onboarding Guide](docs/onboarding_guide.md)** - Comprehensive user onboarding with tutorials and best practices
- **🛠️ [Project Generation Prompt](JAC_PLATFORM_GENERATION_PROMPT.md)** - LLM prompt to reproduce the entire project
- **⚡ [Prompt Engineer Quick Reference](PROMPT_ENGINEER_QUICK_REFERENCE.md)** - Quick technical reference for prompt engineering

### Deployment & Operations

- **📦 [Deployment Guide](DEPLOYMENT_GUIDE.md)** - Multiple deployment options (Docker, Kubernetes, AWS, GCP, PaaS)
- **📊 [Monitoring & Observability Guide](MONITORING_OBSERVABILITY_GUIDE.md)** - Complete monitoring stack (Prometheus, Grafana, Jaeger, Loki)
- **📁 [Project Structure](PROJECT_STRUCTURE.md)** - Complete folder structure with detailed descriptions
- **🐛 [Sentry Error Monitoring](SENTRY_ERROR_MONITORING_GUIDE.md)** - Sentry setup and configuration
- **🔑 [How to Get Sentry DSNs](HOW_TO_GET_SENTRY_DSNS.md)** - Step-by-step guide to obtain Sentry DSNs

### Project Reports

- **📋 [Project Completion Report](PROJECT_COMPLETION_REPORT.md)** - Phase-by-phase project completion summary
- **🔄 [Complete Transformation Summary](COMPLETE_TRANSFORMATION_SUMMARY.md)** - Summary of major transformations and updates
- **🔗 [Integration Status Report](INTEGRATION_STATUS_REPORT.md)** - System integration verification
- **🏭 [Production Deployment](PRODUCTION_DEPLOYMENT.md)** - Production deployment procedures

### Configuration & Setup

- **⚙️ [Environment Configuration](.env.example)** - Complete environment variables template with all credentials
- **🐳 [Docker Configuration](docker-compose.yml)** - Container orchestration configuration
- **🔒 [Security Setup](SENTRY_QUICK_SETUP.md)** - 5-minute Sentry configuration checklist

## 📞 Support

- **Email**: [cavin.otieno012@gmail.com](mailto:cavin.otieno012@gmail.com)
- **LinkedIn**: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)
- **Phone**: +254708101604
- **WhatsApp**: [Contact via WhatsApp](https://wa.me/254708101604)
- **GitHub Issues**: Create an issue for bugs or feature requests

## 🔗 Useful Links

- [API Documentation](http://localhost:8000/api/docs/)
- [GitHub Repository](https://github.com/OumaCavin/jac-interactive-learning-platform)
- [Docker Hub Images](https://hub.docker.com/u/jacplatform)
- [Monitoring Dashboards](http://localhost:3001)

---

**Author**: Cavin Otieno  
**Version**: 2.0.0  
**Last Updated**: 2025-11-21  
**License**: MIT  
**Repository**: [github.com/OumaCavin/jac-interactive-learning-platform](https://github.com/OumaCavin/jac-interactive-learning-platform)