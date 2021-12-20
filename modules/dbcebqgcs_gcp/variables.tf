variable "project_id" { 
  type        = string
  description = "Project_id to be used."
}

variable "region" {
  type        = string
  description = "Region where the instances should be created."
}

variable "zone" {
  type        = string
  description = "Zone where the instances should be created. If not specified, instances will be spread across available zones in the region."
}

variable "network_name" {
    type     = string
}

variable "vm_name" {
    type     = string
}

variable "vm_machine_type" {
    type     = string
}