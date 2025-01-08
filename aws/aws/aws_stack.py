from pathlib import Path
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_elasticloadbalancingv2 as elbv2,
    Stack,
    CfnOutput,
    Duration
)
from constructs import Construct


class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "vpc", max_azs=2)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "fargate-cluster", vpc=vpc)

        # Define the task definition
        task_definition = ecs.FargateTaskDefinition(
            self, "TaskDef",
            cpu=256,
            memory_limit_mib=512
        )

        # Add a container to the task definition
        src_path = Path(__file__).parents[2].joinpath("hello_api")
        if not src_path.exists():
            print(f"path {src_path} does not exist")

        container = task_definition.add_container(
            "app-container",
            image=ecs.ContainerImage.from_asset(str(src_path)),
            container_name="app-container",
            health_check=ecs.HealthCheck(
                command=[
                    "CMD-SHELL", "curl -f http://localhost:8000/hello/health || exit 1"],
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                retries=3,
                start_period=Duration.seconds(10)
            )
        )

        # Add port mappings for the container
        container.add_port_mappings(
            ecs.PortMapping(container_port=8000)
        )

        # Create a Fargate service
        service = ecs.FargateService(
            self, "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            assign_public_ip=True
        )

        # Create an ALB
        lb = elbv2.ApplicationLoadBalancer(
            self, "LB",
            vpc=vpc,
            internet_facing=True
        )

        # Add a listener to the ALB
        listener = lb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        # Attach the service to the listener
        target_group = listener.add_targets(
            "ECS",
            port=8000,
            targets=[service],
            health_check=elbv2.HealthCheck(
                path="/hello/health",
                interval=Duration.seconds(30),
                timeout=Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=2
            )
        )

        # Output the endpoint URL
        CfnOutput(
            self, "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )
