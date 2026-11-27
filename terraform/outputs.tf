output "container_app_url" {
  description = "Public HTTPS URL of the RAG backend Container App"
  value       = "https://${azurerm_container_app.main_container_app.ingress[0].fqdn}"
}

output "foundry_endpoint" {
  description = "Azure AI Foundry account endpoint"
  value       = azurerm_cognitive_account.main_foundry.endpoint
}
