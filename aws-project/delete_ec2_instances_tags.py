import boto3
from botocore.exceptions import ClientError

# Set your target region
region = 'us-east-1'

# Tag key to match and remove (value doesn't matter)
tag_key_to_remove = 'Create_Auto_Alarms'

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name=region)

# Describe instances
response = ec2.describe_instances()

# Loop and remove tag if key matches (value doesn't matter)
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        tags = instance.get('Tags', [])

        for tag in tags:
            if tag['Key'] == tag_key_to_remove:
                print(f"Removing tag '{tag_key_to_remove}' from instance {instance_id}")
                try:
                    ec2.delete_tags(
                        Resources=[instance_id],
                        Tags=[{'Key': tag_key_to_remove}]
                        # dry_run=True  # Uncomment for safe testing
                    )
                except ClientError as e:
                    print(f"Error removing tag from {instance_id}: {e}")
                break  # Done with this instance

