#!/bin/bash
dnf update -y
dnf install -y nginx

systemctl enable nginx
systemctl start nginx

echo "<h1>Terraform EC2 Server</h1>" > /usr/share/nginx/html/index.html