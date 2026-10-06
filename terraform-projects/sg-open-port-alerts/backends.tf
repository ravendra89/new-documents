terraform {
  backend "s3" {
    bucket = "bucket-name"
    key    = "securitygroup-open-ports-alerts/terraform.tfstate"
    region = "us-east-1"
    acl    = "bucket-owner-full-control"
    # Comment/Uncomment this to execute with aws account profile
    profile = "default"
  }
}

# terraform init -reconfigure -backend-config=bucket=bucket-name -backend-config=key=securitygroup-open-ports-alerts/terraform.tfstate -backend-config=profile=default
# terraform plan -var-file=tfvars.json
# terraform apply -var-file=tfvars.json