# Student handbook — Enterprise Integration Architecture

**Course ID:** `baylearn-eia-001`  
**Certificate:** BayLearn Certificate of Completion — Enterprise Integration Architecture

Read [`GETTING_STARTED.md`](../GETTING_STARTED.md) first. This handbook is the operating agreement for the rest of the course.

## 1. What you are being graded on

Architecture decisions, not Terraform cosmetics.

Every substantial answer should name:

1. The **requirement**
2. The **integration characteristics** (latency, size, consumers, protocol, sensitivity)
3. The **style** (API / Message / Event / File / ESB-Adapter / AI Agent)
4. **Rejected options** and the NFR they fail
5. Technology **last** (AWS example only after the style)

ADRs use [`templates/adr.md`](../templates/adr.md). Capstone packets use [`templates/portfolio.md`](../templates/portfolio.md).

## 2. Environment

| Requirement | Notes |
|-------------|--------|
| AWS **sandbox** account | Isolated from employer production. Prefer a dedicated student account. |
| Region | Default `us-west-2` (see `.env.example`) |
| Terraform ≥ 1.5 | `terraform version` |
| Python 3.10+ | Lambdas run **3.12** in AWS; 3.10+ is enough on your laptop |
| AWS CLI | `aws sts get-caller-identity` must succeed before Lab 2 |
| IAM | AdministratorAccess **in the sandbox** is acceptable. Do not use personal production keys. |

```bash
python3 scripts/check_prereqs.py
python3 -m pip install -r requirements.txt
```

Copy `terraform/labs/<lab>/terraform.tfvars.example` → `terraform.tfvars` (already gitignored). Change region there if your sandbox is not `us-west-2`.

## 3. Course player

From the repository root (required so lessons load):

```bash
./scripts/start_course.sh
```

Open http://localhost:8080/course-ui/

Do **not** open `index.html` as a `file://` URL — the player cannot fetch markdown that way.

Mark lessons, labs, and capstones complete in the player so the certificate can unlock. Challenges require a correct direction **and** a rationale of at least 40 characters.

## 4. Labs

| ID | AWS? | Validator |
|----|------|-----------|
| lab-01-classification | No | Worksheet with 15 rationales |
| lab-02-api … lab-07-large-files | Yes | HTTP / queues / files against the stack |
| lab-08-esb-modernization | Optional façade | ADR + local strangler demo |
| lab-11-chaos | Yes (dedicated stack) | Notes (C1–C7, min four) + DLQ drill |
| lab-12-security | Yes | **FAIL** while `insecure=true` |
| lab-13-observability | Yes | Metrics lambda + dashboard |
| lab-15-ai-agent | Yes | Tools + HITL `/approve` |

```bash
./scripts/lab_up.sh <id>
python3 scripts/validate_lab.py <id>
./scripts/lab_down.sh <id>
```

If validation times out: CloudWatch Logs for the lab Lambda, IAM, and event source mappings — then the remediation line printed by the validator.

**Cleanup is part of the lab.** Leaving stacks up is a cost incident.

## 5. Cost

- Destroy after each session: `./scripts/lab_down.sh <id>` or `./scripts/destroy_all.sh --yes`
- Transfer Family (Lab 6) is **off** unless the instructor enables it for a live SFTP hour
- No NAT gateways, no always-on EC2, no unused ONLINE transfer endpoints

## 6. Capstones

You receive a brief, not a finished platform. A **working slice** exists under `terraform/capstones/` so you can prove styles run. Your diagrams and ADRs must still be yours.

```bash
./scripts/lab_up.sh banking    # or ecommerce | healthcare | manufacturing
python3 scripts/validate_lab.py banking
./scripts/lab_down.sh banking
```

Forbidden: `AI → unrestricted production database`.  
Required: `AI → authorized tools → integration layer → authorized service`.

## 7. Submissions

`submissions/` is gitignored. Create files locally:

```text
submissions/lab-01/worksheet.md
submissions/lab-08/adr.md
submissions/lab-11/notes.md
submissions/capstones/banking/   (README, ADRs, diagram notes)
submissions/final-assessment/
```

Do **not** submit:

- `labs/lab-01-classification/sample-completed-worksheet.md` as your Lab 1
- `labs/lab-08-esb-modernization/reference/adr.md` as your Lab 8
- Secrets, `terraform.tfstate`, or account IDs in write-ups

## 8. Academic integrity

Samples and reference ADRs exist so **instructors** can smoke-test validators. Using them as your submission is plagiarism for this course.

You may reuse **your** lab code inside capstones. You may not paste another cohort’s ADRs.

## 9. Certificate

The player issues a completion certificate when:

- All 15 modules’ lessons are marked complete
- All 12 labs are marked complete
- All 25 architecture challenges are complete (correct option + rationale)
- All four capstones are marked complete
- The final assessment is marked submitted

Your instructor may still require oral defense of the final assessment.

## 10. Getting unstuck

1. Re-read the lab **Architecture** and **Architecture Questions** before changing Terraform.
2. Read the validator **Remediation** line.
3. Confirm you ran commands from the **repo root**.
4. Ask your instructor with: requirement, style you chose, error text, correlation ID.

## 16-week rhythm (self-paced or cohort)

| Week | Focus |
|------|--------|
| 1 | Module 1 + Lab 1 |
| 2 | Module 2 + Lab 2 |
| 3 | Module 3 + Lab 3 |
| 4 | Module 4 + Lab 4 |
| 5 | Module 5 + Lab 5 |
| 6 | Module 6 + Lab 6 (Transfer off unless scheduled) |
| 7 | Module 7 + Lab 7 |
| 8 | Modules 8–9 + Lab 8 |
| 9 | Module 10 (patterns) |
| 10 | Module 11 + Lab 11 |
| 11 | Module 12 + Lab 12 |
| 12 | Module 13 + Lab 13 |
| 13 | Modules 14–15 + Lab 15 |
| 14 | Capstones 1–2 |
| 15 | Capstones 3–4 |
| 16 | Final assessment + certificate |

Compressed workshops: Modules 1–7 in days 1–3; modernization, security, agents, one capstone in days 4–5.
