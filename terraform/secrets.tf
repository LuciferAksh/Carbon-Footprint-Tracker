/**
 * CarbonCoach — Secret Manager Configuration
 */

# Maps API key
resource "google_secret_manager_secret" "maps_api_key" {
  secret_id = "carboncoach-maps-api-key"

  depends_on = [google_project_service.apis]

  replication {
    auto {}
  }

  labels = {
    app = "carboncoach"
  }
}

resource "google_secret_manager_secret_version" "maps_api_key_version" {
  secret      = google_secret_manager_secret.maps_api_key.id
  secret_data = "placeholder-maps-key"
}

# Embedding snapshots storage bucket
resource "google_storage_bucket" "embeddings" {
  name     = "${var.project_id}-carboncoach-embeddings"
  location = var.region

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 90 # Clean up old snapshots after 90 days
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    app = "carboncoach"
  }
}

# Grant backend access to embeddings bucket
resource "google_storage_bucket_iam_member" "backend_storage" {
  bucket = google_storage_bucket.embeddings.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.backend.email}"
}
