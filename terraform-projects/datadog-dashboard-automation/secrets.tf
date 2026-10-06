data "azurerm_key_vault" "datadog_secrets" {
  name                = "key vault name"
  resource_group_name = "rg name"
}

data "azurerm_key_vault_secret" "datadog_api_key" {
  name         = "datadog-api-key"
  key_vault_id = data.azurerm_key_vault.datadog_secrets.id
}

data "azurerm_key_vault_secret" "datadog_app_key" {
  name         = "datadog-app-key"
  key_vault_id = data.azurerm_key_vault.datadog_secrets.id
}
