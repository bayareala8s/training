# Content Quality Standards

All generated materials for the Enterprise Architecture Leadership Masterclass must meet these standards.

---

## Case study and fiction rules

- Use **NorthStar Financial Services** consistently across every module
- Clearly label NorthStar as a **fictional** instructional case study
- Avoid proprietary or confidential claims
- Avoid implying affiliation with any real employer, bank, or cloud customer
- Invented application names, costs, and risks must be plausible but not attributable to real systems

---

## Architecture quality

- Explain **trade-offs**; do not claim one universal answer
- Connect technical decisions to **business value**, cost, risk, and operability
- Include security, resilience, and operational considerations in technical designs
- Prefer realistic enterprise constraints over idealized greenfield designs
- Document assumptions and decision rights explicitly

---

## Writing quality

- Use accessible language; avoid unnecessary jargon
- When jargon is required, define it once
- Use consistent terminology (see glossary below)
- Avoid generic filler and motivational fluff
- Prefer concrete deliverables and checklists over abstract advice
- Write at executive quality: concise, decision-oriented, scannable

---

## Branding and presentation

| Element | Standard |
| ------- | -------- |
| Platform | BayLearn |
| Owner | BayAreaLa8s |
| Colors | Dark navy, white, restrained gold accents |
| Slides | 16:9, 15–25 per module, speaker notes on every slide |
| Imagery | Professional; no cartoonish visuals |
| Tone | Practical architecture leadership |

---

## Terminology glossary (canonical)

| Term | Meaning in this course |
| ---- | ---------------------- |
| Enterprise architect (EA) | Leader who connects strategy to technology direction across domains |
| Solution architect (SA) | Architect focused on a solution or product delivery boundary |
| Architecture principle | Enduring rule guiding decisions and exceptions |
| Capability | What the business does, independent of org chart or systems |
| TIME | Tolerate, Invest, Migrate, Eliminate |
| Transition architecture | Interim architecture between current and target state |
| ADR | Architecture Decision Record |
| Guardrail | Preventive/automated control enabling safe autonomy |
| Gate | Review checkpoint requiring approval before proceeding |
| Landing zone | Foundational multi-account cloud environment with guardrails |
| Golden path | Supported, opinionated path for delivering a class of workloads |
| HITL | Human-in-the-loop approval for high-risk AI decisions |

---

## Assessment content rules

- Every quiz must include answer explanations and learning-objective mapping
- Every assignment must reference the standard rubric (or documented override)
- Scenario questions must require architecture judgment, not trivia
- Discussion questions must be usable live without a single “correct” script

---

## AWS lab rules

- Default to serverless
- Avoid NAT Gateway, always-on EC2, EKS, OpenSearch
- Avoid continuously running Transfer Family endpoints unless optional and cost-warned
- Include estimated cost, cleanup, tagging, validation, troubleshooting, and failure scenarios
- Separate reference solutions from student instructions

---

## Separation of student and instructor materials

| Audience | May include | Must not include |
| -------- | ----------- | ---------------- |
| Student | Labs, templates, datasets, quizzes without keys | Full answer keys, reference solutions, grading keys |
| Instructor | Everything student + solutions, keys, facilitation notes | — |

Packaging automation must enforce this separation.

---

## Anti-patterns (reject in QA)

- Placeholder text (`TODO`, `TBD`, `lorem ipsum`) in published assets
- Module content that ignores NorthStar
- “Best practice” claims without context or trade-offs
- Labs without cleanup (AWS)
- Broken internal links
- Duplicate contradictory guidance across modules
- Cartoon icons or meme imagery in slides
