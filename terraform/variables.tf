# Authentication
variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "region" {}

# Compartment
variable "compartment_ocid" {}

# VM
variable "ssh_public_key" {
  description = "SSH public key to access the VM"
}

variable "availability_domain" {
  default = "apMk:AP-OSAKA-1-AD-1"
}

variable "vm_shape" {
  default = "VM.Standard.A1.Flex"
}

variable "vm_ocpus" {
  default = 2
}

variable "vm_memory_gb" {
  default = 12
}

variable "vm_display_name" {
  default = "devops-sandbox"
}
