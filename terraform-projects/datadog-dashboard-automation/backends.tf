terraform {
  backend "azurerm" {
    storage_account_name = "storageaccountname"
    container_name       = "containername"
    key                  = "terraform.tfstate"
  }
}

# client name
# terraform init -reconfigure -backend-config="resource_group_name=rgname" -backend-config="storage_account_name=storageaccountname" -backend-config="container_name=datadog-tfstate" -backend-config="key=clientname/terraform.tfstate"
# terraform plan -var-file="parameters/clientname/tfvars.json"
# terraform apply -var-file="parameters/clientname/tfvars.json"


