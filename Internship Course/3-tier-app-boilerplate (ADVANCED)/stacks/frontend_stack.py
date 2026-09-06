"""
Frontend Stack - Application Load Balancer and CloudFront

Creates presentation tier with:
- Application Load Balancer in public subnets
- CloudFront CDN for global content delivery
- Security groups for ALB access
"""

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

        # Allow HTTPS from anywhere
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
        self.alb = elbv2.ApplicationLoadBalancer(
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
        http_listener = self.alb.add_listener(
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
                    self.alb,
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
            value=f"http://{self.alb.load_balancer_dns_name}",
            description="Application Load Balancer URL",
        )

        CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="CloudFront Distribution URL (recommended)",
        )
