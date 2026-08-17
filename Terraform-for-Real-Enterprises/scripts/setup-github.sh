#!/usr/bin/env bash
# Create GitHub repository and push (run after: gh auth login)
set -euo pipefail

# Course is published under bayareala8s/training (monorepo).
# Run from repository root after cloning training.

TRAINING_REPO="${TRAINING_REPO:-https://github.com/bayareala8s/training.git}"
COURSE_PATH="Terraform-for-Real-Enterprises"

echo "This course is part of: ${TRAINING_REPO}"
echo "Path: ${COURSE_PATH}"
echo ""
echo "To contribute:"
echo "  git clone ${TRAINING_REPO}"
echo "  cd training/${COURSE_PATH}"
echo "  # make changes, commit from repo root, push to main"
