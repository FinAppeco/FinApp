output "ip" {
  value = google_compute_instance.finapp_instance.network_interface.0.network_ip
}
