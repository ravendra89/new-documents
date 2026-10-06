variable "country_block_rules" {
  type = list(any)
  default = [
    {
      name          = "geo-block-rule"
      priority      = 0
      country_codes = ["CN", "RU", "UA"] # Block traffic from China, Russia and Ukraine.
      metric_name   = "geo-block-rule"
    }
  ]
}

variable "managed_rules" {
  type = list(any)
  default = [
    # {
    #   name                                     = "AWS-AWSManagedRulesAmazonIpReputationList"
    #   priority                                 = 1
    #   managed_rule_group_statement_name        = "AWSManagedRulesAmazonIpReputationList"
    #   managed_rule_group_statement_vendor_name = "AWS"
    #   metric_name                              = "AWS-AWSManagedRulesAmazonIpReputationList"                               
    # },
    {
      name                                     = "AWS-AWSManagedRulesLinuxRuleSet"
      priority                                 = 2
      managed_rule_group_statement_name        = "AWSManagedRulesLinuxRuleSet"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesLinuxRuleSet"
    },
    {
      name                                     = "AWS-AWSManagedRulesSQLiRuleSet"
      priority                                 = 3
      managed_rule_group_statement_name        = "AWSManagedRulesSQLiRuleSet"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesSQLiRuleSet"
    },
    {
      name                                     = "AWS-AWSManagedRulesCommonRuleSet"
      priority                                 = 4
      managed_rule_group_statement_name        = "AWSManagedRulesCommonRuleSet"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesCommonRuleSet"
    },
    {
      name                                     = "AWS-AWSManagedRulesKnownBadInputsRuleSet"
      priority                                 = 5
      managed_rule_group_statement_name        = "AWSManagedRulesKnownBadInputsRuleSet"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesKnownBadInputsRuleSet"
    },
    {
      name                                     = "AWS-AWSManagedRulesPHPRuleSet"
      priority                                 = 6
      managed_rule_group_statement_name        = "AWSManagedRulesPHPRuleSet"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesPHPRuleSet"
    },
    {
      name                                     = "AWS-AWSManagedRulesAnonymousIpList"
      priority                                 = 7
      managed_rule_group_statement_name        = "AWSManagedRulesAnonymousIpList"
      managed_rule_group_statement_vendor_name = "AWS"
      metric_name                              = "AWS-AWSManagedRulesAnonymousIpList"
    }
  ]
}