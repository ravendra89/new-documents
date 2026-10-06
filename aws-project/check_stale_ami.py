import boto3
import csv
from datetime import datetime, timedelta
import pytz

# Create EC2 and Auto Scaling clients
ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

# Function to get the list of AMIs
def get_amis():
    amis = []
    paginator = ec2_client.get_paginator('describe_images')
    for page in paginator.paginate(Owners=['self']):
        amis.extend(page.get('Images', []))
    print(f"Total AMIs retrieved: {len(amis)}")
    return amis

# Function to filter out AMIs older than 168 days
def filter_old_amis(amis):
    current_time = datetime.now(pytz.UTC)
    old_amis = []

    for ami in amis:
        creation_date = ami.get('CreationDate')
        if creation_date:
            resource_date = datetime.strptime(creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
            resource_date = pytz.UTC.localize(resource_date)

            # Convert UTC to IST
            ist_timezone = pytz.timezone('Asia/Kolkata')
            resource_date_ist = resource_date.astimezone(ist_timezone)

            # If older than 168 days
            if current_time - resource_date > timedelta(days=162):
                old_amis.append({
                    'Resource ID': ami['ImageId'],
                    'Creation Date (IST)': resource_date_ist.strftime("%Y-%m-%d %H:%M:%S"),
                    'Name': ami.get('Name', 'N/A')
                })

    return old_amis

# Function to check if the AMI is used by EC2 instances
def is_ami_used_by_ec2(ami_id):
    instances = ec2_client.describe_instances(Filters=[{
        'Name': 'image-id',
        'Values': [ami_id]
    }])
    return len(instances['Reservations']) > 0

# Function to check if the AMI is used by Auto Scaling groups
def is_ami_used_by_asg(ami_id):
    asg_groups = asg_client.describe_auto_scaling_groups()

    for group in asg_groups['AutoScalingGroups']:
        if group.get('LaunchConfigurationName'):
            lc = asg_client.describe_launch_configurations(
                LaunchConfigurationNames=[group['LaunchConfigurationName']]
            )
            for lc_item in lc['LaunchConfigurations']:
                if lc_item.get('ImageId') == ami_id:
                    return True
        if group.get('LaunchTemplate'):
            if group['LaunchTemplate']['Version'] == 'Latest':
                lt = asg_client.describe_launch_templates(
                    LaunchTemplateNames=[group['LaunchTemplate']['LaunchTemplateName']]
                )
                for lt_item in lt['LaunchTemplateVersions']:
                    if lt_item['LaunchTemplateData'].get('ImageId') == ami_id:
                        return True
    return False

# Function to remove AMIs that are currently in use
def filter_unused_amis(old_amis):
    unused_amis = []
    for ami in old_amis:
        ami_id = ami['Resource ID']
        if not is_ami_used_by_ec2(ami_id) and not is_ami_used_by_asg(ami_id):
            unused_amis.append(ami)
        else:
            print(f"AMI {ami_id} is in use and will be skipped.")
    return unused_amis

# Function to save the result to a CSV file
def save_to_csv(amis):
    with open('old_unused_amis.csv', mode='w', newline='') as file:
        fieldnames = ['Resource ID', 'Creation Date (IST)', 'Name']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for ami in amis:
            writer.writerow(ami)

# Main function
def main():
    amis = get_amis()
    old_amis = filter_old_amis(amis)
    print(f"Found {len(old_amis)} AMIs older than 6 months.")

    unused_amis = filter_unused_amis(old_amis)
    print(f"{len(unused_amis)} of them are unused.")

    save_to_csv(unused_amis)
    print("Results saved to old_unused_amis.csv.")

if __name__ == "__main__":
    main()
