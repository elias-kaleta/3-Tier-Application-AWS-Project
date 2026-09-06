# Beginner AWS Three-Tier Application Project

Build and validate a secure three-tier web application using the AWS Management Console. This beginner-friendly, console-first project is the final hands-on deployment for the AWS Cloud Architecture internship course.

The repository supplies a small TicketHub application so learners can focus on AWS architecture, networking, security, scaling, monitoring, and operational decisions.

## Important Before You Begin

> [!WARNING]
> This lab creates billable AWS resources, including a NAT Gateway, RDS database, EC2 instances, an Application Load Balancer, public IPv4 addresses, CloudFront, AWS WAF, Secrets Manager, and CloudWatch resources. Prices and free offers vary. Estimate the cost, configure an AWS Budget, set a cleanup deadline, and complete the cleanup lesson.

- Use an instructor-provided sandbox, AWS Academy account, or permission-scoped IAM role—not the root user.
- Do not attach `AdministratorAccess` merely to complete the lab.
- Use fictitious customer information only. Never publish passwords, secret values, account IDs, tokens, or the CloudFront origin-verification value.
- This is a teaching architecture, not a production-ready reference implementation.
- Never run the cleanup steps against production, shared, or uncertain resources.

## Architecture

```text
User
  │ HTTPS
  ▼
Amazon CloudFront + AWS WAF
  │ HTTP 80 in the base lab
  ▼
Application Load Balancer
  │ TCP 5000
  ▼
EC2 Auto Scaling group in private subnets
  │ TLS over TCP 3306
  ▼
Amazon RDS for MySQL in isolated subnets
```

The VPC spans two Availability Zones and contains six subnets:

- Two public subnets for the Application Load Balancer
- Two private subnets for EC2 application instances
- Two isolated database subnets for RDS

The project also uses Amazon S3 for private application assets, AWS Secrets Manager for database credentials, Systems Manager Session Manager for administration, and CloudWatch and SNS for monitoring and notifications.

## Who This Project Is For

This guide is designed for AWS beginners, interns, and learners who want guided experience deploying a complete database-backed application. It assumes basic familiarity with:

- Networking concepts such as IP addresses, subnets, and routes
- Linux command-line operations
- Web requests and relational databases
- Basic Python or JavaScript concepts
- Navigating the AWS Management Console

No application development is required; the project resources are provided.

## Choose a Deployment Mode

| Mode | RDS | Auto Scaling capacity | Recommended use |
|---|---|---|---|
| Lab Mode | Single-AZ | Minimum 1, desired 1, maximum 2 | First-time learners and shorter, lower-cost labs |
| High-Availability Mode | Multi-AZ | Minimum 2, desired 2, maximum 6 | Demonstrating resilience at additional cost |

Both modes use one NAT Gateway for this course. This lowers lab cost but retains an Availability Zone dependency.

## Course Guide

Complete the lessons in numeric order. Each lesson includes outcomes, prerequisites, console steps, checkpoints, troubleshooting, and knowledge checks.

| Lesson | Topic |
|---|---|
| [00](00-course-overview-and-preflight.md) | Architecture overview, account safety, cost planning, naming, and preflight |
| [01](01-network-foundation.md) | VPC, six subnets, Internet Gateway, NAT Gateway, and route tables |
| [02](02-database-tier.md) | Security groups, isolated RDS MySQL, backups, encryption, and secrets |
| [03](03-application-tier.md) | Private S3 assets, scoped IAM, launch template, EC2, and Auto Scaling |
| [04](04-load-balancing-and-auto-scaling.md) | Target group, Application Load Balancer, health checks, and scaling policy |
| [05](05-cloudfront-and-security.md) | CloudFront HTTPS, origin protection, ALB restriction, and AWS WAF |
| [06](06-monitoring-and-validation.md) | CloudWatch, SNS, functional testing, security checks, and resilience testing |
| [07](07-presentation-and-well-architected.md) | Architecture presentation and AWS Well-Architected review |
| [08](08-complete-resource-cleanup.md) | Dependency-ordered teardown and billing verification |

Start with **[Lesson 00: Course Overview and Preflight](00-course-overview-and-preflight.md)**. Do not skip **[Lesson 08: Complete Resource Cleanup](08-complete-resource-cleanup.md)**.

## Included Application Resources

The [`course-resources`](course-resources/) directory contains:

| File | Purpose |
|---|---|
| [`app.py`](course-resources/app.py) | Flask and PyMySQL TicketHub application |
| [`index.html`](course-resources/index.html) | Dependency-free browser interface |
| [`requirements.txt`](course-resources/requirements.txt) | Pinned Python dependencies |
| [`user-data.sh`](course-resources/user-data.sh) | Amazon Linux EC2 bootstrap script |

Download all four files before Lesson 03. Upload only `app.py`, `index.html`, and `requirements.txt` to the private S3 application path. Customize `user-data.sh` locally and paste it into the EC2 launch template as instructed.

## What You Will Learn

By completing the project, you will be able to:

- Design segmented public, private application, and isolated database tiers across two Availability Zones
- Deploy a database-backed application without public EC2 or RDS access
- Use security-group references, scoped IAM permissions, managed secrets, and verified RDS TLS
- Route traffic through CloudFront, AWS WAF, an ALB, and an Auto Scaling group
- Validate application health, CRUD behavior, origin isolation, replacement resilience, and bounded scaling
- Build CloudWatch dashboards and alarms with SNS notifications
- Evaluate design decisions using all six AWS Well-Architected pillars
- Remove AWS resources safely in dependency order and verify remaining charges

## Security and Design Limitations

This project intentionally favors an understandable learning path over production completeness:

- Viewer traffic uses HTTPS to CloudFront, but the base CloudFront-to-ALB connection uses HTTP. End-to-end TLS requires a custom origin domain and matching ACM certificate.
- One NAT Gateway remains an Availability Zone dependency. A production design commonly uses one per AZ or appropriate VPC endpoints.
- The sample runtime database identity has schema-scoped DDL permissions because the application initializes tables at startup. Production systems should separate migration and CRUD-only runtime identities.
- Dynamic caching is disabled to prevent stale or inappropriate API responses. Production systems should define separate static and dynamic cache behaviors.
- Production readiness also requires workload-specific threat modeling, load testing, recovery objectives, governance, compliance, and operational ownership.

## Final Project Deliverables

Use the running project to produce:

1. An AWS architecture diagram
2. A working TicketHub deployment and sanitized demonstration
3. A rationale for each AWS service selected
4. An analysis covering all six AWS Well-Architected pillars
5. A short demo recording or live demonstration
6. A presentation describing decisions, limitations, and scaling opportunities
7. Retrospective notes describing lessons learned and future improvements

Complete these deliverables before deleting the environment, then follow the cleanup guide immediately to limit ongoing charges.

## Repository Scope

This repository contains the final beginner three-tier console project. It does not implement every topic from the broader four-week internship curriculum, such as CloudFormation, CI/CD, serverless APIs, or container orchestration.

## License and Usage

Use this material in an authorized AWS training account or sandbox. Follow your organization’s security, data-handling, cost-management, and resource-retention policies.