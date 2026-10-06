import boto3
import csv
from datetime import datetime

# Initialize boto3 clients for EC2 and Auto Scaling
ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

def get_instances_not_in_asg():
    # Retrieve all EC2 instances
    response = ec2_client.describe_instances()

    # Get all Auto Scaling groups
    asg_response = asg_client.describe_auto_scaling_groups()

    # Create a set of instance IDs that are part of an Auto Scaling group
    asg_instance_ids = set()
    for asg in asg_response['AutoScalingGroups']:
        for instance in asg['Instances']:
            asg_instance_ids.add(instance['InstanceId'])

    # Prepare a list to hold instance details
    non_asg_instances = []

    # Loop through EC2 instances and collect data for non-ASG instances
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            # Check if the instance is not part of an Auto Scaling group
            if instance_id not in asg_instance_ids:
                # Determine platform type
                platform = instance.get('Platform')
                if platform == 'windows':
                    platform_type = 'Windows'
                else:
                    platform_type = 'Linux/UNIX'  # Default if no 'Platform' key present

                instance_data = {
                    'InstanceId': instance_id,
                    'InstanceType': instance['InstanceType'],
                    'Platform': platform_type,
                    'State': instance['State']['Name'],
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                }
                non_asg_instances.append(instance_data)

    # Write the data to a CSV file
    if non_asg_instances:
        with open('non_ephemeral_ec2_instances.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=non_asg_instances[0].keys())
            writer.writeheader()
            for instance in non_asg_instances:
                writer.writerow(instance)
        print(f"Data of non-ephemeral EC2 instances has been saved to 'non_ephemeral_ec2_instances.csv'")
    else:
        print("No non-ASG instances found.")

if __name__ == '__main__':
    get_instances_not_in_asg()

