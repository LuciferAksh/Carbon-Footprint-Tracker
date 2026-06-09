/**
 * CarbonCoach — Terraform Outputs
 */

output "cloud_run_url" {
  description = "Backend API URL (Cloud Run)"
  value       = google_cloud_run_v2_service.backend.uri
}

output "challenge_function_url" {
  description = "Challenge generator Cloud Function URL"
  value       = google_cloudfunctions2_function.challenge_generator.url
}

output "bigquery_dataset" {
  description = "BigQuery analytics dataset ID"
  value       = google_bigquery_dataset.analytics.dataset_id
}

output "embeddings_bucket" {
  description = "Cloud Storage bucket for embedding snapshots"
  value       = google_storage_bucket.embeddings.name
}
