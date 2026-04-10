# Nira — NIS TransferTrack Voice

Voice-enabled **lifecycle tracking and governance** for file transfer requests. This is **not** a transfer engine: no SFTP/S3 execution, orchestration, or provisioning.

## Executive & innovation briefing

**One line**  
Nira shows how leadership could **see the whole transfer portfolio at a glance** and **get answers quickly**—including by **asking in plain language**—instead of chasing spreadsheets and status meetings.

**Problem it illustrates**  
Large programs generate many interdependent requests. Executives need fast answers: *Where are we stuck? What’s off track? Who owns the risk?* That often still means ad-hoc updates and meetings.

**What to show (about 3–4 minutes)**  
1. **Dashboard** — Volume, blockers, aging risk, and how work sits across owners (portfolio story first).  
2. **Discovery** — **Advanced search** for precision; then **Ask Nira** so sponsors can describe what they want (“blocked in prod,” “still has open tasks”) without learning every field. The same intent drives the structured view either way.  
3. **Drill-down** — One request: lifecycle position, task health, evidence and audit trail—**accountability and governance** without claiming the app executes transfers.

**How to position voice**  
Lead with **outcomes** (clarity, speed, fewer surprises), not the microphone. Treat voice as **optional**: busy executives can **speak or type** natural language; it’s differentiation for hands-busy moments, not the only path. One line that works in the room: *“You can ask what’s blocked or who’s overloaded in plain language—including voice—without learning the product.”*

**Scope (say once)**  
Demo = **visibility and governance only**; it does **not** run file transfers.

**Innovation takeaway**  
**AI-assisted discovery** plus **portfolio analytics** in a form a sponsor can use in a meeting—faster clarity and clearer ownership, grounded in a working experience.

## Stack

- **Frontend:** React, TypeScript, Vite (browser Speech Recognition for Nira)
- **Backend:** Python FastAPI on AWS Lambda (Mangum), DynamoDB, S3 presigned uploads
- **Infra:** Terraform (API Gateway HTTP API, Lambda, DynamoDB, S3, CloudFront, IAM, CloudWatch)

## Quick start (local)

```bash
# Terminal 1 — API
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — UI (see docs for env vars if using real AWS tables)
cd frontend && npm install && npm run dev
```

## Deploy to AWS

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

### Demo environment (this account)

After `terraform apply` and `npm run build` + `aws s3 sync`, use Terraform outputs:

- **App (HTTPS):** run `terraform -chdir=infra/terraform output -raw app_url`
- **API:** run `terraform -chdir=infra/terraform output -raw api_endpoint`

Tight browser CORS (API + presigned S3 uploads): copy [infra/terraform/demo.tfvars.example](infra/terraform/demo.tfvars.example) to `infra/terraform/demo.tfvars`, set `cors_origins` to your `app_url`, then `terraform apply -var-file=demo.tfvars`.

**Redeploy UI + API (demo):** `bash scripts/deploy-demo.sh` (requires AWS CLI, Terraform, Node/npm, and `infra/terraform/demo.tfvars`).

## Tests

```bash
cd backend && pytest -q
cd frontend && npm run build
```

## Project layout

```
frontend/     React app
backend/      FastAPI application + lambda_handler.py
infra/terraform/   AWS resources
docs/         Deployment and operations notes
scripts/      build-lambda.sh
```
