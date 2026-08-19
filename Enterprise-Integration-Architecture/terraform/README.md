# Terraform labs and capstones

Each folder under `terraform/labs/` and `terraform/capstones/` is an independent stack.

```bash
./scripts/lab_up.sh lab-02-api
python3 scripts/validate_lab.py lab-02-api
./scripts/lab_down.sh lab-02-api
```

Capstones use the same scripts (`banking`, `ecommerce`, `healthcare`, `manufacturing`).

**Cost:** Prefer destroy after each session. Lab 6 Transfer Family is **off** by default (`enable_transfer_family=false`) because ONLINE endpoint hours dominate cost. Do not keep unused Transfer servers.

`python3 scripts/validate_lab.py` is a real PASS/FAIL against the deployed stack (HTTP, SQS, SNS, EventBridge, S3, DynamoDB, IAM). It will **FAIL** Lab 12 while `insecure=true`.
