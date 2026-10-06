import boto3
import csv

# Initialize EC2 and AutoScaling client
ec2_client = boto3.client('ec2')
autoscaling_client = boto3.client('autoscaling')

# Function to get the list of all Windows instances
def get_windows_instances():
    # Fetch all instances
    instances = ec2_client.describe_instances()

    # Prepare to store instance details
    windows_instances = []

    # Loop through all reservations and instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            # Check if the instance is running and is Windows
            if instance.get('Platform') == 'windows':  # Filters only Windows instances
                instance_id = instance['InstanceId']
                instance_name = 'N/A'  # Default value if no Name tag is present

                # Get the instance name from the tags (if available)
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            instance_name = tag['Value']
                            break

                # Get the instance type, private and public IPs, and state
                instance_type = instance['InstanceType']
                private_ip = instance.get('PrivateIpAddress', 'N/A')
                public_ip = instance.get('PublicIpAddress', 'N/A')
                state = instance['State']['Name']
                platform = instance.get('Platform', 'N/A')

                # Check if the instance belongs to an AutoScaling Group
                autoscaling_group = get_autoscaling_group(instance_id)

                # Add instance information to the list
                windows_instances.append({
                    'InstanceId': instance_id,
                    'InstanceName': instance_name,
                    'InstanceType': instance_type,
                    'PrivateIP': private_ip,
                    'PublicIP': public_ip,
                    'State': state,
                    'Platform': platform,
                    'AutoScalingGroup': autoscaling_group
                })

    # Return the list of Windows instances
    return windows_instances

# Function to get AutoScaling Group for an instance
def get_autoscaling_group(instance_id):
    response = autoscaling_client.describe_auto_scaling_instances(InstanceIds=[instance_id])
    # Check if the instance belongs to an Auto Scaling Group
    if response['AutoScalingInstances']:
        return response['AutoScalingInstances'][0].get('AutoScalingGroupName', 'N/A')
    return 'N/A'  # Return 'N/A' if not part of an Auto Scaling Group

# Function to write instance details to a CSV file
def write_to_csv(instances, filename='windows_instances.csv'):
    # Define the CSV column headers
    headers = ['InstanceId', 'InstanceName', 'InstanceType', 'PrivateIP', 'PublicIP', 'State', 'Platform', 'AutoScalingGroup']

    # Open the CSV file in write mode
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write each instance's details
        for instance in instances:
            writer.writerow(instance)

    print(f"Data has been written to {filename}")

# Get all Windows instances
windows_instances = get_windows_instances()

# Write the Windows instances details to a CSV file
write_to_csv(windows_instances)


