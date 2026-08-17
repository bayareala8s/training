# Diagram Library

Canonical Mermaid diagram sources for the Principal Architect Knowledge System.

## Structure

```text
diagrams/
├── mermaid/          # Source-of-truth Mermaid (.mmd) files
│   ├── distributed-systems/
│   ├── consensus/
│   ├── replication/
│   ├── consistency/
│   ├── system-design/
│   └── reference/
├── source/           # Editable source files (optional)
├── generated/        # Build outputs (PNG/SVG exports)
├── drawio/           # Complex architecture (Draw.io)
└── excalidraw/       # Whiteboard-style diagrams
```

## Usage

- **In chapters:** Mermaid blocks are embedded directly in `docs/**/*.md` for Docusaurus rendering.
- **Canonical copies:** Key diagrams are duplicated in `diagrams/mermaid/` for reuse, validation, and export.
- **Validation:** Run `make validate-diagrams` or `python3 scripts/validate_mermaid.py`.

## Diagram Standards

Per `.cursor/rules/diagrams.mdc`:

1. Every diagram has a **title** and **explanation** below it
2. Name all important components
3. Show direction and data flow clearly
4. Identify failure or trust boundaries where relevant
5. Prefer Mermaid for text-maintainable diagrams

## Required Counts

| Content type | Minimum diagrams |
|--------------|------------------|
| Curriculum chapters | 3 (2 architecture + 1 sequence) |
| Case studies | 2 |
| Domain overviews | 1 |
| Labs (architecture.md) | 2 |

## Catalog

See `diagrams/catalog.yaml` for the full index of canonical diagrams.

## Export (optional)

```bash
# Mermaid → SVG (requires @mermaid-js/mermaid-cli)
mmdc -i diagrams/mermaid/consensus/raft-states.mmd -o diagrams/generated/raft-states.svg

# AWS Architecture Icons PNGs — Stripe payment idempotency (18 slides)
make generate-stripe-aws-pngs
# Output: static/img/aws-architecture/stripe-payment-idempotency/*.png
```
