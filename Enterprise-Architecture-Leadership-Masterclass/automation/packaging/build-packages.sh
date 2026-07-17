#!/usr/bin/env bash
# Build student, instructor, aws-labs, capstone, and baylearn-seed ZIP packages.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$ROOT/packages"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

cd "$ROOT"
mkdir -p "$OUT"

echo "==> Packaging into $OUT (stamp $STAMP)"

# Copy helper: rsync if available, else cp -R then prune heavy/secret paths
copy_tree() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a \
      --exclude '.terraform/' \
      --exclude '.terraform.lock.hcl' \
      --exclude 'terraform.tfstate' \
      --exclude 'terraform.tfstate.*' \
      --exclude '.DS_Store' \
      "$src" "$dest"
  else
    cp -R "$src" "$dest"
  fi
}

prune_tf() {
  local root="$1"
  find "$root" -type d -name '.terraform' -prune -exec rm -rf {} + 2>/dev/null || true
  find "$root" \( -name '.terraform.lock.hcl' -o -name 'terraform.tfstate' -o -name 'terraform.tfstate.*' \) -delete 2>/dev/null || true
}

zip_dir() {
  local src="$1" zipfile="$2"
  local tmpzip
  # macOS mktemp requires trailing X's (no suffix after XXXXXX)
  tmpzip="$(mktemp "$OUT/.pack-XXXXXX")"
  rm -f "$tmpzip"
  (
    cd "$src"
    zip -qr "$tmpzip.zip" .
  )
  mv -f "$tmpzip.zip" "$zipfile"
}

# --- Student package (exclude answer-keys and reference-solutions) ---
echo "--> student-course.zip"
TMP_STUDENT="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_STUDENT" "${TMP_INSTRUCTOR:-}" "${TMP_AWS:-}" "${TMP_CAP:-}" "${TMP_SEED:-}"
  rm -f "$OUT"/.pack-* 2>/dev/null || true
}
trap cleanup EXIT

for path in \
  README.md \
  STUDENT_START_HERE.md \
  COURSE_MANIFEST.json \
  modules \
  labs \
  slides \
  student \
  course-specification \
  assessments/assignments \
  assessments/rubrics \
  assessments/quizzes \
  infrastructure \
  diagrams \
  diagram-library \
  capstone/scenario \
  capstone/student-brief \
  capstone/datasets \
  capstone/presentation-template \
  capstone/rubric
do
  if [[ -e "$ROOT/$path" ]]; then
    if [[ -d "$ROOT/$path" ]]; then
      mkdir -p "$TMP_STUDENT/$path"
      copy_tree "$ROOT/$path/" "$TMP_STUDENT/$path/"
    else
      mkdir -p "$TMP_STUDENT/$(dirname "$path")"
      cp "$ROOT/$path" "$TMP_STUDENT/$path"
    fi
  fi
done

rm -rf "$TMP_STUDENT/assessments/answer-keys" \
       "$TMP_STUDENT/instructor" \
       "$TMP_STUDENT/capstone/reference-architecture" \
       "$TMP_STUDENT/automation" \
       "$TMP_STUDENT/packages"
prune_tf "$TMP_STUDENT"
zip_dir "$TMP_STUDENT" "$OUT/student-course.zip"

# --- Instructor package ---
echo "--> instructor-course.zip"
TMP_INSTRUCTOR="$(mktemp -d)"
for path in \
  README.md \
  INSTRUCTOR_START_HERE.md \
  COURSE_MANIFEST.json \
  COURSE_BUILD_PLAN.md \
  instructor \
  assessments \
  modules \
  labs \
  slides \
  course-specification \
  capstone \
  infrastructure \
  qa \
  automation
do
  if [[ -e "$ROOT/$path" ]]; then
    if [[ -d "$ROOT/$path" ]]; then
      mkdir -p "$TMP_INSTRUCTOR/$path"
      copy_tree "$ROOT/$path/" "$TMP_INSTRUCTOR/$path/"
    else
      mkdir -p "$TMP_INSTRUCTOR/$(dirname "$path")"
      cp "$ROOT/$path" "$TMP_INSTRUCTOR/$path"
    fi
  fi
done
prune_tf "$TMP_INSTRUCTOR"
zip_dir "$TMP_INSTRUCTOR" "$OUT/instructor-course.zip"

# --- AWS labs package ---
echo "--> aws-labs.zip"
TMP_AWS="$(mktemp -d)"
mkdir -p "$TMP_AWS/labs" "$TMP_AWS/infrastructure"
if [[ -d "$ROOT/infrastructure" ]]; then
  copy_tree "$ROOT/infrastructure/" "$TMP_AWS/infrastructure/"
fi
for lab in lab-05-cloud-platform-foundation lab-06-integration-platform lab-07-security-resilience lab-08-ai-decision-assistant; do
  if [[ -d "$ROOT/labs/$lab" ]]; then
    copy_tree "$ROOT/labs/$lab/" "$TMP_AWS/labs/$lab/"
  fi
done
find "$TMP_AWS" -type d -name 'reference-solutions' -prune -exec rm -rf {} + 2>/dev/null || true
prune_tf "$TMP_AWS"
zip_dir "$TMP_AWS" "$OUT/aws-labs.zip"

# --- Capstone package ---
echo "--> capstone.zip"
TMP_CAP="$(mktemp -d)"
copy_tree "$ROOT/capstone/" "$TMP_CAP/capstone/"
mkdir -p "$TMP_CAP/student/templates" "$TMP_CAP/student/datasets" "$TMP_CAP/labs"
if [[ -f "$ROOT/student/templates/25-executive-presentation-outline.md" ]]; then
  cp "$ROOT/student/templates/25-executive-presentation-outline.md" "$TMP_CAP/student/templates/"
fi
if [[ -f "$ROOT/student/datasets/northstar-application-inventory.csv" ]]; then
  cp "$ROOT/student/datasets/northstar-application-inventory.csv" "$TMP_CAP/student/datasets/"
fi
if [[ -d "$ROOT/labs/lab-10-capstone" ]]; then
  copy_tree "$ROOT/labs/lab-10-capstone/" "$TMP_CAP/labs/lab-10-capstone/"
fi
zip_dir "$TMP_CAP" "$OUT/capstone.zip"

# --- BayLearn seed package ---
echo "--> baylearn-seed.zip"
TMP_SEED="$(mktemp -d)"
copy_tree "$ROOT/baylearn-seed/" "$TMP_SEED/baylearn-seed/"
zip_dir "$TMP_SEED" "$OUT/baylearn-seed.zip"

echo "==> Done"
ls -lh "$OUT"/*.zip
