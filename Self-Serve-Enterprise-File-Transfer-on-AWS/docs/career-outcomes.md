# Career outcomes

## Target roles

| Role | How this course helps |
|------|------------------------|
| **Cloud Integration Engineer** | Hands-on Transfer Family, S3 pipelines, partner onboarding |
| **AWS Solutions Architect** | Reference architectures, security tradeoffs, migration narratives |
| **Platform Engineer** | Self-serve APIs, catalog models, operational runbooks |
| **MFT / EDI Specialist (modernized)** | Map legacy concepts to AWS-managed services |
| **DevOps / SRE** | Observability, idempotency, failure modes, cost controls |

## Skills matrix (graduate profile)

| Skill domain | Proficiency after course |
|--------------|--------------------------|
| Transfer protocols (SFTP/FTPS) | **Proficient** — deploy and harden |
| S3 data movement patterns | **Proficient** |
| IAM / KMS for B2B | **Proficient** |
| Workflow orchestration | **Working** → **Proficient** with capstone |
| Self-serve API design | **Working** |
| Compliance storytelling | **Aware** → **Working** (audit, retention) |
| Terraform for integration | **Working** |
| Legacy MFT migration planning | **Aware** → **Working** (Track C capstone) |

## Portfolio artifacts

Include in LinkedIn / portfolio:

1. **Architecture diagram** (capstone) — C4 or logical view  
2. **Demo video** (3–5 min) — SFTP upload → process → outbound  
3. **Runbook excerpt** — alarms, escalation, partner onboarding  
4. **IaC repo link** — redact account IDs; show module structure  

## Interview preparation

### Common questions

1. How do you isolate **partner A** from **partner B** on a shared Transfer endpoint?  
2. What IAM trust policies does Transfer Family require, and what breaks if `aws:SourceArn` is too tight?  
3. How do you guarantee **exactly-once** or **at-least-once** semantics in file pipelines?  
4. When would you use a **connector** vs. a **managed SFTP server**?  
5. How do you design **self-serve** without exposing raw IAM or bucket-wide listing?  

### Suggested answers (study prompts)

- Prefix-scoped IAM policies per partner; separate users or logical directory mappings.  
- Trust `transfer.amazonaws.com` with `aws:SourceAccount`; validate against AWS docs for connector vs. server roles.  
- Idempotency keys in DynamoDB; content hashes; S3 versioning; Step Functions task tokens.  
- Connectors for **pull/push to remote** SFTP; servers for **partner uploads to you**.  
- Cognito + API that returns only authorized connections; no direct SFTP credential sharing in UI.  

## Certification alignment (external)

This course **complements** (does not replace):

- **AWS Certified Solutions Architect – Associate/Professional**  
- **AWS Certified DevOps Engineer – Professional**  

Map week 2–4 content to SAA/DOP domain objectives for study synergy.

## BayLearn credential

Completing with **≥ 80%** earns **BayLearn Certificate of Completion: Enterprise File Transfer on AWS** (configure issuance via LMS).

## Continuing learning

- BayAreaLa8s **BayRelay** advanced workshop (agentic control plane)  
- Enterprise **private capstone review** with principal architect  
- AWS **Immersion Day** Transfer Family sessions (public AWS events)  
