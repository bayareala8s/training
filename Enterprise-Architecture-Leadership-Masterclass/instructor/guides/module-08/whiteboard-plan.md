# Whiteboard Plan — Module 08: AI Strategy and Intelligent Enterprise Architecture

**Session:** Live cohort  
**Boards needed:** 1 large (or digital equivalent)

---

## Board 1 — Use-case scorecard (10 min)

Columns: Value · Feasibility · Data readiness · Risk/harm · Operability · Cost · Alignment  

Score the **incident decision assistant** live (1–5). Mark **Conditional-go** with HITL for severity ≥ High.

## Board 2 — Governed pipeline (10 min)

Boxes left-to-right:

```text
Intake → Infer (model/mock) → Validate schema → Deterministic rules → Persist → HITL? → Act/Advise
```

Red gates on Validate and HITL. Annotate: *model proposes; rules decide autonomy*.

## Board 3 — HITL triggers (8 min)

Sticky triggers: severity ≥ High · low confidence · regulated action · schema fail · novel category  

Ask: what must never be auto-executed at NorthStar?

## Board 4 — Eval + cost (7 min)

Two columns: **Quality measure** (e.g., field agreement vs labels) · **Cost/token** (per invoke, monthly estimate)  

Place 3 sample incident titles under Pass / HITL / Fail.

## Capture

Photograph boards; map to templates `12-ai-use-case-scorecard.md` and `19-ai-governance-checklist.md`.
