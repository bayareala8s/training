# ADR-0002: Content Structure

## Status

Accepted

## Date

2026-07-24

## Context

The curriculum spans 32 domains from computer architecture to mock interviews. Content must be navigable, ordered, and extensible.

## Decision Drivers

- Logical learning progression from foundations to advanced topics
- Numbered directories for stable ordering
- Separation of concerns (docs, labs, case studies, interview)
- Progress tracking integration

## Considered Options

1. **Numbered domain directories** (`docs/04-distributed-systems-foundations/`)
2. **Flat tag-based structure** (single docs folder with tags)
3. **Monorepo packages per domain**

## Decision Outcome

Chosen option: **Numbered domain directories**, because they provide stable ordering, clear navigation in Docusaurus sidebars, and align with the curriculum specification.

### Positive Consequences

- Predictable file locations
- Sidebar maps directly to curriculum
- Easy to identify prerequisites by domain number

### Negative Consequences

- Renumbering is disruptive if domains are reordered
- Long directory names

## Links

- `progress/curriculum.yaml`
- `sidebars.ts`
