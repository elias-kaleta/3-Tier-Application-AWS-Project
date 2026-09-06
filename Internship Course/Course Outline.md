# AWS Cloud Architecture Internship - 4 Week Course Outline

## Course Overview
A hands-on 4-week internship program designed to build foundational AWS cloud architecture skills, culminating in the design and deployment of a complete 3-tier application on AWS.

---

## Week 1: AWS Fundamentals & Core Services

### Day 1: Introduction to Cloud Computing & AWS
- Morning: Cloud computing concepts (IaaS, PaaS, SaaS)
- Introduction to AWS console and navigation
- AWS account setup and IAM basics
- Afternoon: Create IAM users, groups, and policies
- Lab: Setup MFA and implement least privilege access

### Day 2: Compute Services - EC2
- Morning: EC2 fundamentals and instance types
- Security groups and key pairs
- Afternoon: Launch and connect to EC2 instances
- Lab: Deploy a web server on EC2

### Day 3: Storage Services
- Morning: S3 bucket creation and management
- S3 storage classes and lifecycle policies
- Afternoon: EBS volumes and snapshots
- Lab: Host a static website on S3

### Day 4: Networking Basics
- Morning: VPC concepts and components
- Subnets, route tables, and internet gateways
- Afternoon: Security groups vs NACLs
- Lab: Create a custom VPC with public and private subnets

### Day 5: Databases Introduction
- Morning: RDS overview and database engines
- Afternoon: DynamoDB basics
- Lab: Launch an RDS MySQL instance
- Weekly Review: Quiz and knowledge check

---

## Week 2: Advanced Services & Architecture Patterns

### Day 1: Load Balancing & Auto Scaling
- Morning: Elastic Load Balancer types (ALB, NLB, CLB)
- Target groups and health checks
- Afternoon: Auto Scaling Groups and scaling policies
- Lab: Setup ALB with Auto Scaling

### Day 2: Content Delivery & DNS
- Morning: CloudFront CDN concepts
- Route 53 DNS service
- Afternoon: DNS routing policies
- Lab: Configure CloudFront distribution with S3 origin

### Day 3: Serverless Computing
- Morning: Lambda functions and event-driven architecture
- API Gateway basics
- Afternoon: Lambda triggers and integrations
- Lab: Create a serverless API with Lambda and API Gateway

### Day 4: Monitoring & Management
- Morning: CloudWatch metrics, logs, and alarms
- CloudTrail for auditing
- Afternoon: AWS Systems Manager
- Lab: Setup monitoring dashboard and alarms

### Day 5: Security & Compliance
- Morning: AWS security best practices
- Encryption (at rest and in transit)
- Afternoon: AWS WAF and Shield
- Lab: Implement security hardening
- Weekly Review: Architecture design exercise

---

## Week 3: DevOps & Infrastructure as Code

### Day 1: Infrastructure as Code - CloudFormation
- Morning: CloudFormation concepts and templates
- Stack management
- Afternoon: Parameters, mappings, and outputs
- Lab: Create infrastructure using CloudFormation

### Day 2: CI/CD Pipeline
- Morning: CodeCommit and version control
- CodeBuild basics
- Afternoon: CodeDeploy and CodePipeline
- Lab: Build a simple CI/CD pipeline

### Day 3: Containers & Orchestration
- Morning: Docker basics and ECS concepts
- ECR (Elastic Container Registry)
- Afternoon: Fargate vs EC2 launch types
- Lab: Deploy a containerized application on ECS

### Day 4: Advanced Networking
- Morning: VPC peering and Transit Gateway
- VPN and Direct Connect
- Afternoon: NAT Gateway and VPC Endpoints
- Lab: Setup multi-VPC architecture

### Day 5: Cost Optimization
- Morning: AWS pricing models
- Cost Explorer and budgets
- Afternoon: Reserved instances and Savings Plans
- Lab: Analyze and optimize costs
- Weekly Review: Design a scalable architecture

---

## Week 4: Final Project - 3-Tier Application Deployment

> **Note**: Project deliverables and presentation outline are TBC by Danny and Elliot

### Day 1: Ideation & Design
**Goal**: Define the project scope and architect the solution

- Brainstorm project ideas and select one
- Identify the problem being solved and target users
- Whiteboard the system architecture
- Select AWS services to use (and justify why)
- Define success criteria and MVP (minimum viable product) scope

**Deliverable**: Architecture diagram and project plan

### Day 2: Build & Implement
**Goal**: Write the core application logic and begin AWS integration

- Scaffold the project structure
- Vibe code the project
- Set up initial AWS service connections (e.g., EC2, DynamoDB, S3, ALB, etc.)
- Test project locally

**Deliverable**: Working core functionality with at least one AWS service integrated

### Day 3: Integrate & Test
**Goal**: Connect all pieces and get a working end-to-end flow

- Complete remaining AWS service integrations
- Test end-to-end functionality
- Extra: Identify and fix bugs and edge cases
- Document any technical decisions or trade-offs made to be used for presentations later

**Deliverable**: Functional MVP deployed or running against AWS services

### Day 4: Presentation Prep
**Goal**: Compile findings and build the presentation deck

- Record a short demo of the working project
- Document each AWS service used and the rationale for choosing it
- Map the architecture to the AWS Well-Architected Framework pillars:
  - Operational Excellence
  - Security
  - Reliability
  - Performance Efficiency
  - Cost Optimisation
  - Sustainability
- Identify areas for improvement and future scaling opportunities
- Build slide deck covering all of the above
- Rehearse and refine delivery

**Deliverable**: Complete presentation deck with demo recording

### Day 5: Present
**Goal**: Deliver the final presentation

- Final rehearsal and timing check
- Present to the team/stakeholders:
  - Short live, recorded or screenshot demo of the outcome
  - Explanation of AWS services used and why
  - Tie-in to AWS Well-Architected pillars
  - Areas for improvement and scaling path
- Q&A and feedback session
- Retrospective: what went well, what would change next time

**Deliverable**: Completed presentation and feedback collected

---

## Project Deliverables (Week 4)

1. **Architecture Diagram**: Complete AWS architecture showing all components
2. **Working Application**: Functional MVP using AWS services
3. **AWS Service Documentation**: Rationale for each service selected
4. **Well-Architected Framework Analysis**: Coverage of all six pillars
5. **Demo Recording**: Short video demonstrating the application
6. **Presentation Deck**: Complete slides with architecture, decisions, and scaling path
7. **Retrospective Notes**: Lessons learned and future improvements

---

## Learning Outcomes

By the end of this internship, participants will be able to:
- Navigate and use AWS core services confidently
- Design and implement scalable, secure cloud architectures
- Deploy and manage a complete 3-tier application on AWS
- Implement Infrastructure as Code using CloudFormation
- Apply AWS best practices for security and cost optimization
- Monitor and troubleshoot cloud applications

---

## Prerequisites
- Basic understanding of networking concepts
- Familiarity with Linux command line
- Basic programming knowledge (Python or JavaScript preferred)
- AWS account with appropriate permissions

## Resources
- AWS Free Tier account
- AWS Documentation and whitepapers
- Project GitHub repository
- Cloud architecture diagrams tools (draw.io, Lucidchart)
