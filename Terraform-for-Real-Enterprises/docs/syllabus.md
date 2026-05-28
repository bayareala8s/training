# Week-by-Week Professional Syllabus

**Terraform for Real Enterprises (Not Toy Projects)** · 8 weeks · BayAreaLa8s

---

## Week 1 – Enterprise Infrastructure as Code Foundations

### Topics

- Terraform fundamentals
- Terraform vs CloudFormation
- Enterprise IaC challenges
- State management concepts
- Infrastructure lifecycle management

### Hands-On Labs

- Install Terraform
- Configure AWS provider
- Create secure remote state backend

### Deliverables

- Enterprise Terraform repo structure
- Remote backend configuration
- Baseline infrastructure deployment

**Materials:** [course-modules/week-01](../course-modules/week-01/) · [weeks/week-01](../weeks/week-01)

---

## Week 2 – AWS Multi-Account Architecture

### Topics

- AWS Organizations
- Shared services model
- Environment isolation
- Cross-account IAM roles
- Landing zone concepts

### Hands-On Labs

- Provision multi-account infrastructure
- Configure cross-account role access

### Deliverables

- Multi-account architecture design
- Cross-account Terraform workflows

**Materials:** [course-modules/week-02](../course-modules/week-02/) · [weeks/week-02](../weeks/week-02)

---

## Week 3 – Terraform Modules (Enterprise Design)

### Topics

- Reusable module architecture
- Inputs and outputs
- Module versioning
- Dependency management
- Backward compatibility

### Hands-On Labs

- Build VPC module
- Create reusable networking modules
- Publish internal modules

### Deliverables

- Production-grade Terraform modules
- Module documentation

**Materials:** [course-modules/week-03](../course-modules/week-03/) · [weeks/week-03](../weeks/week-03)

---

## Week 4 – CI/CD Pipelines for Terraform

### Topics

- GitOps workflows
- Terraform plan automation
- Approval workflows
- Secrets management
- Infrastructure validation

### Hands-On Labs

- GitHub Actions pipeline
- Plan → Review → Apply workflow
- Automated Terraform validation

### Deliverables

- Terraform CI/CD pipeline
- Automated deployment workflow

**Materials:** [course-modules/week-04](../course-modules/week-04/) · [weeks/week-04](../weeks/week-04)

---

## Week 5 – Environment Promotion & Drift Detection

### Topics

- Dev/Test/Prod promotion
- Drift detection strategies
- Infrastructure consistency
- Refactoring Terraform safely

### Hands-On Labs

- Promote infrastructure across environments
- Simulate infrastructure drift
- Remediate drift

### Deliverables

- Environment promotion workflow
- Drift remediation report

**Materials:** [course-modules/week-05](../course-modules/week-05/) · [weeks/week-05](../weeks/week-05)

---

## Week 6 – Rollback, Recovery & Disaster Recovery

### Topics

- Terraform failure recovery
- State repair techniques
- Rollback strategies
- Region failure planning
- Backup and recovery

### Hands-On Labs

- Simulate failed deployment
- Recover infrastructure from failure
- Restore Terraform state

### Deliverables

- Rollback automation workflow
- Recovery procedure documentation

**Materials:** [course-modules/week-06](../course-modules/week-06/) · [weeks/week-06](../weeks/week-06)

---

## Week 7 – Security, Compliance & Governance as Code

### Topics

- IAM least privilege
- Policy-as-Code concepts
- Cost governance
- Compliance guardrails
- Infrastructure auditability

### Hands-On Labs

- Secure Terraform deployments
- Implement tagging policies
- Configure compliance checks

### Deliverables

- Governance policies
- Security validation report

**Materials:** [course-modules/week-07](../course-modules/week-07/) · [weeks/week-07](../weeks/week-07)

---

## Week 8 – Capstone Project

Choose one track (details in [capstone](../capstone/README.md)):

1. **Enterprise Landing Zone** — Secure multi-account AWS foundation
2. **Shared Services Platform** — Centralized networking and monitoring
3. **Multi-Region DR Infrastructure** — Disaster recovery-enabled deployment
4. **Internal Terraform Platform** — Reusable platform for internal teams

### Capstone Deliverables

- Terraform repositories
- CI/CD pipelines
- Architecture diagrams
- Cost analysis
- Security review
- Final presentation / demo

**Materials:** [course-modules/week-08](../course-modules/week-08/) · [capstone](../capstone)

---

## Enterprise Skills Matrix

| Category | Skills |
|----------|--------|
| **Infrastructure engineering** | IaC, cloud automation, multi-account architecture, environment management, governance |
| **DevOps & platform** | GitOps, CI/CD, policy enforcement, infrastructure testing, release management |
| **Enterprise operations** | Rollback, DR, incident response, cost optimization, compliance readiness |

---

## Real-World Use Cases (By Industry)

| Industry | Examples |
|----------|----------|
| **Financial services** | Multi-account banking, shared services, DR environments |
| **Healthcare** | HIPAA-compliant deployment, isolated patient-data environments |
| **SaaS** | Automated environment provisioning, scalable cloud infra |
| **Enterprise IT** | Shared networking platforms, platform engineering enablement |

---

## Delivery Models

### Live cohort

- Weekend instructor-led sessions
- Guided architecture reviews
- Hands-on labs
- Office hours

### Self-paced

- Recorded videos
- Downloadable labs
- GitHub starter repositories
- Automated assessments

### Enterprise training

- Internal platform engineering workshops
- Terraform governance programs
- Custom architecture sessions
