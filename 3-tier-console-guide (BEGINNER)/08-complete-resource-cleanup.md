# Delete the Complete Lab and Stop Ongoing Charges

## Estimated Time

45–90 minutes, including service wait times

## Lecture Outcome

You will remove the project in dependency order, make deliberate snapshot, secret, and budget-retention decisions, and verify that no expected billable resources remain.

## Warning

> **Warning:** This lecture deletes the lab application and its data. Deletion is irreversible unless you deliberately retain a tested snapshot or backup. Confirm that you are in the training account and correct Region before each action. Never use these steps against a production environment.

## Before You Delete

- Account or sandbox name: ______________________________
- Account ID last four digits: ______________________________
- Project Region: ______________________________
- Required screenshots exported: Yes / No
- Presentation complete: Yes / No
- Need to retain database data: Yes / No
- Approved by instructor or account owner if required: Yes / No

> **Warning:** If you are uncertain whether a resource is part of a production workload, stop and ask the owner.

## Action 1: Stop Test Traffic

1. Stop all CPU or load-generation commands.
2. Close test clients and scripts.
3. Export the final architecture evidence.
4. Record the resource IDs from earlier lectures.

## Action 2: Disassociate and Delete WAF, Then Delete CloudFront

> **Important:** AWS WAF is part of the baseline lab. The only exception is a documented course record showing that an instructor explicitly omitted it for this environment.

1. Open CloudFront and select the project distribution.
2. Confirm that `3tier-app-web-acl` is associated with the distribution.
3. Edit the distribution and disassociate `3tier-app-web-acl`.
4. Wait until the disassociation update is Deployed.
5. Open AWS WAF in the CloudFront scope.
6. Select `3tier-app-web-acl` and delete its `3tier-app-booking-rate-limit` rule, then delete the Web ACL. If the console deletes rules with the Web ACL, verify that both names disappear.
7. Disable the CloudFront distribution.
8. Wait until the disable update is Deployed.
9. Delete the distribution.
10. If an instructor explicitly omitted WAF, record the instructor or course reference and mark only the WAF steps as not applicable; do not assume omission merely because the resources are hard to find.
11. If you created Route 53 records solely for this project, remove them only after confirming they are not shared.
12. If you created an ACM viewer certificate solely for this project, delete it only after CloudFront no longer uses it and after confirming it is not shared.

- CloudFront deletion confirmed: __________
- `3tier-app-web-acl` and `3tier-app-booking-rate-limit` deleted: __________
- Instructor-approved WAF omission reference, if applicable: ______________________________

## Action 3: Delete Load-Balancing Resources

1. Open EC2 Load Balancers.
2. Select `3tier-app-alb` and delete it.
3. Wait until the load balancer and its listeners disappear.
4. If you created a regional ACM certificate for the ALB origin, delete it only after the ALB and listener are deleted and after confirming the certificate is not shared.
5. Open Target Groups.
6. Delete `3tier-app-target-group`.

If the target group reports that it is still in use, wait for ALB deletion to finish and try again.

- ALB deleted: __________
- Target group deleted: __________

## Action 4: Delete Auto Scaling and EC2 Resources

1. Open Auto Scaling Groups.
2. Select `3tier-app-asg`.
3. Set Desired, Minimum, and Maximum capacity to 0 if the console requires it.
4. Delete the Auto Scaling group.
5. Wait until its EC2 instances terminate.
6. Open EC2 Instances and confirm no project instances remain.
7. Open Launch Templates and delete `3tier-app-launch-template` and all of its versions.
8. Open Volumes and confirm project EBS volumes marked Delete on termination are gone.

> **Warning:** Do not manually terminate unrelated instances or delete unrelated volumes.

- Auto Scaling group deleted: __________
- Project EC2 instances gone: __________
- Launch template deleted: __________
- Project EBS volumes gone: __________

## Action 5: Delete the RDS Database

Make a deliberate retention choice.

### If You Need the Data

> **Cost warning:** Create a final snapshot with a unique name, document its owner and deletion date, and understand that retained snapshots can continue to incur storage charges.

### If You Do Not Need the Data

> **Warning:** Skip the final snapshot and acknowledge that the data cannot be recovered.

1. Open RDS Databases.
2. Select `3tier-app-database`.
3. Choose Delete.
4. Select or clear Create final snapshot according to your decision.
5. Choose whether to retain automated backups according to the course policy.
6. Confirm deletion.
7. Wait until the database disappears.
8. Open Snapshots and delete unneeded manual or final snapshots.
9. Open Subnet groups and delete `3tier-app-db-subnet-group`.

- RDS database deleted: __________
- Snapshot retained with owner/date, or all snapshots deleted: __________
- DB subnet group deleted: __________

## Action 6: Delete Database Secrets

1. Open Secrets Manager.
2. Select `3tier-app/runtime-db` and schedule it for deletion using the normal recovery window required by your organization.
3. Search for the RDS-managed master secret associated with `3tier-app-database`. RDS may remove this managed secret automatically when the database is deleted.
4. If the RDS-managed master secret remains, schedule it for deletion using the normal recovery window required by your organization.
5. Do not force immediate deletion merely to speed up the lab.

> **Cost warning:** A secret scheduled for deletion can remain billable during its recovery window. Always schedule `3tier-app/runtime-db` separately, and record the final deletion dates for every secret that remains long enough to schedule.

- Master secret automatically removed or deletion date: ______________________________
- Runtime secret deletion date: ______________________________

## Action 7: Delete Monitoring and Notifications

1. Switch to the project Region and open CloudWatch Alarms.
2. Delete these six regional alarms:

   - `3tier-app-unhealthy-targets`
   - `3tier-app-target-5xx`
   - `3tier-app-high-latency`
   - `3tier-app-high-app-cpu`
   - `3tier-app-high-db-cpu`
   - `3tier-app-low-db-storage`

3. In the project Region, delete `ThreeTierAppDashboard`.
4. In the project Region, open CloudWatch Log groups and delete `/3tier-app/application` and `/3tier-app/user-data` if retention is not required.
5. In the project Region, open SNS and delete `3tier-app-alarms`. Its subscription is removed with the topic.
6. Switch to `us-east-1` and delete the seventh alarm, `3tier-app-cloudfront-5xx-rate`.
7. In `us-east-1`, open SNS and delete `3tier-app-edge-alarms`. Its subscription is removed with the topic.
8. Delete any project-only Flow Logs or CloudTrail trails created as optional extensions. Preserve organization trails and shared audit logs.

- Six project-Region alarms deleted: __________
- `us-east-1` CloudFront alarm deleted: __________
- Seven total alarms deleted: __________
- Dashboard deleted: __________
- Log groups deleted or retained with owner/date: __________
- `3tier-app-alarms` deleted in project Region: __________
- `3tier-app-edge-alarms` deleted in `us-east-1`: __________

## Action 8: Empty and Delete the S3 Asset Bucket

1. Open S3 and select the project asset bucket.
2. Confirm its name matches the bucket recorded in Lecture 3.
3. Empty the bucket, including object versions and delete markers if versioning was enabled.
4. Delete the bucket.

> **Warning:** Do not delete a shared course or instructor bucket.

Asset bucket deleted: __________

## Action 9: Delete IAM Resources

1. Open IAM Roles.
2. Select `3tier-app-ec2-role`.
3. Confirm no non-project instance profile or workload uses it.
4. Delete the role and its inline policy.
5. Do not delete AWS service-linked roles or shared organization roles merely because they appeared during the lab.

EC2 role deleted: __________

## Action 10: Delete Security Groups

> **Important:** Wait for ALB, EC2, and RDS network interfaces to disappear before this step.

Delete in this order:

1. `3tier-app-db-sg`
2. `3tier-app-app-sg`
3. `3tier-app-alb-sg`

If a group is in use, open Network Interfaces in EC2 and identify the dependency. Do not delete an unrelated interface.

Security groups deleted: __________

## Action 11: Delete the NAT Gateway and Release Its Elastic IP

1. Open VPC NAT Gateways.
2. Select `3tier-app-nat-1a` and delete it.
3. Wait until its state is Deleted.
4. Open EC2 Elastic IP addresses.
5. Select the allocation recorded for this project.
6. Release the Elastic IP address.

- NAT Gateway deleted: __________
- Elastic IP released: __________

## Action 12: Delete Subnets, Route Tables, Gateway, and VPC

> **Important:** The three custom route tables are explicitly associated with subnets. Delete the subnets first so AWS removes those associations.

1. Delete all six project subnets.
2. Delete the project’s three non-main route tables:

   - `3tier-app-public-rt`
   - `3tier-app-private-rt`
   - `3tier-app-db-rt`

3. Detach `3tier-app-igw` from `3tier-app-vpc`.
4. Delete `3tier-app-igw`.
5. Delete `3tier-app-vpc`.

The VPC main route table, default network ACL, and default security group disappear with the VPC.

- Six subnets deleted: __________
- Route tables deleted: __________
- Internet Gateway detached and deleted: __________
- VPC deleted: __________

## Action 13: Verify Every Service, Region, and Account-Level Resource

Search by the Project tag and the `3tier-app` prefix. Check at least:

- [ ] EC2 instances, volumes, snapshots, load balancers, target groups, launch templates, Elastic IPs, and Auto Scaling groups
- [ ] RDS databases, snapshots, subnet groups, and retained automated backups
- [ ] VPCs, NAT Gateways, network interfaces, security groups, and Flow Logs
- [ ] CloudFront distributions
- [ ] CloudFront-scope WAF Web ACLs and rules, including `3tier-app-web-acl` and `3tier-app-booking-rate-limit`
- [ ] CloudWatch alarms, dashboards, and log groups
- [ ] SNS topics, including `3tier-app-alarms` in the project Region and `3tier-app-edge-alarms` in `us-east-1`
- [ ] S3 buckets
- [ ] Secrets Manager secrets pending deletion
- [ ] AWS Budgets in Billing and Cost Management
- [ ] Route 53 records and ACM certificates if the end-to-end TLS extension was completed

Repeat regional checks in every Region you used, explicitly including the project Region and `us-east-1`. CloudFront, CloudFront-scope AWS WAF, IAM, and AWS Budgets are global or account-level views.

## Action 14: Verify Billing and Decide the Budget Disposition

1. Open Billing and Cost Management.
2. Review current month charges by service and Region.
3. Open Cost Explorer if available and filter by the Project tag.
4. Remember that usage and cost data can be delayed.
5. Recheck the next day or after your organization’s required billing-delay interval.
6. If charges continue, identify the service and Region before deleting anything else.
7. After the delayed billing recheck, open AWS Budgets and locate `3tier-app-monthly-budget`, the cost budget created during preflight.
8. Confirm whether `3tier-app-monthly-budget` is project-only and verify with its owner that it is not shared with another course, workload, or account process.
9. Make and record one deliberate choice:

   - Delete the project-only budget after it is no longer needed and after confirming it is not shared; or
   - Retain it only with a documented owner and continuing purpose.

> **Warning:** Do not delete a shared or organization-managed budget.

## Final Cleanup Checkpoint

- [ ] No project EC2 instances or EBS volumes: __________
- [ ] No project load balancer or target group: __________
- [ ] No project RDS instance: __________
- [ ] Snapshots intentionally retained or removed: __________
- [ ] No project NAT Gateway or Elastic IP: __________
- [ ] No CloudFront distribution: __________
- [ ] No `3tier-app-web-acl` or `3tier-app-booking-rate-limit`, or instructor omission documented: __________
- [ ] No project S3 bucket: __________
- [ ] Seven alarms deleted across the project Region and `us-east-1`: __________
- [ ] Both SNS topics deleted in their correct Regions: __________
- [ ] No unintended log groups: __________
- [ ] Secrets retention documented: __________
- [ ] Billing checked today: __________
- [ ] Billing recheck date and result: ______________________________
- [ ] Budget disposition: Deleted / Retained with documented owner and purpose
- [ ] Budget owner and purpose if retained: ______________________________

## Troubleshooting

### A VPC Cannot Be Deleted

Use the VPC resource map and EC2 Network Interfaces to find remaining dependencies such as NAT Gateways, load balancers, RDS interfaces, endpoints, or security groups.

### A Security Group Cannot Be Deleted

Another group may reference it, or a network interface may still use it. Wait for service deletion and inspect dependencies.

### The WAF Web ACL Cannot Be Deleted

Confirm `3tier-app-web-acl` is disassociated from the CloudFront distribution and that the distribution update is Deployed. Then remove `3tier-app-booking-rate-limit` and delete the Web ACL in the CloudFront scope.

### The S3 Bucket Is Not Empty

Delete object versions and delete markers as well as current objects.

### The Database Subnet Group Is in Use

Wait until RDS deletion and retained-backup processing complete.

### An Alarm or SNS Topic Is Missing During Cleanup

Check both required Regions: the six regional alarms and `3tier-app-alarms` are in the project Region; `3tier-app-cloudfront-5xx-rate` and `3tier-app-edge-alarms` are in `us-east-1`.

### The Project Budget Might Be Shared

Do not delete it. Confirm with the owner, then either document its continuing owner and purpose or return later when its scope is clear.

### Charges Remain After Cleanup

Billing data may be delayed. Check Cost Explorer by service and Region, inspect retained snapshots and secrets, verify AWS WAF and both SNS/CloudWatch Regions, and contact AWS Support for account-specific billing questions.

## Knowledge Check

1. Why is the NAT Gateway deleted before the VPC?

   **Expected answer:** It creates network interfaces and dependencies that prevent VPC deletion and continues to incur charges.

2. Why must final snapshots be a deliberate choice?

   **Expected answer:** They preserve recoverable data but can continue to incur storage charges and need an owner and deletion date.

3. Why must the budget have an explicit disposition?

   **Expected answer:** A project-only budget can be removed after its delayed billing check, while a shared or still-needed budget must remain with a documented owner and purpose.

4. When is the project truly complete?

   **Expected answer:** After the application is demonstrated, resources are removed, billing is checked again after usage data has updated, and the budget disposition is recorded.

## Course Complete

You designed, built, secured, monitored, validated, explained, and removed a complete three-tier AWS teaching architecture.
