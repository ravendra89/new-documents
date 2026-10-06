terraform {
  required_providers {
    datadog = {
      source  = "DataDog/datadog"
      version = "3.75.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "subscription_id" # subscription ID is used to access Key Vault and retrieve Datadog credentials securely.
}

provider "datadog" {
  api_key = data.azurerm_key_vault_secret.datadog_api_key.value
  app_key = data.azurerm_key_vault_secret.datadog_app_key.value
}


