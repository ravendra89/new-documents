provider "aws" {
  region = var.aws_region
  profile = "terraform_user"
}

# Security Group for ALB
resource "aws_security_group" "alb_sg" {
  name        = "alb-sg"
  description = "Allow HTTP inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ALB
resource "aws_lb" "pre_prod_alb" {
  name               = "pre-prod-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = var.subnet_ids

  enable_deletion_protection = false
}

# Target Group with Conditional Attributes
resource "aws_lb_target_group" "pre_prod_target_grp_http" {
  name     = "test-trg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  load_balancing_algorithm_type     = var.application_name == "UI-WEB" ? "weighted_random" : "round_robin"
  load_balancing_anomaly_mitigation = var.application_name == "UI-WEB" ? "on" : "off"

  health_check {
    healthy_threshold   = 3
    unhealthy_threshold = 5
    timeout             = 10
    port                = 80
    path                = var.health_check_path
    protocol            = "HTTP"
    interval            = 60
    matcher             = "200-299"
  }
}

# Listener
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.pre_prod_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.pre_prod_target_grp_http.arn
  }
}
