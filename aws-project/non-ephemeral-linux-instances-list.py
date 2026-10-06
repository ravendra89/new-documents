import boto3

# Initialize boto3 clients for EC2 and Auto Scaling
region = 'us-east-1'  # Replace with your desired region
ec2_client = boto3.client('ec2', region_name=region)

def get_all_linux_instances_not_in_asg():
    # Step 1: Describe all instances
    instances = ec2_client.describe_instances()

    linux_instances_not_in_asg = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']

            # Skip instances that are in Auto Scaling Groups
            in_asg = False
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'aws:autoscaling:groupName':
                        in_asg = True
                        break
            if in_asg:
                continue

            # Skip ephemeral/spot instances
            if instance.get('InstanceLifecycle') == 'spot':
                continue  # Only interested in On-Demand or Reserved

            # Skip Windows instances
            # If 'Platform' is not present, assume it's Linux/UNIX
            if instance.get('Platform') == 'windows':
                continue

            # Add the Linux instance
            linux_instances_not_in_asg.append({
                'InstanceId': instance_id,
                'State': instance['State']['Name'],
                'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                'PrivateIP': instance.get('PrivateIpAddress', 'N/A'),
                'InstanceType': instance.get('InstanceType', 'N/A'),
            })

    return linux_instances_not_in_asg

def print_linux_instances(instances):
    if not instances:
        print("No Linux non-ephemeral instances found outside Auto Scaling groups.")
        return

    print(f"\n{'Instance ID':<20} {'State':<15} {'Public IP':<15} {'Private IP':<15} {'Type':<10}")
    print("=" * 80)

    for instance in instances:
        print(f"{instance['InstanceId']:<20} {instance['State']:<15} {instance['PublicIP']:<15} {instance['PrivateIP']:<15} {instance['InstanceType']:<10}")

def main():
    linux_instances = get_all_linux_instances_not_in_asg()
    print_linux_instances(linux_instances)

if __name__ == "__main__":
    main()
