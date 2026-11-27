variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}
variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}
variable "resource_group" {
  description = "Resource Group Name"
  type        = string
  default     = "Rag-Chatbot"
}
variable "location" {
  description = "Azure region for the resources"
  type        = string
  default     = "southafricanorth"
}
variable "db_name" {
  description = "The Name of the Postgres Db"
  type        = string
  default     = "rag-chatbot-db"
}
variable "container_registry_name" {
  description = "The name of the Azure Container Registry"
  type        = string
  default     = "ragchatbotacr2026"
}

variable "key_vault_name" {
  description = "The name of the Azure Key Vault"
  type        = string
  default     = "Rag-Chatbot-Vault"
}

variable "foundry_name" {
  description = "The Name of the Azure Foundry Service"
  type        = string
  default     = "Rag-Chatbot-Foundry-2026"
}

variable "container_environment_name" {
  description = "The Name of the Environment for the Container App"
  type        = string
  default     = "rag-backend-env"
}

variable "container_app_name" {
  description = "The Name of the Container App"
  type        = string
  default     = "rag-backend-app"
}