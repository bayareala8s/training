"""Unit tests for Lab 4 validate Lambda logic."""
import importlib.util
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
HANDLER_PATH = ROOT / "app" / "lambdas" / "workflow_validate" / "handler.py"


def load_handler():
    spec = importlib.util.spec_from_file_location("workflow_validate", HANDLER_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["workflow_validate"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_handler_valid_csv():
    with patch.dict(os.environ, {"LANDING_BUCKET": "test-bucket"}):
        mod = load_handler()
        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {"ContentLength": 100}
        mod.s3 = mock_s3
        result = mod.handler(
            {"bucket": "test-bucket", "key": "partners/demo/inbound/x.csv", "correlation_id": "c1"},
            None,
        )
        assert result["valid"] is True
        assert result["reason"] == "ok"


def test_handler_invalid_extension():
    with patch.dict(os.environ, {"LANDING_BUCKET": "test-bucket"}):
        mod = load_handler()
        mock_s3 = MagicMock()
        mock_s3.head_object.return_value = {"ContentLength": 100}
        mod.s3 = mock_s3
        result = mod.handler(
            {"bucket": "test-bucket", "key": "partners/demo/inbound/x.exe", "correlation_id": "c1"},
            None,
        )
        assert result["valid"] is False
