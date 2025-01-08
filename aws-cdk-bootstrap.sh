#!/bin/bash

# Get account and region dynamically
ACCOUNT_NUMBER=$(aws sts get-caller-identity --query "Account" --output text)
REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}

# Define a custom stack name
# CUSTOM_STACK_NAME="TestCDKToolkit"
CUSTOM_STACK_NAME="CDKToolkit"

# Function to create the CDK bootstrap stack
create_bootstrap() {
  if [[ -z "$ACCOUNT_NUMBER" || -z "$REGION" ]]; then
    echo "Error: Unable to determine account or region."
    echo "Ensure AWS CLI is configured or AWS_DEFAULT_REGION is set."
    exit 1
  fi

  echo "Running CDK bootstrap for aws://$ACCOUNT_NUMBER/$REGION with stack name $CUSTOM_STACK_NAME..."
  cdk bootstrap aws://$ACCOUNT_NUMBER/$REGION --toolkit-stack-name $CUSTOM_STACK_NAME

  if [ $? -eq 0 ]; then
    echo "CDK bootstrap completed successfully for aws://$ACCOUNT_NUMBER/$REGION with stack name $CUSTOM_STACK_NAME."
  else
    echo "CDK bootstrap failed for aws://$ACCOUNT_NUMBER/$REGION with stack name $CUSTOM_STACK_NAME." >&2
    exit 1
  fi
}

# Function to delete the CDK bootstrap stack and clean up residual resources
delete_bootstrap() {
  echo "Deleting CDK bootstrap stack $CUSTOM_STACK_NAME in region $REGION..."

  # Get the list of resources from the stack
  BUCKET_NAME=$(aws cloudformation describe-stack-resources --stack-name $CUSTOM_STACK_NAME --region $REGION \
    --query "StackResources[?ResourceType=='AWS::S3::Bucket'].PhysicalResourceId" --output text)

  # Delete objects from the S3 bucket if it exists
  if [[ -n "$BUCKET_NAME" ]]; then
    echo "Found S3 bucket $BUCKET_NAME. Deleting its contents..."
    aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION

    # Delete the bucket itself
    echo "Deleting S3 bucket $BUCKET_NAME..."
    aws s3api delete-bucket --bucket $BUCKET_NAME --region $REGION
  fi

  # Delete the CloudFormation stack
  aws cloudformation delete-stack --stack-name $CUSTOM_STACK_NAME --region $REGION

  # Wait for the stack deletion to complete
  echo "Waiting for stack $CUSTOM_STACK_NAME to be deleted..."
  aws cloudformation wait stack-delete-complete --stack-name $CUSTOM_STACK_NAME --region $REGION

  if [ $? -eq 0 ]; then
    echo "CDK bootstrap stack $CUSTOM_STACK_NAME and associated resources have been deleted successfully."
  else
    echo "Failed to delete stack $CUSTOM_STACK_NAME or its resources." >&2
    exit 1
  fi
}

# Function to check the status of the CDK bootstrap stack
check_bootstrap() {
  echo "Checking status of CDK bootstrap stack $CUSTOM_STACK_NAME in region $REGION..."
  aws cloudformation describe-stacks --stack-name $CUSTOM_STACK_NAME --region $REGION

  if [ $? -eq 0 ]; then
    echo "CDK bootstrap stack $CUSTOM_STACK_NAME exists and is active."
  else
    echo "CDK bootstrap stack $CUSTOM_STACK_NAME does not exist or could not be found." >&2
    exit 1
  fi
}

# Display usage if no arguments are provided
if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <create|delete|check>"
  exit 1
fi

# Execute the appropriate function based on the argument
case "$1" in
create)
  create_bootstrap
  ;;
delete)
  delete_bootstrap
  ;;
check)
  check_bootstrap
  ;;
*)
  echo "Invalid option. Usage: $0 <create|delete|check>"
  exit 1
  ;;
esac
