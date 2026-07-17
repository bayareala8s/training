# Course Packaging

Build distributable ZIP packages under `packages/` for student, instructor, AWS labs, capstone, and BayLearn seed.

## Prerequisites

- `bash`, `zip`, `python3`
- Run from repository root (or let the script `cd` to root)

## Build

```bash
./automation/packaging/build-packages.sh
```

### Outputs (`packages/`)

| ZIP | Contents |
| --- | -------- |
| `student-course.zip` | Modules, labs (student files), student/, slides, course-specification (non-secret), STUDENT_START_HERE, README — **excludes** answer-keys and reference-solutions |
| `instructor-course.zip` | Instructor guides, scripts, grading, reference-solutions, answer-keys, slides notes, INSTRUCTOR_START_HERE |
| `aws-labs.zip` | `infrastructure/`, AWS lab folders (labs 05–08) |
| `capstone.zip` | `capstone/` + student presentation template + dataset pointer CSV |
| `baylearn-seed.zip` | All `baylearn-seed/*.json` |

## Validation first (recommended)

```bash
./automation/validation/validate-structure.sh
python3 ./automation/validation/validate-json.py
```

## Notes

- Student package must never include `assessments/answer-keys/` or `instructor/reference-solutions/`
- Capstone reference architecture is instructor-oriented; included in `capstone.zip` and instructor package — label files INSTRUCTOR when distributing to facilitators only if your ops policy requires splitting further
- Generated `packages/` is gitignored
