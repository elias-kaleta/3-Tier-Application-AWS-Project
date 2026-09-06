# Present the Architecture and Well-Architected Decisions

## Estimated Time

45–60 minutes

## Lecture Outcome

You will prepare a clear architecture diagram, organize evidence, explain trade-offs through the six AWS Well-Architected pillars, and rehearse a short project demonstration.

## Prerequisites

- The final validation checklist is complete.
- You captured screenshots without secrets, account IDs, or personal information.
- The application is still running for the demonstration.

## Action 1: Create the Architecture Diagram

Use an approved diagram tool and official AWS architecture icons where possible.

Your diagram must show:

- Users and the public internet
- CloudFront as the global entry point
- The AWS Region and VPC boundary
- Two Availability Zones
- Two public subnets containing ALB nodes
- Two private application subnets containing the Auto Scaling group
- Two isolated database subnets containing RDS
- Internet Gateway and NAT Gateway
- S3 application-assets bucket
- Secrets Manager secret
- Systems Manager administrative path
- CloudWatch logs, metrics, dashboard, alarms, and SNS
- Security-group flow on ports `80`, `5000`, and `3306`

Add arrows and labels for:

| Connection | Protocol or path |
|---|---|
| Viewer to CloudFront | HTTPS |
| CloudFront to ALB | HTTP in this lab |
| ALB to application | TCP `5000` |
| Application to RDS | TCP `3306` |
| Application outbound updates | NAT Gateway |

### Accessibility

> **Accessibility note:** Include a text description of the architecture so learners who cannot see the diagram receive the same information.

## Action 2: Organize Your Evidence

Prepare these screenshots or short recordings:

1. VPC subnet list showing six CIDRs across two AZs.
2. Public, private, and database route tables.
3. RDS configuration showing encrypted and not publicly accessible.
4. EC2 instance details showing no public IPv4 address.
5. ALB target group showing Healthy targets.
6. Application working through the CloudFront HTTPS URL.
7. One successful placeholder booking.
8. The listener’s `403` captured before SG restriction, plus final evidence that direct ALB access is network-blocked.
9. CloudWatch dashboard with recent data.
10. Auto Scaling Activity showing instance replacement or scale-out.
11. SNS test notification with personal addresses hidden.

> **Security note:** Never include passwords, secret values, origin-header values, account IDs, session tokens, or real customer data.

## Action 3: Explain Each Tier

### Presentation Tier

CloudFront provides the public HTTPS endpoint and edge delivery. The ALB distributes requests across healthy application instances. Header and network controls reduce direct ALB bypass.

### Application Tier

The Auto Scaling group runs replaceable EC2 instances in private subnets. The launch template creates consistent instances, Session Manager avoids inbound SSH, and the application retrieves a schema-scoped runtime identity through its IAM role.

### Data Tier

RDS MySQL runs in isolated database subnets, stores state independently of EC2, encrypts storage, and maintains automated backups. Its security group trusts only the application security group, and application connections verify the RDS TLS certificate.

## Action 4: Map the Design to the Six Well-Architected Pillars

### Operational Excellence

- Implemented: consistent names and tags, systemd service, centralized logs, alarms, dashboard, runbooks, and documented validation.
- Next improvement: deploy with Infrastructure as Code and an automated release pipeline.

### Security

- Implemented: private application and database tiers, security-group references, Session Manager, IAM roles, separate bootstrap and runtime secrets, schema-scoped database permissions, verified RDS TLS, CloudFront HTTPS, input validation, and origin restriction.
- Known gap: the CloudFront-to-ALB hop uses HTTP. End-to-end TLS requires a custom origin domain and matching certificate.

### Reliability

- Implemented: resources span two AZs, ALB health checks, Auto Scaling replacement, RDS backups, and optional Multi-AZ RDS.
- Known gap: one NAT Gateway is an AZ dependency. A production design would normally use one per AZ.

### Performance Efficiency

- Implemented: load balancing, target-tracking scaling, CloudFront, managed database metrics, and burstable lab instances.
- Next improvement: performance tests, right-sizing, static-asset cache behaviors, and database query analysis.

### Cost Optimization

- Implemented: explicit LAB MODE, small resources, bounded scaling, tags, budget alerts, short log retention, and mandatory cleanup.
- Known trade-off: NAT Gateway and ALB have standing charges even when traffic is low.

### Sustainability

- Implemented: scale-in, shared managed services, right-sized lab capacity, and short-lived environments.
- Next improvement: measure utilization, remove idle environments automatically, and choose efficient instance families based on workload evidence.

## Action 5: Prepare a Five-Minute Demo

Suggested flow:

| Time | Activity |
|---|---|
| Minute 0–1 | State the user problem and show the architecture. |
| Minute 1–2 | Open the CloudFront HTTPS URL and browse events. |
| Minute 2–3 | Create a placeholder booking and explain the database flow. |
| Minute 3–4 | Show healthy ALB targets, private EC2 placement, and RDS isolation. |
| Minute 4–5 | Show the dashboard and explain one trade-off and one next improvement. |

> **Note:** Keep a recorded backup or screenshots in case a live AWS service is still updating.

## Action 6: Prepare for Questions

Be ready to answer:

### Why Not Place EC2 in Public Subnets?

Because users should enter through controlled CloudFront and ALB layers; direct instance exposure is unnecessary.

### Why Use Security-Group References Instead of IP Addresses?

Instances change during scaling and replacement. Group references preserve identity-based network rules.

### Why Does the Health Endpoint Check the Database?

It prevents the ALB from sending user traffic to an instance that cannot complete core requests. A production system may separate liveness and readiness checks.

### What Changes for Production?

Infrastructure as Code, CI/CD, end-to-end TLS, per-AZ NAT or VPC endpoints, stronger database-user separation, WAF tuning, restore tests, defined SLOs, and deeper observability.

### Why Is This Not Automatically Production-Ready?

A teaching architecture demonstrates patterns, but production readiness requires workload-specific threat modeling, load testing, recovery objectives, operations, governance, and compliance.

## Action 7: Complete the Retrospective

Answer in three to five sentences each:

1. What worked well?

   ____________________________________________________________

2. What was the most difficult failure to diagnose?

   ____________________________________________________________

3. Which design trade-off would you change first?

   ____________________________________________________________

4. Which metric or alarm was most useful?

   ____________________________________________________________

5. What would you automate next?

   ____________________________________________________________

## Final Presentation Checkpoint

- [ ] Architecture diagram complete: __________
- [ ] Text description included: __________
- [ ] All six pillars covered: __________
- [ ] Trade-offs stated honestly: __________
- [ ] Demo rehearsed: __________
- [ ] No secrets or personal data in evidence: __________
- [ ] Cleanup scheduled immediately after presentation: __________

## Knowledge Check

1. Which pillar addresses runbooks and repeatable operations?

   **Expected answer:** Operational Excellence.

2. Which lab component remains an AZ dependency?

   **Expected answer:** The single NAT Gateway.

3. Why should the presentation include limitations?

   **Expected answer:** Good architecture communication explains evidence and trade-offs rather than claiming every design is universally production-ready.

## Next Lecture

Delete every billable lab resource in dependency order and verify cleanup.
