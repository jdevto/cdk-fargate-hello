#!/usr/bin/env python3
import aws_cdk as cdk
from infra.infra_stack import FargateServiceStack

# Initialize the CDK application
app = cdk.App()

# Instantiate the stack with appropriate logical and physical names
FargateServiceStack(
    app,
    "InfraStack",  # Logical ID of the stack
    stack_name="hello-api",  # Physical name used in AWS
)

# Synthesize the CloudFormation template
app.synth()
