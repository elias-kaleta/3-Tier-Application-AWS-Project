# Add the Application Load Balancer and Auto Scaling

## Estimated Time

45–60 minutes

## Lecture Outcome

You will create an application target group, deploy an internet-facing Application Load Balancer across two public subnets, attach it to the Auto Scaling group, and configure target-tracking scaling.

## Prerequisites

- The first application instance returns healthy from `http://localhost:5000/health`.
- The ALB and application security groups already exist.
- The Auto Scaling group runs in the two private subnets.

## Cost Impact

> **Cost warning:** The Application Load Balancer, processed capacity, EC2 instances, and public IPv4 addresses are billable. Scaling tests can launch additional instances.

## Action 1: Create the Target Group

1. Open EC2 and choose Target Groups under Load Balancing.
2. Choose Create target group.
3. Configure:

   | Setting | Value |
   |---|---|
   | Target type | Instances |
   | Name | `3tier-app-target-group` |
   | Protocol | HTTP |
   | Port | `5000` |
   | IP address type | IPv4 |
   | VPC | `3tier-app-vpc` |
   | Protocol version | HTTP1 |

4. Configure health checks:

   | Setting | Value |
   |---|---|
   | Health check protocol | HTTP |
   | Health check path | `/health` |
   | Port | Traffic port |
   | Healthy threshold | 2 |
   | Unhealthy threshold | 3 |
   | Timeout | 5 seconds |
   | Interval | 30 seconds |
   | Success codes | `200` |

5. Add the standard tags.
6. Continue without manually registering the current instance. The Auto Scaling group will manage registration.
7. Create the target group.

### Why

Manual registration would not automatically include replacement or scaled-out instances. Auto Scaling integration keeps membership current.

## Action 2: Create the Application Load Balancer

1. Choose Load Balancers and Create load balancer.
2. Select Application Load Balancer.
3. Configure:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-alb` |
   | Scheme | Internet-facing |
   | IP address type | IPv4 |
   | VPC | `3tier-app-vpc` |
   | Mappings | Select AZ A/public subnet A and AZ B/public subnet B |
   | Security group | `3tier-app-alb-sg` |
   | Listener | HTTP on port `80` |
   | Default action | Forward to `3tier-app-target-group` |

4. Remove the default security group if the console selected it.
5. Add the standard tags.
6. Create the load balancer.
7. Wait until its state is Active.

## Checkpoint

The ALB is Active and has nodes in both public subnets.

## Action 3: Attach the Target Group to Auto Scaling

1. Open Auto Scaling Groups.
2. Select `3tier-app-asg`.
3. Open Integrations or Load balancing and choose Edit.
4. Attach `3tier-app-target-group`.
5. Enable Elastic Load Balancing health checks.
6. Keep the health-check grace period at 300 seconds.
7. Save changes.
8. Open the target group’s Targets tab.
9. Wait until the application instance becomes Healthy.

If the target is still Initial after several checks, continue to troubleshooting before changing capacity.

## Action 4: Test the ALB

1. Open the ALB details and copy its DNS name.
2. Open this URL in a browser:

   `http://<ALB_DNS_NAME>`

3. Confirm the application page loads.
4. Open:

   `http://<ALB_DNS_NAME>/health`

5. Confirm the response reports healthy and database connected.
6. Use the application to view events and create one test booking with placeholder customer information.

> **Privacy note:** Do not enter real personal information in a training application.

## Checkpoint

The browser reaches the private EC2 application through the public ALB, and one CRUD operation reaches RDS.

## Action 5: Set the Final Auto Scaling Capacity

1. Open `3tier-app-asg` and edit capacity.
2. Set values for your selected mode:

   ### Lab Mode

   | Setting | Value |
   |---|---|
   | Minimum | 1 |
   | Desired | 1 |
   | Maximum | 2 |

   ### High-Availability Mode

   | Setting | Value |
   |---|---|
   | Minimum | 2 |
   | Desired | 2 |
   | Maximum | 6 |

3. Save changes.
4. If using HIGH-AVAILABILITY MODE, wait for the second target to become Healthy.

## Action 6: Create a Target-Tracking Scaling Policy

1. Open the Automatic scaling tab.
2. Choose Create dynamic scaling policy.
3. Select Target tracking.
4. Enter:

   | Setting | Value |
   |---|---|
   | Policy name | `3tier-app-cpu-target-tracking` |
   | Metric type | Average CPU utilization |
   | Target value | 70 |
   | Instance warmup | 300 seconds |
   | Scale in | Enabled |

5. Create the policy.

### Why

Target tracking adjusts capacity to keep average CPU near a goal. The 70% value is a learning baseline, not a universal production threshold.

## Action 7: Test Instance Replacement

> **Important:** This is a controlled resilience test, not a production procedure.

1. Record the current instance ID.
2. In EC2, terminate one instance that belongs to `3tier-app-asg`.
3. Return to Auto Scaling Group Activity.
4. Observe Auto Scaling launch a replacement to restore desired capacity.
5. Open the target group and wait for the replacement target to become Healthy.
6. Refresh the ALB application URL.

**Expected result:** the application becomes or remains available, and data persists because it is stored in RDS.

## Checkpoint

Desired capacity is restored, every expected target is Healthy, and the application still displays database-backed data.

## Save These Values

- Target group ARN: ______________________________
- ALB ARN: ______________________________
- ALB DNS name: ______________________________
- Current healthy target count: ______________________________
- Scaling policy name: `3tier-app-cpu-target-tracking`

## Troubleshooting

### Target Is Unhealthy With Timeout

Confirm `3tier-app-app-sg` permits TCP `5000` from `3tier-app-alb-sg` and the service listens on `0.0.0.0:5000`.

### Target Returns HTTP 500

Use Session Manager and inspect `/var/log/tickethub.log`. A database or secret error makes the supplied `/health` endpoint return `500`.

### The ALB Page Times Out

Confirm the ALB is Active, its public subnets use the public route table, and its security group temporarily allows inbound HTTP from `0.0.0.0/0`.

### The Replacement Instance Never Becomes Healthy

Inspect Auto Scaling Activity for launch errors and the instance’s `/var/log/user-data.log` through Session Manager or CloudWatch Logs.

### Only One Target Appears in High-Availability Mode

Confirm Desired and Minimum are 2 and both private subnets are selected in the Auto Scaling group.

## Knowledge Check

1. Why does Auto Scaling attach the target group instead of registering instances manually?

   **Expected answer:** New and replacement instances are registered and deregistered automatically.

2. What is the purpose of `/health`?

   **Expected answer:** It lets the load balancer determine whether the application and its database dependency are ready to receive traffic.

3. What survives when an application instance is replaced?

   **Expected answer:** Database state in RDS and application assets in S3; the EC2 instance itself is disposable.

## Next Lecture

Place CloudFront in front of the ALB, force viewer HTTPS, and block direct origin access.
