output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.this.id
}

output "instance_arn" {
  description = "EC2 instance ARN"
  value       = aws_instance.this.arn
}


output "private_ip" {
  description = "Private IP address of the instance"
  value       = aws_instance.this.private_ip
}

output "public_ip" {
  description = "Public IP address of the instance (if any)"
  value       = aws_instance.this.public_ip
}

output "ami_id" {
  description = "AMI ID the instance was launched with"
  value       = aws_instance.this.ami
}

output "availability_zone" {
  description = "Availability zone of the instance"
  value       = aws_instance.this.availability_zone
}

output "iam_role_name" {
  description = "IAM role name attached to the instance"
  value       = aws_iam_role.this.name
}

output "iam_role_arn" {
  description = "IAM role ARN"
  value       = aws_iam_role.this.arn
}

output "instance_profile_name" {
  description = "IAM instance profile name"
  value       = aws_iam_instance_profile.this.name
}