terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.11.0"
    }
  }
}

provider "google" {
  credentials = file("/home/secondsecondtrial/orbital-bee-335307-1b6243927020.json")
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}

resource "google_service_account" "service_account" {
  account_id   = "samplesat"
  display_name = "Service Account terrafrom"
}

resource "google_service_account_iam_binding" "admin-account-iam" {
  service_account_id = google_service_account.service_account.name
  role               = "roles/iam.serviceAccountUser"

  members = [
    "serviceAccount:samplesat@orbital-bee-335307.iam.gserviceaccount.com",
  ]
}

resource "google_service_account_iam_binding" "admin-account-ia2m" {
  service_account_id = google_service_account.service_account.name
  role               = "roles/iam.serviceAccountAdmin"

  members = [
    "serviceAccount:samplesat@orbital-bee-335307.iam.gserviceaccount.com",
  ]
}

resource "google_project_iam_custom_role" "c1t" {
  role_id     = "c1_t"
  project     = var.project_id
  title       = "My Custom Role1"
  description = "Attempt using terraform"
  permissions = ["storage.buckets.list", "bigquery.tables.list"]
}

resource "google_service_account_iam_binding" "admin-account-ia3m" {
  service_account_id = google_service_account.service_account.name
  role               = google_project_iam_custom_role.c1t.name

  members = [
    "serviceAccount:samplesat@orbital-bee-335307.iam.gserviceaccount.com",
  ]
}

resource "google_project_iam_custom_role" "c2t" {
  role_id     = "c2_t"
  project     = var.project_id
  title       = "My Custom Role2"
  description = "Attempt using terraform"
  permissions = ["storage.buckets.list", "bigquery.tables.list"]
}
# module "vm_nt" {
#   source = "/home/secondsecondtrial/modules/dbcebqgcs_gcp"
#   project_id = var.project_id
#   region = var.region
#   zone = var.zone
#   network_name = var.network_name
#   vm_name = var.vm_name2
#   vm_machine_type = var.vm_machine_type
# }

# module "vm_nt1" {
#   source = "/home/secondsecondtrial/modules/dbcebqgcs_gcp"
#   project_id = var.project_id
#   region = var.region
#   zone = var.zone
#   network_name = var.network_name2
#   vm_name = var.vm_name
#   vm_machine_type = var.vm_machine_type
# }

# resource "google_composer_environment" "test" {
#   name   = "example-composer-env"
#   region = "us-central1"
# }

# module "kubeflow" {
#     source = "/home/secondsecondtrial/modules/gke"
#     name = var.kubeflow_name
#     location = var.region
#     network = var.network_name
#     subnetwork = var.network_name
#     description = "The cluster's description"
#     sa_full_id = "projectall@orbital-bee-335307.iam.gserviceaccount.com"
# }
