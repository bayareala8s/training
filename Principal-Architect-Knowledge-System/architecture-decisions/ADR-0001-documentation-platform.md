# ADR-0001: Documentation Platform

## Status

Accepted

## Date

2026-07-24

## Context

The Principal Architect Knowledge System requires a documentation platform that supports long-form technical content, Mermaid diagrams, full-text search, and automated CI validation.

## Decision Drivers

- Rich Markdown and MDX support for interactive content
- Mermaid diagram rendering
- Strong ecosystem for technical documentation
- TypeScript and React for future customization
- Local full-text search without external dependencies initially

## Considered Options

1. **Docusaurus** (TypeScript, React, Mermaid plugin)
2. **MkDocs Material** (Python, simpler setup)
3. **Custom static site** (maximum control, high maintenance)

## Decision Outcome

Chosen option: **Docusaurus**, because it provides the best balance of Markdown authoring, Mermaid integration, React extensibility, and community support for technical documentation sites.

### Positive Consequences

- Native Mermaid support via `@docusaurus/theme-mermaid`
- Sidebar navigation maps well to curriculum structure
- GitHub Pages deployment is straightforward
- MDX enables future interactive components

### Negative Consequences

- Node.js dependency for builds
- Heavier than MkDocs for simple Markdown-only sites
- Custom routing requires careful configuration

## Links

- [Docusaurus documentation](https://docusaurus.io/)
- Supersedes: N/A (initial ADR)
