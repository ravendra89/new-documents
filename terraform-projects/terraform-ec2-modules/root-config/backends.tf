terraform {
  backend "s3" {
    bucket  = "bucket-name"
    key     = "project/terraform.tfstate"
    region  = "us-west-2"
    acl     = "bucket-owner-full-control"
    profile = "default"
  }
}

# test
# terraform init -reconfigure -backend-config=bucket=bucket-name -backend-config=key=project/terraform.tfstate -backend-config=profile=default
# terraform plan -var-file=beta3.tfvars
# terraform apply -var-file=terraform.tfvars