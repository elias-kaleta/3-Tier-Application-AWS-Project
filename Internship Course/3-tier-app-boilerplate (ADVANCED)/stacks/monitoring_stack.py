"""
Monitoring Stack - CloudWatch dashboards and alarms

Creates operational visibility with:
- CloudWatch alarms for key metrics
- SNS notifications
- CloudWatch dashboard with key metrics
"""

from aws_cdk import Stack, Duration
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as cw_actions
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_rds as rds
from aws_cdk import aws_autoscaling as autoscaling
from constructs import Construct


class MonitoringStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        alb: elbv2.IApplicationLoadBalancer,
        target_group: elbv2.IApplicationTargetGroup,
        asg: autoscaling.IAutoScalingGroup,
        database: rds.IDatabaseInstance,
        **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # SNS Topic for alarm notifications
        alarm_topic = sns.Topic(
            self,
            "AlarmTopic",
            display_name="3-Tier App Alarms",
        )

        # Subscribe email to receive alarm notifications
        # Replace with your email address
        alarm_topic.add_subscription(
            subscriptions.EmailSubscription("your-email@example.com")
        )

        # === APPLICATION LOAD BALANCER ALARMS ===

        # High 5XX error rate
        alb_5xx_alarm = cloudwatch.Alarm(
            self,
            "ALB5XXAlarm",
            metric=alb.metric_http_code_target(
                code=elbv2.HttpCodeTarget.TARGET_5XX_COUNT,
                statistic=cloudwatch.Stats.SUM,
                period=Duration.minutes(5),
            ),
            threshold=10,
            evaluation_periods=2,
            alarm_description="ALB is receiving too many 5XX errors from targets",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        alb_5xx_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # Unhealthy target count
        unhealthy_target_alarm = cloudwatch.Alarm(
            self,
            "UnhealthyTargetAlarm",
            metric=target_group.metric_unhealthy_host_count(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(1),
            ),
            threshold=1,
            evaluation_periods=2,
            alarm_description="One or more targets are unhealthy",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        unhealthy_target_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # High response time
        response_time_alarm = cloudwatch.Alarm(
            self,
            "ResponseTimeAlarm",
            metric=target_group.metric_target_response_time(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(5),
            ),
            threshold=1.0,  # 1 second
            evaluation_periods=2,
            alarm_description="Target response time is too high",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        response_time_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # === AUTO SCALING GROUP ALARMS ===

        # High CPU utilization
        cpu_alarm = cloudwatch.Alarm(
            self,
            "HighCPUAlarm",
            metric=asg.metric_cpu_utilization(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(5),
            ),
            threshold=80,
            evaluation_periods=2,
            alarm_description="Auto Scaling Group CPU is consistently high",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        cpu_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # === RDS DATABASE ALARMS ===

        # High CPU utilization
        db_cpu_alarm = cloudwatch.Alarm(
            self,
            "DBCPUAlarm",
            metric=database.metric_cpu_utilization(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(5),
            ),
            threshold=80,
            evaluation_periods=2,
            alarm_description="Database CPU utilization is high",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        db_cpu_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # Low free storage space
        db_storage_alarm = cloudwatch.Alarm(
            self,
            "DBStorageAlarm",
            metric=database.metric_free_storage_space(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(5),
            ),
            threshold=2_000_000_000,  # 2 GB in bytes
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            alarm_description="Database free storage is running low",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        db_storage_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # High database connections
        db_connections_alarm = cloudwatch.Alarm(
            self,
            "DBConnectionsAlarm",
            metric=database.metric_database_connections(
                statistic=cloudwatch.Stats.AVERAGE,
                period=Duration.minutes(5),
            ),
            threshold=80,  # Adjust based on instance class
            evaluation_periods=2,
            alarm_description="Database connection count is high",
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        db_connections_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # === CLOUDWATCH DASHBOARD ===

        dashboard = cloudwatch.Dashboard(
            self,
            "AppDashboard",
            dashboard_name="ThreeTierAppDashboard",
        )

        # Add widgets to dashboard
        dashboard.add_widgets(
            # Row 1: Load Balancer Metrics
            cloudwatch.GraphWidget(
                title="ALB Request Count",
                left=[
                    alb.metric_request_count(
                        statistic=cloudwatch.Stats.SUM,
                        period=Duration.minutes(5),
                    )
                ],
                width=12,
            ),
            cloudwatch.GraphWidget(
                title="ALB Target Response Time",
                left=[
                    target_group.metric_target_response_time(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=12,
            ),
        )

        dashboard.add_widgets(
            # Row 2: Error Rates
            cloudwatch.GraphWidget(
                title="ALB 5XX Errors",
                left=[
                    alb.metric_http_code_target(
                        code=elbv2.HttpCodeTarget.TARGET_5XX_COUNT,
                        statistic=cloudwatch.Stats.SUM,
                        period=Duration.minutes(5),
                    )
                ],
                width=8,
            ),
            cloudwatch.GraphWidget(
                title="Target Health",
                left=[
                    target_group.metric_healthy_host_count(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(1),
                    ),
                    target_group.metric_unhealthy_host_count(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(1),
                    ),
                ],
                width=8,
            ),
            cloudwatch.SingleValueWidget(
                title="Current Target Count",
                metrics=[
                    target_group.metric_target_count(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=8,
            ),
        )

        dashboard.add_widgets(
            # Row 3: Application Tier
            cloudwatch.GraphWidget(
                title="Auto Scaling Group CPU",
                left=[
                    asg.metric_cpu_utilization(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=12,
            ),
            cloudwatch.GraphWidget(
                title="Instance Count",
                left=[
                    cloudwatch.Metric(
                        namespace="AWS/AutoScaling",
                        metric_name="GroupInServiceInstances",
                        dimensions_map={
                            "AutoScalingGroupName": asg.auto_scaling_group_name,
                        },
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(1),
                    )
                ],
                width=12,
            ),
        )

        dashboard.add_widgets(
            # Row 4: Database
            cloudwatch.GraphWidget(
                title="Database CPU",
                left=[
                    database.metric_cpu_utilization(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=8,
            ),
            cloudwatch.GraphWidget(
                title="Database Connections",
                left=[
                    database.metric_database_connections(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=8,
            ),
            cloudwatch.GraphWidget(
                title="Database Free Storage",
                left=[
                    database.metric_free_storage_space(
                        statistic=cloudwatch.Stats.AVERAGE,
                        period=Duration.minutes(5),
                    )
                ],
                width=8,
            ),
        )

        # Alarm status widget
        dashboard.add_widgets(
            cloudwatch.AlarmStatusWidget(
                title="Alarm Status",
                alarms=[
                    alb_5xx_alarm,
                    unhealthy_target_alarm,
                    response_time_alarm,
                    cpu_alarm,
                    db_cpu_alarm,
                    db_storage_alarm,
                    db_connections_alarm,
                ],
                width=24,
            )
        )
