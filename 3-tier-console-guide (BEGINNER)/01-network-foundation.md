# Create the Network Foundation

## Estimated Time

45–60 minutes

## Lecture Outcome

You will create one VPC, six subnets across two Availability Zones, an Internet Gateway, one NAT Gateway, and separate route tables for the public, application, and database tiers.

## Prerequisites

- Complete the overview and preflight lecture.
- Select one Region and two Availability Zones.
- Keep the network plan from the previous lecture available.

## Cost Impact

> **Cost warning:** The VPC, subnets, route tables, and Internet Gateway have no hourly charge. The NAT Gateway, its public IPv4 address, and processed data are billable. Verify current prices for your Region before continuing.

## Before You Click

> **Important:** Confirm the Region shown in the AWS console. All VPC resources in this lecture must be in that Region.

## Action 1: Create the VPC

1. Search for VPC in the AWS console.
2. Choose Your VPCs.
3. Choose Create VPC.
4. Select VPC only.
5. Enter these values:

   | Setting | Value |
   |---|---|
   | Name tag | `3tier-app-vpc` |
   | IPv4 CIDR | `10.0.0.0/16` |
   | IPv6 CIDR | No IPv6 CIDR block |
   | Tenancy | Default |

6. Add the standard Project, Environment, Owner, ManagedBy, and ExpirationDate tags.
7. Choose Create VPC.
8. Select the new VPC, choose Actions, and then Edit VPC settings.
9. Enable DNS resolution and DNS hostnames.
10. Save the changes.

### Why

DNS support lets private EC2 instances resolve AWS service endpoints and the RDS DNS endpoint.

## Checkpoint

The VPC status is Available and both DNS resolution and DNS hostnames are enabled.

## Action 2: Create the Six Subnets

1. In the VPC console, choose Subnets.
2. Choose Create subnet.
3. Select `3tier-app-vpc`.
4. Add the following six subnets. Use your selected AZ A and AZ B rather than blindly copying an example Region.

### Subnet 1

| Setting | Value |
|---|---|
| Name | `3tier-app-public-1a` |
| Availability Zone | AZ A |
| IPv4 CIDR | `10.0.1.0/24` |
| Tier tag | public |

### Subnet 2

| Setting | Value |
|---|---|
| Name | `3tier-app-public-1b` |
| Availability Zone | AZ B |
| IPv4 CIDR | `10.0.2.0/24` |
| Tier tag | public |

### Subnet 3

| Setting | Value |
|---|---|
| Name | `3tier-app-private-1a` |
| Availability Zone | AZ A |
| IPv4 CIDR | `10.0.11.0/24` |
| Tier tag | application |

### Subnet 4

| Setting | Value |
|---|---|
| Name | `3tier-app-private-1b` |
| Availability Zone | AZ B |
| IPv4 CIDR | `10.0.12.0/24` |
| Tier tag | application |

### Subnet 5

| Setting | Value |
|---|---|
| Name | `3tier-app-db-1a` |
| Availability Zone | AZ A |
| IPv4 CIDR | `10.0.21.0/24` |
| Tier tag | database |

### Subnet 6

| Setting | Value |
|---|---|
| Name | `3tier-app-db-1b` |
| Availability Zone | AZ B |
| IPv4 CIDR | `10.0.22.0/24` |
| Tier tag | database |

5. Add the standard tags to each subnet.
6. Choose Create subnet.

### Security Note

> **Security note:** Leave automatic public IPv4 assignment disabled on every subnet. An Application Load Balancer can be internet-facing without automatically assigning public IP addresses to other resources launched into the subnet.

## Checkpoint

You can see six Available subnets. Each pair is split across AZ A and AZ B, and no CIDR blocks overlap.

## Action 3: Create and Attach the Internet Gateway

1. Choose Internet gateways.
2. Choose Create internet gateway.
3. Name it `3tier-app-igw` and add the standard tags.
4. Choose Create internet gateway.
5. Select it, choose Actions, and then Attach to a VPC.
6. Select `3tier-app-vpc` and attach it.

## Checkpoint

The Internet Gateway state is Attached and the VPC ID matches `3tier-app-vpc`.

## Action 4: Create the Public Route Table

1. Choose Route tables and Create route table.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-public-rt` |
   | VPC | `3tier-app-vpc` |

3. Add the standard tags and create it.
4. Open its Routes tab and choose Edit routes.
5. Add this route:

   | Setting | Value |
   |---|---|
   | Destination | `0.0.0.0/0` |
   | Target | Internet Gateway, `3tier-app-igw` |

6. Save changes.
7. Open Subnet associations and choose Edit subnet associations.
8. Select `3tier-app-public-1a` and `3tier-app-public-1b` only.
9. Save associations.

### Why

The default route lets internet-facing load balancer nodes communicate through the Internet Gateway.

## Action 5: Create the NAT Gateway

1. Choose NAT gateways and Create NAT gateway.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-nat-1a` |
   | Subnet | `3tier-app-public-1a` |
   | Connectivity type | Public |
   | Elastic IP | Allocate Elastic IP |

3. Add the standard tags.
4. Create the NAT Gateway.
5. Wait until its state is Available before creating the private default route.

### Why

Private EC2 instances use the NAT Gateway for outbound package downloads and AWS API calls. The NAT Gateway does not allow unsolicited inbound connections to those instances.

### Design Trade-Off

One NAT Gateway lowers lab cost but creates an AZ dependency and may create cross-AZ data charges for the second private subnet. A production design commonly uses one NAT Gateway per AZ and an AZ-local private route table.

## Action 6: Create the Private Route Table

1. Create another route table.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-private-rt` |
   | VPC | `3tier-app-vpc` |

3. Add the standard tags and create it.
4. Edit routes and add:

   | Setting | Value |
   |---|---|
   | Destination | `0.0.0.0/0` |
   | Target | NAT Gateway, `3tier-app-nat-1a` |

5. Save changes.
6. Associate only `3tier-app-private-1a` and `3tier-app-private-1b`.

## Action 7: Create the Database Route Table

1. Create one more route table.
2. Enter:

   | Setting | Value |
   |---|---|
   | Name | `3tier-app-db-rt` |
   | VPC | `3tier-app-vpc` |

3. Add the standard tags and create it.
4. Do not add a default internet route. Keep only the automatically created local route for `10.0.0.0/16`.
5. Associate only `3tier-app-db-1a` and `3tier-app-db-1b`.

### Why

The database tier needs private connectivity inside the VPC, but it does not need a route to the internet or NAT Gateway.

## Action 8: Verify the Routing Design

Check each route table and association.

### Public Route Table

- [ ] `10.0.0.0/16` points to local.
- [ ] `0.0.0.0/0` points to the Internet Gateway.
- [ ] It is associated with the two public subnets only.

### Private Route Table

- [ ] `10.0.0.0/16` points to local.
- [ ] `0.0.0.0/0` points to the NAT Gateway.
- [ ] It is associated with the two private application subnets only.

### Database Route Table

- [ ] `10.0.0.0/16` points to local.
- [ ] It has no `0.0.0.0/0` route.
- [ ] It is associated with the two database subnets only.

## Final Checkpoint

Your VPC contains six subnets across two AZs. Public traffic can use the Internet Gateway, private application traffic can leave through NAT, and the database tier has no internet route.

## Save These Values

- VPC ID: ______________________________
- Public subnet A ID: ______________________________
- Public subnet B ID: ______________________________
- Private subnet A ID: ______________________________
- Private subnet B ID: ______________________________
- Database subnet A ID: ______________________________
- Database subnet B ID: ______________________________
- Internet Gateway ID: ______________________________
- NAT Gateway ID: ______________________________
- NAT Elastic IP allocation ID: ______________________________

## Troubleshooting

### A Subnet CIDR Is Rejected

Confirm it is inside `10.0.0.0/16` and does not overlap another subnet.

### The NAT Gateway Remains Pending

Wait several minutes and refresh. Confirm it is in a public subnet with an Elastic IP.

### The Private Route Cannot Select the NAT Gateway

Wait for the NAT Gateway state to become Available and confirm both resources are in the same Region.

### A Subnet Appears to Use the Main Route Table

Explicitly associate it with the intended route table. Do not rely on the main table for this lab.

## Knowledge Check

1. Which tier has a route to the NAT Gateway?

   **Expected answer:** The private application tier.

2. Does a NAT Gateway make private instances reachable from the internet?

   **Expected answer:** No. It provides outbound translation and return traffic only.

3. Why does the database route table contain no default route?

   **Expected answer:** The database should communicate privately inside the VPC and does not need internet access.

## Next Lecture

Create the security-group chain and the private RDS MySQL database.
