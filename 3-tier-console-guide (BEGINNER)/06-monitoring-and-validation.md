# Monitor and Validate the Complete Application

## Estimated Time

75–105 minutes

## Lecture Outcome

You will create regional and CloudFront notification channels, seven CloudWatch alarms, and a dashboard, then prove functionality, edge visibility, isolation, resilience, and optional scale-out behavior.

## Prerequisites

- The CloudFront application URL works over HTTPS.
- `3tier-app-web-acl` and `3tier-app-booking-rate-limit` are active and associated with the distribution.
- Direct ALB access is network-blocked after you captured the listener’s earlier `403` response.
- All target-group instances are Healthy.
- You can use a monitored email address for SNS confirmation.

## Cost Impact

> **Cost warning:** CloudWatch custom dashboards, alarms, log ingestion, retention, and SNS delivery can create charges. Metrics included with AWS resources may still incur dashboard or alarm charges. Review current pricing.

## Region Model

> **Important:** The `3tier-app-alarms` SNS topic and the six alarms for ALB, EC2, Auto Scaling, and RDS live in your project Region. CloudFront metrics are published through `us-east-1`, so the CloudFront alarm and its SNS action live in `us-east-1`. Keep the console Region visible while following each action.

## Action 1: Create the Project-Region SNS Alarm Topic

1. Switch the console to your project Region.
2. Open Amazon SNS.
3. Choose Topics and Create topic.
4. Select Standard.
5. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-alarms` |
   | Display name | `ThreeTierApp` |

6. Add the standard tags and create the topic.
7. Choose Create subscription.
8. Select:

   | Setting | Value |
   |---|---|
   | Protocol | Email |
   | Endpoint | `<YOUR_MONITORED_EMAIL>` |

9. Create the subscription.
10. Open the confirmation email and choose Confirm subscription.
11. Return to SNS and verify the status is Confirmed.
12. Publish a harmless test message to confirm delivery.

## Checkpoint

In the project Region, the `3tier-app-alarms` subscription is Confirmed and the test notification arrives.

## Action 2: Create the US-East-1 Edge SNS Alarm Topic

CloudWatch alarm actions must use an SNS topic in the same Region as the alarm. The CloudFront alarm will be in `us-east-1`, so it cannot use the project-Region topic unless the project Region is already `us-east-1`. Create or confirm a separate topic with a distinct name even when the project Region is `us-east-1`.

1. Switch the console Region to US East (N. Virginia), `us-east-1`.
2. Open Amazon SNS, choose Topics, and look for `3tier-app-edge-alarms`.
3. If it does not exist, create a Standard topic:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-edge-alarms` |
   | Display name | `ThreeTierEdge` |

4. Add the standard tags.
5. Create an Email subscription using the same monitored email address.
6. Confirm the subscription from the email message.
7. Verify the subscription status is Confirmed and publish a harmless test message.

## Checkpoint

In `us-east-1`, the `3tier-app-edge-alarms` subscription is Confirmed and the test notification arrives.

## Action 3: Create Seven Core CloudWatch Alarms

> **Note:** The thresholds below are teaching baselines. Production thresholds should be tied to service-level objectives, normal traffic, and tested runbooks.

For alarms A through F:

1. Switch to the project Region.
2. Open CloudWatch, Alarms, and Create alarm.
3. Select the metric and correct resource dimensions.
4. Configure the condition.
5. Send the In alarm notification to `3tier-app-alarms`.
6. Add a clear description and the standard tags if supported.

### Alarm A: Unhealthy ALB Target

| Setting | Value |
|---|---|
| Namespace | `AWS/ApplicationELB` |
| Metric | `UnHealthyHostCount` |
| Dimensions | Your target group and load balancer |
| Statistic | Maximum |
| Period | 1 minute |
| Condition | Greater than or equal to 1 |
| Datapoints | 2 out of 2 |
| Missing data | Treat as missing |
| Name | `3tier-app-unhealthy-targets` |

**Response:** Check target health reason, application logs, recent launches, and database connectivity.

### Alarm B: Target 5XX Errors

| Setting | Value |
|---|---|
| Namespace | `AWS/ApplicationELB` |
| Metric | `HTTPCode_Target_5XX_Count` |
| Dimensions | Your target group and load balancer |
| Statistic | Sum |
| Period | 5 minutes |
| Condition | Greater than or equal to 10 |
| Datapoints | 2 out of 2 |
| Name | `3tier-app-target-5xx` |

**Response:** Inspect `/3tier-app/application` logs and correlate errors with RDS metrics and deployments.

### Alarm C: High Target Response Time

| Setting | Value |
|---|---|
| Namespace | `AWS/ApplicationELB` |
| Metric | `TargetResponseTime` |
| Dimensions | Your load balancer and target group |
| Statistic | Average |
| Period | 5 minutes |
| Condition | Greater than or equal to 1 second |
| Datapoints | 2 out of 2 |
| Name | `3tier-app-high-latency` |

**Response:** Check CPU, database connections, slow queries, target count, and recent traffic changes.

### Alarm D: High Auto Scaling CPU

| Setting | Value |
|---|---|
| Namespace | `AWS/EC2` |
| Metric | `CPUUtilization` |
| Dimension | `AutoScalingGroupName = 3tier-app-asg` |
| Statistic | Average |
| Period | 5 minutes |
| Condition | Greater than or equal to 80 percent |
| Datapoints | 2 out of 2 |
| Name | `3tier-app-high-app-cpu` |

**Response:** Confirm target-tracking activity, target health, workload source, and maximum capacity.

### Alarm E: High RDS CPU

| Setting | Value |
|---|---|
| Namespace | `AWS/RDS` |
| Metric | `CPUUtilization` |
| Dimension | `DBInstanceIdentifier = 3tier-app-database` |
| Statistic | Average |
| Period | 5 minutes |
| Condition | Greater than or equal to 80 percent |
| Datapoints | 2 out of 2 |
| Name | `3tier-app-high-db-cpu` |

**Response:** Review connections, slow queries, workload changes, and instance sizing.

### Alarm F: Low RDS Free Storage

| Setting | Value |
|---|---|
| Namespace | `AWS/RDS` |
| Metric | `FreeStorageSpace` |
| Dimension | `DBInstanceIdentifier = 3tier-app-database` |
| Statistic | Minimum |
| Period | 5 minutes |
| Condition | Lower than or equal to 2147483648 bytes, which is 2 GiB |
| Datapoints | 1 out of 1 |
| Name | `3tier-app-low-db-storage` |

**Response:** Stop unexpected growth, review logs and tables, then deliberately increase storage if necessary. RDS storage generally cannot be reduced in place.

### Alarm G: CloudFront 5XX Error Rate

1. Switch the console Region to `us-east-1` before creating this alarm.
2. Select the CloudFront distribution metric below. CloudFront may label its metric dimension Region as Global even though you access the metrics and create the alarm in `us-east-1`.

| Setting | Value |
|---|---|
| Namespace | `AWS/CloudFront` |
| Metric | `5xxErrorRate` |
| Dimensions | DistributionId = your project distribution; Region = Global |
| Statistic | Average |
| Period | 5 minutes |
| Condition | Greater than or equal to 5 percent |
| Datapoints | 2 out of 2 |
| Missing data | Treat as not breaching |
| Alarm Region | `us-east-1` |
| Notification topic | `3tier-app-edge-alarms` |
| Name | `3tier-app-cloudfront-5xx-rate` |

**Response:** Check the CloudFront distribution status, AWS WAF sampled requests, origin reachability, ALB target health, and application errors. Determine whether failures occur at the edge or origin before changing configuration, and confirm recovery with successful CloudFront requests and a cleared `5xxErrorRate`.

## Action 4: Create the Dashboard

1. Switch to the project Region.
2. Open CloudWatch, Dashboards, and create or open `ThreeTierAppDashboard`.
3. Add the regional widgets below and explicitly keep their metric Region set to the project Region:

   ### Application Load Balancer

   - `RequestCount` using Sum
   - `TargetResponseTime` using Average and p95 if available
   - `HTTPCode_Target_5XX_Count` using Sum
   - `HealthyHostCount` and `UnHealthyHostCount`

   ### Auto Scaling and EC2

   - `GroupInServiceInstances`
   - `GroupDesiredCapacity`
   - `CPUUtilization` by Auto Scaling group
   - `NetworkIn` and `NetworkOut`

   ### RDS

   - `CPUUtilization`
   - `DatabaseConnections`
   - `FreeStorageSpace`
   - `ReadLatency` and `WriteLatency`

4. Add CloudFront metric widgets and explicitly select `us-east-1` as the metric Region. Select your distribution and the Region = Global metric dimension:

   ### CloudFront

   - `Requests` using Sum
   - `4xxErrorRate` using Average, displayed as percent
   - `5xxErrorRate` using Average, displayed as percent

5. Add alarm-status coverage for all seven alarms. If the console separates alarm widgets by Region, add the six project-Region alarms to one alarm-status widget and `3tier-app-cloudfront-5xx-rate` from `us-east-1` to a second widget.
6. Set the dashboard time range to the last 3 hours and save.
7. Generate one normal page load, wait for metric delivery, and confirm the CloudFront Requests widget becomes visible. Error-rate metrics can remain zero during healthy traffic.

## Action 5: Run the Functional Test

Use placeholder data only. If you completed the WAF bounded validation recently, first wait out its five-minute evaluation window.

1. Open the CloudFront URL over HTTPS.
2. Confirm events load from the database.
3. Open one event.
4. Create one booking with a fictitious name and `example.com` email address.
5. Refresh the page and confirm ticket availability changed.
6. Open `/health` and confirm database connected.
7. Check the ALB target group and confirm every expected target is Healthy.
8. Open CloudWatch Logs and confirm recent application requests appear without credentials.
9. Open `ThreeTierAppDashboard` and confirm CloudFront Requests reflects traffic through the distribution.
10. Confirm the CloudFront `4xxErrorRate` and `5xxErrorRate` widgets are present and `3tier-app-cloudfront-5xx-rate` is visible in `us-east-1`.

### Pass Criteria

The user interface, API, and database-backed create/read flow work through CloudFront, and CloudFront request/error visibility is present.

## Action 6: Run the Security and Isolation Test

Confirm each result and record Pass or Fail.

- [ ] CloudFront HTTP redirects to HTTPS: __________
- [ ] CloudFront HTTPS loads application: __________
- [ ] `3tier-app-web-acl` is associated with this distribution: __________
- [ ] `3tier-app-booking-rate-limit` is active with Block action: __________
- [ ] Rate rule uses source IP, five minutes, limit 20, and exact POST plus `/api/bookings` scope: __________
- [ ] Bounded WAF validation showed application `400` then WAF `403`, or documented review completed: __________
- [ ] Listener returned `403` before security-group restriction: __________
- [ ] Direct ALB access is now network-blocked or times out: __________
- [ ] EC2 instances have no public IPv4 address: __________
- [ ] RDS Publicly accessible is No: __________
- [ ] Application SG has no `0.0.0.0/0` inbound rule: __________
- [ ] Database SG allows `3306` only from application SG: __________
- [ ] No security group permits inbound SSH: __________
- [ ] S3 application bucket blocks public access: __________
- [ ] EC2 role cannot read the RDS master secret: __________
- [ ] Runtime database identity is `tickethub_app`: __________
- [ ] RDS connections use the downloaded CA bundle with hostname checking: __________
- [ ] CloudWatch logs contain no passwords or secret values: __________

> **Important:** Use the bounded evidence from Lecture 5; do not rerun traffic merely to fill this checklist. Do not test database isolation by opening port `3306` to the internet.

## Action 7: Run the Resilience Test

If you already completed the replacement test in the previous lecture, review the evidence. Otherwise:

1. Record the current desired capacity and healthy target count.
2. Terminate one Auto Scaling instance.
3. Observe Auto Scaling Activity launch a replacement.
4. Confirm the replacement becomes Healthy without master-secret access.
5. Confirm the CloudFront application still loads and database data remains.
6. Confirm CloudFront Requests continues to show viewer traffic and investigate any unexpected edge 5xx errors.

### Pass Criteria

The Auto Scaling group returns to desired capacity without rebuilding database data or granting master access, and the application remains visible through CloudFront.

## Optional Action 8: Run a Bounded Scale-Out Test

> **Warning:** Only perform this in your own sandbox or with instructor approval. Never direct an uncontrolled load generator at a public endpoint. Lecture 3 enabled detailed monitoring so CPU samples arrive every minute.

### Lab Mode With One Instance

1. Connect to the instance with Session Manager.
2. Run one bounded worker per detected vCPU for ten minutes:

   ```bash
   for i in $(seq 1 "$(nproc)"); do timeout 600 python3 -c 'while True: pass' & done; wait
   ```

3. Watch EC2 `CPUUtilization` and Auto Scaling Activity.
4. Allow for the one-minute metric cadence and 300-second instance warmup.
5. Confirm desired capacity can increase from 1 to 2.
6. Wait for the new target to become Healthy.
7. After the workload stops, confirm the group eventually scales back to minimum capacity.

### High-Availability Mode

Group CPU is averaged across all instances. Run the same bounded command on both current instances at approximately the same time, or use an instructor-approved distributed test. Do not exceed maximum capacity, and stop every process after ten minutes.

### Pass Criteria

The policy scales out under sustained group CPU load, registers a healthy target, and later scales in without dropping below minimum capacity.

## Action 9: Review Alarm Response Runbooks

For every alarm, verify the description answers:

- [ ] What does this alarm mean?
- [ ] What dashboard and log group should be checked first?
- [ ] What immediate action is safe?
- [ ] When should the issue be escalated?
- [ ] How will recovery be confirmed?

For `3tier-app-cloudfront-5xx-rate`, the first response must distinguish CloudFront/WAF behavior from ALB target or application failures and identify `3tier-app-edge-alarms` as the `us-east-1` notification path.

Monitoring without an owner and response is only data collection.

## Final Validation Checklist

- [ ] Network tiers and route isolation verified: __________
- [ ] RDS encryption and backups verified: __________
- [ ] Application health and create/read flow verified: __________
- [ ] All ALB targets healthy: __________
- [ ] CloudFront HTTPS, dynamic requests, and metric visibility verified: __________
- [ ] WAF association and booking rate rule verified: __________
- [ ] Direct origin blocked: __________
- [ ] Both SNS test messages delivered: __________
- [ ] Seven alarms present across the project Region and `us-east-1`: __________
- [ ] Dashboard populated with regional and CloudFront widgets: __________
- [ ] Auto Scaling replacement verified: __________
- [ ] Scale-out verified or documented as not performed: __________

## Troubleshooting

### A Regional Alarm Stays in Insufficient Data

Confirm the resource dimension and project Region. Some metrics are emitted only when requests occur.

### The CloudFront Alarm or Widgets Have No Data

Select `us-east-1` for `AWS/CloudFront` metrics, choose your DistributionId, and use the Region = Global metric dimension. Generate one normal page load and allow time for metric delivery.

### The CloudFront Alarm Cannot Use the Selected SNS Topic

Alarm actions must be in the alarm Region. In `us-east-1`, confirm the Standard topic is named `3tier-app-edge-alarms` and its email subscription is Confirmed. Do not select `3tier-app-alarms` from another Region.

### SNS Notifications Do Not Arrive

Check the topic in the correct Region, confirm the subscription, check spam filtering, and publish another harmless test message.

### The WAF Rate Rule Is Missing or Does Not Show Blocked Requests

Open the CloudFront-scope `3tier-app-web-acl`, confirm its distribution association and active status, then verify `3tier-app-booking-rate-limit` is enabled with Block action and sampled requests. Do not run additional unbounded traffic; reuse the Lecture 5 bounded procedure only when its evaluation window has expired and classroom coordination permits it.

### The Application Log Group Is Missing

Check the CloudWatch agent status and `/var/log/user-data.log`. Confirm the EC2 role includes `CloudWatchAgentServerPolicy`.

### Metrics Appear on the Wrong Resource

Recreate the widget or alarm using both the LoadBalancer and TargetGroup dimensions where required, and verify regional metrics use the project Region while CloudFront metrics use `us-east-1`.

### Scale-Out Does Not Occur

Check the target-tracking policy, average CPU across the entire group, warmup, maximum capacity, and whether the workload lasted long enough.

## Knowledge Check

1. Why does the CloudFront alarm use a separate SNS topic?

   **Expected answer:** The alarm is created in `us-east-1` for CloudFront metrics, and its SNS alarm action must be in the same Region.

2. What does a healthy ALB target prove?

   **Expected answer:** The load balancer can reach the application health endpoint and the endpoint’s dependency checks pass.

3. Why must rate and load testing be bounded?

   **Expected answer:** Uncontrolled traffic can create cost, instability, shared-IP blocking, and unintended traffic impact.

## Next Lecture

Turn your implementation evidence into an architecture explanation, Well-Architected review, and final demonstration.
