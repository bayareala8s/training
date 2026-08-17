# Contributing

Thank you for contributing to the Principal Architect Knowledge System.

## Content Standards

All technical content must:

- Explain the problem, assumptions, mechanism, guarantees, and failure modes
- Include explicit tradeoffs and decision criteria
- Define acronyms on first use
- Include authoritative references
- Follow the chapter template in `templates/chapter-template.md`

Do not invent facts, benchmark numbers, or product capabilities. Mark uncertain claims for verification.

## Workflow

1. Read related existing content before creating new chapters
2. Use templates from `templates/`
3. Add valid YAML frontmatter to all chapters
4. Update `progress/curriculum.yaml` and relevant progress files
5. Run validations before submitting changes

```bash
make validate
make lint
make spell
```

## Pull Request Checklist

- [ ] Metadata is valid
- [ ] Structure matches the appropriate template
- [ ] Internal links work
- [ ] Diagrams render (Mermaid)
- [ ] Interview questions included where required
- [ ] Progress metadata updated
- [ ] Linting passes

## Cursor Rules

Review `.cursor/rules/` before authoring content. Rules cover content authoring, technical accuracy, diagrams, labs, and interview content.

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
