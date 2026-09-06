# Guide 01: VPC Setup

Create the networking foundation with a VPC, subnets, route tables, and internet connectivity.

**Time Required**: 30-45 minutes  
**Difficulty**: Beginner  
**Week 4 Day**: Day 1

---

## What You'll Build

- 1 VPC (10.0.0.0/16)
- 6 Subnets across 2 Availability Zones
  - 2 Public subnets (for load balancers)
  - 2 Private subnets (for EC2 instances)
  - 2 Database subnets (for RDS)
- 1 Internet Gateway
- 1 NAT Gateway
- Route tables for each tier

---

## Architecture Diagram

```
VPC (10.0.0.0/16)
├── AZ 1 (us-east-1a)
│   ├── Public Subnet (10.0.1.0/24)
│   ├── Private Subnet (10.0.11.0/24)
│   └── DB Subnet (10.0.21.0/24)
└── AZ 2 (us-east-1b)
    ├── Public Subnet (10.0.2.0/24)
    ├── Private Subnet (10.0.12.0/24)
    └── DB Subnet (10.0.22.0/24)
```

---

## Step 1: Create the VPC

1. Open **AWS Console** → Search for **VPC**
2. Click **"Your VPCs"** in left sidebar
3. Click **"Create VPC"**

### VPC Configuration

```
VPC settings: VPC only (we'll create subnets manually)
Name tag: 3tier-app-vpc
IPv4 CIDR block: 10.0.0.0/16
IPv6 CIDR block: No IPv6 CIDR block
Tenancy: Default
Tags:
  - Key: Name | Value: 3tier-app-vpc
  - Key: Project | Value: 3tier-app
```

4. Click **"Create VPC"**

### ✅ Checkpoint
- VPC created with ID like `vpc-0abc123...`
- Shows "Available" status

---

## Step 2: Enable DNS Hostnames

This allows EC2 instances to get DNS names.

1. Select your VPC: **3tier-app-vpc**
2. Click **Actions** → **Edit VPC settings**
3. Enable: ☑️ **Enable DNS hostnames**
4. Click **"Save"**

---

## Step 3: Create Internet Gateway

This allows public subnets to reach the internet.

1. Click **"Internet Gateways"** in left sidebar
2. Click **"Create internet gateway"**

```
Name tag: 3tier-app-igw
Tags:
  - Key: Name | Value: 3tier-app-igw
  - Key: Project | Value: 3tier-app
```

3. Click **"Create internet gateway"**
4. Select the IGW you just created
5. Click **Actions** → **Attach to VPC**
6. Select **3tier-app-vpc**
7. Click **"Attach internet gateway"**

### ✅ Checkpoint
- Internet Gateway shows "Attached" to your VPC

---

## Step 4: Create Subnets

Create 6 subnets total. We'll start with public subnets.

### Public Subnet 1

1. Click **"Subnets"** in left sidebar
2. Click **"Create subnet"**

```
VPC ID: Select "3tier-app-vpc"
Subnet settings:
  Subnet name: 3tier-app-public-1a
  Availability Zone: us-east-1a (or first AZ in your region)
  IPv4 CIDR block: 10.0.1.0/24
Tags:
  - Key: Name | Value: 3tier-app-public-1a
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: public
```

3. Click **"Add new subnet"** at the bottom

### Public Subnet 2

```
Subnet name: 3tier-app-public-1b
Availability Zone: us-east-1b (or second AZ)
IPv4 CIDR block: 10.0.2.0/24
Tags:
  - Key: Name | Value: 3tier-app-public-1b
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: public
```

### Private Subnet 1

Click **"Add new subnet"** again

```
Subnet name: 3tier-app-private-1a
Availability Zone: us-east-1a
IPv4 CIDR block: 10.0.11.0/24
Tags:
  - Key: Name | Value: 3tier-app-private-1a
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: private
```

### Private Subnet 2

```
Subnet name: 3tier-app-private-1b
Availability Zone: us-east-1b
IPv4 CIDR block: 10.0.12.0/24
Tags:
  - Key: Name | Value: 3tier-app-private-1b
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: private
```

### Database Subnet 1

```
Subnet name: 3tier-app-db-1a
Availability Zone: us-east-1a
IPv4 CIDR block: 10.0.21.0/24
Tags:
  - Key: Name | Value: 3tier-app-db-1a
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: database
```

### Database Subnet 2

```
Subnet name: 3tier-app-db-1b
Availability Zone: us-east-1b
IPv4 CIDR block: 10.0.22.0/24
Tags:
  - Key: Name | Value: 3tier-app-db-1b
  - Key: Project | Value: 3tier-app
  - Key: Tier | Value: database
```

4. Click **"Create subnet"** (creates all 6 at once)

### ✅ Checkpoint
- You should see 6 subnets in your subnets list
- Each shows "Available" status
- CIDR blocks match the plan above

---

## Step 5: Enable Auto-Assign Public IP for Public Subnets

1. Select **3tier-app-public-1a** subnet
2. Click **Actions** → **Edit subnet settings**
3. Enable: ☑️ **Enable auto-assign public IPv4 address**
4. Click **"Save"**

5. Repeat for **3tier-app-public-1b**

---

## Step 6: Create NAT Gateway

NAT Gateway allows private subnets to reach the internet (for updates).

1. Click **"NAT Gateways"** in left sidebar
2. Click **"Create NAT gateway"**

```
Name: 3tier-app-nat
Subnet: 3tier-app-public-1a (must be public subnet!)
Connectivity type: Public
Elastic IP allocation ID: Click "Allocate Elastic IP"
Tags:
  - Key: Name | Value: 3tier-app-nat
  - Key: Project | Value: 3tier-app
```

3. Click **"Create NAT gateway"**

**Note**: NAT Gateway takes 2-3 minutes to become "Available"

### ✅ Checkpoint
- NAT Gateway shows "Available" status
- Has an Elastic IP associated

---

## Step 7: Create Route Tables

### Public Route Table

1. Click **"Route Tables"** in left sidebar
2. Click **"Create route table"**

```
Name: 3tier-app-public-rt
VPC: 3tier-app-vpc
Tags:
  - Key: Name | Value: 3tier-app-public-rt
  - Key: Project | Value: 3tier-app
```

3. Click **"Create route table"**

#### Add Internet Gateway Route

1. Select **3tier-app-public-rt**
2. Go to **"Routes"** tab
3. Click **"Edit routes"**
4. Click **"Add route"**

```
Destination: 0.0.0.0/0
Target: Internet Gateway → Select "3tier-app-igw"
```

5. Click **"Save changes"**

#### Associate Public Subnets

1. Go to **"Subnet associations"** tab
2. Click **"Edit subnet associations"**
3. Select both public subnets:
   - ☑️ 3tier-app-public-1a
   - ☑️ 3tier-app-public-1b
4. Click **"Save associations"**

### Private Route Table

1. Click **"Create route table"**

```
Name: 3tier-app-private-rt
VPC: 3tier-app-vpc
Tags:
  - Key: Name | Value: 3tier-app-private-rt
  - Key: Project | Value: 3tier-app
```

2. Click **"Create route table"**

#### Add NAT Gateway Route

1. Select **3tier-app-private-rt**
2. Go to **"Routes"** tab
3. Click **"Edit routes"**
4. Click **"Add route"**

```
Destination: 0.0.0.0/0
Target: NAT Gateway → Select "3tier-app-nat"
```

5. Click **"Save changes"**

#### Associate Private Subnets

1. Go to **"Subnet associations"** tab
2. Click **"Edit subnet associations"**
3. Select both private subnets:
   - ☑️ 3tier-app-private-1a
   - ☑️ 3tier-app-private-1b
4. Click **"Save associations"**

### Database Route Table

Database subnets get NO internet access (isolated).

1. Click **"Create route table"**

```
Name: 3tier-app-db-rt
VPC: 3tier-app-vpc
Tags:
  - Key: Name | Value: 3tier-app-db-rt
  - Key: Project | Value: 3tier-app
```

2. Click **"Create route table"**
3. **Do NOT add any routes** (only local VPC traffic allowed)

#### Associate Database Subnets

1. Select **3tier-app-db-rt**
2. Go to **"Subnet associations"** tab
3. Click **"Edit subnet associations"**
4. Select both database subnets:
   - ☑️ 3tier-app-db-1a
   - ☑️ 3tier-app-db-1b
5. Click **"Save associations"**

---

## Step 8: Verify Your Setup

### Check Subnets
1. Go to **Subnets**
2. You should see:
   - 2 subnets with **public** route table
   - 2 subnets with **private** route table
   - 2 subnets with **database** route table

### Check Route Tables
1. Go to **Route Tables**
2. **Public RT** should have route: `0.0.0.0/0` → Internet Gateway
3. **Private RT** should have route: `0.0.0.0/0` → NAT Gateway
4. **Database RT** should have ONLY local VPC route

---

## What You've Built

✅ VPC with 65,536 IP addresses  
✅ 6 subnets across 2 Availability Zones  
✅ Public subnets can reach internet via Internet Gateway  
✅ Private subnets can reach internet via NAT Gateway  
✅ Database subnets have NO internet access  
✅ Multi-AZ setup for high availability  

---

## Architecture Explanation

### Why 3 Subnet Tiers?

**Public Subnets**:
- For resources that need to be accessed from internet
- Load balancers, bastion hosts
- Route: 0.0.0.0/0 → Internet Gateway

**Private Subnets**:
- For application servers
- Can reach internet for updates (via NAT)
- Not directly accessible from internet
- Route: 0.0.0.0/0 → NAT Gateway

**Database Subnets**:
- Maximum security for sensitive data
- NO internet access at all
- Only local VPC traffic
- Route: Only local (10.0.0.0/16)

### Why 2 Availability Zones?

- High availability: survive datacenter failure
- Load distribution across zones
- Required for Multi-AZ RDS
- Best practice: use at least 2 AZs

---

## Cost Breakdown

- **VPC**: Free
- **Subnets**: Free
- **Internet Gateway**: Free
- **Route Tables**: Free
- **NAT Gateway**: ~$32/month + data processing (~$0.045/GB)
- **Elastic IP**: Free while attached to NAT Gateway

**Total**: ~$32/month for NAT Gateway

---

## Troubleshooting

### Can't Create Subnet
- Check CIDR blocks don't overlap
- Ensure you're in the correct VPC
- Verify CIDR is within VPC range (10.0.0.0/16)

### NAT Gateway Stuck "Pending"
- Wait 2-3 minutes
- Refresh the page
- Check Elastic IP was allocated

### Route Not Saving
- Ensure target resource exists (IGW/NAT)
- Check resource is attached to VPC
- Try refreshing the page

---

## Next Steps

✅ VPC setup complete!

Continue to **[02-database-setup.md](./02-database-setup.md)** to create your RDS database.

---

## Clean Up (If Starting Over)

To delete everything:

1. Delete NAT Gateway (wait 5 min for deletion)
2. Release Elastic IP
3. Delete Route Tables (except main)
4. Delete Subnets
5. Detach and delete Internet Gateway
6. Delete VPC

**Warning**: Only do this if you need to start fresh!
