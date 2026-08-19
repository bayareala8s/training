# Lesson 2.7 — Authentication and Authorization

**Module:** 02 — API-Based Integration  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Separate authentication (who) from authorization (what).
2. Choose OAuth2/OIDC, IAM, mTLS, or API keys for the right audience.
3. Apply least privilege to the integration identity, not the human user only.

---

## Enterprise scenario

A vendor kept a static API key in a mobile binary. The key could POST refunds. Authentication happened; authorization was “if you have the key, you are God.” That is not an enterprise API.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Authentication establishes identity: a user, an app, a partner system. Authorization decides permitted operations and data. They are different controls. API keys identify an app poorly and do not bind a user. OAuth2/OIDC binds users and apps with scopes. mTLS binds machines. IAM binds AWS principals. Fine-grained authorization (this customer may see only their orders) often lives in the application after identity is proven.

---

## WHEN an Enterprise Architect uses it

- Human users: OIDC + scoped tokens.
- Service-to-service inside AWS: IAM or private mTLS.
- Partners: OAuth client credentials or mTLS plus allow lists.
- Always: least privilege on the execution role behind the API.

### When NOT to use it

- API keys as the only control for money movement.
- Long-lived God tokens in Git.
- Authorizing only at the edge and trusting every downstream call blindly without identity propagation.

---

## HOW — the pattern (vendor-neutral)

Define the audience. Propagate a correlation ID and a subject. Enforce object-level auth in the service. Log access decisions for audit. Rotate credentials. Prefer short-lived tokens. For employees versus customers, do not mix identity stores accidentally.

### Architecture diagram

```mermaid
flowchart LR
  U[User] --> IdP[IdP]
  IdP --> T[Token]
  T --> GW[API Gateway]
  GW --> AuthZ[Authorize]
  AuthZ --> Svc[Service]
  Svc --> IAM[Execution role]
```

---

## HOW — AWS implementation (after the pattern)

API Gateway authorizers: JWT, Lambda, IAM. Cognito can issue tokens. The Lambda’s IAM role is a second identity—it must not have dynamodb:* on all tables. Module 12 deepens this. Lab 2 requires IAM least privilege on DynamoDB.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Logging raw access tokens.
- Using the same role for read APIs and administrative replay.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| JWT user tokens | User-aware authz | Revocation and clock skew complexity |
| IAM service auth | Strong AWS binding | Awkward for external partners |

---

## Architecture decision prompt

The mobile app and the batch partner both create orders. Do they share a credential? What scope prevents the mobile app from issuing refunds?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** Why are API keys insufficient for refunds?

*Answer.* They poorly bind identity, are often embedded or shared, and rarely encode least-privilege user context.

---

## Architect's note

Security is an NFR in the decision framework, not a later overlay.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
