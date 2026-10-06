data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "${path.module}/lambda_function_payload.zip"
}

resource "aws_lambda_function" "sg_open_port_alert_lambda" {
  function_name = local.name_prefix
  runtime       = "python3.13"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "lambda_function.lambda_handler"
  filename      = data.archive_file.lambda_zip.output_path
  memory_size   = 128
  timeout       = 300

 environment {
    variables = {
      EXCLUDED_SECURITY_GROUP_IDS = var.excluded_security_group_ids
      SNS_TOPIC_ARN               = var.sns_topic_arn
    }
  }

  depends_on = [data.archive_file.lambda_zip]
}

resource "aws_cloudwatch_event_rule" "sg_open_port_alert_rule" {
  name                = local.name_prefix
  schedule_expression = "rate(1 hour)"
  state               = "ENABLED"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.sg_open_port_alert_rule.name
  target_id = "SGCheckLambda"
  arn       = aws_lambda_function.sg_open_port_alert_lambda.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sg_open_port_alert_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.sg_open_port_alert_rule.arn
}
