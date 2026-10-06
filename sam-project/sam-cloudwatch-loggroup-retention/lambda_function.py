import boto3

def lambda_handler(event, context):
    # Create CloudWatch client
    cloudwatch_client = boto3.client("logs")

    # Set retention period to 90 days (3 months)
    retention_period = 90

    # Get all log groups with a retention policy
    paginator = cloudwatch_client.get_paginator("describe_log_groups")
    response = paginator.paginate()

    # Lists to hold log groups to update
    log_groups_wo_retention = []
    log_groups_to_update = []

    # Process each log group from paginated response
    for page in response:
        log_groups = page.get("logGroups", [])
        for group in log_groups:
            retention_days = group.get("retentionInDays")

            # Logic 1: Identify log groups with no retention policy
            if retention_days is None:  # No retention set (None means no retention policy)
                log_groups_wo_retention.append(group["logGroupName"])

            # Logic 2: Identify log groups with 10-year (3653 days) retention
            elif retention_days == 3653:  # 10-year retention (3653 days)
                log_groups_to_update.append(group["logGroupName"])

    # Count of log groups to update (both without retention and with 10 years retention)
    lg_count = len(log_groups_wo_retention) + len(log_groups_to_update)
    print(f"Count of log groups to update: {lg_count}")

    # Set retention policy for log groups without retention
    for log_group_name in log_groups_wo_retention:
        try:
            cloudwatch_client.put_retention_policy(
                logGroupName=log_group_name, retentionInDays=retention_period
            )
            print(f"Successfully set retention for log group {log_group_name}")
        except Exception as e:
            print(f"Error setting retention for log group {log_group_name}: {str(e)}")

    # Set retention policy for log groups with 10 years (3653 days) retention
    for log_group_name in log_groups_to_update:
        try:
            cloudwatch_client.put_retention_policy(
                logGroupName=log_group_name, retentionInDays=retention_period
            )
            print(f"Successfully set retention for log group {log_group_name}")
        except Exception as e:
            print(f"Error setting retention for log group {log_group_name}: {str(e)}")

    return {
        'statusCode': 200,
        'body': f'Successfully updated retention policy for {lg_count} log groups.'
    }
