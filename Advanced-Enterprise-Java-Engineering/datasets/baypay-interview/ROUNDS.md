# BayPay interview rounds — Module 16

**Fictional company. Phase A is paper plus JSON.** Students may read this file. A live BayLearn interview UI is Phase B and is **not** required to pass.

## Modes (spec §25)

| Mode | Lab | What “done” means |
|---|---|---|
| Practice | INTERVIEW-1601 | Open a question, write Engineer + Senior (or Staff), then compare to the bank — no timer required |
| Timed interview | INTERVIEW-1601 (variant) or 1605 | Same quality bar under a clock (e.g. 8 minutes / question) |
| Rapid fire | INTERVIEW-1602 | Short answers, many items; depth is not the grade |
| Troubleshooting | INTERVIEW-1603 | Evidence → hypothesis → next gate; lucky RCA does not max Diagnostic method |
| System design | INTERVIEW-1604 | One BayPay design; trade-offs; portfolio `PF-design.md` |
| Full mock loop | INTERVIEW-1605 | Several rounds in one sitting, including one timed item |

## Bank

Exactly **100** records in [interview-bank/questions.json](../../interview-bank/questions.json). Domain counts are locked in `COURSE_MANIFEST.json`. Do not add a 101st question. Do not rewrite an id’s domain.

## Maturity

Answers must differ by **Engineer / Senior / Staff / Principal**. One memorized paragraph is a fail. The bank stores `engineerAnswer` plus the spec fields `seniorAnswer`, `staffAnswer`, `principalAnswer`.

## What you must not do

- Treat a model dump or a copied bank answer as your spoken answer in a live mock.
- Name instructor RCAs from INCIDENT labs as if they were the only correct interview story.
- Require a portal simulator or Bedrock.
- Invent a second 100-question file.
