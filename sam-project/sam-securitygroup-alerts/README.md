# SAM Commands For The Deployment Of SecurityGroup Alerts.
# sam validate
# SAM Build Commands

sam build

# awsaccountname

# awsaccountname
sam deploy --config-env awsaccountname-us-east-1

# Delete
sam delete --stack-name Sam-Prod-SecurityGroup-Alerts
#Configurations Needed for new Accounts
For each new account need to add the needed configuraiton in samconfig.toml
Update the following fields: s3_bucket, region
