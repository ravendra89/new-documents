#!/usr/bin/python3.11
import boto3
import json
import os

IdentityStoreId = os.environ.get("IdentityStoreId")
sns_client = boto3.client("sns")
client = boto3.client("identitystore")

SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")


def lambda_handler(event, context):
    print("Event Payload: ")
    print(event)

    try:
        eventName = event["detail"]["eventName"]
        eventID = event["detail"]["eventID"]

        if eventName == "AddMemberToGroup":
            userId = event["detail"]["requestParameters"]["member"]["memberId"]
        elif eventName == "RemoveMemberFromGroup":
            userId = event["detail"]["requestParameters"]["memberId"]
        else:
            print("Unsupported event: " + eventName)
            return False

        response = client.describe_user(IdentityStoreId=IdentityStoreId, UserId=userId)
        print("User details: ")
        print(response)
        if "UserName" not in response:
            print("The username not found.")
            return False
        userName = response["UserName"]

        groupId = event["detail"]["requestParameters"]["groupId"]
        response = client.describe_group(
            IdentityStoreId=IdentityStoreId, GroupId=groupId
        )
        print("Group details: ")
        print(response)
        if "DisplayName" not in response:
            print("The group name not found.")
            return False
        groupName = response["DisplayName"]

        messageDict = {
            "eventID": eventID,
            "eventName": eventName,
            "userId": userId,
            "userName": userName,
            "groupId": groupId,
            "groupName": groupName,
        }
        snsMessage = {
            "version": "1.0",
            "source": "custom",
            "content": {
                "title": "Okta - IAM Identity Center Notification",
                "description": json.dumps(messageDict),
            },
        }
        print("Sending message:", snsMessage)

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps({"default": json.dumps(snsMessage)}),
            MessageStructure="json",
        )
        print("SNS Response: ", response)

        return True
    except Exception as e:
        print(e)
        return False

