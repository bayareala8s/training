# SECURITY-1103 — Instructor solution

**Do not share these files with students before they submit tightened JSON.**

Students start from `labs/SECURITY-1103/starter/`. Apply is not required. Teaching account `123456789012` and CMK id `aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeee1103` are synthetic.

## Files

| File | Role |
|---|---|
| [iam-execution-role.json](iam-execution-role.json) | Pull, logs, one secret, one CMK |
| [iam-task-role.json](iam-task-role.json) | Separate principal; deny account-admin; no `GetSecretValue` |
| [task-definition.json](task-definition.json) | `secrets.valueFrom` ARNs; no plaintext `BAYPAY_DB_*` |
| [kms-key-policy.json](kms-key-policy.json) | Root administers; execution role decrypts via Secrets Manager |

A student file that matches contracts (split roles, no admin, no `changeme`, `valueFrom` ARNs, CMK names the execution role) passes even if SID strings differ.

## What the starter got wrong

- One role, `AdministratorAccess`, used as **both** `executionRoleArn` and `taskRoleArn`.
- Plaintext `BAYPAY_DB_URL` / `USER` / `PASSWORD=changeme` in `environment`.

The starter was valid-looking JSON. It was not the ACCOUNT.md contract.

## Required contracts

```text
execution:  ecr auth + pull baypay/payment-service
            logs on the payment log group
            secretsmanager:GetSecretValue on baypay/payment/db*
            kms:Decrypt on the teaching CMK
task:       not AdministratorAccess; no GetSecretValue for this app
task def:   secrets valueFrom :url:: :username:: :password::
            no changeme, no password environment
kms:        execution role can Decrypt; no Principal "*"
region:     us-west-2
```

`ecr:GetAuthorizationToken` requires `Resource: "*"` (AWS API shape). That is the only starred allow that is acceptable here. Call it out if a student flags it.

The deny on `iam:*` in the task role is teaching emphasis. An empty task-role policy also passes.

## Checklist

- [x] Two role names
- [x] No `AdministratorAccess`
- [x] Execution reads one secret + one CMK
- [x] Task does not copy `GetSecretValue`
- [x] Task def uses `valueFrom`
- [x] No plaintext password

## Diagram

AEJE-D-050: execution role reaches ECR, logs, Secrets Manager, and KMS. The JVM receives injected env. The task role is a separate, narrow principal.

## Scoring notes

`AdministratorAccess` remaining on either role fails Security / reliability. A leftover `changeme` fails Security / reliability regardless of role split. Copying `GetSecretValue` onto the task role without a written reason caps Technical accuracy. Skipping apply is not an Efficiency penalty.
