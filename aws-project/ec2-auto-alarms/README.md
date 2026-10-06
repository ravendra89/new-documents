
## Guides

* Base Project for Auto-Alarms

  https://github.com/aws-samples/amazon-cloudwatch-auto-alarms

* SAM Framework

  https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-template-anatomy.html

## Summary
* An EC2 alarm is added when an instance is being created and has the proper alarms.

* For already existing instane, sdd the following tags to an instance to create the alarms:
  ````
  Key, Value
  Create_Auto_Alarms,
  notify, SNS_TOPIC_ARN
  ````

* The value of SNS_TOPIC_ARN depends of the topic where the alerts should be sent to.

* You can manually run the lambda to add the alarms to the instances or wait for the scheuled process that runs once per day.

* Add the following tag to a lambda to create the alarms:
  ````
  Key, Value
  Create_Auto_Alarms,
  notify, SNS_TOPIC_ARN
  ````

* For lambda there's no need to run the main lambda. A lambda alarm is created when the tag Create_Auto_Alarms is added.

## Files in Project

* template.yml
  - The thresholds for cpu, memory and disk space were updated

* cw_auto_alarms.py
  - Script that defines what are the "default" alarms that will be created
  - The alarm for "CPU Credit Balance" was commented
  - The alarm for "Status check" was added
  - The default alarms for disk space were updated to use wildcards so an alarm is created for each disk/volume 

* samconfig.toml
  - It needs to be updated depending on the account/region that the project will be deployed to
  - stack_name   = "sam-auto-alarms"
  - region       = "us-east-1"
  - capabilities = "CAPABILITY_IAM CAPABILITY_NAMED_IAM"
  - s3_bucket    = "ymcareers-devops-sls-projects" (S3 bucket to upload the template)

* You can specify CloudWatch to treat missing data points as any of the following:
  - notBreaching – Missing data points are treated as "good" and within the threshold
  - breaching – Missing data points are treated as "bad" and breaching the threshold
  - ignore – The current alarm state is maintained
  - missing – If all data points in the alarm evaluation range are missing, the alarm transitions to INSUFFICIENT_DATA.

* The SNS Topics were created manually
  - Careers
    - EC2 Prod: arn:aws:sns:us-east-1:590578770109:CloudOps-Notifications
    - EC2 Lower Envs: arn:aws:sns:us-east-1:590578770109:CloudOps-Alerts-Lower-Env
    - Lambda Prod: arn:aws:sns:us-east-1:590578770109:Lambda-Alerts
    - Lambda Lower Envs: arn:aws:sns:us-east-1:590578770109:Lambda-Alerts-Lower-Env

* Leave the parameter AlarmNotificationARN. The notifications are set by the tag "notify"

## Steps to Deploy Project updates

1. Install SAM Cli

    https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html


2. On the file "template.yml" update the parameter AlarmNotificationARN (if needed).
This parameter is the SNS topic where the alarm alerts will be sent.

3. On the console, run 
    ````
    sam build
    ````
    Get the message -> Build Succeeded

4. On the console, run
    ````
    sam deploy --config-env core-apps-us-east-1

    sam delete --stack-name sam-auto-alarms
    ````

## TODO
* The alarm creation fails when the notify tag is not sent
