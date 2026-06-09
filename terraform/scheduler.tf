/**
 * CarbonCoach — Cloud Scheduler & Pub/Sub for Weekly Challenges
 */

# Pub/Sub topic for challenge generation triggers
resource "google_pubsub_topic" "challenge_trigger" {
  name = "carboncoach-challenge-trigger"

  depends_on = [google_project_service.apis]
}

# Cloud Scheduler job: every Monday at 8:00 AM IST
resource "google_cloud_scheduler_job" "weekly_challenges" {
  name        = "carboncoach-weekly-challenges"
  description = "Triggers weekly carbon challenge generation for all users"
  schedule    = var.challenge_cron_schedule
  time_zone   = var.challenge_cron_timezone
  region      = var.region

  depends_on = [google_project_service.apis]

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.challenge_generator.url

    oidc_token {
      service_account_email = google_service_account.scheduler.email
    }
  }

  retry_config {
    retry_count          = 3
    min_backoff_duration = "10s"
    max_backoff_duration = "300s"
  }
}

# Cloud Function for challenge generation
resource "google_cloudfunctions2_function" "challenge_generator" {
  name     = "carboncoach-challenge-generator"
  location = var.region

  depends_on = [google_project_service.apis]

  build_config {
    runtime     = "python311"
    entry_point = "generate_weekly_challenges"

    source {
      storage_source {
        bucket = google_storage_bucket.functions_source.name
        object = google_storage_bucket_object.functions_zip.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "512M"
    timeout_seconds       = 540 # 9 minutes (max for gen2)
    service_account_email = google_service_account.challenge_function.email

    environment_variables = {
      GOOGLE_CLOUD_PROJECT = var.project_id
      VERTEX_AI_LOCATION   = var.region
    }
  }
}

# Storage bucket for function source code
resource "google_storage_bucket" "functions_source" {
  name     = "${var.project_id}-functions-source"
  location = var.region

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "functions_zip" {
  name   = "functions-source.zip"
  bucket = google_storage_bucket.functions_source.name
  source = "../functions/functions-source.zip"
}

# Service accounts
resource "google_service_account" "scheduler" {
  account_id   = "carboncoach-scheduler"
  display_name = "CarbonCoach Cloud Scheduler"
}

resource "google_service_account" "challenge_function" {
  account_id   = "carboncoach-challenge-fn"
  display_name = "CarbonCoach Challenge Generator Function"
}

# Grant function SA access to Firestore and Vertex AI
resource "google_project_iam_member" "function_firestore" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.challenge_function.email}"
}

resource "google_project_iam_member" "function_vertex" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.challenge_function.email}"
}

# Allow scheduler to invoke the function
resource "google_cloud_run_v2_service_iam_member" "scheduler_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloudfunctions2_function.challenge_generator.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.scheduler.email}"
}
