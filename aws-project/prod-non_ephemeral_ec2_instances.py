import boto3
import csv
from datetime import datetime

# Initialize boto3 clients
ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

def get_prod_non_asg_instances():
    # Retrieve all EC2 instances
    response = ec2_client.describe_instances()

    # Get all Auto Scaling groups
    asg_response = asg_client.describe_auto_scaling_groups()

    # Collect all ASG-managed instance IDs
    asg_instance_ids = {
        instance['InstanceId']
        for asg in asg_response['AutoScalingGroups']
        for instance in asg['Instances']
    }

    prod_non_asg_instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            # Skip instances that are part of ASG
            if instance_id in asg_instance_ids:
                continue

            # Check for 'Environment' tag set to 'prod'
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            if tags.get('Environment', '').lower() != 'prod':
                continue

            # Collect relevant instance details
            instance_data = {
                'InstanceId': instance_id,
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
            }
            prod_non_asg_instances.append(instance_data)

    # Export to CSV if any instances match
    if prod_non_asg_instances:
        with open('prod_non_ephemeral_ec2_instances.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=prod_non_asg_instances[0].keys())
            writer.writeheader()
            for instance in prod_non_asg_instances:
                writer.writerow(instance)

        print("Data of 'prod' non-ephemeral EC2 instances has been saved to 'prod_non_ephemeral_ec2_instances.csv'")
    else:
        print("No 'prod' non-ephemeral EC2 instances found.")

if __name__ == '__main__':
    get_prod_non_asg_instances()

