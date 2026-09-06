"""
Networking Stack - VPC with three-tier subnet configuration

Creates the foundation VPC infrastructure with:
- Public subnets for load balancers
- Private subnets with NAT for application servers  
- Isolated subnets for databases
"""

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct


class NetworkingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC with three-tier subnet configuration
        self.vpc = ec2.Vpc(
            self,
            "ThreeTierVpc",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,  # Deploy across 2 availability zones
            nat_gateways=1,  # Single NAT gateway for cost savings
            subnet_configuration=[
                # Public tier - for load balancers, NAT gateways
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,  # 10.0.0.0/24, 10.0.1.0/24
                ),
                # Private tier - for application servers
                ec2.SubnetConfiguration(
                    name="Application",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=20,  # 10.0.16.0/20, 10.0.32.0/20
                ),
                # Isolated tier - for databases (no internet access)
                ec2.SubnetConfiguration(
                    name="Database",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24,  # 10.0.2.0/24, 10.0.3.0/24
                ),
            ],
        )
