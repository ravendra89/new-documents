import boto3
import logging
from datetime import datetime, timedelta

# Initialize clients for DynamoDB and EC2
dynamodb = boto3.resource('dynamodb')
ec2 = boto3.client('ec2')

# List of DynamoDB tables
tables = [
    "mms-prod-ad-servers"
]

# Set up logging for the application
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def process_terminated_instances():
    """
    Main function to process and remove terminated instances from DynamoDB.
    """
    # Get the cutoff date: 6 months ago
    cutoff_date = datetime.now() - timedelta(days=180)
    cutoff_timestamp = int(cutoff_date.timestamp())  # Convert to Unix timestamp (seconds)

    # Loop through each table to check terminated instances
    terminated_instances = []
    for table in tables:
        terminated_instances.extend(find_terminated_instances(table, cutoff_timestamp))

    if not terminated_instances:
        logger.info("No terminated instances found in DynamoDB.")
        return {"statusCode": 200, "body": "No terminated instances found."}  # Exit if no terminated instances are found

    # Cross-check with EC2
    instances_status_verified = cross_check_instances(terminated_instances)

    # If EC2 state matches found, append the EC2 state to each terminated instance
    if not instances_status_verified:
        logger.info("No instances found in EC2 that match the terminated instances from DynamoDB.")
        # Still, append 'EC2State' as "Not Found" for instances
        for instance in terminated_instances:
            instance['EC2State'] = 'Not Found'

    # Remove terminated instances from DynamoDB after cross-check
    remove_terminated_instances_from_dynamodb(terminated_instances)

    return {"statusCode": 200, "body": "Terminated instances verified and removed."}

def find_terminated_instances(table_name, cutoff_timestamp):
    terminated_instances = []

    # Get the DynamoDB table resource
    table = dynamodb.Table(table_name)

    # Scan the table for all items
    scan_kwargs = {'TableName': table_name}
    last_evaluated_key = None

    while True:
        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

        try:
            response = table.scan(**scan_kwargs)
        except Exception as e:
            logger.error(f"Error scanning table {table_name}: {str(e)}")
            return terminated_instances  # Exit if there's a scan error

        items = response.get('Items', [])
        logger.info(f"Scanned {len(items)} items in table {table_name}")

        for item in items:
            instance_state = item.get('InstanceState', '')

            if isinstance(instance_state, dict):
                instance_state = instance_state.get('S', '')

            if instance_state == 'TERMINATED':
                ad_join_date = item.get('ADJoinDate', '')
                instance_termination_date = item.get('InstanceTerminationDate', '')  # Correct field name

                if isinstance(ad_join_date, dict):
                    ad_join_date = ad_join_date.get('S', '')

                if isinstance(instance_termination_date, dict):
                    instance_termination_date = instance_termination_date.get('S', '')

                # Case 1: ADJoinDate is found and is older than cutoff date
                if ad_join_date:
                    try:
                        ad_join_datetime = datetime.fromisoformat(ad_join_date)
                        item_timestamp = int(ad_join_datetime.timestamp())

                        if item_timestamp <= cutoff_timestamp:
                            terminated_instances.append(item)
                    except ValueError:
                        continue  # Skip invalid ADJoinDate format

                # Case 2: ADJoinDate is not found, but InstanceTerminationDate is older than 6 months
                elif instance_termination_date:
                    try:
                        termination_datetime = datetime.fromisoformat(instance_termination_date)
                        termination_timestamp = int(termination_datetime.timestamp())

                        if termination_timestamp <= cutoff_timestamp:
                            terminated_instances.append(item)
                    except ValueError:
                        continue  # Skip invalid InstanceTerminationDate format

        last_evaluated_key = response.get('LastEvaluatedKey')
        if not last_evaluated_key:
            break

    return terminated_instances

def cross_check_instances(terminated_instances):
    instances_status_verified = []

    # Fix: Correct handling of instance ID, which might be a string or dictionary.
    instance_ids = [
        instance['InstanceId']['S'] if isinstance(instance.get('InstanceId', ''), dict) else instance.get('InstanceId', '')
        for instance in terminated_instances if 'InstanceId' in instance
    ]

    logger.info(f"Checking status for {len(instance_ids)} instance(s) on EC2...")

    batch_size = 100
    batches = [instance_ids[i:i + batch_size] for i in range(0, len(instance_ids), batch_size)]

    for batch in batches:
        try:
            response = ec2.describe_instance_status(InstanceIds=batch, IncludeAllInstances=True)
            logger.info(f"EC2 Response for batch: {response}")

            for reservation in response.get('InstanceStatuses', []):
                instance_id = reservation['InstanceId']
                ec2_state = reservation['InstanceState']['Name']
                for instance in terminated_instances:
                    if instance.get('InstanceId', {}).get('S', '') == instance_id:
                        instance['EC2State'] = ec2_state
                        instances_status_verified.append(instance)
        except ec2.exceptions.ClientError as e:
            if 'InvalidInstanceID.NotFound' in str(e):
                continue
            else:
                logger.error(f"Error querying EC2 status for batch {batch}: {str(e)}")
                continue

    return instances_status_verified

def remove_terminated_instances_from_dynamodb(terminated_instances):
    for table_name in tables:
        table = dynamodb.Table(table_name)
        with table.batch_writer() as batch:
            for instance in terminated_instances:
                instance_id = instance.get('InstanceId', '')
                if instance_id:
                    batch.delete_item(Key={'InstanceId': instance_id})
                    logger.info(f"Deleted terminated instance {instance_id} from table {table_name}.")

if __name__ == '__main__':
    result = process_terminated_instances()
    print(result)
