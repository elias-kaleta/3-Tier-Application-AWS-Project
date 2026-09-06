# Quick Start Guide

Get your 3-tier application deployed in 30 minutes.

## Prerequisites

- AWS Account with admin access
- AWS CLI configured (`aws configure`)
- Python 3.10 or higher
- Node.js 14 or higher (for CDK CLI)

## Step 1: Install AWS CDK

```bash
npm install -g aws-cdk
cdk --version
```

## Step 2: Bootstrap Your AWS Account

This creates an S3 bucket and IAM roles for CDK deployments:

```bash
cdk bootstrap aws://ACCOUNT-ID/REGION

# Example:
# cdk bootstrap aws://123456789012/us-east-1
```

## Step 3: Set Up Python Environment

```bash
# Navigate to project directory
cd 3-tier-app-boilerplate

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Configure Email Notifications (Optional)

Edit `stacks/monitoring_stack.py` and replace the email:

```python
# Line 35-37
alarm_topic.add_subscription(
    subscriptions.EmailSubscription("YOUR-EMAIL@example.com")
)
```

## Step 5: Review What Will Be Created

```bash
cdk synth
```

This generates CloudFormation templates in `cdk.out/` directory.

## Step 6: Deploy the Application

```bash
# Deploy all stacks at once
cdk deploy --all

# Or deploy incrementally (recommended for learning)
cdk deploy NetworkingStack
cdk deploy DatabaseStack
cdk deploy ApplicationStack
cdk deploy FrontendStack
cdk deploy MonitoringStack
```

**Note**: Deployment takes 15-20 minutes due to RDS Multi-AZ setup.

## Step 7: Test Your Application

After deployment completes, look for the outputs:

```
FrontendStack.CloudFrontURL = https://d1234567890.cloudfront.net
FrontendStack.LoadBalancerURL = http://app-lb-123456.us-east-1.elb.amazonaws.com
```

### Test the Load Balancer

```bash
curl http://YOUR-ALB-URL/

# Expected response:
# {
#   "message": "Connected to database!",
#   "database_version": "8.0.35"
# }
```

### Test the CloudFront CDN

```bash
curl https://YOUR-CLOUDFRONT-URL/

# Same response as above
```

### Test Health Endpoint

```bash
curl http://YOUR-ALB-URL/health

# Expected response:
# {
#   "status": "healthy"
# }
```

## Step 8: View Your Dashboard

1. Go to AWS Console → CloudWatch → Dashboards
2. Open "ThreeTierAppDashboard"
3. See metrics for ALB, Auto Scaling, and RDS

## Step 9: Confirm Email Subscription

1. Check your email for "AWS Notification - Subscription Confirmation"
2. Click "Confirm subscription"
3. You'll now receive alarm notifications

## Architecture Overview

```
Internet
    ↓
CloudFront CDN (HTTPS)
    ↓
Application Load Balancer (HTTP)
    ↓
EC2 Auto Scaling Group (2-6 instances)
    ↓
RDS MySQL Multi-AZ Database
```

## Cost Estimate

**Free Tier Eligible** (first 12 months):
- EC2 t3.micro: 750 hours/month free
- RDS db.t3.micro: 750 hours/month free
- ALB: 750 hours/month free
- CloudFront: 1 TB transfer/month free

**After Free Tier** (monthly):
- NAT Gateway: ~$32
- RDS Multi-AZ: ~$30
- EC2 instances x2: ~$15
- ALB: ~$16
- CloudFront: ~$1
- **Total**: ~$94/month

## Common Issues

### Issue: Bootstrap Error

```bash
# Error: Account 123456789012 has not been bootstrapped
cdk bootstrap
```

### Issue: Insufficient IAM Permissions

Ensure your AWS user/role has:
- AdministratorAccess policy (easiest)
- OR specific policies for VPC, EC2, RDS, CloudFormation, IAM

### Issue: "Stack already exists"

```bash
# Destroy existing stack
cdk destroy --all

# Redeploy
cdk deploy --all
```

### Issue: RDS Takes Forever

RDS Multi-AZ deployment takes 10-15 minutes. Be patient!

## Next Steps

1. **Read the Recipes**: Go through each recipe file in `recipes/` to understand how each component works
2. **Customize**: Modify the application code in `application_stack.py`
3. **Add Features**: Add Lambda functions, DynamoDB, S3, etc.
4. **Security**: Review `recipes/05-security-hardening.md`
5. **Monitoring**: Set up custom alarms and dashboards

## Cleanup

To avoid charges, destroy all resources:

```bash
cdk destroy --all
```

**Warning**: This deletes everything including the database. A final snapshot is created automatically.

## Learning Path

Follow this order:

1. ✅ Deploy the application (you're here!)
2. 📖 Read [[recipes/01-networking-foundation.md]]
3. 📖 Read [[recipes/02-data-tier.md]]
4. 📖 Read [[recipes/03-application-tier.md]]
5. 📖 Read [[recipes/04-presentation-tier.md]]
6. 📖 Read [[recipes/05-security-hardening.md]]
7. 📖 Read [[recipes/06-monitoring-alarms.md]]

## Getting Help

- AWS CDK Documentation: https://docs.aws.amazon.com/cdk/
- CDK Workshop: https://cdkworkshop.com/
- AWS re:Post: https://repost.aws/

## Troubleshooting Commands

```bash
# View stack status
cdk list

# Show what changed
cdk diff

# View CloudFormation events
aws cloudformation describe-stack-events --stack-name NetworkingStack

# Check logs
aws logs tail /aws/rds/instance/YOUR-DB-ID --follow

# SSH into instance (via Session Manager)
aws ssm start-session --target i-1234567890abcdef
```

Happy building! 🚀
