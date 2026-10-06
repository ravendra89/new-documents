import boto3
import csv

regions = ['us-east-1'] 

output_file = 'ec2_instance_tags.csv'
csv_headers = ['Region', 'InstanceId', 'TagKey', 'TagValue']

with open(output_file, mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_headers)

    for region in regions:
        print(f"Checking region: {region}")
        ec2 = boto3.client('ec2', region_name=region)

        response = ec2.describe_instances()

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                tags = instance.get('Tags', [])

                if tags:
                    for tag in tags:
                        writer.writerow([region, instance_id, tag['Key'], tag['Value']])
                else:
                    writer.writerow([region, instance_id, '', ''])

print(f"Done. EC2 tag information saved to: {output_file}")

