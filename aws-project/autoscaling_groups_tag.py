import boto3
import csv

def get_autoscaling_groups_with_notify_tag():
    client = boto3.client('autoscaling')

    paginator = client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate()

    groups_with_notify_tag = []

    for page in page_iterator:
        for group in page['AutoScalingGroups']:
            tags = group.get('Tags', [])
            for tag in tags:
                if tag.get('Key') == 'notify':
                    groups_with_notify_tag.append(group['AutoScalingGroupName'])
                    break  # Found the tag, no need to check others

    return groups_with_notify_tag

def save_to_csv(group_names, filename="notify_autoscaling_groups.csv"):
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AutoScalingGroupName'])
        for name in group_names:
            writer.writerow([name])
    print(f"Saved {len(group_names)} group(s) to {filename}")

if __name__ == "__main__":
    matching_groups = get_autoscaling_groups_with_notify_tag()
    if matching_groups:
        print("Auto Scaling Groups with 'notify' tag found:")
        for name in matching_groups:
            print(f" - {name}")
        save_to_csv(matching_groups)
    else:
        print("No Auto Scaling Groups found with the 'notify' tag.")
