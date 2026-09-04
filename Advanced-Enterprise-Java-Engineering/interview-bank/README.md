# Interview bank — Advanced Enterprise Java Engineering

Exactly **100** BayPay-scoped questions. Phase A: this folder plus Module 16 labs. Phase B (BayLearn UI) is optional and not required to pass.

| File | Role |
|---|---|
| [questions.json](questions.json) | Assembled bank (source of truth after merge) |
| [schema.json](schema.json) | Record contract |
| [modes.md](modes.md) | Simulator modes |
| [simulator.py](simulator.py) | Local practice / rapid-fire (no network) |
| `domains/*.json` | Authoring slices; merge with `qa/merge_interview_bank.py` |

Domains and counts match `COURSE_MANIFEST.json` `interviewBank.domainCounts`.

Run:

```bash
python3 interview-bank/simulator.py --mode practice --id AEJE-IQ-012
python3 interview-bank/simulator.py --mode rapid-fire --count 8 --seed 16
```

Do not commit a second bank. Do not send PAN or live secrets into a prompt.
