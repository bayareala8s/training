"""Curated transform for patients – mask SSN and hash email (PHI minimization)."""

from __future__ import annotations

import hashlib


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Produce analytics-safe patient rows with masked SSN and hashed email."""
    curated: list[dict] = []
    for row in records:
        ssn = str(row.get("ssn", ""))
        email = str(row.get("email", "")).strip().lower()
        curated.append(
            {
                "patient_id": row["patient_id"],
                "first_name": row.get("first_name", ""),
                "last_name": row.get("last_name", ""),
                "age": int(float(row["age"])),
                "sex": row["sex"],
                "ssn_masked": _mask_ssn(ssn),
                "email_hash": _hash_email(email),
                "state": row.get("state", ""),
                "insurance_plan": row.get("insurance_plan", ""),
                "processing_date": processing_date,
                "pii_policy": "ssn_masked_last4;email_sha256",
            }
        )
    return curated


def _mask_ssn(ssn: str) -> str:
    digits = "".join(ch for ch in ssn if ch.isdigit())
    last4 = digits[-4:] if len(digits) >= 4 else "XXXX"
    return f"***-**-{last4}"


def _hash_email(email: str) -> str:
    if not email:
        return ""
    return hashlib.sha256(email.encode("utf-8")).hexdigest()
