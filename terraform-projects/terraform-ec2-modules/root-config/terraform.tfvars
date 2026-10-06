# ── General ───────────────────────────────────────────────────────────────────
aws_region  = "us-east-1"
project     = "my-project"
environment = "test"
name_prefix = "test"

tags = {
  Owner     = "devops-team"
  ManagedBy = "Terraform"
}

# ── VPC ───────────────────────────────────────────────────────────────────────
vpc_cidr             = "10.0.0.0/16"
availability_zones   = ["us-east-1a", "us-east-1b"]

public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24"
]

private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24"
]

enable_nat_gateway = true

# ── Security Group ────────────────────────────────────────────────────────────
ssh_port   = 22
http_port  = 80
https_port = 443
app_port   = 8080

ssh_allowed_cidr = "203.0.113.10/32"

# ── Network Interface ─────────────────────────────────────────────────────────
create_eip = false

# ── EC2 ───────────────────────────────────────────────────────────────────────
name_suffix      = "app"
ami_id           = ""
instance_type    = "t3.micro"
key_name         = "my-keypair"
root_volume_size = 20

# ── Extra EBS Volumes ─────────────────────────────────────────────────────────
extra_ebs_volumes = [
  {
    device_name           = "/dev/sdb"
    volume_type           = "gp3"
    volume_size           = 50
    encrypted             = true
    delete_on_termination = true
  }
]