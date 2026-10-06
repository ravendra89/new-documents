variable "aws_region" {
  type = string
}

variable "environment" {
  type = string
}

variable "excluded_security_group_ids" {
  type        = string
  description = "Comma-separated security group IDs to exclude"
}

variable "sns_topic_arn" {
  type        = string
  description = "SNS Topic ARN for Lambda alerts"
}
