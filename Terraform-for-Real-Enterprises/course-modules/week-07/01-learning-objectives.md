# Week 7 — Learning Objectives

By the end of this module, students will be able to:

## Knowledge (Remember / Understand)

1. Explain **least privilege** for Terraform CI/CD roles and why long-lived admin credentials are unacceptable in enterprises.
2. Describe how **resource tags** support cost allocation, automation, and attribute-based access control (ABAC).
3. Compare static analysis tools (Checkov, tfsec, tflint) and what classes of risk each detects.
4. Define **policy-as-code** and how OPA/Sentinel, SCPs, and Config rules complement Terraform guardrails.

## Skills (Apply / Analyze)

5. Refine a Terraform runner IAM policy by replacing overly broad actions with scoped permissions.
6. Enforce required tags through variables, validations, and `default_tags` consistent with course standards.
7. Run Checkov against modules and shared environments; document pass/fail and accepted risks in a validation report.
8. Integrate or document security checks in CI consistent with Week 4 pipelines.

## Professional practice (Evaluate / Create)

9. Map Terraform controls to a compliance framework excerpt (e.g., SOC2 CC6, CIS AWS benchmark themes).
10. Propose a governance model: who approves policy exceptions, how findings are tracked, and SLAs for remediation.

## Bloom’s alignment

| Level | Objective # |
|-------|----------------|
| Understand | 1–4 |
| Apply | 5–8 |
| Evaluate | 9–10 |

## Certification alignment (optional study)

- AWS Security Specialty: IAM, logging, detective controls
- HashiCorp Terraform Associate: sensitive data, provider configuration
