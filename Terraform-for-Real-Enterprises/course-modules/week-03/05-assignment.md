# Week 3 — Assignment: Enterprise Module Design Review

**Weight:** Part of 15% assignments grade · **Due:** End of Week 3 · **Length:** 2–3 pages or 800–1200 words + diagram

## Prompt

Review the course `modules/vpc/` module (or a module your team uses in production) as if you were the **platform architecture council** deciding whether to approve it for org-wide consumption.

### Tasks

1. **Interface audit** — Table of every input variable: name, type, required?, default, validation present?, documentation quality (1–5). Identify gaps.

2. **Output audit** — List outputs; flag any that expose unnecessary internals or missing values consumers need (e.g. for peering, TGW attachment).

3. **Composition sketch** — Diagram showing how `vpc`, `security-group`, and `compute` modules should compose for a three-tier web app. Include output → input arrows.

4. **Versioning policy** — Write semver rules for your org (when MAJOR vs MINOR). Include example: adding optional S3 endpoint = ? ; renaming output = ?

5. **Improvement plan** — Prioritized top five changes (with effort S/M/L). One must address security or compliance (Checkov-style concern).

## Rubric

| Criterion | Excellent (90–100%) | Proficient (75–89%) | Needs work (<75%) |
|-----------|----------------------|---------------------|-------------------|
| Interface audit | Complete table, actionable gaps | Most variables covered | Superficial |
| Outputs | Clear consumer-focused critique | Minor gaps | Missing |
| Composition diagram | Accurate data flow | Minor errors | Disconnected modules |
| Versioning | Correct semver semantics | One error | Treats all changes as patch |
| Improvement plan | Prioritized, realistic, includes security | Some prioritization | Vague wish list |

## Submission format

- `docs/assignments/week-03-yourname.md`
- Mermaid diagram for composition

## Academic integrity

Individual work. Cite Terraform module documentation where applicable.
