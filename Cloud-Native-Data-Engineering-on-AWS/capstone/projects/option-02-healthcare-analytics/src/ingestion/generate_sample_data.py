#!/usr/bin/env python3
"""Generate SYNTHETIC healthcare sample data (fake names/IDs only).

Produces ~30 patients (with bad records), ~40 appointments, ~50 lab results.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sample-data"
RNG = random.Random(7)

FIRST = [
    "Jordan", "Riley", "Casey", "Avery", "Quinn", "Morgan", "Reese", "Skyler",
    "Taylor", "Cameron", "Harper", "Rowan", "Parker", "Finley", "Hayden",
]
LAST = [
    "Nguyen", "Brooks", "Silva", "Anders", "Kline", "Okoye", "Diaz", "Singh",
    "Murphy", "Sato", "Ali", "Cohen", "Garcia", "Ivanov", "Walsh",
]
STATES = ["CA", "TX", "NY", "FL", "WA", "IL", "MA", "CO"]
PLANS = ["Aetna-PPO", "UHC-HMO", "BCBS-EPO", "Medicare-Adv", "Medicaid-MCO", "Self-Pay"]
DEPARTMENTS = [
    "cardiology", "oncology", "pediatrics", "orthopedics", "primary_care", "radiology",
]
APT_STATUSES = ["scheduled", "completed", "cancelled", "no_show"]
TEST_CODES = ["CBC", "BMP", "LIPID", "A1C", "TSH", "COVID_PCR"]
FLAGS = ["normal", "high", "low", "critical"]
UNITS = {
    "CBC": "K/uL",
    "BMP": "mg/dL",
    "LIPID": "mg/dL",
    "A1C": "%",
    "TSH": "mIU/L",
    "COVID_PCR": "Ct",
}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def fake_ssn(i: int) -> str:
    return f"{100 + (i % 899):03d}-{10 + (i % 89):02d}-{1000 + (i * 37) % 9000:04d}"


def generate_patients(n: int = 30) -> list[dict]:
    patients = []
    for i in range(1, n + 1):
        first = FIRST[(i - 1) % len(FIRST)]
        last = LAST[(i - 1) % len(LAST)]
        patients.append(
            {
                "patient_id": f"PAT-{i:06d}",
                "first_name": first,
                "last_name": last,
                "age": RNG.randint(1, 95),
                "sex": RNG.choice(["F", "M", "X", "U"]),
                "ssn": fake_ssn(i),
                "email": f"{first.lower()}.{last.lower()}{i}@example.com",
                "state": STATES[(i - 1) % len(STATES)],
                "insurance_plan": PLANS[(i - 1) % len(PLANS)],
            }
        )
    # Intentional bad records (~4)
    patients[26] = {
        **patients[26],
        "patient_id": "P-26",  # regex fail
        "ssn": "123456789",  # regex fail
    }
    patients[27] = {
        **patients[27],
        "last_name": "",  # not_null
        "age": 200,  # range
    }
    patients[28] = {
        **patients[28],
        "email": "not-an-email",  # regex
        "sex": "Z",  # enum
    }
    patients[29] = {
        **patients[29],
        "patient_id": "",  # not_null
        "ssn": "000-00-0000",
        "email": "ok@example.com",
    }
    return patients


def generate_appointments(patients: list[dict], n: int = 40) -> list[dict]:
    good_patients = [p for p in patients if str(p.get("patient_id", "")).startswith("PAT-")]
    appointments = []
    dates = ["2024-01-12", "2024-01-15", "2024-01-18", "2024-01-22"]
    for i in range(1, n + 1):
        date = dates[(i - 1) % len(dates)]
        ymd = date.replace("-", "")
        appointments.append(
            {
                "appointment_id": f"APT-{ymd}-{i:04d}",
                "patient_id": good_patients[(i - 1) % len(good_patients)]["patient_id"],
                "appointment_date": date,
                "department": DEPARTMENTS[(i - 1) % len(DEPARTMENTS)],
                "status": APT_STATUSES[(i - 1) % len(APT_STATUSES)],
                "duration_minutes": RNG.choice([15, 20, 30, 45, 60, 90]),
                "provider_id": f"PRV-{(i % 12) + 1:03d}",
                "facility": RNG.choice(["North Clinic", "East Pavilion", "Central Hospital"]),
            }
        )
    # Bad records
    appointments[37] = {
        **appointments[37],
        "appointment_id": "APPT-BAD",  # regex
        "duration_minutes": 1,  # range
    }
    appointments[38] = {
        **appointments[38],
        "patient_id": "",  # not_null
        "department": "dermatology",  # enum not allowed
    }
    appointments[39] = {
        **appointments[39],
        "status": "rescheduled",  # enum
        "appointment_date": "15-01-2024",  # regex
    }
    return appointments


def generate_lab_results(patients: list[dict], n: int = 50) -> list[dict]:
    good_patients = [p for p in patients if str(p.get("patient_id", "")).startswith("PAT-")]
    results = []
    dates = ["2024-01-10", "2024-01-15", "2024-01-20"]
    for i in range(1, n + 1):
        date = dates[(i - 1) % len(dates)]
        ymd = date.replace("-", "")
        code = TEST_CODES[(i - 1) % len(TEST_CODES)]
        results.append(
            {
                "result_id": f"LAB-{ymd}-{i:04d}",
                "patient_id": good_patients[(i - 1) % len(good_patients)]["patient_id"],
                "test_code": code,
                "numeric_value": round(RNG.uniform(0.5, 400), 3),
                "unit": UNITS[code],
                "result_flag": FLAGS[(i - 1) % len(FLAGS)],
                "collected_date": date,
                "ordering_dept": DEPARTMENTS[(i - 1) % len(DEPARTMENTS)],
            }
        )
    # Bad records
    results[47] = {
        **results[47],
        "result_id": "LABBAD",  # regex
        "numeric_value": -5,  # range
    }
    results[48] = {
        **results[48],
        "patient_id": "",  # not_null
        "test_code": "MRI",  # enum
    }
    results[49] = {
        **results[49],
        "result_flag": "panic",  # enum
        "collected_date": "2024/01/15",  # regex
    }
    return results


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    patients = generate_patients(30)
    appointments = generate_appointments(patients, 40)
    lab_results = generate_lab_results(patients, 50)

    write_csv(OUT / "patients.csv", patients)
    write_csv(OUT / "appointments.csv", appointments)
    (OUT / "lab_results.json").write_text(json.dumps(lab_results, indent=2), encoding="utf-8")

    print(f"Wrote {len(patients)} patients → {OUT / 'patients.csv'}")
    print(f"Wrote {len(appointments)} appointments → {OUT / 'appointments.csv'}")
    print(f"Wrote {len(lab_results)} lab_results → {OUT / 'lab_results.json'}")
    print("SYNTHETIC data only. Included intentional bad records for quarantine demo.")


if __name__ == "__main__":
    main()
