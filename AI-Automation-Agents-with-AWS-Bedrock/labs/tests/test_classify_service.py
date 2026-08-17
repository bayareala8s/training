import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from week03.classify_service import classify_text


def test_classify_mock_mode():
    out = classify_text("invoice issue", correlation_id="test-1", use_bedrock=False)
    assert out["correlation_id"] == "test-1"
    assert out["result"]["label"] == "unknown"
