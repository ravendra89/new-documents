import json
import boto3

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))  # Log the full event for debugging

    # Extract event details
    if "detail" in event and "eventName" in event["detail"]:
        ctevent = event["detail"]["eventName"]
        facts = {
            "Event": ctevent,
            "Region": event["detail"].get("awsRegion"),
            "User": event["detail"]["userIdentity"]["arn"].split('/')[-1],
            "Time": event["detail"].get("eventTime"),
            "SourceIp": event["detail"].get("sourceIPAddress")
        }
    else:
        print("Event does not contain required detail.")
        return {'statusCode': 400, 'body': json.dumps('Invalid event structure')}

    try:
        ec2_client = boto3.client('ec2', region_name=facts["Region"])

        if ctevent == "CreateSecurityGroup":
            SecGroup_ID = event["detail"]["responseElements"].get("groupId")
            facts["Security Group ID"] = SecGroup_ID

            # Fetch the security group details
            response = ec2_client.describe_security_groups(GroupIds=[SecGroup_ID])
            security_group = response["SecurityGroups"][0] if response["SecurityGroups"] else {}
            facts["Security Group Name"] = security_group.get("GroupName")
            facts["Security Group Description"] = security_group.get("Description")

            print(f"Security Group created: {facts}")

        elif ctevent in ["DeleteSecurityGroup", "RevokeSecurityGroupIngress", "AuthorizeSecurityGroupIngress"]:
            SecGroup_ID = event["detail"]["requestParameters"].get("groupId")
            facts["Security Group ID"] = SecGroup_ID

            if ctevent == "DeleteSecurityGroup":
                facts["Action"] = "Deleted"
                print(f"Security Group deleted: {facts}")
            elif ctevent == "RevokeSecurityGroupIngress":
                # Fetch the security group details for rule revocation
                response = ec2_client.describe_security_groups(GroupIds=[SecGroup_ID])
                security_group = response["SecurityGroups"][0] if response["SecurityGroups"] else {}
                facts["Security Group Name"] = security_group.get("GroupName")
                facts["Security Group Description"] = security_group.get("Description")

                # Additional information about the rule being revoked
                IpPermissions = event["detail"]["requestParameters"].get("ipPermissions")
                facts["IpPermissions"] = json.dumps(IpPermissions).replace('\n', '') if IpPermissions else "None"
                print(f"Security Group rule revoked: {facts}")
            elif ctevent == "AuthorizeSecurityGroupIngress":
                # Fetch the security group details for rule addition
                response = ec2_client.describe_security_groups(GroupIds=[SecGroup_ID])
                security_group = response["SecurityGroups"][0] if response["SecurityGroups"] else {}
                facts["Security Group Name"] = security_group.get("GroupName")
                facts["Security Group Description"] = security_group.get("Description")

                # Additional information about the rule being added
                IpPermissions = event["detail"]["requestParameters"].get("ipPermissions")
                facts["IpPermissions"] = json.dumps(IpPermissions).replace('\n', '') if IpPermissions else "None"
                print(f"Security Group rule added: {facts}")

        else:
            print(f"Ignored event: {ctevent}")
            return {'statusCode': 200, 'body': 'Event type ignored'}

        # Prepare and send the SNS message
        message = str(facts).replace('\n', '')  # Remove newline characters from the main message
        smsmessage = {
            "version": "1.0",
            "source": "custom",
            "content": {
                "title": "Security Group Notification",
                "description": message
            }
        }

        print("Sending message:", smsmessage)

        topic_arn = 'sns_topic_arn'  # Replace with your SNS topic ARN
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=json.dumps({'default': json.dumps(smsmessage)}),
            MessageStructure='json'
        )
        print("SNS Response:", response)

    except Exception as e:
        print("Error processing event:", str(e))
        return {'statusCode': 500, 'body': json.dumps('Error processing event')}

    return {'statusCode': 200, 'body': json.dumps('Message sent to SNS!')}

