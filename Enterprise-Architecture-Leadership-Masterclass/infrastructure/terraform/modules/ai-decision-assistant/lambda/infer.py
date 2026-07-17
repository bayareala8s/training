"""Infer Lambda — Bedrock or deterministic mock classifier for Lab 08."""
from __future__ import annotations

import json
import os
import re
import time
from decimal import Decimal
from typing import Any

import boto3

MODE = os.environ.get("USE_MOCK_BEDROCK", "true").lower()
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "")
METRIC_NAMESPACE = os.environ.get("METRIC_NAMESPACE", "BayLearn/Lab08")
PROMPT_BUCKET = os.environ.get("PROMPT_BUCKET", "")
GUARDRAIL_ID = os.environ.get("GUARDRAIL_ID", "")
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "")

cw = boto3.client("cloudwatch")
bedrock = boto3.client("bedrock-runtime")
s3 = boto3.client("s3")

SYSTEM_PROMPT = """You are NorthStar Financial Services (fictional) incident triage assistant.
Return ONLY valid JSON with keys:
category, severity, business_impact, routing_team, next_actions, hitl_required, confidence, rationale.
severity must be one of: low, medium, high, critical.
next_actions must be an array of short strings.
Do not invent real customer PII. hitl_required should be true for high/critical or security issues.
"""


def _put_metrics(inp_tokens: int, out_tokens: int, estimated_cost: float, mode: str) -> None:
    cw.put_metric_data(
        Namespace=METRIC_NAMESPACE,
        MetricData=[
            {
                "MetricName": "InputTokens",
                "Value": float(inp_tokens),
                "Unit": "Count",
                "Dimensions": [{"Name": "Mode", "Value": mode}],
            },
            {
                "MetricName": "OutputTokens",
                "Value": float(out_tokens),
                "Unit": "Count",
                "Dimensions": [{"Name": "Mode", "Value": mode}],
            },
            {
                "MetricName": "EstimatedCostUsd",
                "Value": float(estimated_cost),
                "Unit": "None",
                "Dimensions": [{"Name": "Mode", "Value": mode}],
            },
        ],
    )


def _mock_classify(text: str) -> dict[str, Any]:
    t = text.lower()
    category = "noise"
    severity = "low"
    team = "platform-sre"
    impact = "Limited operational impact"
    confidence = 0.55
    actions = ["Triage in backlog", "Confirm customer impact"]

    if any(k in t for k in ("phish", "credential", "waf", "delete burst", "security")):
        category, severity, team = "security", "high", "security-ir"
        impact = "Potential security control failure or account risk"
        confidence = 0.8
        actions = ["Page security IR", "Preserve logs", "Disable suspected credentials if confirmed"]
    if any(k in t for k in ("payment", "checkout", "wire transfer", "authorization api", "fx rate")):
        category = "availability" if "fx" not in t else "data_integrity"
        if "fx" in t or "incorrect" in t:
            category, severity, team = "data_integrity", "critical", "payments-risk"
            impact = "Financial integrity risk"
        else:
            severity = "critical" if any(k in t for k in ("critical", "backing up", "flash sale", "failing")) else "high"
            team = "payments-sre"
            impact = "Customer payments or checkout impacted"
        confidence = 0.85
        actions = ["Page payments on-call", "Check error budgets", "Communicate to business ops"]
    if "settlement file" in t or "partner" in t and "file" in t:
        category, severity, team = "data_quality", "medium", "partner-integrations"
        impact = "Settlement reconciliation may slip"
        confidence = 0.75
        actions = ["Contact partner", "Check landing bucket", "Re-run intake job"]
    if "throttle" in t or "dynamodb" in t:
        category, severity, team = "availability", "critical", "platform-sre"
        impact = "Session/checkout failures; revenue impact"
        confidence = 0.9
    if "assistant suggested closing" in t or "ai " in t:
        category, severity, team = "ai_governance", "high", "architecture-gov"
        impact = "Unsafe automation behavior"
        confidence = 0.7
        actions = ["Disable auto-close", "Open architecture review", "Add HITL control"]
    if "marketing" in t or "analytics dashboard" in t or "ci pipeline" in t:
        category, severity, team = ("batch_failure" if "batch" in t or "marketing" in t else "delivery"), "low", (
            "data-platform" if "marketing" in t else "mobile-platform" if "ci" in t else "bi-support"
        )
        impact = "Internal delivery or reporting delay"
        confidence = 0.65
        actions = ["Assign owner", "Schedule fix"]
    if "finops" in t or "left running" in t or "cost" in t:
        category, severity, team = "cost", "low", "cloud-finops"
        impact = "Sandbox cost overrun risk"
        confidence = 0.7
    if "certificate" in t:
        category, severity, team = "compliance", "medium", "platform-sre"
        impact = "Future outage if untreated"
        confidence = 0.7
    if "schema mismatch" in t or "step functions execution timeout" in t or "onboarding" in t:
        category, severity, team = "integration", "medium", (
            "digital-onboarding" if "onboarding" in t or "timeout" in t else "partner-integrations"
        )
        impact = "Journey or partner friction"
        confidence = 0.7
    if "sms provider" in t:
        category, severity, team = "availability", "medium", "customer-ops"
        impact = "OTP delays for some customers"
        confidence = 0.75
        actions = ["Confirm email fallback", "Status page update", "Provider ticket"]
    if "golden-record" in t or "duplicate customer" in t:
        category, severity, team = "data_integrity", "high", "data-governance"
        impact = "Customer statement errors"
        confidence = 0.8
        actions = ["Stop merges", "Data stewardship review", "Customer comms plan"]
    if "canary" in t and "flapping" in t:
        category, severity, team = "noise", "low", "platform-sre"
        impact = "Minimal customer impact"
        confidence = 0.6

    hitl = severity in ("high", "critical") or category in ("security", "ai_governance", "data_integrity")
    return {
        "category": category,
        "severity": severity,
        "business_impact": impact,
        "routing_team": team,
        "next_actions": actions,
        "hitl_required": hitl,
        "confidence": confidence,
        "rationale": "Deterministic mock classifier for BayLearn lab (fictional NorthStar).",
        "mode": "mock",
    }


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _bedrock_classify(incident_text: str) -> tuple[dict[str, Any], int, int, float]:
    user = f"Incident narrative:\n{incident_text}\n\nRespond with JSON only."
    body: dict[str, Any] = {
        "messages": [
            {"role": "user", "content": [{"text": SYSTEM_PROMPT + "\n\n" + user}]}
        ],
        "inferenceConfig": {"maxTokens": 512, "temperature": 0},
    }
    kwargs: dict[str, Any] = {
        "modelId": MODEL_ID,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps(body),
    }
    # Converse API preferred when available; fall back to invoke_model shapes vary by model.
    # Using converse for Nova / Anthropic on Bedrock.
    try:
        converse_args: dict[str, Any] = {
            "modelId": MODEL_ID,
            "messages": [{"role": "user", "content": [{"text": SYSTEM_PROMPT + "\n\n" + user}]}],
            "inferenceConfig": {"maxTokens": 512, "temperature": 0},
        }
        if GUARDRAIL_ID:
            converse_args["guardrailConfig"] = {
                "guardrailIdentifier": GUARDRAIL_ID,
                "guardrailVersion": GUARDRAIL_VERSION or "DRAFT",
            }
        resp = bedrock.converse(**converse_args)
        parts = resp.get("output", {}).get("message", {}).get("content", [])
        text = "".join(p.get("text", "") for p in parts if "text" in p)
        usage = resp.get("usage", {})
        inp = int(usage.get("inputTokens", 0))
        out = int(usage.get("outputTokens", 0))
        # Rough instructional estimate only — not billing truth
        estimated = (inp + out) * 0.0000002
        data = _extract_json(text)
        data["mode"] = "bedrock"
        return data, inp, out, estimated
    except Exception as exc:  # noqa: BLE001 — surface to Step Functions
        raise RuntimeError(
            f"Bedrock inference failed ({exc}). Enable model access or set USE_MOCK_BEDROCK=true."
        ) from exc


def handler(event, context):
    incident_id = event.get("incident_id", "UNKNOWN")
    incident_text = event.get("incident_text", "")
    if not incident_text:
        raise ValueError("incident_text is required")

    mode = "mock" if MODE in ("1", "true", "yes") else "bedrock"
    t0 = time.time()

    if mode == "mock":
        decision = _mock_classify(incident_text)
        inp_tokens, out_tokens, cost = 0, 0, 0.0
    else:
        decision, inp_tokens, out_tokens, cost = _bedrock_classify(incident_text)

    _put_metrics(inp_tokens, out_tokens, cost, mode)

    if PROMPT_BUCKET:
        key = f"safe-logs/{incident_id}/{int(time.time())}.json"
        safe = {
            "incident_id": incident_id,
            "text_sha11": str(abs(hash(incident_text)) % 10_000_000_000),
            "text_length": len(incident_text),
            "mode": mode,
            "model_id": MODEL_ID if mode == "bedrock" else "mock",
            "input_tokens": inp_tokens,
            "output_tokens": out_tokens,
            "estimated_cost_usd": cost,
            "note": "Redacted safe log — fictional NorthStar lab; raw text not stored",
        }
        s3.put_object(
            Bucket=PROMPT_BUCKET,
            Key=key,
            Body=json.dumps(safe).encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )

    return {
        "incident_id": incident_id,
        "incident_text": incident_text,
        "decision": decision,
        "metrics": {
            "input_tokens": inp_tokens,
            "output_tokens": out_tokens,
            "estimated_cost_usd": cost,
            "latency_ms": int((time.time() - t0) * 1000),
            "mode": mode,
        },
    }
