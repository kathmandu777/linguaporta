resource "google_cloud_run_service" "linguaporta" {
  name     = "linguaporta"
  location = "asia-northeast1"

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello"
      }
    }
  }

  lifecycle {
    ignore_changes = [template]
  }

  depends_on = [
    google_project_service.project["run.googleapis.com"],
  ]
}
