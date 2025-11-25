variable "project_name" {
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
