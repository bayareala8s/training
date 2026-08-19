# Capstone 1 — Enterprise Payment Integration Platform

**Domain:** Banking  
**Do not start from a target AWS diagram.** Design from requirements.

## Engagement brief

Northbridge Bank (instructional fiction) receives payment instructions from corporate customers via **REST API**, **batch files**, and **SFTP**. You are the integration architect. The PMO wants “one platform.” They do not want a services tutorial.

## Existing architecture

- Core ledger: system of record, 300 ms reads for balances on a *different* channel (out of scope except isolation).
- A 2012 ESB still maps two historic partners (ISO 20022 over MQ).
- Ad-hoc SFTP on an EC2 jump box with a shared user `sftpuser`.
- Mobile app for retail is **not** this platform (do not couple them).

## Integration inventory (incomplete — extend it)

| ID | Source | Dest | Notes |
|----|--------|------|-------|
| P1 | Corporate REST | Ledger posting | Real-time, idempotent |
| P2 | Nightly CSV | Ledger | 100 MB–few GB |
| P3 | SFTP partners | Landing | Mixed naming |
| P4 | Ops | Humans | “Did ABC’s file arrive?” |

## Functional requirements

Real-time payments, batch processing, large files, duplicate detection, validation, reconciliation, audit, retry, DLQ, replay, encryption, **customer isolation**.

## NFRs (minimum)

- No double-post on retries.
- Customer A cannot list Customer B prefixes.
- Reprocess is auditable and approved.
- Edge ACK ≠ posted.
- Correlation IDs from API and files.

## Constraints

- Some customers will never leave SFTP this year.
- Transfer Family cost must be in the ADR.
- Agents cannot open the ledger database.

## AI component

Operations agent answers:

- Did Customer ABC's payment file arrive?
- Why did it fail?
- How many transactions failed?
- Can it be reprocessed?

**Reprocessing requires approval.** Tools only.

## Deliverables (portfolio)

1. Architecture diagram (your design — not a copy of `diagrams/13-banking-capstone.md` without decisions)
2. API design
3. File architecture
4. Event model
5. Message architecture
6. Security design
7. Observability design
8. ADRs (`templates/adr.md`)
9. Working implementation (Terraform + code; you may extend `terraform/labs` rather than invent from zero)
10. Failure scenarios and test notes

## Starter code

Working slice (compose API + queue posting + files + HITL tools):

```bash
./scripts/lab_up.sh banking
python3 scripts/validate_lab.py banking
./scripts/lab_down.sh banking
```

Stack: `terraform/capstones/banking/`. ADRs in this folder remain the source of truth for *your* design; the slice proves the styles run. Agents cannot open the ledger — tools call HTTP APIs only.

## Grading emphasis

Style choices with NFRs. Silent “everything on EventBridge” fails. LLM→database fails the course.
