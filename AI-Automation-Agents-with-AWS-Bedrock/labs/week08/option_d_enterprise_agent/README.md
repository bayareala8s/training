# Option D — Enterprise Agent (Internal AI API Platform)

**Status:** Implemented · multi-tool planner + policy + memory + composes A/B/C

**Problem:** Deliver a governed agent that picks tools safely for internal teams.

## Implemented flow

1. Plan tool via Bedrock JSON (or deterministic `tool_hint` for demos)
2. Allow-list enforcement
3. Risky keyword policy → deny unless `approval_request`
4. Execute: `incident_triage` | `doc_classify` | `approval_request` | `summarize` | `classify_route`
5. Session memory in DynamoDB
6. Audit

## Tools

| Tool | Calls |
|------|--------|
| `incident_triage` | Option A service |
| `doc_classify` | Option B service |
| `approval_request` | Option C service |
| `summarize` | Bedrock summary |
| `classify_route` | Week 3 classify + route |

## API

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/agent" \
  -H "Content-Type: application/json" \
  -d @week08/samples/agent_incident.json | python3 -m json.tool
```

## Demo

```bash
./week08/option_d_enterprise_agent/demo.sh
```

Samples: `agent_multiturn.json`, `agent_incident.json`, `agent_risky_deny.json`

## Portfolio extensions

- Per-client rate limits
- Prompt versioning + golden-set eval gate
- Streaming responses
