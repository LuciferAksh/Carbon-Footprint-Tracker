/**
 * CarbonCoach — Cloud Run Backend Service
 */

resource "google_cloud_run_v2_service" "backend" {
  name     = "carboncoach-backend"
  location = var.region

  depends_on = [google_project_service.apis]

  template {
    containers {
      image = var.backend_image

      ports {
        container_port = 8000
      }

      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }

      env {
        name  = "VERTEX_AI_LOCATION"
        value = var.region
      }

      env {
        name  = "FIRESTORE_DATABASE"
        value = "(default)"
      }

      env {
        name  = "BIGQUERY_DATASET"
        value = google_bigquery_dataset.analytics.dataset_id
      }

      env {
        name = "MAPS_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.maps_api_key.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true # Scale to zero when not in use
      }

      startup_probe {
        http_get {
          path = "/api/health"
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        failure_threshold     = 3
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    service_account = google_service_account.backend.email
  }

  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}

# Service account for the backend
resource "google_service_account" "backend" {
  account_id   = "carboncoach-backend"
  display_name = "CarbonCoach Backend Service Account"
}

# Grant necessary roles to the backend service account
resource "google_project_iam_member" "backend_firestore" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_project_iam_member" "backend_vertex" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_project_iam_member" "backend_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_project_iam_member" "backend_secrets" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

# Allow unauthenticated access (Firebase handles auth at app level)
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "backend_url" {
  description = "Cloud Run backend service URL"
  value       = google_cloud_run_v2_service.backend.uri
}
