# 3-Tier Application - AWS Console Guide

A hands-on guide for building a complete 3-tier web application using **only the AWS Console** - no code required!

**Audience**: Cloud architecture interns learning AWS through practical, hands-on experience.

**Prerequisites**: 
- AWS account with admin access
- Basic understanding of web applications
- Completion of Weeks 1-3 of the internship course

---

## What You'll Build

A production-ready three-tier web application:

```
Internet
    ↓
CloudFront (CDN)
    ↓
Application Load Balancer
    ↓
EC2 Web Servers (Auto Scaling 2-6 instances)
    ↓
RDS MySQL Database (Multi-AZ)
```

### Architecture Overview

- **Presentation Tier**: CloudFront + Application Load Balancer in public subnets
- **Application Tier**: EC2 instances with Auto Scaling in private subnets
- **Data Tier**: RDS MySQL database in isolated subnets

---

## Time Estimate

- **Day 1**: 2-3 hours (Networking + Database)
- **Day 2**: 2-3 hours (Application tier)
- **Day 3**: 1-2 hours (Load Balancer + Testing)
- **Day 4**: 1-2 hours (CloudFront + Monitoring)
- **Total**: 6-10 hours spread across Week 4

---

## Guide Structure

Follow these guides in order:

| Guide | What You'll Build | Time | Week 4 Day |
|-------|-------------------|------|------------|
| [[01-vpc-setup]] | VPC with 3 subnet tiers | 30 min | Day 1 |
| [[02-database-setup]] | RDS Multi-AZ MySQL | 45 min | Day 1 |
| [[03-application-setup]] | EC2 with Auto Scaling | 90 min | Day 2 |
| [[04-load-balancer-setup]] | ALB configuration | 30 min | Day 3 |
| [[05-cloudfront-setup]] | CDN distribution | 20 min | Day 4 |
| [[06-monitoring-setup]] | CloudWatch alarms | 30 min | Day 4 |

---

## Learning Objectives

By the end of this guide, you will:

✅ Create a VPC with public, private, and isolated subnets  
✅ Configure route tables and security groups  
✅ Launch a Multi-AZ RDS database  
✅ Create EC2 launch templates  
✅ Set up Auto Scaling Groups  
✅ Configure Application Load Balancers  
✅ Create CloudFront distributions  
✅ Set up CloudWatch monitoring and alarms  
✅ Understand AWS Well-Architected Framework principles  

---

## Cost Warning

This architecture costs money! Estimated costs:

- **While Learning** (~5-10 hours): $1-3
- **Per Day Running**: $3-5
- **Per Month**: ~$94

**Important**: Follow the cleanup guide at the end to avoid charges!

Free tier covers:
- 750 hours EC2 t2.micro/t3.micro
- 750 hours RDS db.t2.micro/db.t3.micro
- 750 hours Application Load Balancer
- 1 TB CloudFront data transfer

---

## Before You Start

### 1. Choose Your AWS Region

Pick a region close to you:
- **US East (N. Virginia)**: us-east-1
- **US West (Oregon)**: us-west-2
- **EU (Ireland)**: eu-west-1
- **Asia Pacific (Singapore)**: ap-southeast-1

**Important**: Use the SAME region for all resources!

### 2. Create an IAM User (If Using Root)

For security, create an IAM user instead of using root:

1. Go to IAM → Users → Add User
2. Username: `intern-admin`
3. Enable AWS Management Console access
4. Attach policy: `AdministratorAccess`
5. Save credentials securely

### 3. Enable MFA (Recommended)

1. IAM → Users → Security credentials
2. Assigned MFA device → Activate MFA
3. Use Google Authenticator or Authy

---

## Naming Convention

Use consistent naming throughout:

```
Project Prefix: 3tier-app

Examples:
- VPC: 3tier-app-vpc
- Subnet: 3tier-app-public-1a
- Security Group: 3tier-app-alb-sg
- EC2: 3tier-app-web-server
- RDS: 3tier-app-database
```

This makes resources easy to find and manage.

---

## Quick Reference

### IP Address Ranges (CIDR)

- **VPC**: 10.0.0.0/16 (65,536 IPs)
- **Public Subnet 1**: 10.0.1.0/24 (256 IPs)
- **Public Subnet 2**: 10.0.2.0/24 (256 IPs)
- **Private Subnet 1**: 10.0.11.0/24 (256 IPs)
- **Private Subnet 2**: 10.0.12.0/24 (256 IPs)
- **Database Subnet 1**: 10.0.21.0/24 (256 IPs)
- **Database Subnet 2**: 10.0.22.0/24 (256 IPs)

### Security Group Rules

Will be defined in each guide, but here's the overview:

- **ALB SG**: Allow HTTP (80) and HTTPS (443) from 0.0.0.0/0
- **EC2 SG**: Allow HTTP (80) from ALB SG only
- **RDS SG**: Allow MySQL (3306) from EC2 SG only

---

## Console Navigation Tips

### Finding Services
- Use the search bar at the top: "Type service name here"
- Pin frequently used services: Click star icon

### Switching Regions
- Top right corner: Select your region
- **Always verify** you're in the correct region!

### Tagging Resources
Add these tags to every resource:
- **Key**: Project | **Value**: 3tier-app
- **Key**: Environment | **Value**: dev
- **Key**: Owner | **Value**: your-name

---

## Troubleshooting Common Issues

### Can't Find Resource
- ✅ Check you're in the correct region
- ✅ Check filters (clear all filters)
- ✅ Check resource name/ID

### Permission Denied
- ✅ Ensure IAM user has AdministratorAccess
- ✅ Try logging out and back in
- ✅ Check MFA is working

### Service Quota Exceeded
- ✅ AWS limits resources in new accounts
- ✅ Request quota increase: Service Quotas console
- ✅ Wait 24-48 hours for approval

### Free Tier Exceeded
- ✅ Check AWS Budgets for current spend
- ✅ Set up billing alerts
- ✅ Stop resources when not in use

---

## Getting Help

### AWS Documentation
- VPC User Guide: https://docs.aws.amazon.com/vpc/
- EC2 User Guide: https://docs.aws.amazon.com/ec2/
- RDS User Guide: https://docs.aws.amazon.com/rds/
- ELB User Guide: https://docs.aws.amazon.com/elasticloadbalancing/

### AWS Support
- Basic support included with all accounts
- Use "Support Center" in console
- AWS re:Post community: https://repost.aws/

### Course Resources
- Review Week 1-3 materials
- Ask instructors during lab sessions
- Collaborate with fellow interns

---

## What's Next?

Ready to start? Follow the guides in order:

1. **[01-vpc-setup.md](./01-vpc-setup.md)** - Create your VPC foundation
2. **[02-database-setup.md](./02-database-setup.md)** - Set up RDS database
3. **[03-application-setup.md](./03-application-setup.md)** - Launch EC2 instances
4. **[04-load-balancer-setup.md](./04-load-balancer-setup.md)** - Configure ALB
5. **[05-cloudfront-setup.md](./05-cloudfront-setup.md)** - Add CDN
6. **[06-monitoring-setup.md](./06-monitoring-setup.md)** - Set up monitoring

Then customize the application for your team's project!

---

## Week 4 Schedule Alignment

- **Day 1**: Complete guides 1-2 (VPC + Database)
- **Day 2**: Complete guide 3 (Application tier)
- **Day 3**: Complete guide 4 (Load Balancer + Testing)
- **Day 4**: Complete guides 5-6 (CloudFront + Monitoring)
- **Day 5**: Present your architecture!

---

## Success Criteria

You've completed this successfully when:

✅ You can access your application via CloudFront URL  
✅ All health checks are passing  
✅ Database is responding to queries  
✅ Auto Scaling is working (scale up/down)  
✅ CloudWatch dashboard shows metrics  
✅ You can explain each component's purpose  

Good luck! 🚀
