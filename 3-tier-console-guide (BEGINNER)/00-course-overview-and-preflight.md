# Build a Three-Tier AWS Application: Overview and Preflight

## Estimated Time

20–30 minutes

## Lecture Outcome

By the end of this lecture, you will understand the architecture, choose a cost mode, prepare a safe AWS environment, and record the values used throughout the project.

## Important Course Note

> **Important:** This is a console-first project. You will create the AWS infrastructure in the AWS Management Console rather than with Infrastructure as Code. A small application is supplied in the course resources and deployed later.
>
> Do not use the AWS account root user for this lab. Use an instructor-provided sandbox, AWS Academy account, or a permission-scoped IAM role. If you are working in your own account, protect the root user with MFA and store its credentials securely.

## What You Will Build

Traffic will follow this path:

1. User
2. CloudFront distribution
3. Application Load Balancer in two public subnets
4. Auto Scaling group of EC2 instances in two private subnets
5. RDS MySQL database in two isolated database subnets

The application tier can download updates through a NAT Gateway, but it cannot receive direct internet traffic. The database has no internet route and accepts MySQL connections only from the application security group.

## Lab Mode or High-Availability Mode

Choose one mode before you begin.

### Lab Mode

- RDS: Single-AZ
- EC2 Auto Scaling: minimum 1, desired 1, maximum 2
- One NAT Gateway
- Best for short training sessions and lower cost

### High-Availability Mode

- RDS: Multi-AZ
- EC2 Auto Scaling: minimum 2, desired 2, maximum 6
- One NAT Gateway for this course; two NAT Gateways would remove the cross-AZ dependency in a production design
- Best for demonstrating resilience, but it costs more

Write your choice here: ______________________________

## Cost Warning

> **Warning:** This lab creates billable resources, including a NAT Gateway, RDS database, EC2 instances, Application Load Balancer, public IPv4 addresses, CloudWatch logs, and the required AWS WAF baseline. Prices and free offers vary by account, date, and Region.

Before creating resources:

1. Open the AWS Pricing Calculator at `https://calculator.aws/`.
2. Estimate the current cost in your selected Region.
3. Open Billing and Cost Management, then Budgets.
4. Create a cost budget named `3tier-app-monthly-budget` with email alerts at limits appropriate to your account.
5. Record a cleanup deadline.

> **Important:** A budget alert is not a hard spending limit and billing data can be delayed. Complete the final cleanup lecture even if you think your account is covered by a free offer.

Cleanup deadline: ______________________________

## Prerequisites

- An AWS account or sandbox with permission to use VPC, EC2, Elastic Load Balancing, Auto Scaling, IAM roles, S3, RDS, Secrets Manager, CloudFront, CloudWatch, SNS, and Billing
- The downloadable Lecture 3 resource bundle: `app.py`, `index.html`, `requirements.txt`, and `user-data.sh`
- Basic familiarity with IPv4 addresses, web requests, and relational databases
- A password manager for any credentials you must handle

## Region Check

Select one AWS Region and use it for every regional resource in this project. CloudFront is a global service, but its origin resources remain regional.

- Selected Region name: ______________________________
- Selected Region code: ______________________________
- Availability Zone A: ______________________________
- Availability Zone B: ______________________________

> **Important:** Do not copy `us-east-1a` or `us-east-1b` unless those are valid choices in your selected Region. Availability Zone labels can map differently between accounts.

## Naming Standard

Use these names exactly unless your instructor provides a unique prefix:

| Resource | Name |
|---|---|
| Project prefix | `3tier-app` |
| VPC | `3tier-app-vpc` |
| Public subnets | `3tier-app-public-1a` and `3tier-app-public-1b` |
| Private subnets | `3tier-app-private-1a` and `3tier-app-private-1b` |
| Database subnets | `3tier-app-db-1a` and `3tier-app-db-1b` |
| Internet Gateway | `3tier-app-igw` |
| NAT Gateway | `3tier-app-nat-1a` |
| Route tables | `3tier-app-public-rt`, `3tier-app-private-rt`, `3tier-app-db-rt` |
| Security groups | `3tier-app-alb-sg`, `3tier-app-app-sg`, `3tier-app-db-sg` |
| RDS subnet group | `3tier-app-db-subnet-group` |
| RDS database | `3tier-app-database` |
| Application asset bucket | create a globally unique name such as `3tier-app-assets-<ACCOUNT_ID>-<REGION>` |
| IAM role | `3tier-app-ec2-role` |
| Launch template | `3tier-app-launch-template` |
| Auto Scaling group | `3tier-app-asg` |
| Target group | `3tier-app-target-group` |
| Load balancer | `3tier-app-alb` |
| SNS topic in project Region | `3tier-app-alarms` |
| SNS topic in us-east-1 | `3tier-app-edge-alarms` |
| WAF Web ACL | `3tier-app-web-acl` |
| WAF rate rule | `3tier-app-booking-rate-limit` |
| Cost budget | `3tier-app-monthly-budget` |
| Dashboard | `ThreeTierAppDashboard` |

## Standard Tags

Add these tags wherever the service supports them:

| Tag | Value |
|---|---|
| Project | `3tier-app` |
| Environment | `dev` |
| Owner | `<YOUR_NAME_OR_TEAM>` |
| ManagedBy | `ConsoleCourse` |
| ExpirationDate | `<YOUR_CLEANUP_DATE>` |

## Network Plan

| Network | CIDR |
|---|---|
| VPC | `10.0.0.0/16` |
| Public subnet A | `10.0.1.0/24` |
| Public subnet B | `10.0.2.0/24` |
| Private subnet A | `10.0.11.0/24` |
| Private subnet B | `10.0.12.0/24` |
| Database subnet A | `10.0.21.0/24` |
| Database subnet B | `10.0.22.0/24` |

## Security Flow

| Connection | Protocol or port |
|---|---|
| Internet to CloudFront | HTTPS |
| CloudFront to ALB | HTTP 80 for this lab |
| ALB to application | TCP 5000 |
| Application to RDS | TCP 3306 |
| Administrators to EC2 | Systems Manager Session Manager, not SSH |

The course uses HTTPS between users and CloudFront. Encrypting the CloudFront-to-ALB connection requires a domain name and an ACM certificate that matches that domain. That is listed as an optional extension.

## Action: Prepare the Account

1. Sign in with your sandbox identity or IAM role.
2. Confirm the account alias or account ID in the top-right menu.
3. Select your Region.
4. Open IAM and confirm that MFA is enabled for long-lived human users.
5. Do not attach `AdministratorAccess` merely to complete this lab. Ask your instructor for a scoped lab role if a required action is denied.
6. Open Service Quotas and confirm your account can create at least one VPC, one NAT Gateway, one load balancer, two EC2 instances, and one RDS database.
7. Open Billing and Cost Management and configure your budget alert.

## Checkpoint

You are signed in without the root user, your Region is visible in the console header, and you have recorded a cleanup deadline.

## Project Success Criteria

You will be finished when you can demonstrate all of the following:

- [ ] The CloudFront URL loads the ticket-booking application over HTTPS.
- [ ] The application lists events stored in RDS and can create a booking.
- [ ] ALB target health is healthy.
- [ ] EC2 instances have no public IPv4 addresses.
- [ ] RDS is not publicly accessible.
- [ ] Auto Scaling replaces a terminated instance.
- [ ] CloudWatch displays application metrics and an alarm can notify an SNS subscription.
- [ ] Direct access to the ALB is blocked after origin protection is enabled.
- [ ] You can explain the architecture using all six AWS Well-Architected pillars.
- [ ] You remove all lab resources in dependency order.

## Course Lecture Order

1. Lecture 1: Network foundation
2. Lecture 2: Database tier
3. Lecture 3: Application tier
4. Lecture 4: Load balancing and Auto Scaling
5. Lecture 5: CloudFront and security hardening
6. Lecture 6: Monitoring and end-to-end validation
7. Lecture 7: Presentation and Well-Architected review
8. Lecture 8: Complete resource cleanup

## Knowledge Check

1. Why should the database use isolated subnets?

   **Expected answer:** It does not need direct internet access, so removing an internet route reduces its attack surface.

2. Is an AWS Budget a hard spending cap?

   **Expected answer:** No. It sends alerts, and billing data can be delayed.

3. Why are two cost modes provided?

   **Expected answer:** The lower-cost mode is suitable for learning, while the high-availability mode demonstrates redundancy at additional cost.

## Next Lecture

Create the VPC, six subnets, gateways, and route tables.
