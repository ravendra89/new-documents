terraform {
  backend "s3" {
    bucket = "bucketname"
    key    = "waf/terraform.tfstate"
    region = "us-east-1"
    acl    = "bucket-owner-full-control"
    # Comment/Uncomment/change to execute with aws account profile
    # profile = "default"
  }
}

# prod
# terraform init -reconfigure -backend-config=bucket=bucketname -backend-config=key=waf/terraform.tfstate -backend-config=profile=default
# terraform plan -var-file=prod.tfvars.json
# terraform apply -var-file=prod.tfvars.json