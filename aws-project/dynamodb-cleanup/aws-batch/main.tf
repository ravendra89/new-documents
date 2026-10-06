# ===============================
# Security Group
resource "aws_security_group" "batch_sg" {
  vpc_id      = var.vpc_id
  name        = "${var.environment}-${var.security_group_name}"
  description = "DYNAMODB CLEANUP AWSBATCH SG"

  tags = {
    Name = "${var.environment}-${var.security_group_name}"
  }

  ingress = [
    merge(
      var.default_sg_rule,  
      {
        protocol    = "tcp",
        cidr_blocks = [var.vpc_cidr],
        from_port   = 80,
        to_port     = 80
      }
    ),
    merge(
      var.default_sg_rule,  
      {
        protocol    = "tcp",
        cidr_blocks = [var.vpc_cidr],
        from_port   = 443,
        to_port     = 443
      }
    ),
    merge(
      var.default_sg_rule,  
      {
        protocol    = "tcp",
        cidr_blocks = [var.vpc_cidr],
        from_port   = 22,
        to_port     = 22
      }
    )
  ]

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

}

# ===============================
# Compute Environment
resource "aws_batch_compute_environment" "batch_env" {
  compute_resources {
    max_vcpus = 4

    security_group_ids = [
      aws_security_group.batch_sg.id
    ]

    subnets = [
      var.subnet_id
    ]

    type = "FARGATE"
  }

  service_role = "arn:aws:iam::376267276199:role/aws-service-role/batch.amazonaws.com/AWSServiceRoleForBatch"
  type         = "MANAGED"
}

# ===============================
# Job Queue
resource "aws_batch_job_queue" "batch_queue" {
  name     = "${var.environment}-AD-SERVERS-DYNAMODB-CLEANUP-QUEUE"
  state    = "ENABLED"
  priority = 200

  compute_environment_order {
    compute_environment = aws_batch_compute_environment.batch_env.arn
    order = 1
  }

  # compute_environments = [
  #   aws_batch_compute_environment.batch_env.arn
  # ]
}

#===============================
#Job Definitions
resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.environment}-AD-SERVERS-DYNAMODB-CLEANUP-ROLE"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "inline_policy" {
  name = "${var.environment}-AD-SERVERS-DYNAMODB-CLEANUP-POLICY"
  role = aws_iam_role.ecs_task_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:DeleteItem",
          "s3:PutObject",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken",
          "ecr:ReplicateImage",
          "ecr:PutImage",
          "ec2:DescribeInstances"
        ]
        Effect   = "Allow"
        Resource = [
          "*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "aws_batch_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_iam_role_policy_attachment" "aws_ssm_read_only_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "ssm_managed_instance_core" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "ec2_read_only" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "image_builder_read_only" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSImageBuilderReadOnlyAccess"
}

resource "aws_iam_role_policy_attachment" "ec2_image_builder_cross_account_distribution" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/Ec2ImageBuilderCrossAccountDistributionAccess"
}

data "template_file" "dynamo_cleanup_job_template" {
  template = "${file("dynamo_cleanup_job.json")}"

  vars = {
    "JOB_ROLE" = "${aws_iam_role.ecs_task_execution_role.arn}"
    "EXECUTION_ROLE" = "${aws_iam_role.ecs_task_execution_role.arn}"
  }

}

resource "aws_batch_job_definition" "dynamo_cleanup_job" {
  name = "${var.environment}-AD-SERVERS-DYNAMODB-CLEANUP-DEFINITION"
  type = "container"
  platform_capabilities = [
    "FARGATE",
  ]
  timeout {
    attempt_duration_seconds = 129600 # 36 hours timeout
  }
  container_properties   = "${data.template_file.dynamo_cleanup_job_template.rendered}"
}