# Instructor Guide

**Course:** Terraform for Real Enterprises (Not Toy Projects)  
**Provider:** BayAreaLa8s · 8 weeks · 64–72 hours

---

## Course package contents

| Path | Purpose |
|------|---------|
| `course-modules/` | Full 8-week curriculum (lectures, assignments, quizzes, instructor notes) |
| `course-modules/STUDENT-WORKBOOK.md` | Student weekly checklist |
| `labs/week-XX/` | Step-by-step lab guides (LAB-*.md) |
| `labs/shared/environments/` | dev / test / prod Terraform stacks |
| `modules/` | VPC, compute modules |
| `scripts/aws/` | pause/resume, start/stop, verify-labs |
| `docs/` | Syllabus, onboarding, demo guides, runbooks |
| `capstone/` | Capstone options and rubric |

## Teaching materials (demo & run)

| Document | Purpose |
|----------|---------|
| [docs/INSTRUCTOR-DEMO-SCRIPT.md](../docs/INSTRUCTOR-DEMO-SCRIPT.md) | Numbered demo steps per lab |
| [docs/LAB-DEMO-GUIDE.md](../docs/LAB-DEMO-GUIDE.md) | Full run + student steps |
| [docs/STUDENT-ONBOARDING.md](../docs/STUDENT-ONBOARDING.md) | Send to students pre-cohort |
| `course-modules/week-XX/06-instructor-notes.md` | Per-week teaching notes |

## Lab demo & run guide (all 22 labs)

Step-by-step instructions: [docs/LAB-DEMO-GUIDE.md](../docs/LAB-DEMO-GUIDE.md)

## Pre-cohort setup (1–2 days)

1. **AWS**
   - Create OU or single sandbox account per student team
   - Budget alerts per account
   - Optional: AWS Organizations for Week 2

2. **GitHub**
   - Template repository from this course repo
   - Branch protection on `main`: require PR, require CI
   - Environments: `dev`, `prod` with reviewers

3. **Student onboarding email**

   Send link to [docs/STUDENT-ONBOARDING.md](../docs/STUDENT-ONBOARDING.md) with:
   - Required tools: Terraform 1.5+, AWS CLI, Git
   - `make lab-pause` after each session
   - Monorepo path: `training/Terraform-for-Real-Enterprises`

---

## Weekly teaching notes

### Week 1
- Emphasize **bootstrap vs workload** state
- Common failure: bucket name not globally unique
- Demo: `make lab-stop` / `make lab-start`

### Week 2
- Single-account mode is OK for small cohorts
- IAM lab may need org admin — provide pre-created role ARN

### Week 3
- Code review module interfaces, not implementation details
- Require semantic versioning discussion

### Week 4
- OIDC setup is hardest — schedule office hours
- CI can run validate-only without AWS on first PR

### Week 5
- Drift lab is favorite — encourage “malicious” console edits
- Use drift report template

### Week 6
- Stress: never edit state by hand without backup
- Walk through S3 versioning restore in sandbox

### Week 7
- Balance security vs lab pragmatism (scoped `ec2:*` in template)
- Checkov `soft_fail` in CI until students remediate

### Week 8
- Capstone presentations: 15 min strict
- Grading rubric in `capstone/README.md`

---

## Grading quick reference

| Component | Weight |
|-----------|--------|
| Weekly labs | 35% |
| Assignments | 15% |
| Architecture reviews | 10% |
| Capstone | 30% |
| Participation | 10% |

Collect weekly PRs tagged `week-01` … `week-08`.

---

## Cost management for cohort

Instruct students to run after every session:

```bash
make lab-pause
```

Resume before next session:

```bash
make lab-resume
```

Weekend full teardown:

```bash
make destroy ENV=dev
```

**Do not** destroy bootstrap bucket until course ends.

Estimated monthly cost per active student (dev only, NAT instance mode): **$15–40** depending on EC2 runtime.

---

## Lab demo & run guide (all 22 labs)

Step-by-step instructions for demoing and running every lab: [docs/LAB-DEMO-GUIDE.md](../docs/LAB-DEMO-GUIDE.md)

## Instructor smoke test (one command)

Run this before a cohort to confirm labs still work end-to-end (apply → start/stop → teardown) and finish with **no running resources**.

### Prerequisites

- AWS CLI authenticated to the intended lab account
- `labs/shared/environments/dev/backend.hcl` and `terraform.tfvars` created from the examples

### Command

```bash
./scripts/aws/verify-labs.sh all
```

### Expected result

- Script exits **0**
- You see:
  - `Apply complete!` for the dev stack
  - stop/start status showing instances transition `running → stopped → running`
  - `Destroy complete!` at the end
- Final `./scripts/aws/status-lab.sh` shows **no running** instances for `Course=terraform-enterprise`

### If `terraform init` fails (provider registry)

```bash
./scripts/aws/install-provider.sh 5.90.0
export TF_CLI_CONFIG_FILE=/tmp/terraform-lab.rc
./scripts/aws/verify-labs.sh all
```

---

## Support escalation

| Issue | Action |
|-------|--------|
| State lock | `terraform force-unlock LOCK_ID` after verifying no running apply |
| Stuck NAT GW charges | `terraform destroy` target NAT resources |
| CI OIDC failure | Re-check trust policy `sub` claim matches repo |

---

## Customization

- Change `LAB_TAG_VALUE` in `scripts/aws/config.sh` for your org
- Replace `bayareala8s-tf-course` project name in tags
- Add your logo to `docs/` for slide exports
