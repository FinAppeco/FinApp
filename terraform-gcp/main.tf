terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.22.0"
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

//https://cloud.google.com/sql/docs/postgres/authorize-networks?authuser=1#terraform
resource "google_sql_database_instance" "default" {
  name                = "postgres-instance-finapp"
  database_version    = "POSTGRES_14"
  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      # Enable public IP
      ipv4_enabled = true
      authorized_networks {
        name  = "Christian"
        value = "190.121.133.221/32"
      }

    }
  }
  deletion_protection = "true"
}
#When you create a new Cloud SQL instance, you must configure the default user account
#before you can connect to the instance. For Cloud SQL for PostgreSQL, the default user is postgres.
#gcloud sql users set-password postgres --instance=INSTANCE_NAME --prompt-for-password
//https://cloud.google.com/sql/docs/postgres/create-manage-users?authuser=1
resource "google_sql_user" "finapp" {
  name     = "finapp"
  instance = google_sql_database_instance.default.name
  password = "${var.sql_user_pwd}"
}

//https://cloud.google.com/sql/docs/postgres/authorize-networks?authuser=1#terraform
resource "google_sql_database_instance" "default" {
  name                = "postgres-instance-finapp"
  database_version    = "POSTGRES_14"
  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      # Enable public IP
      ipv4_enabled = true
      authorized_networks {
        name  = "Christian"
        value = "190.121.133.221/32"
      }

    }
  }
  deletion_protection = "true"
}
#When you create a new Cloud SQL instance, you must configure the default user account
#before you can connect to the instance. For Cloud SQL for PostgreSQL, the default user is postgres.
#gcloud sql users set-password postgres --instance=INSTANCE_NAME --prompt-for-password
//https://cloud.google.com/sql/docs/postgres/create-manage-users?authuser=1
resource "google_sql_user" "finapp" {
  name     = "finapp"
  instance = google_sql_database_instance.default.name
  password = "${var.sql_user_pwd}"
}

//https://cloud.google.com/sql/docs/postgres/authorize-networks?authuser=1#terraform
resource "google_sql_database_instance" "default" {
  name                = "postgres-instance-finapp"
  database_version    = "POSTGRES_14"
  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      # Enable public IP
      ipv4_enabled = true
      authorized_networks {
        name  = "Christian"
        value = "190.121.133.221/32"
      }

    }
  }
  deletion_protection = "true"
}
#When you create a new Cloud SQL instance, you must configure the default user account
#before you can connect to the instance. For Cloud SQL for PostgreSQL, the default user is postgres.
#gcloud sql users set-password postgres --instance=INSTANCE_NAME --prompt-for-password
//https://cloud.google.com/sql/docs/postgres/create-manage-users?authuser=1
resource "google_sql_user" "finapp" {
  name     = "finapp"
  instance = google_sql_database_instance.default.name
  password = "${var.sql_user_pwd}"
}

//https://cloud.google.com/sql/docs/postgres/authorize-networks?authuser=1#terraform
resource "google_sql_database_instance" "default" {
  name                = "postgres-instance-finapp"
  database_version    = "POSTGRES_14"
  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      # Enable public IP
      ipv4_enabled = true
      authorized_networks {
        name  = "Christian"
        value = "190.121.133.221/32"
      }

    }
  }
  deletion_protection = "true"
}
#When you create a new Cloud SQL instance, you must configure the default user account
#before you can connect to the instance. For Cloud SQL for PostgreSQL, the default user is postgres.
#gcloud sql users set-password postgres --instance=INSTANCE_NAME --prompt-for-password
//https://cloud.google.com/sql/docs/postgres/create-manage-users?authuser=1
resource "google_sql_user" "finapp" {
  name     = "finapp"
  instance = google_sql_database_instance.default.name
  password = "${var.sql_user_pwd}"
}

//https://cloud.google.com/sql/docs/postgres/authorize-networks?authuser=1#terraform
resource "google_sql_database_instance" "default" {
  name                = "postgres-instance-finapp"
  database_version    = "POSTGRES_14"
  settings {
    tier = "db-custom-2-7680"
    ip_configuration {
      # Enable public IP
      ipv4_enabled = true
      authorized_networks {
        name  = "Christian"
        value = "190.121.133.221/32"
      }

    }
  }
  deletion_protection = "true"
}
#When you create a new Cloud SQL instance, you must configure the default user account
#before you can connect to the instance. For Cloud SQL for PostgreSQL, the default user is postgres.
#gcloud sql users set-password postgres --instance=INSTANCE_NAME --prompt-for-password
//https://cloud.google.com/sql/docs/postgres/create-manage-users?authuser=1
resource "google_sql_user" "finapp" {
  name     = "finapp"
  instance = google_sql_database_instance.default.name
  password = "${var.sql_user_pwd}"
}