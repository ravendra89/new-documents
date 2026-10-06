import boto3
import datetime
import json

# Initialize the Boto3 clients
s3_client = boto3.client('s3')
sts_client = boto3.client('sts')

def lambda_handler(event, context):
    # Log the entire event to CloudWatch for debugging purposes
    print("Received event: ", json.dumps(event))
    
    # Extract the bucket name from the event
    try:
        # Extract the bucket name from the EventBridge event (CloudTrail event)
        if 'detail' in event and 'requestParameters' in event['detail']:
            bucket_name = event['detail']['requestParameters']['bucketName']
        else:
            raise KeyError("Bucket name not found in event detail")

    except KeyError as e:
        print(f"Error: Missing bucket name in event: {e}")
        raise e

    # Get the AWS account ID (useful for some cases where cross-account info is needed)
    try:
        account_id = sts_client.get_caller_identity()['Account']
    except Exception as e:
        print(f"Error retrieving account ID: {e}")
        raise e

    # Get the user who created the bucket (may need to extract from CloudTrail or use IAM user info)
    created_by = 'unknown'  # Default value for 'created_by'
    try:
        # Check if 'userIdentity' exists and extract the userName from it
        if 'detail' in event and 'userIdentity' in event['detail']:
            user_identity = event['detail']['userIdentity']
            # Prefer 'userName' if available, otherwise fallback to 'arn'
            created_by = user_identity.get('userName', user_identity.get('arn', 'unknown'))
        else:
            print("User identity not found in event.")
    except KeyError as e:
        print(f"Error: 'userIdentity' not found in event: {e}")

    # Current UTC time when the bucket is created
    utc_now = datetime.datetime.utcnow()

    # Format the UTC time to string (in the format: YYYY-MM-DD HH:MM:SS)
    created_date_utc = utc_now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Define the tags to be added
    tags = [
        {'Key': 'CreatedBy', 'Value': created_by},
        {'Key': 'CreatedDate', 'Value': created_date_utc}
    ]

    # Adding tags to the S3 bucket
    try:
        response = s3_client.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={'TagSet': tags}
        )
        print(f"Successfully added tags to bucket {bucket_name}")
    except Exception as e:
        print(f"Error adding tags to bucket {bucket_name}: {e}")
        raise e

