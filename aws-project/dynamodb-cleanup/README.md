# SAM Project Dynampdb Cleanup
The resources are defined in the template.yaml file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

# Generate and Update the image
<!-- Push code updates in the file "utilities\dynamo-cleanup\remove-old-records.py" to the careers repo

1.1 Update the branch name (line 31) in the Dockerfile "terraform\dynamo-cleanup\image-builder\Dockerfile" if needed

Generate new image in Image Builder

1.2 Select the Image Builder pipeline "DYNAMO-CLEANUP-PIPELINE"

1.3 Select "Actions" -> "Run Pipeline"

1.4 Wait for image to get created and pushed to ECR "dynamo-cleanup"

1.5 Go to the ECR repository "dynamo-cleanup"

1.6 Copy the URI of the latest image

1.7 Update the file "terraform\DYNAMODB-CLEANUP\aws-batch\dynamo_cleanup_job.json" -->

# Build the docker image for application and Push to ECR ( Apply this process when building docker image manually)
Update the file "DYNAMODB-CLEANUP\aws-batch\dynamo_cleanup_job.json"


# Apply the Batch Terraform infra changes

# Update the State Machine Job Definition/queues to point to the new version

2.1 Go to AWS Batch Job definitions/queues

2.3 Select the definition/queues

2.4 Copy the ARN

2.5 Update the value of "JobDefinitionArn" and "JobQueueArn" in the file "aws-sam\DYNAMODB-CLEANUP\template.yaml"

# Deploy the SAM app

Test running Step Function "Step Function Name"

Enable EventBridge schedule rule that is disabled by default

# Deploy the application
The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. If needed, the deploy parameters need to be updated in the samconfig.toml file.

# To use the SAM CLI, you need the following tools.

SAM CLI - Install the SAM CLI
Python 3 installed

# To build and deploy your application, run the following in your shell:

sam build
sam deploy --config-env prod

# Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in the SAM specification, you can use standard AWS CloudFormation resource types.

# Cleanup
To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

sam delete --stack-name SAM-STAGING-AD-SERVERS-DYNAMODB-CLEANUP