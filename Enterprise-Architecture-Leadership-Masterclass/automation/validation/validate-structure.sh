#!/usr/bin/env bash
# Validate course structure: modules, labs, quizzes, seed JSON.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

FAIL=0
pass() { echo "  PASS: $*"; }
fail() { echo "  FAIL: $*"; FAIL=$((FAIL + 1)); }

echo "==> validate-structure (repo: $ROOT)"

# --- 10 modules with README ---
echo "--> Modules (README)"
for i in 01 02 03 04 05 06 07 08 09 10; do
  dir=$(ls -d modules/module-$i-* 2>/dev/null | head -1 || true)
  if [[ -z "${dir}" ]]; then
    fail "missing module directory for $i"
  elif [[ ! -f "$dir/README.md" ]]; then
    fail "$dir/README.md missing"
  else
    pass "$dir/README.md"
  fi
done

# --- Labs with student-instructions ---
echo "--> Labs (student-instructions.md)"
for i in 01 02 03 04 05 06 07 08 09 10; do
  dir=$(ls -d labs/lab-$i-* 2>/dev/null | head -1 || true)
  if [[ -z "${dir}" ]]; then
    fail "missing lab directory for $i"
  elif [[ ! -f "$dir/student-instructions.md" ]]; then
    fail "$dir/student-instructions.md missing"
  else
    pass "$dir/student-instructions.md"
  fi
done

# --- Quizzes ---
echo "--> Quizzes"
for i in 01 02 03 04 05 06 07 08 09 10; do
  q="assessments/quizzes/module-$i-quiz.md"
  if [[ -f "$q" ]]; then
    pass "$q"
  else
    fail "$q missing"
  fi
done

# --- Capstone essentials ---
echo "--> Capstone package"
for f in \
  capstone/scenario/README.md \
  capstone/student-brief/capstone-brief.md \
  capstone/datasets/README.md \
  capstone/reference-architecture/README.md \
  capstone/rubric/capstone-rubric.md \
  capstone/presentation-template/executive-presentation-outline.md \
  student/templates/25-executive-presentation-outline.md \
  STUDENT_START_HERE.md
do
  if [[ -f "$f" ]]; then pass "$f"; else fail "$f missing"; fi
done

# --- BayLearn seed files exist ---
echo "--> BayLearn seed files present"
for f in course modules lessons assignments rubrics materials quizzes cohort; do
  path="baylearn-seed/$f.json"
  if [[ -f "$path" ]]; then pass "$path"; else fail "$path missing"; fi
done

# --- JSON parse ---
echo "--> Seed JSON parse"
if python3 "$ROOT/automation/validation/validate-json.py"; then
  pass "validate-json.py"
else
  fail "validate-json.py"
fi

# --- Dataset pointer ---
echo "--> Dataset"
if [[ -f student/datasets/northstar-application-inventory.csv ]]; then
  pass "student/datasets/northstar-application-inventory.csv"
else
  fail "application inventory CSV missing"
fi

echo
if [[ "$FAIL" -eq 0 ]]; then
  echo "OK: structure validation passed"
  exit 0
else
  echo "ERROR: $FAIL check(s) failed"
  exit 1
fi
