/**
 * CarbonCoach — Terraform Variables
 */

variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region for deployment"
  type        = string
  default     = "asia-south1" # Mumbai
}

variable "zone" {
  description = "Google Cloud zone"
  type        = string
  default     = "asia-south1-a"
}

variable "backend_image" {
  description = "Docker image for the Cloud Run backend service"
  type        = string
  default     = "gcr.io/PROJECT_ID/carboncoach-backend:latest"
}

variable "frontend_domain" {
  description = "Custom domain for Firebase Hosting (optional)"
  type        = string
  default     = ""
}

variable "challenge_cron_schedule" {
  description = "Cron schedule for weekly challenge generation (default: Monday 8am IST)"
  type        = string
  default     = "0 8 * * 1" # Monday at 8:00 AM
}

variable "challenge_cron_timezone" {
  description = "Timezone for the challenge cron schedule"
  type        = string
  default     = "Asia/Kolkata"
}
