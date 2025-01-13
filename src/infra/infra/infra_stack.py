from pathlib import Path
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    CfnOutput,
    Stack,
    Tags,
)
from constructs import Construct


class FargateServiceStack(Stack):
    """Defines infrastructure for the Hello API Fargate service."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(
            self,
            "HelloApiVpc",
            max_azs=2,  # Provides 2 public and 2 private subnets
            nat_gateways=1,
        )

        # Add tags to VPC
        Tags.of(vpc).add("Environment", "Production")

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "HelloApiCluster", vpc=vpc)

        # Path to the application source
        src_path = Path(__file__).parents[2].joinpath("hello_api")

        if not src_path.exists():
            raise ValueError(f"Invalid source path: {src_path}")
        else:
            print(f"Source path {src_path} exists.")

        # Create a Fargate service with an Application Load Balancer
        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "HelloApiService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(  # noqa: E501
                image=ecs.ContainerImage.from_asset(str(src_path)),
                container_name="HelloApiContainer",
                container_port=8000,
            ),
            task_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            desired_count=2,
        )

        # Configure health check
        service.target_group.configure_health_check(path="/hello/health")

        lb_dns = service.load_balancer.load_balancer_dns_name

        # Add an output for the service endpoint
        CfnOutput(
            self,
            "HelloApiEndpoint",
            value=(f"http://{lb_dns}/hello"),
            description="The endpoint for the Hello API application.",
        )
