import os

# Override via environment or SAM template
AWS_REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
# Default: Amazon Nova Lite (Converse API). Override if your account uses another active model.
BEDROCK_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
MAX_INPUT_CHARS = int(os.environ.get("MAX_INPUT_CHARS", "8000"))
MAX_OUTPUT_TOKENS = int(os.environ.get("MAX_OUTPUT_TOKENS", "512"))
DEFAULT_TEMPERATURE = float(os.environ.get("DEFAULT_TEMPERATURE", "0.2"))
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.65"))
AUDIT_TABLE_NAME = os.environ.get("AUDIT_TABLE_NAME", "")
MEMORY_TABLE_NAME = os.environ.get("MEMORY_TABLE_NAME", "")
RESULTS_TABLE_NAME = os.environ.get("RESULTS_TABLE_NAME", "")

CLASSIFICATION_LABELS = frozenset(
    {"billing", "technical", "security", "general", "unknown"}
)
ROUTE_TARGETS = frozenset(
    {"team_billing", "team_engineering", "team_security", "team_general", "human_review"}
)

# Week 8 capstone — document classification
DOCUMENT_LABELS = frozenset(
    {"invoice", "contract", "hr", "legal", "general", "unknown"}
)
DOCUMENT_QUEUES = frozenset(
    {"queue_invoices", "queue_contracts", "queue_hr", "queue_legal", "queue_general", "human_review"}
)

CAPSTONE_APPROVALS_TABLE = os.environ.get("CAPSTONE_APPROVALS_TABLE", "")
