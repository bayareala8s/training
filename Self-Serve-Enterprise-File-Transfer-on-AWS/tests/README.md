# Tests

## Unit tests (no AWS)

```bash
./scripts/ci_verify.sh
```

Or:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r tests/requirements.txt
pytest tests/unit -v
```

## Integration tests (requires deployed stack)

```bash
./scripts/start_stack.sh --yes
./scripts/test_all_labs.sh
./scripts/stop_stack.sh --yes
```

## Full course validation

```bash
LAB_LARGE_FILE_MB=5 ./scripts/lab_cycle.sh --yes --destroy
```
