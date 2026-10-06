#Define variables
variable "aws_region" {
  type = string
}
variable "environment" {
  type = string
}

variable "cloudwatch_loggroup_name" {
  description = "Name of The CloudWatch LogGroup"
  type        = string
  default     = "aws-waf-logs-waf" # Need to create log group with prefix - 'aws-waf-logs'
}


