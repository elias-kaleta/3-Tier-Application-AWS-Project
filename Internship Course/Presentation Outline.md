# Presentation Outline

## 1. Introduction & Problem Statement

- What problem are we solving?
- Who are the target users?
- Why does this problem matter?
- What was our MVP scope and success criteria?

---

## 2. Architecture Overview

- High-level system architecture diagram (three-tier: presentation, application, data)
- How the tiers communicate
- Data flow from user request to response

---

## 3. AWS Services Used & Justification

For each service, cover:

- What it does in our architecture
- Why we chose it over alternatives
- How it fits into the three-tier model

---

## 4. Technical Decisions & Trade-offs

- Key decisions made during build (e.g., serverless vs EC2, SQL vs NoSQL)
- What trade-offs were accepted and why
- Bugs or edge cases encountered and how they were handled

---

## 5. AWS Well-Architected Framework Mapping

Address each pillar with specific examples from the project:

- **Operational Excellence** — How we deploy, monitor, and iterate (e.g., CloudWatch, IaC)
- **Security** — How we protect data and access (e.g., IAM roles, encryption, security groups)
- **Reliability** — How we handle failure (e.g., multi-AZ, health checks, backups)
- **Performance Efficiency** — How we chose the right resource types and sizes
- **Cost Optimisation** — How we minimized spend (e.g., right-sizing, free tier, on-demand vs reserved)
- **Sustainability** — How we reduce environmental impact (e.g., efficient resource use, scaling down when idle)

---

## 6. Areas for Improvement & Scaling Path

- What would we add with more time?
- How would this scale to more users? (Auto Scaling, caching, read replicas)
- What would a production-ready version look like?
- Any services we'd swap out at scale?

---

## 7. Retrospective

- What went well
- What we'd change next time
- Key learnings about AWS and the development process
