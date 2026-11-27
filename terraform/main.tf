resource "azurerm_resource_group" "main_rg" {
  name     = var.resource_group
  location = var.location
}
resource "azurerm_postgresql_flexible_server" "main_db" {
  name                = var.db_name
  resource_group_name = azurerm_resource_group.main_rg.name
  location            = azurerm_resource_group.main_rg.location
  zone                = "2"
}

resource "azurerm_container_registry" "main_container_registry" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.main_rg.name
  location            = azurerm_resource_group.main_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_key_vault" "main_key_vault" {
  name                = var.key_vault_name
  resource_group_name = azurerm_resource_group.main_rg.name
  location            = azurerm_resource_group.main_rg.location
  sku_name            = "standard"
  tenant_id           = var.tenant_id

}
resource "azurerm_cognitive_account" "main_foundry" {
  name                       = var.foundry_name
  resource_group_name        = azurerm_resource_group.main_rg.name
  location                   = azurerm_resource_group.main_rg.location
  kind                       = "AIServices"
  sku_name                   = "S0"
  project_management_enabled = true
  identity {
    type = "SystemAssigned"
  }
  custom_subdomain_name = "rag-chatbot-foundry-2026"


  network_acls {
    default_action = "Allow"
    ip_rules       = []
  }

}
resource "azurerm_cognitive_account_project" "main_foundry_project" {
  name                 = var.foundry_name
  location             = azurerm_resource_group.main_rg.location
  cognitive_account_id = azurerm_cognitive_account.main_foundry.id
  description          = "Default project created with the resource"
  display_name         = "Rag-Chatbot-Foundry-2026"

  identity {
    type = "SystemAssigned"
  }


}
resource "azurerm_container_app_environment" "main_container_env" {
  name                = var.container_environment_name
  resource_group_name = azurerm_resource_group.main_rg.name
  location            = azurerm_resource_group.main_rg.location
  workload_profile {
    name                  = "Consumption"
    workload_profile_type = "Consumption"
  }

  lifecycle {
    ignore_changes = [log_analytics_workspace_id]
  }
}
resource "azurerm_container_app" "main_container_app" {
  name                         = var.container_app_name
  container_app_environment_id = azurerm_container_app_environment.main_container_env.id
  resource_group_name          = azurerm_resource_group.main_rg.name
  revision_mode                = "Single"
  max_inactive_revisions       = 100
  workload_profile_name        = "Consumption"

  identity {
    type = "SystemAssigned"
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 8000
    transport                  = "auto"

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = "ragchatbotacr2026.azurecr.io"
    username             = "ragchatbotacr2026"
    password_secret_name = "ragchatbotacr2026azurecrio-ragchatbotacr2026"
  }

  template {
    container {
      name   = "rag-backend-app"
      image  = "ragchatbotacr2026.azurecr.io/rag-backend:bc46d5a91d3b1ab6836724c5d129163b37cf7d47"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name        = "API_KEY"
        secret_name = "api-key"
      }
      env {
        name        = "DATABASE_URL"
        secret_name = "database-url"
      }
      env {
        name        = "ENCRYPTION_KEY"
        secret_name = "encryption-key"
      }
      env {
        name        = "LANGFUSE_HOST"
        secret_name = "langfuse-host"
      }
      env {
        name        = "LANGFUSE_PUBLIC_KEY"
        secret_name = "langfuse-public-key"
      }
      env {
        name        = "LANGFUSE_SECRET_KEY"
        secret_name = "langfuse-secret-key"
      }
      env {
        name        = "OPENAI_API_KEY"
        secret_name = "openai-api-key"
      }
      env {
        name        = "SECRET_KEY"
        secret_name = "secret-key"
      }
      env {
        name        = "AZURE_INFERENCE_URL"
        secret_name = "azure-inference-url"
      }
      env {
        name        = "AZURE_INFERENCE_CREDENTIAL"
        secret_name = "azure-inference-credential"
      }
    }
  }

  lifecycle {
    ignore_changes = [
      secret,
      template[0].container[0].image,
      template[0].container[0].liveness_probe,
      template[0].container[0].readiness_probe,
      template[0].container[0].startup_probe,
    ]
  }
}


