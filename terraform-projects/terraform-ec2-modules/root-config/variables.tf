# ── General ───────────────────────────────────────────────────────────────────

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
}

variable "project" {
  description = "Project name used in all resource names"
  type        = string
}

variable "environment" {
  description = "Environment name (dev | staging | prod)"
  type        = string
}

variable "name_prefix" {
  type        = string
  description = "The full dynamic name prefix for resources"
}

variable "tags" {
  description = "Common tags applied to all resources"
  type        = map(string)
  default     = {}
}

# ── VPC ───────────────────────────────────────────────────────────────────────

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

# ── Security Group ────────────────────────────────────────────────────────────

variable "ssh_port" {
  description = "SSH port"
  type        = number
}

variable "http_port" {
  description = "HTTP port"
  type        = number
}

variable "https_port" {
  description = "HTTPS port"
  type        = number
}

variable "app_port" {
  description = "Custom application port"
  type        = number
}

variable "ssh_allowed_cidr" {
  description = "CIDR allowed to SSH. Restrict to your IP in production."
  type        = string
}

# ── Network Interface ─────────────────────────────────────────────────────────

variable "create_eip" {
  description = "Allocate and attach an Elastic IP to the ENI"
  type        = bool
}


# ── EC2 ───────────────────────────────────────────────────────────────────────

variable "name_suffix" {
  description = "Suffix for EC2 resource names e.g. app, web, bastion"
  type        = string
}

variable "ami_id" {
  description = "AMI ID. Leave empty to auto-select latest Amazon Linux 2023."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "key_name" {
  description = "Existing EC2 Key Pair name. Null = no SSH key (use SSM)."
  type        = string
}

variable "root_volume_size" {
  description = "Root EBS volume size in GB"
  type        = number
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring"
  type        = bool
}

variable "extra_policy_arns" {
  description = "Additional IAM policy ARNs to attach to the EC2 role"
  type        = list(string)
}

variable "extra_ebs_volumes" {
  description = "Additional EBS volumes to attach to EC2"
  type = list(object({
    device_name           = string
    volume_type           = optional(string, "gp3")
    volume_size           = optional(number, 20)
    encrypted             = optional(bool, true)
    delete_on_termination = optional(bool, true)
  }))
}

variable "user_data" {
  description = "Shell script to run on first boot"
  type        = string
}