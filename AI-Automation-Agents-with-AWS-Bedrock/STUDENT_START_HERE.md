## Student Start Here — AI Automation & Agents with AWS Bedrock

Welcome! This guide gets you from zero to your first successful lab in under 30 minutes.

### Course home (BayLearn)

- **BayLearn course:** https://baylearn.bayareala8s.com/courses/9d6c8974-eab4-45b3-aa0d-a058b9cda228/
- **GitHub repo (monorepo):** https://github.com/bayareala8s/training → folder `AI-Automation-Agents-with-AWS-Bedrock/`

### What you need before Week 1

| Item | Action |
|------|--------|
| AWS account | Learner/sandbox account with billing alerts enabled |
| Bedrock access | Enable **Amazon Nova Lite** (`amazon.nova-lite-v1:0`) in `us-east-1` |
| Python 3.11+ | `python3 --version` |
| AWS CLI v2 | `aws sts get-caller-identity` |
| Git | Clone the repo above |

### Week-by-week path

| Week | Read | Do |
|------|------|-----|
| 1 | `weeks/WEEK_01.md` | `labs/week01/` local Bedrock scripts |
| 2 | `weeks/WEEK_02.md` | Deploy SAM stack: `labs/scripts/labs.sh cycle` |
| 3 | `weeks/WEEK_03.md` | Classification + validation labs |
| 4 | `weeks/WEEK_04.md` | Step Functions workflow |
| 5 | `weeks/WEEK_05.md` | API Gateway (`/classify`, `/summarize`, `/route`) |
| 6 | `weeks/WEEK_06.md` | Audit + dashboard (`labs/week06/`) |
| 7 | `weeks/WEEK_07.md` | Agent router + memory |
| 8 | `weeks/WEEK_08.md` | Capstone — pick one option A–D in `labs/week08/` |

Full file map: `BAYLEARN_MODULE_MAP.md`

### First lab (Week 1)

```bash
cd labs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

cd week01
python invoke_bedrock.py
python compare_outputs.py
```

### Deploy labs to AWS (Week 2+)

```bash
cd labs
export PROJECT_PREFIX=ba-la8s-ai-YOURNAME   # unique per student
./scripts/labs.sh cycle                     # deploy, test, teardown (safe first run)
```

When ready to keep the stack running for the week:

```bash
./scripts/labs.sh start
source .stack.env
./scripts/labs.sh verify
```

**Stop when done** to avoid charges: `./scripts/labs.sh stop` — see `labs/COST_CONTROL.md`.

### Capstone options (Week 8)

Pick **one** to extend for your portfolio (or demo all four):

| Option | Track | API |
|--------|-------|-----|
| A | Incident triage | `POST /capstone/incident` |
| B | Document classification | `POST /capstone/document` |
| C | Approval workflow | `POST /capstone/approval/request` + `/decide` |
| D | Enterprise agent | `POST /capstone/agent` |

Details: `CAPSTONE_HANDBOOK.md` and `labs/week08/README.md`.

### Where to get help

1. Check `LABS_GUIDE.md` for step-by-step lab instructions
2. Run unit tests locally: `cd labs && pytest tests/ -v`
3. Ask in BayLearn discussion forums or class Slack
4. Instructor materials: `COURSE_GUIDE.md`, `INSTRUCTOR_LESSON_PLANS.md`

### Portfolio checklist (end of course)

- [ ] Architecture diagram for your capstone
- [ ] Runnable repo with `README` instructions
- [ ] Evidence of validation + audit trail (correlation ID query)
- [ ] CloudWatch dashboard screenshot
- [ ] Cost/risk analysis (1–2 pages)
- [ ] Demo video or live demo script

Good luck — build something you'd be proud to show in an interview.
