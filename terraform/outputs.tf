# ── Outputs ───────────────────────────────────────────────────
output "vm_public_ip" {
  description = "Public IP of the sandbox VM"
  value       = oci_core_instance.sandbox_vm.public_ip
}

output "vm_private_ip" {
  description = "Private IP of the sandbox VM"
  value       = oci_core_instance.sandbox_vm.private_ip
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh opc@${oci_core_instance.sandbox_vm.public_ip}"
}

output "api_url" {
  description = "URL to access the API"
  value       = "http://${oci_core_instance.sandbox_vm.public_ip}:8000"
}

output "pgadmin_url" {
  description = "URL to access pgAdmin"
  value       = "http://${oci_core_instance.sandbox_vm.public_ip}:5050"
}
