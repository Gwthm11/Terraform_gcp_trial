variable "project_id" {
  default     = "orbital-bee-335307"
  description = "Project_id to be used."
}

variable "region" {
  default     = "us-central1"
  description = "Region to be used."
}

variable "zone" {
  default     = "us-central1-c"
  description = "Zone to be used."
}

variable "network_name" {
  default     = "vpc-network"
  description = "Network name to be created."
}

variable "network_name2" {
  default     = "vpc-network2"
  description = "Network name to be created."
}

variable "network_name3" {
  default     = "vpc-network3"
  description = "Network name to be created."
}

variable "vm_name" {
  default     = "terramoduletestvm"
  description = "Virtual Machine name to be created."
}

variable "vm_name2" {
  default     = "terramoduletestvm2"
  description = "Virtual Machine name to be created."
}

variable "vm_name3" {
  default     = "terramoduletestvm3"
  description = "Virtual Machine name to be created."
}

variable "vm_machine_type" {
  default     = "f1-micro"
  description = "Machine type of Virtual Machine name to be created."
}

variable "kubeflow_name" {
  default     = "samplekubeflow"
  description = "Machine type of Virtual Machine name to be created."
}