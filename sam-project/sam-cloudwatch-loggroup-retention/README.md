# SAM Project to deploy cloudwatch-loggroup-retention-process

# sam validate

# SAM Build Commands

sam build

# SAM Deploy Commands

# awsaccountname
sam deploy --config-env awsaccountname-us-east-1
sam deploy --config-env awsaccountname-us-east-2


# Delete
sam delete --stack-name "sam-prod-cloudwatch-loggroup-retention"
#Configurations Needed for new Accounts
For each new account need to add the needed configuraiton in samconfig.toml
Update the following fields: s3_bucket, region
