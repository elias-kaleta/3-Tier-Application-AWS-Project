---
tags:
  - database
  - rds
  - data-tier
---

# Data Tier - RDS Database

A Multi-AZ RDS MySQL database deployed in isolated subnets with automated backups, encryption, and security group restrictions.

## Code

```python
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
)
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
```

## What's Happening

### Database Engine

- **MySQL 8.0.35**: Latest stable version with improved performance and security
- Alternatives: PostgreSQL, MariaDB, Oracle, SQL Server
- Version pinning prevents automatic upgrades that might break compatibility

### Instance Sizing

- **db.t3.micro**: Free tier eligible, 2 vCPU, 1 GB RAM
- Burstable performance instances accumulate CPU credits during idle periods
- Production workloads need larger instances (t3.medium, m6g.large, etc.)
- Consider Amazon Aurora for production (better performance, auto-scaling storage)

### Multi-AZ Deployment

**How it Works**:
1. Primary instance runs in AZ-1
2. Standby instance runs in AZ-2 (synchronous replication)
3. Automatic failover if primary fails (typically 60-120 seconds)
4. DNS endpoint stays the same - application reconnects automatically

**What it Provides**:
- High availability during hardware failures
- Automated backups from standby (no performance impact)
- Maintenance windows use standby promotion
- **Cost**: ~2x single instance pricing

### Storage Configuration

- **GP3**: Latest generation SSD, better performance per dollar than GP2
- **20 GB**: Minimum allocation, free tier includes up to 20 GB
- **Encryption**: AES-256 encryption at rest using AWS managed key
- Storage auto-scales if you enable `storage_autoscaling=True`

### Backup Strategy

- **Automated Backups**: Daily snapshots retained for 7 days
- **Backup Window**: Happens during low-traffic hours (configurable)
- **Point-in-Time Recovery**: Restore to any second within retention period
- **Final Snapshot**: `RemovalPolicy.SNAPSHOT` creates snapshot before deletion

### Security Group

The database security group starts with **zero inbound rules**. The application tier will add an ingress rule in the next step:

```python
# This happens in application_stack.py
db_security_group.add_ingress_rule(
    peer=app_security_group,
    connection=ec2.Port.tcp(3306),
    description="Allow MySQL from application tier"
)
```

This implements **least privilege**: only application servers can reach the database.

### CloudWatch Logs

- **error logs**: Database errors and warnings
- **general logs**: All SQL statements (high volume, use sparingly)
- **slowquery logs**: Queries exceeding `long_query_time` threshold

Use for debugging and performance tuning. Logs export to CloudWatch Logs `/aws/rds/instance/<db-name>/`.

## Key CDK Concepts

- **Cross-Stack Dependencies**: Passing `vpc` from `NetworkingStack` creates an implicit dependency - CDK deploys them in order.

- **Secrets Management**: CDK auto-creates a secret in AWS Secrets Manager with the master password:
  ```python
  # Access the secret
  secret = self.database.secret
  secret_arn = secret.secret_arn
  
  # Grant application read access
  secret.grant_read(app_role)
  ```

- **Connection String**: Get the endpoint programmatically:
  ```python
  endpoint = self.database.db_instance_endpoint_address
  port = self.database.db_instance_endpoint_port
  ```

## AWS Resources Created

- 1 RDS DB Instance (primary)
- 1 RDS DB Instance (standby replica in second AZ)
- 1 DB Subnet Group (spanning isolated subnets)
- 1 Security Group
- 1 Secret (master password in Secrets Manager)
- CloudWatch Log Groups (error, general, slowquery)
- Automated backup snapshots

## Cost Estimate

- db.t3.micro Multi-AZ: ~$30/month (free tier covers 750 hours/month)
- 20 GB GP3 storage: ~$4/month
- Backup storage: Free up to DB size
- **Total**: ~$34/month (or free within free tier limits)

## Security Checklist

✅ Deployed in isolated subnets (no internet access)  
✅ Encryption at rest enabled  
✅ Security group with no inbound rules (app tier adds specific rule)  
✅ Password stored in Secrets Manager  
✅ Automated backups enabled  
✅ CloudWatch logging for audit trail  

## Production Enhancements

For production workloads, consider:

- Enable `deletion_protection=True`
- Increase `backup_retention` to 30+ days
- Use larger instance class (m6g.large or r6g.xlarge)
- Enable Performance Insights for query monitoring
- Set up CloudWatch alarms for CPU, storage, connections
- Use Aurora for better scalability and performance

## Next Steps

See [[03-application-tier]] to deploy EC2 instances that connect to this database.
