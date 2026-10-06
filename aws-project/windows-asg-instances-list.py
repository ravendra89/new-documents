import boto3

# Initialize boto3 clients for EC2 and Auto Scaling
region = 'us-east-2'  # Replace with your desired region
ec2_client = boto3.client('ec2', region_name=region)
asg_client = boto3.client('autoscaling', region_name=region)

def get_windows_instances_in_asg():
    # Step 1: Fetch all Auto Scaling Groups
    asgs = asg_client.describe_auto_scaling_groups()
    
    # This will hold the details of Windows instances behind Auto Scaling groups
    windows_instances = []

    # Step 2: Loop through Auto Scaling Groups to get instance IDs
    for asg in asgs['AutoScalingGroups']:
        asg_name = asg['AutoScalingGroupName']
        print(f"Checking Auto Scaling Group: {asg_name}")

        for instance in asg['Instances']:
            instance_id = instance['InstanceId']
            lifecycle_state = instance['LifecycleState']

            # Step 3: Get instance details for the instance ID
            response = ec2_client.describe_instances(InstanceIds=[instance_id])

            # Step 4: Check if the instance is a Windows instance
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    if 'Platform' in instance and instance['Platform'] == 'windows':
                        windows_instances.append({
                            'InstanceId': instance['InstanceId'],
                            'State': instance['State']['Name'],
                            'AutoScalingGroup': asg_name,
                            'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                            'PrivateIP': instance['PrivateIpAddress']
                        })

    return windows_instances

def print_windows_instances(windows_instances):
    if not windows_instances:
        print("No Windows instances found behind Auto Scaling groups.")
        return

    print(f"\n{'Instance ID':<20} {'State':<15} {'Auto Scaling Group':<30} {'Public IP':<15} {'Private IP':<15}")
    print("=" * 95)

    for instance in windows_instances:
        print(f"{instance['InstanceId']:<20} {instance['State']:<15} {instance['AutoScalingGroup']:<30} {instance['PublicIP']:<15} {instance['PrivateIP']:<15}")

def main():
    # Step 1: Get list of Windows instances in Auto Scaling groups
    windows_instances = get_windows_instances_in_asg()

    # Step 2: Print the results
    print_windows_instances(windows_instances)

if __name__ == "__main__":
    main()

