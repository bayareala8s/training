# Principal Architect Knowledge System

A comprehensive knowledge platform for **Senior Principal Architect**, **Distinguished Engineer**, and **Principal Engineer** interview preparation at technically rigorous companies.

**Author:** Himanshu Bhadra

## Purpose

This system combines:

1. Graduate-level distributed-systems education
2. Production architecture guidance
3. Principal-level system-design preparation
4. Cloud and AI platform architecture
5. Hands-on labs
6. Architecture leadership
7. Company-specific interview preparation
8. Personalized interview stories
9. Flashcards and cheat sheets
10. Progress tracking

## Quick Start

```bash
# Install dependencies
npm install

# Start documentation site locally
npm start

# Run validations
make validate
```

Open [http://localhost:3000](http://localhost:3000) for the homepage. Documentation lives under `/docs`.

### Deploy to AWS (share with students)

```bash
make aws-setup    # one-time: S3 + CloudFront
make aws-deploy   # build and publish

# Optional: branded subdomain (like baylearn.bayareala8s.com)
CUSTOM_DOMAIN=paks.bayareala8s.com HOSTED_ZONE_NAME=bayareala8s.com make aws-domain
make aws-deploy
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for full instructions. Estimated cost: **~$0–1/month** for personal use.

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| `docs/` | Curriculum chapters and learning paths |
| `case-studies/` | Production system deep dives |
| `interview/` | Question banks, company guides, rubrics |
| `labs/` | Hands-on exercises |
| `templates/` | Content authoring templates |
| `progress/` | Curriculum and readiness tracking |
| `scripts/` | Validation and build automation |
| `architecture-decisions/` | Architecture Decision Records (ADRs) |

## Learning Paths

- **12-Week Interview Sprint** — for active applications
- **24-Week Deep Preparation** — two weeks per major domain with labs
- **40-Week Principal Architect Mastery** — comprehensive mastery path

Start with [Welcome](docs/00-start-here/welcome.md) or the [12-Week Learning Path](docs/00-start-here/12-week-learning-path.md).

## Development Commands

```bash
make install      # Install Node and Python dependencies
make start        # Start Docusaurus dev server
make build        # Build documentation site
make aws-setup    # One-time: create S3 + CloudFront stack
make aws-deploy   # Build and deploy to AWS
make aws-domain   # Attach custom domain (e.g. paks.bayareala8s.com)
make lint         # Lint Markdown and TypeScript
make spell        # Run spelling checks
make validate     # Validate metadata, links, and coverage
make ci           # Full CI pipeline locally
```

## Guiding Principles

- **Depth before breadth** — explain problems, mechanisms, guarantees, and failures
- **First-principles reasoning** — avoid shallow definitions
- **Tradeoffs over prescriptions** — no universal best practices
- **Production realism** — connect theory to operations
- **Interview usefulness** — every module includes principal-level questions

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
