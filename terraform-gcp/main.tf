terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.21.0"
    }
  }
}

provider "google" {
  credentials = "${var.credentials_file}"
  project     = "${var.project}"
  region      = "${var.region}"
  zone        = "${var.zone}"
}

resource "google_compute_network" "vpc_network" {
  name = "finapp-network"
}

resource "google_compute_firewall" "finapp_firewall" {
  name    = "finapp-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol  = "tcp"
    ports     = ["80", "8080", "1000-2000"]
  }

  allow {
    protocol = "tcp"
    ports    = ["80", "8080", "1000-2000"]
  }

  source_tags = ["web"]
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
//https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_instance
resource "google_compute_instance" "finapp_instance" {
  name         = "terraform-instance"
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }
}