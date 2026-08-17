#!/usr/bin/env python3
"""Generate synthetic banking sample data for the regulatory capstone.

Produces ~50 transactions (with intentional bad records), ~20 settlements,
and ~15 accounts under sample-data/.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sample-data"
RNG = random.Random(42)

CURRENCIES = ["USD", "EUR", "GBP", "CAD"]
TXN_TYPES = ["wire", "ach", "card", "internal"]
TXN_STATUSES = ["posted", "pending", "reversed", "settled"]
CHANNELS = ["online", "branch", "atm", "mobile", "api"]
SETTLE_STATUSES = ["completed", "pending", "failed", "reconciled"]
ACCOUNT_TYPES = ["checking", "savings", "money_market", "brokerage"]
ACCOUNT_STATUSES = ["active", "dormant", "closed", "frozen"]
RISK_TIERS = ["low", "standard", "elevated", "high"]
NAMES = [
    "Ava Chen", "Marcus Webb", "Priya Nair", "Jonah Hale", "Elena Rossi",
    "Devon Park", "Sofia Mendes", "Liam Okafor", "Nora Blake", "Kai Tanaka",
    "Amelia Cruz", "Owen Briggs", "Hana Kim", "Felix Ortega", "Maya Patel",
]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def generate_accounts(n: int = 15) -> list[dict]:
    accounts = []
    for i in range(1, n + 1):
        accounts.append(
            {
                "account_id": f"ACC-{i:06d}",
                "customer_name": NAMES[i - 1],
                "account_type": ACCOUNT_TYPES[(i - 1) % len(ACCOUNT_TYPES)],
                "status": "active" if i <= 12 else ACCOUNT_STATUSES[(i - 1) % 4],
                "currency": CURRENCIES[(i - 1) % len(CURRENCIES)],
                "balance": round(RNG.uniform(-200, 250000), 2) if i != 14 else round(RNG.uniform(1000, 50000), 2),
                "opened_date": f"201{RNG.randint(5, 9)}-{RNG.randint(1, 12):02d}-{RNG.randint(1, 28):02d}",
                "branch_code": f"BR{RNG.randint(100, 999)}",
                "risk_tier": RISK_TIERS[(i - 1) % len(RISK_TIERS)],
            }
        )
    # Intentional bad records for quarantine demo
    accounts[12] = {
        **accounts[12],
        "account_id": "BAD-ACC",  # fails regex
        "balance": "not-a-number",  # fails range
    }
    accounts[13] = {
        **accounts[13],
        "customer_name": "",  # fails not_null
        "account_type": "crypto",  # fails enum
        "status": "active",
    }
    return accounts


def generate_settlements(n: int = 20) -> list[dict]:
    settlements = []
    dates = ["2024-01-14", "2024-01-15", "2024-01-16"]
    for i in range(1, n + 1):
        date = dates[(i - 1) % len(dates)]
        ymd = date.replace("-", "")
        gross = round(RNG.uniform(5000, 850000), 2)
        fee = round(gross * RNG.uniform(0.001, 0.015), 2)
        settlements.append(
            {
                "settlement_id": f"STL-{ymd}-{i:04X}",
                "settlement_date": date,
                "currency": CURRENCIES[(i - 1) % len(CURRENCIES)],
                "status": SETTLE_STATUSES[(i - 1) % len(SETTLE_STATUSES)],
                "gross_amount": gross,
                "net_amount": round(gross - fee, 2),
                "fee_amount": fee,
                "clearing_house": RNG.choice(["CHIPS", "Fedwire", "SEPA", "LYNX"]),
                "batch_id": f"BATCH-{ymd}-{((i - 1) // 5) + 1:02d}",
            }
        )
    # Bad records
    settlements[17] = {
        **settlements[17],
        "settlement_id": "SETTLE-BAD",  # regex fail
        "gross_amount": -100,  # range fail
    }
    settlements[18] = {
        **settlements[18],
        "settlement_date": "",  # not_null fail
        "status": "unknown",  # enum fail
        "currency": "USD",
    }
    return settlements


def generate_transactions(accounts: list[dict], settlements: list[dict], n: int = 50) -> list[dict]:
    good_accounts = [
        a
        for a in accounts
        if str(a["account_id"]).startswith("ACC-") and a.get("customer_name")
    ]
    # Exclude intentionally invalid settlements so good txns keep valid dates/IDs
    good_settlements = [
        s
        for s in settlements
        if str(s["settlement_id"]).startswith("STL-")
        and s.get("settlement_date")
        and s.get("status") in SETTLE_STATUSES
        and float(s.get("gross_amount", 0)) > 0
    ]
    transactions = []
    for i in range(1, n + 1):
        settle = good_settlements[(i - 1) % len(good_settlements)]
        acct = good_accounts[(i - 1) % len(good_accounts)]
        date = settle["settlement_date"]
        ymd = date.replace("-", "")
        transactions.append(
            {
                "transaction_id": f"TXN-{ymd}-{i:04d}",
                "account_id": acct["account_id"],
                "settlement_id": settle["settlement_id"],
                "amount": round(RNG.uniform(5, 75000), 2),
                "currency": settle["currency"],
                "status": TXN_STATUSES[(i - 1) % len(TXN_STATUSES)],
                "transaction_type": TXN_TYPES[(i - 1) % len(TXN_TYPES)],
                "settlement_date": date,
                "channel": CHANNELS[(i - 1) % len(CHANNELS)],
                "memo": f"Synthetic payment {i}",
            }
        )
    # 5 intentional bad records
    transactions[45] = {
        **transactions[45],
        "transaction_id": "TX-BAD-1",  # regex
        "amount": -50,  # range
    }
    transactions[46] = {
        **transactions[46],
        "account_id": "",  # not_null
        "currency": "JPY",  # enum
    }
    transactions[47] = {
        **transactions[47],
        "status": "hacked",  # enum
        "settlement_date": "01/15/2024",  # regex date
    }
    transactions[48] = {
        **transactions[48],
        "transaction_id": "",  # not_null
        "amount": 99999999,  # range max
    }
    transactions[49] = {
        **transactions[49],
        "transaction_id": "TXN-20240115-9999",
        "currency": "XXX",  # enum
        "status": "posted",
    }
    return transactions


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    accounts = generate_accounts(15)
    settlements = generate_settlements(20)
    transactions = generate_transactions(accounts, settlements, 50)

    (OUT / "accounts.json").write_text(json.dumps(accounts, indent=2), encoding="utf-8")
    write_csv(OUT / "settlements.csv", settlements)
    write_csv(OUT / "transactions.csv", transactions)

    print(f"Wrote {len(accounts)} accounts → {OUT / 'accounts.json'}")
    print(f"Wrote {len(settlements)} settlements → {OUT / 'settlements.csv'}")
    print(f"Wrote {len(transactions)} transactions → {OUT / 'transactions.csv'}")
    print("Included intentional bad records for quarantine demo.")


if __name__ == "__main__":
    main()
