/**
 * CarbonCoach — Terraform Infrastructure Configuration
 *
 * Provisions all Google Cloud resources for the CarbonCoach application:
 * - Cloud Run (backend API)
 * - Cloud Scheduler + Pub/Sub (weekly challenge cron)
 * - BigQuery (aggregate analytics)
 * - Secret Manager (API keys)
 * - Cloud Storage (embedding snapshots)
 */

terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "carboncoach-terraform-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudscheduler.googleapis.com",
    "bigquery.googleapis.com",
    "aiplatform.googleapis.com",
    "firestore.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "pubsub.googleapis.com",
  ])

  service            = each.value
  disable_on_destroy = false
}
