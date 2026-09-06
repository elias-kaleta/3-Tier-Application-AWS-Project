# Guide 02: Database Setup

Create a Multi-AZ RDS MySQL database with automated backups and security.

**Time Required**: 45-60 minutes (mostly waiting for RDS to launch)  
**Difficulty**: Beginner  
**Week 4 Day**: Day 1

---

## What You'll Build

- RDS MySQL 8.0 database
- Multi-AZ deployment (primary + standby)
- DB Subnet Group
- Security Group for database access
- Encrypted storage
- Automated backups

---

## Prerequisites

✅ Completed [01-vpc-setup.md](./01-vpc-setup.md)

---

## Step 1: Create DB Subnet Group

RDS needs a subnet group spanning multiple AZs.

1. Open **AWS Console** → Search for **RDS**
2. Click **"Subnet groups"** in left sidebar
3. Click **"Create DB subnet group"**

```
Subnet group details:
  Name: 3tier-app-db-subnet-group
  Description: Subnet group for 3-tier app database
  VPC: Select "3tier-app-vpc"

Add subnets:
  Availability Zones: Select BOTH zones
    - us-east-1a (or your first AZ)
    - us-east-1b (or your second AZ)
  
  Subnets: Select the database subnets
    - 10.0.21.0/24 (3tier-app-db-1a)
    - 10.0.22.0/24 (3tier-app-db-1b)

Tags:
  - Key: Name | Value: 3tier-app-db-subnet-group
  - Key: Project | Value: 3tier-app
```

4. Click **"Create"**

### ✅ Checkpoint
- DB Subnet Group created
- Shows 2 subnets in 2 AZs

---

## Step 2: Create Security Group for Database

1. Go to **VPC Console** → **Security Groups**
2. Click **"Create security group"**

```
Security group name: 3tier-app-db-sg
Description: Security group for RDS database
VPC: 3tier-app-vpc

Inbound rules: (Leave empty for now - we'll add later)
  We'll add rules from the application tier in Guide 03

Outbound rules: (Delete the default rule)
  No outbound rules needed

Tags:
  - Key: Name | Value: 3tier-app-db-sg
  - Key: Project | Value: 3tier-app
```

3. Click **"Create security group"**

**Why no inbound rules yet?** We'll add MySQL access from the application security group after we create it in Guide 03.

---

## Step 3: Create RDS Database

1. Go back to **RDS Console**
2. Click **"Databases"** in left sidebar
3. Click **"Create database"**

### Database Creation Method

```
Choose a database creation method:
  ◉ Standard create
```

### Engine Options

```
Engine type:
  ◉ MySQL

Engine version:
  MySQL 8.0.35 (or latest 8.0.x)
  
Templates:
  ◉ Free tier (if eligible)
  OR
  ◉ Dev/Test (if free tier not available)
```

### Settings

```
DB instance identifier: 3tier-app-database

Credentials Settings:
  Master username: admin
  
  Credentials management:
    ◉ Self managed
  
  Master password: Create a strong password
    Example: MySecurePassword123!
  
  Confirm password: (enter same password)
```

**Important**: Save this password! You'll need it to connect to the database.

### Instance Configuration

```
DB instance class:
  ◉ Burstable classes (includes t classes)
  
  Select: db.t3.micro (free tier eligible)
  OR db.t4g.micro (newer, faster)
  
Storage type: General Purpose SSD (gp3)
Allocated storage: 20 GiB (free tier includes 20 GB)

Storage autoscaling:
  ☐ Enable storage autoscaling (uncheck for now)
```

### Availability & Durability

```
Multi-AZ deployment:
  ☑️ Create a standby instance (recommended for production resiliency)
  
  Multi-AZ DB instance
```

**Important**: Multi-AZ doubles the cost but provides high availability!

### Connectivity

```
Compute resource:
  ◉ Don't connect to an EC2 compute resource

Network type:
  ◉ IPv4

Virtual private cloud (VPC):
  Select: 3tier-app-vpc

DB subnet group:
  Select: 3tier-app-db-subnet-group

Public access:
  ◉ No (database should never be publicly accessible)

VPC security group (firewall):
  ◉ Choose existing
  Select: 3tier-app-db-sg
  Remove: default (if present)

Availability Zone:
  ◉ No preference (let AWS choose)

RDS Proxy:
  ☐ Do not create proxy
```

### Database Authentication

```
Database authentication:
  ☑️ Password authentication
  ☐ Password and IAM database authentication (optional enhancement)
```

### Monitoring

```
☑️ Enable Enhanced monitoring
  Granularity: 60 seconds
  Monitoring Role: Create a new role (rds-monitoring-role)
```

### Additional Configuration (Click to expand)

```
Database options:
  Initial database name: appdb
  DB parameter group: default.mysql8.0
  Option group: default:mysql-8-0
  
Backup:
  ☑️ Enable automated backups
  Backup retention period: 7 days
  Backup window: No preference
  Copy tags to snapshots: Yes
  
  ☑️ Enable Backup Replication: No (optional for disaster recovery)

Encryption:
  ☑️ Enable encryption
  AWS KMS key: (default) aws/rds
  
Log exports: (Select all for learning purposes)
  ☑️ Error log
  ☑️ General log
  ☑️ Slow query log

Maintenance:
  ☑️ Enable auto minor version upgrade
  Maintenance window: No preference

Deletion protection:
  ☐ Enable deletion protection (uncheck for easier cleanup)
  
  Note: Enable this in production!
```

4. Click **"Create database"**

---

## Step 4: Wait for Database Creation

This takes **10-15 minutes** for Multi-AZ deployment.

### While You Wait

1. Go to **RDS** → **Databases**
2. You'll see **3tier-app-database** with status: "Creating"
3. Status changes:
   - Creating (0-5 minutes)
   - Backing up (5-10 minutes)
   - Available (10-15 minutes)

### What's Happening Behind the Scenes?

- AWS creates primary database in AZ-1
- AWS creates standby replica in AZ-2
- Sets up synchronous replication
- Takes initial backup
- Configures automated backups

**Tip**: Continue reading this guide while waiting!

---

## Step 5: Get Database Endpoint

Once status is "Available":

1. Click on **3tier-app-database**
2. Go to **"Connectivity & security"** tab
3. Find **"Endpoint"** - it looks like:
   ```
   3tier-app-database.abc123xyz.us-east-1.rds.amazonaws.com
   ```
4. **Copy and save this endpoint** - you'll need it in Guide 03

---

## Step 6: Verify Database Configuration

### Check Connectivity

1. Select your database
2. **"Connectivity & security"** tab should show:
   - Endpoint: `3tier-app-database....rds.amazonaws.com`
   - Port: `3306`
   - VPC: `3tier-app-vpc`
   - Subnets: 2 database subnets
   - Security groups: `3tier-app-db-sg`
   - Publicly accessible: **No**

### Check Configuration

1. **"Configuration"** tab should show:
   - DB instance class: `db.t3.micro`
   - Storage: `20 GiB gp3`
   - Multi-AZ: **Yes**
   - Availability Zone: Both zones listed

### Check Monitoring

1. **"Monitoring"** tab shows:
   - CPU Utilization (should be low)
   - Database Connections (should be 0)
   - Free Storage Space (should be ~20 GB)

---

## What You've Built

✅ MySQL 8.0 database  
✅ Multi-AZ deployment (high availability)  
✅ Deployed in isolated subnets (no internet)  
✅ Encrypted storage  
✅ Automated daily backups  
✅ Security group (will add rules in next guide)  
✅ CloudWatch monitoring enabled  

---

## Architecture Explanation

### Why Multi-AZ?

**Without Multi-AZ** (Single Instance):
- Database runs in one AZ
- If that AZ fails, database is down
- Manual failover required
- ~15-30 minutes downtime

**With Multi-AZ**:
- Primary in AZ-1, Standby in AZ-2
- Automatic synchronous replication
- If primary fails, automatic failover to standby
- ~60-120 seconds downtime
- DNS endpoint stays the same (app reconnects automatically)

### Why Isolated Subnets?

- Database has NO internet access
- Can only communicate with resources in VPC
- Reduces attack surface
- Best security practice

### Why Automated Backups?

- Daily automated snapshots
- Point-in-time recovery (restore to any second in last 7 days)
- Backups run on standby (no performance impact on primary)
- Retention: 7 days (configurable 1-35 days)

---

## Cost Breakdown

- **db.t3.micro Single-AZ**: ~$15/month
- **db.t3.micro Multi-AZ**: ~$30/month (2x single instance)
- **Storage (20 GB gp3)**: ~$2.50/month
- **Backup storage**: First 20 GB free (equal to DB size)
- **Data transfer**: Free within same AZ

**Total**: ~$32.50/month

**Free Tier** (first 12 months):
- 750 hours/month of db.t2.micro or db.t3.micro
- 20 GB storage
- 20 GB backups

---

## Testing Database Connection (Optional)

You can't connect yet because:
1. Database is in isolated subnet (no internet)
2. No security group rules allowing connections

We'll test connectivity in Guide 03 after launching EC2 instances.

---

## Database Best Practices

### Security
- ✅ Never make database publicly accessible
- ✅ Use strong passwords (20+ characters)
- ✅ Enable encryption at rest
- ✅ Use SSL/TLS for connections
- ✅ Rotate passwords regularly (use Secrets Manager)

### Performance
- ✅ Monitor CPU, connections, IOPS
- ✅ Enable Enhanced Monitoring
- ✅ Use appropriate instance size
- ✅ Review slow query logs

### Reliability
- ✅ Enable Multi-AZ
- ✅ Configure automated backups
- ✅ Test backup restoration
- ✅ Set up CloudWatch alarms

### Cost Optimization
- ✅ Use Reserved Instances for production (save 30-60%)
- ✅ Right-size instance (start small, scale up)
- ✅ Delete unused snapshots
- ✅ Enable storage autoscaling carefully

---

## Troubleshooting

### Database Stuck "Creating"
- Wait 15 minutes
- Check AWS Service Health Dashboard
- If > 20 minutes, contact AWS Support

### Can't Select Subnet Group
- Ensure subnet group has 2+ subnets in different AZs
- Verify subnets are in same VPC
- Check VPC has DNS hostnames enabled

### "Insufficient Free Tier Resources"
- You may have used free tier hours this month
- Wait until next month
- OR pay for db.t3.micro (~$15/month single-AZ)

### Forgot Database Password
- You can modify the database later
- RDS → Databases → Select DB → Modify
- Change master password
- Apply immediately

---

## Next Steps

✅ Database is ready!

While database is creating, you can start reading **[03-application-setup.md](./03-application-setup.md)**.

Once database shows "Available", continue to Guide 03 to launch EC2 instances.

---

## Cleanup (If Starting Over)

To delete the database:

1. RDS → Databases → Select database
2. Actions → Delete
3. Options:
   - ☑️ Create final snapshot (if you want to save data)
   - Type: `delete me` to confirm
4. Click Delete

**Warning**: Deletion takes 5-10 minutes and cannot be undone!

---

## Save These Values

Write these down for the next guides:

```
Database Endpoint: 3tier-app-database._____.rds.amazonaws.com
Database Name: appdb
Master Username: admin
Master Password: [your password]
Port: 3306
Security Group ID: sg-_____ (3tier-app-db-sg)
```

You'll need these in Guide 03!
