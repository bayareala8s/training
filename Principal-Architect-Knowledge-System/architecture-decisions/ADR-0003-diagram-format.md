# ADR-0003: Diagram Format

## Status

Accepted

## Date

2026-07-24

## Context

Architecture content requires diagrams for component views, sequence flows, state machines, and failure domains.

## Decision Drivers

- Text-maintainable diagrams in version control
- CI validation capability
- Renders in Docusaurus without external tools
- Support for complex diagrams when Mermaid is insufficient

## Considered Options

1. **Mermaid primary, Draw.io/Excalidraw secondary**
2. **PlantUML only**
3. **Image-only diagrams** (PNG/SVG exports)

## Decision Outcome

Chosen option: **Mermaid primary, Draw.io/Excalidraw secondary**, because Mermaid integrates natively with Docusaurus and supports CI validation, while Draw.io and Excalidraw handle complex architecture diagrams that Mermaid cannot express cleanly.

### Positive Consequences

- Diagrams live alongside content in Git
- Mermaid renders in docs site and can be validated in CI
- Complex diagrams stored in `diagrams/drawio/` and `diagrams/excalidraw/`

### Negative Consequences

- Mermaid has layout limitations for large diagrams
- Draw.io/Excalidraw require manual export for embedding

## Links

- `.cursor/rules/diagrams.mdc`
- `diagrams/` directory structure
