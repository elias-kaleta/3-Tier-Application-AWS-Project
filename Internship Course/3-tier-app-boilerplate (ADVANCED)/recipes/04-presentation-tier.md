---
tags:
  - load-balancer
  - cloudfront
  - presentation-tier
---

# Presentation Tier - Load Balancer and CDN

An Application Load Balancer distributing traffic across application instances, fronted by CloudFront for global content delivery and DDoS protection.

## Code

```python
from aws_cdk import Stack, CfnOutput
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from constructs import Construct


class FrontendStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        target_group: elbv2.IApplicationTargetGroup,
        app_security_group: ec2.ISecurityGroup,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Security group for ALB
        alb_security_group = ec2.SecurityGroup(
            self,
            "ALBSecurityGroup",
            vpc=vpc,
            description="Security group for Application Load Balancer",
            allow_all_outbound=False,
        )

        # Allow HTTP from anywhere
        alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP from internet",
        )

        # Allow HTTPS from anywhere (if using certificates)
        alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443),
            description="Allow HTTPS from internet",
        )

        # Allow ALB to reach application instances
        app_security_group.add_ingress_rule(
            peer=alb_security_group,
            connection=ec2.Port.tcp(80),
            description="Allow HTTP from ALB",
        )

        # Create Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "AppLoadBalancer",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_security_group,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC  # Must be in public subnets
            ),
        )

        # Add HTTP listener
        http_listener = alb.add_listener(
            "HttpListener",
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            default_target_groups=[target_group],
        )

        # CloudFront distribution
        distribution = cloudfront.Distribution(
            self,
            "AppDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.LoadBalancerV2Origin(
                    alb,
                    protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_ALL,
                cached_methods=cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,  # North America + Europe
        )

        # Output the URLs
        CfnOutput(
            self,
            "LoadBalancerURL",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Application Load Balancer URL",
        )

        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront Distribution URL (recommended)",
        )
```

## What's Happening

### Application Load Balancer (ALB)

**Why ALB over NLB or CLB?**
- Operates at Layer 7 (HTTP/HTTPS) - can route based on URL paths, headers, query strings
- Native integration with Auto Scaling Groups
- Better health checks (can check specific paths)
- Lower cost than NLB for typical web traffic

**Internet-Facing**:
- `internet_facing=True` gives the ALB a public DNS name
- Deployed in public subnets
- Gets a public IP address

**Target Group Integration**:
- The ALB receives the target group from ApplicationStack
- Traffic flows: Internet → ALB → Target Group → EC2 Instances

### Security Group Flow

```
Internet (any IP)
    ↓ HTTP/HTTPS (ports 80, 443)
ALB Security Group
    ↓ HTTP (port 80)
Application Security Group
    ↓ MySQL (port 3306)
Database Security Group
```

Each tier only accepts traffic from the tier above it (defense in depth).

### CloudFront CDN

**Benefits**:
1. **Global Distribution**: Content served from edge locations near users
2. **DDoS Protection**: AWS Shield Standard included (protection against SYN floods, UDP reflection)
3. **SSL/TLS**: Free HTTPS via CloudFront certificate
4. **Cost Savings**: Reduced load on ALB, lower data transfer costs
5. **Performance**: Static content cached at edge (faster for users)

**Configuration**:
- **Origin**: Points to ALB (not direct to EC2)
- **Protocol Policy**: CloudFront to ALB uses HTTP (no TLS overhead between AWS services)
- **Viewer Protocol**: Clients forced to HTTPS (security best practice)
- **Cache Policy**: Optimized for common web content (caches GET/HEAD/OPTIONS)

**Price Class**:
- `PRICE_CLASS_100`: North America + Europe edge locations
- Cheaper than `PRICE_CLASS_ALL` (global)
- Choose based on your user geography

### Caching Strategy

**Cached by Default**:
- Static assets (images, CSS, JavaScript)
- GET requests with no query strings
- HEAD and OPTIONS requests

**Not Cached** (passed to origin):
- POST, PUT, DELETE requests
- Requests with `Cache-Control: no-cache` header
- Dynamic content (can customize with cache behaviors)

### Custom Domains (Not Implemented)

For production, add:

```python
# In Route 53 stack
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_certificatemanager as acm

# Request ACM certificate
certificate = acm.Certificate(
    self, "Certificate",
    domain_name="example.com",
    validation=acm.CertificateValidation.from_dns(hosted_zone),
)

# Add to CloudFront
distribution = cloudfront.Distribution(
    self, "Distribution",
    domain_names=["example.com"],
    certificate=certificate,
    # ... other props
)

# Create Route 53 record
route53.ARecord(
    self, "AliasRecord",
    zone=hosted_zone,
    target=route53.RecordTarget.from_alias(
        targets.CloudFrontTarget(distribution)
    ),
)
```

## Key CDK Concepts

- **Cross-Stack Dependencies**: This stack depends on NetworkingStack (vpc), ApplicationStack (target_group, security_group). CDK deploys them in order.

- **CfnOutput**: Exports values to the console after deployment:
  ```bash
  cdk deploy
  # Outputs:
  # FrontendStack.LoadBalancerURL = http://app-alb-123456789.us-east-1.elb.amazonaws.com
  # FrontendStack.CloudFrontURL = https://d1234567890.cloudfront.net
  ```

- **Security Group References**: Passing `app_security_group` allows this stack to add ingress rules to it (security groups are mutable).

## AWS Resources Created

- 1 Application Load Balancer
- 1 ALB Security Group
- 1 HTTP Listener
- 1 CloudFront Distribution
- CloudWatch metrics (ALB traffic, errors, latency)

## Cost Estimate

- ALB: ~$16/month + $0.008/LCU-hour
- CloudFront: $0.085/GB data transfer (first 10 TB)
- CloudFront Requests: $0.0075-$0.016 per 10,000 requests
- **Total**: ~$20-30/month for light traffic

## Traffic Flow

```
User Request
    ↓
CloudFront Edge Location (caching)
    ↓ (cache miss)
Application Load Balancer
    ↓ (health check passing)
Target Group
    ↓ (round-robin)
EC2 Instance in AZ-1 or AZ-2
    ↓
RDS Database (connection pooling)
    ↓
Response (cached at CloudFront for next request)
```

## Health Check Behavior

**ALB Health Checks**:
- Sends GET request to `/health` every 30 seconds
- Expects HTTP 200 response
- 2 consecutive successes → Healthy
- 3 consecutive failures → Unhealthy
- Unhealthy instances don't receive traffic

**What Happens on Failure**:
1. Instance fails health check
2. ALB stops routing traffic to it
3. Auto Scaling Group detects failure
4. Auto Scaling terminates unhealthy instance
5. Auto Scaling launches replacement
6. New instance passes health check
7. ALB starts routing traffic to it

## Performance Optimizations

**Latency Reduction**:
- CloudFront edge locations (sub-100ms for most users)
- Keep-alive connections (ALB to instances)
- HTTP/2 support (CloudFront to clients)

**Throughput Optimization**:
- Auto Scaling adds capacity under load
- CloudFront caching reduces origin load
- Multi-AZ distribution for redundancy

## Security Features

✅ HTTPS at CloudFront edge (encrypts client-to-AWS traffic)  
✅ AWS Shield Standard (DDoS protection)  
✅ ALB in public subnets (instances remain private)  
✅ Security groups restrict access between tiers  
✅ CloudWatch logs for audit trail  

## Production Enhancements

Consider adding:
- AWS WAF for application-level protection (SQL injection, XSS)
- ACM certificate + custom domain
- HTTPS listener on ALB (end-to-end encryption)
- CloudFront access logs to S3
- ALB access logs to S3
- CloudWatch alarms for 5XX errors
- Multiple cache behaviors for API vs static content

## Next Steps

See [[05-security-hardening]] for additional security controls.
See [[06-monitoring-alarms]] for operational visibility.
