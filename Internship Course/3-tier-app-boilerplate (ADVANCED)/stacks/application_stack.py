"""
Application Stack - EC2 Auto Scaling Group

Creates application tier with:
- EC2 instances in private subnets
- Auto Scaling based on CPU utilization
- IAM roles for AWS service access
- User data script to run Flask application
"""

from aws_cdk import Stack, Duration
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct


class ApplicationStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        db_security_group: ec2.ISecurityGroup,
        db_endpoint: str,
        db_secret_arn: str,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Security group for application instances
        self.app_security_group = ec2.SecurityGroup(
            self,
            "AppSecurityGroup",
            vpc=vpc,
            description="Security group for application servers",
            allow_all_outbound=True,
        )

        # Allow application tier to connect to database
        db_security_group.add_ingress_rule(
            peer=self.app_security_group,
            connection=ec2.Port.tcp(3306),
            description="MySQL from application tier",
        )

        # IAM role for EC2 instances
        instance_role = iam.Role(
            self,
            "AppInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                # Allow SSM Session Manager access (no SSH keys needed)
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                # Allow CloudWatch logs and metrics
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchAgentServerPolicy"
                ),
            ],
        )

        # Grant read access to database secret
        db_secret = secretsmanager.Secret.from_secret_complete_arn(
            self, "DBSecret", db_secret_arn
        )
        db_secret.grant_read(instance_role)

        # User data script - runs on instance launch
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "#!/bin/bash",
            "yum update -y",
            "yum install -y python3 python3-pip mysql",
            
            # Install application dependencies
            "pip3 install flask pymysql boto3",
            
            # Create application directory
            "mkdir -p /opt/app",
            
            # Simple Flask application
            "cat > /opt/app/app.py << 'EOF'",
            "from flask import Flask, jsonify",
            "import os",
            "import json",
            "import boto3",
            "import pymysql",
            "",
            "app = Flask(__name__)",
            "",
            "# Get DB credentials from Secrets Manager",
            "def get_db_connection():",
            "    secrets_client = boto3.client('secretsmanager')",
            f"    secret = secrets_client.get_secret_value(SecretId='{db_secret_arn}')",
            "    creds = json.loads(secret['SecretString'])",
            "    ",
            "    connection = pymysql.connect(",
            f"        host='{db_endpoint}',",
            "        user=creds['username'],",
            "        password=creds['password'],",
            "        database=creds['dbname'],",
            "        cursorclass=pymysql.cursors.DictCursor",
            "    )",
            "    return connection",
            "",
            "@app.route('/health')",
            "def health():",
            "    return jsonify({'status': 'healthy'}), 200",
            "",
            "@app.route('/')",
            "def index():",
            "    try:",
            "        conn = get_db_connection()",
            "        cursor = conn.cursor()",
            "        cursor.execute('SELECT VERSION() as version')",
            "        result = cursor.fetchone()",
            "        conn.close()",
            "        return jsonify({",
            "            'message': 'Connected to database!',",
            "            'database_version': result['version']",
            "        })",
            "    except Exception as e:",
            "        return jsonify({'error': str(e)}), 500",
            "",
            "if __name__ == '__main__':",
            "    app.run(host='0.0.0.0', port=80)",
            "EOF",
            
            # Start application
            "nohup python3 /opt/app/app.py > /var/log/app.log 2>&1 &",
        )

        # Launch template for EC2 instances
        launch_template = ec2.LaunchTemplate(
            self,
            "AppLaunchTemplate",
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,  # Free tier eligible
            ),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            role=instance_role,
            security_group=self.app_security_group,
            user_data=user_data,
        )

        # Auto Scaling Group
        self.asg = autoscaling.AutoScalingGroup(
            self,
            "AppAutoScalingGroup",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name="Application"  # Private subnets
            ),
            launch_template=launch_template,
            min_capacity=2,  # Always run at least 2 instances
            max_capacity=6,  # Can scale up to 6 instances
            desired_capacity=2,
            health_check=autoscaling.HealthCheck.elb(
                grace=Duration.minutes(5)
            ),
        )

        # Scale based on CPU utilization
        self.asg.scale_on_cpu_utilization(
            "CpuScaling",
            target_utilization_percent=70,
        )

        # Create target group for ALB
        self.target_group = elbv2.ApplicationTargetGroup(
            self,
            "AppTargetGroup",
            vpc=vpc,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[self.asg],
            health_check=elbv2.HealthCheck(
                path="/health",
                interval=Duration.seconds(30),
                healthy_threshold_count=2,
                unhealthy_threshold_count=3,
            ),
        )
