# Simulator modes (Phase A)

Content-first. No portal session store.

| Mode | How to run | Reveal |
|---|---|---|
| Practice | `simulator.py --mode practice --domain Java/JVM` or `--id AEJE-IQ-00N` | Answers hidden until `--reveal` |
| Timed interview | Same as practice; student starts a timer (8 minutes default). Lab INTERVIEW-1601. |
| Rapid fire | `simulator.py --mode rapid-fire --count 10` | Prompt only; 60–90 seconds spoken |
| Troubleshooting | Lab INTERVIEW-1603 uses a symptom pack, not a trivia id |
| System design | Lab INTERVIEW-1604 / `PF-design.md` |
| Full mock loop | Lab INTERVIEW-1605 sequences practice + timed + troubleshooting + design |

Scoring uses the question `scoreRubric` plus course weights when the item is diagnostic: Technical 25 / Method 20 / Production 15 / Trade-off 15 / Security 10 / Comms 10 / Efficiency 5.
