# SAM Project to automate s3 bucket tagging on creation
# sam validate

# SAM Build Commands

sam build

# SAM Deploy Commands

# aws account name
sam deploy --config-env awsaccountname-us-east-1

# Delete
sam delete --stack-name "sam-prod-cloudwatch-loggroup-retention"
#Configurations Needed for new Accounts
For each new account need to add the needed configuraiton in samconfig.toml
Update the following fields: s3_bucket, region
