import boto3
import os
import json

ec2 = boto3.client('ec2')
sns_client = boto3.client('sns')

# Environment variables
EXCLUDED_SG_IDS = os.environ.get("EXCLUDED_SECURITY_GROUP_IDS", "").split(",")
TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

def lambda_handler(event, context):
    findings = []
    next_token = None

    try:
        while True:
            if next_token:
                response = ec2.describe_security_groups(NextToken=next_token)
            else:
                response = ec2.describe_security_groups()

            for sg in response['SecurityGroups']:
                sg_id = sg['GroupId']
                sg_name = sg.get('GroupName', '')

                if sg_id in EXCLUDED_SG_IDS:
                    continue  # Skip excluded security groups

                for permission in sg.get('IpPermissions', []):
                    from_port = permission.get('FromPort')
                    to_port = permission.get('ToPort')
                    ip_ranges = permission.get('IpRanges', [])

                    # Check if port range includes 22 or 3389
                    if (from_port is not None and to_port is not None) and \
                       (from_port <= 22 <= to_port or from_port <= 3389 <= to_port):
                        for ip_range in ip_ranges:
                            cidr = ip_range.get('CidrIp')
                            if cidr == '0.0.0.0/0':
                                port = 22 if from_port <= 22 <= to_port else 3389
                                findings.append({
                                    'SecurityGroupId': sg_id,
                                    'SecurityGroupName': sg_name,
                                    'Port': port,
                                    'CIDR': cidr
                                })

            next_token = response.get('NextToken')
            if not next_token:
                break

        if findings:
            facts = ""
            for f in findings:
                facts += (
                    f"- Security Group ID: {f['SecurityGroupId']}\n"
                    f"  Security Group Name: {f['SecurityGroupName']}\n"
                    f"  Inbound Port: {f['Port']}\n"
                    f"  Inbound CIDR: {f['CIDR']}\n\n"
                )

            smsmessage = {
                "version": "1.0",
                "source": "custom",
                "content": {
                    "title": "Security Group Open Ports Alert",
                    "description": facts
                }
            }

            print("Sending message:\n", facts)

            response = sns_client.publish(
                TopicArn=TOPIC_ARN,
                Message=json.dumps({'default': json.dumps(smsmessage)}),
                MessageStructure='json'
            )

            print("SNS Response:", response)
            return {'statusCode': 200, 'body': json.dumps('Message sent to SNS!')}

        else:
            print("No open ports (22 or 3389) to the internet were found.")
            return {'statusCode': 200, 'body': json.dumps('No open ports found.')}

    except Exception as e:
        print("Error processing event:", str(e))
        return {'statusCode': 500, 'body': json.dumps('Error processing event')}
