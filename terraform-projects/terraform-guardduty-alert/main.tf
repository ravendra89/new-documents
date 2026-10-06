resource "aws_guardduty_detector" "guardduty" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = false
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = true
        }
      }
    }
  }
}

resource "aws_sns_topic" "sns_topic" {
  name            = "sns-topic"
  delivery_policy = <<EOF
{
  "http": {
    "defaultHealthyRetryPolicy": {
      "minDelayTarget": 20,
      "maxDelayTarget": 20,
      "numRetries": 3,
      "numMaxDelayRetries": 0,
      "numNoDelayRetries": 0,
      "numMinDelayRetries": 0,
      "backoffFunction": "linear"
    },
    "disableSubscriptionOverrides": false,
    "defaultThrottlePolicy": {
      "maxReceivesPerSecond": 1
    }
  }
}
EOF
}

# Create subscription for the SNS topic
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.sns_topic.arn
  protocol  = "email"
  endpoint  = "example.com" # Replace with your email address
}

# Create CloudWatch Event Rule to forward GuardDuty findings to the SNS topic
resource "aws_cloudwatch_event_rule" "guardduty_event_rule" {
  name        = "ForwardGuardDutyFindings"
  description = "Forward GuardDuty findings to SNS Topic"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.guardduty"
  ],
  "detail-type": [
    "GuardDuty Finding"
  ],
  "detail": {
    "severity": [
      4,
      4.0,
      4.1,
      4.2,
      4.3,
      4.4,
      4.5,
      4.6,
      4.7,
      4.8,
      4.9,
      5,
      5.0,
      5.1,
      5.2,
      5.3,
      5.4,
      5.5,
      5.6,
      5.7,
      5.8,
      5.9,
      6,
      6.0,
      6.1,
      6.2,
      6.3,
      6.4,
      6.5,
      6.6,
      6.7,
      6.8,
      6.9,
      7,
      7.0,
      7.1,
      7.2,
      7.3,
      7.4,
      7.5,
      7.6,
      7.7,
      7.8,
      7.9,
      8,
      8.0,
      8.1,
      8.2,
      8.3,
      8.4,
      8.5,
      8.6,
      8.7,
      8.8,
      8.9
    ]
  }
}
PATTERN

}

# Permission for CloudWatch Events to invoke SNS topic
resource "aws_cloudwatch_event_target" "guardduty_event_target" {
  rule      = aws_cloudwatch_event_rule.guardduty_event_rule.name
  target_id = "sns_target"
  arn       = aws_sns_topic.sns_topic.arn
  # following code used into the  Target input transformer, for the Input Path text box.

  input_transformer {
    input_paths = {
      "severity": "$.detail.severity",
      "Account_ID": "$.detail.accountId",
      "Finding_ID": "$.detail.id",
      "Finding_Type": "$.detail.type",
      "region": "$.region",
      "Finding_description": "$.detail.description"
    }
    # following code used into the Input Template field to format the email.
    input_template = <<TEMPLATE
"AWS <Account_ID> has a severity <severity> GuardDuty finding type <Finding_Type> in the <region> region."
"Finding Description:"
"<Finding_description>. "
"For more details, open the GuardDuty console at https://console.aws.amazon.com/guardduty/home?region=<region>#/findings?search=id%3D<Finding_ID>"
TEMPLATE
  }

}

# Create CloudWatch Event Rule for SNS subscription
resource "aws_cloudwatch_event_rule" "sns_rule" {
  name        = "GuardDutySNSSubscription"
  description = "Subscribe SNS topic to CloudWatch Events"
  event_pattern = jsonencode({
    source      = ["aws.sns"],
    detail_type = ["AWS API Call via CloudTrail"],
    resources   = [aws_sns_topic.sns_topic.arn],
  })
}

# Create CloudWatch Event Target for SNS subscription
resource "aws_cloudwatch_event_target" "sns_target" {
  rule      = aws_cloudwatch_event_rule.sns_rule.name
  target_id = "sns_subscription"
  arn       = aws_sns_topic.sns_topic.arn
}
