terraform {
  required_version = ">= 1.0.9" #TODO
  
  backend "s3" {
    bucket = "bucket name"
    #key    = "workloads/stg/dynamodb-cleanup/aws-batch.tfstate"
    #key    = "workloads/qa/dynamodb-cleanup/aws-batch.tfstate"
    key    = "workloads/dynamodb-cleanup/aws-batch.tfstate"
    region = "us-east-1"
    acl    = "bucket-owner-full-control"
  }
}

# PROD ENVIRONMENT
# terraform init -reconfigure -backend-config="key=workloads/dynamodb-cleanup/aws-batch.tfstate"
# terraform plan -var-file="prod.tfvars"
# terraform apply -var-file="prod.tfvars"
