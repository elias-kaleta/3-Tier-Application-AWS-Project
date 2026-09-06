#!/usr/bin/env python3
"""
3-Tier Web Application CDK App

This app deploys a complete three-tier web application architecture:
- Presentation Tier: CloudFront + ALB
- Application Tier: Auto Scaling EC2 instances
- Data Tier: RDS Multi-AZ database

Deploy with: cdk deploy --all
"""

from aws_cdk import App, Environment
from stacks.networking_stack import NetworkingStack
from stacks.database_stack import DatabaseStack
from stacks.application_stack import ApplicationStack
from stacks.frontend_stack import FrontendStack
from stacks.monitoring_stack import MonitoringStack

# Create CDK app
app = App()

# Define environment (optional - uses default credentials if not specified)
# env = Environment(
#     account="123456789012",
#     region="us-east-1"
# )

# 1. Networking Foundation - VPC with three subnet tiers
networking_stack = NetworkingStack(
    app,
    "NetworkingStack",
    description="VPC infrastructure with public, private, and isolated subnets",
    # env=env,
)

# 2. Data Tier - RDS Multi-AZ database in isolated subnets
database_stack = DatabaseStack(
    app,
    "DatabaseStack",
    vpc=networking_stack.vpc,
    description="RDS MySQL database with Multi-AZ deployment",
    # env=env,
)
database_stack.add_dependency(networking_stack)

# 3. Application Tier - EC2 Auto Scaling Group in private subnets
application_stack = ApplicationStack(
    app,
    "ApplicationStack",
    vpc=networking_stack.vpc,
    db_security_group=database_stack.db_security_group,
    db_endpoint=database_stack.db_endpoint,
    db_secret_arn=database_stack.db_secret_arn,
    description="Application servers with Auto Scaling",
    # env=env,
)
application_stack.add_dependency(database_stack)

# 4. Presentation Tier - ALB and CloudFront in public subnets
frontend_stack = FrontendStack(
    app,
    "FrontendStack",
    vpc=networking_stack.vpc,
    target_group=application_stack.target_group,
    app_security_group=application_stack.app_security_group,
    description="Application Load Balancer and CloudFront CDN",
    # env=env,
)
frontend_stack.add_dependency(application_stack)

# 5. Monitoring - CloudWatch dashboards and alarms
monitoring_stack = MonitoringStack(
    app,
    "MonitoringStack",
    alb=frontend_stack.alb,
    target_group=application_stack.target_group,
    asg=application_stack.asg,
    database=database_stack.database,
    description="CloudWatch monitoring and alarms",
    # env=env,
)
monitoring_stack.add_dependency(frontend_stack)

# Synthesize CloudFormation templates
app.synth()
