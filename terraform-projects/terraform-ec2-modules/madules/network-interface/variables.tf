variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "name_suffix" {
  description = "Suffix for the ENI name, e.g. app, bastion, web"
  type        = string
}

variable "description" {
  description = "ENI description (auto-generated if empty)"
  type        = string
}

variable "subnet_id" {
  description = "Subnet ID to place the ENI in"
  type        = string
}

variable "security_group_ids" {
  description = "List of security group IDs to attach to the ENI"
  type        = list(string)
}

variable "private_ips" {
  description = "Static private IPs to assign. Leave empty for auto-assign."
  type        = list(string)
}

variable "create_eip" {
  description = "Allocate and attach an Elastic IP to this ENI"
  type        = bool
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
}