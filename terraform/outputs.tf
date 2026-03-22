output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.main.id
}

output "instance_public_ip" {
  description = "Public IP of the EC2 instance (use this for EC2_HOST secret)"
  value       = aws_instance.main.public_ip
}

output "app_url" {
  description = "URL to access the TaskMaster app"
  value       = "http://${aws_instance.main.public_ip}:${var.app_port}"
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = "ssh -i taskmaster-key.pem ubuntu@${aws_instance.main.public_ip}"
}

output "private_key_pem" {
  description = "SSH private key (use this for EC2_SSH_KEY secret)"
  value       = tls_private_key.ssh_key.private_key_pem
  sensitive   = true
}

output "setup_instructions" {
  description = "How to connect terraform outputs to the CD workflow"
  value       = <<-INSTRUCTIONS

  ============================================
    Set these GitHub repository secrets:
  ============================================

    EC2_HOST    = ${aws_instance.main.public_ip}
    EC2_USER    = ubuntu
    EC2_SSH_KEY = Run: terraform output -raw private_key_pem

  Then push app code to main to trigger deployment!

  INSTRUCTIONS
}
