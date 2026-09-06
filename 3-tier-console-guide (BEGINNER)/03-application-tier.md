# Deploy the Application Tier on Private EC2 Instances

## Estimated Time

75–100 minutes

## Lecture Outcome

You will publish the downloadable application assets to a private S3 bucket, create a least-privilege EC2 role, bootstrap a schema-scoped database user over verified TLS, and launch an Auto Scaling group in private subnets.

## Downloadable Udemy Resources

Attach these four files from the `course-resources` folder to this lecture:

- `app.py`
- `index.html`
- `requirements.txt`
- `user-data.sh`

Learners should download all four before starting. The `app.py` supplied here intentionally differs from older TicketHub examples: it verifies the RDS certificate, uses a scoped runtime identity, returns generic errors, validates booking input, and does not expose a public booking-details endpoint containing customer information.

## Prerequisites

- RDS status is Available.
- You recorded the RDS master-secret ARN and `3tier-app/runtime-db` secret ARN.
- You downloaded all four Lecture 3 resources.
- The NAT Gateway is Available.

## Cost Impact

> **Cost warning:** S3, EC2, EBS, NAT data processing, Secrets Manager, and CloudWatch Logs can create charges. Use the small instance class approved for your lab.

## Action 1: Create a Private Application-Asset Bucket

S3 bucket names are globally unique. Replace the placeholders with your account ID and Region, or another unique suffix.

1. Open S3 and choose Create bucket.
2. Configure:

   | Setting | Value |
   |---|---|
   | Bucket name | `3tier-app-assets-<ACCOUNT_ID>-<REGION>` |
   | Region | Your project Region |
   | Object Ownership | ACLs disabled |
   | Block Public Access | Keep every option enabled |
   | Bucket Versioning | Enable if your lab permits the small additional storage cost |
   | Default encryption | Amazon S3 managed keys |

3. Add the standard tags and create the bucket.
4. Create a folder named `ticket-booking`.
5. Upload `app.py`, `index.html`, and `requirements.txt` to `ticket-booking/`.
6. Do not upload `user-data.sh` to S3 and do not make any object public.

Asset bucket name: ______________________________

## Checkpoint

The three application files are under `ticket-booking/` and Block Public Access is enabled.

## Action 2: Create the EC2 IAM Role

1. Open IAM, choose Roles, and Create role.
2. Select AWS service and EC2.
3. Add:

   - `AmazonSSMManagedInstanceCore`
   - `CloudWatchAgentServerPolicy`

4. Name the role `3tier-app-ec2-role` and create it.
5. Add an inline policy using the JSON below.
6. Replace the bucket and both secret ARN placeholders.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadApplicationAssets",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<YOUR_ASSET_BUCKET>/ticket-booking/*"
    },
    {
      "Sid": "ReadDatabaseSecretsDuringBootstrap",
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": [
        "<YOUR_RDS_MASTER_SECRET_ARN>",
        "<YOUR_RUNTIME_SECRET_ARN>"
      ]
    }
  ]
}
```

7. Name it `3tier-app-read-assets-and-db-secrets`.
8. Save it.

### Security Note

> **Security note:** Master-secret access is temporary. You will remove it after the first instance creates `tickethub_app` with `appdb`-scoped permissions.

## Action 3: Customize the Downloaded User Data

1. Open the downloaded `user-data.sh` in a plain-text editor.
2. Replace all four values at the top:

   | Setting | Value |
   |---|---|
   | `ASSET_BUCKET` | Your private S3 bucket name |
   | `MASTER_SECRET_ARN` | The RDS-managed master-secret ARN |
   | `RUNTIME_SECRET_ARN` | The `3tier-app/runtime-db` ARN |
   | `AWS_REGION` | Your Region code, such as `eu-west-1` |

3. Search the entire file for `<YOUR_`.
4. Do not continue if any placeholder remains.
5. Never paste either secret value or database password into the script.

### What the Script Does

- Downloads only the three application files allowed by the role.
- Downloads the AWS RDS global CA bundle.
- Uses verified TLS for bootstrap and runtime database connections.
- Validates that the runtime username is `tickethub_app` and tries the runtime identity first.
- Uses the master identity only when MySQL reports runtime authentication denial with error `1045`.
- Grants `tickethub_app` permissions only on `appdb`.
- Starts Gunicorn through systemd on port `5000`.
- Sends application and user-data logs to CloudWatch Logs.

### Teaching Compromise

> **Note:** `tickethub_app` has schema-scoped DDL permissions because this sample initializes its tables at startup. Production systems should use a separate migration identity and a CRUD-only runtime identity.

## Checkpoint

Exactly four placeholders have been replaced, and the file contains no password or secret value.

## Action 4: Create the Launch Template

1. Open EC2, Launch Templates, and Create launch template.
2. Configure:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-launch-template` |
   | Description | Private TicketHub application instances |
   | Auto Scaling guidance | Enabled |
   | AMI | Current Amazon Linux 2023 AMI from Quick Start |
   | Instance type | A small burstable type approved for your account |
   | Key pair | Proceed without a key pair |
   | Security group | `3tier-app-app-sg` |
   | IAM instance profile | `3tier-app-ec2-role` |

3. Do not assign a public IPv4 address.
4. Configure the root EBS volume as encrypted with Delete on termination enabled.
5. In Advanced details:

   | Setting | Value |
   |---|---|
   | Metadata version or HTTP tokens | IMDSv2 required |
   | Detailed CloudWatch monitoring | Enabled for one-minute CPU data |
   | User data | Paste the complete customized `user-data.sh` content |

6. Add the standard tags to instances and volumes.
7. Create the launch template.

### Security Note

> **Security note:** Session Manager replaces inbound SSH. The application security group must have no port `22` rule.

## Action 5: Create the Auto Scaling Group

1. Open Auto Scaling Groups and choose Create Auto Scaling group.
2. Configure:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-asg` |
   | Launch template | `3tier-app-launch-template` |
   | Version | Default |
   | VPC | `3tier-app-vpc` |
   | Subnets | `3tier-app-private-1a` and `3tier-app-private-1b` only |

3. Do not attach a load balancer yet.
4. Use EC2 health checks initially and a 300-second grace period.
5. Start with:

   | Setting | Value |
   |---|---|
   | Desired | 1 |
   | Minimum | 1 |
   | Maximum | 2 in LAB MODE or 6 in HIGH-AVAILABILITY MODE |

6. Add the standard tags, propagate them to instances, and create the group.

### Why Start With One Instance

The first launch creates the scoped database user and initializes tables. Later instances connect with that existing user.

## Action 6: Verify the Private Instance

Wait approximately 5–10 minutes.

1. Open EC2 Instances and select the instance created by `3tier-app-asg`.
2. Confirm it has a private address and no public IPv4 address.
3. Choose Connect, Session Manager, and Connect.
4. Run:

   ```bash
   sudo systemctl status tickethub --no-pager
   curl -s http://localhost:5000/health
   sudo tail -n 50 /var/log/tickethub.log
   sudo tail -n 50 /var/log/user-data.log
   ```

5. Confirm `/health` reports healthy and database connected.
6. Confirm the logs say the runtime user exists or was created with `appdb`-scoped permissions.
7. Confirm no log line displays either password.
8. Open CloudWatch Logs and confirm:

   - `/3tier-app/application`
   - `/3tier-app/user-data`

## Action 7: Remove Master-Secret Access

> **Important:** Do not skip this least-privilege step.

1. Open IAM and select `3tier-app-ec2-role`.
2. Edit `3tier-app-read-assets-and-db-secrets`.
3. Remove only the actual RDS master-secret ARN from the Resource list.
4. Keep the actual `3tier-app/runtime-db` ARN.
5. Rename the statement ID to `ReadRuntimeDatabaseSecret` if desired.
6. Save the policy.
7. Confirm the policy no longer grants the EC2 role access to the master secret.

Future instances run the runtime connection check first. Because `tickethub_app` now exists, they do not need the master identity. If the runtime user is accidentally removed, new instances fail closed rather than regaining master access.

## Action 8: Verify Replacement Safety

1. In Auto Scaling, temporarily increase Desired capacity from 1 to 2.
2. Wait for the second instance to enter InService.
3. Use Session Manager or CloudWatch Logs to confirm its `/health` response succeeds without master-secret access.
4. Return Desired capacity to 1 in LAB MODE. Leave Desired capacity at 2 in HIGH-AVAILABILITY MODE.

## Checkpoint

The application runs in a private subnet, connects to RDS with verified TLS using `tickethub_app`, and the EC2 role can no longer read the RDS master secret.

## Troubleshooting

### Session Manager Is Unavailable

Confirm `AmazonSSMManagedInstanceCore` is attached, NAT is Available, and outbound HTTPS is allowed.

### S3 Copy Returns AccessDenied

Check the bucket name, object path, role attachment, and object ARN ending in `/ticket-booking/*`.

### Bootstrap Returns AccessDenied

Before the first successful bootstrap only, confirm both exact secret ARNs are in the inline policy. Do not add wildcard secret access.

### TLS Connection Fails

Confirm `global-bundle.pem` downloaded successfully, the runtime secret host is the exact RDS endpoint, and the system clock is correct.

### Health Returns Unhealthy

Inspect both log files. Confirm RDS is Available, port `3306` is allowed from `3tier-app-app-sg`, and the runtime secret contains username, password, host, port, and dbname.

### A Replacement Fails After Master Access Is Removed

Verify `tickethub_app` still exists and its runtime secret matches. Restore the scoped user deliberately; do not permanently restore master access to every instance.

## Knowledge Check

1. Why is master access removed after bootstrap?

   **Expected answer:** The application needs only schema-scoped runtime permissions, so retaining master access violates least privilege.

2. How is the RDS server identity verified?

   **Expected answer:** PyMySQL validates the RDS hostname with the AWS RDS CA bundle.

3. Why does the EC2 instance have no public IP or SSH rule?

   **Expected answer:** User traffic enters through the ALB, and administration uses Session Manager.

## Save These Values

- Asset bucket: ______________________________
- IAM role ARN: ______________________________
- Launch template ID: ______________________________
- Auto Scaling group: `3tier-app-asg`
- Initial EC2 instance ID: ______________________________
- Master-secret access removed: Yes / No

## Next Lecture

Create the target group and ALB, attach Auto Scaling, and configure CPU-based scaling.
