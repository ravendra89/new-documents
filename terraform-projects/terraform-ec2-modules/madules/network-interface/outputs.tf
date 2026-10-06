output "eni_id" {
  description = "ENI ID"
  value       = aws_network_interface.this.id
}

output "eni_arn" {
  description = "ENI ARN"
  value       = aws_network_interface.this.arn
}

output "private_ip" {
  description = "Primary private IP of the ENI"
  value       = aws_network_interface.this.private_ip
}

output "private_ips" {
  description = "All private IPs assigned to the ENI"
  value       = aws_network_interface.this.private_ip_list
}

output "mac_address" {
  description = "MAC address of the ENI"
  value       = aws_network_interface.this.mac_address
}

output "availability_zone" {
  description = "Availability zone the ENI is placed in"
  value       = aws_network_interface.this.availability_zone
}

output "elastic_ip" {
  description = "Elastic IP address (null if create_eip = false)"
  value       = var.create_eip ? aws_eip.this[0].public_ip : null
}
