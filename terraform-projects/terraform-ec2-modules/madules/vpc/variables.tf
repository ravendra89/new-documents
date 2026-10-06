variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name (dev | staging | prod)"
  type        = string
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets — one per AZ"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets — one per AZ"
  type        = list(string)
}

variable "enable_nat_gateway" {
  description = "Create a NAT Gateway for private subnet outbound access"
  type        = bool
}
