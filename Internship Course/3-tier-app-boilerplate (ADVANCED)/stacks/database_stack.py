"""
Database Stack - RDS Multi-AZ MySQL database

Creates a highly available database with:
- Multi-AZ deployment for fault tolerance
- Encryption at rest
- Automated backups
- Security group restrictions
"""

from aws_cdk import Stack, RemovalPolicy, Duration, CfnOutput
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from constructs import Construct


class DatabaseStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Security group for database
        self.db_security_group = ec2.SecurityGroup(
            self,
            "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for RDS database",
            allow_all_outbound=False,  # No outbound access needed
        )

        # RDS instance in isolated subnets
        self.database = rds.DatabaseInstance(
            self,
            "AppDatabase",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_35
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,  # Free tier eligible
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_group_name="Database"  # Isolated subnets
            ),
            security_groups=[self.db_security_group],
            multi_az=True,  # Deploy standby in second AZ
            allocated_storage=20,  # GB - free tier includes 20GB
            storage_type=rds.StorageType.GP3,  # Latest generation
            storage_encrypted=True,  # Encryption at rest
            database_name="appdb",
            backup_retention=Duration.days(7),
            delete_automated_backups=True,
            removal_policy=RemovalPolicy.SNAPSHOT,  # Create final snapshot on delete
            deletion_protection=False,  # Set True for production
            cloudwatch_logs_exports=["error", "general", "slowquery"],
        )

        # Export values for use in other stacks
        self.db_endpoint = self.database.db_instance_endpoint_address
        self.db_secret_arn = self.database.secret.secret_arn

        # Output database endpoint
        CfnOutput(
            self,
            "DatabaseEndpoint",
            value=self.db_endpoint,
            description="RDS database endpoint",
        )

        CfnOutput(
            self,
            "DatabaseSecretArn",
            value=self.db_secret_arn,
            description="ARN of the database credentials secret",
        )
