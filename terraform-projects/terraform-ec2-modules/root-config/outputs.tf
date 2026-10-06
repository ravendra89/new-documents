################################################################################
# Root outputs.tf
################################################################################

# ── VPC ───────────────────────────────────────────────────────────────────────

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "nat_public_ip" {
  description = "NAT Gateway public IP"
  value       = module.vpc.nat_public_ip
}

# ── Security Group ────────────────────────────────────────────────────────────

output "sg_id" {
  description = "Security group ID"
  value       = module.sg.sg_id
}

output "sg_name" {
  description = "Security group name"
  value       = module.sg.sg_name
}

# ── Network Interface ─────────────────────────────────────────────────────────

output "eni_id" {
  description = "ENI ID"
  value       = module.eni.eni_id
}

output "eni_private_ip" {
  description = "ENI private IP"
  value       = module.eni.private_ip
}

output "elastic_ip" {
  description = "Elastic IP (null if create_eip = false)"
  value       = module.eni.elastic_ip
}

# ── EC2 ───────────────────────────────────────────────────────────────────────

output "instance_id" {
  description = "EC2 instance ID"
  value       = module.ec2.instance_id
}

output "instance_private_ip" {
  description = "EC2 private IP"
  value       = module.ec2.private_ip
}

output "instance_public_ip" {
  description = "EC2 public IP"
  value       = module.ec2.public_ip
}

output "iam_role_name" {
  description = "IAM role name"
  value       = module.ec2.iam_role_name
}