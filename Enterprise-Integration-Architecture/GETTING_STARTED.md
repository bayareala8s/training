# Getting started

Welcome to **Enterprise Integration Architecture** (BayLearn · BayAreaLa8s).

This is **not** an AWS services tutorial. You will decide **API vs Message vs Event vs File vs ESB/Adapter vs AI Agent** from requirements, then implement.

## First 30 minutes

1. Confirm tools (see below).
2. From the **repository root**:

```bash
python3 scripts/check_prereqs.py
python3 -m pip install -r requirements.txt
./scripts/start_course.sh
```

3. Open [http://localhost:8080/course-ui/](http://localhost:8080/course-ui/)
4. Read this page in the player (**Start**), then complete **Lesson 1.1**.
5. Do **Lab 1** (no AWS) before any Terraform lab.

## Tools you need

| Tool | Why |
|------|-----|
| Python **3.10+** | Labs, validators, course server (AWS Lambda runtime is 3.12) |
| Terraform **≥ 1.5** | AWS labs and capstones |
| AWS CLI v2 | Identity and optional debugging |
| A **sandbox AWS account** | Never production. Destroy stacks after each session. |
| Browser | Course player |

Optional: `boto3` (`pip install -r requirements.txt`) for `validate_lab.py`.

## How a week works

1. Lessons in the player (WHY → WHEN → HOW).
2. Architecture challenges (letter **and** ≥ 40 characters of rationale).
3. Lab workbook under `labs/` → deploy if AWS → `python3 scripts/validate_lab.py <lab-id>` → destroy.
4. Put written work in `submissions/` (gitignored so you do not commit secrets).

## AWS labs (after Lab 1)

```bash
./scripts/lab_up.sh lab-02-api
python3 scripts/validate_lab.py lab-02-api
./scripts/lab_down.sh lab-02-api
```

**Cost:** Destroy when you stop working. Lab 6 Transfer Family stays **off** (`enable_transfer_family=false`) unless your instructor runs an SFTP hour.

**Lab 12** starts insecure. `validate_lab.py lab-12-security` must **FAIL** until you set `insecure=false` and re-apply.

## Rules that fail the course

- Starting a design with an AWS service name.
- `LLM → production database`.
- Leaving Transfer Family ONLINE idle.
- Copying `sample-completed-worksheet.md` or the Lab 8 reference ADR and calling it your work.
- Committing `terraform.tfvars`, keys, or `.env`.

## Where to put work

| Deliverable | Path |
|-------------|------|
| Lab 1 worksheet | `submissions/lab-01/worksheet.md` |
| Lab 8 ADR | `submissions/lab-08/adr.md` |
| Lab 11 chaos notes | `submissions/lab-11/notes.md` |
| Capstone portfolio | `submissions/capstones/<name>/` |
| Final assessment | `submissions/final-assessment/` |

Challenges and lesson completion are stored in the player (`localStorage`). Use the same browser.

## Next

- Handbook: [`docs/STUDENT_HANDBOOK.md`](docs/STUDENT_HANDBOOK.md)
- 16-week plan: [`COURSE.md`](COURSE.md)
- ADR template: [`templates/adr.md`](templates/adr.md)
- Capstone checklist: [`templates/portfolio.md`](templates/portfolio.md)
