# Banking capstone Terraform

Working slice: payments API, SQS posting, S3 file catalog, HITL reprocess.

```bash
./scripts/lab_up.sh banking
python3 scripts/validate_lab.py banking
./scripts/lab_down.sh banking
```

ADRs in `capstones/banking/` remain the source of truth for the full platform design.
