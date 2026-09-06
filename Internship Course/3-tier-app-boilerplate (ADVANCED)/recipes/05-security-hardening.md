---
tags:
  - security
  - iam
  - encryption
---

# Security Hardening

Additional security controls including IAM policies, encryption, secrets rotation, and AWS WAF for comprehensive defense in depth.

## Code

```python
from aws_cdk import Stack, RemovalPolicy, Duration
from aws_cdk import aws_wafv2 as waf
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_kms as kms
from aws_cdk import aws_iam as iam
from constructs import Construct


class SecurityStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        distribution: cloudfront.IDistribution,
        db_secret: secretsmanager.ISecret,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # KMS key for encrypting secrets
        kms_key = kms.Key(
            self,
            "AppEncryptionKey",
            description="Key for encrypting application secrets",
            enable_key_rotation=True,  # Automatic yearly rotation
            removal_policy=RemovalPolicy.RETAIN,  # Don't delete key on stack delete
        )

        # Secrets rotation (optional enhancement)
        # Requires Lambda function to update database password
        # db_secret.add_rotation_schedule(
        #     "RotationSchedule",
        #     automatically_after=Duration.days(30),
        # )

        # WAF Web ACL for CloudFront
        web_acl = waf.CfnWebACL(
            self,
            "CloudFrontWebACL",
            scope="CLOUDFRONT",  # Must be CLOUDFRONT for CloudFront distributions
            default_action=waf.CfnWebACL.DefaultActionProperty(
                allow={}  # Allow by default, block specific patterns
            ),
            visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="CloudFrontWebACL",
                sampled_requests_enabled=True,
            ),
            rules=[
                # Block common SQL injection patterns
                waf.CfnWebACL.RuleProperty(
                    name="SQLInjectionRule",
                    priority=1,
                    statement=waf.CfnWebACL.StatementProperty(
                        sqli_match_statement=waf.CfnWebACL.SqliMatchStatementProperty(
                            field_to_match=waf.CfnWebACL.FieldToMatchProperty(
                                all_query_arguments={}
                            ),
                            text_transformations=[
                                waf.CfnWebACL.TextTransformationProperty(
                                    priority=0,
                                    type="URL_DECODE",
                                )
                            ],
                        )
                    ),
                    action=waf.CfnWebACL.RuleActionProperty(block={}),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="SQLInjectionRule",
                        sampled_requests_enabled=True,
                    ),
                ),
                # Block Cross-Site Scripting (XSS) attempts
                waf.CfnWebACL.RuleProperty(
                    name="XSSRule",
                    priority=2,
                    statement=waf.CfnWebACL.StatementProperty(
                        xss_match_statement=waf.CfnWebACL.XssMatchStatementProperty(
                            field_to_match=waf.CfnWebACL.FieldToMatchProperty(
                                all_query_arguments={}
                            ),
                            text_transformations=[
                                waf.CfnWebACL.TextTransformationProperty(
                                    priority=0,
                                    type="URL_DECODE",
                                )
                            ],
                        )
                    ),
                    action=waf.CfnWebACL.RuleActionProperty(block={}),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="XSSRule",
                        sampled_requests_enabled=True,
                    ),
                ),
                # Rate limiting - max 2000 requests per 5 minutes per IP
                waf.CfnWebACL.RuleProperty(
                    name="RateLimitRule",
                    priority=3,
                    statement=waf.CfnWebACL.StatementProperty(
                        rate_based_statement=waf.CfnWebACL.RateBasedStatementProperty(
                            limit=2000,
                            aggregate_key_type="IP",
                        )
                    ),
                    action=waf.CfnWebACL.RuleActionProperty(block={}),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="RateLimitRule",
                        sampled_requests_enabled=True,
                    ),
                ),
                # Block requests from known malicious IP addresses
                # Uses AWS Managed Rules - IP Reputation List
                waf.CfnWebACL.RuleProperty(
                    name="AWSIPReputationList",
                    priority=4,
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesAmazonIpReputationList",
                        )
                    ),
                    override_action=waf.CfnWebACL.OverrideActionProperty(none={}),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="AWSIPReputationList",
                        sampled_requests_enabled=True,
                    ),
                ),
                # Core rule set - protects against common vulnerabilities
                waf.CfnWebACL.RuleProperty(
                    name="AWSCoreRuleSet",
                    priority=5,
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            vendor_name="AWS",
                            name="AWSManagedRulesCommonRuleSet",
                        )
                    ),
                    override_action=waf.CfnWebACL.OverrideActionProperty(none={}),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name="AWSCoreRuleSet",
                        sampled_requests_enabled=True,
                    ),
                ),
            ],
        )

        # Note: Associate Web ACL with CloudFront in the FrontendStack
        # distribution = cloudfront.Distribution(
        #     self, "Distribution",
        #     web_acl_id=web_acl.attr_arn,
        #     ...
        # )
```

## What's Happening

### KMS Encryption Key

**Automatic Key Rotation**:
- AWS rotates the key material every year
- Old versions retained for decryption
- Application code doesn't need to change

**Removal Policy**:
- `RETAIN` prevents accidental key deletion
- Deleted keys have a 7-30 day waiting period
- Production keys should always use `RETAIN`

**Usage**:
```python
# Use KMS key with Secrets Manager
secret = secretsmanager.Secret(
    self, "MySecret",
    encryption_key=kms_key,
)

# Use KMS key with S3
bucket = s3.Bucket(
    self, "MyBucket",
    encryption_key=kms_key,
    encryption=s3.BucketEncryption.KMS,
)
```

### AWS WAF (Web Application Firewall)

Protects against common web exploits at Layer 7 (application layer).

**Rule Types**:

1. **SQL Injection Protection**
   - Inspects query parameters for SQL injection patterns
   - Blocks requests like: `?id=1 OR 1=1; DROP TABLE users--`
   - Uses AWS's SQL pattern detection

2. **Cross-Site Scripting (XSS) Protection**
   - Blocks script injection attempts
   - Catches patterns like: `<script>alert('XSS')</script>`
   - Protects against reflected and stored XSS

3. **Rate Limiting**
   - Limits requests per IP address
   - 2000 requests per 5 minutes = ~6.6 requests/second
   - Prevents DDoS and brute force attacks
   - Automatically unblocks after the time window

4. **IP Reputation List**
   - AWS managed list of known malicious IPs
   - Updated automatically by AWS threat intelligence
   - Blocks requests from botnets, compromised machines

5. **Core Rule Set**
   - Protection against OWASP Top 10 vulnerabilities
   - Includes rules for:
     - Path traversal (`../../etc/passwd`)
     - Remote file inclusion
     - Command injection
     - Protocol attacks

### WAF Scope

```python
scope="CLOUDFRONT"  # For CloudFront distributions
# OR
scope="REGIONAL"    # For ALB, API Gateway (in a specific region)
```

CloudFront WAF must be deployed in `us-east-1` region.

### Visibility Configuration

```python
visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
    cloud_watch_metrics_enabled=True,  # Send metrics to CloudWatch
    metric_name="RuleName",            # Metric name for this rule
    sampled_requests_enabled=True,     # Sample blocked requests
)
```

**CloudWatch Metrics**:
- `AllowedRequests`: Count of requests that passed
- `BlockedRequests`: Count of requests blocked
- Per-rule metrics for debugging

**Sampled Requests**:
- WAF stores sample of blocked requests
- View in AWS Console: WAF → Web ACLs → Sampled requests
- Includes IP, headers, query parameters (for troubleshooting false positives)

### Secrets Rotation

```python
db_secret.add_rotation_schedule(
    "RotationSchedule",
    automatically_after=Duration.days(30),
)
```

**What Happens**:
1. Lambda function generates new password
2. Updates database with new password
3. Updates Secrets Manager with new value
4. Application automatically gets new secret on next read

**Requirements**:
- Lambda function with rotation logic (CDK can generate)
- Database must support password changes
- Application must not cache credentials

## Key CDK Concepts

- **L1 vs L2 Constructs**: `CfnWebACL` is an L1 (low-level) construct - maps 1:1 to CloudFormation. No L2 construct exists yet for WAF v2, so we use L1.

- **Managed Rule Groups**: AWS maintains these rule sets and updates them automatically. You get the latest protection without code changes.

- **Cost Awareness**: WAF charges per Web ACL ($5/month) + per rule ($1/month) + per million requests ($0.60). This configuration costs ~$12/month + request charges.

## AWS Resources Created

- 1 KMS Key
- 1 WAF Web ACL
- 5 WAF Rules
- CloudWatch Metrics for each rule

## Cost Estimate

- KMS Key: Free (20,000 requests/month free tier)
- WAF Web ACL: $5/month
- WAF Rules: $1/month × 5 = $5/month
- WAF Requests: $0.60 per million requests
- **Total**: ~$12/month + request charges

## Security Checklist

This completes the security hardening:

✅ **Network Security**
- VPC with isolated subnets
- Security groups with least privilege
- No public IPs on application/database tiers

✅ **Data Protection**
- Encryption at rest (RDS, EBS, Secrets)
- Encryption in transit (TLS/SSL)
- KMS key rotation

✅ **Access Control**
- IAM roles with least privilege
- No hardcoded credentials
- SSM Session Manager (no SSH keys)

✅ **Application Security**
- WAF protection against OWASP Top 10
- Rate limiting
- DDoS protection (Shield Standard + CloudFront)

✅ **Monitoring**
- CloudWatch logs for all services
- WAF sampled requests
- CloudTrail for API audit

## Production Best Practices

**Additional Hardening**:
1. Enable AWS Config for compliance monitoring
2. Use AWS Inspector for vulnerability scanning
3. Implement Amazon GuardDuty for threat detection
4. Set up AWS Security Hub for centralized findings
5. Enable VPC Flow Logs for network traffic analysis
6. Use AWS Systems Manager Parameter Store for non-secret config
7. Implement resource tagging strategy for cost allocation

**Compliance**:
- PCI DSS: Requires encryption, network isolation, logging
- HIPAA: Requires encryption, access controls, audit trails
- SOC 2: Requires monitoring, change management, access reviews

## Testing WAF Rules

**Test SQL Injection Block**:
```bash
curl 'https://YOUR-CLOUDFRONT-URL/?id=1%20OR%201=1'
# Should return 403 Forbidden
```

**Test XSS Block**:
```bash
curl 'https://YOUR-CLOUDFRONT-URL/?search=<script>alert(1)</script>'
# Should return 403 Forbidden
```

**Test Rate Limit**:
```bash
for i in {1..2100}; do curl https://YOUR-CLOUDFRONT-URL/; done
# After 2000 requests, should start getting 403
```

## Next Steps

See [[06-monitoring-alarms]] for operational visibility and alerting.
