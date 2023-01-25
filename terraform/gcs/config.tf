terraform {
  backend "gcs" {
    bucket = "linguaporta-tfstate" # before terraform init, create this bucket
    # key    = "gcp/terraform.tfstate"
    # region = var.region
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}
