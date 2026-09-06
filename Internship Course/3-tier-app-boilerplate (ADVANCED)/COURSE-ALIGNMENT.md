# Course Alignment Guide

How this 3-tier application boilerplate aligns with the 4-week internship course.

## Week-by-Week Mapping

### Week 1: AWS Fundamentals & Core Services

**What you learned**:
- EC2 instances and security groups
- S3 buckets
- VPC, subnets, route tables
- RDS databases

**Where it's used in this project**:
- `networking_stack.py`: VPC with subnets (Day 4 content)
- `database_stack.py`: RDS MySQL instance (Day 5 content)
- `application_stack.py`: EC2 launch template (Day 2 content)
- Security groups throughout all stacks

---

### Week 2: Advanced Services & Architecture Patterns

**What you learned**:
- Application Load Balancers (Day 1)
- CloudFront CDN (Day 2)
- Auto Scaling Groups (Day 1)
- CloudWatch monitoring (Day 4)

**Where it's used in this project**:
- `frontend_stack.py`: ALB + CloudFront (Days 1-2 content)
- `application_stack.py`: Auto Scaling Group (Day 1 content)
- `monitoring_stack.py`: CloudWatch alarms and dashboard (Day 4 content)

---

### Week 3: DevOps & Infrastructure as Code

**What you learned**:
- CloudFormation/CDK (Day 1)
- IAM roles and policies
- Container basics (Day 3)

**Where it's used in this project**:
- **Entire project** is Infrastructure as Code using CDK
- `application_stack.py`: IAM roles for EC2 instances
- All stacks: CloudFormation under the hood

**Skills practiced**:
- Writing CDK in Python
- Stack dependencies
- Parameter passing between stacks
- Synthesis and deployment

---

### Week 4: Final Project

**Day 1: Ideation & Design** ✅
- This boilerplate **IS** your architecture design
- Use `README.md` as your architecture documentation
- Modify and customize based on your team's problem statement

**Day 2: Build & Implement** ✅
- Start with this boilerplate
- Customize the Flask application in `application_stack.py`
- Add your business logic
- Integrate additional AWS services as needed

**Day 3: Integrate & Test** ✅
- Deploy with `cdk deploy --all`
- Test with `curl` commands
- Check CloudWatch dashboard
- Fix any issues

**Day 4: Presentation Prep** ✅
- Use the Well-Architected Framework section in `README.md`
- Screenshot the CloudWatch dashboard
- Document architecture decisions
- Record demo of working application

**Day 5: Present** ✅
- Demo the CloudFront URL
- Explain each tier and its purpose
- Show the CloudWatch dashboard
- Discuss trade-offs and future improvements

---

## AWS Well-Architected Framework Coverage

Use this for your Day 4 presentation preparation.

### Operational Excellence

**What we implemented**:
- ✅ Infrastructure as Code (CDK)
- ✅ CloudWatch monitoring and alarms
- ✅ Automated deployments via CDK
- ✅ CloudWatch logs for debugging

**In your presentation, mention**:
- How CDK makes deployments repeatable
- How CloudWatch helps us monitor and troubleshoot
- How Auto Scaling responds to issues automatically

---

### Security

**What we implemented**:
- ✅ VPC network isolation (3 subnet tiers)
- ✅ Security groups with least privilege
- ✅ Encryption at rest (RDS, EBS)
- ✅ Encryption in transit (CloudFront HTTPS)
- ✅ IAM roles (no hardcoded credentials)
- ✅ Database in isolated subnets
- ✅ Secrets Manager for database password

**In your presentation, mention**:
- Defense in depth: multiple layers of security
- Principle of least privilege
- No public IPs on application/database tiers
- Encryption everywhere

---

### Reliability

**What we implemented**:
- ✅ Multi-AZ deployment (RDS, Auto Scaling)
- ✅ Auto Scaling for fault tolerance
- ✅ Load balancer health checks
- ✅ Automated backups (RDS)
- ✅ CloudWatch alarms for proactive monitoring

**In your presentation, mention**:
- How we survive datacenter failures
- How Auto Scaling replaces failed instances
- How RDS automatically fails over
- Recovery Time Objective (RTO) and Recovery Point Objective (RPO)

---

### Performance Efficiency

**What we implemented**:
- ✅ CloudFront CDN (edge caching)
- ✅ Auto Scaling based on demand
- ✅ Right-sized instance types (t3.micro for dev)
- ✅ GP3 storage (latest generation)
- ✅ Multi-AZ for low latency

**In your presentation, mention**:
- How CloudFront reduces latency globally
- How Auto Scaling maintains performance under load
- How we chose instance types
- Future: read replicas, caching layers

---

### Cost Optimization

**What we implemented**:
- ✅ Free tier eligible resources
- ✅ Auto Scaling (scale down when idle)
- ✅ Single NAT Gateway (not one per AZ)
- ✅ CloudFront reduces data transfer costs
- ✅ GP3 storage (better price/performance)

**In your presentation, mention**:
- Estimated monthly costs (~$94/month after free tier)
- Cost-saving decisions (single NAT, t3.micro instances)
- How Auto Scaling reduces waste
- Future: Reserved Instances, Savings Plans

---

### Sustainability

**What we implemented**:
- ✅ Auto Scaling reduces idle resources
- ✅ Right-sized instances (no over-provisioning)
- ✅ CloudFront reduces redundant data transfer
- ✅ Multi-AZ only where needed (not for all resources)

**In your presentation, mention**:
- How Auto Scaling eliminates waste
- How CloudFront reduces network load
- How right-sizing reduces energy consumption
- AWS's commitment to renewable energy

---

## Customization Ideas for Your Project

Make this boilerplate your own:

### Frontend Enhancements
- Add React/Vue.js frontend (serve from S3 + CloudFront)
- Add custom domain with Route 53
- Add SSL certificate with ACM
- Add API Gateway for serverless API

### Backend Enhancements
- Add Lambda functions for serverless logic
- Add SQS queues for async processing
- Add ElastiCache for session storage
- Add Cognito for user authentication

### Data Tier Enhancements
- Add DynamoDB for NoSQL data
- Add S3 for file uploads
- Add read replicas for scaling
- Add Aurora Serverless v2

### DevOps Enhancements
- Add CodePipeline for CI/CD
- Add unit tests
- Add integration tests
- Add blue/green deployments

### Security Enhancements
- Add AWS WAF (see `recipes/05-security-hardening.md`)
- Add GuardDuty for threat detection
- Add Config for compliance
- Add VPC Flow Logs

---

## Presentation Structure

Use this outline for your Day 5 presentation:

### 1. Introduction (2 minutes)
- Problem statement
- Target users
- Why we chose 3-tier architecture

### 2. Architecture Overview (3 minutes)
- Show architecture diagram
- Explain each tier's purpose
- Data flow from user to database

### 3. AWS Services Used (4 minutes)
- VPC & Subnets → network isolation
- RDS Multi-AZ → high availability database
- Auto Scaling Group → elastic compute
- ALB → load distribution
- CloudFront → global CDN
- CloudWatch → monitoring

### 4. Demo (3 minutes)
- Show CloudFront URL
- Make request, show response
- Show CloudWatch dashboard
- Show Auto Scaling (if time permits)

### 5. Well-Architected Framework (3 minutes)
- One slide per pillar
- Specific examples from our implementation
- Trade-offs we made

### 6. Future Improvements (2 minutes)
- What we'd add with more time
- How to scale to 1M users
- Production-ready enhancements

### 7. Retrospective (2 minutes)
- What went well
- What we'd change
- Key learnings

### 8. Q&A (3 minutes)
- Be ready to discuss:
  - Why Multi-AZ?
  - Why CloudFront?
  - Why private subnets?
  - Cost breakdown
  - Scaling strategy

---

## Key Talking Points

Memorize these for your presentation:

**Why Three Tiers?**
- Separation of concerns
- Security isolation
- Independent scaling
- Team specialization

**Why Multi-AZ?**
- High availability (99.95% SLA)
- Automatic failover
- Zero-downtime deployments
- Disaster recovery

**Why Auto Scaling?**
- Handle variable traffic
- Cost optimization (scale down at night)
- Automatic recovery (replace failed instances)
- Maintain performance

**Why CloudFront?**
- Global edge network (low latency)
- DDoS protection (Shield Standard)
- HTTPS for free
- Reduces origin load

**Cost vs. Reliability Trade-offs**:
- Single NAT Gateway → saves $32/month, but single point of failure
- Multi-AZ RDS → 2x cost, but automatic failover
- Free tier instances → limited performance, but good for learning

---

## Demo Script

Practice this before your presentation:

```bash
# 1. Show the application works
curl https://YOUR-CLOUDFRONT-URL/
# "Connected to database! Version: 8.0.35"

# 2. Show health check
curl https://YOUR-CLOUDFRONT-URL/health
# "status: healthy"

# 3. Show it's actually hitting the database
# (Point out the database version in response)

# 4. Open CloudWatch dashboard
# - Show request count graph
# - Show healthy instance count
# - Show database CPU (should be low)

# 5. Explain monitoring
# "We have alarms set for 5XX errors, unhealthy targets, 
#  high CPU, and low database storage"
```

---

## Questions You Might Get

**Q: Why not use Lambda instead of EC2?**
A: Lambda is great for event-driven workloads, but EC2 gives us more control and is easier to understand for learning. In production, we could migrate to ECS Fargate or Lambda for better cost optimization.

**Q: Why MySQL instead of DynamoDB?**
A: We chose relational database because most traditional applications use SQL. DynamoDB is better for key-value access patterns. For our use case, RDS provides ACID guarantees and familiar query language.

**Q: How does this handle 1 million users?**
A: Current setup handles ~1000 concurrent users. For 1M users we'd add:
- Read replicas for database
- ElastiCache for caching
- More Auto Scaling capacity
- CloudFront caching policies
- Consider Aurora Serverless v2

**Q: What's the RTO and RPO?**
A: 
- RTO (Recovery Time Objective): 2-5 minutes (RDS failover time)
- RPO (Recovery Point Objective): Near zero (synchronous replication)

**Q: How do you deploy code changes?**
A: Currently, we'd update the user_data script and `cdk deploy`. Production would use CodePipeline for blue/green deployments or ECS for faster deploys.

---

## Success Criteria

Your project is successful if you can:

✅ Deploy all stacks without errors  
✅ Access the application via CloudFront URL  
✅ Explain each tier's purpose  
✅ Map to Well-Architected Framework  
✅ Discuss trade-offs you made  
✅ Answer questions about scaling and reliability  
✅ Demonstrate CloudWatch monitoring  
✅ Explain the security model  

---

## Additional Resources

- AWS Well-Architected Labs: https://wellarchitectedlabs.com/
- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/
- CDK Examples: https://github.com/aws-samples/aws-cdk-examples
- AWS This Is My Architecture: https://aws.amazon.com/this-is-my-architecture/

Good luck with your presentation! 🚀
