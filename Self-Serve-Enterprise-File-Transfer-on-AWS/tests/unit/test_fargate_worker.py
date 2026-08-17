"""Unit tests for Lab 9 Fargate worker helpers."""
import hashlib
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKER_PATH = ROOT / "app" / "workers" / "fargate" / "worker.py"


def load_worker():
    spec = importlib.util.spec_from_file_location("fargate_worker", WORKER_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fargate_worker"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_sha256_file():
    worker = load_worker()
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"baylearn-test-payload")
        path = f.name
    expected = hashlib.sha256(b"baylearn-test-payload").hexdigest()
    assert worker._sha256_file(path) == expected
