# cdk-fargate-hello

## CDK Bootstrap Script

This script automates the creation, deletion, and status check of the AWS CDK bootstrap stack. It dynamically determines the AWS account and region, allowing seamless integration with AWS environments. It also supports the use of existing AWS credentials or assumes a role if provided.

### Features

- **Create**: Bootstraps the AWS environment for CDK deployments with a custom stack name.
- **Delete**: Removes the CDK bootstrap stack and associated resources.
- **Check**: Verifies the existence and status of the CDK bootstrap stack.
- **Role Assumption**: Supports execution using a specified IAM Role ARN.
- **Validation**: Ensures AWS credentials are set either through environment variables or role assumption.

### Prerequisites

- **AWS CLI**: Installed and configured on your system.
- **AWS CDK**: Installed globally using Node.js (`npm install -g aws-cdk`).
- Sufficient IAM permissions to:
  - Create and delete CloudFormation stacks.
  - Manage resources like S3 buckets.

### Usage

#### Syntax

```bash
./script.sh <create|delete|check> [role-arn]
```

#### Parameters

- `<create|delete|check>`: The operation to perform:
  - `create`: Creates the CDK bootstrap stack.
  - `delete`: Deletes the CDK bootstrap stack.
  - `check`: Checks the status of the CDK bootstrap stack.
- `[role-arn]` (Optional): The ARN of the IAM role to assume for execution. If not provided, the script uses existing AWS environment variables.

#### Examples

##### Create the CDK Bootstrap Stack

Using existing AWS credentials:

```bash
./script.sh create
```

Assuming an IAM role:

```bash
./script.sh create arn:aws:iam::123456789012:role/MyRole
```

##### Delete the CDK Bootstrap Stack

Using existing AWS credentials:

```bash
./script.sh delete
```

Assuming an IAM role:

```bash
./script.sh delete arn:aws:iam::123456789012:role/MyRole
```

##### Check the CDK Bootstrap Stack Status

Using existing AWS credentials:

```bash
./script.sh check
```

Assuming an IAM role:

```bash
./script.sh check arn:aws:iam::123456789012:role/MyRole
```

### Environment Variables

- `AWS_ACCESS_KEY_ID`: The access key for AWS.
- `AWS_SECRET_ACCESS_KEY`: The secret key for AWS.
- `AWS_SESSION_TOKEN`: The session token for AWS (if using temporary credentials).
- `AWS_DEFAULT_REGION`: The default AWS region.

### Error Handling

- The script exits with an error message if:
  - Required AWS credentials are not set.
  - The provided role ARN is invalid or cannot be assumed.
  - The CloudFormation stack operation fails.

### Notes

- For resources like S3 buckets that are not automatically cleaned up by CloudFormation, manual deletion may be required after running the `delete` operation.
- The script is idempotent, meaning you can safely rerun it without unintended side effects.

### License

This script is provided "as-is" without warranty of any kind. Use at your own risk.
