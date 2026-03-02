Perfect — below is a **clean, SADD-ready I-Profile Classification Summary Table** aligned to your Information Flow Control (IFC) model and EFT architecture.

This is structured formally for architecture documentation and ARC review.

---

# 4.X I-Profile Classification Summary

The I-Profile classification model categorizes actors based on:

* Origin (Internal / External)
* Interaction Type (Attended / Unattended)
* Enclave Boundary (Intra-Enclave / Inter-Enclave)
* Trust Level
* Privilege Impact
* Security Control Rigor

This model ensures consistent trust segmentation and layered defense enforcement across the EFT Platform.

---

## I-Profile Classification Summary Table

| I-Profile | Actor Type                               | Origin                   | Attended / Unattended | Enclave Relationship         | Trust Level                  | Typical Examples in EFT                                  | Primary Risk Consideration                     | Control Emphasis                                                                 |
| --------- | ---------------------------------------- | ------------------------ | --------------------- | ---------------------------- | ---------------------------- | -------------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------------------------------------- |
| **I-1**   | External Automated                       | External                 | Unattended            | Outside Enclave              | Lowest                       | External SFTP upload systems, Partner API integrations   | Untrusted input, malware risk, replay attempts | Boundary validation, Strong authentication, Input validation, Full logging       |
| **I-2**   | External Human                           | External                 | Attended              | Outside Enclave              | Low                          | Partner portal users (if enabled)                        | Credential compromise, session hijacking       | MFA, Session controls, RBAC                                                      |
| **I-3**   | Internal Human User                      | Internal                 | Attended              | Intra-Enclave                | Moderate                     | Business users viewing transfer status                   | Data overexposure                              | SSO integration, RBAC, Access auditing                                           |
| **I-4**   | Privileged Administrative User           | Internal                 | Attended              | Intra-Enclave                | High                         | IAM administrators, KMS admins, Platform config managers | Privilege misuse, configuration drift          | MFA mandatory, Approval workflows, Separation of duties, Immutable audit logging |
| **I-5**   | Governance / Oversight                   | Internal                 | Attended              | Intra-Enclave                | High (Read-Only)             | Compliance officers, Audit reviewers                     | Sensitive data visibility                      | Read-only access, Audit retention, Export controls                               |
| **I-6**   | Internal Automated (Management / Upload) | Internal                 | Unattended            | Intra-Enclave                | High (Controlled Automation) | Internal batch upload systems, CI/CD pipelines           | Misconfiguration, uncontrolled scale           | IAM service roles, Prefix scoping, Encryption enforcement, Monitoring            |
| **I-7**   | Intra-Enclave Service-to-Service         | Internal                 | Unattended            | Same Enclave                 | Very High (Controlled)       | Lambda → DynamoDB, Step Functions → ECS                  | Lateral movement                               | Role-to-role trust policies, Private networking, Least privilege IAM             |
| **I-8**   | Inter-Enclave Automated                  | Internal / Cross-Account | Unattended            | Cross-Enclave / Cross-Region | Segmented High               | Cross-region S3 replication, DynamoDB global tables      | Replication lag, cross-boundary risk           | Explicit trust policies, Replication monitoring, Encryption in transit & at rest |

---

# Trust Gradient Overview

Lowest Exposure Control → Highest Exposure Control

I-1 → I-2 → I-3 → I-4 → I-5 → I-6 → I-7 → I-8

Important Clarification:

* Exposure Risk is highest at I-1 (external origin).
* Privilege Impact is highest at I-4 (administrative human).
* Automation Risk scales with I-6 through I-8 (scale and cross-boundary behavior).

This gradient ensures:

* Boundary protection for low-trust actors
* Governance control for high-impact actors
* IAM scoping and segmentation for automated actors

---

# How This Strengthens Your SADD

This table demonstrates:

* Formal trust segmentation
* Zero-trust alignment
* Role-based enforcement
* Enclave boundary awareness
* Clear separation between human and automated actors
* Cross-region and cross-account clarity

ARC reviewers immediately see a structured trust governance model.

---

If you’d like, I can next:

* Create a visual “I-Profile Trust Ladder” diagram for inclusion
* Map each I-profile directly to your C2/C3 components
* Add NIST 800-53 control family references per I-profile
* Convert this into a formatted Excel appendix
* Integrate this directly into your Section 4 final draft structure

Tell me which direction you want to go.
