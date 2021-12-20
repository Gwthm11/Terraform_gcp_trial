output "instances_self_links" {
  description = "List of self-links for compute instances"
  value       = google_compute_instance.vm_instance.*.self_link
}

output "instances_details" {
  description = "List of all details for compute instances"
  value       = google_compute_instance.vm_instance.*
}

output "network_details" {
  description = "List of all details for network"
  value       = google_compute_network.vpc_network.*
}

