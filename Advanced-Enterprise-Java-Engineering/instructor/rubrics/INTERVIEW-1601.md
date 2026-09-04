# Rubric — INTERVIEW-1601 Practice mode

**Type:** INTERVIEW  
**awsLab:** no (CLI + paper)  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

Reveal-first or one memorized paragraph in both maturity boxes must **not** max Diagnostic method (20%) or Technical accuracy (25%).

Do **not** require a BayLearn UI, Bedrock, or AWS apply. Do **not** require Principal-length answers.

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | 3–5 real `AEJE-IQ-*` ids; Engineer + Senior/Staff differ in scope; BayPay create path named correctly | Two levels present; one is a clone or one id is invented | One paragraph reused; wrong serving plane (`PaymentCluster` as prod) |
| Diagnostic method | `simulator.py --mode practice` without `--reveal` first; gap list after optional reveal; timed item marked honestly | Wrote first; skipped gap list | Reveal-first, or opened `solutions/INTERVIEW-1601/` before drafts |
| Production awareness | No apply, no portal required, no leftover-ND bounce, no TLS-off in answers | Mentions paper but still “would apply EKS to be sure” | Applied AWS or invoked Bedrock as the grade path |
| Trade-off analysis | Higher maturity names a this-quarter trade-off (ECS default vs EKS, 99.9% vs 99.99%, monolith vs hop) | One honest difference in scope | No trade-off; Staff box is longer Engineer |
| Security / reliability | Avery UUID / `c1601a11-…` ok; no PAN / password / label-cardinality; secrets refused | Avery named | Secrets or PAN in notes |
| Communication | Two voices a partner could hear; timed row labeled | Readable notes, thin second voice | Fragment ids only |
| Efficiency | 60–90 minutes; 3–5 items; one 8-minute variant | Complete but unfocused | Fewer than 3 items or untimed-only with no variant |

A portal 404 is not a defect. A 101st invented question caps Technical accuracy at 3 or below.

**Pass guideline:** weighted score ≥ 70, ≥3 ids, two non-clone maturities, write-before-reveal, one 8-minute row, no apply / Bedrock / portal requirement.
