import boto3

ec2 = boto3.client('ec2')

# 1. Get all security groups
security_groups = ec2.describe_security_groups()['SecurityGroups']

# 2. Get all network interfaces and collect used SGs
used_sg_ids = set()

paginator = ec2.get_paginator('describe_network_interfaces')
for page in paginator.paginate():
    for eni in page['NetworkInterfaces']:
        for group in eni['Groups']:
            used_sg_ids.add(group['GroupId'])

# 3. Print results
print("\nUSED SECURITY GROUPS:")
print("-" * 50)
for sg in security_groups:
    if sg['GroupId'] in used_sg_ids:
        print(f"{sg['GroupId']}  |  {sg['GroupName']}")

print("\nUNUSED SECURITY GROUPS:")
print("-" * 50)
for sg in security_groups:
    if sg['GroupId'] not in used_sg_ids:
        print(f"{sg['GroupId']}  |  {sg['GroupName']}")

