---
tags:
  - compute
  - auto-scaling
  - application-tier
---

# Application Tier - Auto Scaling Group

EC2 instances running the application logic, deployed in private subnets with Auto Scaling for elasticity and fault tolerance.

## Code

```python
from aws_cdk import Stack, Duration
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
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
        from aws_cdk import aws_secretsmanager as secretsmanager
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
```

## What's Happening

### Security Groups

**Application Security Group**:
- Allows all outbound traffic (needs to reach database, Secrets Manager, package repos)
- Inbound rules added by ALB in the presentation tier
- Adds ingress rule to database security group (principle: source controls access)

### IAM Role and Permissions

**Instance Role** provides:
- **SSM Session Manager**: Connect to instances without SSH keys or bastion hosts
- **CloudWatch Agent**: Send custom metrics and logs
- **Secrets Manager**: Read database credentials

This follows **least privilege** - only the permissions needed for the application to function.

### User Data Script

Runs once at instance launch:

1. Updates packages
2. Installs Python, pip, MySQL client
3. Installs Flask web framework and dependencies
4. Creates a simple Flask app that:
   - Exposes `/health` endpoint for load balancer checks
   - Connects to RDS using Secrets Manager credentials
   - Returns database version on root path

**Production Pattern**: Use AWS CodeDeploy or custom AMIs instead of user data for faster launches and version control.

### Launch Template

Defines the EC2 configuration:
- **t3.micro**: Free tier eligible, 1 vCPU, 1 GB RAM
- **Amazon Linux 2**: Optimized for AWS, includes SSM agent
- Separates configuration from Auto Scaling Group (makes updates easier)

### Auto Scaling Group

**Capacity**:
- **min_capacity=2**: Always run 2 instances minimum (high availability)
- **max_capacity=6**: Can scale up to 6 instances under load
- **desired_capacity=2**: Start with 2 instances

**Subnet Placement**:
- Deploys to private subnets (Application tier)
- Automatically distributes across AZs for fault tolerance

**Health Checks**:
- Uses ELB health checks (more reliable than EC2 status checks)
- 5 minute grace period for instance to become healthy
- Automatically replaces unhealthy instances

### CPU-Based Scaling

```python
scale_on_cpu_utilization(target_utilization_percent=70)
```

CDK creates two CloudWatch alarms:
1. **Scale Up**: If average CPU > 70% for 3 minutes, add 1 instance
2. **Scale Down**: If average CPU < 70% for 15 minutes, remove 1 instance

This maintains performance while optimizing cost.

### Target Group

Registers Auto Scaling Group instances with the load balancer:
- **Health Check Path**: `/health` endpoint
- **Interval**: Check every 30 seconds
- **Thresholds**: 2 consecutive healthy checks to mark healthy, 3 unhealthy to mark unhealthy

## Key CDK Concepts

- **Cross-Stack Communication**: Pass `db_security_group`, `db_endpoint`, `db_secret_arn` from DatabaseStack to enable database connectivity.

- **Security Group Rules**: The app tier adds a rule TO the database security group, not from it. This is the AWS security model: ingress rules on the destination.

- **User Data Tokens**: The `user_data` can include CDK tokens that resolve at synthesis time (like `{db_secret_arn}`).

- **Automatic IAM Grants**: `db_secret.grant_read(role)` automatically adds the correct IAM policy statement.

## AWS Resources Created

- 1 Launch Template
- 1 Auto Scaling Group
- 2-6 EC2 Instances (based on scaling)
- 1 Security Group
- 1 IAM Role and Instance Profile
- 1 Target Group
- 2 CloudWatch Alarms (scale up/down)

## Cost Estimate

- EC2 t3.micro x 2: ~$15/month (free tier covers 750 hours/month)
- EBS volumes (8 GB per instance): ~$2/month
- Data transfer: Variable
- **Total**: ~$17/month (or free within free tier)

## Security Checklist

✅ Deployed in private subnets (no public IPs)  
✅ Uses IAM roles (no hardcoded credentials)  
✅ Database credentials from Secrets Manager  
✅ SSM Session Manager (no SSH keys)  
✅ Security group with least privilege  
✅ Multi-AZ deployment for fault tolerance  

## Scaling Behavior

**Traffic Increases**:
1. CPU utilization rises above 70%
2. CloudWatch alarm triggers after 3 minutes
3. Auto Scaling adds 1 instance
4. New instance launches, passes health check
5. ALB starts sending traffic to it

**Traffic Decreases**:
1. CPU utilization drops below 70%
2. CloudWatch alarm triggers after 15 minutes
3. Auto Scaling removes 1 instance
4. ALB stops sending traffic to it
5. Instance terminates

## Next Steps

See [[04-presentation-tier]] to add an Application Load Balancer and CloudFront.
