"""Unit tests for Lab 3 S3 processor logic."""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
HANDLER_PATH = ROOT / "app" / "lambdas" / "s3_processor" / "handler.py"


def load_handler():
    spec = importlib.util.spec_from_file_location("s3_processor_handler", HANDLER_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["s3_processor_handler"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def handler_module():
    with patch.dict(os.environ, {"IDEMPOTENCY_TABLE": "test-table", "INBOUND_PREFIX": "partners/demo/inbound/"}):
        yield load_handler()


def test_route_inbound_to_processing(handler_module):
    handler_module.s3 = MagicMock()
    dest = handler_module._route("bucket", "partners/demo/inbound/file.csv", "processing")
    assert dest == "partners/demo/processing/file.csv"
    handler_module.s3.copy_object.assert_called_once()


def test_route_quarantine(handler_module):
    handler_module.s3 = MagicMock()
    dest = handler_module._route("bucket", "partners/demo/inbound/bad.exe", "quarantine")
    assert dest == "partners/demo/quarantine/bad.exe"


def test_validation_accepts_csv_extension(handler_module):
    ext = os.path.splitext("partners/demo/inbound/a.CSV")[1].lower()
    assert ext in handler_module.ALLOWED


def test_validation_rejects_exe(handler_module):
    ext = os.path.splitext("partners/demo/inbound/a.exe")[1].lower()
    assert ext not in handler_module.ALLOWED
