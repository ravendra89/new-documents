variable "environment" { }

variable "region" { }

variable "subnet_id" { }

# variable "security_group_id" { }

variable "security_group_name" { }

variable "list_command" {
  type = list
}

variable "vpc_id" { }

variable "vpc_cidr" {
  
}

# Ingress and Egress Rules
variable "default_sg_rule" {
  default = {
    from_port       = null
    to_port         = null
    protocol        = null
    # cidr_block      = null
    description     = null
    # ipv6_cidr_block = null
    prefix_list_ids = null
    security_groups = null
    self            = null
    cidr_blocks     = null
    ipv6_cidr_blocks = null
  }
}