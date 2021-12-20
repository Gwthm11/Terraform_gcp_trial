# terraform {
#   required_providers {
#     google = {
#       source  = "hashicorp/google"
#       version = "3.5.0"
#     }
#   }
# }

# provider "google" {
#   credentials = file("orbital-bee-335307-4808ad0a4583.json")

#   project = var.project_id
#   region  = var.region
#   zone    = var.zone
# }

resource "google_compute_network" "vpc_network" {
  name = var.network_name
  project = var.project_id

}

resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name
  machine_type = var.vm_machine_type
  project = var.project_id

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
}
}