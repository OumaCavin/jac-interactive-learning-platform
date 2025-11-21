# Monitoring & Observability Setup Guide

This document outlines the comprehensive monitoring and observability infrastructure for the JAC Interactive Learning Platform.

## 🏗️ Monitoring Architecture

### Components Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    MONITORING STACK                          │
├─────────────────────────────────────────────────────────────┤
│  Prometheus  │  Grafana     │  Jaeger    │  Loki           │
│  (Metrics)   │  (Dashboards)│  (Tracing) │  (Logs)         │
├─────────────────────────────────────────────────────────────┤
│              JAC LEARNING PLATFORM SERVICES                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Frontend   │ │   Backend   │ │   Celery    │           │
│  │   (React)   │ │   (Django)  │ │   Workers   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ PostgreSQL  │ │    Redis    │ │    Nginx    │           │
│  │  Database   │ │    Cache    │ │   Proxy     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Metrics Collection (Prometheus)

### Application Metrics
- **Request Metrics**: Request rate, response time, error rate
- **Business Metrics**: Learning progress, agent performance, code execution stats
- **Resource Metrics**: CPU, memory, disk usage per service
- **Custom Metrics**: User engagement, learning path completion rates

### Prometheus Configuration
```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'jac-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    
  - job_name: 'jac-frontend'
    static_configs:
      - targets: ['frontend:3000']
    metrics_path: '/metrics'
    
  - job_name: 'jac-celery'
    static_configs:
      - targets: ['celery-worker:8000']
    metrics_path: '/metrics'
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
      
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

### Custom Metrics Implementation

#### Backend Metrics (Django)
```python
# backend/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Business metrics
LEARNING_PATH_COMPLETIONS = Counter('learning_path_completions_total', 'Total learning path completions')
CODE_EXECUTIONS = Counter('code_executions_total', 'Total code executions', ['language', 'status'])
AGENT_TASKS = Counter('agent_tasks_total', 'Total agent tasks', ['agent_type', 'status'])

# Resource metrics
CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('system_memory_usage_bytes', 'Memory usage in bytes')

def track_request(func):
    def wrapper(request, *args, **kwargs):
        start_time = time.time()
        method = request.method
        endpoint = request.path
        
        try:
            response = func(request, *args, **kwargs)
            status = 'success'
        except Exception as e:
            status = 'error'
            raise
        finally:
            duration = time.time() - start_time
            REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
            REQUEST_LATENCY.observe(duration)
            
        return response
    return wrapper
```

#### Frontend Metrics (React)
```typescript
// frontend/src/utils/metrics.ts
import { init as initPrometheus } from '@cvin/prom-client';

const client = initPrometheus();

// Custom metrics
export const pageViewCounter = new client.Counter({
  name: 'frontend_page_views_total',
  help: 'Total page views',
  labelNames: ['page', 'user_type'] as const,
});

export const apiRequestLatency = new client.Histogram({
  name: 'frontend_api_request_duration_seconds',
  help: 'API request latency',
  labelNames: ['endpoint', 'method'] as const,
  buckets: [0.1, 0.5, 1, 2, 5, 10],
});

export function trackPageView(page: string, userType: string = 'anonymous') {
  pageViewCounter.inc({ page, user_type: userType });
}

export function trackApiRequest(endpoint: string, method: string, duration: number) {
  apiRequestLatency.observe({ endpoint, method }, duration / 1000);
}
```

## 📈 Dashboards (Grafana)

### Dashboard Categories

#### 1. **System Overview Dashboard**
- Real-time system health
- Service status overview
- Critical alerts summary
- Resource utilization trends

#### 2. **Application Performance Dashboard**
- Request rate and latency
- Error rates and types
- Database performance
- Cache hit rates

#### 3. **Business Intelligence Dashboard**
- Learning progress metrics
- User engagement statistics
- Agent performance analysis
- Code execution success rates

#### 4. **Infrastructure Dashboard**
- Container resource usage
- Network performance
- Database connections
- Storage utilization

### Grafana Dashboard Configuration
```json
{
  "dashboard": {
    "title": "JAC Learning Platform - System Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph", 
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

## 🔍 Distributed Tracing (Jaeger)

### Tracing Architecture
- **Request Tracing**: Trace user requests through all services
- **Agent Coordination**: Track multi-agent communication
- **Database Queries**: Monitor database performance
- **Code Execution**: Trace code execution pipeline

### Jaeger Configuration
```yaml
# monitoring/jaeger/jaeger-config.yml
version: '3.8'

services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # Jaeger UI
      - "14268:14268"  # HTTP collector
      - "14250:14250"  # gRPC collector
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
    volumes:
      - jaeger_data:/tmp
    networks:
      - monitoring

volumes:
  jaeger_data:

networks:
  monitoring:
    driver: bridge
```

### Tracing Implementation

#### Backend Tracing (Django)
```python
# backend/monitoring/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracing
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "jac-backend"}))
)

tracer = trace.get_tracer(__name__)

# Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

def trace_request(func):
    def wrapper(request, *args, **kwargs):
        with tracer.start_as_current_span(f"{func.__name__}_request") as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", request.path)
            
            try:
                result = func(request, *args, **kwargs)
                span.set_attribute("http.status_code", 200)
                return result
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.message", str(e))
                raise
    return wrapper
```

#### Frontend Tracing (React)
```typescript
// frontend/src/utils/tracing.ts
import { init as initJaeger } from 'jaeger-client';

const tracer = initJaeger(
  'jac-frontend',
  {
    reporter: {
      logSpans: true,
      agentHost: 'jaeger',
      agentPort: 6832,
    },
    sampler: {
      type: 'const',
      param: 1,
    },
  },
);

export function traceComponent(name: string) {
  return function <T extends (...args: any[]) => any>(originalMethod: T, context: ClassMethodDecoratorContext): T {
    function replacementMethod(this: any, ...args: any[]) {
      const span = tracer.startSpan(name);
      try {
        const result = originalMethod.apply(this, args);
        span.setTag('success', true);
        return result;
      } catch (error) {
        span.setTag('error', true);
        span.log({ error: error.message });
        throw error;
      } finally {
        span.finish();
      }
    }
    return replacementMethod as T;
  };
}
```

## 📋 Centralized Logging (Loki + ELK)

### Logging Architecture
- **Structured Logging**: JSON-formatted logs with correlation IDs
- **Log Aggregation**: All services log to centralized system
- **Log Parsing**: Automatic parsing and indexing
- **Log Retention**: Configurable retention policies

### Loki Configuration
```yaml
# monitoring/loki/loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  path_prefix: /tmp/loki
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules
  replication_factor: 1
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory

query_scheduler:
  max_outstanding_requests_per_tenant: 2048

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  ingestion_rate_mb: 16
  ingestion_burst_size_mb: 32
```

### Structured Logging Implementation

#### Backend Logging (Django)
```python
# backend/monitoring/logging.py
import logging
import json
from pythonjsonlogger import jsonlogger
from django.utils import timezone

class StructuredJSONFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['timestamp'] = timezone.now().isoformat()
        log_record['service'] = 'jac-backend'
        log_record['correlation_id'] = getattr(record, 'correlation_id', None)
        log_record['user_id'] = getattr(record, 'user_id', None)

# Configure logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': StructuredJSONFormatter,
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'json': {
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['json'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['json'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

def get_logger(name):
    return logging.getLogger(name)
```

#### Frontend Logging (React)
```typescript
// frontend/src/utils/logging.ts
interface LogEntry {
  timestamp: string;
  service: string;
  level: 'info' | 'warn' | 'error';
  message: string;
  context?: Record<string, any>;
  correlationId?: string;
  userId?: string;
  sessionId?: string;
}

class StructuredLogger {
  private service = 'jac-frontend';
  private sessionId = this.generateSessionId();

  private generateSessionId(): string {
    return Math.random().toString(36).substring(2, 15);
  }

  private log(level: LogEntry['level'], message: string, context?: Record<string, any>) {
    const logEntry: LogEntry = {
      timestamp: new Date().toISOString(),
      service: this.service,
      level,
      message,
      context,
      sessionId: this.sessionId,
    };

    // Send to logging service
    fetch('/api/logs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logEntry),
    }).catch(console.error);

    // Console output for development
    console[level](logEntry);
  }

  info(message: string, context?: Record<string, any>) {
    this.log('info', message, context);
  }

  warn(message: string, context?: Record<string, any>) {
    this.log('warn', message, context);
  }

  error(message: string, context?: Record<string, any>) {
    this.log('error', message, context);
  }
}

export const logger = new StructuredLogger();
```

## 🚨 Alerting Rules

### Alert Categories

#### 1. **Critical Alerts**
- Service down/unreachable
- High error rates (>10%)
- Database connection failures
- Security breaches

#### 2. **Warning Alerts**
- High response times (>2s)
- High resource utilization (>80%)
- Failed deployments
- Certificate expiration

#### 3. **Info Alerts**
- Learning milestone achievements
- User registrations
- System maintenance

### Prometheus Alert Rules
```yaml
# monitoring/prometheus/rules/alerts.yml
groups:
- name: jac-learning-alerts
  rules:
  
  - alert: ServiceDown
    expr: up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Service {{ $labels.job }} is down"
      description: "Service {{ $labels.job }} has been down for more than 1 minute"
      
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }} errors per second"
      
  - alert: HighResponseTime
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High response time detected"
      description: "95th percentile response time is {{ $value }}s"
      
  - alert: HighMemoryUsage
    expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.8
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage"
      description: "Memory usage is above 80%"
```

## 🚀 Deployment

### Docker Compose Monitoring Stack
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus:/etc/prometheus
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki:/etc/loki
      - loki_data:/tmp/loki

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

### Start Monitoring Stack
```bash
# Start main application
docker-compose up -d

# Start monitoring stack
docker-compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Access monitoring interfaces
# Grafana: http://localhost:3001 (admin/admin123)
# Prometheus: http://localhost:9090
# Jaeger: http://localhost:16686
```

## 📊 Key Performance Indicators (KPIs)

### Application KPIs
- **Response Time**: < 200ms for 95th percentile
- **Error Rate**: < 1% of total requests
- **Availability**: 99.9% uptime
- **Throughput**: > 1000 requests/minute

### Business KPIs
- **Learning Path Completion**: Target > 80%
- **User Engagement**: > 5 sessions/week
- **Code Execution Success**: > 95%
- **Agent Task Success**: > 90%

### Infrastructure KPIs
- **CPU Usage**: < 70% average
- **Memory Usage**: < 80% average
- **Disk Usage**: < 85% capacity
- **Network Latency**: < 10ms internal

## 🛠️ Maintenance

### Log Rotation
```bash
# Rotate logs daily
0 2 * * * find /var/log/jac -name "*.log" -mtime +7 -delete

# Compress old logs
0 3 * * * find /var/log/jac -name "*.log.1" -exec gzip {} \;
```

### Database Maintenance
```bash
# Monitor query performance
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;

# Check table sizes
SELECT schemaname,tablename,pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public';
```

### Health Checks
```bash
# Application health
curl -f http://localhost:8000/api/health || exit 1

# Database health
docker exec postgres pg_isready -U jac_user

# Redis health
docker exec redis redis-cli ping

# Service status
docker-compose ps
```

---

**Author**: Cavin Otieno  
**Contact**: cavin.otieno012@gmail.com | +254708101604 | [LinkedIn](https://www.linkedin.com/in/cavin-otieno-9a841260/) | [WhatsApp](https://wa.me/254708101604)