resource "aws_wafv2_web_acl" "prod_ae_webacl" {
  name        = local.name_prefix
  scope       = "REGIONAL" # or "CLOUDFRONT" for global
  description = "A WAF ACL with dynamic rules"

  default_action {
    allow {}
  }

  # Dynamic block to define rules from var.rules
  dynamic "rule" {
    for_each = toset(var.managed_rules)

    content {
      name     = rule.value.name
      priority = rule.value.priority

      override_action {
        count {}
      }

      statement {
        managed_rule_group_statement {
          name        = rule.value.managed_rule_group_statement_name
          vendor_name = rule.value.managed_rule_group_statement_vendor_name
        }
      }

      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name                = rule.value.metric_name
        sampled_requests_enabled   = true
      }
    }
  }
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "main-web-acl-metrics"
    sampled_requests_enabled   = true
  }
  #Add Geo-block Rules dynamically
  dynamic "rule" {
    for_each = toset(var.country_block_rules)

    content {
      name     = rule.value.name
      priority = rule.value.priority

      action {
        block {}
      }

      statement {
        geo_match_statement {
          country_codes = rule.value.country_codes
        }
      }

      visibility_config {
        cloudwatch_metrics_enabled = true
        metric_name                = rule.value.metric_name
        sampled_requests_enabled   = true
      }
    }
  }
  # AmazonIpReputationList block Rules
  rule {
    name     = "AWS-AWSManagedRulesAmazonIpReputationList"
    priority = 1

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"

        rule_action_override {
          name = "AWSManagedIPReputationList"
          action_to_use {
            block {}
          }
        }

        rule_action_override {
          name = "AWSManagedReconnaissanceList"
          action_to_use {
            block {}
          }
        }

        rule_action_override {
          name = "AWSManagedIPDDoSList"
          action_to_use {
            block {}
          }
        }
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AWS-AWSManagedRulesAmazonIpReputationList"
      sampled_requests_enabled   = true
    }
  }
}
# Create CloudWatch Log Group for WAF logs
resource "aws_cloudwatch_log_group" "waf_log_group" {
  name              = var.cloudwatch_loggroup_name
  retention_in_days = 90
}
# Set up logging configuration for WAF ACL
resource "aws_wafv2_web_acl_logging_configuration" "waf_acl_logging" {
  log_destination_configs = [aws_cloudwatch_log_group.waf_log_group.arn]
  resource_arn            = aws_wafv2_web_acl.prod_ae_webacl.arn
  depends_on              = [aws_cloudwatch_log_group.waf_log_group]
  redacted_fields {
    single_header {
      name = "user-agent"
    }
  }
}

#  WAF ACL association with the Application Load Balancer (existing ALB)
# resource "aws_wafv2_web_acl_association" "prod_alb_waf_acl_association" {
#   resource_arn = aws_lb.prod_alb.arn  # Reference the ALB resource created elsewhere
#   web_acl_arn  = aws_wafv2_web_acl.prod-ae-web-webacl.arn
# }
