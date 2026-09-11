# 🎓 AWS Cloud Architecture Internship - 4-Week Program

[![AWS](https://img.shields.io/badge/AWS-Cloud%20Architecture-orange?logo=amazon-aws)](https://aws.amazon.com/)
[![Duration](https://img.shields.io/badge/Duration-4%20Weeks-green.svg)]()
[![Hands-On](https://img.shields.io/badge/Labs-50%2B-blue.svg)]()

> A comprehensive, hands-on learning journey from AI fundamentals to building production-ready AWS applications

---

## 📋 Quick Navigation

- [Course Overview](#-course-overview)
- [Week-by-Week Breakdown](#-week-by-week-breakdown)
- [Getting Started](#-getting-started)
- [Repository Structure](#-repository-structure)
- [Key Resources](#-key-resources)
- [Learning Path](#-learning-path)

---

## 🎯 Course Overview

This 4-week intensive program takes you from **AI fundamentals** through **cloud architecture mastery**, culminating in a **production-ready three-tier application**.

### What You'll Learn

| Week | Focus Area | Hours | Key Outcomes |
|------|------------|-------|--------------|
| **1** | 🤖 AI & Modern Dev | 40h | AI ethics, LLMs, Vibe Coding, Chatbots |
| **2** | ☁️ AWS Core Services | 40h | VPC, EC2, S3, Lambda, IAM, Security |
| **3** | 🗄️ Databases & Observability | 40h | RDS, DynamoDB, CloudWatch, Troubleshooting |
| **4** | 🚀 Capstone Project | 40h | Complete 3-Tier App in 5 Days |

**Total:** ~160 hours | **Labs:** 50+ | **Projects:** 3 major deliverables

---

## 📅 Week-by-Week Breakdown

### 🤖 Week 1: AI Fundamentals & Development

**Theme:** Modern Development with AI

#### Monday: Responsible AI & Ethics
- ✅ Five Pillars of Ethical AI
- ✅ AI Risk Assessment
- ✅ Privacy & Bias
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Large Language Models basics

#### Tuesday: AI First Steps
- ✅ Prompt Engineering techniques
- ✅ Tokenization concepts
- ✅ Temperature & Top-K parameters
- ✅ Handling hallucinations

#### Wednesday: Enhancing AI Utility
- ✅ Amazon Bedrock hands-on
- ✅ Building RAG applications
- ✅ Guardrails for AI
- ✅ AI Agents
- ✅ Governance & Compliance

#### Thursday: Vibe Coding
- ✅ AI-assisted development
- ✅ Using Canvas features (ChatGPT, Claude)
- ✅ GitHub Copilot integration
- ✅ Building full-stack apps with AI
- ✅ Best practices for vibe coding

#### Friday: Chatbot Development
- ✅ Building conversational AI
- ✅ OpenAI API integration
- ✅ System prompts & fine-tuning
- ✅ DALL-E image generation
- ✅ Complete chatbot project

**📦 Deliverable:** Working chatbot + vibe-coded browser game

---

### ☁️ Week 2: AWS Core Services

**Theme:** Cloud Fundamentals & Architecture

#### Monday: VPC & Networking
- ✅ IP addressing & DNS
- ✅ VPC, Subnets, Route Tables
- ✅ Internet & NAT Gateways
- ✅ Security Groups & NACLs
- ✅ Route 53 & CloudFront
- ✅ VPC Peering & Transit Gateway

#### Tuesday: Compute Services
- ✅ EC2 instances & types
- ✅ Elastic Load Balancing
- ✅ Auto Scaling Groups
- ✅ AWS Lambda & serverless
- ✅ Hands-on labs for each service

#### Wednesday: Storage Solutions
- ✅ EBS volumes & snapshots
- ✅ Amazon S3 (buckets, versioning, lifecycle)
- ✅ EFS & FSx file systems
- ✅ AWS Snow Family
- ✅ Storage Gateway

#### Thursday: Security & IAM
- ✅ IAM users, roles, policies
- ✅ S3 bucket policies
- ✅ Encryption & secrets management
- ✅ Security best practices

#### Friday: Three-Tier Architecture Lab
- ✅ Build VPC with public/private subnets
- ✅ Deploy web servers with load balancer
- ✅ Configure security groups
- ✅ Test high availability

**📦 Deliverable:** Basic three-tier architecture deployment

---

### 🗄️ Week 3: Databases & Monitoring

**Theme:** Data Persistence & Observability

#### Monday: RDS & Relational Databases
- ✅ RDS database types
- ✅ Multi-AZ deployments
- ✅ Backups & snapshots
- ✅ Aurora workshops
- ✅ Best practices

#### Tuesday: DynamoDB & NoSQL
- ✅ NoSQL concepts
- ✅ DynamoDB tables & indexes
- ✅ Partition keys & sort keys
- ✅ Serverless architectures
- ✅ Hands-on labs

#### Wednesday: CloudWatch & CloudTrail
- ✅ Metrics & alarms
- ✅ Log groups & Insights
- ✅ Dashboards
- ✅ CloudTrail audit logs
- ✅ VPC Flow Logs

#### Thursday: Troubleshooting
- ✅ Database selection strategies
- ✅ Common issues & solutions
- ✅ Performance optimization
- ✅ Security monitoring
- ✅ Best practices

#### Friday: Service Deep Dive Presentations
- ✅ 4-hour research sprint
- ✅ 10-minute presentations
- ✅ Teach an AWS service to peers
- ✅ Q&A practice

**📦 Deliverable:** AWS Service presentation (10 min)

---

### 🚀 Week 4: Capstone Project (5 Days)

**Theme:** Production-Ready Application

> **Timeline:** Monday through Friday - Build, Test, and Present

#### Complete Three-Tier Application Architecture

```
User (HTTPS)
    ↓
CloudFront + AWS WAF
    ↓
Application Load Balancer (Public Subnets)
    ↓
EC2 Auto Scaling Group (Private Subnets)
    ↓
RDS MySQL (Isolated Subnets)
```

#### 5-Day Sprint

**Monday: Network & Database Foundation**
- ✅ Create VPC with 6 subnets (2 AZs)
- ✅ Configure Internet Gateway, NAT Gateway & route tables
- ✅ Set up security groups
- ✅ Deploy RDS MySQL with encryption
- ✅ Configure Secrets Manager

**Tuesday: Application Tier**
- ✅ Create S3 bucket for application assets
- ✅ Create IAM role for EC2 instances
- ✅ Build launch template with user data script
- ✅ Deploy EC2 instances in Auto Scaling Group
- ✅ Test database connectivity

**Wednesday: Load Balancing & Scaling**
- ✅ Create target group
- ✅ Configure Application Load Balancer
- ✅ Set up health checks
- ✅ Configure Auto Scaling policies
- ✅ Test application via ALB

**Thursday: Security & CDN**
- ✅ Deploy CloudFront distribution
- ✅ Configure AWS WAF rules
- ✅ Secure ALB with custom header
- ✅ Set up CloudWatch dashboards & alarms
- ✅ Configure SNS notifications
- ✅ End-to-end testing

**Friday: Presentation Day**
- ✅ Create architecture diagram
- ✅ Complete Well-Architected Framework review
- ✅ Record demo video
- ✅ Prepare presentation slides
- ✅ Present to cohort (15-20 minutes)
- ✅ **After presentation:** Complete cleanup

**📦 Deliverable:** Complete production-ready three-tier app + presentation + demo

---

## 🚀 Getting Started

### Prerequisites

- AWS Account (sandbox, AWS Academy, or personal)
- Basic understanding of:
  - Networking concepts (IP addresses, subnets)
  - Linux command line
  - Web requests & databases
  - Basic programming (Python/JavaScript helpful)

### Setup Steps

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd 3-Tier-Application-AWS-Project
   ```

2. **Review the curriculum**
   - Read `AWS-Internship-Curriculum.md` for detailed learning resources

3. **Set up your AWS account**
   - Configure MFA
   - Create billing alerts
   - Set up IAM user (never use root!)

4. **Start Week 1**
   - Follow the structured daily curriculum
   - Complete hands-on labs
   - Build your AI chatbot project

---

## 📁 Repository Structure

```
3-Tier-Application-AWS-Project/
│
├── AWS-Internship-Curriculum.md          # Complete 4-week curriculum with links
├── Vibe-Coding-Lab.md                    # Week 1 hands-on AI coding lab
├── AWS-Service-Deep-Dive-Presentation-Instructions.md  # Week 3 presentation guide
├── Week 4 Schedule.md                    # Detailed capstone project timeline
│
├── 3-tier-console-guide (BEGINNER)/      # Step-by-step console deployment
│   ├── README.md                         # Project overview
│   ├── 00-course-overview-and-preflight.md
│   ├── 01-network-foundation.md
│   ├── 02-database-tier.md
│   ├── 03-application-tier.md
│   ├── 04-load-balancing-and-auto-scaling.md
│   ├── 05-cloudfront-and-security.md
│   ├── 06-monitoring-and-validation.md
│   ├── 07-presentation-and-well-architected.md
│   ├── 08-complete-resource-cleanup.md
│   └── course-resources/                # Application files (Flask, HTML, etc.)
│
└── frontend-boilerplate/                 # Starter templates for web apps
```

---

## 📚 Key Resources

### Week 1: AI & Development
- 🎓 [Udemy AI Ethics Course](https://www.udemy.com/course/ai-ethicsresponsible-use/)
- 🎓 [AWS SkillBuilder - Generative AI](https://skillbuilder.aws)
- 🎓 [Vibe Coding Bootcamp](https://www.udemy.com/course/vibe-coding-bootcamp-build-web-apps-with-ai-chatgpt-gemini-lovable/)

### Week 2: AWS Core Services
- 🎓 [AWS Networking Course](https://www.udemy.com/course/aws-networking-amazon-vpc-aws-vpn-hybrid-cloud/)
- 🎓 [AWS Cloud Practitioner](https://www.udemy.com/course/aws-certified-cloud-practitioner-new/)
- 🧪 [AWS SkillBuilder Labs](https://skillbuilder.aws) (Free Tier available)

### Week 3: Databases & Monitoring
- 🎓 [AWS Solutions Architect Associate](https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/)
- 🔬 [DynamoDB Immersion Day](https://catalog.workshops.aws)
- 🔬 [RDS PostgreSQL Workshop](https://catalog.workshops.aws)

### Week 4: Capstone Project
- 📖 3-tier-console-guide (BEGINNER)/ - Follow step-by-step
- 📖 AWS-Service-Deep-Dive-Presentation-Instructions.md
- 📖 Week 4 Schedule.md

---

## 🎯 Learning Path

### Recommended Daily Schedule

**Morning (3-4 hours):**
- 📺 Video lectures & reading
- 📝 Take notes on key concepts
- ❓ Review knowledge checks

**Afternoon (3-4 hours):**
- 🧪 Hands-on labs in AWS Console
- 💻 Coding exercises
- 🔧 Troubleshooting practice

**Evening (1-2 hours):**
- 📊 Review what you learned
- 🎯 Quiz yourself
- 📖 Read AWS documentation

---

## 💡 Tips for Success

### 1. **Hands-On Practice**
- Don't just watch videos - actually build things!
- Make mistakes in labs (that's how you learn)
- Take screenshots of your work

### 2. **Cost Management**
- ⚠️ **Set up billing alerts immediately**
- Use AWS Free Tier where possible
- Clean up resources after each lab
- Budget: ~$50-100 for the full 4 weeks

### 3. **Time Management**
- Block 6-8 hours per day
- Take breaks every 90 minutes
- Don't rush - understanding > completion

### 4. **Learning Strategies**
- **Week 1:** Experiment with AI tools
- **Week 2:** Rebuild labs from memory
- **Week 3:** Explain concepts to others
- **Week 4:** 5-day sprint - stay focused, ask for help early

### 5. **Getting Help**
- Use AWS documentation (docs.aws.amazon.com)
- Search AWS re:Invent videos on YouTube
- Ask AI assistants to explain concepts
- Join AWS communities (Reddit r/aws, Discord)

---

## 🎓 Assessment & Deliverables

### Week 1
- ✅ AI Ethics quiz
- ✅ Vibe-coded browser game (GitHub repo)
- ✅ Working chatbot with DALL-E

### Week 2
- ✅ VPC & Networking quiz
- ✅ Basic three-tier architecture deployment
- ✅ Security group configurations

### Week 3
- ✅ Database selection quiz
- ✅ CloudWatch dashboard
- ✅ 10-minute AWS Service presentation

### Week 4
- ✅ Complete three-tier application (5 days)
- ✅ Architecture diagram
- ✅ Well-Architected Framework analysis
- ✅ Final presentation (15-20 minutes)
- ✅ Demo recording
- ✅ Cleanup immediately after presentation

---

## ⚠️ Important Warnings

### Cost & Billing
> **WARNING:** Week 4 creates billable resources including NAT Gateway (~$32/month), RDS, ALB, and CloudFront. Always:
> - Set up billing alerts BEFORE starting
> - Use Lab Mode (single-AZ) for learning
> - **Complete cleanup Friday after presentations**
> - Resources running 5 days ≈ $15-25 total cost
> - Verify charges in Billing Dashboard after cleanup

### Security Best Practices
- ✅ Never use AWS root user for daily work
- ✅ Enable MFA on all accounts
- ✅ Never commit AWS credentials to GitHub
- ✅ Use IAM roles, not access keys
- ✅ Keep security groups restrictive

### Account Safety
- ✅ Use sandbox or AWS Academy account
- ✅ Set up AWS Budget alerts
- ✅ Review IAM permissions regularly
- ✅ Clean up after every lab

---

## 🏆 Capstone Project Highlights (Week 4)

### 5-Day Sprint Format

**Why 5 Days?**
- Simulates real-world project deadlines
- Intensive, focused learning experience
- Time to build, test, AND present
- Immediate cleanup to minimize costs

### Daily Breakdown

| Day | Focus | Hours | Output |
|-----|-------|-------|--------|
| **Mon** | VPC + Database | 8h | Network foundation + RDS |
| **Tue** | Application Tier | 8h | EC2 instances running app |
| **Wed** | Load Balancing | 8h | Working ALB + Auto Scaling |
| **Thu** | Security + Monitoring | 8h | CloudFront, WAF, CloudWatch |
| **Fri** | **Presentation Day** | 8h | Present + Demo + Cleanup |

### What Makes This Project Special

1. **Production-Ready Architecture**
   - Multi-AZ deployment
   - Private EC2 instances (no SSH!)
   - Encrypted RDS with Secrets Manager
   - CloudFront with AWS WAF

2. **Console-First Approach**
   - Understand before automating
   - See all configuration options
   - Better troubleshooting skills

3. **Complete Lifecycle**
   - Planning → Deployment → Testing → Presentation → Cleanup
   - Real-world workflow

4. **Included Sample App**
   - TicketHub event booking system
   - Flask + MySQL backend
   - No coding required - focus on AWS!

---

## 📞 Support & Community

### Getting Help
- 📧 Email your instructor
- 💬 Use cohort communication channel
- 🐛 GitHub Issues for technical problems
- 📚 AWS Documentation: docs.aws.amazon.com

### Additional Resources
- 🎥 [AWS re:Invent Videos](https://www.youtube.com/user/AmazonWebServices)
- 📖 [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- 🎓 [AWS Training & Certification](https://aws.amazon.com/training/)
- 🏗️ [AWS Architecture Center](https://aws.amazon.com/architecture/)

---

## 🚀 Next Steps

1. **Read the full curriculum:** Open `AWS-Internship-Curriculum.md`
2. **Set up your AWS account:** Enable MFA, create billing alerts
3. **Start Week 1:** Begin with Responsible AI & Ethics
4. **Join the community:** Connect with other learners
5. **Build amazing things!** 🎉

---

## 📝 License

This educational material is provided for AWS training purposes. Follow your organization's security and data-handling policies.

---

<div align="center">

**Built with ❤️ for AWS Cloud Architecture Interns**

*Ready to become a cloud architect? Let's get started!* 🚀

[🔝 Back to Top](#-aws-cloud-architecture-internship---4-week-program)

</div>
