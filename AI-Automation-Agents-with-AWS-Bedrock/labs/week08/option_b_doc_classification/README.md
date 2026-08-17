# Option B — Document Classification & Routing Platform

**Status:** Implemented · API + validation + queues + source metadata + audit

**Problem:** Automate document ingestion classification and routing.

## Implemented flow

1. Accept `document_text` (or `text`) plus optional `source_uri` / `content_type` / `doc_type_hint` (S3-style metadata)
2. Bedrock JSON classify → `doc_type` + confidence
3. Deterministic validation + confidence gate
4. Route to queue (`queue_invoices`, `queue_contracts`, … or `human_review`)
5. Notify stub when needs review
6. Persist + audit

## API

```bash
curl -sS -X POST "$API_ENDPOINT/capstone/document" \
  -H "Content-Type: application/json" \
  -d @week08/samples/document_invoice.json | python3 -m json.tool
```

## Demo

```bash
./week08/option_b_doc_classification/demo.sh
```

Samples: `document_invoice.json`, `document_contract.json`, `document_unknown.json`

## Portfolio extensions

- S3 upload bucket + ObjectCreated → Lambda
- Textract for scanned PDFs
- Per-queue DLQs
