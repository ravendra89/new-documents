variable "project" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "name_suffix" {
  description = "Suffix for resource names, e.g. app, web, bastion"
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

variable "eni_id" {
  description = "ENI ID to attach as the primary network interface (device_index = 0)"
  type        = string
}

variable "root_volume_size" {
  description = "Root EBS volume size in GB"
  type        = number
}

variable "extra_ebs_volumes" {
  description = "Additional EBS volumes to attach"
  type = list(object({
    device_name           = string
    volume_type           = optional(string, "gp3")
    volume_size           = optional(number, 20)
    encrypted             = optional(bool, true)
    delete_on_termination = optional(bool, true)
  }))
}

variable "user_data" {
  description = "Shell script to run on first boot (plain string, not base64)"
  type        = string
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed (1-minute) CloudWatch monitoring"
  type        = bool
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
}