---
tags:
  - networking
  - foundation
  - vpc
---

# Networking Foundation

The VPC infrastructure that supports all three tiers: public subnets for load balancers, private subnets with NAT for application servers, and isolated subnets for databases.

## Code

```python
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
```

## What's Happening

### VPC and CIDR Blocks

- **`10.0.0.0/16`** gives us 65,536 IP addresses to work with. CDK automatically subdivides this range across the three subnet tiers based on the `cidr_mask` values.

- **`max_azs=2`** deploys subnets across two availability zones for high availability. If one datacenter fails, your application continues running in the other. Production workloads should use 3 AZs.

### Subnet Tiers

**Public Subnets** (`/24` = 256 IPs each)
- Get a route to an Internet Gateway (`0.0.0.0/0 -> igw-xxx`)
- Resources receive public IP addresses
- Used for: Load balancers, bastion hosts, NAT gateways

**Private Subnets with Egress** (`/20` = 4,096 IPs each)
- Get a route to a NAT Gateway for outbound internet access
- No public IPs, not accessible from internet
- Used for: Application servers, web tier instances

**Isolated Subnets** (`/24` = 256 IPs each)
- No route to internet at all (no NAT, no IGW)
- Maximum security for sensitive data
- Used for: Databases, internal message queues

### NAT Gateway Cost Optimization

- **`nat_gateways=1`** creates a single NAT gateway in one AZ
- All private subnets in the other AZ route through it (cross-AZ traffic incurs charges)
- **Cost**: ~$32/month per NAT Gateway + $0.045/GB processed
- **Production pattern**: Set `nat_gateways=max_azs` for fault tolerance (eliminates cross-AZ traffic but costs more)

### Subnet Selection Pattern

When deploying resources to specific tiers, use `vpc.select_subnets()`:

```python
# Select application tier subnets
app_subnets = self.vpc.select_subnets(
    subnet_group_name="Application"
)

# Select database tier subnets
db_subnets = self.vpc.select_subnets(
    subnet_group_name="Database"
)

# Select public subnets
public_subnets = self.vpc.select_subnets(
    subnet_type=ec2.SubnetType.PUBLIC
)
```

## Key CDK Concepts

- **Construct Tree**: The VPC construct automatically creates subnets, route tables, Internet Gateway, NAT Gateway, and all routing associations. Each becomes a CloudFormation resource.

- **Cross-Stack References**: Export `self.vpc` as a public attribute so other stacks can import it:
  ```python
  database_stack = DatabaseStack(app, "DatabaseStack", vpc=networking_stack.vpc)
  ```

- **Immutable CIDR**: Changing `cidr_mask` or subnet order after deployment forces subnet replacement, which causes downtime for attached resources. Plan subnet sizing carefully.

## AWS Resources Created

- 1 VPC
- 1 Internet Gateway
- 1 NAT Gateway
- 1 Elastic IP (for NAT Gateway)
- 6 Subnets (2 public, 2 private, 2 isolated)
- 6 Route Tables (one per subnet)
- Route table associations

## Cost Estimate

- VPC: Free
- NAT Gateway: ~$32/month + data processing
- Elastic IP: Free while attached
- **Total**: ~$32/month base cost

## Security Considerations

- **Network Isolation**: Database tier has zero internet connectivity
- **Egress Control**: Application tier can only reach internet via NAT (single egress point for monitoring)
- **Multi-AZ**: Resources distributed across failure domains

## Next Steps

See [[02-data-tier]] to deploy an RDS database in the isolated subnets.
