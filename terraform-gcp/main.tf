terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.21.0"
    }
  }
}

provider "google" {
  credentials = file("keyfile.json")
  project     = "mlops-3"
  region      = "us-central1"
  zone        = "us-central1-c"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

# Create new storage bucket in the US multi-region
# with coldline storage
resource "google_storage_bucket" "data-lake" {
  name          = "finapp"
  location      = "US"
  storage_class = "COLDLINE"
  force_destroy = true

  uniform_bucket_level_access = true
}