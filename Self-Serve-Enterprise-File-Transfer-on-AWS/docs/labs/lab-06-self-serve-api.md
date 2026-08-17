# Lab 6 — Self-serve API surface

**Week 6 · Estimated time: 5 hours**

> **Terraform:** Cognito user pool, HTTP API (`/v1/connections`, `/v1/jobs`), API Lambda. Login: `./scripts/cognito_login.sh`.

## Objectives

Expose a minimal **self-serve** API: authenticated users manage connection records and submit transfer jobs.

## Steps (Terraform)

### 1. Get token

```bash
./scripts/cognito_login.sh
source <(grep export .lab/cognito_token.json 2>/dev/null || true)
# Or:
export BAYLEARN_ID_TOKEN=$(jq -r '.AuthenticationResult.IdToken' .lab/cognito_token.json)
API=$(terraform -chdir=infra/environments/lab output -raw api_endpoint)
```

### 2. Create connection

```bash
curl -s -X POST "$API/v1/connections" \
  -H "Authorization: Bearer $BAYLEARN_ID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Vendor Demo","type":"SFTP_INBOUND"}' | jq .
```

### 3. List connections

```bash
curl -s "$API/v1/connections" -H "Authorization: Bearer $BAYLEARN_ID_TOKEN" | jq .
```

### 4. Submit job

```bash
CONN=$(curl -s "$API/v1/connections" -H "Authorization: Bearer $BAYLEARN_ID_TOKEN" | jq -r '.connections[0].connection_id')
BUCKET=$(terraform -chdir=infra/environments/lab output -raw landing_bucket)
KEY="partners/demo/inbound/sample.csv"
curl -s -X POST "$API/v1/jobs" \
  -H "Authorization: Bearer $BAYLEARN_ID_TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-idempotency-key: lab06-$(date +%s)" \
  -d "{\"connection_id\":\"$CONN\",\"source_key\":\"$KEY\"}" | jq .
```

## Domain model (simplified)

| Entity | Attributes |
|--------|------------|
| **Connection** | `connection_id`, `owner_sub`, `name`, `type` (SFTP_INBOUND, S3_TO_SFTP), `status` |
| **Job** | `job_id`, `connection_id`, `state`, `created_at`, `correlation_id` |

Store in DynamoDB tables or single-table design.

## API (minimum)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/v1/connections` | List caller's connections |
| POST | `/v1/connections` | Create connection metadata (no raw passwords in body) |
| POST | `/v1/jobs` | Submit job `{ "connection_id", "source_key" }` |
| GET | `/v1/jobs/{job_id}` | Job status |

## Auth

- Cognito User Pool + JWT authorizer on API Gateway.  
- Map `sub` to `owner_sub`; deny cross-user access.

## Implementation path

1. Create User Pool and test user.  
2. Lambda handlers + API Gateway HTTP API.  
3. `POST /v1/jobs` triggers Step Functions (Lab 4) or async stub.  

## Deliverables

- `submissions/week-06/openapi.yaml` (3+ endpoints)  
- Postman collection **or** 2-min screen recording  
- README: authZ rules  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| Cognito auth enforced | 3 |
| CRUD/list scoped to user | 3 |
| Job submission works | 3 |
| OpenAPI / collection | 1 |

## BayServe alignment

Optional: compare your API to BayServe connection catalog patterns (read-only review of platform docs if provided by instructor).
