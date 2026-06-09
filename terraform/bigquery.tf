/**
 * CarbonCoach — BigQuery Analytics Dataset
 */

resource "google_bigquery_dataset" "analytics" {
  dataset_id    = "carboncoach_analytics"
  friendly_name = "CarbonCoach Analytics"
  description   = "Aggregate carbon footprint trends and community analytics"
  location      = var.region

  depends_on = [google_project_service.apis]

  default_table_expiration_ms = null # No expiration

  labels = {
    app = "carboncoach"
    env = "production"
  }
}

# Daily aggregate emissions table
resource "google_bigquery_table" "daily_emissions" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "daily_emissions"

  time_partitioning {
    type  = "DAY"
    field = "date"
  }

  clustering = ["category", "region"]

  schema = jsonencode([
    {
      name = "date"
      type = "DATE"
      mode = "REQUIRED"
      description = "Activity date"
    },
    {
      name = "user_id"
      type = "STRING"
      mode = "REQUIRED"
      description = "Anonymous user identifier"
    },
    {
      name = "category"
      type = "STRING"
      mode = "REQUIRED"
      description = "Emission category: transport, food, energy, shopping"
    },
    {
      name = "co2_kg"
      type = "FLOAT64"
      mode = "REQUIRED"
      description = "CO2 emissions in kilograms"
    },
    {
      name = "region"
      type = "STRING"
      mode = "NULLABLE"
      description = "User region for geographic analysis"
    },
    {
      name = "carbon_profile_type"
      type = "STRING"
      mode = "NULLABLE"
      description = "User's Gemini-assigned carbon profile type"
    },
  ])

  labels = {
    app = "carboncoach"
  }
}

# Community aggregates view
resource "google_bigquery_table" "community_aggregates" {
  dataset_id = google_bigquery_dataset.analytics.dataset_id
  table_id   = "community_aggregates_view"

  view {
    query          = <<-SQL
      SELECT
        category,
        AVG(co2_kg) AS avg_co2_kg,
        APPROX_QUANTILES(co2_kg, 100)[OFFSET(50)] AS median_co2_kg,
        APPROX_QUANTILES(co2_kg, 100)[OFFSET(20)] AS p20_co2_kg,
        APPROX_QUANTILES(co2_kg, 100)[OFFSET(80)] AS p80_co2_kg,
        COUNT(DISTINCT user_id) AS total_users,
        DATE_TRUNC(date, WEEK) AS week
      FROM `${var.project_id}.${google_bigquery_dataset.analytics.dataset_id}.daily_emissions`
      WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
      GROUP BY category, week
      ORDER BY week DESC, category
    SQL
    use_legacy_sql = false
  }

  labels = {
    app = "carboncoach"
  }
}
