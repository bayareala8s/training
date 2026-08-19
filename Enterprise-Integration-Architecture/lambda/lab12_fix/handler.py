"""Placeholder processor used by the security lab."""
def lambda_handler(event, _ctx):
    return {"ok": True, "note": "Tighten IAM in Terraform until validate_lab.py PASSes."}
