# 3-Tier Application Boilerplate

A complete AWS CDK implementation of a three-tier web application architecture. This project demonstrates how to build a scalable, secure web application using AWS best practices.

**Audience**: Cloud architecture interns learning to design and deploy production-ready applications on AWS using Infrastructure as Code.

**Prerequisites**: 
- AWS CDK v2 installed
- Python 3.10+
- AWS account bootstrapped (`cdk bootstrap`)
- Basic understanding of web application architecture

---

## Architecture Overview

This application demonstrates the classic three-tier architecture pattern:

```
Internet → CloudFront → ALB → EC2 Auto Scaling Group → RDS Database
           (CDN)        ↓     (Application Tier)        (Data Tier)
                    WAF/Shield
```

### Tiers

1. **Presentation Tier** (Public)
   - CloudFront CDN for content delivery
   - Application Load Balancer
   - Web servers in Auto Scaling Group
   - Public subnets across multiple AZs

2. **Application Tier** (Private)
   - EC2 instances running business logic
   - Auto Scaling Group for elasticity
   - Private subnets with NAT Gateway for outbound access
   - Security groups restricting access to ALB only

3. **Data Tier** (Isolated)
   - RDS Multi-AZ database
   - Isolated subnets (no internet access)
   - Encrypted at rest and in transit
   - Security groups allowing only application tier access

---

## Project Structure

```
3-tier-app-boilerplate/
├── README.md                          # This file
├── app.py                             # CDK app entry point
├── cdk.json                           # CDK configuration
├── requirements.txt                   # Python dependencies
├── recipes/
│   ├── 01-networking-foundation.md    # VPC, subnets, routing
│   ├── 02-data-tier.md               # RDS database setup
│   ├── 03-application-tier.md        # EC2, Auto Scaling
│   ├── 04-presentation-tier.md       # ALB, CloudFront
│   ├── 05-security-hardening.md      # IAM, security groups
│   └── 06-monitoring-alarms.md       # CloudWatch, alarms
└── stacks/
    ├── __init__.py
    ├── networking_stack.py           # VPC infrastructure
    ├── database_stack.py             # RDS and security
    ├── application_stack.py          # Compute resources
    ├── frontend_stack.py             # ALB and CloudFront
    └── monitoring_stack.py           # CloudWatch dashboards
```

---

## Recipes

Each recipe file explains one layer of the architecture with annotated CDK code and deployment patterns.

| Recipe | What it covers |
|--------|----------------|
| [[01-networking-foundation]] | VPC with public, private, and isolated subnets; NAT Gateway; route tables |
| [[02-data-tier]] | RDS Multi-AZ MySQL database, security groups, parameter groups, automated backups |
| [[03-application-tier]] | Launch template, Auto Scaling Group, target group, application code deployment |
| [[04-presentation-tier]] | Application Load Balancer, CloudFront distribution, SSL/TLS certificates |
| [[05-security-hardening]] | IAM roles, security group rules, encryption, secrets management |
| [[06-monitoring-alarms]] | CloudWatch metrics, dashboards, alarms, SNS notifications |

---

## Quick Start

### 1. Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Bootstrap Your AWS Account

```bash
cdk bootstrap aws://ACCOUNT-ID/REGION
```

### 3. Review the Synthesized Template

```bash
cdk synth
```

### 4. Deploy the Application

```bash
# Deploy all stacks
cdk deploy --all

# Or deploy incrementally
cdk deploy NetworkingStack
cdk deploy DatabaseStack
cdk deploy ApplicationStack
cdk deploy FrontendStack
cdk deploy MonitoringStack
```

### 5. Access Your Application

After deployment completes, the CloudFront URL will be in the stack outputs:

```
FrontendStack.CloudFrontURL = https://d1234567890.cloudfront.net
```

---

## Architecture Decisions

### Why Three Tiers?

- **Separation of Concerns**: Each tier has a distinct responsibility
- **Security**: Network isolation limits blast radius of breaches
- **Scalability**: Tiers can scale independently based on load
- **Maintainability**: Changes to one tier don't affect others

### Why Multi-AZ?

- **High Availability**: Survive datacenter failures
- **Zero-Downtime Deployments**: Rolling updates across AZs
- **Disaster Recovery**: RDS automatic failover

### Why Auto Scaling?

- **Cost Optimization**: Scale down during low traffic
- **Performance**: Scale up during high traffic
- **Resilience**: Automatically replace failed instances

### Cost Considerations

- **NAT Gateway**: ~$32/month per gateway + data transfer
- **RDS Multi-AZ**: ~2x single instance cost for redundancy
- **ALB**: ~$16/month + LCU pricing
- **CloudFront**: Pay for data transfer out

**Optimization Tips**:
- Use single NAT Gateway (not one per AZ) for dev/test
- Use RDS db.t3.micro or t4g.micro for free tier eligible workloads
- Consider Aurora Serverless v2 for variable workloads
- Use CloudFront to reduce ALB data transfer costs

---

## AWS Well-Architected Framework Alignment

### Operational Excellence
- Infrastructure as Code (CDK)
- CloudWatch monitoring and alarms
- Automated deployments

### Security
- Network isolation (VPC, subnets)
- Encryption at rest (RDS, EBS)
- Encryption in transit (TLS/SSL)
- IAM least privilege
- Security groups (stateful firewall)

### Reliability
- Multi-AZ deployment
- Auto Scaling for fault tolerance
- RDS automated backups
- Health checks and auto-recovery

### Performance Efficiency
- CloudFront CDN for content delivery
- Auto Scaling based on demand
- Right-sized instance types

### Cost Optimization
- Auto Scaling (scale down when idle)
- Free tier eligible resources
- Consolidated billing across stacks

### Sustainability
- Efficient resource utilization
- Auto Scaling reduces waste
- CloudFront reduces data transfer

---

## Learning Path

1. Start with [[01-networking-foundation]] to understand VPC design
2. Build the data layer with [[02-data-tier]]
3. Add compute with [[03-application-tier]]
4. Expose your app via [[04-presentation-tier]]
5. Secure everything in [[05-security-hardening]]
6. Monitor and alert with [[06-monitoring-alarms]]

---

## Deployment Commands

```bash
# See what changes will be made
cdk diff

# Deploy with manual approval
cdk deploy --require-approval=broadening

# Destroy all resources (be careful!)
cdk destroy --all

# Watch mode (auto-deploy on code changes)
cdk watch
```

---

## Next Steps

After completing this boilerplate, consider:

- Adding a CI/CD pipeline with CodePipeline
- Implementing blue/green deployments
- Adding Lambda functions for serverless components
- Setting up DynamoDB for session storage
- Integrating Cognito for authentication
- Adding ElastiCache for caching
- Implementing S3 for static assets

---

## Resources

- [AWS CDK Documentation](https://docs.aws.amazon.com/cdk/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [CDK Workshop](https://cdkworkshop.com/)
