variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "The VPC ID for the ALB and target group"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for ALB"
  type        = list(string)
}

variable "application_name" {
  description = "Application name used for conditional logic"
  type        = string
}

variable "health_check_path" {
  description = "Path for the ALB health check"
  type        = string
}
