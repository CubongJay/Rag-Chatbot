
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "Rg-Terraform-State"
    storage_account_name = "sttfstateubj2026"
    container_name       = "tfstate"
    key                  = "ragchatbot.tfstate"

  }
}
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}