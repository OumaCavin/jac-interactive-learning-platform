#!/usr/bin/env python3
"""
Integration Capabilities Implementation Plan

This script implements the missing integration capabilities identified
in the analysis report.
"""

import os
import json
import subprocess

def create_vscode_configuration():
    """Create VS Code workspace configuration for IDE support"""
    
    # Create .vscode directory
    vscode_dir = "/workspace/.vscode"
    os.makedirs(vscode_dir, exist_ok=True)
    
    # Extensions configuration
    extensions_config = {
        "recommendations": [
            "ms-python.python",
            "ms-vscode.vscode-typescript-next", 
            "bradlc.vscode-tailwindcss",
            "ms-vscode.vscode-json",
            "esbenp.prettier-vscode",
            "ms-python.pylint",
            "ms-python.black-formatter",
            "ms-python.isort",
            "dbaeumer.vscode-eslint",
            "ms-vscode-remote.remote-containers"
        ]
    }
    
    with open(f"{vscode_dir}/extensions.json", "w") as f:
        json.dump(extensions_config, f, indent=2)
    
    # Debugging configuration
    debug_config = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Django",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/backend/manage.py",
                "args": ["runserver", "0.0.0.0:8000"],
                "django": True,
                "justMyCode": False,
                "console": "integratedTerminal"
            },
            {
                "name": "Python: Django Shell",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/backend/manage.py",
                "args": ["shell"],
                "django": True
            },
            {
                "name": "React: Chrome",
                "type": "node",
                "request": "launch",
                "program": "${workspaceFolder}/frontend/node_modules/.bin/react-scripts",
                "args": ["start"],
                "cwd": "${workspaceFolder}/frontend",
                "protocol": "inspector",
                "console": "integratedTerminal"
            }
        ]
    }
    
    with open(f"{vscode_dir}/launch.json", "w") as f:
        json.dump(debug_config, f, indent=2)
    
    # Tasks configuration
    tasks_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "Start Backend",
                "type": "shell",
                "command": "cd ${workspaceFolder}/backend && python manage.py runserver",
                "group": "build",
                "presentation": {"echo": True, "reveal": "always"}
            },
            {
                "label": "Start Frontend", 
                "type": "shell",
                "command": "cd ${workspaceFolder}/frontend && npm start",
                "group": "build",
                "presentation": {"echo": True, "reveal": "always"}
            },
            {
                "label": "Run Migrations",
                "type": "shell",
                "command": "cd ${workspaceFolder}/backend && python manage.py migrate",
                "group": "build",
                "presentation": {"echo": True, "reveal": "always"}
            },
            {
                "label": "Create Superuser",
                "type": "shell",
                "command": "cd ${workspaceFolder}/backend && python manage.py createsuperuser",
                "group": "build"
            }
        ]
    }
    
    with open(f"{vscode_dir}/tasks.json", "w") as f:
        json.dump(tasks_config, f, indent=2)
    
    # Settings configuration
    settings_config = {
        "python.defaultInterpreterPath": "./backend/.venv/bin/python",
        "python.terminal.activateEnvironment": True,
        "python.linting.enabled": True,
        "python.linting.pylintEnabled": True,
        "python.formatting.provider": "black",
        "python.sortImports.args": ["--profile", "black"],
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": True
        },
        "typescript.preferences.importModuleSpecifier": "relative",
        "eslint.workingDirectories": ["frontend/src"]
    }
    
    with open(f"{vscode_dir}/settings.json", "w") as f:
        json.dump(settings_config, f, indent=2)
    
    print("✅ VS Code workspace configuration created")

def create_github_actions():
    """Create GitHub Actions workflow for CI/CD"""
    
    # Create .github directory
    github_dir = "/workspace/.github"
    workflows_dir = f"{github_dir}/workflows"
    os.makedirs(workflows_dir, exist_ok=True)
    
    # Main CI/CD workflow
    ci_workflow = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_USER: postgres
          POSTGRES_DB: jac_learning_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run backend tests
      run: |
        cd backend
        python manage.py test
    
    - name: Run migrations
      run: |
        cd backend
        python manage.py migrate
    
    - name: Check code style
      run: |
        cd backend
        python -m flake8 apps/
        python -m black --check apps/
        python -m isort --check-only apps/

  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm test -- --coverage
    
    - name: Build frontend
      run: |
        cd frontend
        npm run build
    
    - name: Check code style
      run: |
        cd frontend
        npx eslint src/ --ext .js,.jsx,.ts,.tsx
        npx prettier --check src/

  deploy:
    needs: [test-backend, test-frontend]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Add deployment commands here
"""
    
    with open(f"{workflows_dir}/ci-cd.yml", "w") as f:
        f.write(ci_workflow)
    
    print("✅ GitHub Actions CI/CD workflow created")

def create_pre_commit_config():
    """Create pre-commit configuration for code quality"""
    
    pre_commit_config = """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: check-merge-conflict
    -   id: debug-statements

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
        language_version: python3

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        args: [--max-line-length=88]

-   repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.42.0
    hooks:
    -   id: eslint
        files: \.(js|jsx|ts|tsx)$
        types: [file]
        additional_dependencies:
        -   eslint@8.42.0
        -   eslint-plugin-react@7.32.2
        -   eslint-plugin-react-hooks@4.6.0
"""
    
    with open("/workspace/.pre-commit-config.yaml", "w") as f:
        f.write(pre_commit_config)
    
    print("✅ Pre-commit configuration created")

def create_terraform_config():
    """Create basic Terraform configuration for cloud deployment"""
    
    # Create terraform directory
    terraform_dir = "/workspace/terraform"
    os.makedirs(terraform_dir, exist_ok=True)
    
    # AWS main configuration
    aws_main = """terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
}

# VPC Configuration
resource "aws_vpc" "jac_learning_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Subnets
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.jac_learning_vpc.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zones[0]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.jac_learning_vpc.id
  cidr_block        = var.private_subnet_cidr
  availability_zone = var.availability_zones[0]
  
  tags = {
    Name = "${var.project_name}-private-subnet"
  }
}

# RDS Database
resource "aws_db_subnet_group" "jac_db_subnet_group" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = [aws_subnet.public_subnet.id, aws_subnet.private_subnet.id]
  
  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for RDS"
  vpc_id      = aws_vpc.jac_learning_vpc.id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "jac_learning_db" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.jac_db_subnet_group.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot"
  
  tags = {
    Name = "${var.project_name}-database"
  }
}
"""
    
    with open(f"{terraform_dir}/main.tf", "w") as f:
        f.write(aws_main)
    
    # Variables configuration
    terraform_vars = """variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "jac-learning-platform"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for public subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "CIDR block for private subnet"
  type        = string
  default     = "10.0.2.0/24"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a"]
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "jac_learning_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "jac_user"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
"""
    
    with open(f"{terraform_dir}/variables.tf", "w") as f:
        f.write(terraform_vars)
    
    # Outputs configuration
    terraform_outputs = """output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.jac_learning_db.endpoint
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.jac_learning_vpc.id
}

output "public_subnet_id" {
  description = "Public subnet ID"
  value       = aws_subnet.public_subnet.id
}
"""
    
    with open(f"{terraform_dir}/outputs.tf", "w") as f:
        f.write(terraform_outputs)
    
    print("✅ Terraform configuration created")

def main():
    """Main function to implement integration capabilities"""
    
    print("🚀 Implementing Integration Capabilities")
    print("=" * 50)
    
    # Create VS Code workspace configuration
    print("\n📁 Creating VS Code workspace configuration...")
    create_vscode_configuration()
    
    # Create GitHub Actions workflow
    print("\n🔧 Creating GitHub Actions CI/CD workflow...")
    create_github_actions()
    
    # Create pre-commit configuration
    print("\n🔍 Creating pre-commit configuration...")
    create_pre_commit_config()
    
    # Create Terraform configuration
    print("\n☁️  Creating Terraform cloud configuration...")
    create_terraform_config()
    
    print("\n" + "=" * 50)
    print("✅ Integration capabilities implementation complete!")
    print("\n📋 Summary of new features:")
    print("   • VS Code workspace configuration with debugging")
    print("   • GitHub Actions CI/CD pipeline")
    print("   • Pre-commit hooks for code quality")
    print("   • Terraform AWS infrastructure configuration")
    
    print("\n🎯 Next steps:")
    print("   1. Install pre-commit: pip install pre-commit")
    print("   2. Set up pre-commit: pre-commit install")
    print("   3. Install VS Code recommended extensions")
    print("   4. Configure AWS credentials for Terraform")
    print("   5. Push changes to trigger CI/CD pipeline")

if __name__ == "__main__":
    main()