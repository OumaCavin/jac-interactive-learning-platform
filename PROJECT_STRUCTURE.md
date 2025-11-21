# JAC Interactive Learning Platform - Complete Folder Structure

## 📁 Repository Structure

This document provides a comprehensive overview of the complete JAC Interactive Learning Platform repository structure, organized by functionality and following best practices for maintainable, scalable applications.

## 🌳 Root Directory Structure

```
jac-interactive-learning-platform/
├── 📁 backend/                     # Django backend application
├── 📁 frontend/                    # React frontend application  
├── 📁 monitoring/                  # Monitoring and observability stack
├── 📁 scripts/                     # Automation and deployment scripts
├── 📁 docs/                        # Documentation and specifications
├── 📁 tests/                       # Test suites for all components
├── 📁 jac_models/                  # JAC language models and examples
├── 📁 knowledge_graph/             # OSP knowledge graph implementation
├── 📁 shared/                      # Shared utilities and types
├── 📁 k8s/                         # Kubernetes deployment manifests
├── 📁 terraform/                   # Infrastructure as Code
├── 📁 helm/                        # Helm charts for K8s deployment
├── 📁 nginx/                       # Nginx configuration files
├── 📁 database/                    # Database scripts and migrations
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 docker-compose.yml           # Main Docker orchestration
├── 📄 docker-compose.monitoring.yml # Monitoring stack
├── 📄 docker-compose.prod.yml      # Production Docker configuration
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 Makefile                     # Build and automation commands
├── 📄 requirements.txt             # Python dependencies
├── 📄 package.json                 # Node.js dependencies
└── 📄 PROJECT_STRUCTURE.md         # This file
```

## 🔧 Backend Structure (Django)

```
backend/
├── 📁 config/                      # Django project configuration
│   ├── 📁 settings/                # Environment-specific settings
│   │   ├── __init__.py
│   │   ├── base.py                 # Base configuration
│   │   ├── development.py          # Development settings
│   │   ├── production.py           # Production settings
│   │   ├── test.py                 # Test settings
│   │   └── local.py                # Local development settings
│   ├── __init__.py
│   ├── urls.py                     # Main URL routing
│   ├── wsgi.py                     # WSGI configuration
│   ├── asgi.py                     # ASGI configuration
│   └── sentry.py                   # Sentry error monitoring
├── 📁 apps/                        # Django applications
│   ├── 📁 agents/                  # Multi-agent system
│   │   ├── 📁 migrations/          # Database migrations
│   │   ├── __init__.py
│   │   ├── admin.py                # Django admin configuration
│   │   ├── apps.py                 # Agent app configuration
│   │   ├── models.py               # Agent data models
│   │   ├── views.py                # Agent API views
│   │   ├── serializers.py          # Agent serialization
│   │   ├── urls.py                 # Agent URL routing
│   │   ├── tasks.py                # Celery tasks for agents
│   │   ├── signals.py              # Django signals
│   │   ├── base_agent.py           # Base agent class
│   │   ├── agents_manager.py       # Agent coordination system
│   │   ├── system_orchestrator.py  # Central orchestrator
│   │   ├── content_curator.py      # Content curation agent
│   │   ├── quiz_master.py          # Assessment generation agent
│   │   ├── evaluator.py            # Code evaluation agent
│   │   ├── progress_tracker.py     # Progress monitoring agent
│   │   ├── motivator.py            # Gamification agent
│   │   └── utils.py                # Agent utility functions
│   ├── 📁 learning/                # Learning management system
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py               # Learning data models
│   │   ├── views.py                # Learning API views
│   │   ├── serializers.py          # Learning serialization
│   │   ├── urls.py                 # Learning URL routing
│   │   ├── tasks.py                # Learning-related tasks
│   │   ├── jac_code_executor.py    # JAC code execution engine
│   │   ├── execution_sandbox.py    # Secure code execution
│   │   ├── learning_paths.py       # Learning path management
│   │   ├── assessments.py          # Assessment system
│   │   └── utils.py                # Learning utilities
│   ├── 📁 users/                   # User management
│   │   ├── 📁 migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py               # User data models
│   │   ├── views.py                # User API views
│   │   ├── serializers.py          # User serialization
│   │   ├── urls.py                 # User URL routing
│   │   ├── permissions.py          # Custom permissions
│   │   ├── authentication.py       # Custom authentication
│   │   └── utils.py                # User utilities
│   └── 📁 api/                     # API documentation and versioning
│       ├── __init__.py
│       ├── v1/                     # API version 1
│       │   ├── __init__.py
│       │   ├── urls.py
│       │   ├── views.py
│       │   └── serializers.py
│       └── docs.py                 # API documentation
├── 📁 static/                      # Static files
│   ├── 📁 css/
│   ├── 📁 js/
│   ├── 📁 images/
│   └── 📁 fonts/
├── 📁 media/                       # User-uploaded files
│   ├── 📁 avatars/
│   ├── 📁 code_samples/
│   └── 📁 learning_materials/
├── 📁 templates/                   # Django templates
│   ├── 📁 admin/                   # Admin templates
│   └── 📁 registration/            # Authentication templates
├── 📁 logs/                        # Application logs
│   ├── django.log
│   ├── celery.log
│   └── error.log
├── 📁 scripts/                     # Backend scripts
│   ├── __init__.py
│   ├── setup_admin.py              # Admin setup script
│   ├── load_fixtures.py            # Load test data
│   └── database_backup.py          # Database backup
├── 📁 tests/                       # Backend tests
│   ├── 📁 unit/                    # Unit tests
│   │   ├── test_agents.py
│   │   ├── test_learning.py
│   │   ├── test_users.py
│   │   └── test_utils.py
│   ├── 📁 integration/             # Integration tests
│   ├── 📁 e2e/                     # End-to-end tests
│   └── conftest.py                 # Pytest configuration
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── requirements-prod.txt           # Production dependencies
├── manage.py                       # Django management script
├── Dockerfile                      # Backend container
├── Dockerfile.dev                  # Development container
├── docker-compose.backend.yml      # Backend Docker config
└── pytest.ini                     # Pytest configuration
```

## 🎨 Frontend Structure (React)

```
frontend/
├── 📁 public/                      # Public assets
│   ├── index.html                  # Main HTML template
│   ├── favicon.ico
│   ├── manifest.json               # PWA manifest
│   └── robots.txt
├── 📁 src/                         # Source code
│   ├── 📁 components/              # React components
│   │   ├── 📁 layout/              # Layout components
│   │   │   ├── __tests__/          # Layout component tests
│   │   │   ├── MainLayout.tsx      # Main application layout
│   │   │   ├── AuthLayout.tsx      # Authentication layout
│   │   │   ├── Sidebar.tsx         # Navigation sidebar
│   │   │   ├── Header.tsx          # Application header
│   │   │   └── Footer.tsx          # Application footer
│   │   ├── 📁 ui/                  # UI components library
│   │   │   ├── __tests__/
│   │   │   ├── Button.tsx          # Button component
│   │   │   ├── Modal.tsx           # Modal component
│   │   │   ├── Input.tsx           # Input component
│   │   │   ├── Select.tsx          # Select component
│   │   │   ├── LoadingSpinner.tsx
│   │   │   ├── NotificationProvider.tsx
│   │   │   ├── ErrorBoundary.tsx
│   │   │   ├── Toast.tsx
│   │   │   └── index.ts            # UI component exports
│   │   ├── 📁 code/                # Code editor components
│   │   │   ├── __tests__/
│   │   │   ├── MonacoEditor.tsx    # Monaco code editor wrapper
│   │   │   ├── SyntaxHighlighter.tsx
│   │   │   ├── ExecutionResult.tsx
│   │   │   ├── CodeToolbar.tsx
│   │   │   ├── LineNumbers.tsx
│   │   │   └── JACLanguage.ts      # JAC language definition
│   │   ├── 📁 charts/              # Chart and graph components
│   │   │   ├── __tests__/
│   │   │   ├── ProgressChart.tsx
│   │   │   ├── LearningPathGraph.tsx
│   │   │   ├── AgentNetwork.tsx
│   │   │   └── KnowledgeGraph.tsx
│   │   └── 📁 shared/              # Shared components
│   │       ├── __tests__/
│   │       ├── PageHeader.tsx
│   │       ├── Card.tsx
│   │       ├── Badge.tsx
│   │       └── Loader.tsx
│   ├── 📁 pages/                   # Page components
│   │   ├── 📁 auth/                # Authentication pages
│   │   │   ├── __tests__/
│   │   │   ├── LoginPage.tsx       # Login page
│   │   │   ├── RegisterPage.tsx    # Registration page
│   │   │   ├── ForgotPassword.tsx  # Password reset
│   │   │   └── VerifyEmail.tsx     # Email verification
│   │   ├── 📁 learning/            # Learning pages
│   │   │   ├── __tests__/
│   │   │   ├── Dashboard.tsx       # Main dashboard
│   │   │   ├── LearningPaths.tsx   # Learning paths list
│   │   │   ├── LearningPathDetail.tsx
│   │   │   ├── ModuleContent.tsx   # Module content viewer
│   │   │   ├── ProgressTracker.tsx
│   │   │   └── Certificates.tsx    # Achievement certificates
│   │   ├── CodeEditor.tsx          # Code editor page
│   │   ├── KnowledgeGraph.tsx      # Knowledge graph visualization
│   │   ├── 📁 assessments/         # Assessment pages
│   │   │   ├── __tests__/
│   │   │   ├── Assessments.tsx     # Assessment list
│   │   │   ├── AssessmentDetail.tsx
│   │   │   ├── QuizPage.tsx        # Interactive quiz
│   │   │   └── ResultsPage.tsx     # Assessment results
│   │   ├── 📁 profile/             # User profile pages
│   │   │   ├── __tests__/
│   │   │   ├── ProfilePage.tsx
│   │   │   ├── SettingsPage.tsx
│   │   │   └── PreferencesPage.tsx
│   │   └── __tests__/              # Page-level tests
│   ├── 📁 services/                # API services layer
│   │   ├── __tests__/
│   │   ├── apiService.ts           # Main API service
│   │   ├── authService.ts          # Authentication service
│   │   ├── agentService.ts         # Agent interaction service
│   │   ├── executionService.ts     # Code execution service
│   │   ├── learningService.ts      # Learning management service
│   │   ├── assessmentService.ts    # Assessment service
│   │   ├── websocketService.ts     # WebSocket service
│   │   └── httpClient.ts           # HTTP client configuration
│   ├── 📁 store/                   # Redux store
│   │   ├── __tests__/
│   │   ├── store.ts                # Store configuration
│   │   ├── hooks.ts                # Store hooks
│   │   └── 📁 slices/              # Redux slices
│   │       ├── authSlice.ts        # Authentication state
│   │       ├── learningSlice.ts    # Learning state
│   │       ├── agentsSlice.ts      # Agents state
│   │       ├── uiSlice.ts          # UI state
│   │       └── notificationsSlice.ts
│   ├── 📁 types/                   # TypeScript type definitions
│   │   ├── __tests__/
│   │   ├── user.ts                 # User-related types
│   │   ├── learning.ts             # Learning-related types
│   │   ├── agents.ts               # Agent-related types
│   │   ├── execution.ts            # Code execution types
│   │   ├── api.ts                  # API response types
│   │   └── common.ts               # Common utility types
│   ├── 📁 utils/                   # Utility functions
│   │   ├── __tests__/
│   │   ├── constants.ts            # Application constants
│   │   ├── helpers.ts              # General helper functions
│   │   ├── validation.ts           # Form validation functions
│   │   ├── formatting.ts           # Data formatting utilities
│   │   ├── storage.ts              # Local storage utilities
│   │   ├── date.ts                 # Date manipulation utilities
│   │   ├── sentry.ts               # Sentry configuration
│   │   ├── analytics.ts            # Analytics tracking
│   │   └── performance.ts          # Performance monitoring
│   ├── 📁 hooks/                   # Custom React hooks
│   │   ├── __tests__/
│   │   ├── useAuth.ts              # Authentication hook
│   │   ├── useAgents.ts            # Agent interaction hook
│   │   ├── useLearning.ts          # Learning progress hook
│   │   ├── useLocalStorage.ts      # Local storage hook
│   │   ├── useWebSocket.ts         # WebSocket hook
│   │   └── useDebounce.ts          # Debounce hook
│   ├── 📁 contexts/                # React contexts
│   │   ├── __tests__/
│   │   ├── AuthContext.tsx         # Authentication context
│   │   ├── ThemeContext.tsx        # Theme context
│   │   └── NotificationContext.tsx # Notification context
│   ├── App.tsx                     # Main application component
│   ├── App.css                     # Application styles
│   ├── index.tsx                   # Application entry point
│   ├── index.css                   # Global styles
│   └── react-app-env.d.ts         # TypeScript definitions
├── 📁 cypress/                     # End-to-end tests
│   ├── fixtures/                   # Test fixtures
│   ├── integration/                # E2E test cases
│   ├── support/                    # Test support utilities
│   └── cypress.config.ts           # Cypress configuration
├── 📁 .storybook/                  # Storybook configuration
│   ├── main.ts                     # Storybook main config
│   ├── preview.ts                  # Storybook preview config
│   └── 📁 stories/                 # Component stories
├── package.json                    # Node.js dependencies
├── package-lock.json               # Dependency lock file
├── tsconfig.json                   # TypeScript configuration
├── tailwind.config.js              # Tailwind CSS configuration
├── postcss.config.js               # PostCSS configuration
├── jest.config.js                  # Jest testing configuration
├── webpack.config.js               # Webpack configuration
├── Dockerfile                      # Frontend container
├── Dockerfile.prod                 # Production container
├── nginx.conf                      # Nginx configuration
└── .env.example                    # Environment variables template
```

## 📊 Monitoring & Observability Structure

```
monitoring/
├── 📁 prometheus/                  # Prometheus configuration
│   ├── prometheus.yml              # Main Prometheus configuration
│   ├── 📁 rules/                   # Alerting rules
│   │   ├── alerts.yml              # Alert rules
│   │   ├── recording_rules.yml     # Recording rules
│   │   └── jac_learning_rules.yml  # Platform-specific rules
│   ├── 📁 targets/                 # Service discovery
│   └── 📁 exporters/               # Custom exporters
├── 📁 grafana/                     # Grafana dashboards
│   ├── 📁 dashboards/              # Dashboard definitions
│   │   ├── system-overview.json    # System overview dashboard
│   │   ├── application-performance.json
│   │   ├── business-intelligence.json
│   │   ├── infrastructure.json
│   │   └── jac-specific.json       # JAC learning metrics
│   ├── 📁 provisioning/            # Dashboard provisioning
│   │   ├── 📁 dashboards/          # Auto-provisioning
│   │   └── 📁 datasources/         # Data source configuration
│   └── 📁 datasources/             # Data source configs
├── 📁 loki/                        # Centralized logging
│   ├── loki-config.yml             # Loki configuration
│   ├── 📁 promtail/                # Log collection
│   │   ├── promtail-config.yml
│   │   └── 📁 scrape_configs/
│   └── 📁 logql/                   # LogQL queries
├── 📁 jaeger/                      # Distributed tracing
│   ├── jaeger-config.yml           # Jaeger configuration
│   ├── 📁 spans/                   # Custom span definitions
│   └── 📁 sampling/                # Sampling strategies
├── 📁 alertmanager/                # Alert management
│   ├── alertmanager.yml            # Alertmanager configuration
│   └── 📁 templates/               # Notification templates
├── 📁 node-exporter/               # System metrics
│   └── node-exporter-config.yml
├── 📁 custom-metrics/              # Custom metric collectors
│   ├── jac_agent_metrics.py
│   ├── code_execution_metrics.py
│   └── learning_progress_metrics.py
└── 📁 dashboards/                  # Additional dashboard configs
    ├── kubernetes-dashboard.json
    └── database-dashboard.json
```

## 🤖 Scripts & Automation Structure

```
scripts/
├── 📁 deployment/                  # Deployment scripts
│   ├── deploy.sh                   # Main deployment script
│   ├── docker-deploy.sh            # Docker deployment
│   ├── k8s-deploy.sh               # Kubernetes deployment
│   ├── heroku-deploy.sh            # Heroku deployment
│   └── rollback.sh                 # Rollback script
├── 📁 maintenance/                 # Maintenance scripts
│   ├── backup.sh                   # Database backup
│   ├── restore.sh                  # Database restore
│   ├── health-check.sh             # Health monitoring
│   ├── log-rotate.sh               # Log rotation
│   ├── cleanup.sh                  # Cleanup old data
│   └── update-deps.sh              # Update dependencies
├── 📁 testing/                     # Testing scripts
│   ├── run-tests.sh                # Run all tests
│   ├── run-unit-tests.sh           # Unit tests only
│   ├── run-integration-tests.sh    # Integration tests
│   ├── run-e2e-tests.sh            # End-to-end tests
│   └── load-testing.sh             # Load testing
├── 📁 development/                 # Development utilities
│   ├── setup-dev.sh                # Development setup
│   ├── generate-models.py          # Model generation
│   ├── create-migration.py         # Migration creation
│   ├── seed-data.py                # Seed test data
│   └── generate-docs.py            # Documentation generation
├── 📁 monitoring/                  # Monitoring setup
│   ├── setup-monitoring.sh         # Monitoring stack setup
│   ├── configure-alerts.sh         # Alert configuration
│   ├── backup-metrics.sh           # Metrics backup
│   └── update-dashboards.sh        # Dashboard updates
└── 📁 utils/                       # Utility scripts
    ├── common.sh                   # Common utilities
    ├── logging.sh                  # Logging utilities
    ├── validation.sh               # Validation utilities
    └── security.sh                 # Security utilities
```

## 📚 Documentation Structure

```
docs/
├── 📁 api/                         # API documentation
│   ├── openapi.yml                 # OpenAPI/Swagger specification
│   ├── graphql-schema.graphql      # GraphQL schema
│   ├── 📁 endpoints/               # Individual endpoint docs
│   │   ├── authentication.md
│   │   ├── users.md
│   │   ├── agents.md
│   │   ├── learning.md
│   │   ├── assessments.md
│   │   └── code-execution.md
│   └── 📁 examples/                # API usage examples
│       ├── curl-examples/
│       ├── python-examples/
│       └── javascript-examples/
├── 📁 architecture/                # Architecture documentation
│   ├── system-architecture.md      # Overall system architecture
│   ├── agent-system.md             # Multi-agent system design
│   ├── database-schema.md          # Database design
│   ├── api-design.md               # API architecture
│   ├── security-architecture.md    # Security design
│   ├── scalability.md              # Scalability considerations
│   └── 📁 diagrams/                # Architecture diagrams
│       ├── system-overview.puml
│       ├── database-erd.puml
│       ├── sequence-diagrams.puml
│       └── deployment-architecture.puml
├── 📁 deployment/                  # Deployment documentation
│   ├── docker-compose.md           # Docker deployment
│   ├── kubernetes.md               # K8s deployment
│   ├── cloud-deployment.md         # Cloud platform deployment
│   ├── environment-setup.md        # Environment configuration
│   ├── monitoring-setup.md         # Monitoring configuration
│   └── troubleshooting.md          # Common deployment issues
├── 📁 development/                 # Development documentation
│   ├── setup-guide.md              # Development setup
│   ├── coding-standards.md         # Coding standards and guidelines
│   ├── testing-strategy.md         # Testing approach
│   ├── contributing.md             # Contribution guidelines
│   ├── git-workflow.md             # Git workflow
│   └── performance-guidelines.md   # Performance best practices
├── 📁 user/                        # User documentation
│   ├── user-manual.md              # Complete user manual
│   ├── quick-start-guide.md        # Quick start for users
│   ├── learning-path-guide.md      # Learning path instructions
│   ├── assessment-guide.md         # Assessment instructions
│   ├── troubleshooting.md          # User troubleshooting
│   └── faq.md                      # Frequently asked questions
├── 📁 jac/                         # JAC language documentation
│   ├── jac-tutorial.md             # JAC programming tutorial
│   ├── jac-syntax-reference.md     # JAC syntax reference
│   ├── jac-examples/               # JAC code examples
│   │   ├── basic-examples/
│   │   ├── intermediate-examples/
│   │   └── advanced-examples/
│   └── jac-best-practices.md       # JAC best practices
└── 📁 guides/                      # General guides
    ├── admin-guide.md              # Administrator guide
    ├── api-integration.md          # Third-party integration
    ├── customization-guide.md      # Platform customization
    ├── backup-recovery.md          # Backup and recovery
    └── security-guide.md           # Security guidelines
```

## 🧪 Testing Structure

```
tests/
├── 📁 backend/                     # Backend tests
│   ├── 📁 unit/                    # Unit tests
│   │   ├── 📁 test_agents/
│   │   │   ├── test_base_agent.py
│   │   │   ├── test_system_orchestrator.py
│   │   │   ├── test_content_curator.py
│   │   │   ├── test_quiz_master.py
│   │   │   ├── test_evaluator.py
│   │   │   ├── test_progress_tracker.py
│   │   │   └── test_motivator.py
│   │   ├── 📁 test_learning/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   ├── test_serializers.py
│   │   │   ├── test_jac_executor.py
│   │   │   └── test_sandbox.py
│   │   ├── 📁 test_users/
│   │   ├── 📁 test_api/
│   │   ├── 📁 test_utils/
│   │   └── conftest.py             # Pytest configuration
│   ├── 📁 integration/             # Integration tests
│   │   ├── test_agent_workflow.py
│   │   ├── test_code_execution.py
│   │   ├── test_learning_paths.py
│   │   ├── test_assessment_system.py
│   │   └── test_user_progression.py
│   ├── 📁 e2e/                     # End-to-end tests
│   │   ├── test_complete_user_journey.py
│   │   ├── test_agent_coordination.py
│   │   └── test_system_performance.py
│   ├── 📁 fixtures/                # Test data fixtures
│   ├── 📁 mocks/                   # Mock objects and data
│   └── pytest.ini                 # Pytest configuration
├── 📁 frontend/                    # Frontend tests
│   ├── 📁 unit/                    # Unit tests
│   │   ├── 📁 components/
│   │   │   ├── test_Button.tsx
│   │   │   ├── test_Modal.tsx
│   │   │   ├── test_MonacoEditor.tsx
│   │   │   └── test_Layout.tsx
│   │   ├── 📁 pages/
│   │   ├── 📁 services/
│   │   ├── 📁 hooks/
│   │   ├── 📁 utils/
│   │   └── __mocks__/              # Jest mocks
│   ├── 📁 integration/             # Integration tests
│   │   ├── test_auth_flow.tsx
│   │   ├── test_learning_flow.tsx
│   │   ├── test_agent_interaction.tsx
│   │   └── test_code_editor.tsx
│   ├── 📁 e2e/                     # Cypress E2E tests
│   │   ├── cypress.config.ts
│   │   ├── 📁 specs/               # Test specifications
│   │   │   ├── auth.cy.ts
│   │   │   ├── learning.cy.ts
│   │   │   ├── code-editor.cy.ts
│   │   │   ├── assessments.cy.ts
│   │   │   └── agent-system.cy.ts
│   │   ├── 📁 fixtures/            # Test fixtures
│   │   └── 📁 support/             # Test support
│   └── 📁 performance/             # Performance tests
│       ├── test_page_load.tsx
│       ├── test_api_performance.tsx
│       └── test_memory_usage.tsx
└── 📁 load/                        # Load testing
    ├── 📁 k6/                      # K6 load tests
    │   ├── api-load-test.js
    │   ├── frontend-load-test.js
    │   ├── websocket-load-test.js
    │   └── database-load-test.js
    ├── 📁 artillery/               # Artillery tests
    └── 📁 locust/                  # Locust tests
```

## 🏗️ Infrastructure Structure

```
k8s/                                 # Kubernetes manifests
├── namespace.yaml                   # Kubernetes namespace
├── postgres.yaml                    # PostgreSQL deployment
├── redis.yaml                       # Redis deployment
├── backend.yaml                     # Backend deployment
├── frontend.yaml                    # Frontend deployment
├── celery-worker.yaml               # Celery worker deployment
├── celery-beat.yaml                 # Celery beat deployment
├── ingress.yaml                     # Ingress configuration
├── hpa.yaml                         # Horizontal Pod Autoscaler
├── pdb.yaml                         # Pod Disruption Budget
├── pvc.yaml                         # Persistent Volume Claims
├── secrets.yaml                     # Kubernetes secrets
├── configmap.yaml                   # ConfigMaps
├── service.yaml                     # Service definitions
├── network-policy.yaml              # Network policies
└── 📁 monitoring/                   # Monitoring in K8s
    ├── prometheus-config.yaml
    ├── grafana-config.yaml
    └── jaeger-config.yaml

terraform/                           # Infrastructure as Code
├── main.tf                          # Main Terraform configuration
├── variables.tf                     # Variable definitions
├── outputs.tf                       # Output definitions
├── 📁 modules/                      # Reusable modules
│   ├── 📁 eks/                      # EKS cluster module
│   ├── 📁 rds/                      # RDS module
│   ├── 📁 elasticache/              # ElastiCache module
│   ├── 📁 vpc/                      # VPC module
│   └── 📁 monitoring/               # Monitoring module
├── 📁 environments/                 # Environment-specific configs
│   ├── 📁 development/
│   ├── 📁 staging/
│   └── 📁 production/
└── 📁 scripts/                      # Terraform utilities
    ├── plan.sh
    ├── apply.sh
    └── destroy.sh

helm/                                # Helm charts
├── jac-learning-platform/           # Main application chart
│   ├── Chart.yaml                   # Chart metadata
│   ├── values.yaml                  # Default values
│   ├── templates/                   # Chart templates
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   ├── configmap.yaml
│   │   └── secrets.yaml
│   └── 📁 charts/                   # Subcharts
└── monitoring/                      # Monitoring charts
    ├── prometheus/
    ├── grafana/
    └── jaeger/

nginx/                               # Nginx configuration
├── nginx.conf                       # Main Nginx configuration
├── 📁 conf.d/                       # Additional configurations
│   ├── backend.conf                 # Backend proxy configuration
│   ├── frontend.conf                # Frontend configuration
│   ├── ssl.conf                     # SSL configuration
│   └── rate-limiting.conf           # Rate limiting
├── 📁 ssl/                          # SSL certificates
└── 📁 sites-available/              # Site configurations

database/                            # Database-related files
├── init.sql                         # Database initialization
├── 📁 migrations/                   # Migration scripts
├── 📁 seeds/                        # Seed data scripts
├── 📁 backup/                       # Backup scripts and templates
├── 📁 restore/                      # Restore scripts
└── 📁 optimization/                 # Database optimization scripts
```

## 📋 Shared Utilities

```
shared/                              # Shared utilities and types
├── 📁 types/                        # Shared TypeScript types
│   ├── api.types.ts                 # Common API types
│   ├── user.types.ts                # User-related types
│   ├── agent.types.ts               # Agent-related types
│   ├── learning.types.ts            # Learning-related types
│   ├── execution.types.ts           # Code execution types
│   └── common.types.ts              # Common utility types
├── 📁 utils/                        # Shared utility functions
│   ├── validation.ts                # Validation utilities
│   ├── formatting.ts                # Data formatting
│   ├── date.ts                      # Date manipulation
│   ├── storage.ts                   # Storage utilities
│   ├── security.ts                  # Security utilities
│   └── analytics.ts                 # Analytics utilities
├── 📁 constants/                    # Shared constants
│   ├── api.ts                       # API endpoints
│   ├── routes.ts                    # Application routes
│   ├── colors.ts                    # Color schemes
│   └── config.ts                    # Configuration constants
├── 📁 models/                       # Shared data models
│   ├── base.model.ts                # Base model interface
│   ├── agent.model.ts               # Agent model
│   ├── learning.model.ts            # Learning model
│   └── user.model.ts                # User model
└── 📁 middleware/                   # Shared middleware
    ├── auth.middleware.ts           # Authentication middleware
    ├── logging.middleware.ts        # Logging middleware
    └── validation.middleware.ts     # Validation middleware
```

## 🎯 JAC Models & Examples

```
jac_models/                          # JAC language resources
├── 📁 examples/                     # JAC code examples
│   ├── 📁 basic/                    # Basic JAC examples
│   │   ├── hello_world.jac
│   │   ├── nodes_and_edges.jac
│   │   ├── simple_walker.jac
│   │   └── basic_graph.jac
│   ├── 📁 intermediate/             # Intermediate examples
│   │   ├── complex_graph_operations.jac
│   │   ├── custom_walkers.jac
│   │   ├── data_structures.jac
│   │   └── algorithms.jac
│   ├── 📁 advanced/                 # Advanced examples
│   │   ├── machine_learning.jac
│   │   ├── network_analysis.jac
│   │   ├── graph_algorithms.jac
│   │   └── optimization_problems.jac
│   └── 📁 tutorials/                # Tutorial examples
│       ├── lesson_1_basics.jac
│       ├── lesson_2_graphs.jac
│       ├── lesson_3_walkers.jac
│       └── lesson_4_advanced.jac
├── 📁 templates/                    # JAC code templates
│   ├── project_template.jac         # New project template
│   ├── graph_template.jac           # Graph template
│   ├── walker_template.jac          # Walker template
│   └── algorithm_template.jac       # Algorithm template
├── 📁 reference/                    # JAC reference materials
│   ├── syntax_reference.md          # JAC syntax reference
│   ├── builtin_functions.md         # Built-in functions
│   ├── best_practices.md            # Best practices
│   └── troubleshooting.md           # Common issues and solutions
├── 📁 stdlib/                       # JAC standard library
│   ├── graph_operations.jac         # Graph utilities
│   ├── data_structures.jac          # Data structure implementations
│   ├── algorithms.jac               # Algorithm implementations
│   └── utils.jac                    # General utilities
└── 📁 tests/                        # JAC test files
    ├── basic_tests.jac
    ├── graph_tests.jac
    ├── walker_tests.jac
    └── performance_tests.jac
```

## 🧠 Knowledge Graph Implementation

```
knowledge_graph/                     # OSP Knowledge Graph
├── 📁 graph_models/                 # Graph data models
│   ├── node.py                      # Node model
│   ├── edge.py                      # Edge model
│   ├── graph.py                     # Graph model
│   ├── path.py                      # Path model
│   └── __init__.py
├── 📁 algorithms/                   # Graph algorithms
│   ├── __init__.py
│   ├── traversal.py                 # Graph traversal algorithms
│   ├── pathfinding.py               # Path finding algorithms
│   ├── centrality.py                # Centrality measures
│   ├── clustering.py                # Clustering algorithms
│   └── visualization.py             # Graph visualization
├── 📁 storage/                      # Graph storage backends
│   ├── __init__.py
│   ├── memory_storage.py            # In-memory storage
│   ├── database_storage.py          # Database storage
│   ├── redis_storage.py             # Redis storage
│   └── file_storage.py              # File-based storage
├── 📁 visualization/                # Graph visualization
│   ├── __init__.py
│   ├── d3_visualizer.py             # D3.js integration
│   ├── graphviz_visualizer.py       # GraphViz integration
│   ├── force_directed.py            # Force-directed layout
│   └── hierarchical.py              # Hierarchical layout
├── 📁 learning/                     # Learning-specific graph operations
│   ├── concept_graph.py             # Concept relationship graphs
│   ├── prerequisite_graph.py        # Learning prerequisite graphs
│   ├── skill_graph.py               # Skill progression graphs
│   └── assessment_graph.py          # Assessment relationship graphs
├── 📁 api/                          # Graph API
│   ├── __init__.py
│   ├── graph_api.py                 # Main graph API
│   ├── visualization_api.py         # Visualization API
│   └── analytics_api.py             # Analytics API
└── 📁 utils/                        # Graph utilities
    ├── __init__.py
    ├── validators.py                # Graph validation
    ├── converters.py                # Data conversion utilities
    ├── exporters.py                 # Graph export utilities
    └── importers.py                 # Graph import utilities
```

## 🔒 Security & Configuration Files

```
├── .env.example                     # Environment variables template
├── .env.development                 # Development environment
├── .env.staging                     # Staging environment
├── .env.production                  # Production environment
├── .gitignore                       # Git ignore rules
├── .dockerignore                    # Docker ignore rules
├── .editorconfig                    # Editor configuration
├── .prettierrc                      # Prettier configuration
├── .eslintrc.js                     # ESLint configuration
├── .eslintignore                    # ESLint ignore rules
├── .pylintrc                        # Python linting configuration
├── .flake8                          # Python code style checking
├── Makefile                         # Build and automation commands
├── docker-compose.yml               # Main Docker orchestration
├── docker-compose.monitoring.yml    # Monitoring stack
├── docker-compose.prod.yml          # Production configuration
├── docker-compose.dev.yml           # Development configuration
├── Dockerfile                       # Backend container
├── Dockerfile.dev                   # Development container
├── Dockerfile.prod                  # Production container
├── frontend/Dockerfile              # Frontend container
├── frontend/Dockerfile.prod         # Frontend production container
├── nginx/nginx.conf                 # Nginx configuration
├── nginx/ssl/                       # SSL certificates directory
├── security-scan-config.json        # Security scanning configuration
├── code-quality-config.yaml         # Code quality tools configuration
└── LICENSE                          # MIT License
```

## 📝 Documentation Files

```
├── README.md                        # Main project documentation
├── PROJECT_STRUCTURE.md             # This file
├── CONTRIBUTING.md                  # Contribution guidelines
├── CODE_OF_CONDUCT.md               # Code of conduct
├── CHANGELOG.md                     # Version changelog
├── LICENSE                          # MIT License
├── DEPLOYMENT_GUIDE.md              # Deployment documentation
├── MONITORING_OBSERVABILITY_GUIDE.md # Monitoring guide
├── API_DOCUMENTATION.md             # API documentation
├── ARCHITECTURE.md                  # Architecture overview
├── SECURITY.md                      # Security documentation
├── TROUBLESHOOTING.md               # Troubleshooting guide
└── SUPPORT.md                       # Support information
```

## 🎯 Usage Summary

### Quick Navigation
```bash
# Backend development
cd backend/

# Frontend development  
cd frontend/

# Monitoring and observability
cd monitoring/

# Deployment scripts
cd scripts/deployment/

# Documentation
cd docs/

# Testing
cd tests/

# Kubernetes manifests
cd k8s/

# Infrastructure as Code
cd terraform/
```

### Key Directories by Purpose

**🔧 Development**
- `backend/` - Django application
- `frontend/` - React application
- `shared/` - Shared utilities and types
- `scripts/development/` - Development utilities

**🚀 Deployment**
- `k8s/` - Kubernetes manifests
- `terraform/` - Infrastructure as Code
- `helm/` - Helm charts
- `scripts/deployment/` - Deployment automation
- `docker-compose*.yml` - Docker orchestration

**📊 Monitoring**
- `monitoring/` - Monitoring and observability stack
- `scripts/monitoring/` - Monitoring setup scripts
- `monitoring/grafana/` - Dashboards
- `monitoring/prometheus/` - Metrics configuration

**🧪 Testing**
- `tests/` - All test suites
- `tests/backend/` - Backend tests
- `tests/frontend/` - Frontend tests
- `tests/load/` - Load testing

**📚 Documentation**
- `docs/` - Comprehensive documentation
- `docs/api/` - API documentation
- `docs/architecture/` - System architecture
- `docs/user/` - User guides

**🎓 JAC Resources**
- `jac_models/` - JAC language examples and templates
- `knowledge_graph/` - OSP knowledge graph implementation
- `shared/models/` - Shared data models

---

**Author**: Cavin Otieno  
**Contact**: cavin.otieno012@gmail.com | +254708101604 | [LinkedIn](https://www.linkedin.com/in/cavin-otieno-9a841260/) | [WhatsApp](https://wa.me/254708101604)  
**Repository**: [github.com/OumaCavin/jac-interactive-learning-platform](https://github.com/OumaCavin/jac-interactive-learning-platform)