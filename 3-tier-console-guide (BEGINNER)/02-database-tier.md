# Create the Security Boundary and Database Tier

## Estimated Time

45–75 minutes, including RDS creation time

## Lecture Outcome

You will create three security groups, an RDS subnet group, a private encrypted MySQL database, managed credentials, automated backups, and database monitoring.

## Prerequisites

- The network foundation is complete.
- You have selected LAB MODE or HIGH-AVAILABILITY MODE.
- You have current permission to use RDS, EC2 security groups, Secrets Manager, and IAM service-linked roles.

## Cost Impact

> **Cost warning:** RDS compute, storage, backups beyond included allowances, public IPv4 usage, enhanced monitoring, and Multi-AZ capacity can create charges. Multi-AZ normally costs substantially more than Single-AZ. Check current prices in your account and Region.

## Action 1: Create the ALB Security Group

1. Open the EC2 or VPC console and choose Security Groups.
2. Choose Create security group.
3. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-alb-sg` |
   | Description | Allows web traffic to the application load balancer |
   | VPC | `3tier-app-vpc` |

4. Add one temporary inbound rule:

   | Setting | Value |
   |---|---|
   | Type | HTTP |
   | Port | `80` |
   | Source | Anywhere-IPv4, `0.0.0.0/0` |
   | Description | Temporary public test access; restricted after CloudFront setup |

5. Leave the default outbound rule for now.
6. Add the standard tags and create the group.

### Security Note

> **Security note:** The public inbound rule is temporary. In the CloudFront lecture, you will restrict the source and require a private origin-verification header.

## Action 2: Create the Application Security Group

1. Create another security group.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-app-sg` |
   | Description | Allows application traffic from the ALB only |
   | VPC | `3tier-app-vpc` |

3. Add this inbound rule:

   | Setting | Value |
   |---|---|
   | Type | Custom TCP |
   | Port | `5000` |
   | Source | Security group, `3tier-app-alb-sg` |
   | Description | Application traffic from ALB only |

4. Keep the default outbound rule. The instances need outbound HTTPS for Systems Manager, Secrets Manager, S3, package repositories, and CloudWatch through the NAT Gateway.
5. Add the standard tags and create the group.

## Action 3: Create the Database Security Group

1. Create a third security group.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-db-sg` |
   | Description | Allows MySQL from the application tier only |
   | VPC | `3tier-app-vpc` |

3. Add this inbound rule:

   | Setting | Value |
   |---|---|
   | Type | MySQL/Aurora |
   | Port | `3306` |
   | Source | Security group, `3tier-app-app-sg` |
   | Description | MySQL from application instances only |

4. Remove the default outbound rule if the console allows it. RDS database connections are initiated by the application, so this lab does not require database-initiated outbound traffic.
5. Add the standard tags and create the group.

### Why Security-Group References Matter

The rules trust workload identity through security-group membership rather than changing private IP addresses. Never open MySQL port `3306` to `0.0.0.0/0`.

## Checkpoint

The traffic chain is ALB security group to application security group on port `5000`, then application security group to database security group on port `3306`.

## Action 4: Create the DB Subnet Group

1. Open the RDS console.
2. Choose Subnet groups.
3. Choose Create DB subnet group.
4. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-db-subnet-group` |
   | Description | Isolated subnets for the three-tier application database |
   | VPC | `3tier-app-vpc` |

5. Select AZ A and AZ B.
6. Select only the subnets with CIDRs `10.0.21.0/24` and `10.0.22.0/24`.
7. Add the standard tags.
8. Create the group.

## Checkpoint

The subnet group contains exactly two database subnets in two different Availability Zones.

## Action 5: Create the RDS MySQL Database

> **Note:** Console labels change over time. Match the setting’s purpose if its exact label differs.

1. In RDS, choose Databases and Create database.
2. Select Standard create.
3. Configure:

   | Setting | Value |
   |---|---|
   | Engine | MySQL |
   | Engine version | A currently supported MySQL 8.0 version available in your Region |
   | Template | Dev/Test or the lowest-cost eligible option shown in your account |
   | DB instance identifier | `3tier-app-database` |
   | Initial database name | `appdb` |
   | Master username | `admin` |

4. For credentials management, choose Manage master credentials in AWS Secrets Manager if offered.
5. Let RDS generate the password. Do not place a database password in course notes, screenshots, user data, or source code.
6. Select a small burstable DB instance class that is currently offered in your Region and suitable for the lab.
7. Select General Purpose SSD storage and 20 GiB, or the lowest supported allocation shown by the console.
8. Leave storage autoscaling disabled for a short controlled lab, or set a deliberate maximum and explain its cost impact.
9. Configure availability:

   ### Lab Mode

   Single DB instance, Single-AZ

   ### High-Availability Mode

   Multi-AZ DB instance with a standby

10. Configure connectivity:

    | Setting | Value |
    |---|---|
    | Compute resource | Do not connect to an EC2 compute resource |
    | Network type | IPv4 |
    | VPC | `3tier-app-vpc` |
    | DB subnet group | `3tier-app-db-subnet-group` |
    | Public access | No |
    | Existing VPC security group | `3tier-app-db-sg` |
    | Remove the default security group if it is selected | |
    | Availability Zone | No preference |
    | RDS Proxy | Do not create for this lab |
    | Port | `3306` |

11. Configure authentication:

    | Setting | Value |
    |---|---|
    | Database authentication | Password authentication |

12. Configure monitoring:

    | Setting | Value |
    |---|---|
    | Performance Insights or Database Insights | Use the no-additional-cost or standard option appropriate to your account |
    | Enhanced Monitoring | Optional for LAB MODE; 60-second granularity for HIGH-AVAILABILITY MODE |

13. Open Additional configuration and set:

    | Setting | Value |
    |---|---|
    | Initial database name | `appdb` |
    | Automated backups | Enabled |
    | Backup retention | 7 days |
    | Copy tags to snapshots | Enabled |
    | Encryption | Enabled |
    | KMS key | `aws/rds` |
    | Error log export | Enabled |
    | Slow query log export | Optional; useful only when the related database parameters are enabled |
    | General log export | Leave disabled unless specifically needed because it can increase log volume and cost |
    | Auto minor version upgrade | Enabled if permitted by your course environment |
    | Deletion protection | Disabled for this short lab so cleanup can be completed |

14. Review the estimated monthly cost shown by the console.
15. Choose Create database.
16. Wait until the status becomes Available. Multi-AZ creation usually takes longer.

### Security Note

> **Security note:** Disabling deletion protection is a lab cleanup choice, not a production recommendation. Production systems should use deliberate change controls, protected backups, and tested recovery procedures.

## Action 6: Record the Master Secret and Endpoint

1. Select `3tier-app-database`.
2. On Connectivity and security, copy the endpoint and port.
3. Locate the managed master-credentials secret link or open Secrets Manager and find the secret associated with the database.
4. Copy the master secret ARN. Do not reveal its value in screenshots.

- Database endpoint: ______________________________
- Database port: `3306`
- Database name: `appdb`
- RDS master secret ARN: ______________________________
- Database security group ID: ______________________________

## Action 7: Create a Schema-Scoped Runtime Secret

The public-facing application should not keep using the RDS master identity. Create a separate secret for a runtime database user that will receive permissions only on `appdb`.

1. Open Secrets Manager and choose Store a new secret.
2. Select Other type of secret.
3. Add these key/value pairs:

   | Key | Value |
   |---|---|
   | username | `tickethub_app` |
   | password | `<GENERATE_A_UNIQUE_RANDOM_PASSWORD_IN_YOUR_PASSWORD_MANAGER>` |
   | host | `<YOUR_RDS_ENDPOINT>` |
   | port | `3306` |
   | dbname | `appdb` |

4. Do not paste the generated password into notes, screenshots, or application files.
5. Use the `aws/secretsmanager` encryption key for this beginner course.
6. Name the secret `3tier-app/runtime-db`.
7. Add the standard tags and store the secret.
8. Record only its ARN.

Runtime secret ARN: ______________________________

### Customer-Managed Key Note

> **Note:** If your organization requires a customer-managed key for Secrets Manager, the EC2 role needs narrowly scoped `kms:Decrypt` permission on the applicable key ARN, and the key policy must allow the role. Coordinate with your administrator rather than broadening permissions.

### Why Two Secrets

The RDS-managed secret contains the database master identity and is used once to create the schema-scoped runtime user. The application then uses `3tier-app/runtime-db`. Lecture 3 removes the EC2 role’s access to the master secret after bootstrap.

### Teaching Compromise

> **Note:** `tickethub_app` has schema-scoped DDL permissions because this sample initializes its tables at startup. Production systems should use a separate migration identity and a CRUD-only runtime identity.

## Action 8: Verify the Database

Confirm all of the following:

- [ ] Status is Available.
- [ ] Publicly accessible is No.
- [ ] VPC is `3tier-app-vpc`.
- [ ] Subnet group is `3tier-app-db-subnet-group`.
- [ ] Security group is `3tier-app-db-sg`.
- [ ] Storage encryption is enabled.
- [ ] Automated backup retention is 7 days.
- [ ] Multi-AZ matches your selected lab mode.
- [ ] Database connections are currently zero or near zero.
- [ ] No rule allows port `3306` from an internet CIDR.
- [ ] Both secret ARNs are recorded without exposing either password.

## Checkpoint

The database exists in isolated subnets, but it is not directly reachable from your laptop. That is expected. You will bootstrap and test it from the private application tier over verified TLS.

## Troubleshooting

### The Subnet Group Is Unavailable

Confirm it contains two subnets in different AZs and that both belong to `3tier-app-vpc`.

### The Selected Instance Class Is Unavailable

Choose a currently offered small burstable class. Offerings vary by Region and account.

### RDS Cannot Create Its Monitoring Role

Your IAM permissions may not allow service-linked role creation. Ask the lab administrator rather than granting yourself broad administrative access.

### The Database Remains Creating

Wait and refresh. Multi-AZ provisioning can take time. Review RDS events if it remains in the same state unusually long.

### A Log Export Is Empty

Some MySQL logs require database parameter settings before entries are generated. Export selection alone does not enable every type of logging.

## Knowledge Check

1. Why is Public access set to No?

   **Expected answer:** The application reaches RDS privately inside the VPC, so the database does not need a public endpoint.

2. Why is the application security group the source of the MySQL rule?

   **Expected answer:** Only instances attached to that security group should initiate database connections.

3. Why are there separate master and runtime secrets?

   **Expected answer:** The master identity performs one-time user bootstrap, while the application uses a schema-scoped identity with fewer privileges.

## Next Lecture

Upload the downloadable application bundle, create its IAM role and launch template, and start private EC2 capacity.
