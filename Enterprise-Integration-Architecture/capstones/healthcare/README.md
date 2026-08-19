# Capstone 3 — Secure Healthcare Integration Platform

**Domain:** Healthcare  
Security and privacy dominate style choices.

## Scenario

CareMesh Health (fiction) integrates patient portal, hospitals, labs, EHR, billing, notifications, and legacy interfaces (files, HL7-like adapters). Teach interoperability at **architecture** level using **FHIR** as published language at edges — not as a 400-page implementation course.

## Requirements (emphasis)

Authentication, authorization, encryption, audit, data minimization, access control. Minimum necessary on events. No diagnoses in routing keys.

## AI agent

Authorized assistant retrieves **permitted** information through governed APIs.

Explicitly demonstrate why this is unacceptable:

```text
AI → unrestricted production database
```

Required:

```text
AI → authorized tools → integration layer → authorized service → data
```

## Constraints

- Labs may stay single-account serverless; your **diagrams** must show network and classification.
- Prompt injection via lab PDFs / file contents must be in the threat model.

## Deliverables

Portfolio set + data classification table + agent tool catalog with denied tools listed.

## Working slice

```bash
./scripts/lab_up.sh healthcare
python3 scripts/validate_lab.py healthcare
./scripts/lab_down.sh healthcare
```

`GET /patients/{id}` enforces `x-actor-role` / `x-actor-id`. The agent tool `GetPatientSummary` HTTP-calls that API. `ScanAllPatients` is denied. There is no DynamoDB grant on the tools role.

