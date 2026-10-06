import boto3

# Initialize boto3 clients for EC2 and Auto Scaling
region = 'us-east-1'  # Replace with your desired region
ec2_client = boto3.client('ec2', region_name=region)
asg_client = boto3.client('autoscaling', region_name=region)

def get_all_windows_instances_not_in_asg():
    # Step 1: List all EC2 instances
    instances = ec2_client.describe_instances()

    # This will hold the details of Windows instances that are not part of any Auto Scaling group
    windows_instances_not_in_asg = []

    # Step 2: Loop through all EC2 instances
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            
            # Step 3: Check if the instance is a Windows instance
            if 'Platform' in instance and instance['Platform'] == 'windows':
                # Step 4: Check if the instance is part of an Auto Scaling group by looking for the AutoScaling group tag
                is_in_asg = False
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'aws:autoscaling:groupName':
                            is_in_asg = True
                            break
                
                # If the instance is not in an Auto Scaling Group, add it to the list
                if not is_in_asg:
                    windows_instances_not_in_asg.append({
                        'InstanceId': instance['InstanceId'],
                        'State': instance['State']['Name'],
                        'PublicIP': instance.get('PublicIpAddress', 'N/A'),
                        'PrivateIP': instance['PrivateIpAddress']
                    })

    return windows_instances_not_in_asg

def print_windows_instances(windows_instances):
    if not windows_instances:
        print("No Windows instances found that do not belong to Auto Scaling groups.")
        return

    print(f"\n{'Instance ID':<20} {'State':<15} {'Public IP':<15} {'Private IP':<15}")
    print("=" * 65)

    for instance in windows_instances:
        print(f"{instance['InstanceId']:<20} {instance['State']:<15} {instance['PublicIP']:<15} {instance['PrivateIP']:<15}")

def main():
    # Step 1: Get list of Windows instances that are not part of Auto Scaling groups
    windows_instances = get_all_windows_instances_not_in_asg()

    # Step 2: Print the results
    print_windows_instances(windows_instances)

if __name__ == "__main__":
    main()

