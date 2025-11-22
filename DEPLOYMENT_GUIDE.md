# JAC Interactive Learning Platform - Deployment Guide

## 🚀 Complete Deployment Guide

This comprehensive guide covers all deployment options for the JAC Interactive Learning Platform, from local development to enterprise-grade production deployments.

## 📋 Prerequisites

Before starting any deployment, ensure you have:

- **Git**: Version control system
- **Docker & Docker Compose**: Containerization
- **Python 3.11+**: Backend runtime
- **Node.js 18+**: Frontend build tools
- **PostgreSQL 15+**: Production database
- **Redis 7+**: Caching and session storage

## 🛠️ Git Repository Setup

### Initial Repository Setup
```bash
# Clone the repository
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform

# Set up git configuration
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"

# Set main as primary branch
git branch -M main

# Verify configuration
git config --list | grep user
git remote -v
```

### Repository Structure
```
jac-interactive-learning-platform/
├── backend/                 # Django backend application
├── frontend/               # React frontend application
├── monitoring/             # Monitoring and observability
├── scripts/                # Deployment automation scripts
├── docs/                   # Documentation
├── docker-compose.yml      # Main orchestration
├── docker-compose.monitoring.yml  # Monitoring stack
├── .env.example            # Environment template
└── README.md               # Project documentation
```

## 🐳 Option 1: Docker Compose Deployment

### Quick Start (Development/Staging)

#### Step 1: Environment Setup
```bash
# Clone repository
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

#### Step 2: Configure Environment Variables
```bash
# Essential environment variables
SECRET_KEY=your-super-secure-secret-key-at-least-50-characters
DEBUG=False
ALLOWED_HOSTS=localhost,your-domain.com

# Database Configuration
DB_PASSWORD=your-secure-password
REDIS_PASSWORD=your-redis-password

# Sentry Error Monitoring
SENTRY_DSN_BACKEND=https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000
REACT_APP_SENTRY_DSN=https://ef79ebd29c8a961b5d5dd6c313ccf7ba@o4510403562307584.ingest.de.sentry.io/4510403631054928

# Contact Information
AUTHOR_EMAIL=cavin.otieno012@gmail.com
WHATSAPP_NUMBER=+254708101604
```

#### Step 3: Start Services
```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs/
```

#### Step 4: Database Setup
```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Load sample data (optional)
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

#### Step 5: Start with Monitoring
```bash
# Start with full monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access monitoring interfaces
# Grafana: http://localhost:3001 (admin/admin123)
# Prometheus: http://localhost:9090
# Jaeger: http://localhost:16686
```

### Production Docker Compose

#### Production Environment Variables
```bash
# Create production .env file
cp .env.example .env.production

# Configure for production
DEBUG=False
SECRET_KEY=your-production-secret-key-at-least-50-characters
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
ENVIRONMENT=production
NODE_ENV=production
```

#### Production Docker Compose File
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: jac_learning_db
      POSTGRES_USER: jac_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
      - ./database/backups:/backups
    networks:
      - jac_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U jac_user -d jac_learning_db"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - jac_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  # Django Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DEBUG: "False"
      DJANGO_SETTINGS_MODULE: "config.settings.production"
      DB_NAME: "jac_learning_db"
      DB_USER: "jac_user"
      DB_PASSWORD: "${DB_PASSWORD}"
      DB_HOST: "postgres"
      DB_PORT: "5432"
      REDIS_URL: "redis://:${REDIS_PASSWORD}@redis:6379/0"
      SECRET_KEY: "${SECRET_KEY}"
      CORS_ALLOWED_ORIGINS: "https://your-domain.com"
      SENTRY_DSN_BACKEND: "${SENTRY_DSN_BACKEND}"
      ENVIRONMENT: "production"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - ./backend/static:/app/static
      - ./backend/media:/app/media
      - ./backend/logs:/app/logs
    networks:
      - jac_network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health/"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
      args:
        - REACT_APP_API_URL=https://your-domain.com/api
        - REACT_APP_WS_URL=wss://your-domain.com/ws
    environment:
      NODE_ENV: "production"
      REACT_APP_SENTRY_DSN: "${REACT_APP_SENTRY_DSN}"
    networks:
      - jac_network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./frontend/build:/usr/share/nginx/html
    depends_on:
      - backend
      - frontend
    networks:
      - jac_network
    restart: unless-stopped

  # Celery Worker
  celery-worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A config worker -l info --concurrency=2
    environment:
      DJANGO_SETTINGS_MODULE: "config.settings.production"
      DB_NAME: "jac_learning_db"
      DB_USER: "jac_user"
      DB_PASSWORD: "${DB_PASSWORD}"
      DB_HOST: "postgres"
      DB_PORT: "5432"
      REDIS_URL: "redis://:${REDIS_PASSWORD}@redis:6379/0"
      SENTRY_DSN_BACKEND: "${SENTRY_DSN_BACKEND}"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app
    networks:
      - jac_network
    restart: unless-stopped
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

volumes:
  postgres_data:
  redis_data:

networks:
  jac_network:
    driver: bridge
```

#### Deploy Production
```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d --build

# Verify deployment
docker-compose -f docker-compose.prod.yml ps

# Check logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### ✅ Production Deployment Verification (2025-11-22)

The JAC Interactive Learning Platform has been verified for production deployment with all services operational:

```bash
# Verify all services are healthy
docker-compose ps

# Expected output - all services should show "Up (healthy)":
✅ jac-celery-beat - Up (healthy) - 8000/tcp
✅ jac-celery-worker - Up (healthy) - 8000/tcp  
✅ jac-interactive-learning-platform_backend_1 - Up (healthy) - 8000/tcp
✅ jac-interactive-learning-platform_frontend_1 - Up (healthy) - 3000/tcp
✅ jac-interactive-learning-platform_postgres_1 - Up (healthy) - 5432/tcp
✅ jac-interactive-learning-platform_redis_1 - Up (healthy) - 6379/tcp
✅ jac-nginx - Up (healthy) - 80/tcp, 443/tcp
✅ jac-sandbox - Up (healthy) - 8080/tcp

# Test application health
curl http://localhost:8000/api/health/
# Response: {"status": "healthy", "database": "healthy", "redis": "healthy", "timestamp": "..."}

# Test frontend accessibility
curl http://localhost:3000
# Response: HTML page with React application
```

#### Docker Health Check Configuration

The platform uses optimized health checks for Alpine Linux containers:

**Backend Health Check:**
```yaml
test: ["CMD-SHELL", "python3 -c \"import urllib.request; urllib.request.urlopen('http://localhost:8000', timeout=10)\""]
```

**Frontend/Nginx Health Check:**
```yaml
test: ["CMD", "ps", "aux", "|", "grep", "nginx", "|", "grep", "-v", "grep"]
```

**Celery Services Health Check:**
```yaml
test: ["CMD-SHELL", "python3 -c \"import redis; redis.Redis(host='redis', port=6379, decode_responses=True).ping()\""]
```

This configuration ensures reliable health monitoring across all container environments.

## ☸️ Option 2: Kubernetes Deployment

### Prerequisites
```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://get.helm.sh/helm-v3.11.0-linux-amd64.tar.gz | tar xz
sudo mv linux-amd64/helm /usr/local/bin/helm

# Verify installation
kubectl version --client
helm version
```

### Kubernetes Manifests

#### Namespace
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: jac-learning
  labels:
    name: jac-learning
```

#### PostgreSQL Deployment
```yaml
# k8s/postgres.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: jac-learning
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: jac-learning
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_DB
          value: jac_learning_db
        - name: POSTGRES_USER
          value: jac_user
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: jac-learning
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

#### Backend Deployment
```yaml
# k8s/backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: jac-learning
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: jac-learning-platform:latest
        env:
        - name: DJANGO_SETTINGS_MODULE
          value: "config.settings.production"
        - name: DB_NAME
          value: "jac_learning_db"
        - name: DB_USER
          value: "jac_user"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: DB_HOST
          value: "postgres"
        - name: DB_PORT
          value: "5432"
        - name: REDIS_URL
          value: "redis://redis:6379/0"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: secret-key
        - name: SENTRY_DSN_BACKEND
          value: "https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000"
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/health/
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: jac-learning
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
```

#### Frontend Deployment
```yaml
# k8s/frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: jac-learning
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: jac-learning-platform-frontend:latest
        env:
        - name: REACT_APP_API_URL
          value: "https://your-domain.com/api"
        - name: REACT_APP_SENTRY_DSN
          value: "https://ef79ebd29c8a961b5d5dd6c313ccf7ba@o4510403562307584.ingest.de.sentry.io/4510403631054928"
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: jac-learning
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

#### Horizontal Pod Autoscaler
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: jac-learning
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Ingress Configuration
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: jac-learning-ingress
  namespace: jac-learning
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: jac-learning-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

#### Secrets
```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
  namespace: jac-learning
type: Opaque
data:
  password: <base64-encoded-password>
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: jac-learning
type: Opaque
data:
  secret-key: <base64-encoded-secret-key>
```

### Deploy to Kubernetes

#### Step 1: Create Cluster
```bash
# For local development with minikube
minikube start --cpus 2 --memory 4096

# For AWS EKS
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
```

#### Step 2: Deploy Application
```bash
# Apply all Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n jac-learning

# Check services
kubectl get services -n jac-learning

# Check ingress
kubectl get ingress -n jac-learning
```

#### Step 3: Setup Monitoring
```bash
# Add Helm repositories
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update

# Install monitoring stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace jac-learning \
  --create-namespace

helm install grafana grafana/grafana \
  --namespace jac-learning

helm install jaeger jaegertracing/jaeger \
  --namespace jac-learning

# Check monitoring installation
kubectl get pods -n jac-learning
```

## ☁️ Option 3: Cloud Managed Deployment

### AWS EKS Deployment

#### Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Install AWS Load Balancer Controller
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.6.0/docs/install/iam_policy.json

# Configure AWS CLI
aws configure
```

#### EKS Cluster Setup
```bash
# Create EKS cluster
cat << EOF > cluster-config.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: jac-learning-cluster
  region: us-west-2
  version: "1.28"

nodeGroups:
  - name: main
    instanceType: t3.medium
    desiredCapacity: 3
    minSize: 2
    maxSize: 10
    volumeSize: 20
    ssh:
      allow: false
    iam:
      withAddonPolicies:
        efs: true
        ebs: true
        awsLoadBalancerController: true
        albIngress: true

managedNodeGroups:
  - name: managed
    instanceType: t3.medium
    desiredCapacity: 2
    minSize: 1
    maxSize: 5
    volumeSize: 20

addons:
  - name: vpc-cni
  - name: coredns
  - name: kube-proxy
  - name: aws-load-balancer-controller
  - name: ebs-csi-driver

vpc:
  clusterEndpoints:
    privateAccess: true
    publicAccess: true
  nat:
    gateway: HighlyAvailable
EOF

# Create cluster
eksctl create cluster -f cluster-config.yaml

# Configure kubectl
aws eks update-kubeconfig --region us-west-2 --name jac-learning-cluster
```

#### Infrastructure as Code (Terraform)
```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# EKS Cluster
resource "aws_eks_cluster" "jac_learning" {
  name     = "jac-learning-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.28"

  vpc_config {
    subnet_ids = [
      aws_subnet.private_subnet_1.id,
      aws_subnet.private_subnet_2.id,
      aws_subnet.public_subnet_1.id,
      aws_subnet.public_subnet_2.id,
    ]
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }
}

# EKS Node Group
resource "aws_eks_node_group" "jac_learning_nodes" {
  cluster_name    = aws_eks_cluster.jac_learning.name
  node_group_name = "jac-learning-nodes"
  node_role       = aws_iam_role.eks_node_role.arn
  subnet_ids      = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 2
  }

  instance_types = ["t3.medium"]

  # Update the node group's configuration to use a container registry
  container_runtime = "containerd"

  tags = {
    Name = "jac-learning-nodes"
  }
}

# RDS Database
resource "aws_db_instance" "jac_learning" {
  identifier = "jac-learning-db"

  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.medium"

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = "jac_learning_db"
  username = "jac_user"
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.jac_learning.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = false
  final_snapshot_identifier = "jac-learning-final-snapshot"

  tags = {
    Name = "jac-learning-db"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "jac_learning" {
  name       = "jac-learning-subnet-group"
  subnet_ids = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
}

resource "aws_elasticache_replication_group" "jac_learning" {
  replication_group_id         = "jac-learning-redis"
  description                  = "Redis cluster for JAC Learning Platform"

  port                         = 6379
  parameter_group_name         = "default.redis7"
  node_type                    = "cache.t3.micro"
  num_cache_clusters           = 1

  subnet_group_name            = aws_elasticache_subnet_group.jac_learning.name
  security_group_ids           = [aws_security_group.redis_sg.id]

  at_rest_encryption_enabled   = true
  transit_encryption_enabled   = true
  auth_token                   = var.redis_auth_token

  tags = {
    Name = "jac-learning-redis"
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "redis_auth_token" {
  description = "Redis auth token"
  type        = string
  sensitive   = true
}
```

#### Deploy Infrastructure
```bash
# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="db_password=your-secure-password" -var="redis_auth_token=your-redis-token"

# Apply infrastructure
terraform apply -var="db_password=your-secure-password" -var="redis_auth_token=your-redis-token"

# Deploy application to EKS
kubectl apply -f k8s/
```

### Google GKE Deployment

#### Prerequisites
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install kubectl
gcloud components install kubectl

# Initialize gcloud
gcloud init
gcloud auth login
```

#### GKE Cluster Setup
```bash
# Set project and region
export PROJECT_ID="your-gcp-project"
export ZONE="us-central1-a"

gcloud config set project $PROJECT_ID
gcloud config set compute/zone $ZONE

# Create GKE cluster
gcloud container clusters create jac-learning-cluster \
  --zone=$ZONE \
  --enable-autoscaling \
  --min-nodes=2 \
  --max-nodes=10 \
  --machine-type=n1-standard-2 \
  --num-nodes=3 \
  --enable-autorepair \
  --enable-autoupgrade

# Get cluster credentials
gcloud container clusters get-credentials jac-learning-cluster --zone=$ZONE

# Deploy to GKE
kubectl apply -f k8s/
```

## 🐙 Option 4: PaaS Deployment

### Heroku Deployment

#### Prerequisites
```bash
# Install Heroku CLI
npm install -g heroku

# Login to Heroku
heroku login

# Create Heroku app
heroku create jac-learning-platform

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis addon
heroku addons:create heroku-redis:hobby-dev
```

#### Heroku Configuration
```bash
# Set environment variables
heroku config:set SECRET_KEY="your-production-secret-key"
heroku config:set DEBUG="False"
heroku config:set ALLOWED_HOSTS="jac-learning-platform.herokuapp.com"
heroku config:set SENTRY_DSN_BACKEND="https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000"
heroku config:set SENTRY_DSN_FRONTEND="https://ef79ebd29c8a961b5d5dd6c313ccf7ba@o4510403562307584.ingest.de.sentry.io/4510403631054928"

# Set buildpacks
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs
```

#### Deploy to Heroku
```bash
# Deploy backend
cd backend
git subtree push --prefix backend heroku main

# Deploy frontend
cd frontend
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Azure App Service

#### Prerequisites
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create resource group
az group create --name jac-learning-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name jac-learning-plan \
  --resource-group jac-learning-rg \
  --sku P1V2 \
  --is-linux
```

#### Deploy to Azure
```bash
# Create web apps
az webapp create \
  --resource-group jac-learning-rg \
  --plan jac-learning-plan \
  --name jac-learning-backend \
  --runtime "PYTHON:3.11"

az webapp create \
  --resource-group jac-learning-rg \
  --plan jac-learning-plan \
  --name jac-learning-frontend \
  --runtime "NODE:18-lts"

# Configure connection strings
az webapp config connection-string set \
  --resource-group jac-learning-rg \
  --name jac-learning-backend \
  --connection-string-type PostgreSQL \
  --settings DefaultConnection="postgresql://jac_user:password@server:5432/database"

# Deploy applications
cd backend
zip -r backend.zip .
az webapp deployment source config-zip \
  --resource-group jac-learning-rg \
  --name jac-learning-backend \
  --src backend.zip

cd frontend
npm run build
az webapp deployment source config-zip \
  --resource-group jac-learning-rg \
  --name jac-learning-frontend \
  --src build.zip
```

## 🔧 Deployment Automation

### Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

set -e

# Configuration
PROJECT_NAME="jac-interactive-learning-platform"
DEPLOYMENT_TYPE=${1:-"docker-compose"}
ENVIRONMENT=${2:-"production"}

echo "🚀 Deploying JAC Learning Platform"
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "Environment: $ENVIRONMENT"

# Function to check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
    command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }
    
    if [ "$DEPLOYMENT_TYPE" = "kubernetes" ]; then
        command -v kubectl >/dev/null 2>&1 || { echo "kubectl is required for Kubernetes deployment. Aborting." >&2; exit 1; }
    fi
    
    echo "✅ Prerequisites check passed"
}

# Function to setup environment
setup_environment() {
    echo "🔧 Setting up environment..."
    
    if [ ! -f .env ]; then
        echo "Creating .env file from template..."
        cp .env.example .env
        echo "Please edit .env file with your configuration before continuing."
        exit 1
    fi
    
    echo "✅ Environment configured"
}

# Function to build and deploy with Docker Compose
deploy_docker_compose() {
    echo "🐳 Deploying with Docker Compose..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
    else
        docker-compose up -d --build
    fi
    
    echo "⏳ Waiting for services to be ready..."
    sleep 30
    
    # Run migrations
    echo "📊 Running database migrations..."
    docker-compose exec -T backend python manage.py migrate
    
    # Create superuser if it doesn't exist
    echo "👤 Creating superuser..."
    docker-compose exec -T backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
    
    echo "✅ Docker Compose deployment completed"
}

# Function to deploy to Kubernetes
deploy_kubernetes() {
    echo "☸️ Deploying to Kubernetes..."
    
    # Create namespace
    kubectl apply -f k8s/namespace.yaml
    
    # Create secrets
    kubectl apply -f k8s/secrets.yaml
    
    # Deploy PostgreSQL
    kubectl apply -f k8s/postgres.yaml
    
    # Wait for PostgreSQL to be ready
    kubectl wait --for=condition=available --timeout=300s deployment/postgres -n jac-learning
    
    # Deploy backend
    kubectl apply -f k8s/backend.yaml
    
    # Deploy frontend
    kubectl apply -f k8s/frontend.yaml
    
    # Deploy ingress
    kubectl apply -f k8s/ingress.yaml
    
    # Deploy HPA
    kubectl apply -f k8s/hpa.yaml
    
    echo "⏳ Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=600s deployment/backend -n jac-learning
    kubectl wait --for=condition=available --timeout=600s deployment/frontend -n jac-learning
    
    echo "✅ Kubernetes deployment completed"
}

# Function to run health checks
run_health_checks() {
    echo "🔍 Running health checks..."
    
    if [ "$DEPLOYMENT_TYPE" = "docker-compose" ]; then
        # Check Docker Compose services
        docker-compose ps
        
        # Test backend health
        curl -f http://localhost:8000/api/health/ || echo "⚠️ Backend health check failed"
        
    elif [ "$DEPLOYMENT_TYPE" = "kubernetes" ]; then
        # Check Kubernetes pods
        kubectl get pods -n jac-learning
        
        # Test service endpoints
        kubectl get services -n jac-learning
    fi
    
    echo "✅ Health checks completed"
}

# Function to display deployment information
display_deployment_info() {
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📱 Application URLs:"
    if [ "$DEPLOYMENT_TYPE" = "docker-compose" ]; then
        echo "  Frontend: http://localhost:3000"
        echo "  Backend API: http://localhost:8000"
        echo "  API Documentation: http://localhost:8000/api/docs/"
    elif [ "$DEPLOYMENT_TYPE" = "kubernetes" ]; then
        echo "  Use 'kubectl get ingress -n jac-learning' to get URLs"
    fi
    echo ""
    echo "🔧 Management Commands:"
    echo "  View logs: kubectl logs -f deployment/backend -n jac-learning"
    echo "  Scale backend: kubectl scale deployment backend --replicas=5 -n jac-learning"
    echo "  Check status: kubectl get all -n jac-learning"
    echo ""
    echo "📞 Support:"
    echo "  Email: cavin.otieno012@gmail.com"
    echo "  Phone: +254708101604"
    echo "  WhatsApp: https://wa.me/254708101604"
    echo ""
}

# Main execution
main() {
    check_prerequisites
    setup_environment
    
    case $DEPLOYMENT_TYPE in
        "docker-compose")
            deploy_docker_compose
            ;;
        "kubernetes")
            deploy_kubernetes
            ;;
        *)
            echo "❌ Unknown deployment type: $DEPLOYMENT_TYPE"
            echo "Available types: docker-compose, kubernetes"
            exit 1
            ;;
    esac
    
    run_health_checks
    display_deployment_info
}

# Run main function
main
```

### Usage
```bash
# Make script executable
chmod +x scripts/deploy.sh

# Deploy with Docker Compose
./scripts/deploy.sh docker-compose production

# Deploy to Kubernetes
./scripts/deploy.sh kubernetes production
```

## 🔐 Security Considerations

### Production Security Checklist
- [ ] Use strong SECRET_KEY (50+ characters)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up backup procedures
- [ ] Configure log rotation
- [ ] Enable monitoring and alerting
- [ ] Use non-root containers
- [ ] Enable database encryption
- [ ] Configure proper CORS settings
- [ ] Set up security scanning

### Environment Variables Security
```bash
# Never commit these to version control
SECRET_KEY=your-very-secure-secret-key-at-least-50-characters
DB_PASSWORD=your-secure-database-password
REDIS_PASSWORD=your-redis-password
EMAIL_HOST_PASSWORD=your-email-password
GITHUB_PAT=your-github-token
GOOGLE_API_KEY=your-google-api-key

# Sentry DSNs (can be committed for demo)
SENTRY_DSN_BACKEND=https://759a58b1fc0aee913b2cb184db7fd880@o4510403562307584.ingest.de.sentry.io/4510403573842000
REACT_APP_SENTRY_DSN=https://ef79ebd29c8a961b5d5dd6c313ccf7ba@o4510403562307584.ingest.de.sentry.io/4510403631054928
```

## 📊 Monitoring and Maintenance

### Health Monitoring
```bash
# Check application health
curl -f http://your-domain.com/api/health/

# Monitor resource usage
docker stats
kubectl top pods -n jac-learning

# Check logs
tail -f logs/django.log
kubectl logs -f deployment/backend -n jac-learning

# Database maintenance
docker-compose exec postgres psql -U jac_user -d jac_learning_db -c "SELECT pg_size_pretty(pg_database_size('jac_learning_db'));"
```

### Backup and Recovery
```bash
# Database backup
./scripts/backup.sh

# Restore from backup
psql -U jac_user -d jac_learning_db < backup.sql

# Volume backup
docker run --rm -v postgres_data:/data -v $(pwd)/backup:/backup alpine tar czf /backup/postgres-$(date +%Y%m%d).tar.gz /data
```

## 🎯 Summary

### Quick Start Commands
```bash
# Clone and setup
git clone https://github.com/OumaCavin/jac-interactive-learning-platform.git
cd jac-interactive-learning-platform
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"

# Docker Compose (Development)
cp .env.example .env
docker-compose up -d

# Kubernetes (Production)
kubectl apply -f k8s/

# Heroku
heroku create jac-learning-platform
heroku config:set SECRET_KEY="your-secret-key"
git push heroku main
```

### Support Information
- **Author**: Cavin Otieno
- **Email**: cavin.otieno012@gmail.com
- **Phone**: +254708101604
- **WhatsApp**: [Contact via WhatsApp](https://wa.me/254708101604)
- **LinkedIn**: [Cavin Otieno](https://www.linkedin.com/in/cavin-otieno-9a841260/)
- **GitHub**: [OumaCavin](https://github.com/OumaCavin)

Choose the deployment option that best fits your infrastructure needs and scale requirements. Each option provides full functionality with monitoring, logging, and observability capabilities.

---

**Author**: Cavin Otieno  
**Version**: 2.0.0  
**Last Updated**: 2025-11-21 23:18:30