import boto3
import csv
from datetime import datetime

# Initialize boto3 clients
ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

def get_asg_instances():
    # Get all Auto Scaling groups
    asg_response = asg_client.describe_auto_scaling_groups()

    # Collect all instance IDs in ASGs
    asg_instance_ids = []
    for asg in asg_response['AutoScalingGroups']:
        for instance in asg['Instances']:
            asg_instance_ids.append(instance['InstanceId'])

    if not asg_instance_ids:
        print("No ASG instances found.")
        return

    # Split instance IDs (describe_instances supports up to 1000 at once)
    def chunks(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    instance_details = []
    for chunk in chunks(asg_instance_ids, 1000):
        ec2_response = ec2_client.describe_instances(InstanceIds=chunk)
        for reservation in ec2_response['Reservations']:
            for instance in reservation['Instances']:
                # Determine platform type
                platform = instance.get('Platform')
                if platform == 'windows':
                    platform_type = 'Windows'
                else:
                    platform_type = 'Linux/UNIX'

                instance_data = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'Platform': platform_type,
                    'State': instance['State']['Name'],
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'LaunchTime': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                }
                instance_details.append(instance_data)

    # Save to CSV
    if instance_details:
        with open('ephemeral_asg_ec2_instances.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=instance_details[0].keys())
            writer.writeheader()
            for instance in instance_details:
                writer.writerow(instance)
        print(f"Data of ASG-based EC2 instances has been saved to 'ephemeral_asg_ec2_instances.csv'")
    else:
        print("No ASG instances found.")

if __name__ == '__main__':
    get_asg_instances()
