---
tags:
  - monitoring
  - cloudwatch
  - alarms
---

# Monitoring and Alarms

CloudWatch dashboards, metrics, and alarms for complete operational visibility across all three tiers.

## Code

```python
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
```

## What's Happening

### SNS Topic for Notifications

**Email Subscriptions**:
- After deployment, check your email for confirmation
- Click "Confirm subscription" link
- You'll receive emails when alarms trigger

**Alternative Notification Methods**:
```python
# Slack via Lambda
alarm_topic.add_subscription(
    subscriptions.LambdaSubscription(slack_lambda)
)

# SMS (be careful - costs $0.00645 per message)
alarm_topic.add_subscription(
    subscriptions.SmsSubscription("+1234567890")
)

# PagerDuty, Opsgenie (via HTTPS endpoint)
alarm_topic.add_subscription(
    subscriptions.UrlSubscription("https://...")
)
```

### CloudWatch Alarms

**Anatomy of an Alarm**:
```python
cloudwatch.Alarm(
    metric=...,              # What to measure
    threshold=80,            # Value that triggers alarm
    evaluation_periods=2,    # How many periods must breach
    period=Duration.minutes(5),  # Length of each period
)
```

**Example**: `cpu_alarm` triggers if average CPU > 80% for 2 consecutive 5-minute periods (10 minutes total).

### Alarm States

- **OK**: Metric below threshold
- **ALARM**: Metric exceeded threshold for specified evaluation periods
- **INSUFFICIENT_DATA**: Not enough data to evaluate (common after deployment)

### Treat Missing Data

```python
treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING
```

Options:
- `NOT_BREACHING`: Missing data doesn't trigger alarm (best for intermittent metrics)
- `BREACHING`: Missing data triggers alarm (use for critical metrics that should always report)
- `IGNORE`: Skip evaluation period with missing data
- `MISSING`: Treat as missing (alarm goes to INSUFFICIENT_DATA state)

### Key Metrics Explained

**Load Balancer**:
- `RequestCount`: Total HTTP requests received
- `TargetResponseTime`: Time for targets to respond (latency)
- `HTTPCode_Target_5XX_Count`: Application errors
- `UnHealthyHostCount`: Targets failing health checks

**Auto Scaling Group**:
- `CPUUtilization`: Average CPU across all instances
- `GroupInServiceInstances`: Number of healthy instances

**RDS Database**:
- `CPUUtilization`: Database CPU usage
- `DatabaseConnections`: Active database connections
- `FreeStorageSpace`: Available disk space
- `ReadLatency` / `WriteLatency`: I/O performance

### Dashboard Widgets

**GraphWidget**: Time-series line charts
```python
cloudwatch.GraphWidget(
    title="My Metric",
    left=[metric1, metric2],  # Left Y-axis
    right=[metric3],          # Right Y-axis (different scale)
    width=12,                 # Grid is 24 columns wide
)
```

**SingleValueWidget**: Current metric value
```python
cloudwatch.SingleValueWidget(
    title="Current Value",
    metrics=[metric],
    width=6,
)
```

**AlarmStatusWidget**: Shows alarm states
```python
cloudwatch.AlarmStatusWidget(
    alarms=[alarm1, alarm2, alarm3],
)
```

## Key CDK Concepts

- **Metric Factory Methods**: Every AWS resource has `.metric_*()` methods that return pre-configured `Metric` objects. No need to specify namespace, dimensions manually.

- **Automatic Dimensions**: 
  ```python
  alb.metric_request_count()  # Automatically includes LoadBalancer dimension
  ```

- **Composite Alarms**: Create alarms based on multiple alarms (not shown):
  ```python
  composite = cloudwatch.CompositeAlarm(
      self, "CompositeAlarm",
      alarm_rule=cloudwatch.AlarmRule.any_of(alarm1, alarm2, alarm3),
  )
  ```

## AWS Resources Created

- 1 SNS Topic
- 1 Email Subscription (requires confirmation)
- 7 CloudWatch Alarms
- 1 CloudWatch Dashboard

## Cost Estimate

- SNS Topic: Free
- Email Notifications: Free
- CloudWatch Alarms: First 10 free, $0.10/month each after
- Dashboard: First 3 free, $3/month each after
- Metrics: Most AWS service metrics are free
- **Total**: Free (within free tier)

## Alarm Response Workflow

When an alarm triggers:

1. **SNS Notification Sent**
   - Email arrives with alarm details
   - Includes link to CloudWatch console

2. **Investigate**
   - Open CloudWatch dashboard
   - Check correlated metrics
   - Review application logs

3. **Common Causes**:
   - High CPU: Traffic spike, inefficient code
   - 5XX Errors: Application bug, database timeout
   - Unhealthy Targets: Failed health checks, instance issues
   - Low Storage: Need to expand RDS storage

4. **Auto Scaling Response**
   - High CPU triggers scale-up automatically
   - Low CPU triggers scale-down (after 15 min cooldown)

5. **Manual Response**
   - Update application code
   - Increase RDS instance size
   - Add read replicas
   - Optimize database queries

## Dashboard Usage

**Access Dashboard**:
1. AWS Console → CloudWatch → Dashboards
2. Select "ThreeTierAppDashboard"
3. Optionally: Add to favorites, share with team

**Time Range Selection**:
- Last 1 hour (default)
- Last 3 hours, 12 hours, 1 day, 3 days, 1 week
- Custom range

**Auto-Refresh**:
- Click "Actions" → "Auto refresh"
- Select: 10s, 1m, 2m, 5m, 15m

## Production Enhancements

**Additional Alarms**:
- RDS read/write latency
- EBS burst balance (for t3 instances)
- Network throughput
- ALB 4XX errors (client errors)
- CloudFront error rate

**Enhanced Monitoring**:
- Enable RDS Enhanced Monitoring (detailed OS metrics)
- CloudWatch Container Insights (if using ECS)
- X-Ray for distributed tracing
- CloudWatch Logs Insights queries

**Anomaly Detection**:
```python
metric.create_alarm_from_anomaly_detection(
    threshold=2,  # Standard deviations from normal
    evaluation_periods=2,
    actions_enabled=True,
)
```

## Alarm Testing

**Test 5XX Alarm**:
```bash
# Make application code return 500
# Wait for alarm to trigger (5-10 minutes)
```

**Test CPU Alarm**:
```bash
# SSH to instance (via Session Manager)
stress-ng --cpu 8 --timeout 600s
```

**Test Database Storage Alarm**:
```bash
# Fill database with test data until storage low
```

## Runbook Integration

Create runbooks for each alarm:

**High CPU Alarm**:
1. Check dashboard for traffic spike
2. Review Auto Scaling history
3. If traffic is legitimate, increase max_capacity
4. If traffic is attack, enable rate limiting

**Database Connection Alarm**:
1. Check application logs for connection leaks
2. Review slow query log
3. Consider read replicas
4. Increase connection pool size

**5XX Error Alarm**:
1. Check application logs in CloudWatch
2. Review recent deployments
3. Check database connectivity
4. Roll back if necessary

## Next Steps

This completes the 3-tier application boilerplate!

**Production Deployment Checklist**:
- [ ] Replace email with PagerDuty/Opsgenie
- [ ] Add custom domain and SSL certificate
- [ ] Enable RDS automated backups
- [ ] Configure log retention policies
- [ ] Set up AWS Backup for disaster recovery
- [ ] Enable AWS Config for compliance
- [ ] Document runbooks for each alarm
- [ ] Load test the application
- [ ] Perform security audit
- [ ] Set up CI/CD pipeline
